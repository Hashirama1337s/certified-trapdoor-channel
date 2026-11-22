> Saved by the lead from the hand-back (seat a825801c, 2026-11-22). The text below is the seat's report verbatim.

# REFEREE-LB3: cert_backward.py, ERROR-LEMMA.md, and the floor C >= 0.57492740773049

Seat: hostile referee. Files judged: build-lb2/cert_backward.py (sha 4c58774b...), trapcommon.py (01464639...), ERROR-LEMMA.md (20b95acf...), s9_d100000_z0.0005.txt (24b31a62...). The hashes match SEALS-LB3.txt. No existing file was modified.

## In plain words
The program computes the right quantity. My own evaluator, written from the definition with a different channel model, a different way of getting the stationary law and a different entropy formula, matches it to about 1e-16 on four new law/depth pairs, both with and without chunking. A perturbed law moves the value by 1.3e-10, so the comparison is able to fail. The rounding-error lemma is sound for the operations the code actually performs. The one real gap is Assumption A2 (the library log2 is accurate to 2^-48 relative), which is tested but not proven. So the 14-digit N = 24 value is "proven given A2", not proven outright. A2 can be weakened by a factor of about 2^20 and the floor still stays above 0.5749, and it can be removed entirely with a log routine that uses only +, *, / (see item 3).

## Item 1: the code computes PROOF-LB1's L_N. CORRECT
Line-by-line check:
- Channel: if x = s then y = s and s' = s. If x != s then y is 0 or 1 with probability 1/2 each and s' = x^y^s, so s' = s when y = x and s' = x when y = s. This is the bag model.
- Hidden state: h = 2c+s, with c the last K inputs (newest bit is the least significant, same as the file's strings, which list the oldest bit first). H_0 = (C_0, S_0), as Lemma 2 needs.
- pi: exact flint solve, then pi P = pi checked on every entry. A singular system (non-unique law) raises an error.
- pxs = sum_h pi_h Pr(X != s | h). This is Pr(X_t != S_{t-1}), as in Lemma 1.
- Word order: inside a leaf, the column index has the last-in-time symbol as its least significant bit. So `Bl[:,0::2]+Bl[:,1::2]` sums out Y_N and gives Pr(Y^{N-1}|h), not Pr(Y_2^N|h). A wrong order would change the value, and my evaluator conditions on Y^{N-1} explicitly, so the match on four new pairs (below) checks this.
- Entropies are conditioned on H_0 ~ pi, and states with pi_h = 0 are skipped (they carry zero weight).
- Side note: many states are transient because the laws have exact zero entries. pi > 0 on 440/1024 states (order 9), 256/512 (order 8) and 148/256 (order 7). This is harmless, and both codes agree on it.

## Item 2: the error lemma covers the actual operations. CORRECT WITH FIXES (wording only)
I re-derived steps (a)-(e) and E. My exact recomputation (e_vs_lambda.py) gives E(24, 2^-48) = 7.0788e-13, and the build log prints 7.079e-13.
- Products and sums: each step makes three roundings (coefficient, product, sum) on non-negative terms, giving eps_n = (1+u)^{3n} - 1. Correct. The zero pattern is exact.
- f(p) = -p log2 p near 0: exact zeros give 0 * log2(2^-1000) = -0, which is exact. Positive values are covered by the relative-error form. Near 1: this regime does not occur. The largest beta-tilde is 4.6e-4 at N = 24 and 0.082 at N = 11.
- The 2^N-term sum is pairwise: depth nb + (N-nb) = N for H_N, and (nb-1) + (N-nb) plus one pre-addition for H_{N-1}. The bound gamma_N * sum|t| is correct.
- Cancellation: H_N - H_{N-1} is formed in exact rationals and E is an absolute bound on each H, so no loss goes uncounted.
- Underflow and subnormals: none occur. The smallest positive beta-tilde is 3.1e-16.
- Rational combination: exact fmpq, and |L~ - L| <= E because pi >= 0 and sums to 1.
- Fix 1. Check C1 asserts only on leaf arrays. Intermediate beta values and the products a*b are never checked. Replace the check by the a-priori fact: every positive coefficient is >= 1/(2*den) = 5e-6, so every positive intermediate or product is >= (5e-6)^(N+1), about 1e-133 at N = 24, which is far above 2^-1022.
- Fix 2. State A2 only on the input range that occurs ([3.1e-16, 4.6e-4] at N = 24). That keeps it away from the near-1 regime, where relative accuracy of log is the most fragile.
- Measured slack: the actual error is <= 3e-16 against E of about 2e-13, roughly 700x.

## Item 3: Assumption A2. GAP (not proven; easy to shrink, removable)
- The seat's test and my side test agree: 1.1e-16 on ~8,000 real beta values from my runs (max 1.103e-16). Neither is a proof.
- This machine reports AVX and AVX2 only (numpy 2.4.4). I did not determine which log2 implementation numpy dispatches to, and none of them documents an error bound.
- Fix A (safety factor, immediate): E is affine in lambda.
  - lambda = 2^-28 gives the endpoint 0.57492723264201.
  - lambda = 2^-24 gives 0.57492460631235.
  - Any lambda <= 2^-20.71 keeps the endpoint >= 0.5749, and any lambda <= 2^-22.60 keeps it >= 0.57492.
  - So the claim can rest on "log2 is good to about 2^-24 relative", about 2^29 ULP of slack. This is still an assumption, but a negligible one.
- Fix B (proven, A1 only): replace np.log2 with x = m*2^e from frexp (exact), plus ln m = 2 atanh((m-1)/(m+1)) on [sqrt(1/2), sqrt 2), truncated at a proven term count. Alternatively use chord and tangent bounds of the concave log2 on a 2^16-bin table whose end values are certified with arb. Both need only IEEE +, *, /, and the error analysis fits on one page.
- A full arb re-evaluation at N = 24 is not practical (about 7e9 logs).

## Item 4: the printed endpoint is rounded down. CORRECT
floor_dec applies math.floor to the exact Fraction Lf - E, and E is evaluated in exact rationals. For negative inputs the output string is still <= the true value.

## Independent check (referee/lb3/ref_lb3.py: integer arithmetic plus arb balls at 320 bits)
| law, N | ref_lb3 ball | cert_backward L~ (16 digits, rounded down) | diff | E |
|---|---|---|---|---|
| k4, N=14 (positive control) | 0.574129234755855275434258216935 +/- 2.12e-31 | PROOF-LB1: 0.57412923475585527543 | <1e-20 | - |
| s8, N=12, nb=12 / nb=5 | 0.574655528577903154741 +/- 3.4e-32 | 0.5746555285779034 / ...9032 | 2.5e-16 / 4.5e-17 | 2.243e-13 |
| s9, N=11, nb=11 / nb=5 | 0.574423804813292196092 +/- 2.2e-32 | 0.5744238048132922 / ...2919 | 4e-18 / -3.0e-16 | 1.955e-13 |
| s9, N=13 | 0.574763804058242098176 +/- 1.8e-31 | 0.5747638040582421 | 2e-18 | 2.548e-13 |
| s7, N=14, nb=7 | 0.574803850691004801058 +/- 5.5e-32 | 0.5748038506910047 | -1e-16 | 2.871e-13 |
| s9, N=11, theta(0) + 1e-5 (null) | 0.574423804687188145667 | (unperturbed) 0.5744238048132922 | 1.26e-10 | DISAGREES, as it should |

Every cert_backward endpoint lies below my rigorous lower endpoint. Without A2, the exact value L_13 >= 0.574763804058242098 is proven by my evaluator for the order-9 law.

## What blocks release
1. Calling 0.57492740773049 "proven" is blocked while A2 stands (doctrine rule 3). Either quote it as conditional on A2, or apply Fix A and quote 0.57492 (log2 accuracy assumption 2^-22.6), or do Fix B for an unconditional value.
2. NOT CHECKED: I did not re-run N = 24 myself. That is BAR-LB3 P3, the lead's re-run.
3. Gallager Ch. 4.6/5.9 is still TEXTBOOK (carried over from PROOF-LB1).

## Single next strike
Implement Fix B (frexp plus an atanh series with a written error bound, A1 only) as a new kernel log. Re-run s9 at N = 24, and confirm agreement with ref_lb3 at N = 11-13.

## Outputs (referee/lb3/)
ref_lb3.py, e_vs_lambda.py, e_vs_lambda.out, posctl_k4_N14.out, ref_s8_N12.out, ref_s9_N11.out, ref_s9_N13.out, ref_s7_N14.out, null_s9_N11_perturb.out, cb_s8_N12.out, cb_s8_N12_nb5.out, cb_s9_N11.out, cb_s9_N11_nb5.out, cb_s9_N13.out, cb_s7_N14_nb7.out.
