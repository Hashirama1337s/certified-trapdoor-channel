# BAR-LB4: order-9 floor with the proven log routine (assumption A2 removed)

Raid TRAPDOOR, step T3. Sealed by the lead before the lead's runs.

## Disclosed before sealing (seen)
build-lb3 seat, cert_backward2.py:
- order 9 (s9_d100000_z0.0005.txt) N=24: 0.57492740773047 (E 7.227e-13);
- N=13: 0.57476380405797; N=11: 0.57442380481309;
- order 8 N=12: 0.57465552857767; N=18: 0.57491787607017.

Exact reference values (REFEREE-LB3, ref_lb3.py and ref_exact.py): order 9 N=13 0.574763804058242098176; N=11 0.574423804813292196092.

## Instruments (sha256 in SEALS-LB4.txt)
- build-lb3/cert_backward2.py a7a0ae24...
- build-lb3/trapcommon.py 01464639...
- build-lb3/s9_d100000_z0.0005.txt 24b31a62...
- build-lb3/ERROR-LEMMA2.md 97c3dd25...

## Predictions
- **R1 (reproduction, lead run).** cert_backward2.py on the order-9 law at N=24 prints a lower endpoint in [0.57492740773040, 0.57492740773050].
- **R2 (content).** At N=12 (a depth no evaluator has printed for this law), the cert_backward2.py endpoint is <= the exact value from referee/lb1/ref_exact.py at N=12, and below it by at most E + 1e-14 + 1e-15, where 1e-14 covers the 14-decimal print truncation.
- **N1 (null).** cert_backward2.py on lead/theta_k4.txt at N=14 gives an endpoint in [0.5741292347550, 0.5741292347559], far below R1.

## Verdict
HOLD if R1, R2 and N1 all pass; FAILED otherwise. The N=24 value also rests on ERROR-LEMMA2.md, which goes to a hostile referee in parallel; it is quoted as proven only after that referee returns CORRECT or CORRECT WITH FIXES.

## Seal fields
- formula_ref: PROOF-LB1.md:11-17, build-lb3/ERROR-LEMMA2.md:1-75
- calibrated_on: none - R1 reproduces a disclosed value; R2 predicts agreement at an unprinted depth
- depends_on: a2847556a8
- null_not_symmetry: N1 uses a different input law with a known certified value
- target_form: rigorous lower endpoints
- parameters: order 9 at N = 24 and 12; null order 4 at N = 14
- instruments: cert_backward2.py, trapcommon.py, s9_d100000_z0.0005.txt, ref_exact.py
- tolerances: E (the kernel's own proven bound) plus 1e-14 print truncation plus 1e-15 interval rounding, giving headroom
- ceiling: a certified lower bound on C
- toy_model: order 4 (BAR-LB1)
