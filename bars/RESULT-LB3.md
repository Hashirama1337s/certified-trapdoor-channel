# RESULT-LB3 (BAR-LB3 0f9368dea6): FAILED (P1 as worded); P2, P3, N1 pass

Outputs in runs/lb3/.
- P1: FAILED as worded. cert_backward.py N=13 printed lower endpoint 0.57476380405798; ref_exact.py 0.5747638040582420981764693. The difference, 2.62e-13, exceeds the sealed tolerance E + 1e-15 = 2.558e-13. The bar did not budget for cert_backward truncating its printed endpoint to 14 decimals (up to 1e-14). The computed value cert_backward prints before subtracting E is 0.5747638040582421, which agrees with ref_exact to about 2e-18. That is a lead's wording slip, not a content disagreement, but the bar is scored as written.
- P2: PASS. cert_lb.py N=13 [0.57476380405824209818 +/- 3.54e-21] agrees with ref_exact to about 1e-20. The first launch omitted the PREC argument and crashed before computing; that log is kept as p2_certlb_N13_missing_prec_arg.out.
- P3: PASS. Lead re-run of cert_backward.py at N=24: 0.57492740773049 (E 7.079e-13).
- N1: PASS. Order-4 law at N=14: 0.57412923475556, which agrees with the BAR-LB1 value 0.5741292347558 within E.

Status of the N=24 floor 0.57492740773049: proven given assumption A2 (library log2 accuracy); see REFEREE-LB3.md. It is NOT quoted as proven. A clean bar follows when build-lb3 (proven log, A1 only) reports.
