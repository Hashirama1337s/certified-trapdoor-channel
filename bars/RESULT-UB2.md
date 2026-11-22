# RESULT-UB2 (BAR-UB2 4174b6d291): HOLD 4/4

Lead re-run on the lead's machine; outputs in runs/ub2/.
- Q1: blind check_ub.py on the (10,10) lift certificate: rho_up 0.575092822039761 (arb and iv agree). PASS.
- Q2: on (8,8): 0.575140726012508. PASS.
- Q3: control (4,4): 0.576476036829145, the same as BAR-UB1. PASS.
- N1: (8,8) certificate with T0[node 0] raised by 0.01 (0.6712 to 0.6812), checked by verify_u2b.py: 0.619702255187, larger than Q2. PASS.

Statement: C_trapdoor <= 0.575092822040 (rounded up). Certificate build-ub2/certs/cert_u2b_d10_k10_lift_d9k9b1e6.json (sha e55f668e...), proof chain PROOF-UB1.
Certified interval now: 0.574804833039 <= C <= 0.575092822040 (width 2.880e-4).
