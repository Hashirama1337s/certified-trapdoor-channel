# Referee (ub3) independent checker for collapsed certificates. Written from the definitions in the brief,
# not from verify_collapsed.py. Different log library (mpmath interval arithmetic), different dyadic grid (2^-200),
# different index convention internally (oldest symbol = LSB), Fraction residuals.
#
# Channel (brief): state s, input x. If x == s then y = x (state stays). Else y in {x, s} w.p. 1/2, s' = x ^ y ^ s.
# g(s; z_1..z_k, a) = E[ r(a, S_k, (Y_1..Y_k)) | S_0 = s, inputs z_1..z_k ]
# r(c, s, q) = D(P(.|c,s) || T(.|q)) bits.
# rho = max_{w=(s,x_1..x_k), a} g(s; x_1..x_k, a) + sum_s' K(s'|x_1,s) h(s', x_2..x_k, a) - h(w)
import sys, json, itertools, random, time
from fractions import Fraction
from mpmath import iv, mp

P = 200
iv.prec = 300
mp.prec = 400


def chan(x, s):
    if x == s:
        return [(x, Fraction(1), s)]
    return [(y, Fraction(1, 2), x ^ y ^ s) for y in (x, s)]


def neglog2_upper(num, den):
    """integer L with L / 2^P >= -log2(num/den), rigorous via mpmath interval arithmetic."""
    v = -iv.log(iv.mpf(num) / iv.mpf(den)) / iv.log(iv.mpf(2))
    sign, man, exp, bc = v._mpi_[1]
    val = Fraction(int(man) * (2 ** exp if exp >= 0 else 1), 1 if exp >= 0 else 2 ** (-exp))
    if sign:
        val = -val
    # sanity: high-precision point value must lie inside the interval
    pt = -mp.log(mp.mpf(num) / den) / mp.log(2)
    lo_s, lo_m, lo_e, _ = v._mpi_[0]
    lo = Fraction(int(lo_m) * (2 ** lo_e if lo_e >= 0 else 1), 1 if lo_e >= 0 else 2 ** (-lo_e))
    if lo_s:
        lo = -lo
    assert lo <= Fraction(mp.nstr(pt, 100)) + Fraction(1, 10 ** 90) and Fraction(mp.nstr(pt, 100)) - Fraction(1, 10 ** 90) <= val
    assert val - lo < Fraction(1, 2 ** 250)
    n = val.numerator * 2 ** P
    return -((-n) // val.denominator)  # ceil


def rev(v, k):
    return int(format(v, f"0{k}b")[::-1], 2) if k > 0 else 0


def terminal(k, rfun):
    """my index: idx = s*2^(k+1) + sum_{i=1..k+1} z_i 2^(i-1) (oldest LSB). Terminal holds r(z_{k+1}, s, q=z_1..z_k)."""
    N = 2 ** (k + 2)
    out = [None] * N
    for idx in range(N):
        s = idx >> (k + 1)
        word = idx & (2 ** (k + 1) - 1)
        a = (word >> k) & 1
        ylow = word & (2 ** k - 1)          # y_1 at bit 0
        qcert = rev(ylow, k)                 # cert convention: oldest = MSB
        out[idx] = rfun(a, s, qcert)
    return out


def g_rec(k, term, scaled):
    """backward over slots k..1. If scaled, values are ints and each level doubles (no halving)."""
    V = list(term)
    SB = 1 << (k + 1)
    for m in range(k - 1, -1, -1):
        bb = 1 << m
        W = [None] * len(V)
        for idx in range(len(V)):
            s = 1 if idx & SB else 0
            b = 1 if idx & bb else 0
            if b == s:
                W[idx] = 2 * V[idx] if scaled else V[idx]
            else:
                p = idx ^ SB ^ bb
                W[idx] = V[idx] + V[p] if scaled else (V[idx] + V[p]) / 2
        V = W
    return V


def g_brute(k, rfun):
    """direct path enumeration with chan(), returns dict keyed by (s, z tuple of length k+1)."""
    out = {}
    for s in (0, 1):
        for z in itertools.product((0, 1), repeat=k + 1):
            lay = [((), Fraction(1), s)]
            for x in z[:k]:
                lay = [(ys + (y,), p * pr, sn) for (ys, p, st) in lay for (y, pr, sn) in chan(x, st)]
            tot = Fraction(0)
            for ys, p, sk in lay:
                q = int("".join(map(str, ys)), 2) if k else 0
                tot += p * rfun(z[k], sk, q)
            out[(s, z)] = tot
    return out


def myidx(s, z, k):
    return (s << (k + 1)) | sum(b << i for i, b in enumerate(z))


def selftest(kmax=6, seed=777):
    rnd = random.Random(seed)
    for k in range(1, kmax + 1):
        tab = {(c, s, q): Fraction(rnd.randint(-999, 999), rnd.randint(1, 999)) for c in (0, 1) for s in (0, 1) for q in range(2 ** k)}
        rf = lambda c, s, q: tab[(c, s, q)]
        V = g_rec(k, terminal(k, rf), False)
        B = g_brute(k, rf)
        for (s, z), val in B.items():
            assert V[myidx(s, z, k)] == val, (k, s, z)
    return True


def lemma_c1_exact(k=3, n=7, seed=5):
    """exact test of Lemma C1 for an arbitrary (random rational) reward table: E[r_t] by full enumeration of the
    channel vs sum_s P(S_{t-k-1}=s) g(s; x_{t-k..t}). All x^n, both s0, all start words qbar, t = k+1..n."""
    rnd = random.Random(seed)
    tab = {(c, s, q): Fraction(rnd.randint(0, 999), rnd.randint(1, 999)) for c in (0, 1) for s in (0, 1) for q in range(2 ** k)}
    rf = lambda c, s, q: tab[(c, s, q)]
    V = g_rec(k, terminal(k, rf), False)
    cnt = 0
    for s0 in (0, 1):
        for xs in itertools.product((0, 1), repeat=n):
            # layers: list of (ys, prob, state) after t steps
            lay = [((), Fraction(1), s0)]
            layers = [lay]
            for x in xs:
                lay = [(ys + (y,), p * pr, sn) for (ys, p, st) in lay for (y, pr, sn) in chan(x, st)]
                layers.append(lay)
            for t in range(k + 1, n + 1):
                Er = Fraction(0)
                for ys, p, st in layers[t - 1]:
                    q = int("".join(map(str, ys[t - 1 - k:t - 1])), 2)
                    Er += p * rf(xs[t - 1], st, q)
                j = t - k - 1
                PS = {0: Fraction(0), 1: Fraction(0)}
                for ys, p, st in layers[j]:
                    PS[st] += p
                rhs = sum(PS[s] * V[myidx(s, xs[j:t], k)] for s in (0, 1))
                assert Er == rhs, (s0, xs, t)
                cnt += 1
    return cnt


def check_cert(path):
    t0 = time.time()
    C = json.load(open(path))
    k = int(C["k"])
    Tden = int(C["T_den"]); T0 = [int(v) for v in C["T0_num"]]
    assert len(T0) == 2 ** k and all(0 < v < Tden for v in T0)
    hden = int(C["h_den"]); hn = [int(v) for v in C["h_num"]]
    assert len(hn) == 2 ** (k + 1) and hden > 0
    L = [(neglog2_upper(v, Tden), neglog2_upper(Tden - v, Tden)) for v in T0]
    two = 2 ** (P + 1)

    def r_scaled(c, s, q):  # 2^(P+1) * r_up
        if c == s:
            return 2 * L[q][c]
        return L[q][0] + L[q][1] - two
    term = terminal(k, r_scaled)
    if k <= 5:  # recursion vs brute force on the certificate's own terminal
        V0 = g_rec(k, [Fraction(v, two) for v in term], False)
        B = g_brute(k, lambda c, s, q: Fraction(r_scaled(c, s, q), two))
        assert all(V0[myidx(s, z, k)] == v for (s, z), v in B.items())
    G = g_rec(k, term, True)
    scale = 2 ** (P + 1 + k)
    best = None; arg = None
    for s in (0, 1):
        for xw in range(2 ** k):                      # cert convention x_1 = MSB
            xs = [(xw >> (k - 1 - i)) & 1 for i in range(k)]
            hw = Fraction(hn[s * 2 ** k + xw], hden)
            x1 = xs[0]
            for a in (0, 1):
                nxt = ((xw << 1) & (2 ** k - 1)) | a  # (x_2..x_k, a)
                if x1 == s:
                    Eh = Fraction(hn[s * 2 ** k + nxt], hden)
                else:
                    Eh = Fraction(hn[nxt] + hn[2 ** k + nxt], 2 * hden)
                g = Fraction(G[myidx(s, xs + [a], k)], scale)
                res = g + Eh - hw
                if best is None or res > best:
                    best, arg = res, (s, "".join(map(str, xs)), a)
    up12 = -((-best.numerator * 10 ** 12) // best.denominator)
    up15 = -((-best.numerator * 10 ** 15) // best.denominator)
    print(f"{path}\n  k={k}  rho_up(ref) 12dp-up = {up12 // 10**12}.{up12 % 10**12:012d}   15dp-up = {up15 // 10**15}.{up15 % 10**15:015d}"
          f"   argmax={arg}   time {time.time()-t0:.1f}s", flush=True)
    if "claimed_rho_upper" in C:
        print(f"  claimed_rho_upper {C['claimed_rho_upper']}: {'PASS' if best <= Fraction(C['claimed_rho_upper']) else 'FAIL'}")
    return best


if __name__ == "__main__":
    t = time.time()
    selftest(6)
    print(f"selftest recursion == channel path enumeration, random rational rewards, k=1..6: PASS ({time.time()-t:.1f}s)")
    if "--c1" in sys.argv:
        t = time.time()
        c = lemma_c1_exact(3, 7)
        c += lemma_c1_exact(2, 6, seed=9)
        print(f"Lemma C1 exact (k=3 n=7, k=2 n=6, all x^n, both s0): {c} identities PASS ({time.time()-t:.1f}s)")
    for p in sys.argv[1:]:
        if p.startswith("--"):
            continue
        check_cert(p)
