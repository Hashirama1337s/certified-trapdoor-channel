# RESULT-LB2 (BAR-LB2 a2847556a8): HOLD 3/3

Independent evaluator referee/lb1/ref_exact.py (integer arithmetic + mpmath intervals), outputs in runs/lb2/:
- P1: theta_K7_rat.txt, N=15: L_N in [0.5748048330396107077870222 +/- 1.4e-44]. Lower endpoint >= 0.5748048330 and agrees with cert_lb.py (0.57480483303961070779) to ~1e-20. PASS.
- P2: N=12: 0.5745932935620149554521 (cert_lb.py 0.57459329356201495545). PASS.
- N1: theta_k4.txt, N=15: 0.5741329179 < 0.5745 (matches the post hoc L_15 in PROOF-LB1). PASS.
- An earlier launch failed on a wrapper error (memcap needs the interpreter named) and ran nothing; its logs are kept in runs/lb2/failed_launch/.

Statement: C_trapdoor >= 0.574804833039610 (rounded down), witness build-lb/theta_K7_rat.txt (sha 7126905a...). The proof chain is PROOF-LB1 Lemmas 0-3, which hold for any rational stationary Markov input.
