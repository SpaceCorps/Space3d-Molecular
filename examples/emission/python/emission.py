"""spaceemit client example — standard library only (Python 3.9+).

    SPACEEMIT_URL=http://localhost:8741 python3 emission.py
"""
import json
import os
import urllib.error
import urllib.request

URL = os.environ.get("SPACEEMIT_URL", "http://localhost:8741")


def post(path, body):
    req = urllib.request.Request(URL + path, data=json.dumps(body).encode(),
                                 headers={"content-type": "application/json"})
    try:
        with urllib.request.urlopen(req) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        err = json.load(e)["error"]
        raise RuntimeError(f"{err['code']}: {err['message']}") from None


# Fowler–Nordheim-style scan: J vs field at two temperatures.
fields = [2 + 0.5 * i for i in range(17)]
for T in (300, 1500):
    r = post("/v1/emission", {"field": fields, "radius": 20, "workFunction": 4.5, "temperature": T})
    print(f"T = {T} K")
    for F, J, P, E, regime in zip(fields, r["currentDensity"], r["nottinghamHeat"],
                                  r["meanEnergy"], r["regime"]):
        if J is None:
            continue
        # A/nm^2 -> A/cm^2 is x 1e14; W/nm^2 -> W/cm^2 likewise.
        print(f"  F={F:5.2f} V/nm  J={J * 1e14:10.3e} A/cm^2  P_N={P * 1e14:10.3e} W/cm^2"
              f"  <E-E_F>={E:+.3f} eV  {regime}")
    for e in r["errors"]:
        print("  point", e["index"], "failed:", e["code"], e["message"])

# Energy spectra of one point; the sum rules should all be ~1.
s = post("/v1/spectra", {"field": 5, "radius": 20, "workFunction": 4.5, "temperature": 1000, "points": 128})
ted = s["totalEnergyDistribution"]
peak = max(range(len(ted["value"])), key=ted["value"].__getitem__)
print(f"TED peak at E - E_F = {ted['energy'][peak]:+.3f} eV; sum rules {s['sumRules']}")

# Fit an I-V curve.
fit = post("/v1/iv-fit", {"voltage": [800, 900, 1000, 1100], "current": [1e-9, 2e-8, 2.2e-7, 1.5e-6],
                          "workFunction": 4.5, "radius": 30, "fit": ["radius"]})
print(f"beta = {fit['beta']['value']:.5f} ± {fit['beta']['sigma']:.5f} 1/nm, "
      f"R = {fit['radius']['value']:.1f} ± {fit['radius']['sigma']:.1f} nm, "
      f"area = {fit['area']['value']:.3g} nm^2, converged = {fit['converged']}")
