# PROOF-LB1: C_trapdoor >= 0.5741292 (proof note; status PROOF DRAFT refereed CWF)

Written by the lead after REFEREE-LB1.md (verdict: V1-V3, V5 CORRECT; V4, V6 CORRECT WITH FIXES; V7 wording WRONG, fixed here). RESULT-LB1.md is kept unchanged; this file supersedes its plain-words paragraph.

## Statement
The feedforward (no-feedback) capacity of Blackwell's trapdoor channel satisfies C >= 0.574129234755855 bits per use.

## Plain words (referee's corrected wording)
The trapdoor channel's capacity without feedback is at least 0.5741292 bits per use. The witness is an order-4 Markov input law whose information rate is certified at or above that value; by the standard theorem for channels that forget their initial state, the unknown starting ball does not lower the capacity. The rate is reached by codes whose existence the theorem guarantees, not by sending the Markov source as it stands. Both published estimates of C (0.572, Kobayashi; 0.57246, arXiv 2301.00621) lie below this proven achievable rate: a correction to estimates, not to theorems.

## Proof chain
Channel (1911.02113 Sec. V-A, OPENED): y_t = x_t or s_{t-1} with probability 1/2 each when they differ (y_t = x_t when equal); s_t = x_t XOR y_t XOR s_{t-1}.
- **Lemma 0 (indecomposable).** For every x_1 the state s_1 = x_1 has positive probability from both initial states, so the channel is indecomposable (1911.02113 Def. 1 and remark; verified by the referee). By Gallager's theorem (1911.02113 Thm 1, citing Gallager Ch. 4.6; TEXTBOOK, not opened) C = lim_n a_n(s) for each s, where a_n(s) = max_P (1/n) I(X^n;Y^n | S_0 = s), and C is the operational capacity (Gallager Ch. 4.6/5.9, TEXTBOOK).
- **Lemma 1.** Let the input be the stationary order-4 Markov law theta (lead/theta_k4.txt), independent of the channel noise. Given (X^t, Y^{t-1}, S_0) the state S_{t-1} is determined (unifilar), so H(Y^n | X^n, S_0) = sum_t Pr(X_t != S_{t-1}) = n * pxs exactly, and H(Y^n|X^n) differs from it by I(S_0;Y^n|X^n) in [0,1].
- **Lemma 2.** With H_0 the full hidden state (context, s): H(Y) >= H(Y_N | Y^{N-1}, H_0) for every N (output past and future independent given H_0).
- **Lemma 3 (unknown start).** For each fixed s, P(x^n | S_0 = s) from the stationary law is an admissible input law, so (1/n) I(X^n;Y^n|S_0) <= max_s a_n(s). Also I(X^n;Y^n|S_0) >= I(X^n;Y^n) - H(S_0) >= I(X^n;Y^n) - 1. Letting n -> infinity and using Lemma 0: C >= lim (1/n) I(X^n;Y^n) = H(Y) - pxs >= L_N.
- **Computation.** L_14 in [0.57412923475585527543 +/- 4.26e-21] (lead, cert_lb.py, exact rationals + arb 128 bits); independently [0.5741292347558552754342582 ...], width 8.5e-45 (referee ref_exact.py, integer arithmetic + mpmath iv). Lower endpoint - 0.574129234755855 = 2.754e-16 > 0 (exact comparison, referee). POST HOC: L_15 >= 0.5741329179, L_16 >= 0.5741345293.

## Fixes owed (from the referee), status
- Printed endpoint rounded down, explicit uniqueness assert for pi: to go into cert_lb2.py (new file; cert_lb.py is sealed).
- P2 of BAR-LB1 was an instrument check, not content (L_N is non-decreasing for any stationary hidden chain): noted.
- Gallager Ch. 4.6 and 5.9: TEXTBOOK, not opened. Ask the owner for the text to upgrade to OPENED.
