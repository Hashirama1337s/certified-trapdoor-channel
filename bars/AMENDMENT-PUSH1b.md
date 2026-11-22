# AMENDMENT-PUSH1b: a live content null for the floor (follow-up to BAR-PUSH1 N2)

Written and sealed by the lead before the run below.

## Why
The blind referee ran N2 of BAR-PUSH1 on the first line of the input file, key (1,1,1), as the lead's brief said. That key has zero stationary mass, so the perturbation cannot move L_11, and it did not (difference 0). BAR-PUSH1 is scored on its own terms; this amendment does not rescue it. Two live-key runs already exist and are NOT used here: the referee's key (1,3,1) (POST HOC) and the lead's key (4,3,3), which ran before its amendment PUSH1a could be sealed (VOID, logged).

## Prediction
- **N2b.** referee/push1/td_ln.py (sha256 7941fe3ee5ff90e4b945072d14da89c8efd21bb84cd81afc760bdc56ec29db3e), run by the lead on runs/push1b/fL6_pert_644.txt (sha256 dd30dd7f55037fca4e9170e7d7edc92ce483f7801aa786924da4788ecf1791b1; the input with key (6,4,4) changed from 16689/25000 to 66757/100000, i.e. +1/100000; the key is not among the referee's listed zero-mass keys (a,1,1), (a,1,2)) at levels 10,11, gives an L_11 that differs from the referee's unperturbed L_11 = 0.5745010139654546250372718133665959694962 by more than 1e-12 in absolute value.

## Verdict
HOLD if N2b passes; FAILED otherwise. Together with P1, P2, P3, N1 of BAR-PUSH1 this decides whether the new interval is quoted as sealed.

## Seal fields
- formula_ref: PROOF-LB1.md:11-17
- calibrated_on: none
- depends_on: 2cbf9db44e
- null_not_symmetry: perturbs one live transition probability
- target_form: absolute difference of two rigorous values
- parameters: key (6,4,4), +1/100000, N = 11
- instruments: td_ln.py, fL6_pert_644.txt
- tolerances: 1e-12
- ceiling: content control for the floor evaluator
- toy_model: BAR-PUSH1 N2
