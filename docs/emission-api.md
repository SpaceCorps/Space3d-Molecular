# spaceemit — electron emission API

`spaceemit` computes thermal-field electron emission from metal and semiconductor surfaces:
current density, Nottingham heat, energy spectra, barrier profiles, transmission probabilities,
and fits to measured I–V curves. It is served as an HTTP/JSON API (default port **8741**).

Machine-readable spec: [`openapi.yaml`](openapi.yaml).

- [Conventions](#conventions)
- [Endpoints](#endpoints): [`/health`](#get-health) · [`/v1/info`](#get-v1info) ·
  [`/v1/emission`](#post-v1emission) · [`/v1/spectra`](#post-v1spectra) ·
  [`/v1/barrier`](#post-v1barrier) · [`/v1/transmission`](#post-v1transmission) ·
  [`/v1/iv-fit`](#post-v1iv-fit)
- [Errors](#errors)
- [Physics models and references](#physics-models-and-references)

## Conventions

- JSON in, JSON out, `camelCase` keys. Send `content-type: application/json`.
- Responses are gzip-compressed if the request carries `accept-encoding: gzip`. CORS is open.
- Energies are in eV. The **vacuum level at the surface is 0**, so the **Fermi level is at −W**.
  Spectrum and transmission energies are given **relative to E_F** (parallel energies are ≥ 0).
- Values that cannot be computed come back as `null`; batch endpoints add a per-point entry to
  `errors` instead of failing the whole request.

### Units

| key | unit | meaning |
|---|---|---|
| `field` | V/nm | local electric field at the emitting surface |
| `radius` | nm | local radius of curvature; omitted or `null` = planar surface (in arrays: numbers only) |
| `gamma` | 1 | barrier shape: ratio of the local to the far field, ≥ 1 (default 10) |
| `workFunction` | eV | work function W |
| `temperature` | K | electron temperature (default 300) |
| `effectiveMass` | mₑ | effective mass of the emitting band (default 1 = free-electron metal) |
| `bandDepth` | eV | band bottom to Fermi level (default 10) |
| `currentDensity` | A/nm² | emitted current density J (1 A/nm² = 10¹⁸ A/m²) |
| `nottinghamHeat` | W/nm² | ∫(E − E_F) j(E) dE: power carried away relative to E_F. **Negative ⇒ the emitter is heated**, positive ⇒ cooled |
| `meanEnergy` | eV | mean emitted energy relative to E_F (= nottinghamHeat / currentDensity) |
| `barrierTop` | eV | barrier maximum relative to E_F |
| `regime` | – | `"field"`, `"intermediate"` or `"thermionic"` |
| spectrum values | A/nm²/eV | dJ/dE |
| `distance` | nm | distance from the electrical surface |
| `potential` | eV | barrier potential relative to the vacuum level at the surface |
| `voltage`, `current` | V, A | measured I–V data |
| `beta` | 1/nm | field conversion factor, F = β·V |
| `area` | nm² | effective emission area |

### Options

Every compute endpoint accepts an optional `options` object:

| key | default | meaning |
|---|---|---|
| `mode` | `"exact"` | `"exact"`: numerically exact quantum transmission. `"wkb"`: faster semiclassical (Kemble) approximation — typically tens of % off in J, useful for scans |
| `tolerance` | `1e-6` | target relative accuracy of `exact` results |

## Endpoints

### `GET /health`

```json
{"status":"ok"}
```

### `GET /v1/info`

Version, defaults, units, endpoint list, model summary and citations.

### `POST /v1/emission`

Batch current density and Nottingham heat. **Every numeric input is a number or an array**;
arrays must share one length and scalars are broadcast. Required: `field`, `workFunction`.

```sh
curl -s localhost:8741/v1/emission -H 'content-type: application/json' -d '{
  "field": [3, 5, 8], "radius": 50, "workFunction": 4.5, "temperature": [300, 1000, 2000]
}'
```

```json
{
  "count": 3,
  "currentDensity": [1.9801404244016396e-13, 3.6048064548481467e-09, 9.852636328538773e-07],
  "nottinghamHeat": [-2.153918644900658e-14, -3.181914215084101e-10, -5.0086490207984195e-08],
  "meanEnergy": [-0.10877605539271443, -0.0882686561661225, -0.05083562260682003],
  "barrierTop": [2.432346260396952, 1.8275371928772408, 1.1167179059392134],
  "regime": ["field", "field", "field"],
  "errors": [],
  "elapsedMs": 0.838
}
```

Semiconductor / finite band: add `effectiveMass` and `bandDepth`.

```sh
curl -s localhost:8741/v1/emission -H 'content-type: application/json' \
  -d '{"field": 5, "workFunction": 4.5, "effectiveMass": 0.3, "bandDepth": 1.5, "temperature": 800}'
```

A bad point does not fail the batch:

```json
{"count": 2,
 "currentDensity": [3.5245343693801343e-9, null], "nottinghamHeat": [-7.247139034978009e-10, null],
 "meanEnergy": [-0.2056197578306656, null], "barrierTop": [1.8167514578010109, null],
 "regime": ["field", null],
 "errors": [{"index": 1, "code": "invalid_parameter",
             "message": "invalid parameter `field` = -1: must be finite and > 0 V/nm"}],
 "elapsedMs": 0.052}
```

### `POST /v1/spectra`

Total, normal and parallel energy distributions of **one** point. `points` sets the number of
samples per distribution (default 256). `sumRules` gives ∫distribution / J for each of the three
(1 = exact).

```sh
curl -s localhost:8741/v1/spectra -H 'content-type: application/json' \
  -d '{"field": 4, "radius": 20, "workFunction": 4.5, "temperature": 300, "points": 64}'
```

```json
{
  "currentDensity": 4.541498337717358e-11,
  "nottinghamHeat": -6.673528335499985e-12,
  "totalEnergyDistribution":    {"energy": [-3.376, -3.296, "…"], "value": [0.0, 6.94e-21, "…"]},
  "normalEnergyDistribution":   {"energy": [-3.376, -3.313, "…"], "value": [2.08e-19, 3.44e-19, "…"]},
  "parallelEnergyDistribution": {"energy": [0.0, 0.00111, "…"],   "value": [2.78e-10, 2.76e-10, "…"]},
  "sumRules": [1.00024, 1.00004, 1.00226]
}
```

### `POST /v1/barrier`

Barrier potential U(x) for `field`, `radius`, `gamma`, at the given `distance` values — or
`points` log-spaced samples from 0.05 nm to `maxDistance` (a default grid if neither is given) —
plus the barrier top.

```sh
curl -s localhost:8741/v1/barrier -H 'content-type: application/json' \
  -d '{"field": 5, "radius": 20, "gamma": 10, "distance": [0.2, 0.5, 1, 2]}'
```

```json
{"distance": [0.2, 0.5, 1.0, 2.0],
 "potential": [-2.781110571506159, -3.1502827930620785, -5.114368760064305, -9.271424350933643],
 "topDistance": 0.2719590314816497, "topPotential": -2.6563371386592354, "topHbarOmega": 1.6404488271180342}
```

`topHbarOmega` (eV) is the curvature energy ħω of the barrier top.

### `POST /v1/transmission`

Transmission probability through the barrier versus **normal** energy (relative to E_F), for one
point. Give `energy` (number or array), or `points` (default 101) evenly spaced energies from
3 eV below E_F (or the band bottom, if higher) to 1 eV above the barrier top. `parallelEnergy`
(eV, default 0) is the emitted electron's parallel kinetic energy; it matters for bands with
m* ≠ 1.

```sh
curl -s localhost:8741/v1/transmission -H 'content-type: application/json' \
  -d '{"field": 5, "radius": 20, "workFunction": 4.5, "energy": [-1, -0.5, 0, 0.5]}'
```

```json
{"energy": [-1.0, -0.5, 0.0, 0.5],
 "transmission":    [2.0564425773844336e-06, 2.5588781321484128e-05, 0.0002756900138046107, "…"],
 "logTransmission": [-13.094532972163009, -10.57335653215895, -8.196233461828792, "…"],
 "gamow":           [13.150794331960052, 10.524976516371343, 8.028984820552996, "…"],
 "kemble":          [1.9439350248863634e-06, 2.6856481400079225e-05, 0.00032577270414158705, "…"]}
```

`transmission` is the exact result; `gamow` (G) and `kemble` = 1/(1 + e^G) are the
semiclassical values, for comparison.

### `POST /v1/iv-fit`

Fits measured current–voltage data (at least 3 points with V > 0 and I > 0). Always fitted: the
field conversion factor β (F = β·V) and the effective emission area. Optionally also any of
`radius`, `gamma`, `workFunction`, `temperature` — list them in `fit`; the others are held at
the given values (`effectiveMass` and `bandDepth` may also be given).

Optional: `bounds` — any subset of `{"beta", "radius", "gamma", "workFunction", "temperature"}`
as `[lower, upper]` (defaults: β [1e-7, 10] nm⁻¹, R [1, 10⁵] nm, γ [1, 1000], W [1, 8] eV,
T [1, 5000] K); `initialBeta` (nm⁻¹, default from a Fowler–Nordheim plot); `maxIterations`
(default 60); `options`.

```sh
curl -s localhost:8741/v1/iv-fit -H 'content-type: application/json' -d '{
  "voltage": [800, 900, 1000, 1100], "current": [1e-9, 2e-8, 2.2e-7, 1.5e-6],
  "workFunction": 4.5, "radius": 30, "fit": ["radius"], "bounds": {"radius": [5, 200]}
}'
```

```json
{"converged": true, "iterations": 10, "rmsLogResidual": 0.006694665857809055,
 "beta":   {"value": 0.0036693229969331706, "sigma": 0.00020512198628269324},
 "area":   {"value": 35951.79252645955, "sigma": 240.6852379539235},
 "radius": {"value": 15.62808743933196, "sigma": 6.622251771322876},
 "gamma": {"value": 10.0, "sigma": 0.0}, "workFunction": {"value": 4.5, "sigma": 0.0},
 "temperature": {"value": 300.0, "sigma": 0.0},
 "voltage": [800.0, 900.0, 1000.0, 1100.0], "current": [1e-09, 2e-08, 2.2e-07, 1.5e-06],
 "field": [2.9354583975465367, 3.3023906972398533, 3.6693229969331704, "…"],
 "fittedCurrent": [9.979560508636348e-10, 2.015826680450604e-08, 2.1784500933143476e-07, "…"]}
```

`sigma` is the one-standard-deviation uncertainty (0 for parameters held fixed).

## Errors

Request-level errors return a non-2xx status with

```json
{"error": {"code": "length_mismatch", "message": "array length mismatch: `field` has 2 elements, expected 1 or 3"}}
```

| code | status | when |
|---|---|---|
| `invalid_json` | 400 | body is not JSON |
| `invalid_request` | 422 | JSON does not match the endpoint schema (e.g. missing `workFunction`) |
| `invalid_parameter` | 422 | a value is out of range (also used per point in `errors`) |
| `no_barrier` | 422 | the barrier has no maximum above the band for these parameters |
| `length_mismatch` | 422 | array inputs of different lengths |
| `fit_failed` | 422 | the I–V fit did not converge |
| `payload_too_large` | 413 | request body too large |
| `batch_too_large` | 413 | too many points in one request — split the batch |
| `not_found` | 404 | unknown endpoint |

Codes are stable; messages are for humans and may change.

## Physics models and references

- **Barrier:** general barrier for curved emitters with local field F, radius of curvature R and
  shape parameter γ, reducing to the planar Schottky–Nordheim barrier as R → ∞.
  A. Kyritsakis & F. Djurabekova, *Comput. Mater. Sci.* **128**, 15 (2017);
  A. Kyritsakis & J. P. Xanthakis, *Proc. R. Soc. A* **471**, 20140811 (2015).
- **Transmission:** numerically exact one-dimensional quantum transmission from the emitter band
  (flat interior potential at the band bottom) through the barrier.
- **Supply and finite bands:** Fermi–Dirac supply with conservation of parallel momentum for a
  band of effective mass m* and finite depth. R. Stratton, *Phys. Rev.* **125**, 67 (1962);
  **135**, A794 (1964); S. Barranco Cárceles et al., arXiv:2506.06198 (2025).
- **Limits reproduced:** Murphy–Good (E. L. Murphy & R. H. Good, *Phys. Rev.* **102**, 1464
  (1956); R. G. Forbes, *Appl. Phys. Lett.* **89**, 113122 (2006)), Richardson–Schottky, the
  Nottingham inversion temperature, and the planar limit.
