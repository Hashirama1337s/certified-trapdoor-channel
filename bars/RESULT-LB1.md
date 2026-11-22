# RESULT-LB1: scored against BAR-LB1 (seal fac3ef4afd)

Runs: runs/lb1_N14.out, runs/lb1_N13.out, runs/lb1_null.out (lead/cert_lb.py, theta_k4.txt, theta_k4_null.txt; hashes as sealed).

- **P1 HOLD.** L_14 enclosure [0.57412923475585527543 +/- 4.26e-21]; certified lower endpoint 0.574129234755855 (>= 0.5741; midpoint inside [0.574120, 0.574135]).
- **P2 HOLD.** L_13 = [0.57412090100120186401 +/- 3.13e-21] < L_14.
- **P3 HOLD.** 0.5741292 > 0.57246 (largest published estimate of C).
- **P4 HOLD.** 0.5741292 < log2(3/2) = 0.5849625.
- **N1 HOLD.** Perturbed input: L_14 = 0.572686648904838, which is 0.00144 below the P1 midpoint (needed >= 0.0005).

**Verdict: HOLD 5/5.**

In plain words: an explicit signalling strategy that remembers its last 4 balls provably achieves at least 0.5741292 bits per ball by the certified computation, provided the theory step C >= L_N (ARGUED in DESIGN-TRAPDOOR.md, not yet refereed) holds. If it holds, the trapdoor channel's capacity is at least 0.5741292, above both published estimates of the capacity (0.572 and 0.57246) and far above the best rigorous lower bound we could find (0.5).
