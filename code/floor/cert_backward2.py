"""cert_backward2.py THETAFILE N [--nb NB] [--chunk ELEMS]
Certified lower bound L_N - E on the trapdoor feedforward capacity from an order-K Markov input.
Same L_N and same backward recursion as ../build-lb2/cert_backward.py, but the library log2 is REPLACED by
log2_rig, a routine built only from IEEE +, -, *, / and frexp (exact), with a proven relative error bound LAMBDA
(ERROR-LEMMA2.md). Assumption A1 only: numpy +, -, *, / on float64 arrays are single correctly rounded
(round-to-nearest) IEEE binary64 operations; frexp is exact. No other library accuracy is assumed.
Input range of log2_rig: positive normal x with 2^-1000 <= x < 2 (checked a priori in certify(), see ERROR-LEMMA2.md Sec. 3)."""
import sys, time, math
from fractions import Fraction as F
import numpy as np
import flint
from flint import fmpq, arb
from trapcommon import load_input, build_rows_gen, exact_pi_gen, sha256_file

U = F(1, 2 ** 53)          # unit roundoff, binary64, round to nearest
TINY = 2.0 ** -1000

# ---------------- log2_rig constants (all enclosed rigorously, checked at import) ----------------
KT = 10                    # number of series terms: P(w) = sum_{k<KT} w^k/(2k+1)
CTHR = 0.7071067811865476  # float threshold C; mantissa reduced into [C, 2C)
flint.ctx.prec = 300
_ln2 = arb(2).log()
_inv = 1 / _ln2
C2 = 2.0 * float(_inv.mid())      # 2/ln2 rounded to nearest (power-of-two scaling of the float 1/ln2 is exact)
_c1 = C2 / 2.0
assert abs(arb(_c1) - _inv) < arb(1) / arb(2 ** 53) * _inv, 'float(1/ln2) relative error must be <= u'   # certified by arb
assert abs(arb(C2) - 2 * _inv) < arb(1) / arb(2 ** 53) * 2 * _inv
RC = U                     # relative error of the stored constant C2 vs 2/ln2 (verified just above)
HC = [float(F(1, 2 * k + 1)) for k in range(KT)]   # Fraction->float is correctly rounded: relative error <= u; HC[0] == 1.0 exactly
assert HC[0] == 1.0
# range of z0 = (m-1)/(m+1) for m in [C, 2C): |z0| <= ZMAX, w0 = z0^2 <= WMAX (exact rational check)
_Cq, _2Cq = F(CTHR), F(2 * CTHR)
ZMAX = F(1716, 10000)
assert abs((_Cq - 1) / (_Cq + 1)) <= ZMAX and abs((_2Cq - 1) / (_2Cq + 1)) <= ZMAX
WMAX = F(295, 10000)
assert ZMAX * ZMAX <= WMAX
TAU = WMAX ** KT / ((2 * KT + 1) * (1 - WMAX))      # relative truncation bound (P >= 1)
NPOW = 2 * KT + 11                                    # exponent in (1+u)^NPOW, ERROR-LEMMA2.md Sec. 2
GAMMA_LOG = (1 + U) ** NPOW * (1 + RC) - 1 + TAU      # relative error of g = log2(m') (mantissa part)
KAPPA = F(21, 20)                                     # |log2 m'| / |e + log2 m'| for e != 0
LAMBDA = KAPPA * GAMMA_LOG * (1 + U) + U              # relative error of log2_rig on its whole input range


def log2_rig(x, buf=None):
    """Vectorised log2 of positive normal x in [2^-1000, 2) (and of 0 -> some finite value, harmless since multiplied by 0).
    Uses only frexp, +, -, *, / on float64 arrays and the constants above. Relative error <= LAMBDA (proved)."""
    m, e = np.frexp(x)                 # x = m * 2^e exactly, m in [0.5, 1)
    lo = (m < CTHR)
    m += m * lo                        # exact: m -> 2m where m < C
    ef = e.astype(np.float64)
    ef -= lo                           # exact small integers
    d = m - 1.0                        # exact (Sterbenz) since m in [0.5, 2]
    s = m + 1.0
    z = d / s
    w = z * z
    q = np.full_like(w, HC[KT - 1])
    for k in range(KT - 2, -1, -1):
        q *= w
        q += HC[k]
    z *= q
    z *= C2
    ef += z                            # when ef == 0 this is exact (0 + g = g)
    return ef


def err_bound(N, m, eps, lam):
    """Bound on |computed H(Y^m|h) - true H(Y^m|h)| (ERROR-LEMMA2.md, Lemma 3). eps = relative error of beta-tilde."""
    eta = (1 + lam) * (1 + U) - 1
    gam = (1 + U) ** N - 1
    S = m + eps * (m + 2)
    return gam * (1 + eta) * S + eta * S + eps * (m + 2)


def floor_dec(x, digits):
    n = math.floor(x * 10 ** digits)
    sign = '-' if n < 0 else ''
    n = abs(n)
    s = str(n).rjust(digits + 1, '0')
    return sign + s[:-digits] + '.' + s[-digits:]


def float_rows(R, M):
    out = {}
    amin = None
    for y in (0, 1):
        terms = [[] for _ in range(M)]
        for h, j, p in R[y]:
            terms[h].append((j, float(p)))   # Fraction -> float is correctly rounded
        j1 = np.zeros(M, dtype=np.int64); j2 = np.zeros(M, dtype=np.int64)
        a1 = np.zeros(M); a2 = np.zeros(M)
        for h in range(M):
            assert len(terms[h]) <= 2
            if len(terms[h]) >= 1:
                j1[h], a1[h] = terms[h][0]
            if len(terms[h]) == 2:
                j2[h], a2[h] = terms[h][1]
        for a in (a1, a2):
            pos = a[a > 0]
            if len(pos):
                amin = float(pos.min()) if amin is None else min(amin, float(pos.min()))
        out[y] = (j1, a1[:, None], j2, a2[:, None])
    return out, amin


def apply(rows, y, B):
    j1, a1, j2, a2 = rows[y]
    t = B[j1]
    t *= a1
    t2 = B[j2]
    t2 *= a2
    t += t2
    return t


def tree_sum_cols(x):
    while x.shape[1] > 1:
        h = x.shape[1] // 2
        x = x[:, :h] + x[:, h:]
    return x[:, 0]


def tree_sum_rows(x):
    n = x.shape[0]
    p = 1
    while p < n:
        p *= 2
    if p != n:
        x = np.concatenate([x, np.zeros((p - n, x.shape[1]))], axis=0)
    while x.shape[0] > 1:
        h = x.shape[0] // 2
        x = x[:h] + x[h:]
    return x[0]


def xlogx_cols(Bl, chunk):
    """sum over columns (pairwise) of Bl * log2_rig(Bl); the product is formed in place, row blocks keep temporaries small."""
    T = np.empty_like(Bl)
    M, cols = Bl.shape
    r = max(1, chunk // cols)
    for i in range(0, M, r):
        blk = Bl[i:i + r]
        L = log2_rig(blk)
        L *= blk
        T[i:i + r] = L
    return tree_sum_cols(T)


def run_kernel(rows, M, N, nb, log=None, chunk=1 << 18):
    r = N - nb
    leaves_N, leaves_m = [], []
    stats = {'minpos': np.inf, 'maxb': 0.0, 'nan': False}
    B = np.ones((M, 1))
    for _ in range(nb):
        B = np.concatenate([apply(rows, 0, B), apply(rows, 1, B)], axis=1)
    t0 = time.time()
    cnt = [0]

    def leaf(Bl):
        # diagnostics only (the proof uses the a-priori bound checked in certify)
        pos = Bl[Bl > 0]
        stats['minpos'] = min(stats['minpos'], float(pos.min()))
        stats['maxb'] = max(stats['maxb'], float(Bl.max()))
        if np.isnan(Bl).any():
            stats['nan'] = True
        leaves_N.append(xlogx_cols(Bl, chunk))
        Bm = Bl[:, 0::2] + Bl[:, 1::2]
        leaves_m.append(xlogx_cols(Bm, chunk))
        cnt[0] += 1
        if log and (cnt[0] & (cnt[0] - 1)) == 0:
            log('  leaf %d/%d  %.1fs' % (cnt[0], 2 ** r, time.time() - t0))

    def dfs(d, Bc):
        if d == r:
            leaf(Bc)
            return
        for y in (0, 1):
            dfs(d + 1, apply(rows, y, Bc))

    dfs(0, B)
    SN = tree_sum_rows(np.array(leaves_N))
    Sm = tree_sum_rows(np.array(leaves_m))
    return SN, Sm, stats


def certify(path, N, nb=None, log=print, pre=None, chunk=1 << 18):
    t0 = time.time()
    inp = load_input(path)
    M = 2 * inp.nq
    R, pxs_w = build_rows_gen(inp)
    pi, pxs = pre if pre is not None else exact_pi_gen(inp, R, pxs_w)
    t_pi = time.time() - t0
    if nb is None:
        nb = min(N, 18 if M <= 256 else 17 if M <= 512 else 16)
    nb = min(nb, N)
    rows, amin = float_rows(R, M)
    # A-priori range check (ERROR-LEMMA2.md Sec. 3): every computed positive value is >= amin^N / 2 >= 2^-1000 (normal), all values < 2.
    assert F(amin) ** N / 2 > F(1, 2 ** 1000), 'a-priori underflow bound fails'
    epsN = (1 + U) ** (3 * N) - 1
    assert 1 + epsN < 2
    SN, Sm, stats = run_kernel(rows, M, N, nb, log, chunk)
    assert not stats['nan']
    assert np.isfinite(SN).all() and np.isfinite(Sm).all()
    L = fmpq(0)
    for h in range(M):
        if pi[h] == 0:
            continue
        a = fmpq(*float(-SN[h]).as_integer_ratio())
        b = fmpq(*float(-Sm[h]).as_integer_ratio())
        L += pi[h] * (a - b)
    L -= pxs
    Lf = F(int(L.p), int(L.q))
    epsm = (1 + epsN) * (1 + U) - 1
    E = err_bound(N, N, epsN, LAMBDA) + err_bound(N, N - 1, epsm, LAMBDA)
    lower = Lf - E
    return dict(K=inp.label, N=N, nb=nb, Lcomp=Lf, E=E, lower=lower, pxs=F(int(pxs.p), int(pxs.q)), stats=stats,
                amin=amin, time=time.time() - t0, t_pi=t_pi)


if __name__ == '__main__':
    args = sys.argv[1:]
    nb = None
    chunk = 1 << 18
    if '--nb' in args:
        i = args.index('--nb'); nb = int(args[i + 1]); del args[i:i + 2]
    if '--chunk' in args:
        i = args.index('--chunk'); chunk = int(args[i + 1]); del args[i:i + 2]
    path, N = args[0], int(args[1])
    info = certify(path, N, nb, log=lambda s: print(s, flush=True), chunk=chunk)
    print('input sha256 =', sha256_file(path))
    print('input %s N=%d nb=%d  (proven log2 routine: LAMBDA = %.4e = 2^%.2f, series terms %d)' % (
        info['K'], N, info['nb'], float(LAMBDA), math.log2(float(LAMBDA)), KT))
    print('Pr(X != S) exact ~', float(info['pxs']))
    print('a-priori: smallest positive float coefficient %.6e, amin^N/2 = %.3e > 2^-1000' % (info['amin'], float(F(info['amin']) ** N / 2)))
    print('observed (diagnostic): min positive beta-tilde = %.3e  max beta-tilde = %.17g' % (info['stats']['minpos'], info['stats']['maxb']))
    print('L_N computed (exact combination of float entropies) = ' + floor_dec(info['Lcomp'], 16) + ' (rounded down)')
    print('rigorous error bound E = %.3e' % float(info['E']))
    print('CERTIFIED LOWER ENDPOINT:', floor_dec(info['lower'], 14))
    print('time pi %.1fs total %.1fs' % (info['t_pi'], info['time']))
