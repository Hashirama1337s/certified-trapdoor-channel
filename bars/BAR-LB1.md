# BAR-LB1: a certified lower bound above 0.574 on the trapdoor feedforward capacity

Raid TRAPDOOR, step T3 (lower side). Written and sealed by the lead before the certified N = 14 run.

## Object
L_N(theta) = sum_i pi_i [H(Y^N | h0 = i) - H(Y^(N-1) | h0 = i)] - Pr(X != S) for the order-4 Markov input theta in lead/theta_k4.txt (16 exact rationals, two of them exactly 0 and 1), computed by lead/cert_lb.py: exact rational kernel and stationary law (pi P = pi checked exactly), exact Pr(X != S), and python-flint arb enclosures of every -p log2 p (p exact rational). Claimed consequence (ARGUED, DESIGN-TRAPDOOR.md L1 steps 1-3; referee item, not part of this bar's verdict): C >= L_N.

## Disclosed before sealing
- Float probe lead/lb_markov.py (independent code, optimiser): K = 2: 0.571121; K = 3: 0.572667; K = 4: 0.574129 (n = 14, unrounded theta), upper companion 0.574136.
- cert_lb.py runs already seen: K = 1 uniform, N = 8: 0.49996195529 ...; K = 1 theta = 0.2876, N = 10: 0.56725788329 ...; K = 4 (this theta file), N = 9: 0.57373698077 ... (lower endpoint).
- Published values of C: 0.572 (Kobayashi, extrapolated estimate), 0.57246 (neural estimate, arXiv 2301.00621); rigorous upper bound log2(3/2) = 0.5849625 (arXiv 1911.02113 Thm 7).

## Instruments (sha256)
- lead/cert_lb.py 06aa54048344d9d7181ee7cb6676385a72ebca2732d1908d00427142e8e472df
- lead/lb_markov.py 7f2abaebe10a964bd4b98113a21a58b42651e3629d568efb6bccfdafc4a26e1a
- lead/theta_k4.txt 45be35fffa4dfcfa0272e6d62518af6127d1564819e0cc799a580022fac30667
- Settings: N = 14 and N = 13, PREC = 128 bits.

## Predictions
- **P1 (target).** cert_lb.py theta_k4.txt 14 128: the certified lower endpoint is >= 0.5741 and the enclosure midpoint lies in [0.574120, 0.574135].
- **P2 (monotonicity, content).** The N = 13 enclosure lies wholly below the N = 14 enclosure's upper endpoint and its midpoint is <= the N = 14 midpoint (L_N is non-decreasing in N).
- **P3 (above the published estimates).** The P1 lower endpoint exceeds 0.57246 (the largest published estimate of C).
- **P4 (below the rigorous upper bound).** The P1 upper endpoint is below log2(3/2) = 0.58496.
- **N1 (null, content).** A perturbed input (every theta moved 1/10 of the way toward 1/2, file lead/theta_k4_null.txt written from theta_k4.txt by the lead before the run) gives a certified L_14 at least 0.0005 below the P1 midpoint.

## Verdict
HOLD if P1-P4 and N1 all pass; FAILED otherwise. Failures are kept and reported.

## Not claimed
The theory step C >= L_N (ARGUED, to be refereed before any claim reaches the owner as proved); optimality of theta; anything about the upper side.

## Seal fields
- formula_ref: lead/cert_lb.py:1-7, DESIGN-TRAPDOOR.md:225-236
- calibrated_on: none - no threshold tuned; P1 window set from the disclosed float probe
- depends_on: none - first bar of this raid
- null_not_symmetry: N1 changes the input law itself, not a relabelling
- target_form: certified interval endpoints and inequalities
- parameters: N = 14 fixed - the evaluation length of the disclosed probe; N = 13 used only for P2
- instruments: lead/cert_lb.py, lead/theta_k4.txt, lead/theta_k4_null.txt (sha256 96166711c5319e8fd3a4ca96484e797b06903810ee0766179bd00ac93c5940c4)
- tolerances: none - arb enclosures with rigorous radii; P1 window width 1.5e-5 around the float probe
- ceiling: a certified bound on C; the true C is unknown
- toy_model: K = 1 inputs (disclosed runs)
