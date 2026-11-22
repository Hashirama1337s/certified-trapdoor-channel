# ERROR-LEMMA2 fix (lead annotation from REFEREE-LB4, 2026-11-22)

Section 2c, bullet "w inside P": the sentence "P(w0 f) <= max(f,1) P(w0) (monomials scale by f^k)" is false in general (P = 1 + w^2, w0 = 1, f = 2). It is replaced by:

|P(w0 f) - P(w0)| <= sum_{k>=1} c_k w0^k ((1+a)^k - 1) <= ((1+a)^(K-1) - 1)(P(w0) - 1), and (P(w0) - 1)/P(w0) <= (WMAX/3)/(1 - WMAX) = 0.010132.

So the relative cost is <= 0.0912 a < a with a = (1+u)^7 - 1. The exponent 7 and LAMBDA = 3.8671e-15 are unchanged (referee recomputed, bit-equal).
