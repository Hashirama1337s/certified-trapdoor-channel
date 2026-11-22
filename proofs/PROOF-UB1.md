# PROOF-UB1: C_trapdoor <= 0.575232734724 (status: PROOF DRAFT refereed CWF, arithmetic blind-verified)

Written by the lead after REFEREE-UB1.md (all steps CORRECT or CORRECT WITH FIXES, nothing blocks the mathematics) and RESULT-UB1.md (BAR-UB1 d110ac48e8 HOLD 5/5, blind re-implementation to 15 digits).

## Statement
The feedforward (no-feedback) capacity of Blackwell's trapdoor channel satisfies C <= 0.575232734724 bits per use (certificate build-ub/certs/cert_u2b_d8_k7.json, sha256 27ca42bb07b6...). Also C <= 0.576476036830 (d = 4), the certified version of the simulated 0.5765 of arXiv 2303.18008.

## Credit (method is published)
The duality upper bound with test distributions on Q-graphs and its evaluation as an average-reward dynamic program are from Huleihel, Sabag, Permuter, Kashyap, Shamai (arXiv 1911.02113); the delayed-feedback extension, the transformed state (S_{t-d}, X_{t-d+1..t-1}) and the simulated 0.5765 are from 2303.18008. Ours: rigorous certificates (exact rationals + arb), their independent verification, and the evaluations at d = 5..8.

## Proof chain (fixes from the referee folded in)
1. Fano + data processing: nR <= I(W;Y^n|s0) + 1 + P_e nR for every s0. Since W is independent of S0, I(W;Y^n) <= I(W;Y^n,S0) = I(W;Y^n|S0), so the bound covers known, unknown, random or adversarial s0.
2. Dual bound: for any output law R > 0, I(X^n;Y^n|s0) <= max_{x^n} D(P_{Y^n|x^n,s0} || R) (elementary identity sum_x P(x) D = I + D(P_Y||R)).
3. R from the Q-graph test law: R(y^n) = prod_t T(y_t | q_{t-1}), any start node.
4. Chain rule: with x^n fixed, S_{t-1} is a function of (s0, x^{t-1}, y^{t-1}) (unifilar), so D splits into per-step rewards.
5. Augmented state W_j = (S_j, x_{j+1..j+d-1}, Q_j); W_j is a function of Y^j because x^n is fixed. rho_cert is a max of the Bellman residual over ALL states and both actions, so telescoping gives D <= n rho_cert + h(W_0) - E h(W_n), hence C <= rho_cert. (rho_cert also bounds the delay-d feedback capacity; a fixed input sequence is one admissible policy.)

## Independent checks
- Referee brute force (referee/ub1/ref_bf.py, own channel, path-by-path D): d = 2 slack identity 1.01e-11 for every input; d = 4, n = 10-14, all start nodes: min slack 6.9e-9; d = 8, n = 11: 1.7e-11; negative controls (rho - 1e-4, mutated T) VIOLATE.
- Blind verifier (blind-ub/check_ub.py): d = 8 0.575232734723357, d = 4 0.576476036829145, d = 2 = log2(3/2), d = 1 above log2 golden ratio; every single-entry lowering of h raises rho by ~1/100.
- Hand derivation of the d = 2 closed form: all 16 residuals equal log2(3/2) exactly.

## Fixes still owed
NOTES.md wording (A2, step 5) is superseded by this file; replace the weak tripwire check_telescoping.py with the tight form of ref_bf.py in any release bar; never quote solver_info.cvx_rho (it is below the certified value and not a bound).
