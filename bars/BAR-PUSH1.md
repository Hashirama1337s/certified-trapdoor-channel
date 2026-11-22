# BAR-PUSH1: run-length floor C >= 0.57493196741521 and continued ceiling C <= 0.574968285761

Raid TRAPDOOR, push round. Written and sealed by the lead before the independent checks run.

## Disclosed before sealing
- Floor: run-length automaton input build-lb5/fL6_10_8_6.txt (caps 10,8,6; 1920 hidden states), certified by the unmodified build-lb3/cert_backward2.py. Lead run at N = 24, nb = 15: CERTIFIED LOWER ENDPOINT 0.57493196741521, E = 7.227e-13 (runs/push1/cert_fL6_10_8_6_N24_nb15_lead.log). Same kernel at N = 11: L~ = 0.5745010139654546, E = 2.021e-13; N = 12: L~ = 0.5747012967683128, E = 2.315e-13 (runs/push1/cb2_fL6_N11.log, N12.log).
- Ceiling: build-ub4/certs/cert_col_k15_cont.json, verify_collapsed.py rho_up 0.574968285761 (15 dp 0.574968285760847). Claim copy runs/push1/cert_col_k15_cont_claim.json; too-low copy negctl_k15_cont_low.json (claims 0.574968285760).
- New in kind for the floor: the input is a run-length automaton, not a Markov law. The referee checker referee/lb3/ref_lb3.py reads Markov laws only, so the floor's independent check needs a new evaluator written by a blind referee seat.

## Instruments (sha256)
- build-lb5/fL6_10_8_6.txt 833a072661459f6f3ee982438b75360b6f90c4f9f921512af0f25cfb07d3ed94
- build-lb3/cert_backward2.py a7a0ae2477ec8807eebdd6e579a65878796b3eee9e64616d1f19fb0058cd87dd
- build-ub3/verify_collapsed.py 34e9066d8b6edb1011e3af9ea2bb33734c3b87604f6ee2025ff1d668e06b8971
- referee/ub3/ref_ub3_verify.py 1b49e5e7f149ad3ff1fb31eb0ddbd93bedc1d89b962cca50a9b12988ed0ad719
- runs/push1/cert_col_k15_cont_claim.json 99a32f8db5747f2bfc70fee49445cbf87febc83722d3f989af89ca10b12eb556
- runs/push1/negctl_k15_cont_low.json 38ef3642857852072fd29aad97a26800558cd95b9ecf458dedeeac3283fe931f

## Predictions
- **P1 (floor, chunking).** cert_backward2.py on fL6_10_8_6.txt at N = 24 with --nb 14 prints a certified endpoint within 1e-13 of 0.57493196741521 (and both are >= 0.574931967415).
- **P2 (floor, independent evaluator).** A blind referee's own exact evaluator of L_N for the automaton input in fL6_10_8_6.txt (written from the channel and automaton definitions, not from cert_backward2.py or trapcommon.py) gives, at N = 11 and N = 12, rigorous values whose distance to the disclosed L~ is at most 3e-13, with the disclosed certified endpoints at or below the referee's lower ends.
- **P3 (ceiling).** verify_collapsed.py on cert_col_k15_cont_claim.json prints RESULT: PASS; ref_ub3_verify.py on the same file prints a 12-dp rounded-up value <= 0.574968285761.
- **N1 (ceiling null, content).** verify_collapsed.py on negctl_k15_cont_low.json prints RESULT: FAIL.
- **N2 (floor null, content).** The referee's evaluator on the law with one transition probability changed by 1/100000 differs from its unperturbed value by more than 1e-9 at N = 11.

## Verdict
HOLD if P1, P2, P3, N1 and N2 all pass; FAILED otherwise. Failures are kept.

## Not claimed
- That the automaton law or the order-15 test law is optimal.
- Anything about the limit of either family.

## Seal fields
- formula_ref: PROOF-LB1.md:11-17
- calibrated_on: none - windows are the disclosed certified values
- depends_on: 1e18a4dca9
- null_not_symmetry: N1 lowers the claimed number; N2 perturbs one transition probability
- target_form: rigorous endpoints (floor lower, ceiling upper)
- parameters: floor N = 11, 12, 24 (nb 14, 15); ceiling k = 15
- instruments: fL6_10_8_6.txt, cert_backward2.py, verify_collapsed.py, ref_ub3_verify.py, referee evaluator (new)
- tolerances: 1e-13 chunking; 3e-13 evaluator agreement; ceiling exact rounded-up comparison
- ceiling: certified interval on C
- toy_model: order-9 floor (BAR-LB4), k15_sm ceiling (BAR-UB3)
