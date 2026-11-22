# BAR-UB1: blind re-verification of the certified upper bounds C <= 0.5752327 (d = 8) and C <= 0.5764760 (d = 4)

Raid TRAPDOOR, step T2. Written and sealed by the lead before the blind seat starts. The blind seat sees the certificate files and the format description only (build-ub/NOTES.md lines 13-29, copied into its brief), never verify_u2b.py, the solver, the logs or this bar's numbers beyond what it must print.

## Disclosed before sealing
- Build seat (own verifier build-ub/verify_u2b.py, already seen): d = 4 k = 4: 0.576476036830; d = 8 k = 7: 0.575232734724; d = 2 snapped: 0.584962500722; d = 1: 0.704837047948. Lead re-ran verify_u2b.py on d = 8 and d = 4 and got the same; the U1 negative control fails.

## Instruments (sha256)
- build-ub/certs/cert_u2b_d8_k7.json 27ca42bb07b68c65b01007bca3cba08ba9953158281483b243df19128cb5455b
- build-ub/certs/cert_u2b_d4_k4.json 9d880c35dccbbd7c6fdba2a17dda9c87daab5658c92539c3c0b241d3800fa6e5
- build-ub/certs/cert_u2b_d2_k1_snap.json 89d6e8e9de93a99931809231cc8af91d534ca3b5b6ad9ec2dfbead8323a170e2
- build-ub/certs/cert_u2b_d1_k1.json df563dd01836012364c0a5c49a88bb7b6445e1a8539d6e96cd7b2ebd6a0e2f75
- The blind seat's own verifier (written fresh in blind-ub/), hashed by the lead after it reports.

## Predictions
- **B1 (target).** Blind verifier on cert_u2b_d8_k7.json reports a rigorous upper endpoint in [0.5752327347, 0.5752327348].
- **B2 (target).** Blind verifier on cert_u2b_d4_k4.json reports a rigorous upper endpoint in [0.5764760368, 0.5764760369].
- **B3 (control).** On cert_u2b_d2_k1_snap.json: upper endpoint within 1e-12 of log2(3/2) = 0.5849625007211562.
- **B4 (control).** On cert_u2b_d1_k1.json: upper endpoint >= log2((1+sqrt5)/2) = 0.6942419136.
- **N1 (null, content).** The blind seat builds a mutated copy of the d = 4 certificate (one h entry lowered by 1/100) and its verifier reports a larger upper endpoint than in B2, or rejects it.

## Verdict
HOLD if B1-B4 and N1 pass; FAILED otherwise. Failures kept.

## Not claimed
The theory argument (build-ub/NOTES.md "The argument"), which goes to a separate hostile referee; optimality of the certificates.

## Seal fields
- formula_ref: build-ub/NOTES.md:13-29, build-ub/NOTES.md:30-94
- calibrated_on: none - windows are the disclosed certified values, which a correct blind re-implementation must reproduce
- depends_on: fac3ef4afd
- null_not_symmetry: N1 alters a certificate entry, not a relabelling
- target_form: rigorous upper endpoints in decimal windows
- parameters: d = 1, 2, 4, 8 fixed - the four shipped certificates spanning control, negative control and targets
- instruments: build-ub/certs/*.json listed above; the blind verifier
- tolerances: none - windows of width 1e-10 around disclosed certified endpoints
- ceiling: a certified upper bound on C
- toy_model: d = 2 (closed form log2(3/2))
