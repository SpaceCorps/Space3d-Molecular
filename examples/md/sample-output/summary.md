# Liquid argon at 94.4 K (Rahman 1964 state point)

spacemd 0.1.0 · units: **metal** (energy eV, length Å, time fs, T K, P bar)

## System

| property | value |
|---|---|
| atoms | 2048 |
| types | Ar×2048 |
| net charge | 0 e |
| cell (Å) | 46.24800 × 46.24800 × 46.24800 (tilt [0.0, 0.0, 0.0]), periodic [true, true, true] |
| potential terms | lj |
| neighbor cutoff + skin | 8.50000 + 1.00000 Å |
| threads | 16 |

## Stage `melt` — md (NVT (Langevin/BAOAB))

1500 steps × dt = 5.00000 fs (31 samples)

| quantity | mean | std | ±err (block) | min | max |
|---|---|---|---|---|---|
| temperature [K] | 188.63007 | 25.24879 | 4.60978 | 94.35391 | 204.12323 |
| kinetic [eV] | 49.93500 | 6.68397 | 1.22032 | 24.97779 | 54.03642 |
| potential [eV] | -92.49901 | 8.09665 | 1.47824 | -128.65824 | -87.60301 |
| lj [eV] | -92.49901 | 8.09665 | 1.47824 | -128.65824 | -87.60301 |
| total [eV] | -42.56401 | 14.60798 | 2.66704 | -103.68046 | -34.41575 |
| reservoir [eV] | -61.12851 | 14.61120 | 2.66763 | -69.27812 | 0 |
| conserved [eV] | -103.69252 | 0.00336 | 6.1332e-4 | -103.69606 | -103.68046 |
| pressure [bar] | 1741.73421 | 908.82601 | 165.92817 | -2348.76203 | 2273.61635 |
| pxx [bar] | 1741.75411 | 913.88176 | 166.85122 | -2355.06596 | 2331.73599 |
| pyy [bar] | 1744.51233 | 915.20432 | 167.09268 | -2344.54064 | 2236.09584 |
| pzz [bar] | 1738.93621 | 905.47693 | 165.31671 | -2346.67949 | 2405.43490 |
| pxy [bar] | -1.58850 | 53.54322 | 9.77561 | -114.16185 | 143.43273 |
| pxz [bar] | 6.17325 | 54.85656 | 10.01539 | -121.03000 | 134.25658 |
| pyz [bar] | 16.35861 | 48.04726 | 8.77219 | -79.93235 | 107.32011 |
| volume [Å³] | 98918.80680 | 4.3656e-11 | 7.9704e-12 | 98918.80680 | 98918.80680 |
| density [g/cm³] | 1.37339 | 4.4409e-16 | 8.1079e-17 | 1.37339 | 1.37339 |

- conserved-quantity drift: -3.9321e-10 eV/(atom·fs) ± 1.1499e-10 = **-3.9321e-4 eV/(atom·ns)**; span 7.6178e-6 eV/atom; σ(conserved)/σ(PE) = 4.1490e-4
- heat capacity C_V = **1.95564 k_B/atom** (NVT total-energy fluctuations ⟨δE²⟩/(k_B T²), second half of stage)
- performance: 5078.27795 steps/s, **1.0400e7 atom-steps/s**, 2193.81607 ns/day

## Stage `equilibrate` — md (NVT (Langevin/BAOAB))

1500 steps × dt = 5.00000 fs (31 samples)

| quantity | mean | std | ±err (block) | min | max |
|---|---|---|---|---|---|
| temperature [K] | 101.37768 | 22.02989 | 4.02209 | 90.73029 | 204.12323 |
| kinetic [eV] | 26.83715 | 5.83185 | 1.06475 | 24.01853 | 54.03642 |
| potential [eV] | -103.72363 | 3.75329 | 0.68525 | -105.64483 | -88.45216 |
| lj [eV] | -103.72363 | 3.75329 | 0.68525 | -105.64483 | -88.45216 |
| total [eV] | -76.88648 | 9.52702 | 1.73939 | -81.36024 | -34.41575 |
| reservoir [eV] | -26.79539 | 9.52946 | 1.73983 | -69.27812 | -22.32055 |
| conserved [eV] | -103.68186 | 0.00252 | 4.6078e-4 | -103.69387 | -103.68025 |
| pressure [bar] | 514.09532 | 404.32328 | 73.81899 | 313.54342 | 2183.89307 |
| pxx [bar] | 495.76381 | 401.84996 | 73.36743 | 255.64401 | 2179.82959 |
| pyy [bar] | 514.94621 | 417.75824 | 76.27187 | 229.35137 | 2236.09584 |
| pzz [bar] | 531.57594 | 398.34710 | 72.72790 | 291.38760 | 2135.75379 |
| pxy [bar] | -7.93005 | 33.12794 | 6.04831 | -70.92981 | 74.92648 |
| pxz [bar] | 12.13538 | 28.92181 | 5.28038 | -52.48598 | 99.83546 |
| pyz [bar] | 6.13055 | 35.43041 | 6.46868 | -58.30654 | 84.46298 |
| volume [Å³] | 98918.80680 | 4.3656e-11 | 7.9704e-12 | 98918.80680 | 98918.80680 |
| density [g/cm³] | 1.37339 | 4.4409e-16 | 8.1079e-17 | 1.37339 | 1.37339 |

- conserved-quantity drift: 1.9821e-10 eV/(atom·fs) ± 9.5490e-11 = **1.9821e-4 eV/(atom·ns)**; span 6.6504e-6 eV/atom; σ(conserved)/σ(PE) = 6.7242e-4
- heat capacity C_V = **3.13585 k_B/atom** (NVT total-energy fluctuations ⟨δE²⟩/(k_B T²), second half of stage)
- performance: 5547.67053 steps/s, **1.1362e7 atom-steps/s**, 2396.59367 ns/day

## Stage `production` — md (NVE)

1500 steps × dt = 5.00000 fs (31 samples)

| quantity | mean | std | ±err (block) | min | max |
|---|---|---|---|---|---|
| temperature [K] | 96.12487 | 0.97455 | 0.17793 | 94.12666 | 98.08808 |
| kinetic [eV] | 25.43418 | 0.25786 | 0.04708 | 24.90546 | 25.95364 |
| potential [eV] | -104.93733 | 0.25795 | 0.04709 | -105.45717 | -104.40880 |
| lj [eV] | -104.93733 | 0.25795 | 0.04709 | -105.45717 | -104.40880 |
| total [eV] | -79.50315 | 2.2402e-4 | 4.0901e-5 | -79.50353 | -79.50274 |
| reservoir [eV] | -24.17867 | 7.1054e-15 | 1.2973e-15 | -24.17867 | -24.17867 |
| conserved [eV] | -103.68182 | 2.2402e-4 | 4.0901e-5 | -103.68220 | -103.68141 |
| pressure [bar] | 395.19986 | 26.05839 | 4.75759 | 326.33933 | 465.77178 |
| pxx [bar] | 399.74798 | 45.62393 | 8.32975 | 314.99873 | 487.46525 |
| pyy [bar] | 382.64861 | 44.91870 | 8.20100 | 289.49280 | 461.32951 |
| pzz [bar] | 403.20298 | 53.76596 | 9.81628 | 284.93172 | 484.43679 |
| pxy [bar] | -8.56551 | 27.20737 | 4.96736 | -76.94263 | 41.32284 |
| pxz [bar] | -1.82306 | 29.36145 | 5.36064 | -85.99298 | 58.06637 |
| pyz [bar] | 1.05078 | 42.07980 | 7.68268 | -92.08676 | 96.99937 |
| volume [Å³] | 98918.80680 | 4.3656e-11 | 7.9704e-12 | 98918.80680 | 98918.80680 |
| density [g/cm³] | 1.37339 | 4.4409e-16 | 8.1079e-17 | 1.37339 | 1.37339 |

- conserved-quantity drift: 1.7154e-11 eV/(atom·fs) ± 8.5072e-12 = **1.7154e-5 eV/(atom·ns)**; span 3.8671e-7 eV/atom; σ(conserved)/σ(PE) = 8.6848e-4
- heat capacity C_V = **2.00630 k_B/atom** (NVE kinetic-energy fluctuations (Lebowitz–Percus–Verlet), second half of stage)
- performance: 5772.28382 steps/s, **1.1822e7 atom-steps/s**, 2493.62661 ns/day

## Structure and dynamics

- g(r): first peak at r = 3.67500 Å (g = 2.84700), first minimum at 5.32500 Å, coordination number 12.63496 (15 frames; see `rdf.csv`)
- MSD (Einstein): D = 2.6660e-4 ± 3.1493e-7 Å²/fs = 2.6660e-5 cm²/s (per type: Ar: 2.6660e-4; see `msd.csv`)
- VACF (Green–Kubo): D = 2.6500e-4 Å²/fs = 2.6500e-5 cm²/s (see `vacf.csv`)

## Notes

- total wall time 0.83 s
