"""Blind evaluator: L_N = H(Y_N | Y^{N-1}, H_0) - Pr(X != S) for the trapdoor channel
driven by a run-length input automaton.  Rigorous: exact integer/rational arithmetic for
all probabilities and the stationary law; arb balls (python-flint) only for the logs.

usage: td_ln.py <automaton file> <outfile> [--perturb-first DELTA_NUM/DELTA_DEN] [--iid-half] [--levels 10,11,12]
"""
import sys, hashlib, math
from fractions import Fraction
import numpy as np
import flint
from flint import fmpq, fmpq_mat, arb, ctx
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import connected_components

ctx.prec = 320


def read_auto(path):
    with open(path) as f:
        lines = [l.strip() for l in f if l.strip()]
    hd = lines[0].split()
    assert hd[0] == '#' and hd[1] == 'auto'
    A, B, C = map(int, hd[2:5])
    p = {}
    order = []
    for l in lines[1:]:
        a, r1, r2, pr = l.split()
        key = (int(a), int(r1), int(r2))
        assert key not in p
        p[key] = Fraction(pr)
        order.append(key)
    assert len(p) == A * B * C
    for k, v in p.items():
        assert 0 <= v <= 1
        assert 1 <= k[0] <= A and 1 <= k[1] <= B and 1 <= k[2] <= C
    return A, B, C, p, order


def build(A, B, C, p):
    nq = 2 * A * B * C
    n = 2 * nq

    def idx(v, a, r1, r2, s):
        return ((((v * A + (a - 1)) * B + (r1 - 1)) * C + (r2 - 1)) * 2) + s

    den = 1
    for v in p.values():
        den = den * v.denominator // math.gcd(den, v.denominator)
    D = 2 * den  # common denominator for all transition weights
    # trans[y] : list of (h, h2, weight_int) ; prob = weight/D
    trans = {0: [], 1: []}
    pxs = np.zeros(n, dtype=object)  # D * Pr(X != S | h)
    for v in (0, 1):
        for a in range(1, A + 1):
            for r1 in range(1, B + 1):
                for r2 in range(1, C + 1):
                    pc = p[(a, r1, r2)]
                    for x, px in ((v, pc), (1 - v, 1 - pc)):
                        if px == 0:
                            continue
                        if x == v:
                            q2 = (v, min(a + 1, A), r1, r2)
                        else:
                            q2 = (x, 1, min(a, B), min(r1, C))
                        W = px * D
                        assert W.denominator == 1 and (W.numerator % 2 == 0)
                        W = W.numerator
                        for s in (0, 1):
                            h = idx(v, a, r1, r2, s)
                            if x == s:
                                trans[s].append((h, idx(*q2, s), W))
                            else:
                                pxs[h] += W
                                for y in (0, 1):
                                    s2 = x ^ y ^ s
                                    trans[y].append((h, idx(*q2, s2), W // 2))
    for h in range(n):
        if pxs[h] == 0:
            pxs[h] = 0
    return n, D, trans, pxs


def stationary(n, D, trans):
    # merged transition integer matrix (weights /D)
    P = {}
    for y in (0, 1):
        for h, h2, w in trans[y]:
            P[(h, h2)] = P.get((h, h2), 0) + w
    rowsum = np.zeros(n, dtype=object)
    for (h, h2), w in P.items():
        rowsum[h] += w
    assert all(int(r) == D for r in rowsum), "rows must sum to 1"
    r = np.array([k[0] for k in P]); c = np.array([k[1] for k in P])
    G = csr_matrix((np.ones(len(r)), (r, c)), shape=(n, n))
    ncomp, lab = connected_components(G, directed=True, connection='strong')
    closed = []
    for comp in range(ncomp):
        mem = set(np.nonzero(lab == comp)[0].tolist())
        ok = all((h2 in mem) for (h, h2) in P if h in mem)
        if ok:
            closed.append(sorted(mem))
    assert len(closed) == 1, f"closed classes: {len(closed)}"
    Cl = closed[0]
    m = len(Cl)
    pos = {h: i for i, h in enumerate(Cl)}
    # solve pi (P - I) = 0 on Cl, sum pi = 1  ->  M pi^T = e_last
    M = [[0] * m for _ in range(m)]
    for (h, h2), w in P.items():
        if h in pos:
            M[pos[h2]][pos[h]] += fmpq(w, D)
    for i in range(m):
        M[i][i] -= 1
    M[m - 1] = [1] * m
    rhs = [[0] for _ in range(m)]
    rhs[m - 1] = [1]
    sol = fmpq_mat(M).solve(fmpq_mat(rhs))
    pi = [fmpq(0)] * n
    for i, h in enumerate(Cl):
        pi[h] = sol[i, 0]
    # exact checks
    assert sum(pi) == 1
    assert all(pi[h] > 0 for h in Cl)
    acc = [fmpq(0)] * n
    for (h, h2), w in P.items():
        if pi[h] != 0:
            acc[h2] += pi[h] * fmpq(w, D)
    assert all(acc[h] == pi[h] for h in range(n)), "pi P != pi"
    # aperiodicity info: period of closed class
    return pi, Cl, ncomp


def row_form(n, trans):
    # for each y: arrays col1,w1,col2,w2 (each row has <=2 entries per y)
    out = {}
    for y in (0, 1):
        ent = [[] for _ in range(n)]
        for h, h2, w in trans[y]:
            ent[h].append((h2, w))
        cols = []
        for h in range(n):
            d = {}
            for h2, w in ent[h]:
                d[h2] = d.get(h2, 0) + w
            cols.append(list(d.items()))
        kmax = max(len(e) for e in cols)
        CI = np.zeros((kmax, n), dtype=np.int64)
        WI = np.zeros((kmax, n), dtype=object)
        for h in range(n):
            for k, (h2, w) in enumerate(cols[h]):
                CI[k, h] = h2; WI[k, h] = w
        out[y] = (CI, WI)
    return out


def entropy_sums(levels_vecs, Cl):
    """S(h0) = sum_y b log2 b over sequences, arb, for h0 in Cl."""
    ln2 = arb(2).log()
    S = {}
    for h in Cl:
        S[h] = arb(0)
    for b in levels_vecs:
        for h in Cl:
            v = b[h]
            if v > 1:
                S[h] += arb(v) * arb(v).log()
    for h in Cl:
        S[h] = S[h] / ln2
    return S


def main():
    args = sys.argv[1:]
    path, outp = args[0], args[1]
    levels = [10, 11, 12]
    perturb = None
    iid = False
    if '--levels' in args:
        levels = [int(t) for t in args[args.index('--levels') + 1].split(',')]
    if '--perturb-first' in args:
        perturb = Fraction(args[args.index('--perturb-first') + 1])
    if '--iid-half' in args:
        iid = True
    A, B, C, p, order = read_auto(path)
    notes = []
    if iid:
        p = {k: Fraction(1, 2) for k in p}
        notes.append('all p replaced by 1/2 (iid fair input)')
    if perturb is not None:
        k0 = order[0]
        newp = p[k0] + perturb
        assert 0 <= newp <= 1
        notes.append(f'p{k0}: {p[k0]} -> {newp}')
        p[k0] = newp
    n, D, trans, pxs = build(A, B, C, p)
    pi, Cl, ncomp = stationary(n, D, trans)
    pdiff = sum(pi[h] * fmpq(int(pxs[h]), D) for h in range(n))
    rf = row_form(n, trans)
    Nmax = max(levels)
    ln2 = arb(2).log()
    log2D = arb(D).log() / ln2
    Hn = {}
    cur = [np.ones(n, dtype=object)]  # length 0: P(empty|h0)=1 -> scaled by D^0
    for L in range(1, Nmax + 1):
        new = []
        for y in (0, 1):
            CI, WI = rf[y]
            for b in cur:
                nb = WI[0] * b[CI[0]]
                for k in range(1, CI.shape[0]):
                    nb = nb + WI[k] * b[CI[k]]
                new.append(nb)
        cur = new
        # exact check: sum_y P(y^L|h0) = 1
        tot = cur[0].copy()
        for b in cur[1:]:
            tot = tot + b
        DL = D ** L
        assert all(int(t) == DL for t in tot), f"normalisation fails at L={L}"
        if L in levels:
            S = entropy_sums(cur, Cl)
            H = arb(0)
            for h in Cl:
                H += arb(pi[h]) * (L * log2D - S[h] / arb(DL))
            Hn[L] = H
            print(f'L={L} H(Y^L|H0)={H.str(30, radius=True)}', flush=True)
    pd = arb(pdiff)
    res = {}
    for L in levels:
        if L - 1 in Hn or L == 1:
            Hprev = Hn[L - 1] if L > 1 else arb(0)
            res[L] = Hn[L] - Hprev - pd
    with open(outp, 'w') as f:
        f.write(f'# td_ln.py input={path} sha256={hashlib.sha256(open(path, "rb").read()).hexdigest()}\n')
        f.write(f'# A,B,C={A},{B},{C} states={n} D={D} SCCs={ncomp} closed_class_size={len(Cl)} notes={notes}\n')
        f.write(f'# prec={ctx.prec} bits; pi exact rational, pi P = pi checked exactly; normalisation checked exactly\n')
        f.write(f'PrXneS = {pdiff}  ~ {pd.str(40)}\n')
        for L in sorted(Hn):
            f.write(f'H(Y^{L}|H0) = {Hn[L].str(40, radius=True)}\n')
        for L in sorted(res):
            r = res[L]
            f.write(f'L_{L} = {r.str(40, radius=True)}   mid={r.mid().str(45)} rad={r.rad().str(5)}\n')
    print(open(outp).read())


if __name__ == '__main__':
    main()
