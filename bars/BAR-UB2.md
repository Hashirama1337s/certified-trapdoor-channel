# BAR-UB2: lead re-run of the blind checker on the round-2 ceiling certificates

Raid TRAPDOOR, step T3 (squeeze). Written and sealed by the lead before the lead's re-run. The proof chain is unchanged from PROOF-UB1 (same certificate format, same theorem); only new certificates are being checked.

## Disclosed before sealing (NOT blind)
- Build seat build-ub2 reported verify_u2b.py and check_ub.py endpoints. (10,10) lift: 0.575092822040 / 0.575092822039761. (8,8): 0.575140726013 / 0.575140726012508. 25 further endpoints are listed in build-ub2/logs/cert_index.txt.
- So this test checks reproducibility, file integrity and the controls on the lead's machine. It is not a blind prediction.

## Instruments (sha256, also in SEALS-UB2.txt)
- build-ub2/certs/cert_u2b_d10_k10_lift_d9k9b1e6.json e55f668e66ea409ca75a1001fd6f4384177988a69534acf5cee079f370f7d93c
- build-ub2/certs/cert_u2b_d8_k8.json bdbe71fcfb5d61de423ce510d90877bd2e8db27d1d5d0fbcbb19bba30270609f
- blind-ub/check_ub.py 424ce217edfbfe2058aa2dd69845039e983e3900a494e0893932666ff788ceac (the blind seat's verifier, unchanged since BAR-UB1)
- build-ub/verify_u2b.py e0cd025e0af312759ee73163821b1b7383a20edf132e28b24e0235d9e4d16c88

## Predictions
- **Q1 (target).** check_ub.py on the (10,10) certificate gives an upper endpoint in [0.5750928220, 0.5750928221].
- **Q2 (target).** check_ub.py on the (8,8) certificate gives an upper endpoint in [0.5751407260, 0.5751407261].
- **Q3 (control).** check_ub.py on build-ub/certs/cert_u2b_d4_k4.json reproduces BAR-UB1 B2: [0.5764760368, 0.5764760369].
- **N1 (null, content).** A copy of the (8,8) certificate with one T entry moved by +0.01 (row kept a distribution), checked by verify_u2b.py, gives a larger endpoint than Q2.

## Verdict
HOLD if Q1-Q3 and N1 all pass; FAILED otherwise.

## Not claimed
Optimality. Novelty of the collapse (that is a separate step, build-ub3).

## Seal fields
- formula_ref: PROOF-UB1.md:11-16
- calibrated_on: none - windows are the disclosed endpoints, which must reproduce on the lead's run
- depends_on: d110ac48e8
- null_not_symmetry: N1 perturbs a test-law entry, not a relabelling
- target_form: rigorous upper endpoints in decimal windows
- parameters: (d,k) = (10,10) lift, (8,8); control (4,4)
- instruments: the two certificates, check_ub.py, verify_u2b.py
- tolerances: windows of width 1e-10, because both verifiers round outward at about 1e-12, leaving headroom
- ceiling: a certified upper bound on C
- toy_model: d = 4 (BAR-UB1)
