> Saved by the lead from the hand-back (seat a7c14c26, 2026-11-22). The text below is the seat's report verbatim.

# REFEREE-LB4: the log2_rig kernel (build-lb3/cert_backward2.py, ERROR-LEMMA2.md)

Files written by the referee, all in referee/lb4/: ref_log2_test.py and .out, ref_E_check.py and .out, cb2_s8_N11.out, cb2_s8_N11_nb5.out, ref_s8_N11.out. No existing files modified.

## In plain words
The new log routine is correct. Its error bound LAMBDA = 3.8671e-15 holds, it really is the only log on the certified path, and it is plugged into E exactly as the old lemma says. One sentence of the proof is false as written: the sensitivity step "P(w0 f) <= max(f,1) P(w0)". Its conclusion still holds here, with about a factor of 10 to spare, because w0 is tiny. That is a wording fix, not a numbers fix. On 306,142 adversarial points the worst error was 0.116 LAMBDA, and a deliberately degraded routine was caught by a factor of 2e7. Direct tests of A1 on this numpy build found no mismatches. My exact evaluation agrees with the kernel at order 8, N = 11.

## 1. Error proof of log2_rig: CORRECT WITH FIXES
- Mantissa reduction: exact. `m += m*lo` gives m or 2m, `ef -= lo` works on small integers, and d = m' - 1 is exact by Sterbenz on [1/2, 2]. frexp exact on 40,000 points (ref_log2_test.out).
- z range recomputed exactly: |z(C)| = |z(2C)| = 0.1715728753 <= 0.1716. CTHR slightly above sqrt(1/2), as the lemma allows.
- Truncation: TAU = 0.0295^10/(21*0.9705) = 2.449093e-17, recomputed; relative because P_inf >= 1.
- Horner: bookkeeping right. Each level costs (1+u)^2, the top coefficient costs u, total (1+u)^(2K-1) = 19. z exponent 3, w exponent 7, z*q product 1, C2 product 1: 31 = 3 + 7 + 19 + 1 + 1 checks out. Lower-side argument valid: 1 - prod(1 - b_i) <= sum b_i <= prod(1 + b_i) - 1. GAMMA_LOG = 3.577205e-15 and LAMBDA = 3.867087e-15 recomputed, bit-equal as Fractions to the kernel's values.
- 2/ln2 constant: enclosed by an arb check run at import (`<` on arb is certain-true only), so rc <= u; scaling by 2 exact.
- Final addition: with e' = 0 exact (0 + g). With e' != 0 no cancellation: x in [1/2, C) gives log2 in [-1, -0.5], x in [2C, 2) gives [0.5, 1); kappa <= 0.5000001/0.4999999, well inside 21/20. At x = 0.5 the result is exactly -1.
- x = 1 returns exactly 0. x = 0 returns -7.155274348620292 (finite); 0 * that is -0.0, harmless.
- FIX (wording, §2c, "w inside P" bullet): "P(w0 f) <= max(f,1) P(w0) (monomials scale by f^k)" is false in general (P = 1 + w^2, w0 = 1, f = 2 gives 5 > 4). Replace with: |P(w0 f) - P(w0)| <= sum_{k>=1} c_k w0^k ((1+a)^k - 1) <= ((1+a)^(K-1) - 1)(P(w0) - 1), and (P(w0) - 1)/P(w0) <= (WMAX/3)/(1 - WMAX) = 0.010132. Relative cost <= 0.0912 a < a, with a = (1+u)^7 - 1, so exponent 7 stays valid.

## 2. Code implements the lemma; no other transcendental on the certified path: CORRECT
- log2_rig matches §2 steps 1-7 line for line, including in-place `q *= w; q += HC[k]` (two roundings per level as analysed).
- Only call site is xlogx_cols, for both length-N and length-(N-1) arrays; strided arrays give bitwise-identical results to contiguous ones.
- Every log in the file: `arb(2).log()` (rigorous constant); `math.log2(float(LAMBDA))` in a print only. np.log2, np.log, np.exp absent from cert_backward2.py; no log/exp in trapcommon.py (sha 0146463961..., identical to build-lb2).
- Sums use explicit halving trees, never np.sum or BLAS. `pos.min()` and `Bl.max()` diagnostics only.

## 3. LAMBDA in E, Fixes 1 and 2: CORRECT
- err_bound matches ERROR-LEMMA §5(b)-(e). Recomputed E(11) = 2.021121e-13 and E(24) = 7.226538e-13, bit-equal to the kernel (ref_E_check.out). Old A2 value 2^-48 gives E(24) = 7.078782e-13. N = 24 log: L~ 0.5749274077312006 minus E = 0.57492740773047797..., floors to the printed 0.57492740773047.
- Fix 1: done, stronger than asked; uses the actual smallest float coefficient (order 9: 1.113500e-02, amin^24/2 = 6.600e-48 > 2^-1000), asserted before the run. 1 + eps_N < 2 asserted; (1+eps_N)(1+u) < 2 implied, not asserted (trivial).
- Fix 2: done. Range [2^-1000, 2) plus x = 0; near-1 regime covered and tested.

## 4. A1 trusted base: CORRECT (reasonable)
- MSVC, x86_64, X86_V3 SIMD; no x87 for doubles on Win64. Each operation a separate ufunc call, so no contraction across calls; a fused op would only remove a rounding.
- Pairwise sum not used.
- Direct checks in-process after importing flint and numpy: 0 mismatches in 40,004 samples each for +, -, *, / against exact Fraction rounding (contiguous, strided, in-place, planted ties). Round-to-nearest-even confirmed; subnormals not flushed.
- Residue: A1 is an assumption about this build; testing cannot prove it.

## Independent tests
- log2_rig vs 256-bit arb, 306,142 points (powers of 2 +-40 ulp for k = -1000..1; near 1 +-20,000 ulp plus random; C*2^k and 2C*2^k +-30 ulp; [2^-1000, 2^-990]; log-uniform; observed range [1e-16, 5e-4]; near 1/2 and 2). Worst inside the lemma range: 4.496e-16 = 0.1163 LAMBDA at x = 1.017151755019231. ALL WITHIN. Outside the range ([2^-1022, 2^-1000)): 1.530e-19. Positive control (KT = 4): worst 8.465e-08 = 21,889,848 LAMBDA, EXCEEDS as required.
- Order 8, N = 11 (s8 sha ae4a1ddc...): kernel endpoint 0.57444859277548 with nb = 11 and nb = 5; L~ = 0.5744485927756841; E = 2.021e-13. Exact ball (ref_lb3, 320 bits): 0.574448592775683951795799122138 +/- 3.00e-31. L~ - exact in [1.482e-16, 2.482e-16]; endpoint <= exact, exact - endpoint = 2.0395e-13. PASS.
- NOT CHECKED: N = 24 not re-run by the referee; consistency checked arithmetically from the log only.

## Verdicts
1. Error proof of log2_rig: CORRECT WITH FIXES (§2c sentence; number unchanged).
2. Code = lemma, no stray transcendental: CORRECT.
3. LAMBDA in E, Fix 1, Fix 2: CORRECT.
4. A1 trusted base: CORRECT (reasonable; still an assumption).

## What blocks release
Nothing in this kernel's scope beyond the §2c fix. Scope items unchanged: PROOF-LB1.md's textbook step (Gallager Ch. 4.6/5.9, TEXTBOOK); A1. Quote as "proven assuming correctly rounded binary64 + - * /".

## Single next strike
Patch ERROR-LEMMA2.md §2c in a new file. Re-run s9 at N = 24 with --nb 16 and --nb 14 to confirm nb-independence at the release depth.
