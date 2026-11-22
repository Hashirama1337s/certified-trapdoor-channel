"""Draws figures/gap_history.png from the four milestone values listed in PAPER.md.
Run from the package root: python code/figure/make_gap_history.py"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# (label, certified/published floor, ceiling); all values as printed in PAPER.md and bars/RESULT-*.md
M = [("published\n(0.5 / 0.5849625)", 0.5, 0.5849625),
     ("LB1 / UB1", 0.5741292, 0.5752327),
     ("LB4 / first k=15 ceiling", 0.5749274, 0.5749686),
     ("this release", 0.5749319, 0.5749683)]
x = list(range(len(M)))
lo = [m[1] for m in M]
hi = [m[2] for m in M]
gap = [h - l for l, h in zip(lo, hi)]

fig, (a, b) = plt.subplots(1, 2, figsize=(11, 4.4), facecolor="white")
a.plot(x, hi, "o-", color="#c0392b", label="certified ceiling")
a.plot(x, lo, "o-", color="#1f6fb2", label="certified floor")
a.set_xticks(x); a.set_xticklabels([m[0] for m in M], fontsize=8)
a.set_ylabel("bits per drop"); a.set_xlabel("milestone")
a.set_ylim(0.49, 0.595); a.grid(alpha=.3); a.legend(loc="center right")
b.semilogy(x, gap, "s-", color="#444444")
for i, g in enumerate(gap):
    b.annotate("%.3g" % g, (i, g), textcoords="offset points", xytext=(6, 6), fontsize=8)
b.set_xticks(x); b.set_xticklabels([m[0] for m in M], fontsize=8)
b.set_ylabel("gap = ceiling minus floor (bits per drop, log scale)"); b.set_xlabel("milestone")
b.grid(alpha=.3, which="both")
fig.tight_layout()
os.makedirs("figures", exist_ok=True)
fig.savefig("figures/gap_history.png", dpi=150, facecolor="white")
print("gaps", gap)
