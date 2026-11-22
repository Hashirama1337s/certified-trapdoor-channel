# PROOF-COLLAPSE-FIXES: corrections to build-ub3/PROOF-COLLAPSE.md from REFEREE-UB3

Written by the lead. PROOF-COLLAPSE.md is hashed and stays unchanged; these lines supersede the named passages.

## In plain words
The referee found no gap in the mathematics. Three passages are worded wrongly or claim more than the proof gives. This file fixes them. No number changes.

## Fix A (Section 0, assumption A2, line 16: "s0 is fixed (knowing it can only help a code)")
Replace with: the message W is independent of the initial state S0, so I(W;Y^n) <= I(W;Y^n,S0) = I(W;Y^n|S0). The bound (*) holds for every s0 with the same constant K0. So the certified rho bounds C whether s0 is known, unknown, random or adversarial (an adversarial-s0 code works in particular for s0 = 0).

## Fix B (scope of the bound)
PROOF-COLLAPSE.md proves a bound on the feedforward capacity C only. Lemmas C1 and K use that the codeword x^n is fixed in advance (no feedback). Do not carry over PROOF-UB1's sentence "rho_cert also bounds the delay-d feedback capacity" to the collapsed certificates.

## Fix C (bookkeeping: the headline number is bound to the verifier)
The certificates cert_col_k12..k15 had no "claimed_rho_upper" field, so "RESULT: PASS" did not bind 0.574968594275. New file fixes/cert_col_k15_sm_claim.json = cert_col_k15_sm.json plus "claimed_rho_upper": "0.574968594275". Negative control fixes/negctl_k15_claim_low.json claims 0.574968594274 and must FAIL. Outputs: verify_k15_claim.out, verify_k15_negctl.out.

## Typo (Section 0, line 23)
"q_t = (last k symbols of q_{t-1} followed by y_t)" should read "last k-1 symbols of q_{t-1} followed by y_t".
