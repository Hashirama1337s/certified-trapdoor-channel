# REFEREE-LB1: hostile referee on "C >= 0.574129234755855" (trapdoor feedforward capacity)

Referee seat, 2026-11-21. Did not see any target before reading BAR-LB1 (the bar prints its own window). Scripts and outputs: `referee/lb1/`. Sealed hashes re-checked: cert_lb.py 06aa5404..., theta_k4.txt 45be35ff..., theta_k4_null.txt 96166711..., lb_markov.py 7f2abaeb... all match BAR-LB1.

## In plain words

The number is right: my own program, built a different way (balls-in-a-box channel, integer arithmetic, a different entropy split, a different interval library), gets the same L_14 = 0.5741292347558552754... to all 20 printed digits, and the bar was scored exactly as sealed. The three theory steps hold. The hardest one (the sender cannot know the starting ball) is fine because of a standard theorem for channels that forget their start: the capacity is the same whichever start you condition on, so a start-dependent input law is allowed inside that formula. What is NOT proved is the plain-words sentence in RESULT-LB1 that "an explicit signalling strategy ... provably achieves" the rate: the rate is reached by codes whose existence the theorem gives, not by running this Markov source. Fix the wording, floor-round the printed endpoint, and write the step-3 chain out properly; nothing blocks the claim C >= 0.5741292 itself.

## Verdicts

| # | item | verdict |
|---|---|---|
| V1 | Certified value L_14 and scoring of P1-P4, N1 | CORRECT |
| V2 | Step 1: H(Y|X) rate = Pr(X_t != S_{t-1}) | CORRECT (state the hypothesis) |
| V3 | Step 2: H(Y) >= H(Y_N | Y^{N-1}, H_0) | CORRECT |
| V4 | Step 3: C >= information rate despite unknown S_0 | CORRECT WITH FIXES |
| V5 | Exact 0/1 entries of theta | CORRECT (no problem) |
| V6 | Certifier exactness and arb radius | CORRECT WITH FIXES |
| V7 | RESULT-LB1 plain-words wording | WRONG as written (overclaim), fix below |

**V1 CORRECT.** Referee code `referee/lb1/ref_exact.py` (output `ref_k4_N14.out`): L_14 in [0.5741292347558552754342582, same to 25 digits], width 8.466e-45; lead: [0.57412923475585527543 +/- 4.26e-21]. Same exact Pr(X != S) = 3244046875651976297624640858674028364559709988/8892982557611889742052917793975084699494580607. N = 13: 0.5741209010012018640068741 (lead 0.57412090100120186401). Null N = 14: 0.5726866489048377305338095 (lead 0.57268664890483773053). Scoring: P1 lower 0.574129234755855 >= 0.5741, midpoint in [0.574120, 0.574135]; P2 L_13 < L_14; P3 > 0.57246; P4 < 0.58496; N1 gap 0.0014426 >= 0.0005. All five as sealed, no moved goalposts. Disclosure item: P2 is not "content". H(Y_t | Y^{t-1}, H_0) is non-decreasing in t for any stationary hidden chain (H(Y_{t+1}|Y^t,H_0) >= H(Y_{t+1}|Y^t,H_0,H_1) = H(Y_t|Y^{t-1},H_0) by stationarity and the Markov property). So P2 can fail only through an instrument bug. It is an instrument check, and doctrine #23 asks for it to be labelled that way.

**V2 CORRECT.** Point (b), conditioning on future inputs: Y_t = f(X_t, S_{t-1}, N_t), and N_t is independent of (S_0, X_1^n, N^{t-1}) because the input source never sees the channel (no feedback; theta depends on past inputs only). Given (X^t, Y^{t-1}, S_0), S_{t-1} is fixed (unifilar). So H(Y_t | Y^{t-1}, X^n, S_0) = Pr(X_t != S_{t-1}), and the per-step value equals the stationary pxs. Also H(Y^n|X^n) - H(Y^n|X^n,S_0) = I(S_0;Y^n|X^n) is in [0, 1], so the two rates agree. The S_0 correlation with the input context is harmless. Empirical check (float, the decoder does not know s0, `mc_k4_pi_n4e6_s2.out`): -(1/n)log2 P(y^n|x^n) = 0.364916 +/- 0.000284 against the counted fraction 0.364915 and the exact value 0.364787275207. Fix: write the hypothesis "the input process is independent of the channel noise" into the step.

**V3 CORRECT.** Emission-on-transition hidden chain (H_{t-1}, Y_t, H_t). Given H_0, the past outputs are independent of the future ones, so H(Y_N|Y^{N-1},H_0) = H(Y_N|Y^{N-1},H_0,Y_{-k}^0) <= H(Y_N|Y_{-k}^{N-1}), which tends to H(Y). Conditioning on the full H_0 = (context, s), not on S_0, is done correctly in both codes. The certifier computes sum_i pi_i [H(Y^N|i) - H(Y^{N-1}|i)], which is exactly this quantity. (Cover-Thomas 4.5.1: TEXTBOOK, not opened by me; I checked the argument directly.)

**V4 CORRECT WITH FIXES.** Point (a). OPENED: 1911.02113 line 191-197, "Theorem 1 ([8], Ch. 4.6). The capacity of an indecomposable FSC is C = lim_n max_{P(x^n)} (1/n) I(X^n;Y^n|S0 = s0), for any s0". Def. 1 (line 168-175) and the remark at line 181-185 give the sufficient condition "for some n and each input sequence x^n there is a choice of state s_n ... such that P(s_n|x^n,s0) > 0 for all initial states s0". The trapdoor meets it with n = 1, s_1 = x_1 (stays with probability 1 if s0 = x1, else probability 1/2). Verified. The channel definition matches 1911.02113 Sec. V-A (line 479-486): "yt, is equal to st-1 or to xt with the same probability ... st = xt XOR yt XOR st-1".
The argument is sound when written as follows. Let a_n(s) = max_P (1/n) I(X^n;Y^n|S_0=s). For each fixed s, P(x^n | S_0 = s) from the stationary law is one admissible input law, and the joint law of Y^n given (x^n, s) is the channel kernel. So (1/n) I(X^n;Y^n|S_0) <= max_s a_n(s). Next, I(X^n;Y^n|S_0) >= I(X^n;Y^n) - H(S_0) >= I(X^n;Y^n) - 1. Both a_n(0) and a_n(1) tend to C, so C >= lim (1/n) I(X^n;Y^n) = H(Y) - pxs >= L_N. The encoder's ignorance of S_0 is handled by the theorem: Gallager's coding theorem for finite-state channels gives the lower capacity (lim max min over s0), which equals C under indecomposability. That operational part is NOT OPENED by me (Gallager Ch. 4.6 and 5.9 cited only through 1911.02113 ref [8]); label it TEXTBOOK.
Fixes: (i) DESIGN step 3 writes "C >= lim (1/n) I(X^n;Y^n|S0)" with S_0 averaged. Replace it with the max_s a_n(s) chain above. (ii) Say that achievability comes from Gallager's codes, not from transmitting this source.

**V5 CORRECT.** Point (c). theta(0101) = 1 and theta(1010) = 0 only forbid the patterns 01010 and 10101. ref_exact.py proves rank(P^T - I) = 31 = M - 1, so the stationary law is unique, and the support is 32 of 32 states. Zero-probability inputs are skipped before any log in both codes. The lead's elimination proves uniqueness only implicitly: a singular system would raise StopIteration in `next(...)`. Fix: add an explicit rank or uniqueness assert in cert_lb.py.

**V6 CORRECT WITH FIXES.** Point (d). theta is parsed exactly by Fraction. The kernel, pi, the exact check pi P = pi, and pxs are all exact rationals. Every p is an exact fmpq turned into an arb ball, log and log 2 are arb, and float() is used only for display. I found no float leak. Two findings:
(1) The printed "CERTIFIED LOWER ENDPOINT 0.574129234755855" is a round-to-nearest decimal of the endpoint, not a directed rounding. Here it happens to sit below: my exact comparison gives lower endpoint - 0.574129234755855 = 2.754e-16 > 0. Fix: print a floor-rounded decimal or an exact dyadic rational.
(2) The radii 4.26e-21 and 2.76e-16 are decimal-printing radii (str(20) and str(15)), not the enclosure's true width. My probe gives a per-term arb radius of about 1e-38 at 128 bits, and my independent mpmath-iv enclosure is 8.47e-45 wide. This is conservative and harmless.

**V7 WRONG as written.** RESULT-LB1 says "an explicit signalling strategy that remembers its last 4 balls provably achieves at least 0.5741292 bits per ball". The certified object is an input distribution whose stationary version correlates with S_0. The operational rate comes through Gallager's theorem. Exact fix: "The trapdoor channel's capacity without feedback is at least 0.5741292 bits per use. The witness is an order-4 Markov input law whose information rate is certified at or above that value; by the standard theorem for channels that forget their initial state, the unknown starting ball does not lower the capacity." Also: "above both published estimates" is fine, but the DINE estimate (0.57246) and Kobayashi's extrapolated "0.572 . . ." then lie below a proven achievable rate. Say that plainly, as a correction to estimates, not to theorems.

## Independent and extra checks (POST HOC beyond the sealed set)

- POST HOC N = 15: L_15 in [0.5741329179111730673836335, ...]. N = 16: L_16 in [0.5741345293125977291537239, ...]. Both are higher, with exact checks `lower endpoint >= 0.574129234755855: True`.
- POST HOC float upper companion (`upper_float_k4.out`): U_14 = 0.574136169, U_16 = 0.574135857. The true rate of this theta is in [0.5741345293 (certified), 0.574135857 (float)].
- POST HOC different start: H_0 uniform on the support gives 0.5741269500656048916268559 at N = 14. That is NOT a valid bound (not stationary) and is shown only to make clear that the pi weighting matters.
- Monte Carlo (float, physical ball simulation, Arnold-Loeliger forward filters; `mc_rate.py`). Stationary start, n = 4e6, seed 2: I-rate 0.573915 +/- 0.000185 (batch SE), which is 1.2 SE below the bracket. Fixed start (context 0000, ball 1, no burn-in, decoder filter uniform), n = 8e6, seed 3: 0.573959 +/- 0.000135. Stationary start, n = 1.2e7, seed 4: 0.574092 +/- 0.000109. Inverse-variance pooled: 0.574018 +/- 0.000077 (referee arithmetic), 1.5 pooled SE below the certified 0.5741345. Consistent, but the Monte Carlo cannot resolve below about 1e-4 and is a sanity check only. In every run the s0-unknown estimate of H(Y|X) equals the counted fraction of x != s to 1e-6, which checks step 1 empirically.
- Limit-case control (`theta_k4_allzero.txt`, N = 6): an all-zero input must give rate 0. Referee gives [-7.9e-48, 7.9e-48] with support 1 of 32; the lead gives exactly 0. Both pass.
- Prior art: a quick web search plus the PRIOR-ART file and the opened 2303.18008 / Kobayashi 2009 text found no rigorous trapdoor lower bound at or above 0.574. Kobayashi 2009 (OPENED, line 343) only says that the optimal input "seems not to be memoryless source or Markov source of any order". The method itself (Markov-input information rates over finite-state channels) is standard and not new. The novelty is the certified number.

## What blocks release

Nothing in the mathematics. Before release, fix V7 (wording), V6(1) (directed rounding of the printed endpoint), V4(i) (write the max_s a_n(s) chain into a proof note) and V5 (explicit uniqueness assert). Relabel P2 as an instrument check.

## Single next strike

Write a one-page proof note: steps 1-3 as lemmas with the hypotheses above, with Gallager's theorems labelled TEXTBOOK (ask the owner for Gallager Ch. 4.6 and 5.9 to upgrade to OPENED). Patch cert_lb.py to print a floor-rounded endpoint and assert uniqueness, then reseal.
