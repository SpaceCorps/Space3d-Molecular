# spacemd — simulation input reference

A simulation is one JSON file: the system, the force field, a list of stages (minimize / run
dynamics) and what to write out. Get the `spacemd` command with
`cargo install spacemd-cli --registry spacecorps` or a prebuilt binary (see the
[README](../README.md#install)); use the `spacemd` crate to drive simulations from Rust.

```sh
spacemd example list            # built-in examples
spacemd example argon > argon.json
spacemd run argon.json          # writes thermo.csv, report.json, summary.md, trajectories …
spacemd run argon.json --out results/   # override the output directory (-q: quiet, --threads N)
```

Ready-made inputs: [`examples/md/`](../examples/md). Output format: [md-reports.md](md-reports.md).
Unknown keys are rejected, so typos fail loudly.

## Top level

```jsonc
{
  "title": "Liquid argon",
  "units": "metal",          // "metal" or "lj"
  "seed": 1,                 // master seed: velocities, random gas, Langevin noise
  "system":     { … },
  "potentials": [ … ],
  "neighbor":   { "skin": 1.0 },
  "stages":     [ … ],
  "output":     { … }
}
```

## Units

| quantity | `metal` | `lj` (reduced) |
|---|---|---|
| length | Å | σ |
| energy | eV | ε |
| time | **fs** | τ = σ√(m/ε) |
| mass | amu (g/mol) | m |
| temperature | K | ε/k_B |
| charge | e | reduced |
| force | eV/Å | ε/σ |
| pressure | bar | ε/σ³ |
| electric field | V/Å | reduced |
| mass density | g/cm³ | m/σ³ |

`metal` matches LAMMPS `metal` units except that time is in fs rather than ps.

## System

```jsonc
"system": {
  "types": [{ "name": "Ar", "mass": 39.948, "charge": 0.0 }],
  "structure": { … },                // one of the four forms below
  "periodic": [true, true, true],    // default: fully periodic
  "velocities": { "temperature": 94.4 }   // Maxwell–Boltzmann, zero net momentum
}
```

Structures:

| form | example |
|---|---|
| crystal lattice (`fcc`, `bcc`, `sc`, `diamond`, `rocksalt`) | `{"lattice": {"kind": "fcc", "a": 5.781, "cells": [8, 8, 8], "types": ["Ar"]}}` — `rocksalt` takes `["Na", "Cl"]` |
| random gas | `{"gas": {"box": [40, 40, 40], "counts": [{"type": "Ar", "count": 500}], "min_distance": 3.0}}` |
| water box | `{"water": {"molecules": 512, "density": 1.0, "oxygen": "O", "hydrogen": "H"}}` |
| from file | `{"xyz": {"path": "start.extxyz", "box": [Lx, Ly, Lz]}}` — extended-XYZ `Lattice=` is used when present (triclinic cells supported) |

## Potentials

A list; energies of all entries add up, and every entry reports its own named energy term.

| `type` | form | parameters | reported terms |
|---|---|---|---|
| `lj` | 4ε[(σ/r)¹² − (σ/r)⁶] | `cutoff`, `shift` (`none`/`energy`/`force`), `tail`, `mixing` (`geometric`/`arithmetic`), `precision` (`double`/`mixed`), `pairs: [{types, epsilon, sigma, cutoff?}]` | `lj`, `lj_tail` |
| `morse` | D₀[e^{−2α(r−r₀)} − 2e^{−α(r−r₀)}] | `cutoff`, `shift`, `pairs: [{types, d0, alpha, r0}]` | `morse` |
| `buckingham` | A e^{−r/ρ} − C/r⁶ | `cutoff`, `shift`, `tail`, `pairs: [{types, a, rho, c}]` | `buckingham`, `buckingham_tail` |
| `coulomb_dsf` | damped shifted-force Coulomb (Fennell & Gezelter 2006) | `alpha`, `cutoff`, `exclude_intramolecular` | `coul_dsf` |
| `ewald` | Ewald summation | `cutoff`, `accuracy` | `coul_real`, `coul_recip`, `coul_self` |
| `eam` | embedded-atom method | `{"setfl": "file.eam.alloy", "elements": {"Cu": "Cu"}}`, `{"funcfl": "Cu_u3.eam"}` (LAMMPS formats) or `{"builtin": "johnson_cu"}` | `eam_embed`, `eam_pair` |
| `bonds` | harmonic ½k(r − r₀)² | `kinds: [{k, r0}]` (note the ½: LAMMPS K = k/2) | `bond` |
| `angles` | harmonic ½k(θ − θ₀)² | `kinds: [{k, theta0_deg}]` | `angle` |
| `efield` | uniform field on charges, E(t) = E₀ cos(ωt + φ) | `field: [Ex, Ey, Ez]`, `omega`, `phase` | `efield` |

The built-in `johnson_cu` EAM is a simple nearest-neighbour copper model for demos and tests; for
production work load a published `setfl`/`funcfl` file.

## Neighbor settings

`"neighbor": {"skin": 1.0}` — extra distance beyond the largest cutoff. Larger skins mean fewer
list rebuilds but more pairs per step; 0.3σ (LJ) or 0.5–1 Å (metal) are good defaults.

## Stages

Stages run in order. Each stage either minimizes or runs dynamics.

```jsonc
"stages": [
  { "name": "relax", "minimize": { "ftol": 1e-4, "max_steps": 2000,
                                   "box_relax": { "pressure": 0.0, "ptol": 1.0 } } },
  { "name": "equilibrate", "steps": 4000,
    "velocities": { "temperature": 94.4 },           // optional re-draw at stage start
    "integrator": { "dt": 5.0,
      "thermostat": { "type": "langevin", "temperature": 94.4, "damping": 500.0 } } },
  { "name": "production", "steps": 10000, "record": true, "integrator": { "dt": 5.0 } }
]
```

| key | meaning |
|---|---|
| `minimize` | energy minimization (FIRE); optional `box_relax` also relaxes the cell to a target pressure |
| `steps`, `integrator.dt` | number of steps and time step |
| `integrator.thermostat` | omitted/`none` → NVE · `{"type": "langevin", temperature, damping, seed?}` · `{"type": "nose_hoover", temperature, damping, chain?}` · `{"type": "berendsen", temperature, tau}` |
| `integrator.barostat` | `{"type": "berendsen", "pressure", "tau", "compressibility", "coupling": "isotropic" \| "anisotropic"}` |
| `record` | collect structural/dynamical analysis in this stage (default: the last dynamics stage) |

`damping` and `tau` are relaxation times in time units. Every thermostat and barostat keeps an
account of the energy it exchanges, so a **conserved quantity** is reported in every ensemble.
Berendsen coupling is not canonical; reports flag it.

## Output

```jsonc
"output": {
  "dir": "argon-out",
  "thermo_every": 50,                 // thermo sample interval (steps)
  "print_every": 1000,                // console progress interval
  "trajectory": { "every": 1000, "format": "extxyz" },   // or "xyz"
  "rdf":  { "every": 100, "r_max": 15.0, "bins": 300 },
  "msd":  { "every": 10, "max_lag": 400, "origin_interval": 20 },
  "vacf": { "every": 2,  "max_lag": 400, "origin_interval": 10 },
  "final_xyz": true
}
```

## Examples

| name | system |
|---|---|
| [`argon`](../examples/md/argon.json) | liquid argon at 94.4 K (Rahman 1964): melt → Langevin → NVE; g(r), MSD, VACF |
| [`lj`](../examples/md/lj.json) | LJ fluid at T* = 2.0, ρ* = 0.8 (Johnson et al. 1993 equation-of-state point) |
| [`nacl`](../examples/md/nacl.json) | rock-salt NaCl (Buckingham + DSF Coulomb) relaxed, then heated through melting at constant pressure |
| [`cu`](../examples/md/cu.json) | 4 000-atom copper (EAM): relax, NVT, NPT |
| [`water`](../examples/md/water.json) | 512 flexible SPC/Fw water molecules |
