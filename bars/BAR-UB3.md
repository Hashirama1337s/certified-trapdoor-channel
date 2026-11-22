# BAR-UB3: blind checker on the collapsed-dual certificates converted back to the refereed old format (k = 10, 11)

Raid TRAPDOOR, step T3. Sealed by the lead before the lead's runs. The proof chain is PROOF-UB1 (refereed); the collapse is used only to FIND the test law, so the new, unrefereed PROOF-COLLAPSE.md is not relied on.

## Disclosed before sealing (seen)
build-ub3 seat, with the unmodified build-ub/verify_u2b.py:
- xcheck_old_u2b_d12_k11_from_col.json: 0.575008505468
- xcheck_old_u2b_d11_k10_from_col.json: 0.575034410522
- collapsed certificates k = 3..15 (k = 15: 0.574968594275), listed in build-ub3/NOTES.md.

The blind checker blind-ub/check_ub.py has NOT been run on these files by anyone.

## Instruments (sha256 in SEALS-UB3.txt)
- build-ub3/certs/xcheck_old_u2b_d12_k11_from_col.json
- build-ub3/certs/xcheck_old_u2b_d11_k10_from_col.json
- blind-ub/check_ub.py 424ce217... (unchanged since BAR-UB1)

## Predictions
- **Q1 (target).** check_ub.py on the d12 k11 file gives an upper endpoint in [0.5750085054, 0.5750085055].
- **Q2 (target).** check_ub.py on the d11 k10 file gives an upper endpoint in [0.5750344105, 0.5750344106].
- **N1 (null, content).** A copy of the d11 k10 file with h_num[0] lowered by h_den/1000 (h lowered by 1e-3 at one state) gives a larger endpoint than Q2 in check_ub.py.

## Verdict
HOLD if Q1, Q2 and N1 all pass; FAILED otherwise.

## Not claimed
The k = 12..15 collapsed certificates, which wait for the referee on PROOF-COLLAPSE.md and an independent collapsed verifier. Optimality.

## Seal fields
- formula_ref: PROOF-UB1.md:11-16
- calibrated_on: none - windows are the disclosed verify_u2b endpoints, which the independent blind checker must reproduce
- depends_on: 4174b6d291
- null_not_symmetry: N1 lowers one value-function entry, not a relabelling
- target_form: rigorous upper endpoints in decimal windows
- parameters: (d,k) = (12,11) and (11,10)
- instruments: xcheck_old_u2b_d12_k11_from_col.json, xcheck_old_u2b_d11_k10_from_col.json, check_ub.py
- tolerances: windows of width 1e-10, because both verifiers round outward at about 1e-12, leaving headroom
- ceiling: a certified upper bound on C
- toy_model: d = 4 (BAR-UB1)
