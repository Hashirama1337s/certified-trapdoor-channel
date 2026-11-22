> Saved by the lead from the hand-back (seat af0d1b6b, 2026-11-22). The text below is the seat's report verbatim.

# REFEREE-UB3: hostile referee report on the collapsed delayed-feedback dual (build-ub3)

Scripts and outputs: referee/ub3/ (ref_ub3_verify.py, ref_ub3_bf.py, run_small.out, run_big.out, their_verifier_rerun.out, bf.out).

## In plain words
The new, shorter argument holds up. I re-derived every step and found no gap in the mathematics. Two pieces were the ones at risk: the claim that the reward depends on the past only through the box state k+1 steps back, and the telescoping on unconditional expectations. Both are right, and both rely on the inputs being fixed in advance, which is all the capacity question needs. My own checker uses a different log library, a different rounding grid and a different bit order, and it reproduces all four certificates (k = 12 to 15) to 15 decimals, with the same argmax. A path-by-path brute force of the bound itself (k = 3, 4, n up to 12) holds with slack of about 1e-12 to 4e-9, and the negative controls fail as they should. The fixes are wording and bookkeeping.

## Verdicts

**1. Lemma 0 (coin form): CORRECT.**
- Cases checked by hand. x = s: both coin values give (y, s') = (s, s). x != s: B = 1 gives y = s and s' = x ^ s ^ s = x; B = 0 gives y = x and s' = s; each has probability 1/2.
- Holds for every fixed pair (x^n, s0). An encoder that knows s0 is also covered: step 2 takes the max over x^n separately for each s0, so x^n may depend on (message, s0).
- Output feedback is not covered, and none is needed.

**2. Lemma C1: CORRECT.**
- For t >= k+1, Q_{t-1} = Y_{j+1..j+k} with j = t-k-1. Iterating the coin map k times gives (S_{t-1}, Y_{j+1..t-1}) as a deterministic function of S_j, the inputs x_{j+1..t-1} and the coins B_{j+1..t-1}.
- S_j is a function of (s0, x^j, B_1..B_j). So the later coins are independent of S_j, given that x^n is fixed.
- Exact test (ref_ub3_verify.py --c1): an arbitrary random rational reward table, every x^n and both s0, for k = 3, n = 7 and k = 2, n = 6. Full channel enumeration of E[r_t] equals sum_s P(S_{t-k-1} = s) g(s; x_{t-k..t}): 1536 identities, all exact (run_small.out).
- Fix (cosmetic): Section 0 says "q_t = last k symbols of q_{t-1} followed by y_t". It should say "last k-1 symbols".

**3. Lemma C2 (telescoping): CORRECT.**
- Lemma K is right. E h(W_{j+1}) = E (P_{a_j} h)(W_j) holds unconditionally.
- The pointwise residual bound holds over all 2^(k+2) state-action pairs, so reachability does not matter.
- Boundary terms are right: h(W_0) - E h(W_{n-k}) <= span h.
- The first k steps are bounded by r_max, which is a max over all q, so start-word symbols are allowed.
- The n <= k case is right: n(r_max - rho) <= k|r_max - rho|.
- K0 does not depend on n, x^n or s0.
- No conditioning on Y^j is needed, so the Y^j-measurability fix from REFEREE-UB1 does not apply here.

**4. Fano / dual / data-processing chain: CORRECT WITH FIXES.**
- Steps 1-3 are the same as the refereed PROOF-UB1 chain. The unifilar update s' = x ^ y ^ s is deterministic.
- Fix A: Section 0 (A2) still says "s0 is fixed (knowing it can only help a code)". This is the wording REFEREE-UB1 asked to replace. Insert the line I(W;Y^n) <= I(W;Y^n,S0) = I(W;Y^n|S0), and state that (*) is uniform in s0.
- Fix B: do not carry over PROOF-UB1's sentence "rho_cert also bounds C_d^fb". The collapse proof uses no feedback in Lemmas C1 and K. Only the feedforward C is proved.

**5. The verifier: CORRECT.**
- (a) g as defined. Code read: terminal values (agree gives 2L[q][a]; disagree gives L0 + L1 - 2^(P+1)); the operator pairs (s, slot) with its partner (flip state, flip slot); one factor of 2 per level, scale 2^(P+1+k); next-state word (x_2..x_k, a); the K weights; the h(w) broadcast over a. My checker computes all of this independently, and its argmax matches the verifier's for all four certificates, which confirms the index convention.
- (b) Logs: arb enclosure at 192 bits, rounded up to the 2^-64 grid. Since r_up >= r and the weights are >= 0, g_up >= g.
- (c) The max runs over all 2^(k+2) entries.
- (d) Decimals printed with a ceiling.
- Fix C (bookkeeping): cert_col_k12/13/14/15 contain no "claimed_rho_upper". The verifier's "RESULT: PASS" therefore does not bind the headline number 0.574968594275. Add the field, or a sealed bar comparator, before release.

**6. Unknown s0: CORRECT** (with Fix A as the written justification).
- (*) holds for every s0 with the same K0. Random or unknown s0: I(W;Y^n) <= I(W;Y^n|S0). Adversarial s0: a code that works for all s0 works for s0 = 0. So rho_cert bounds C under every s0 convention.

## Independent verifier (referee/ub3/ref_ub3_verify.py)
How it differs from verify_collapsed.py: the channel is coded from the brief, not the coin form; logs use mpmath interval arithmetic at 300 bits, each enclosure checked against a 400-bit point value, upper ends rounded to 2^-200, not 2^-64; internal bit order has the oldest symbol as the least significant bit, with an explicit reversal to the certificate convention; residuals are exact Fractions; the recursion is self-tested against channel path enumeration (random rational rewards, k = 1..6) and against the certificate's own terminal for k <= 5.

| cert | 12 dp, rounded up | 15 dp, rounded up | argmax |
|---|---|---|---|
| k12_cvx | 0.574989601774 | 0.574989601773768 | (0, '100010000101', 1) |
| k13_sm | 0.574979956446 | 0.574979956445641 | (0, '0111001111110', 0) |
| k14_sm | 0.574970606024 | 0.574970606023238 | (0, '00000000001110', 1) |
| k15_sm | 0.574968594275 | 0.574968594274944 | (1, '111001101111111', 1) |
| k3_opt | 0.578638551236 | 0.578638551235890 | |
| k4_cvx | 0.576155708536 | 0.576155708535299 | |
| k7_from_d8k7 | 0.575232734723 | 0.575232734722443 | |

Re-run of verify_collapsed.py (their_verifier_rerun.out): same 15-dp values and argmaxes, self-tests pass; sha256 values match NOTES.md (k15: 462f043a...8446).

## Brute force of the bound (ref_ub3_bf.py, bf.out)
P(y^n | x^n, s0) from the channel definition (no chain rule, no coin form); all x^n, all y^n, both s0, all start words. Two forms per input: global D <= n rho + K0; tight D <= sum_{t<=k} E r_t + (n-k) rho + h(W0) - E h(W_{n-k}).
- k = 3 (rho 0.578638551236, K0 3.810780): n = 4, 6, 8, 10, 12: tight min slack 1.097e-13, 3.300e-13, 5.683e-10, 1.852e-09, 3.804e-09, all OK. Global min slack 2.530 at n = 12.
- k = 4 (rho 0.576155708536, K0 5.133810): n = 5, 8, 10, 12: tight min slack 7.003e-13, 2.803e-12, 4.204e-12, 5.607e-12, all OK. Global min slack 3.805 at n = 12.
- Negative controls at n = 12: rho - 1e-4 gives tight -9.000e-04 (k = 3) and -8.000e-04 (k = 4): VIOLATION. T0[0] + 0.05 with the original rho gives tight -3.239e-01 and -2.900e-01: VIOLATION. The global form cannot fail at n = 12 (slack 2.5-3.8); sanity check only. The tight form is the real test.
- Per-step growth of max_x D falls toward rho: for k = 3, 0.602, 0.585, 0.580 against rho 0.5786, consistent with a transient absorbed by the constant K0.

## Not checked
- Prior art for the collapse itself; the build seat did not gate it either. The duality / Q-graph / delayed-feedback method must be credited to 1911.02113 and 2303.18008. NOTES shows that for the same T the collapsed value equals the old (d = k+1, k) value (k <= 11): the collapse is a cheaper evaluation, not a stronger bound per test law. Say so in any write-up.
- The convergence claims in DESIGN-SQUEEZE 2.1 are not used by any bound.
- mpmath interval log and arb log are both trusted base; they agree to 15 dp.

## What blocks release
Nothing in the mathematics. Before release: Fix A (s0 wording); Fix B (drop any delayed-feedback claim); Fix C (claimed_rho_upper in the certificates, or a sealed comparator); the Section 0 "k-1" typo; a prior-art gate on the collapse, with Zenodo.

C <= 0.574968594275 is CORRECT as a certified bound, given the trusted base (log enclosures, Python integers and Fractions).

## Single next strike
Seal a release bar: ref_ub3_verify.py and verify_collapsed.py on cert_col_k15_sm.json (claimed_rho_upper added in a new file); the tight brute force (k = 3, 4, n = 12; slack >= -1e-9) with its rho - 1e-4 negative control; the prior-art gate result for the collapse.
