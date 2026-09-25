#!/usr/bin/env bash
# spaceemit API tour with curl, against the public instance (set SPACEEMIT_URL for your own).
set -euo pipefail
URL=${SPACEEMIT_URL:-https://spaceemit-api.sliplane.app}
post() { curl -sS -X POST "$URL$1" -H 'content-type: application/json' -H 'accept-encoding: gzip' --compressed -d "$2"; echo; }

echo "# health";   curl -sS "$URL/health"; echo

echo "# current density + Nottingham heat, 3 points (scalars broadcast)"
post /v1/emission '{"field": [3, 5, 8], "radius": 50, "workFunction": 4.5, "temperature": [300, 1000, 2000]}'

echo "# semiconductor-like band: effective mass 0.3, band depth 1.5 eV"
post /v1/emission '{"field": 5, "workFunction": 4.5, "effectiveMass": 0.3, "bandDepth": 1.5, "temperature": 800}'

echo "# fast semiclassical mode for a quick scan"
post /v1/emission '{"field": [2, 4, 6, 8, 10], "workFunction": 4.5, "options": {"mode": "wkb"}}'

echo "# barrier profile"
post /v1/barrier '{"field": 5, "radius": 20, "gamma": 10, "distance": [0.2, 0.5, 1, 2]}'

echo "# transmission vs normal energy (relative to E_F)"
post /v1/transmission '{"field": 5, "radius": 20, "workFunction": 4.5, "energy": [-1, -0.5, 0, 0.5]}'

echo "# fit an I-V curve: beta and area always, radius bounded to 5-200 nm"
post /v1/iv-fit '{"voltage": [800, 900, 1000, 1100], "current": [1e-9, 2e-8, 2.2e-7, 1.5e-6],
                  "workFunction": 4.5, "radius": 30, "fit": ["radius"], "bounds": {"radius": [5, 200]}}'
