# Blackwell's trapdoor channel: certified capacity bounds 0.5749319 ≤ C ≤ 0.5749683

Moki & Julio (AI-assisted)

**Version 1.0.**

## In plain words

A box holds one ball, black or white. You drop a ball in, and one of the two balls inside falls out at random. Someone watching the balls fall out tries to read your message. How many bits per drop can you get across, at best? David Blackwell posed this question in 1961, and it is still unsolved. The best proven answer we could find in print is "somewhere between 0.5 and 0.585". This note pins the answer down to

**0.5749319 ≤ C ≤ 0.5749683 bits per drop.**

The gap is 0.0000363. That is about 2,300 times narrower than the best *proven* interval we could find in print (0.5 to 0.585), and about 360 times narrower than the commonly quoted 0.572 to 0.585 (whose lower end we could not trace to a proof; see the table). Both ends are certified by a computer. The ceiling was re-checked by a second program written from the definitions alone; the floor was re-checked that way at depths 11 and 12, and its full-depth value rests on a refereed rounding-error proof. Each end comes with a proof that a specific, exactly written-down object, released with this note, really gives that bound.

How it works, in one sentence each:
- **The floor is a recipe.** We write down an explicit way to choose the next ball, a rule that looks back at how long the last three runs of same-coloured balls were. Then we compute, with every rounding error bounded, how much information that recipe gets through. Any recipe gives a valid floor; the work was finding a good one and certifying it.
- **The ceiling is a guess about the output.** We write down a model of what the falling balls look like, a table of predictions based on the last 15 balls out. A theorem from 2019 and 2023 work says that if no possible input can surprise this model by more than r bits per drop, then the capacity is at most r. We check every case, with every rounding pushed upward.

## Start here

| | value | what it is | how it was checked |
|---|---|---|---|
| Floor | **C ≥ 0.57493196741521** | a run-length input recipe (1,920 hidden states), certified at depth 24 | rounding-error proof + two chunkings agree + a blind exact evaluator agrees to about 3e-17 at depth 11 and 12 |
| Ceiling | **C ≤ 0.574968285761** | an order-15 output model, dual bound | exact verifier + a second verifier written by a referee from the definitions |
| Width | **3.632e-5** | | |
| Published, rigorous | 0.5 < C ≤ log2(3/2) = 0.5849625 | Kobayashi-Morita 2002 (as reported by Permuter et al. 2008); Huleihel et al. 2019, Theorem 7 | |
| Published, other values | 0.572 (Kobayashi et al. 2003); ≈ 0.57246 (arXiv 2301.00621, a neural estimate); C ≤ 0.5765 (arXiv 2303.18008) | 0.572 is quoted as a lower bound by later papers (arXiv 2303.18008, 2611.24700), but its author's own later account (Kobayashi 2009) describes it as an estimate from extrapolated block increments; the 2003 primary source could not be opened. For 0.5765 the authors write that "simulations suggest" it. | |

Both 0.572 and 0.57246 lie below our proven floor. If 0.572 was a proven lower bound, our floor improves it; if it was an estimate of C, the estimate was low. Either way no theorem is contradicted.

## Scorecard (pre-registered tests)

The headline computations were predicted in a sealed file (hashed before the run) and scored afterwards without moving the bar. Failures are kept. The order-13 ceiling row in section 3 was verified but not sealed.

| test | what it checked | verdict |
|---|---|---|
| LB1 | order-4 floor 0.5741292, two exact evaluators | HOLD |
| LB2 | order-7 floor, independent exact re-evaluation | HOLD |
| LB3 | order-9 floor with the fast kernel | **FAILED** (our tolerance forgot a 14-digit print truncation) |
| LB4 | order-9 floor 0.57492740773047 with a proven log routine | HOLD |
| UB1 | ceiling 0.5752327, blind re-implementation of the verifier | HOLD |
| UB2 | ceiling certificates at sizes 8 and 10 | HOLD |
| UB3 | the shortcut ("collapse") cross-checked against the original chain, sizes 10 and 11 | HOLD |
| PUSH1 | this note's floor and ceiling | **FAILED** (one control could not fire: it perturbed a state the recipe never visits). Every value check passed. |
| PUSH1a | a first replacement control | **VOID** (it ran before its seal went through; kept only as an unsealed observation) |
| PUSH1b | a replacement live control, sealed before its run | HOLD |

## 1. The channel

State s ∈ {0,1} (the ball in the box). Input x. If x = s, the output is y = s and the state stays. If x ≠ s, the output is 0 or 1 with probability 1/2 each, and the ball not output stays: s' = x ⊕ y ⊕ s. The capacity C is the feedforward (no feedback) capacity. The channel is indecomposable, so C does not depend on the starting ball (Gallager, Ch. 4.6; TEXTBOOK, not opened by us).

A fact used throughout ("coin form"): take fair coins B_t, independent of everything. If B_t = 1, output the old ball and keep the new one; if B_t = 0, output the new ball. This reproduces the channel exactly. The same construction appears for the grabbag channel (of which the trapdoor is the case M = 1) in Chen and Sakai, arXiv 2611.24700, Lemma 4.

## 2. The floor

**Bound.** For any stationary input produced by a finite hidden state q (independent of the channel's coins), with H_0 = (q_0, s_0),

C ≥ L_N = H(Y_N | Y_1..Y_{N-1}, H_0) − Pr(X ≠ S), for every N.

The first term is Birch's lower bound on the output entropy rate. The second is the exact per-step entropy of the output given the input and the starting ball, available in closed form because the state is a function of past inputs and outputs; not knowing the starting ball changes the total by at most 1 bit, which vanishes per use. The proof is three short lemmas (proofs/PROOF-LB1.md, extended to automaton inputs in proofs/PROOF-LB1-ADDENDUM-AUTOMATON.md).

**The input.** A run-length automaton: the probability that the current run continues depends on its age (capped at 10), the previous run's length (capped at 8) and the run before that (capped at 6). The 480 probabilities are rationals with denominator 100,000, in data/floor/fL6_10_8_6.txt (sha256 833a0726…d3ed94). They were found by gradient ascent on L_N itself, with an exact reverse-mode gradient. An earlier attempt that optimised a smoother stand-in quantity produced recipes that certified *worse*.

**Certification.** The kernel computes all 2^24 output words at once for every start state by a backward recursion, in double precision, with a written bound on every rounding. Logarithms use our own routine (frexp plus an atanh series, 10 terms) whose relative error is proven to be at most 3.8671e-15, using only correctly rounded +, −, ×, ÷. The final error bound at depth 24 is 7.227e-13 and is subtracted before the result is rounded down. The kernel's error lemma was refereed (referees/REFEREE-LB4.md).

| input | hidden states | depth N | certified floor |
|---|---|---|---|
| order 4 Markov | 32 | 14 | 0.574129234755855 |
| order 7 Markov | 256 | 15 | 0.574804833039610 |
| order 9 Markov | 1,024 | 24 | 0.57492740773047 |
| run-length (10,8,6) | 1,920 | 24 | **0.57493196741521** |

**Independent check.** A referee, not shown our code or our values, wrote an exact evaluator (integer arithmetic plus 320-bit ball logarithms) from a word description of the channel and the automaton. At depth 11 and 12 it agrees with our kernel to about 3e-17, and our certified endpoints lie below its values. Perturbing one live transition probability by 1/100,000 moves its value by 9.6e-11, so the comparison can fail.

## 3. The ceiling

**Bound (the duality method).** For any output model T, the capacity is at most the long-run maximum, over all inputs, of the relative entropy between the true output law and T. This method and its evaluation as an average-reward dynamic program are from Huleihel, Sabag, Permuter, Kashyap and Shamai (arXiv 1911.02113), and its delayed-feedback extension from Huleihel, Sabag, Permuter and Kostina (arXiv 2303.18008).

**The shortcut.** With an order-k output model, the coin form shows that the expected reward at time t depends only on the ball k+1 steps back and the last k+1 inputs. So the dynamic program has 2^(k+1) states instead of 2^(2k+1). This is the 1911.02113 special case (Sec. IV-B, for channels whose state depends only on the input) carried over to the trapdoor through the coin form. The shortcut is a self-contained bound. Wherever we compared it with the original program (k ≤ 11), the two gave the same number to 12 digits for the same model; that equality is observed, not proved, and nothing depends on it. Proof of the bound: proofs/PROOF-COLLAPSE.md with corrections in proofs/PROOF-COLLAPSE-FIXES.md; refereed (referees/REFEREE-UB3.md: no gap in the mathematics).

**Certification.** The model T and a value function h are stored as exact dyadic rationals. The verifier encloses every logarithm with 192-bit ball arithmetic, rounds upward, and takes the maximum of the Bellman residual over all 2^(k+2) state-action pairs in exact integers. The certificate states its own claim, and the verifier fails if its value exceeds it.

| model order k | certified ceiling | note |
|---|---|---|
| 1 | log2(3/2) = 0.5849625 | the published Theorem 7, reproduced |
| 7 | 0.575232734723 | shipped collapsed-form certificate; the original-chain verifier gave the same bound one unit higher in the last digit (0.575232734724), blind-verified |
| 11 | 0.575008505468 | original chain and verifier, no shortcut needed |
| 13 | 0.574977689197 | exact convex solve, rounded; verified, not sealed |
| 15 | **0.574968285761** | data/ceiling/cert_col_k15_cont.json (sha256 ceddd873…448372); the same certificate with its claim field, data/ceiling/cert_col_k15_cont_claim.json (sha256 99a32f8d…eb556), is the file the verifier passes against the stated bound |

**Independent check.** A referee's own verifier (300-bit interval logs, a different bit order, the channel coded from its definition, exact residuals) reproduces the order-15 value to 15 decimals. A copy of the certificate claiming one unit less in the last digit fails. A path-by-path brute force of the bound at small sizes holds with slack 1e-13 to 4e-9, and fails when the bound is lowered by 1e-4.

## 4. What this rests on

- **A1:** the computer's +, −, ×, ÷ on double-precision numbers round correctly (IEEE 754). Tested directly on this build (0 mismatches in 40,004 samples per operation), not proven.
- **Gallager's theorem** for indecomposable finite-state channels (Ch. 4.6 and 5.9): cited, not opened by us.
- **Ball-arithmetic logarithms** (arb, mpmath) are trusted.
- Python's exact integers and fractions, python-flint's exact rationals and rational matrices (used to solve for the stationary law), exact frexp, and correctly rounded conversion of fractions to floats are trusted.

## 5. What this does not claim

- That either recipe is optimal, or anything about where C lies inside the interval.
- A closed form for C.
- Any feedback capacity. The shortcut proof uses that the codeword is fixed in advance.
- That we are the first to tighten these bounds. We searched arXiv (abstracts and titles), Zenodo, OpenAlex and Semantic Scholar to 2026-11-22 and found no proven upper bound below 0.5849625 and no traceable proof of a lower bound above 0.5. Three sources could not be opened: Kobayashi, Morita and Hoshi (2003), Kobayashi (2006), and a 2025 doctoral thesis by Huleihel.

## 6. Where the gap could go (estimates, not claims)

Each order added to the ceiling model improves it by less than the order before: the improvements shrink by ratios of about 0.64 to 0.73, while the work grows by a factor of roughly 2.6 to 6 per order (measured 268 s to 700 s from order 12 to 13 with our exact solver). Output models that also remember run lengths did *not* help: at equal size the plain order-k model is better by 1e-4 to 4e-4 (references/NOTES-UB4.md). Larger run-length inputs add under 1e-6 each at double the cost. Extrapolating the ceiling sequence puts the limit of this family between the certified floor 0.5749319 and about 0.57496 (ESTIMATE). A large further factor needs a new idea, not more compute.

## Credit

- Problem: D. Blackwell (1961). Earlier bounds and estimates: Kobayashi and Morita (2002), Kobayashi, Morita and Hoshi (2003), Kobayashi (2006, 2009), Permuter, Cuff, Van Roy and Weissman (arXiv cs/0610047), the neural estimate of arXiv 2301.00621.
- Duality / Q-graph upper bounds and the order-k special case: Huleihel, Sabag, Permuter, Kashyap, Shamai (arXiv 1911.02113). Delayed feedback: Huleihel, Sabag, Permuter, Kostina (arXiv 2303.18008); Yang, Kavčić, Tatikonda (ISIT 2003, title only).
- Coin representation: Chen and Sakai (arXiv 2611.24700); permuting-channel picture, Permuter et al. (cs/0610047, Fig. 3).
- Certified Birch bounds for finite-state inputs, and a certified bounded-potential dual upper bound: Papailiopoulos (arXiv 2609.19412, deletion channel). Run-length hidden states for certified bounds: Khodaiemehr, Feng, Duman (arXiv 2609.24908, deletion channel; abstract read).
- Birch bound: J. J. Birch (1962; cited, not opened); Cover and Thomas, Lemma 4.5.1 (textbook, not opened).

Ours: the certified values, the run-length floor recipe, the proven log kernel, the extension of the order-k shortcut to the trapdoor, and the independent checks.

## Files and reproduction

Floor: `py -3.11 code/floor/cert_backward2.py data/floor/fL6_10_8_6.txt 24 --nb 15` (about 25 minutes, 6.4 GB). Ceiling: `py -3.11 code/ceiling/verify_collapsed.py data/ceiling/cert_col_k15_cont_claim.json` (under a second). Sealed tests: bars/BAR-*.md, bars/AMENDMENT-PUSH1b.md; referee reports: referees/REFEREE-*.md; transcripts of the headline floor and ceiling, their controls and the milestone ceilings: transcripts/ (the order-4 and order-7 floor values, the IEEE test and the solver timings are recorded in bars/RESULT-*.md and referees/); the step-by-step commands: code/README.md.

This note and its code were prepared with AI assistance.
