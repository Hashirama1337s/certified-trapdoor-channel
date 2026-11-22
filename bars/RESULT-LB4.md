# RESULT-LB4 (BAR-LB4 1e18a4dca9): HOLD 3/3

Outputs in runs/lb4/.
- R1: lead re-run, order-9 law at N=24 (--nb 15): 0.57492740773047, E 7.227e-13. PASS.
- R2: N=12: cert_backward2 0.57464550926487; ref_exact [0.5746455092651053816...]. The endpoint is below exact by 2.35e-13, within E + 1e-14 + 1e-15 = 2.425e-13. PASS.
- N1: order-4 law at N=14: 0.57412923475555, inside [0.5741292347550, 0.5741292347559]. PASS.

Referee REFEREE-LB4: CORRECT / CORRECT WITH FIXES (wording fix in build-lb3/ERROR-LEMMA2-FIX.md, number unchanged).

Statement: C_trapdoor >= 0.57492740773047, assuming correctly rounded binary64 + - * / (A1), plus the textbook step of PROOF-LB1 (Gallager Ch. 4.6).

Interval with REFEREE-UB3: 0.57492740773047 <= C <= 0.574968594275 (width 4.12e-5).
