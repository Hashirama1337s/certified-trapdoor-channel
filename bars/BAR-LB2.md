# BAR-LB2: independent re-certification of the order-7 Markov lower bound C >= 0.5748048

Raid TRAPDOOR, step T3 (squeeze). Written and sealed by the lead before the independent check runs.

## Disclosed before sealing
- Build seat, using the sealed lead/cert_lb.py unmodified: theta_K7_rat.txt, N = 15: L_15 enclosure [0.57480483303961070779 +/- 2.98e-21]; certified lower endpoint printed as 0.574804833039611 +/- 2.93e-16. The lead read the log itself.
- Build seat, also seen: K=7 N=14 0.5747703355; K=5 N=16 0.5747397804.
- The independent instrument is the referee's referee/lb1/ref_exact.py: integer arithmetic plus mpmath intervals, a different code base from cert_lb.py. It has already been run on the K=4 theta only.

## Instruments (sha256)
- build-lb/theta_K7_rat.txt 7126905a201840cef4d8d5e0c799312897a1b95cfa08f20ec2512674e3216c89
- lead/cert_lb.py 06aa54048344d9d7181ee7cb6676385a72ebca2732d1908d00427142e8e472df
- referee/lb1/ref_exact.py (hash pinned in SEALS-LB2.txt at sealing)

## Predictions
- **P1 (target).** ref_exact.py on theta_K7_rat.txt at N = 15 gives an enclosure whose lower endpoint is >= 0.5748048330 and lies within 1e-12 of 0.57480483303961.
- **P2 (control).** ref_exact.py on theta_K7_rat.txt at N = 12 gives a value within 1e-12 of 0.5745932936.
- **N1 (null, content).** ref_exact.py on lead/theta_k4.txt at N = 15 gives about 0.57413 (the K=4 value), below 0.5745, and does not reproduce P1.

## Verdict
HOLD if P1, P2 and N1 all pass; FAILED otherwise. Failures are kept.

## Not claimed
- That the order-7 input is optimal.
- The generalized Blahut-Arimoto derivation, which is empirical only. It does not matter for validity, because any rational theta gives a valid bound (PROOF-LB1 Lemmas 1-3).

## Seal fields
- formula_ref: PROOF-LB1.md:11-17
- calibrated_on: none - the windows are the disclosed certified values, which an independent exact evaluation must reproduce
- depends_on: fac3ef4afd
- null_not_symmetry: N1 swaps in a different input law, not a relabelling
- target_form: rigorous lower endpoint of an interval enclosure
- parameters: K = 7, N = 12 and 15; null K = 4, N = 15
- instruments: theta_K7_rat.txt, ref_exact.py
- tolerances: 1e-12 agreement between two exact evaluators
- ceiling: a certified lower bound on C
- toy_model: K = 4 (PROOF-LB1)
