# BAR-LB3: order-9 floor C >= 0.5749274 (backward kernel at N = 24), cross-checked by an independent exact evaluator at small depth

Raid TRAPDOOR, step T3 (squeeze). Written and sealed by the lead before the lead's runs.

## Disclosed before sealing (seen)
Build seat build-lb2 reported, from its own cert_backward.py:
- order 9 (s9_d100000_z0.0005.txt): N=20 0.574924481004, N=22 0.57492668399382, N=24 0.57492740773049;
- the old order-7 law at N=15..24, plus the tables in build-lb2/NOTES.md.

Nothing is disclosed about this law at N <= 16 from any evaluator.

## Instruments (sha256 in SEALS-LB3.txt)
- build-lb2/s9_d100000_z0.0005.txt 24b31a620c88...
- build-lb2/cert_backward.py 4c58774b894f... and build-lb2/trapcommon.py 01464639...
- referee/lb1/ref_exact.py (independent exact evaluator: integer arithmetic plus mpmath intervals), as pinned in BAR-LB2
- lead/cert_lb.py 06aa5404... (second independent exact evaluator, arb)

## Predictions
- **P1 (content, independent).** At N = 13, the ref_exact.py lower endpoint and the cert_backward.py printed lower endpoint differ by at most cert_backward's stated error E (< 1e-12) plus 1e-15. Both are > 0.5748.
- **P2 (content, second independent).** cert_lb.py at N = 13 agrees with ref_exact.py to 1e-15.
- **P3 (reproduction).** The lead re-runs cert_backward.py at N = 24 and gets a lower endpoint within 1e-13 of 0.57492740773049.
- **N1 (null, content).** cert_backward.py on lead/theta_k4.txt at N = 14 reproduces the BAR-LB1 value 0.5741292347558 to within E, which is far below P3.

## Verdict
HOLD if P1-P3 and N1 all pass; FAILED otherwise.

The N = 24 value additionally rests on ERROR-LEMMA.md (sha 20b95acf...; float error bound, assumption A2 on log2 accuracy). A hostile referee checks it in parallel. Until that referee returns CORRECT or CORRECT WITH FIXES, the proven floor quoted to the owner is the N=13 exact value from P1/P2, not the N=24 value.

## Seal fields
- formula_ref: PROOF-LB1.md:11-17, build-lb2/ERROR-LEMMA.md:1-55
- calibrated_on: none - P1/P2 predict agreement between independent evaluators on a value not yet seen; P3 reproduces a disclosed value
- depends_on: a2847556a8
- null_not_symmetry: N1 uses a different input law with a known certified value
- target_form: rigorous lower endpoints
- parameters: order 9, N = 13 and 24; null order 4, N = 14
- instruments: s9_d100000_z0.0005.txt, cert_backward.py, trapcommon.py, ref_exact.py, cert_lb.py
- tolerances: E < 1e-12 is cert_backward's own stated bound; 1e-15 covers arb/mpmath outward rounding, giving headroom
- ceiling: a certified lower bound on C
- toy_model: order 4 (BAR-LB1)
