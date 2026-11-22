# PROOF-LB1-ADDENDUM-AUTOMATON: the floor proof for run-length automaton inputs

Written by the lead; refereed in REFEREE-PAPER1.md (CORRECT WITH FIXES; fixes applied below). PROOF-LB1.md is unchanged; this file extends it from order-K Markov inputs to finite-state (automaton) inputs, as used by build-lb5/fL6_10_8_6.txt.

## In plain words
The floor proof never used that the input remembers "the last K symbols". It only used that the input is produced by a finite hidden state that is stationary, does not see the channel's noise, and that the state together with the ball in the box forms a Markov chain. A run-length automaton has all three properties, so the same three lemmas apply word for word with a bigger hidden state.

## Setting
Input automaton: finite state set Q, next input X_t ~ p(.|q_{t-1}) with rational probabilities, deterministic update q_t = f(q_{t-1}, X_t). For the run-length automaton, q = (v, a, r1, r2) with the update in build-lb2/trapcommon.py:95-115 (the blind referee re-implemented it from a word description: referee/push1/td_ln.py).

## Changes to PROOF-LB1.md
- **Hidden state.** H_t = (q_t, S_t). (H_t) is a Markov chain: given H_{t-1}, the next input depends only on q_{t-1}, the channel's coin is fresh, and (q_t, S_t, Y_t) are functions of (H_{t-1}, X_t, coin). Any stationary law pi works; uniqueness is not required. Here pi is in fact unique: the referee found exactly one closed class (1840 of 1920 states; 80 transient with mass 0; referee/push1/out_real_L10_12.txt), and the kernel's exact solve is nonsingular. Start H_0 ~ pi, so the input process is stationary.
- **Lemma 1 (unchanged).** The channel's coins B_t are independent of H_0 and of the input's own randomness (under pi the input is correlated with S_0, which is allowed), and S_{t-1} is a function of (S_0, X^{t-1}, Y^{t-1}) (unifilar), so H(Y^n | X^n, S_0) = n Pr(X_t != S_{t-1}) under pi.
- **Lemma 2 (same proof).** Given H_0, the output future depends on the past only through H_0 because H is Markov and Y_t is a function of (H_{t-1}, X_t, coin). Hence H(Y) >= H(Y_N | Y^{N-1}, H_0) for every N (Birch's bound).
- **Lemma 3 (unchanged).** P(x^n | S_0 = s) under pi is an admissible input law for each s; the rest of the argument does not use the form of the input.
- **Computation.** L_N = H(Y_N | Y^{N-1}, H_0) - Pr(X != S). The backward kernel build-lb3/cert_backward2.py (refereed in REFEREE-LB4.md) takes the automaton through trapcommon.load_input. The blind evaluator matches it at N = 11 and 12 to about 3e-17 (BAR-PUSH1, P2).

## Credit
Run-length (residual-run) hidden states for certified lower bounds appear for the deletion channel in arXiv 2609.24908 (Khodaiemehr, Feng, Duman; ABSTRACT read). Certified Birch bounds for finite-state inputs appear in arXiv 2609.19412 (Papailiopoulos; OPENED). The Birch bound itself is classical (J. J. Birch 1962; Cover-Thomas Lemma 4.5.1, TEXTBOOK).
