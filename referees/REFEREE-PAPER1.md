> Saved by the lead from the hand-back (seat 2026-11-22, 2026-11-22). The text below is the seat's report verbatim.

# REFEREE-PAPER1: release draft release/PAPER.md and PROOF-LB1-ADDENDUM-AUTOMATON.md

Scratch outputs: referee/paper1/ (recompute_ref_ub3_k15.out, arith.py, arith.out, arxiv_titles.out, seals.out).

## In plain words
Both certified numbers are real. Every digit of 0.57493196741521 and 0.574968285761 traces to a log. I re-ran the referee's own ceiling verifier and got the same value to 15 decimals. The maths of both proof chains holds, including the new automaton addendum. The draft does overclaim in four places, and each needs a fix before release:
- It calls "same number as the original program" proved, when the proof file says it is only observed.
- Its extrapolated range starts below its own proven floor.
- Its "2,300 times narrower than the best interval in print" ignores that [0.572, 0.585] is in print as a bound.
- It says both ends were checked by a second program, but the floor's independent check ran only at depth 11 and 12, not at the certified depth 24.

## Verdicts
1. Numbers trace to files: CORRECT WITH FIXES. Every number matches. Fixes: cite both k15 files (cert_col_k15_cont.json sha ceddd873..., no claim field; runs/push1/cert_col_k15_cont_claim.json sha 99a32f8d..., differ only by claimed_rho_upper). Section 6 "costs about 4 times more": no source (build-ub4/NOTES.md gives x5.8 per k ESTIMATE; measured k12->k13 267.8 s -> 700 s). Source it or drop it.
2. Claims supported by proofs: CORRECT WITH FIXES.
 (a) Addendum: CORRECT WITH FIXES. Lemma 1 holds because the coins B_t are independent of (H_0, the input's own randomness); under pi the input is correlated with S_0, say this. Uniqueness of pi not needed; "is unique (not required)". Status line "refereed by REFEREE-PAPER1". E depends only on N and pi is exact, so REFEREE-LB4 carries over.
 (b) Ceiling via the collapse: CORRECT.
 (c) "same number as the original program ... Proof: PROOF-COLLAPSE.md": WRONG as attributed. PROOF-COLLAPSE.md section 7 calls the equality a numerical observation used only as a self-test. Fix: numerically equal wherever compared (k <= 11, to 12 digits); not proved, not needed.
 (d) A1 and Gallager: CORRECT WITH FIXES. Trusted base also needs frexp exactness, correctly rounded Fraction->float conversion, python-flint fmpq/fmpq_mat.
 (e) "Does not claim first": CORRECT WITH FIXES. Add search limits: arXiv by abstract/title only; unopened Kobayashi-Morita-Hoshi 2003, Kobayashi 2006, Huleihel 2025 thesis.
 (f) Section 2: Pr(X!=S) is the per-step entropy given the input and the starting ball (difference at most 1 bit total).
3. Credit and citations: CORRECT WITH FIXES. All 7 arXiv ids resolve correctly (cs/0610047, 1911.02113, 2303.18008, 2301.00621, 2611.24700, 2609.19412, 2609.24908). The 0.572 row: only Kobayashi 2009 calls it an estimate; Chen-Sakai p.1 and 2303.18008 call it a lower bound; primary 2003 unopened, say so. 0.5765: use "simulations suggest". Add Papailiopoulos's certified bounded-potential dual. Labels: Khodaiemehr-Feng-Duman ABSTRACT, Birch 1962 UNVERIFIED, Cover-Thomas TEXTBOOK.
4. Scorecard: CORRECT WITH FIXES. Add PUSH1a VOID row; mark k=13 "verified, not sealed"; amendment has no own settle record (bookkeeping).
5. Plain words: CORRECT WITH FIXES. "best proven interval" (2339.38x) plus about 360x narrower than the quoted 0.572-0.585 (357). Floor's independent check at depths 11-12; depth 24 rests on the refereed error proof. "Published ... object" -> "released with this note". "We check every case exactly" -> "with every rounding pushed upward".
6. Recompute: CORRECT. ref_ub3_verify on cert_col_k15_cont.json: 12dp-up 0.574968285761, 15dp-up 0.574968285760847, argmax (0,'011001000001101',1); claim copy PASS; negctl FAIL. Width 3.631834579e-05 exactly. Floor float minus E 0.5749319674152149 >= printed.
7. Privacy and neutral authorship: CORRECT.
8. Section 6: WRONG. Lower end 0.574927 is below the proven floor; fix to "between the certified floor 0.5749320 and about 0.57496 (ESTIMATE)". "Shrinks the ceiling about 0.65-0.7 times" misreads the source: the improvement per order shrinks by ratios 0.68, 0.64, 0.73 (build-ub4/NOTES.md:209).

## Required fixes, ranked
1. Same-number wording. 2. Section 6. 3. Proven interval, 360x, 2003 unopened. 4. Floor independent check depths. 5. Both k15 hashes. 6. Scorecard PUSH1a, k13 unsealed. 7. Credit additions and labels, search limits. 8. Trusted base. 9. Addendum wording.

## What blocks release
Fixes 1-4. All text edits; no number changes.
