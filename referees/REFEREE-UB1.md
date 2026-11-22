# REFEREE-UB1: hostile referee, TRAPDOOR upper side (build-ub)

Referee seat, 2026-11-21. I did not open blind-ub/. Scripts and outputs are in referee/ub1/ (ref_bf.py, mkmut.py, eu_test.py, verify_rerun.out, bf_main.out, bf_extra.out).

## In plain words
The proof that each certificate file gives a true ceiling on the trapdoor channel's capacity holds up. I re-derived every step and found no gap. The step that bounds every possible input sequence, with no feedback, is legitimate: the checked inequality holds at every state and for both inputs, so it holds along any fixed input sequence. I wrote my own channel and my own brute force. It reproduces the verifier's rate to within 1e-12 and confirms the summed inequality, nearly tight, for every input block. The d = 2 control is an exact equality, which rules out an off-by-one. I found nothing wrong. The fixes are wording and a weak tripwire. The method itself is published (duality bound plus Bellman, 1911.02113 and 2303.18008). What is new is only that the evaluation is certified.

## Verdicts

**A2, the capacity notion and Fano at a fixed s0: CORRECT WITH FIXES.** nR = H(W) <= I(W;Y^n|s0) + 1 + P_e nR is standard, and data processing W -> X^n -> Y^n holds given s0. The bound (*) is uniform in s0, so it covers every operational variant. Unknown or random s0: I(W;Y^n) <= I(W;Y^n,S0) = I(W;Y^n|S0), because W is independent of S0. Adversarial s0: a code that works for all s0 works for s0 = 0. Encoder-only knowledge of s0: the same inequality applies. Fix: replace "a fixed known s0 is the strongest case" with "(*) is uniform in s0, hence covers known, unknown, random or adversarial s0", and spell out the line I(W;Y^n) <= I(W;Y^n|S0).

**Step 1, the dual bound: CORRECT.** For any P_X and R > 0: sum_x P(x) D(P_{Y|x}||R) = I + D(P_Y||R), so I <= max_x D. This is elementary and does not depend on a cited theorem.

**Step 2, the Q-graph test law: CORRECT.** The verifier asserts 0 < T0 < 1, sets T1 = 1 - T0 exactly, and checks that phi stays in range. Any start node q0 is allowed, because h covers every node.

**Step 3, the unifilar chain rule: CORRECT.** With x^n fixed, S_{t-1} is a function of (s0, x^{t-1}, y^{t-1}). Also s' = x XOR y XOR s matches the physical channel: y = x leaves s in the box, and y = s leaves x. I checked this independently. My brute force computes D path by path without the chain rule, and my own float Bellman rate agrees with the verifier (diff 8.556e-13 at d = 4, 6.432e-13 at d = 8).

**Step 4, the augmented state and padding (attack b): CORRECT.** W_j = (S_j, x_{j+1..j+d-1}, Q_j). The reward uses c = x_{j+1} = xs[0] and T(.|Q_j), consistent with R(y_t) = T(y_t|q_{t-1}) (attack d; verify_u2b.py lines 111-115). The sharp test is ref_bf.py. For every s0, every q0, every x^n and every padding it checks the exact telescoped form D <= n*rho + h(W_0) - E h(W_n), with W_0 built from the actual x_1..x_{d-1}.
- d = 2 snapped, n = 12, all q0: slack lies in [1.012e-11, 1.013e-11] for all inputs, which is n x (verifier round-up). This is an identity, as the all-tight hand derivation below predicts. Any shift in the pending-input window or the reward time would break it.
- d = 4, n = 12, all q0: min slack 6.945e-09, VERDICT OK. n = 14, q0 = 0: min slack 6.949e-09, OK. n = 10: 3.463e-09.
- d = 8 (k = 7), n = 11, q0 = 0: min slack 1.727e-11, OK.
- Negative controls, run in the same batch: d = 4 with rho - 1e-4 gives VIOLATION (-1.000e-03). A mutated T scored with the original rho gives VIOLATION (-4.355e-01). The test can fail.

**Step 5, the Bellman supersolution and telescoping (attack a): CORRECT WITH FIXES.** rho_cert is a max over every state and both actions, so the inequality holds at whatever W_j occurs; reachability is irrelevant. Given Y^j, W_j is deterministic because the inputs are open-loop, so conditioning is legitimate. The bound in fact controls the delay-d feedback dual (C <= C_d^fb <= rho_cert); open-loop inputs are one admissible policy, so bounding the feedforward capacity this way is valid. Fixes:
(i) Add to NOTES: "W_j is Y^j-measurable because x^n is fixed."
(ii) Add: "rho_cert also upper-bounds C_d^fb."
(iii) For d = 1, the d = 1 run is consistent with this: 0.704837047948 >= log2 golden 0.694241913631.

**d = 2 closed form, by hand: CORRECT.** phi(q,y) = y; T(y|q) = 2/3 if y = q, else 1/3; h = 1 at (s,x,q) = (0,0,1) and (1,1,0), else 0. Rewards: c = s = q gives L-1, where L = log2 3; c = s != q gives L; c != s gives L - 3/2.
- (0,0,0) and (1,1,1): L-1 + 0 - 0.
- (0,0,1) and (1,1,0): L + 0 - 1.
- The four c != s states: L - 3/2 + 1/2 - 0. The two equally likely outputs lead to (1,a,0) and (0,a,1) when s = 0, or to (0,a,1) and (1,a,0) when s = 1, and exactly one of them has h = 1 for either action a, so E h = 1/2.
All 16 residuals equal L - 1 = log2(3/2) exactly. The verifier reports 0.584962500722 (1.727e-77 above the arb upper endpoint of log2(3/2)).

**Verifier arithmetic (attack e): CORRECT.**
- The D formulas are right: point mass gives -log2 T(c|q); uniform gives -1 - (log2 T0 + log2 T1)/2.
- The loops cover all 2 x 2^(d-1) x 2^k states and both actions.
- h and T are exact Fractions.
- exact_upper returns >= every ball point. Tested in eu_test.py: the upper endpoint exceeds the midpoint by the radius (3.45e-77), and holds for both signs.
- Decimals are rounded with a ceiling.
- I re-ran verify_rerun.out and reproduced 0.576476036830 (d = 4), 0.575232734724 (d = 8) and 0.584962500722 (d = 2).
- Mutants:
  - Lowering h[198] by h_den//100 raises rho to 0.586476036829, i.e. by 0.01.
  - Setting T0[6] = 1/2 gives 0.835579214749.
  - The brute force with each mutant's own rho gives OK (min slack 9.000e-02 and 2.156e+00).
  - So a bad file gives a weaker bound, never a false one.

**Shipped numbers C <= 0.575232734724 (d = 8, k = 7) and C <= 0.576476036830 (d = 4, k = 4): CORRECT** as certified upper bounds, given the trusted base (arb log enclosures, Fractions). This is pending the blind re-implementation under BAR-UB1, which I did not see.

**U1, log2(3/2) in Q(L) (read plus log only): CORRECT.** The multiplier argument is right: sum_i lambda_i beta_i . z <= max_i beta_i . z, and span <= 1 because beta = {e01, e10}. The negative control fails, exit 1. The result itself is 1911.02113 Thm 7: OPENED, sec. V-A, "Theorem 7. The capacity of the trapdoor channel is upper-bounded by Ctrapdoor <= log2 3/2."

**Tripwire check_telescoping.py: CORRECT but WEAK.** It uses q0 = 0 only and the loose span bound, which has slack 0.268-0.36 at d = 4, n = 10-14. It cannot see a per-symbol error below about 0.03. Fix: replace it with the tight form in referee/ub1/ref_bf.py.

**Prior-art framing: CORRECT WITH FIXES.**
- 2303.18008 (OPENED, eq. (17) and lines 667-668): "these simulations suggest that the feedforward capacity satisfies C ≤ 0.5765."
- 1911.02113 (OPENED, intro line 107): "for any test distribution defined on a Q-graph, the evaluation of this multi-letter expression can be formulated as an infinite-horizon average-reward dynamic programming (DP) problem."
- So the duality, Q-graph and Bellman route, and the delayed-feedback extension, are theirs. Any write-up must say that only the certification and the d = 5..8 evaluations are ours.
- d = 4 at 0.576476 is a certified version of their 0.5765, not a new bound.

## What blocks release
1. BAR-UB1, the blind re-verification, is not yet scored.
2. The NOTES wording fixes (A2, Step 5) and the tight tripwire.
3. The write-up must credit the method to 1911.02113 and 2303.18008.
Nothing in the mathematics blocks the claim. The lab's lower bound 0.5741292 (RESULT-LB1, theory step not refereed here) sits consistently below 0.575232734724.

## Single next strike
Score BAR-UB1 (blind verifier on d = 8, d = 4 and the controls). Then add ref_bf.py's tight check (d = 2 identity; d = 4 slack >= 0) as a sealed control in the release bar.
