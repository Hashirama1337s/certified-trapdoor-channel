# AMENDMENT-PUSH1a: a live content null for the floor (replaces N2 of BAR-PUSH1 for a follow-up score)

Written and sealed by the lead before the run below.

## Why
The blind referee ran N2 of BAR-PUSH1 on the first line of the input file, key (1,1,1), as the lead's brief said. That key has zero stationary mass, so the perturbation cannot move L_11, and it did not (difference 0). BAR-PUSH1 is scored on its own terms; this amendment does not rescue it. The referee also ran a live key (1,3,1) after seeing that, POST HOC; that run is not used here.

## Prediction
- **N2a.** referee/push1/td_ln.py (sha256 7941fe3ee5ff90e4b945072d14da89c8efd21bb84cd81afc760bdc56ec29db3e), run by the lead on runs/push1a/fL6_pert_433.txt (sha256 17db4bd9a270d19f1f4040faa7c90695e185cd0c0420025eb035cf977a9ed88e; the input with key (4,3,3) changed from 68329/100000 to 68330/100000; that key is not among the referee's listed zero-mass keys (a,1,1), (a,1,2)) at levels 10,11, gives an L_11 that differs from the referee's unperturbed L_11 = 0.5745010139654546250372718133665959694962 by more than 1e-12 in absolute value.

## Verdict
HOLD if N2a passes; FAILED otherwise. Together with P1, P2, P3, N1 of BAR-PUSH1 this decides whether the new interval is quoted as sealed.

## Seal fields
- formula_ref: PROOF-LB1.md:11-17
- calibrated_on: none
- depends_on: 2cbf9db44e
- null_not_symmetry: perturbs one live transition probability
- target_form: absolute difference of two rigorous values
- parameters: key (4,3,3), +1/100000, N = 11
- instruments: td_ln.py, fL6_pert_433.txt
- tolerances: 1e-12
- ceiling: content control for the floor evaluator
- toy_model: BAR-PUSH1 N2
