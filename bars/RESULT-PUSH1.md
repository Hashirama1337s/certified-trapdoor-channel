# RESULT-PUSH1: scoring of BAR-PUSH1 (seal 2cbf9db44e) and its amendments

Written by the lead from the run outputs. Verdict as sealed: **FAILED** (one control could not fire). Every value check passed.

## In plain words
The new floor and ceiling both reproduced. The floor gave the same certified value with two different chunk sizes, and a blind referee's exact evaluator matched it at depths 11 and 12. The ceiling passed both verifiers, and a copy claiming one unit less failed. One planned control perturbed a state the input recipe never visits, so it could not move the result: that item failed, and so does the bar. A first replacement control ran before its seal (void). A second replacement control, sealed before its run, passed.

## Items
| item | prediction | measured | verdict |
|---|---|---|---|
| P1 | nb = 14 endpoint within 1e-13 of 0.57493196741521 | 0.57493196741521 (identical) | HOLD |
| P2 | blind evaluator within 3e-13 of the kernel at N = 11, 12; endpoints below | L_11 = 0.5745010139654546250..., L_12 = 0.5747012967683128254...; differences about 2.5e-17; endpoints 0.57450101396525 and 0.57470129676808 below | HOLD |
| P3 | verify_collapsed PASS; ref_ub3_verify 12-dp value <= 0.574968285761 | PASS; 0.574968285761 (15 dp 0.574968285760847) | HOLD |
| N1 | claim 0.574968285760 must FAIL | FAIL, exit code 1 | HOLD |
| N2 | perturbed law moves L_11 by more than 1e-9 | perturbation at key (1,1,1), a state with zero stationary mass: change exactly 0 | FAILED |
| PUSH1a | replacement control at key (4,3,3) | ran before its seal was recorded; change 9.1e-10 kept as an unsealed observation | VOID |
| N2b (amendment 086dd515e0) | key (6,4,4) +1/100000 moves L_11 by more than 1e-12 | change 9.622e-11 | HOLD |

## Files
transcripts/push1/p1_fL6_N24_nb14.log, transcripts/push1/p3_verify.out, transcripts/push1/n1_verify.out, transcripts/push1/p3_ref.out, transcripts/referee-push1/out_real_L10_12.txt, transcripts/referee-push1/out_null_N2_L10_11.txt, transcripts/push1b/out_pert_644.txt.
