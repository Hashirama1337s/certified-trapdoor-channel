"""trapcommon.py: shared exact pieces for the trapdoor input-law certifier (build-lb2).
Hidden state h = 2*c + s, c = K-bit context (oldest bit = most significant), s = ball.
Channel (as in lead/cert_lb.py): x = s -> y = s, s' = s; x != s -> y in {0,1} w.p. 1/2 each, s' = x^y^s."""
import hashlib
from fractions import Fraction as F
import flint
from flint import fmpq, fmpq_mat


def load_theta(path):
    lines = [l.split() for l in open(path) if l.strip() and not l.startswith('#')]
    K = len(lines[0][0])
    th = []
    for i, (c, v) in enumerate(lines):
        assert len(c) == K and int(c, 2) == i, 'contexts must be in lexicographic order'
        f = F(v)
        assert 0 <= f <= 1
        th.append(f)
    assert len(th) == 2 ** K
    return K, th


def sha256_file(path):
    return hashlib.sha256(open(path, 'rb').read()).hexdigest()


def build_rows(K, th):
    """Exact transition entries. R[y] = list of (h, j, prob) with prob = Pr(Y=y, H'=j | H=h) (Fractions, > 0).
    pxs_w[h] = Pr(X != s | h)."""
    nc = 2 ** K
    mask = nc - 1
    R = {0: [], 1: []}
    pxs_w = [F(0)] * (2 * nc)
    for c in range(nc):
        for s in (0, 1):
            h = 2 * c + s
            for x in (0, 1):
                px = th[c] if x == 1 else 1 - th[c]
                if px == 0:
                    continue
                nci = ((c << 1) | x) & mask
                if x == s:
                    R[x].append((h, 2 * nci + s, px))
                else:
                    pxs_w[h] += px
                    for y in (0, 1):
                        R[y].append((h, 2 * nci + (x ^ y ^ s), px / 2))
    return R, pxs_w


def exact_pi(K, R, pxs_w, M=None):
    """Exact stationary law of the hidden chain (python-flint fmpq_mat solve), verified pi P = pi exactly,
    pi >= 0, sum = 1. Returns (pi list of fmpq, pxs fmpq)."""
    M = M if M is not None else 2 * 2 ** K
    ent = {}
    for y in (0, 1):
        for h, j, p in R[y]:
            ent[(h, j)] = ent.get((h, j), F(0)) + p
    rows_by_col = {}
    for (h, j), p in ent.items():
        rows_by_col.setdefault(j, []).append((h, p))
    flat = [fmpq(0)] * (M * M)
    for i in range(M):
        for h, p in rows_by_col.get(i, []):
            flat[i * M + h] += fmpq(p.numerator, p.denominator)
        flat[i * M + i] -= 1
    for j in range(M):
        flat[(M - 1) * M + j] = fmpq(1)
    Amat = fmpq_mat(M, M, flat)
    b = fmpq_mat(M, 1, [fmpq(0)] * (M - 1) + [fmpq(1)])
    x = Amat.solve(b)
    pi = [x[i, 0] for i in range(M)]
    assert sum(pi) == 1 and all(p >= 0 for p in pi), 'pi'
    for i in range(M):
        assert sum((pi[h] * fmpq(p.numerator, p.denominator) for h, p in rows_by_col.get(i, [])), fmpq(0)) == pi[i], 'pi P = pi'
    pxs = sum((pi[h] * fmpq(pxs_w[h].numerator, pxs_w[h].denominator) for h in range(M)), fmpq(0))
    return pi, pxs


# ---- generalisation: any finite input automaton (state q, next state nxt[x][q], Pr(x=1|q) = p1[q]) ----
class Inp:
    pass


def markov_input(K, th):
    inp = Inp()
    nc = 2 ** K
    inp.nq = nc
    inp.p1 = list(th)
    inp.nxt = [[((c << 1) | x) & (nc - 1) for c in range(nc)] for x in (0, 1)]
    inp.label = 'K=%d' % K
    return inp


def run_automaton(A, B, C, pc):
    """pc[(a,r1,r2)] = Pr(continue current run | current run age a (capped at A), previous run length r1 (cap B), run before r2 (cap C)).
    State q = (v, a, r1, r2), v = current symbol. Pr(x=1|q) = pc if v == 1 else 1-pc."""
    states = [(v, a, r1, r2) for v in (0, 1) for a in range(1, A + 1) for r1 in range(1, B + 1) for r2 in range(1, C + 1)]
    idx = {q: i for i, q in enumerate(states)}
    inp = Inp()
    inp.nq = len(states)
    inp.p1 = []
    inp.nxt = [[0] * inp.nq for _ in (0, 1)]
    for i, (v, a, r1, r2) in enumerate(states):
        p = pc[(a, r1, r2)]
        inp.p1.append(p if v == 1 else 1 - p)
        for x in (0, 1):
            if x == v:
                nq = (v, min(a + 1, A), r1, r2)
            else:
                nq = (x, 1, min(a, B), min(r1, C))
            inp.nxt[x][i] = idx[nq]
    inp.label = 'RL(%d,%d,%d)' % (A, B, C)
    inp.states = states
    return inp


def load_input(path):
    """Markov theta file (K-bit contexts) or run-length automaton file: first line '# auto A B C', then lines 'a r1 r2 p'."""
    first = open(path).readline().split()
    if first[:2] == ['#', 'auto']:
        A, B, C = int(first[2]), int(first[3]), int(first[4])
        pc = {}
        for l in open(path):
            if l.strip() and not l.startswith('#'):
                a, r1, r2, p = l.split()
                pc[(int(a), int(r1), int(r2))] = F(p)
        assert len(pc) == A * B * C
        return run_automaton(A, B, C, pc)
    K, th = load_theta(path)
    return markov_input(K, th)


def build_rows_gen(inp):
    nq = inp.nq
    R = {0: [], 1: []}
    pxs_w = [F(0)] * (2 * nq)
    for q in range(nq):
        for s in (0, 1):
            h = 2 * q + s
            for x in (0, 1):
                px = inp.p1[q] if x == 1 else 1 - inp.p1[q]
                if px == 0:
                    continue
                nq2 = inp.nxt[x][q]
                if x == s:
                    R[x].append((h, 2 * nq2 + s, px))
                else:
                    pxs_w[h] += px
                    for y in (0, 1):
                        R[y].append((h, 2 * nq2 + (x ^ y ^ s), px / 2))
    return R, pxs_w


def exact_pi_gen(inp, R, pxs_w):
    return exact_pi(None, R, pxs_w, M=2 * inp.nq)
