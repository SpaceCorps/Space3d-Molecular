# spacemd — reports and output files

Every `spacemd run` writes these files to the output directory. A real example from a short
argon run: [`examples/md/sample-output/`](../examples/md/sample-output).

| file | contents |
|---|---|
| `summary.md` | human-readable report: system, then per stage a statistics table of every quantity, energy drift, heat capacity, throughput; then structure and dynamics |
| `report.json` | the same, machine-readable (plus full g(r), MSD and VACF curves) |
| `thermo.csv` | one row per thermo sample |
| `rdf.csv` | r, g(r), and partial g_ab(r) per type pair |
| `msd.csv` | t, mean squared displacement (total and per type) |
| `vacf.csv` | t, velocity autocorrelation C(t) and C(t)/C(0) |
| `trajectory.extxyz` / `.xyz` | frames every `trajectory.every` steps (atoms in a stable order) |
| `final.extxyz` | the final configuration |

## `thermo.csv` columns

`stage, step, time, temperature, kinetic, potential, <one column per energy term>, total,
reservoir, conserved, pressure, pxx, pyy, pzz, pxy, pxz, pyz, volume, density, lx, ly, lz`,
followed by running (per-stage cumulative) averages `avg_temperature, avg_potential, avg_total,
avg_pressure, avg_density`.

- **Energy terms** are named by the potentials (`lj`, `coul_dsf`, `eam_embed`, `eam_pair`, `bond`, …),
  so you always see where the potential energy comes from.
- `reservoir` is the energy exchanged with thermostats/barostats and `conserved` = `total` +
  `reservoir`; it should stay flat in every ensemble.
- The full **pressure tensor** is reported (`pxx … pyz`), not just the scalar pressure.

## Statistics in the reports

For every column and every stage: `n, mean, std, min, max` and a **block-averaged standard error**
(Flyvbjerg–Petersen), which is honest for correlated MD data, plus the naive error and the
statistical inefficiency.

Per stage:

- **Conserved-quantity drift** per atom per time unit and per atom per ns, with its uncertainty,
  and σ(conserved)/σ(potential) as a quality indicator.
- **Stationarity** flag (is the stage equilibrated?).
- **Heat capacity** from fluctuations: from kinetic-energy fluctuations in NVE
  (Lebowitz–Percus–Verlet) and total-energy fluctuations in NVT. It is computed on the second half
  of a stage, and only if that half is stationary.
- **Minimization results** (energy, max force, cell) for minimize stages.
- **Throughput**: steps/s, atom-steps/s, ns/day.

Structure and dynamics (stages with `record`):

- g(r) with its first peak, first minimum and coordination number;
- diffusion coefficient D from the MSD slope and from the VACF integral.

## Excerpt

```text
## Stage `production` — md (NVE)

| quantity | mean | std | ±err (block) | min | max |
|---|---|---|---|---|---|
| temperature [K] | … |
| kinetic [eV] | … |
| potential [eV] | … |
| lj [eV] | … |
| total [eV] | … |
| conserved [eV] | … |
| pressure [bar] | … |
| pxx [bar] … pyz [bar] | … |
| volume [Å³] | … |
| density [g/cm³] | … |

- conserved-quantity drift: … eV/(atom·ns)
- heat capacity C_V = … k_B/atom
- performance: … atom-steps/s, … ns/day
```

See [`examples/md/sample-output/summary.md`](../examples/md/sample-output/summary.md) for real
numbers.
