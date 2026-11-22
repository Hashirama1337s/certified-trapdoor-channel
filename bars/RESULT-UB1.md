# RESULT-UB1: scored against BAR-UB1 (seal d110ac48e8)

Blind seat files: blind-ub/BLIND-UB1.md, blind-ub/results.json, blind-ub/check_ub.py (sha256 424ce217edfbfe2058aa2dd69845039e983e3900a494e0893932666ff788ceac), blind-ub/mutate_ub.py (a4b4232afa929ab5aa31de724dea9ae5dba5a987f9e2a1a749c04c09403eb353). The blind seat opened no forbidden path (its statement); the convention was fixed by the controls (send-newest and oldest-as-LSB conventions fail them).

- **B1 HOLD.** d = 8, k = 7: upper endpoint 0.575232734723357 (arb ball [0.5752327347233568577321400 +/- 6.89e-27]); in [0.5752327347, 0.5752327348].
- **B2 HOLD.** d = 4, k = 4: 0.576476036829145; in [0.5764760368, 0.5764760369].
- **B3 HOLD.** d = 2 snapped: [0.5849625007211561814537389 +/- 4.40e-26] = log2(3/2) within 1e-12.
- **B4 HOLD.** d = 1: 0.704837047947419 >= 0.6942419136.
- **N1 HOLD.** h[198] of the d = 4 certificate lowered by 1/100: rho_cert = 0.586476036829145 (> B2); all 256 single-entry lowerings raise rho by ~1/100.

**Verdict: HOLD 5/5.** The certificate arithmetic is independently confirmed. The theory chain (rho_cert >= C) is with the hostile referee (REFEREE-UB1, pending).
Flag from the blind seat: solver_info.cvx_rho in the certificate files is below the certified value and is NOT a bound; never quote it.
