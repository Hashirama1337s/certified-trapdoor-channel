# PROOF-COLLAPSE: the collapsed delayed-feedback dual bound for the trapdoor channel

Status: DERIVED by the build seat, not yet refereed. It replaces Steps 4-5 of PROOF-UB1.md (augmented state with the
Q-graph node) by a smaller chain whose state is (S_j, x_{j+1..j+k}). Steps 1-3 of PROOF-UB1.md / build-ub/NOTES.md
are used unchanged and are restated here so the note can be read alone.

## 0. Objects

**Channel (A1).** State s in {0,1}, input x in {0,1}, output y in {0,1}.
- If x = s: y = x with probability 1, and the new state is s.
- If x != s: y = 0 or 1 with probability 1/2 each, and the new state is f(x,y,s) = x XOR y XOR s.

Write P(y|x,s) for the output law and W(y,s'|x,s) := P(y|x,s) 1[s' = f(x,y,s)] for the one-step kernel. In words:
when x != s, output y = s leaves the new state x, and output y = x leaves the state s.

**Capacity notion (A2).** No feedback. A codeword x^n is a function of the message only. The initial state s0 is fixed
(knowing it can only help a code). Given s0 and a fixed x^n, the channel produces (S_1, Y_1), ..., (S_n, Y_n)
sequentially: conditionally on everything before time t, (Y_t, S_t) ~ W(.,.|x_t, S_{t-1}). Hence

  (J)  P(y^n, s^n | x^n, s0) = prod_{t=1}^n W(y_t, s_t | x_t, s_{t-1}).

**Test law.** Fix k >= 1 and T(y|q) for q in {0,1}^k with 0 < T(0|q) < 1, T(1|q) = 1 - T(0|q). Fix a start word
qbar in {0,1}^k. Put q_0 = qbar and q_t = (last k symbols of q_{t-1} followed by y_t). Define
R(y^n) = prod_{t=1}^n T(y_t | q_{t-1}). Then R > 0 on {0,1}^n and sum_{y^n} R(y^n) = 1. For t >= k+1,
q_{t-1} = (y_{t-k}, ..., y_{t-1}), whatever qbar is.

**Per-step reward.** r(c, s, q) := D(P(.|c,s) || T(.|q)) in bits. Explicitly:
- c = s: P(.|c,s) is the point mass at c, so r = -log2 T(c|q).
- c != s: P(.|c,s) is uniform, so r = sum_y (1/2) log2( (1/2) / T(y|q) ) = -1 - (log2 T(0|q) + log2 T(1|q)) / 2.

Both are finite because T is strictly inside (0,1). Put r_max := max over (c,s,q) of r(c,s,q) < infinity; r >= 0.

## 1. Reduction to a per-sequence bound (PROOF-UB1 Steps 1-3, restated)

**Step 1 (Fano and data processing).** For an (n, 2^{nR}) code with error probability P_e and message W uniform,
nR <= I(W; Y^n | S0 = s0) + 1 + P_e nR <= I(X^n; Y^n | S0 = s0) + 1 + P_e nR. So if

  (*)  I(X^n; Y^n | S0 = s0) <= n rho + K   for every n, every input law, every s0, with K independent of n,

then every achievable rate is <= rho, i.e. C <= rho.

**Step 2 (dual bound).** For any law R > 0 on {0,1}^n and any input law P_X:
sum_{x^n} P_X(x^n) D(P_{Y^n|x^n,s0} || R) = I(X^n; Y^n | s0) + D(P_{Y^n|s0} || R) >= I(X^n; Y^n | s0).
Hence I(X^n; Y^n | s0) <= max over x^n of D(P_{Y^n|x^n,s0} || R).

**Step 3 (chain rule).** Fix x^n and s0. By (J), the state S_{t-1} is a deterministic function of (s0, x^{t-1}, y^{t-1})
(the update f is deterministic) and P(y_t | y^{t-1}, x^n, s0) = P(y_t | x_t, s_{t-1}). Therefore
log2 [P(y^n|x^n,s0) / R(y^n)] = sum_t log2 [P(y_t|x_t,s_{t-1}) / T(y_t|q_{t-1})] on every y^n with positive
probability, and taking expectations (terms with probability 0 contribute 0; R > 0 keeps all terms finite):

  D(P_{Y^n|x^n,s0} || R) = sum_{t=1}^n E[ r_t ],   r_t := r(x_t, S_{t-1}, Q_{t-1}).

The expectation is under the law (J) with this fixed x^n and s0. It remains to bound sum_t E[r_t] by n rho + K
uniformly in x^n and s0.

## 2. The coin form (exact realisation of (J))

Let B_1, B_2, ... be i.i.d. fair bits. Fix x^n, s0 and define recursively, with S_0 = s0,

  if B_t = 1:  Y_t = S_{t-1},  S_t = x_t;      if B_t = 0:  Y_t = x_t,  S_t = S_{t-1}.

**Lemma 0.** The process (S_t, Y_t) so defined has exactly the law (J).

Proof. S_{t-1} is a function of (s0, x^{t-1}, B_1..B_{t-1}), so B_t is independent of (S_0..S_{t-1}, Y_1..Y_{t-1}).
Conditionally on the past, with S_{t-1} = s:
- if x_t = s, both coin values give (Y_t, S_t) = (s, s) = (x_t, s): probability 1, matching W;
- if x_t != s, B_t = 1 gives (Y_t, S_t) = (s, x_t), and indeed f(x_t, s, s) = x_t; B_t = 0 gives (x_t, s), and
  f(x_t, x_t, s) = s. Each has probability 1/2, matching W(y, f(x_t,y,s) | x_t, s) = 1/2.
So P(Y_t = y, S_t = s' | past) = W(y, s' | x_t, S_{t-1}) for all y, s', and multiplying over t gives (J). QED.
(The verifier also checks Lemma 0 by exhaustive enumeration for n <= 6, self-test S2.)

Consequence used below. Because every expectation in Step 3 depends only on the law (J), we may compute it in the
coin realisation. In that realisation, for 0 <= j < t:

  (Phi)  (S_t, Y_{j+1}, ..., Y_t) = Phi_{t-j}(S_j; x_{j+1}, ..., x_t; B_{j+1}, ..., B_t)

for a deterministic map Phi_{t-j} (iterate the recursion), and (B_{j+1}, ..., B_t) is independent of S_j, because
S_j is a function of (s0, x^j, B_1..B_j) and the coins are independent. No feedback is essential here: x_{j+1..t}
are fixed numbers, not functions of the outputs.

## 3. Lemma C1 (the reward depends on the past only through S_{t-k-1})

For s in {0,1} and z = (z_1, ..., z_{k+1}) in {0,1}^{k+1} define

  g(s; z) := E_B[ r(z_{k+1}, Sigma_k, (Upsilon_1, ..., Upsilon_k)) ],

where (Sigma_k, Upsilon_1..Upsilon_k) = Phi_k(s; z_1..z_k; B_1..B_k) is the coin chain started in state s and fed
z_1..z_k, and E_B is the average over the 2^k coin vectors. Equivalently

  g(s; z) = sum_{q in {0,1}^k} sum_{s_k} pi(q, s_k | s; z_1..z_k) r(z_{k+1}, s_k, q),

with pi(q, s_k | s; z_1..z_k) = P(Y^k = q, S_k = s_k | S_0 = s, x^k = z_1..z_k), a finite sum with dyadic weights.

**Lemma C1.** For every fixed x^n, s0 and every t with k+1 <= t <= n:

  E[r_t] = sum_{s} P(S_{t-k-1} = s) g(s; x_{t-k}, ..., x_t) = E[ g(S_{t-k-1}; x_{t-k..t}) ].

Proof. Put j = t-k-1 >= 0. For t >= k+1, Q_{t-1} = (Y_{t-k}, ..., Y_{t-1}) = (Y_{j+1}, ..., Y_{j+k}) (Section 0).
So r_t = r(x_t, S_{t-1}, Y_{j+1..j+k}) = F(S_{t-1}, Y_{j+1}, ..., Y_{t-1}) with F(s', y^k) := r(x_t, s', y^k), a function
whose only dependence on the sequence is through the fixed number x_t. By (Phi) with t-1 in place of t,
(S_{t-1}, Y_{j+1..t-1}) = Phi_k(S_j; x_{j+1..t-1}; B_{j+1..t-1}), where B_{j+1..t-1} is independent of S_j and uniform
on {0,1}^k. By independence (Fubini on a finite space, no conditioning on events of probability zero needed):
E[r_t] = sum_s P(S_j = s) E_B[ F(Phi_k(s; x_{j+1..t-1}; B)) ] = sum_s P(S_j = s) g(s; x_{j+1}, ..., x_t),
since z = (x_{j+1}, ..., x_{t-1}, x_t) = x_{t-k..t} has z_{k+1} = x_t. QED.

**Lemma K (state kernel).** For 0 <= j < n, P(S_j = s, S_{j+1} = s') = P(S_j = s) K(s' | x_{j+1}, s), with
K(s|x,s) = 1 if x = s; K(x|x,s) = K(s|x,s) = 1/2 if x != s.
Proof. S_{j+1} is S_j (if B_{j+1} = 0) or x_{j+1} (if B_{j+1} = 1), and B_{j+1} is independent of S_j. QED.

## 4. Lemma C2 (telescoping on the collapsed chain)

**Collapsed chain.** States w = (s, z_1, ..., z_k) in {0,1}^{k+1} (2^{k+1} states), actions a in {0,1}.
Reward G(w, a) := g(s; z_1, ..., z_k, a). Transition: (P_a h)(w) := sum_{s'} K(s' | z_1, s) h(s', z_2, ..., z_k, a)
for any function h on states. For a real function h on the 2^{k+1} states define

  rho_cert(T, h) := max over all w and a of [ G(w,a) + (P_a h)(w) - h(w) ].

**Lemma C2.** For every n, x^n, s0:  D(P_{Y^n|x^n,s0} || R) <= n rho_cert + K0, with
K0 := k |r_max - rho_cert| + (max h - min h), independent of n, x^n and s0.

Proof. Case n <= k: by Step 3, D = sum_{t<=n} E r_t <= n r_max <= n rho_cert + n (r_max - rho_cert)
<= n rho_cert + k |r_max - rho_cert| <= n rho_cert + K0.

Case n >= k+1. For j = 0, ..., n-k define the random state W_j := (S_j, x_{j+1}, ..., x_{j+k}) (all indices <= n) and,
for j <= n-k-1, the action a_j := x_{j+k+1}. Note that W_0 = (s0, x_1..x_k) is deterministic and a_j is a fixed
number. For each j in {0, ..., n-k-1}:
- by Lemma C1 with t = j+k+1:  E[r_{j+k+1}] = E[ G(W_j, a_j) ];
- by Lemma K:  E[h(W_{j+1})] = sum_{s,s'} P(S_j = s) K(s' | x_{j+1}, s) h(s', x_{j+2..j+k+1}) = E[ (P_{a_j} h)(W_j) ];
- by the definition of rho_cert, pointwise for every value of W_j:  G(W_j, a_j) + (P_{a_j} h)(W_j) - h(W_j) <= rho_cert.
Taking expectations of the last line and inserting the first two:
  E[r_{j+k+1}] <= rho_cert + E[h(W_j)] - E[h(W_{j+1})].
Summing over j = 0, ..., n-k-1 the h terms telescope:
  sum_{t=k+1}^{n} E[r_t] <= (n-k) rho_cert + h(W_0) - E[h(W_{n-k})] <= (n-k) rho_cert + (max h - min h).
The first k rewards satisfy E[r_t] <= r_max (t = 1..k; here Q_{t-1} contains symbols of qbar, which is allowed:
r_max is a maximum over all q). Hence, by Step 3,
  D = sum_{t=1}^n E r_t <= k r_max + (n-k) rho_cert + (max h - min h) = n rho_cert + k (r_max - rho_cert) + span h
  <= n rho_cert + K0. QED.

Remarks for the referee.
1. Unlike Step 5 of PROOF-UB1, the telescoping is done on unconditional expectations. No conditioning on Y^j is
   needed: W_j does not have to be a function of the outputs, because Lemma C1 already removed the outputs from the
   reward and Lemma K gives the exact one-step law of the only random coordinate S_j. Both lemmas use that x^n is
   fixed (no feedback); that is all Step 2 requires.
2. rho_cert is a maximum over ALL 2^{k+2} state-action pairs, including state words that a given x^n never shows,
   so the inequality holds pointwise whatever value W_j takes.
3. Any T in (0,1) and any real h give a valid bound. A solver error, a bad rounding or an index mix-up in the
   certificate can only weaken the number, never invalidate it, provided the verifier computes G, P_a and the max
   correctly for the T and h in the file.

## 5. Theorem

For every k >= 1, every order-k test law T with entries in (0,1) and every real h on {0,1}^{k+1}:

  C <= rho_cert(T, h).

Proof. Steps 1-3 and Lemma C2 give (*) with rho = rho_cert and K = K0: for every input law,
I(X^n; Y^n | s0) <= max_{x^n} D(P_{Y^n|x^n,s0} || R) <= n rho_cert + K0. Step 1 concludes. QED.

## 6. What the verifier computes, and why its number is >= rho_cert

**Local-operator recursion for g (Lemma L).** For m = k, k-1, ..., 0 define V_m on (s, y_1..y_m, z_{m+1}..z_{k+1}) by
V_k(s, y_1..y_k, z_{k+1}) := r(z_{k+1}, s, (y_1..y_k)) and

  V_m(s, y^m, b, z_{m+2..k+1}) := (1/2) [ V_{m+1}(s, y^m, b, z_{m+2..k+1}) + V_{m+1}(b, y^m, s, z_{m+2..k+1}) ],

where b = z_{m+1}, and in V_{m+1} the slot that held b now holds y_{m+1}. Then V_0(s, z) = g(s; z).

Proof. One coin step from state s with input b: B = 0 gives (state, output) = (s, b), B = 1 gives (b, s), each with
probability 1/2 (Section 2). If b = s both terms coincide, which is the agree case of the channel. So
V_m(s, y^m, z_{m+1..k+1}) = E[ r(z_{k+1}, Sigma_k, y^m Upsilon_{m+1..k}) | Sigma_m = s ] over the coins
B_{m+1..k}, by induction from m = k down; at m = 0 this is the definition of g. QED.
In array form: on the pair (state bit, slot bit) the operator leaves the entries (0,0) and (1,1) alone and replaces
the entries (0,1) and (1,0) both by their average. g costs k passes over a 2^{k+2} array.

**Upper rounding.** For each (q,y) the verifier encloses -log2 T(y|q) in an arb ball at 192 bits, takes the upper
endpoint as an exact rational, and rounds it up to an integer multiple of 2^-64: L(q,y) >= -log2 T(y|q). It sets
r_up(c,s,q) := L(q,c) if c = s, and -1 + (L(q,0) + L(q,1))/2 if c != s, so r_up >= r. All weights pi are >= 0, so
g_up := (recursion applied to r_up) >= g, computed exactly in integers (the halving of each level is replaced by a
factor 2 on the other branch and one global power of two). With h = h_num / h_den exact, every residual
G_up(w,a) + (P_a h)(w) - h(w) is an exact rational, and rho_up := their maximum >= rho_cert(T, h) >= C.
The printed decimal is rounded up.

**Self-tests on every run.** (S1) the channel kernel against the Kobayashi-Morita matrix recursion (arXiv 1401.4575
eqs. (1)-(2)), all n <= 6, exact; (S2) Lemma 0 by enumeration, n <= 6; (S3) Lemma L: recursion against path
enumeration with the channel kernel, exact Fractions, random rational terminal tables, k = 1..6, every (s, z);
(S4) for certificates with k <= 8, the integer g_up of the certificate against exact path enumeration.

**Trusted base.** (i) the channel definition (A1) and its coding in `verify_collapsed.py::chan`;
(ii) python-flint/arb `log` returning a correct enclosure; (iii) Python integers and `fractions`;
(iv) the integer recursion `g_up_scaled` and the residual loop in `verify` (about 40 lines); (v) the argument above.

## 7. Not claimed here

- Nothing about convergence of rho_cert to C as k grows (that is DESIGN-SQUEEZE Section 2.1, separate, unrefereed).
- The observed equality of the collapsed value with the old (d = k+1, k) value for the same T is a numerical
  observation used only as a self-test (b), not a step of the proof.
