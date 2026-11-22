# build-ub4: deeper-than-window test laws for the collapsed ceiling (trapdoor channel, feedforward capacity C)

Ceiling design+build seat, 2026-11-22. Writes only in build-ub4/. Nothing outside this folder was modified.
Labels: **CERTIFIED** = output of the exact verifier `../build-ub3/verify_collapsed.py` (unmodified); **PROBE** = float
value from a convex solver in this folder (not a bound); **ESTIMATE** = extrapolation, not a bound; **DERIVED** = this
seat's argument, not refereed. Method credit: the duality bound with a test law on an output graph (Q-graph) is from
arXiv 1911.02113 and 2303.18008; the collapse is build-ub3/PROOF-COLLAPSE.md.

## In plain words

The ceiling program asks a referee to predict the next ball colour from what has come out so far. Until now the
referee only looked at the last k balls. We asked whether a referee who also remembers longer stretches of the past,
cheaply (how long the current run of one colour is, how long the previous run was), could give a lower ceiling for
the same amount of work. The answer is no. We worked out the exact bookkeeping that a longer-memory referee needs
(section 2), built a solver for it, and measured. Run lengths beyond the window change the ceiling by less than one
part in a hundred million; even when the previous-run length is added and the puzzle is 72 times bigger, the gain is
8.5e-6. Simply remembering one more plain ball always does better at the same puzzle size. The measurements also
show what drives the slow progress in k: about three quarters of each step comes from the referee's memory of
recent balls in full detail, and about one quarter from the extra step of delay the bookkeeping needs. The ceiling
did not move: it stays at C <= 0.574968594275 (build-ub3, k = 15). Along the way we found an exact factor-2
symmetry that makes the exact solver about 3 times faster (k = 12 in 268 s instead of 754 s), which makes an exact
k = 13 solve possible in about half an hour (not run, over the per-job budget; command below).

**Magic-trick line:** the referee that remembers whole run lengths, up to 14 balls back, scores exactly the same as
the one that only sees 6 balls, to 9 digits; one extra plain ball is worth 2e-4. The output stream's long memory is
not where the runs are.

## 1. Files

| file | role |
|---|---|
| `gen_probe.py` | PROBE solver for the generalised collapsed chain (any unifilar output automaton Q, window k), classes by k-step future equivalence, optional bisimulation; automaton families: (window m, current-run cap L1, previous-run cap L2) and (last R run lengths, capped) |
| `tree_probe.py` | PROBE: variable-depth context tree (selected depth-k contexts split to depth k+1), tied T, bisimulation |
| `ip_sym.py` | PROBE solver, plain order k, exact convex program with complement-symmetry reduction |
| `ip_fact.py` | PROBE solver, plain order k, factored (operator-level) convex program; slower, set aside |
| `opt_collapsed_ub4.py` | copy of `../build-ub3/opt_collapsed.py`, only the output path (and solver tag) changed; used with `--betas none` to snap T and compute h by hard value iteration |
| `T_ip_k*.npy`, `T_fact_k*.npy` | float test laws from the PROBE solvers |
| `certs/cert_col_k12_ipsym.json` | collapsed certificate (build-ub3 format) from the symmetric exact solve at k = 12 (sanity check, not an improvement) |
| `logs/` | all probe and verifier output (in `probe_runlength.log` the run-length-context family prints R as m and the cap as L1) |

All Python runs were under `py -3.11 memcap.py 8 py -3.11 ...`.

## 2. Derivation: the generalised collapse (DERIVED, not refereed)

Notation and Steps 1-3 (Fano, dual bound, chain rule) as in build-ub3/PROOF-COLLAPSE.md sections 0-1. The coin form
(Lemma 0) is used unchanged.

**Test law on an output automaton.** Let Q be a finite set, phi: Q x {0,1} -> Q, q0 in Q. Put Q_0 = q0 and
Q_t = phi(Q_{t-1}, y_t). For T(y|q) strictly inside (0,1), R(y^n) := prod_t T(y_t | Q_{t-1}) is a probability law on
{0,1}^n with R > 0, and Step 3 goes through word for word with q_{t-1} replaced by Q_{t-1} (a function of y^{t-1}):
D(P_{Y^n|x^n,s0} || R) = sum_t E[r_t], r_t := r(x_t, S_{t-1}, Q_{t-1}). The plain order-K law is Q = {0,1}^K with
phi(q,y) = (last K-1 symbols of q, y).

**k-step future equivalence.** For k >= 0 write phi^k(q, u) for the automaton state after reading u in {0,1}^k from q.
Put q ~ q' iff phi^k(q, u) = phi^k(q', u) for every u in {0,1}^k, and write [q] for the class.

Lemma E. q ~ q' implies phi(q, y) ~ phi(q', y) for every y.
Proof. For u in {0,1}^k, phi^k(phi(q,y), u) = phi(phi^k(q, y u_1..u_{k-1}), u_k), and y u_1..u_{k-1} has length k,
so the inner states agree for q and q'. QED.

**Lemma G1 (reward through a finite controlled state).** Fix x^n, s0, and t with k+1 <= t <= n; put j = t-k-1. Define,
for s in {0,1}, a class c and z in {0,1}^{k+1},

  g(s, c; z) := E_B[ r(z_{k+1}, Sigma_k, phi^k(q_c, Upsilon_1..Upsilon_k)) ],  (Sigma_k, Upsilon) = Phi_k(s; z_1..z_k; B),

with q_c any representative of c (by definition of ~ the value does not depend on the choice). Then

  E[r_t] = sum_{s,c} P(S_j = s, [Q_j] = c) g(s, c; x_{j+1..t}).

Proof. Q_{t-1} = phi^k(Q_j, Y_{j+1..t-1}). By (Phi) of PROOF-COLLAPSE.md, (S_{t-1}, Y_{j+1..t-1}) =
Phi_k(S_j; x_{j+1..t-1}; B_{j+1..t-1}). Both S_j and Q_j are functions of (s0, x^j, B_1..B_j) (Q_j through Y^j), so the
later coins are independent of the pair (S_j, Q_j) (x^n fixed: no feedback). Fubini on a finite space gives
E[r_t] = sum_{s,q} P(S_j = s, Q_j = q) E_B[r(x_t, Sigma_k, phi^k(q, Upsilon))], and the inner term depends on q only
through [q]. QED.

Where it differs from Lemma C1: the averaging variable is the PAIR (S_j, [Q_j]) instead of S_j alone. For the plain
order-K law with K <= k, phi^k(q, u) = last K symbols of u for every q: one class, and G1 is exactly C1.

**Lemma K' (one-step law of the pair).** P(S_{j+1} = s', [Q_{j+1}] = c' | S_j = s, Q_j = q) =
- 1[s' = s, c' = [phi(q, s)]] if x_{j+1} = s;
- (1/2) 1[s' = s, c' = [phi(q, x_{j+1})]] + (1/2) 1[s' = x_{j+1}, c' = [phi(q, s)]] if x_{j+1} != s
(coin B_{j+1} = 0 gives y = x_{j+1}, state s; B_{j+1} = 1 gives y = s, state x_{j+1}). By Lemma E the right side
depends on q only through [q]. Proof: B_{j+1} is independent of (S_j, Q_j). QED.

**Lemma G2 (telescoping).** Chain state w = (s, c, z_1..z_k) with c ranging over the classes of the states of Q
reachable from q0 (any superset is allowed), action a, reward G(w, a) := g(s, c; z, a), transition P_a from Lemma K'
with the window shifted to (z_2..z_k, a). For any real h on the states,

  rho_cert := max over ALL (w, a) of [ G(w,a) + (P_a h)(w) - h(w) ],  and for all n, x^n, s0:
  D(P_{Y^n|x^n,s0} || R) <= n rho_cert + k |r_max - rho_cert| + span h.

Proof. Identical to Lemma C2 with W_j := (S_j, [Q_j], x_{j+1..j+k}): by G1, E r_{j+k+1} = E G(W_j, a_j); by K',
E h(W_{j+1}) = E (P_{a_j} h)(W_j); the residual bound holds pointwise for every value of W_j, hence in expectation;
sum and telescope; the first k rewards are bounded by r_max (a max over all contexts, start context allowed). QED.
Telescoping goes through with the max over all states and actions: nothing is conditioned on outputs, and the only
new ingredient is that the random part of the state is the pair (S_j, [Q_j]), whose exact one-step law is K'.
Hence C <= rho_cert(T, h) for every T in (0,1) and every h (Steps 1-3 and the Theorem of PROOF-COLLAPSE.md unchanged).

**What the generalisation costs (DERIVED).** The state count is 2^(k+1) * |classes|. In the minimax form, the
relaxed sender may now choose x_{j+k+1} knowing [Q_j], a summary of the OUTPUTS up to time j: a delayed output-feedback
leak, on top of the delayed state of the plain collapse. A function h that is linear in the joint law of
(S_j, [Q_j]) cannot remove the leak (its residual is linear in that law, so its max sits at a point mass). The leak
is the price of test-law memory deeper than the window, and section 3 measures it.

**Consistency checks (PROBE).** The generalised chain reproduces the plain values (k = 4, 6, 7, 8, 9, 10, all to the
solver's accuracy against build-ub3 / design-squeeze), and for test-law order K = k+1 at window k it reproduces the
OLD formulation (PROOF-UB1, 2^(d+K) states) at d = k+1 <= K: order 6 at window 5 gives 0.5755084640 against the
build-ub2 certificate cert_u2b_d6_k6_L.json 0.575508460805 (4096 states there, 128 here); order 8 at window 7 gives
0.5751407375 against cert_u2b_d8_k8.json 0.575140726013 (32,768 states there, 512 here).

**Two exact reductions used only inside solvers (not needed for validity: any T, h is checked by the verifier).**
(R1) Complement symmetry: flipping every bit maps the channel to itself; rho*(T) is convex in T (a max of
non-negative combinations of -log T entries) and invariant under the flip, so a flip-symmetric T is optimal and the
convex program can be solved on orbits (half the variables and rows). (R2) Bisimulation: states with identical reward
rows and identical transition laws into blocks have equal optimal h; in the plain chain (0, 1, rest) and (1, 0, rest)
coincide (the first coin gives the same (y, s') pairs), so 2^(k+1) -> 3 * 2^(k-1).

## 3. Measurements (all PROBE, float, exact convex solves with CLARABEL)

"states" = chain states 2^(k+1) * classes (in brackets: after bisimulation where used).

### 3.1 Matched state counts: plain order k against extended test laws

| test law | window k | states | value (PROBE) | plain law with the same or fewer states |
|---|---|---|---|---|
| plain order 6 | 6 | 128 | 0.5754579411 | - |
| plain order 7 | 7 | 256 | 0.5752327296 | - |
| plain order 8 | 8 | 512 | 0.5751339171 | - |
| plain order 9 | 9 | 1024 | 0.5750745903 | - |
| plain order 10 | 10 | 2048 | 0.5750344107 | - |
| plain order 11 (ip_sym.py) | 11 | 4096 | 0.5750085161 | - |
| plain order 12 (ip_sym.py) | 12 | 8192 | 0.5749896037 | - |
| order 6 + current run to 7 | 6 | 256 | 0.5754579404 | order 7: 0.5752327296 |
| order 6 + current run to 8 | 6 | 512 | 0.5754579385 | order 8: 0.5751339171 |
| order 6 + current run to 10 | 6 | 1024 | 0.5754579380 | order 9: 0.5750745901 |
| order 6 + current run to 14 | 6 | 2048 | 0.5754579408 (solver "inaccurate") | order 10: 0.5750344116 |
| order 6 + previous run to 3 | 6 | 2304 | 0.5754579378 | order 10: 0.5750344116 |
| order 6 + current run to 8 + previous run to 4 | 6 | 4096 | 0.5754579377 | order 11: 0.5750085161 |
| order 6 + previous run to 6 | 6 | 9216 | 0.5754494733 | order 12: 0.5749896037 |
| order 4 + current run to 8 + previous to 4 | 6 | 4096 | 0.5758684141 (inaccurate) | order 11 |
| order 8 + current run to 10 | 8 | 2048 | 0.5751339145 | order 10: 0.5750344116 |
| order 8 + current run to 8 + previous to 3 | 8 | 9216 | 0.5751339139 | order 12: 0.5749896037 |
| order 4 + current run to 6 | 4 | 128 | 0.5761557080 | order 6: 0.5754579411 |
| order 4 + previous run to 4 | 4 | 1024 | 0.5761557071 | order 9 |
| order 4 + current to 8 + previous to 8 | 4 | 4096 | 0.5761514672 (inaccurate) | order 11 |
| last 3 run lengths, cap 3 (no window) | 4 | 1728 [354] | 0.5761217730 | order 8 (512 [384]): 0.5751339171 |
| last 4 run lengths, cap 4 | 4 | 16384 [3072] | 0.5757714916 | order 11 |
| last 4 run lengths, cap 4 | 5 | 32768 [4512] | 0.5754021160 | order 11-12 |
| context tree: order 6, 8 of 64 contexts split to depth 7 | 6 | 256 [158] | 0.5754451492 | order 7 (256 [192]): 0.5752327296 |
| same, 16 of 64 split | 6 | 256 [166] | 0.5753842572 | order 7 |
| same, 32 of 64 split | 6 | 256 [178] | 0.5753036376 | order 7 |
| same, all 64 split (= order 7 at window 6) | 6 | 256 [192] | 0.5752454275 | order 7 |

Verdict: **the extension does not win.** At every matched state count the plain order-k law is lower, by 1e-4 to 4e-4.
Run-length information beyond the window is worth at most 1e-8 (current run) and 8.5e-6 (previous run up to 6, at
72 times the state count). The context tree with selective deepening also loses to plain order k+1 at the same
(bisimulated) state count; bisimulation merges little once any context reaches past the window, because almost
every chain state can produce a window that uses the deeper context.

Reading (PROBE-based, not a theorem): the dual maximiser's output process has (near) geometric run tails, so how
long a run has lasted beyond the window carries no information about the next output; the useful memory is the
exact pattern of the most recent symbols, i.e. several short runs, which a plain window holds best.

### 3.2 Fixed window, deeper plain memory: is the rate driven by delay or by test-law memory?

V(K, k) := value of the plain order-K law at window k (delay k+1); U_K = V(K, K). Same state count as U_K.

| K | k (window) | V(K,k) | U_k | U_K | memory share of the step U_k -> U_K |
|---|---|---|---|---|---|
| 6 | 3 | 0.5759117542 | 0.5786386 | 0.5754579 | 86 % of 3.18e-3 |
| 6 | 4 | 0.5758304962 | 0.5761557 | 0.5754579 | 47 % of 6.98e-4 |
| 6 | 5 | 0.5755084640 | 0.5756895 | 0.5754579 | 78 % of 2.32e-4 |
| 7 | 6 | 0.5752454255 | 0.5754579 | 0.5752327 | 94 % of 2.25e-4 |
| 8 | 6 | 0.5751649531 | 0.5754579 | 0.5751339 | 90 % of 3.24e-4 |
| 8 | 7 | 0.5751407375 | 0.5752327 | 0.5751339 | 93 % of 9.88e-5 |
| 9 | 7 | 0.5751076108 | 0.5752327 | 0.5750746 | 79 % of 1.58e-4 |
| 9 | 8 | 0.5750900881 | 0.5751339 | 0.5750746 | 74 % of 5.93e-5 |
| 10 | 8 | 0.5750629812 | 0.5751339 | 0.5750344 | 71 % of 9.95e-5 |
| 10 | 9 | 0.5750435004 | 0.5750746 | 0.5750344 | 77 % of 4.02e-5 |

(U_3 = 0.5786386, U_4 = 0.5761557, U_5 = 0.5756895 from design-squeeze p3/p7; re-measured here as orders 3, 4, 5 at window 6, i.e. with extra delay: 0.5786385506, 0.5761557079, 0.5756895472, equal to the delay-(K+1) values to 9 digits, which re-confirms DESIGN-SQUEEZE p4.) With DESIGN-SQUEEZE p4 (extra delay
beyond k+1 buys almost nothing): the 0.7-per-step rate is driven mainly by test-law memory (about three quarters of
each step at k = 8-9), and the remaining quarter is the delay the memory needs; delay without memory is worthless and
memory without delay loses a quarter. In this framework memory deeper than the window always costs states at least
as fast as the plain law does, so the plain order-k law at window k is the efficient point.

### 3.3 Next structural idea actually measured: exact symmetric convex solver

Timings are wall times on a shared machine (another seat ran floor jobs at the same time), so they wobble by up to
2x between runs; same-session pairs are given where available.

| k | unreduced interior point (p7_sparse.py / gen_probe.py) | `ip_sym.py` (symmetry R1) | value (PROBE) |
|---|---|---|---|
| 10 | 20 s (build-ub3 log); 30.7 s (gen_probe, this session) | 7.6 s and 3.1 s (two runs) | 0.5750344116 |
| 11 | 109 s | 45.8 s | 0.5750085161 |
| 12 | 754 s, 5.3 GB | 267.8 s, 3.31 GB peak | 0.5749896037 |
| 13 | not run (expected over 20 min / 8 GB) | not run: ESTIMATE about 1550 s (x5.8 per k), 5-6 GB | - |

Sanity certificate (CERTIFIED, not an improvement): the k = 12 symmetric law, snapped and given h by hard value
iteration (`opt_collapsed_ub4.py 12 --init T_ip_k12.npy --betas none --tag _ipsym`), verified by the unmodified
build-ub3 verifier: rho_up = 0.574989603359 (15 dp 0.574989603358971), 1.6e-9 above build-ub3's k = 12 certificate
(interior-point accuracy). The factored operator formulation (`ip_fact.py`) is no faster than the unreduced one (k = 10: 71.7 s and 30.9 s in two runs; probably because its butterfly-shaped equality graph fills in under sparse factorisation (not checked)), set aside.

### 3.4 Where the smoothed solver loses (diagnosis from build-ub3 logs, ESTIMATE)

- Its smoothed objective f = gmax + log2(sum_w 2^(beta (g_w - gmax)))/beta carries a bias up to log2(2^(k+1))/beta:
  1.6e-6 at k = 15, beta = 1e7 (seen in opt_k15.log: soft 0.574970213 vs hard 0.574968594). That is the size of the
  per-k steps it is trying to resolve. The k = 15 run had no beta = 1e8 stage.
- Optimal U_9..U_12 steps: 5.93e-5, 4.02e-5, 2.59e-5, 1.89e-5 (ratios 0.68, 0.64, 0.73). Extrapolating at 0.70:
  U_13 ~ 0.574976, U_14 ~ 0.574967, U_15 ~ 0.574961 (ESTIMATE). The certified k = 13, 14, 15 values sit about
  3.6e-6, 3.5e-6 and 8e-6 above these. A ratio above about 0.765 would put the limit of U_k below the certified floor
  0.57492740773047, so the limit of the ceiling family is ESTIMATED in [0.574927, 0.57496].
- Consequence: a perfect optimiser at k = 15-16 could lower the ceiling by roughly 1e-5 (ESTIMATE); the ceiling family
  itself has at most about 2-4e-5 left above the floor. The ceiling alone cannot shrink the 4.1e-5 gap by 30-100x;
  the floor has to move too.

## 4. Ceiling status

Unchanged: **C <= 0.574968594275** (CERTIFIED, build-ub3/certs/cert_col_k15_sm.json, sha256
462f043a97fd3a807e237a8558a438299f371a3c612e231e88f10d10688a8446). No new certificate from this seat is lower.

## 5. Commands for the lead (not run here: over the per-job budget)

- Exact k = 13 (ESTIMATE about 26 min, 5-6 GB peak; the 8 GB cap may be tight):
  `py -3.11 memcap.py 8 py -3.11 build-ub4/ip_sym.py 13`
  then `... opt_collapsed_ub4.py 13 --init build-ub4/T_ip_k13.npy --betas none --tag _ipsym` and
  `... build-ub3/verify_collapsed.py build-ub4/certs/cert_col_k13_ipsym.json`.
  This gives the true U_13 (how much the smoothed solver left at k = 13) and an exact warm start for k = 14-16.
- k = 15 continued from its own certificate with the missing beta = 1e8 stage (ESTIMATE 15-30 min, from opt_k15.log):
  `... opt_collapsed_ub4.py 15 --init build-ub3/certs/cert_col_k15_sm.json --precond 1e-6 --betas 1e7,1e8 --maxiter 150 --tag _cont`

## 6. Hashes

See "Hash table (sha256)" at the end of this file.

## Loose ends

- The generalised collapse (Lemmas E, G1, K', G2) is DERIVED here and not refereed. No bound depends on it: no
  certificate of the generalised form was produced, because the extension did not win, so no generalised verifier was
  written and no path-enumeration cross-check of the generalised g was run (the consistency checks in section 2 are
  float values of the convex program, not verifier runs).
- Several probe solves ended "optimal_inaccurate" (marked); their values carry errors of order 1e-9 to 1e-8, far
  below the 1e-4 differences that decide the verdict.
- Only two run-length families and one tree-selection rule (mass-weighted divergence from the order-(k+1) optimum)
  were tried. Other unifilar summaries (for example parity of the number of runs, or counts of boundaries) were not.
- The k = 13 exact solve and the continued k = 15 solve were not run (budget); timings are ESTIMATES from the
  k = 11 -> 12 ratio and from build-ub3's logs.
- The extrapolated U_13..U_15 and the ceiling-limit range are ESTIMATES from four steps with a wobbling ratio.
- Bisimulation and complement symmetry were not combined into one reduction (each alone: 3/4 and 1/2 of the states).
- PROOF-COLLAPSE.md still has the referee's open fixes (s0 wording, claimed_rho_upper in the k = 12-15 certificates,
  prior-art gate); this seat did not address them. The new k = 12 sanity certificate has no claimed_rho_upper either.

## Hash table (sha256)

| file | sha256 |
|---|---|
| `gen_probe.py` | 0722ff6fea3f3a787682e016b906f683fa8daedbc1969ec8c9ac4d29825c4ed1 |
| `tree_probe.py` | d5c6a1be94cba9d2807487c15fdb8ef3ddb9572adf5b68fa57be8baf2c7c310f |
| `ip_sym.py` | 7599b6ad9cabd299535e721b08285b1cc286a1ab5881cd29301baf2d3ebc65fb |
| `ip_fact.py` | b4832e4a61682176d369fe1211d8d8e158bf1d51b8cb8a20d2f0ca58894135f1 |
| `opt_collapsed_ub4.py` | 9431ff50c210c815aafd9b4ec315202d941a2c4b43619345a6c6a6b7f8328f88 |
| `certs/cert_col_k12_ipsym.json` | 7b0dc14c94903c39b9fbb2d17cfc06ef3c3cd49d8f30f65527d95f8f8c05389b |
| `T_ip_k10.npy` | fe036517cca55b0f0f7296e59b31d5fbc7ca813650a23b122aba54a9e49ca2ba |
| `T_ip_k11.npy` | 90694d73b18d694e897069d9e16d6e5cd4adcf634e30fa62097c421bf7e07fa9 |
| `T_ip_k12.npy` | ec5bf7c7436a56fa44bde58bfa3ea11a83fc3887b6af7beb7b678d52dc6cde67 |
| `T_ip_k6.npy` | d8538dd16804fc2fe85195a4e132e07d6cb313ebae0031a3278a0f9b5a868bd7 |
| `T_ip_k8.npy` | 799f68e097dcf47fabc56949247e100247b29dd3102e5394334fcf3870cdfb85 |
| `T_ip_k9.npy` | 3bb303dbdcc25fd34990946b52b2d83dcf3dd434f5a05d0dca4219e4df30bd6f |
| `T_fact_k10.npy` | f7eb92ad7c2b3d25b3d4ae07f29732c60addfe68aebdb2a86390b94f6286de13 |
| `T_fact_k6.npy` | b46b21b9c819cb8a2bfcbfbb111ddc7150161eab50a616ad0cca05672227e791 |
| `T_fact_k8.npy` | 3545a21244233124a2bafe3aa3912697b268c65798820314aef1b435c27db486 |
| `logs/ip_fact.log` | 8f1b9aa3dd52af019bbe7a6768ebac79ab90a2dae843a4b6ae7ed610a95372db |
| `logs/ip_sym_k11.log` | 0b81896cb10c7f09af7aea7231c823d76a36f5556932bd237f0fee9be62e4df2 |
| `logs/ip_sym_k12.log` | d5fbc4bd80ab32934d22a85006fd1c553562654bda1bb789f2b5499be84765f3 |
| `logs/ip_sym_k6_10.log` | e4dc2f7035e6db8adff2a51cb5b09875112a597da3feabafabf0aa84112c374f |
| `logs/opt_k12_ipsym.log` | 98edbb5e8451a63ab6801a54eaecf3c0a9942c8d075c498ee3940addaa9f8df8 |
| `logs/probe_memory_vs_delay.log` | 0ae06453014a681fe043da546f886f9bfd83cf5ef80ae1a3632b65027179ca36 |
| `logs/probe_plain.log` | 961569583fba97968a7f3f892462d636a68d53241004048db814221647106fe1 |
| `logs/probe_runlength.log` | fbcc3c36918df8ec7435b23af7de7812be8c26e46dfd9b93ce1028ca232ae5b6 |
| `logs/tree_probe_k6.log` | 708fa58f43f7078521c71125075f55ec15276e2d075056587c73d933cf8e2860 |
| `logs/verify_k12_ipsym.log` | ad56dc0e8099bf34222e677d795bb23ed2592cf70317013ab83ebdd2c6c1913d |

Certificates: only `certs/cert_col_k12_ipsym.json` (CERTIFIED rho_up 0.574989603359, sanity check). The ceiling of record stays build-ub3/certs/cert_col_k15_sm.json (0.574968594275, sha256 462f043a97fd3a807e237a8558a438299f371a3c612e231e88f10d10688a8446). `logs/probe_memory_vs_delay.log` also holds three extra-delay rows (k=6, m=3,4,5: order m at window 6), used in section 3.2's note.
