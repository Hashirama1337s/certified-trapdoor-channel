# EXACT VERIFIER for collapsed delayed-feedback dual certificates (trapdoor channel, feedforward capacity C).
#
# Certificate (json): k; order-k Markov test law T(0|q) = T0_num[q] / T_den, T(1|q) = 1 - T(0|q), required in (0,1),
# q = (y_{t-k}, ..., y_{t-1}) read as a binary number, oldest output = most significant bit; and h(w) = h_num[w] / h_den
# on the collapsed states w = (s, x_{j+1..j+k}), index w = s*2^k + (x_{j+1}..x_{j+k} as binary, oldest = MSB).
# Optional "claimed_rho_upper" (decimal string): the verifier exits 1 unless its own rho_up <= claim.
#
# It computes the exact rational
#   rho_up = max over (w = (s, x_1..x_k), action a) of [ g_up(s; x_1..x_k, a) + sum_{s'} P(s'|x_1, s) h(s', x_2..x_k a) - h(w) ]
# where g_up >= g (PROOF-COLLAPSE.md) is obtained by replacing every -log2 T(y|q) by an exact dyadic upper bound
# (arb enclosure at 192 bits, upper endpoint, then rounded UP to a multiple of 2^-P). Everything after the logs is exact
# integer arithmetic. rho_up >= rho_cert >= C (PROOF-COLLAPSE.md, Theorem). Printed rounded UP.
#
# g is evaluated by the local-operator recursion (k operators on a 2^(k+2) array). Self-tests run on every call:
#   (S1) channel kernel vs Kobayashi-Morita matrix recursion (arXiv 1401.4575 eqs. (1)-(2)), exact, n <= 6;
#   (S2) coin form reproduces P(y^n, s_n | x^n, s0) exactly, n <= 6;
#   (S3) local-operator g == brute-force path enumeration (channel kernel, exact Fractions) for random rational
#        terminal tables, k = 1..6 (all (s, x^(k+1))).
#   and for the certificate itself if k <= 8: (S4) local-operator g_up == path-enumeration g_up, all entries.
# Usage: verify_collapsed.py cert.json [cert2.json ...]   (exit 1 on any failure)
import sys, json, time, itertools, random, hashlib
from fractions import Fraction
from flint import arb, fmpq, ctx

ctx.prec = 192
P_LOG = 64  # log upper bounds are multiples of 2^-P_LOG


# ---------------------------------------------------------------- channel (trusted base)
def chan(x, s):
    """trapdoor kernel: returns list of (y, prob, s_next). x == s: y = x, state stays. x != s: y uniform,
    s_next = x XOR y XOR s (the ball that was not output)."""
    if x == s:
        return [(x, Fraction(1), s)]
    return [(y, Fraction(1, 2), x ^ y ^ s) for y in (0, 1)]


def selftest_channel(nmax=6):
    """(S1) chan() vs Kobayashi-Morita recursion; (S2) coin form vs chan(), exact, all n <= nmax."""
    P = {0: [[Fraction(1)]], 1: [[Fraction(1)]]}
    for n in range(1, nmax + 1):
        P0, P1 = P[0], P[1]
        m = len(P0)
        Z = [[Fraction(0)] * m for _ in range(m)]
        def blk(A, B, C, D):
            return [A[i] + B[i] for i in range(m)] + [C[i] + D[i] for i in range(m)]
        half = lambda M: [[v / 2 for v in row] for row in M]
        P = {0: blk(P0, Z, half(P1), half(P0)), 1: blk(half(P1), half(P0), Z, P1)}
        for s0 in (0, 1):
            for xs in itertools.product((0, 1), repeat=n):
                lay = [((), Fraction(1), s0)]
                for x in xs:
                    lay = [(ys + (y,), p * q, sn) for (ys, p, s) in lay for (y, q, sn) in chan(x, s)]
                tot = {}; joint = {}
                for ys, p, sn in lay:
                    tot[ys] = tot.get(ys, 0) + p
                    joint[(ys, sn)] = joint.get((ys, sn), 0) + p
                xi = int("".join(map(str, xs)), 2)
                for yi in range(2 ** n):
                    ys = tuple(int(b) for b in format(yi, f"0{n}b"))
                    if tot.get(ys, 0) != P[s0][xi][yi]:
                        raise SystemExit(f"FAIL (S1) n={n} s0={s0} x={xs} y={ys}")
                # coin form: B=1 -> y = s_prev, s = x ; B=0 -> y = x, s = s_prev ; B fair, iid
                cj = {}
                for B in itertools.product((0, 1), repeat=n):
                    s = s0; ys = ()
                    for x, b in zip(xs, B):
                        if b == 1:
                            ys += (s,); s = x
                        else:
                            ys += (x,)
                    cj[(ys, s)] = cj.get((ys, s), 0) + Fraction(1, 2 ** n)
                if cj != joint:
                    raise SystemExit(f"FAIL (S2) coin form n={n} s0={s0} x={xs}")
    return True


# ---------------------------------------------------------------- g: two independent evaluations
def g_operator(k, term):
    """term: list over level-k index j = (s << (k+1)) | (q << 1) | a of an exact value r(a, s_k = s, q) (int or Fraction).
    Returns list over level-0 index i = (s << (k+1)) | (x_1..x_k a) of g(s; x_1..x_k, a) = E[r(a, S_k, Y^k)].
    Local operator Op_b on the pair (state bit, field bit b): entries with s == bit unchanged, the two entries with
    s != bit both replaced by their average (channel step: agree -> (s, y = x); disagree -> (s', y) = (x, s) or (s, x)
    w.p. 1/2). V_m = Op_{k-m} V_{m+1}, g = V_0."""
    V = list(term)
    F = k + 1
    for m in range(k - 1, -1, -1):
        b = k - m
        sb = 1 << F; bb = 1 << b
        W = V[:]
        for i in range(len(V)):
            s = 1 if i & sb else 0
            x = 1 if i & bb else 0
            if s != x:
                j = i ^ sb ^ bb  # partner: state and field bit both flipped
                W[i] = (V[i] + V[j]) / 2 if not isinstance(V[i], int) else Fraction(V[i] + V[j], 2)
        V = W
    return V


def g_brute(k, term):
    """path enumeration with the channel kernel chan(), exact."""
    out = [None] * (2 ** (k + 2))
    for s in (0, 1):
        for xs in itertools.product((0, 1), repeat=k + 1):
            lay = [((), Fraction(1), s)]
            for x in xs[:k]:
                lay = [(ys + (y,), p * q, sn) for (ys, p, st) in lay for (y, q, sn) in chan(x, st)]
            a = xs[k]
            val = Fraction(0)
            for ys, p, sk in lay:
                q = 0
                for y in ys:
                    q = (q << 1) | y
                val += p * term[(sk << (k + 1)) | (q << 1) | a]
            i = (s << (k + 1)) | int("".join(map(str, xs)), 2)
            out[i] = val
    return out


def selftest_g(kmax=6, seed=12345):
    rnd = random.Random(seed)
    for k in range(1, kmax + 1):
        term = [Fraction(rnd.randint(-10 ** 6, 10 ** 6), rnd.randint(1, 10 ** 6)) for _ in range(2 ** (k + 2))]
        if g_operator(k, term) != g_brute(k, term):
            raise SystemExit(f"FAIL (S3) local-operator g != brute force at k={k}")
    return True


# ---------------------------------------------------------------- arithmetic helpers
def exact_upper(a):
    u = a.upper()
    m, e = u.man_exp()
    m, e = int(m), int(e)
    return Fraction(m * 2 ** e) if e >= 0 else Fraction(m, 2 ** (-e))


def ceil_div(a, b):
    return -((-a) // b)


def log_upper_ints(T0num, Tden):
    """for each q and y: integer L[q][y] with L/2^P_LOG >= -log2 T(y|q) (T(0|q) = T0num[q]/Tden)."""
    ln2 = arb(2).log()
    L = []
    for n in T0num:
        row = []
        for num in (n, Tden - n):
            v = -(arb(fmpq(num, Tden)).log() / ln2)
            fu = exact_upper(v)
            row.append(ceil_div(fu.numerator * 2 ** P_LOG, fu.denominator))
        L.append(row)
    return L


def g_up_scaled(k, L):
    """integer array G over level-0 index i, with G[i] / 2^(P_LOG+1+k) = g_up(i). Exact (integer recursion with the
    average replaced by a sum and the agree case doubled; one factor 2 per level)."""
    import numpy as np
    F = k + 1
    N = 2 ** (k + 2)
    term = np.empty(N, dtype=object)
    for j in range(N):
        s = j >> F; q = (j >> 1) & (2 ** k - 1); a = j & 1
        if a == s:
            term[j] = 2 * L[q][a]                                   # 2^(P+1) * (-log2 T(a|q))
        else:
            term[j] = L[q][0] + L[q][1] - 2 ** (P_LOG + 1)         # 2^(P+1) * (-1 - (log2 T0 + log2 T1)/2)
    V = term.reshape(2, N // 2)
    for m in range(k - 1, -1, -1):
        b = k - m
        hi = 2 ** (F - 1 - b)
        V4 = V.reshape(2, hi, 2, 2 ** b)  # [s, field bits above b, bit b, field bits below b]
        W = np.empty_like(V4)
        W[0, :, 0, :] = 2 * V4[0, :, 0, :]
        W[1, :, 1, :] = 2 * V4[1, :, 1, :]
        avg = V4[0, :, 1, :] + V4[1, :, 0, :]
        W[0, :, 1, :] = avg
        W[1, :, 0, :] = avg
        V = W.reshape(2, N // 2)
    return V.reshape(N)


def g_up_brute_check(k, L, G):
    """(S4) exact path-enumeration of g_up against the integer recursion."""
    F = k + 1
    term = []
    for j in range(2 ** (k + 2)):
        s = j >> F; q = (j >> 1) & (2 ** k - 1); a = j & 1
        if a == s:
            term.append(Fraction(L[q][a], 2 ** P_LOG))
        else:
            term.append(Fraction(L[q][0] + L[q][1], 2 ** (P_LOG + 1)) - 1)
    gb = g_brute(k, term)
    sc = 2 ** (P_LOG + 1 + k)
    for i in range(len(gb)):
        if gb[i] * sc != G[i]:
            raise SystemExit(f"FAIL (S4) g_up recursion != path enumeration at i={i}")
    return True


# ---------------------------------------------------------------- main check
def verify(path, quiet=False, cert=None):
    t0 = time.time()
    raw = open(path, "rb").read() if cert is None else None
    C = json.loads(raw) if cert is None else cert
    assert C["route"] == "collapsed" and C["channel"] == "trapdoor"
    k = int(C["k"]); nQ = 2 ** k; nW = 2 ** (k + 1)
    Tden = int(C["T_den"]); T0 = [int(v) for v in C["T0_num"]]
    assert len(T0) == nQ and all(0 < n < Tden for n in T0), "T rows must lie strictly in (0,1)"
    hden = int(C["h_den"]); hn = [int(v) for v in C["h_num"]]
    assert len(hn) == nW and hden > 0
    L = log_upper_ints(T0, Tden)
    G = g_up_scaled(k, L)  # scale 2^E1, E1 = P+1+k
    if k <= 8:
        g_up_brute_check(k, L, G)
    E1 = P_LOG + 1 + k
    # common scale: residual * D, D = 2 * lcm(2^E1, hden) handled as Fractions per term would be slow -> integers:
    # residual = G/2^E1 + Eh - h with Eh = h(next) (agree) or (h(next0)+h(next1))/2 (disagree).
    # Multiply by M = 2 * 2^E1 * hden: R = 2*hden*G + 2^(E1) * (2*hnext or hnext0+hnext1) - 2^(E1+1)*h(w)
    import numpy as np
    Hh = np.array(hn, dtype=object).reshape(2, nQ)          # [s', low k bits]
    G3 = G.reshape(2, 2, nQ)                                # [s, x_1, (x_2..x_k a)]
    Ew = np.empty((2, 2, nQ), dtype=object)                  # 2 * h_num(next), exact
    Ew[0, 0, :] = 2 * Hh[0]
    Ew[1, 1, :] = 2 * Hh[1]
    Ew[0, 1, :] = Hh[0] + Hh[1]
    Ew[1, 0, :] = Hh[0] + Hh[1]
    hw = np.array(hn, dtype=object).reshape(2, 2, nQ // 2, 1)  # h(w), w = (s, x_1, x_2..x_k); action a is the last bit
    hw = np.concatenate([hw, hw], axis=3).reshape(2, 2, nQ)
    R = 2 * hden * G3 + (2 ** E1) * (Ew - 2 * hw)
    flat = R.reshape(-1)
    ibest = max(range(len(flat)), key=lambda i: flat[i])
    best = Fraction(int(flat[ibest]), 2 * hden * 2 ** E1)
    dt = time.time() - t0
    dec12 = ceil_div(best.numerator * 10 ** 12, best.denominator)
    dec15 = ceil_div(best.numerator * 10 ** 15, best.denominator)
    s_ = ibest >> (k + 1); fld = ibest & (nW - 1)
    arg = (s_, format(fld >> 1, f"0{k}b"), fld & 1)
    sha = hashlib.sha256(raw).hexdigest() if raw is not None else None
    ok = True
    if "claimed_rho_upper" in C:
        claim = Fraction(C["claimed_rho_upper"])
        ok = best <= claim
    if not quiet:
        print(f"cert {path}")
        print(f"  k={k} states={nW} state-actions={2*nW}; T rows in (0,1): PASS; logs: arb {ctx.prec}-bit, dyadic 2^-{P_LOG} up"
              + ("; (S4) g_up == path enumeration: PASS" if k <= 8 else ""))
        print(f"  rho_up (rounded up) = {dec12 // 10**12}.{dec12 % 10**12:012d}   [15 dp: {dec15 // 10**15}.{dec15 % 10**15:015d}]"
              f"   argmax (s, x_1..x_k, a) = {arg}")
        if "claimed_rho_upper" in C:
            print(f"  claimed_rho_upper = {C['claimed_rho_upper']}: {'PASS' if ok else 'FAIL (computed rho_up exceeds claim)'}")
        if sha:
            print(f"  sha256 {sha}")
        print(f"  verifier time {dt:.2f}s")
    return best, ok, dt, sha


def main(paths):
    t = time.time()
    selftest_channel(6)
    selftest_g(6)
    print(f"self-tests (S1) Kobayashi-Morita n<=6, (S2) coin form n<=6, (S3) operator g == brute force k=1..6: PASS ({time.time()-t:.1f}s)")
    allok = True
    for p in paths:
        _, ok, _, _ = verify(p)
        allok = allok and ok
    if not allok:
        print("RESULT: FAIL")
        sys.exit(1)
    print("RESULT: PASS")


if __name__ == "__main__":
    main(sys.argv[1:])
