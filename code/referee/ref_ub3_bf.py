# Referee (ub3) brute-force test of the BOUND (not the code): for a collapsed certificate with small k, enumerate all
# x^n and all y^n, both s0, all start words qbar, and check path by path (per input sequence x^n)
#   global:  D(P_{Y^n|x^n,s0} || R) <= n rho + K0,  K0 = k |r_max - rho| + (max h - min h)
#   tight:   D <= sum_{t<=k} E r_t + (n-k) rho + h(W_0) - E h(W_{n-k})
# P is built from the channel definition in the brief (not the coin form, not the chain rule). Float64.
# Negative controls: rho - 1e-4 (tight form), and a perturbed T scored with the original rho (both forms).
import sys, json
import numpy as np

def load(path):
    C = json.load(open(path))
    k = int(C["k"]); Tden = int(C["T_den"])
    T0 = np.array([int(v) / Tden for v in C["T0_num"]])
    h = np.array([int(v) for v in C["h_num"]], dtype=float) / int(C["h_den"])
    return k, T0, h

def rtab(T0):
    T = np.stack([T0, 1 - T0], axis=1)            # T[q, y]
    lT = np.log2(T)
    # r[c, s, q]
    r = np.empty((2, 2, len(T0)))
    for c in (0, 1):
        for s in (0, 1):
            r[c, s] = -lT[:, c] if c == s else -1 - (lT[:, 0] + lT[:, 1]) / 2
    return lT, r

def run(k, T0, h, rho, n, label, tol=-1e-9):
    lT, r = rtab(T0)
    rmax = r.max()
    K0 = k * abs(rmax - rho) + (h.max() - h.min())
    N = 2 ** n
    xbits = (np.arange(N)[:, None] >> (n - 1 - np.arange(n))[None, :]) & 1   # x_1 = MSB
    worst_g = np.inf; worst_t = np.inf; maxD = -np.inf
    for s0 in (0, 1):
        # forward: P[t] shape (2^t, 2^t, 2) over (x prefix, y prefix, state)
        Pt = np.zeros((1, 1, 2)); Pt[0, 0, s0] = 1.0
        Ps_hist = [Pt.sum(axis=1)]                 # (2^t, 2): P(S_t = s | x^t)
        layers = [Pt]
        for t in range(n):
            M = Pt.shape[0]
            new = np.zeros((2 * M, 2 * M, 2))
            for x in (0, 1):
                xi = 2 * np.arange(M) + x
                # y = x: state s kept, prob 1 if s == x else 1/2
                fac = np.array([1.0 if s == x else 0.5 for s in (0, 1)])
                new[np.ix_(xi, 2 * np.arange(M) + x, [0, 1])] = Pt * fac[None, None, :]
                # y = 1-x: only from s = 1-x, new state x, prob 1/2
                blk = np.zeros((M, M, 2)); blk[:, :, x] = 0.5 * Pt[:, :, 1 - x]
                new[np.ix_(xi, 2 * np.arange(M) + (1 - x), [0, 1])] = blk
            Pt = new
            if t + 1 <= k:
                layers.append(Pt)
            Ps_hist.append(Pt.sum(axis=1))
        Py = Pt.sum(axis=2)                          # (N x, N y)
        assert np.allclose(Py.sum(axis=1), 1.0)
        with np.errstate(divide="ignore", invalid="ignore"):
            ent = np.where(Py > 0, Py * np.log2(np.where(Py > 0, Py, 1)), 0.0).sum(axis=1)
        ybits = xbits
        for qbar in range(2 ** k):
            # log2 R(y^n): q_0 = qbar, q_t = last k-1 of q_{t-1} then y_t
            logR = np.zeros(N); q = np.full(N, qbar)
            for t in range(n):
                y = ybits[:, t]
                logR += lT[q, y]
                q = ((q << 1) & (2 ** k - 1)) | y
            D = ent - Py @ logR                       # per x^n
            maxD = max(maxD, D.max())
            # tight RHS
            first = np.zeros(N)
            for t in range(1, k + 1):                 # E r_t, t = 1..k, uses Q_{t-1} = qbar shifted by y^{t-1}
                L = layers[t - 1]                     # (2^(t-1), 2^(t-1), 2)
                M = L.shape[0]
                yb = (np.arange(M)[:, None] >> (t - 2 - np.arange(t - 1))[None, :]) & 1 if t > 1 else np.zeros((1, 0), int)
                qq = np.full(M, qbar)
                for i in range(t - 1):
                    qq = ((qq << 1) & (2 ** k - 1)) | yb[:, i]
                xpref = np.arange(N) >> (n - (t - 1)) if t > 1 else np.zeros(N, int)
                xt = xbits[:, t - 1]
                for s in (0, 1):
                    first += (L[xpref, :, s] * r[xt[:, None], s, qq[None, :]]).sum(axis=1)
            w0 = s0 * 2 ** k + (np.arange(N) >> (n - k))
            hW0 = h[w0]
            PS = Ps_hist[n - k][np.arange(N) >> k]   # P(S_{n-k} = s | x^{n-k}), (N, 2)
            tail = np.arange(N) & (2 ** k - 1)
            EhW = PS[:, 0] * h[tail] + PS[:, 1] * h[2 ** k + tail]
            rhs_t = first + (n - k) * rho + hW0 - EhW
            worst_t = min(worst_t, (rhs_t - D).min())
            worst_g = min(worst_g, (n * rho + K0 - D).min())
    vt = "VIOLATION" if worst_t < tol else "OK"
    vg = "VIOLATION" if worst_g < tol else "OK"
    print(f"{label}: k={k} n={n} rho={rho:.12f} K0={K0:.6f} max_x D={maxD:.9f} (n*rho={n*rho:.9f})  "
          f"tight min slack {worst_t:.3e} {vt}   global min slack {worst_g:.3e} {vg}", flush=True)
    return worst_t, worst_g

if __name__ == "__main__":
    path, rho = sys.argv[1], float(sys.argv[2])
    k, T0, h = load(path)
    for n in [int(v) for v in sys.argv[3].split(",")]:
        run(k, T0, h, rho, n, "MAIN  ")
    n = int(sys.argv[3].split(",")[-1])
    run(k, T0, h, rho - 1e-4, n, "NEG rho-1e-4")
    T0p = T0.copy(); T0p[0] = min(0.999, T0p[0] + 0.05)
    run(k, T0p, h, rho, n, "NEG T0[0]+0.05")
