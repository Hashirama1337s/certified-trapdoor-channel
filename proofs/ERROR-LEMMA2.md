# ERROR-LEMMA2: why cert_backward2.py's printed endpoint is a lower bound on L_N, with NO library-accuracy assumption

Status: written by the build seat, NOT yet refereed. This replaces ../build-lb2/ERROR-LEMMA.md. The only change in the computation is that numpy.log2 (old Assumption A2) is replaced by the routine `log2_rig`, whose relative error is PROVED in Section 2 from IEEE +, -, *, / alone. Everything else (Sections 0, 3-5) is the old lemma with the wording fixes of REFEREE-LB3.md (Fix 1: a-priori underflow bound; Fix 2: the input range is stated).

## 0. What is certified
Identical to the old lemma. For an order-K Markov input theta (rational file), hidden state h = (context, ball), M = 2^(K+1) states, sub-stochastic matrices A_y[h,j] = Pr(Y=y, H'=j | H=h) (exact rationals, channel as in lead/cert_lb.py), exact stationary law pi, exact pxs = Pr(X != S) = sum_h pi_h w_h:

    L_N = sum_h pi_h ( H_N(h) - H_{N-1}(h) ) - pxs,   H_m(h) = - sum_{w in {0,1}^m} beta_w(h) log2 beta_w(h),   beta_w(h) = (A_{w1} ... A_{wm} 1)(h).

By PROOF-LB1.md every N >= 1 gives C >= L_N. The program prints floor_14digits(L~_N - E); L~_N is an exact rational built from float data, E is proved below. So printed <= L~_N - E <= L_N <= C.

## 1. Model of the arithmetic (the whole list of assumptions)
- A1 (IEEE). Each numpy elementwise +, -, *, / on float64 arrays is ONE IEEE binary64 operation with round to nearest (correctly rounded), no extended precision, no fused operations needed (a fused multiply-add would only reduce error; all bounds below remain valid), no flush-to-zero effect (no subnormal ever occurs, Section 3). numpy.frexp is exact (x = m 2^e, m in [1/2, 1)); multiplication or addition of floats whose exact result is representable is exact. u = 2^-53. Standard consequence used repeatedly: if a quantity is the product of factors (1 + delta_i), |delta_i| <= u_i, then its relative deviation from 1 is at most prod(1 + u_i) - 1 (the downward deviation 1 - prod(1 - u_i) is no larger, because (1+a)^n + (1-a)^n >= 2).
- Exact objects (not floats): rational theta, pi (python-flint fmpq solve, checked pi P = pi entrywise, sum 1, pi >= 0), pxs, the final rational combination, all error constants (Python Fraction). Python Fraction -> float is correctly rounded (documented CPython property).
- Constants of log2_rig: C2 = 2 * float(1/ln 2) computed from an arb ball at 300 bits and CHECKED at import by arb: |C2 - 2/ln 2| < u * (2/ln 2) (so the stored constant has relative error rc <= u; the scaling by 2 is exact). Series coefficients HC[k] = float(1/(2k+1)), correctly rounded, relative error <= u, HC[0] = 1 exactly. CTHR = 0.7071067811865476 (a float; its exact value is used in the checks, it is not claimed to equal sqrt(1/2)).
- NO assumption on numpy.log2, libm, or any vendor math library.

## 2. Lemma L (the logarithm routine)
Input: float x with 2^-1000 <= x < 2 (or x = 0, see below). Steps, each line of `log2_rig`:
1. (m, e) = frexp(x): x = m 2^e exactly, m in [1/2, 1).
2. If m < C (C = CTHR): m' = 2m, e' = e - 1; else m' = m, e' = e. Both exact (`m += m*lo`: m*lo is m or 0, m + m = 2m exact; `ef -= lo` integer arithmetic). Then x = m' 2^e' exactly and m' in [C, 2C) (for m >= C: m' = m in [C, 1); for m < C: m' in [1, 2C)).
3. d = m' - 1 is exact (Sterbenz: 1/2 <= m' <= 2). s = fl(m' + 1) = (m'+1)(1 + d_s). z = fl(d / s).
4. w = fl(z z).
5. Horner: q = HC[K-1]; for k = K-2 .. 0: q = fl( fl(q w) + HC[k] ) (two roundings per level). K = KT = 10.
6. g = fl( fl(z q) * C2 ).
7. result r = fl(e' + g) (e' is a small integer, exactly a float).
True value: log2 x = e' + log2 m'. For |z0| < 1 with z0 = (m'-1)/(m'+1): ln m' = 2 artanh z0 = 2 z0 P_inf(w0), w0 = z0^2, P_inf(w) = sum_{k>=0} w^k/(2k+1). So log2 m' = z0 P_inf(w0) (2/ln 2).

(2a) Range of z0. For m' in [C, 2C): |z0| <= ZMAX = 0.1716 and w0 <= WMAX = 0.0295. Proof: z0 is increasing in m', so |z0| <= max(|(C-1)/(C+1)|, |(2C-1)/(2C+1)|), evaluated in exact rationals at import (assert); 0.1716^2 = 0.02944656 <= 0.0295.

(2b) Truncation. P_K(w0) := sum_{k<K} w0^k/(2k+1). Then 0 <= P_inf - P_K = sum_{k>=K} w0^k/(2k+1) <= w0^K / ((2K+1)(1 - w0)) <= WMAX^K / ((2K+1)(1 - WMAX)) =: TAU. Since P_inf >= 1, P_K in [(1 - TAU) P_inf, P_inf]. TAU = 2.449e-17 for K = 10.

(2c) Rounding, factor by factor, as relative deviation bounds in the form (1+u)^n - 1:
- s: relative error u. Division by it contributes a factor 1/(1 + d_s) in [1/(1+u), 1/(1-u)]; |1/(1+d_s) - 1| <= u/(1-u) <= (1+u)^2 - 1. Division rounding: u. So z = z0 (1 + zeta) with |zeta| <= (1+u)^3 - 1. [exponent 3]
- w = fl(z z) = w0 (1+zeta)^2 (1+u): |.-1| <= (1+u)^7 - 1. [exponent 7]
- P is a polynomial with non-negative coefficients, so for a factor f in [1 - a, 1 + a], P(w0 f) is in [(1 - a) P(w0), (1 + a) P(w0)] (monomials scale by f^k, k >= 0, and P(w0 f) <= max(f,1) P(w0), >= min(f,1) P(w0)). So using w instead of w0 costs relative (1+u)^7 - 1 on P_K. [exponent 7]
- Horner levels. Let Q_k(w) = sum_{j>=k} HC_exact[j] w^(j-k) be the exact-coefficient tail polynomial with the computed w, and q_k the computed value. q_{K-1} = HC[K-1] = (1/(2K-1))(1 + delta), so rho_{K-1} <= u. Level k: q_k = ( HC[k](1+d) + w q_{k+1}(1+m) )(1+s), all terms non-negative. If q_{k+1} is within relative rho_{k+1} of Q_{k+1}, then every term inside the bracket is at most (1+rho_{k+1})(1+u) times its exact counterpart, so q_k <= Q_k (1+rho_{k+1})(1+u)^2; the lower side is symmetric. Hence 1 + rho_0 <= (1+u)^(2(K-1)+1), i.e. q_0 = P_K(w) (1 + theta), |theta| <= (1+u)^(2K-1) - 1. [exponent 2K-1]
- fl(z q): relative u, and it multiplies the factors of z (3) and of q. [exponent 1]
- g = fl(y C2): rounding u; and C2 itself has relative error rc <= u (checked), a separate factor (1+rc). [exponent 1, plus (1+rc)]
Total exponent: 3 (z) + 7 (w inside P) + (2K-1) (Horner) + 1 + 1 = 2K + 11 = 31, and the product with (1 + rc). Together with truncation (2b) (the quantity actually computed approximates P_K, which lies in [(1-TAU), 1] times P_inf):

    g = log2(m') (1 + gamma),   |gamma| <= GAMMA_LOG := (1+u)^(2K+11) (1+rc) - 1 + TAU.

(The lower side: 1 - (1-TAU)(1-A) <= TAU + A with A = (1+u)^(2K+11)(1+rc) - 1, using the convexity remark in Section 1.) Numerically GAMMA_LOG = 3.577e-15.

(2d) Final addition. Case e' = 0: r = fl(0 + g) = g exactly, relative error <= GAMMA_LOG. Case e' != 0: |e'| >= 1 and |log2 m'| <= 0.51 (m' in [C, 2C), log2 of 1.4143 < 0.5001 and log2(1/C) < 0.5001), so |e' + log2 m'| >= 0.49 and kappa := |log2 m'| / |e' + log2 m'| <= 0.51/0.49 < 21/20. Then r = (e' + g)(1+s'), and |r - log2 x| / |log2 x| <= kappa GAMMA_LOG (1+u) + u. Define

    LAMBDA := (21/20) GAMMA_LOG (1+u) + u = 3.8671e-15 (about 2^-47.88).

Lemma L. For every float x with 2^-1000 <= x < 2, x != 1: |log2_rig(x) - log2 x| <= LAMBDA |log2 x|. For x = 1 the routine returns exactly 0 (m' = 1, z = 0, g = 0, e' = 0). For x = 0 it returns some finite float (z = -1, w = 1, all finite), which is only ever multiplied by x = 0, giving exactly +-0; so t = x * log2_rig(x) = 0 = x log2 x exactly.
No assumption beyond A1 and the checked constants was used.

## 3. Range and underflow (referee Fix 1 and Fix 2)
a_min := smallest positive float coefficient among all stored a_i (computed from the rows by the program, printed in the log; for the order-9 file 1.1135e-2 = about 1/90). By induction on the recursion length n: every computed value of beta~ at length n, and every intermediate product a_f * b~, is either exactly 0 or at least a_min^n (1-u)^(3n) >= a_min^n / 2 (a positive beta needs a positive path; rounding is monotone; 3nu < 1/2). The program ASSERTS (exact rational test, in `certify`, before the run) that a_min^N / 2 > 2^-1000 (N = 24: about 1e-47 for the order-9 file). Hence every positive intermediate is a NORMAL float, in particular no subnormal and no underflow can occur in the recursion, and every positive argument of log2_rig is >= 2^-1000. Upper bound: computed values are <= (1+eps_n) times the true beta <= 1, and the program asserts 1 + eps_N < 2, so all arguments are < 2. (The old leaf-only runtime check is kept in the program only as a printed diagnostic; the proof does not use it.) Inside log2_rig: for x != 1 with x in [1/2, 2) the nonzero value |m'-1| is >= 2^-53, so z, w and the products are far above 2^-1022; for x < 1/2, |log2 x| >= 1; hence t = x * log2_rig(x) is nonzero-or-exact-zero and normal (|t| >= min(2^-1000, 2^-55)). Fix 2: the stated input range of log2_rig is [2^-1000, 2) (plus the harmless x = 0); in the runs the observed arguments at N = 24 (order-9 file) lie in [3.1e-16, 4.6e-4]. Lemma L covers the near-1 regime too, because the reduction is exact and every step is relative (no cancellation: m' - 1 exact).

## 4. Lemma 1 (the beta array) -- unchanged from ERROR-LEMMA.md
For fixed y every row has at most two non-zero entries, beta_{y w}(h) = a1 beta_w(j1) + a2 beta_w(j2). The program stores a_i float = a_i (1+d), |d| <= u. Computed fl( fl(a1f b1) + fl(a2f b2) ) with all terms >= 0 gives relative error at most (1+eps)(1+u)^3 - 1; zero rows and zero terms are exact. Hence beta~_w(h) = beta_w(h)(1 + e), |e| <= eps_n = (1+u)^(3n) - 1, beta~ = 0 iff beta = 0. Length N-1: one float addition of the two length-N values (computed identically), relative error eps'_N = (1+eps_N)(1+u) - 1.

## 5. Lemma 2/3 (entropy sum and E) -- identical, with LAMBDA from Lemma L
Fix h, m in {N, N-1}, relative error eps of beta~, f(p) = -p log2 p.
(a) sum_w |f(beta~_w) - f(beta_w)| <= eps (m+2), S := sum_w |f(beta~_w)| <= m + eps (m+2). (Uses beta_w <= 1, sum beta_w = 1, sum beta_w |log2 beta_w| = H_m <= m, |log2(1+e)| <= eps/((1-eps) ln 2); for the true H the quantity ln 2 is the real constant, no float involved.)
(b) Term evaluation. The program forms t~_w = fl( beta~_w * log2_rig(beta~_w) ). By Lemma L (beta~ in the range of Section 3, or beta~ = 0), log2_rig(beta~) = log2(beta~)(1 + d), |d| <= LAMBDA; with the product rounding, t~_w = -f(beta~_w)(1 + delta_w), |delta_w| <= eta := (1+LAMBDA)(1+u) - 1 (and t~_w = 0 = f(0) when beta~_w = 0). So sum|t~| <= (1+eta) S and |sum t~ + sum f(beta~)| <= eta S.
(c) Summation: tree_sum_cols inside a leaf of 2^nb columns and tree_sum_rows over the 2^(N-nb) leaves, every addition one binary64 operation, each term passes through at most N additions: |fl(sum t~) - sum t~| <= gamma_N sum|t~|, gamma_N = (1+u)^N - 1 (all additions of Section 3 magnitudes, no subnormals; padding zeros exact).
(d) |H~_m(h) - H_m(h)| <= E_m := gamma_N (1+eta) S + eta S + eps (m+2), S = m + eps (m+2).
(e) L~_N := sum_h pi_h (H~_N(h) - H~_{N-1}(h)) - pxs evaluated in exact rationals (floats converted exactly), pi_h >= 0, sum pi_h = 1: |L~_N - L_N| <= E := E_N + E_{N-1}. All of eps, eta, gamma, E, LAMBDA are exact Fractions in the program (`err_bound`, `LAMBDA`).

## 6. Checks performed and evidence (not part of the proof)
- Asserts: exact constants (arb check of C2, ZMAX/WMAX in exact rationals), a-priori underflow bound (Section 3), 1 + eps_N < 2, no NaN in the beta arrays, all entropy sums finite, pi checks as before, rows have <= 2 terms.
- test_log2_rig.py / .log: 110010 points over [1e-300, 1], the observed range [1e-16, 0.1], near 1 from below and above, mantissa-edge points (just below/at/above 2^k C and 2^k), special points: every point's error compared with a 300-bit arb ball (upper bound used); worst relative error 4.4e-16 (2^-51.0) against LAMBDA = 3.9e-15 (2^-47.88).
- test_agree2.py / .log: agreement with the referee's arb-ball exact values (order-9 N = 11, 13; order-8 N = 12), every printed endpoint <= exact value, |L~ - exact| <= E.

## 7. What a hostile referee should still attack
1. A1: that numpy's elementwise +,-,*,/ on float64 are correctly rounded single operations on this build (standard; no SIMD path is known to violate it for these four operations), and that frexp is exact.
2. The proof chain from L_N to C (PROOF-LB1.md): Gallager Ch. 4.6/5.9 is still TEXTBOOK there; unchanged.
3. The exponent bookkeeping in 2c (31 = 3 + 7 + 19 + 1 + 1) is deliberately generous (one extra factor u/(1-u) vs u handled by a full extra u), so LAMBDA is about 3.9e-15; observed error is about 10x smaller.
