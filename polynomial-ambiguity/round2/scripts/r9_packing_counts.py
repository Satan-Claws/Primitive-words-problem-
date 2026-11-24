"""r9_packing_counts.py -- exact counts: best searched unambiguous family (negative excursions b D a, Catalan)
vs G⁻ and the rotation threshold 2^n/n.  Also partial Bernoulli measures sum_n |L_n| 2^-n (Theorem M)."""
from math import comb
from fractions import Fraction
mE = mG = 0.0
for n in range(2, 2001, 2):
    E = comb(n - 2, (n - 2) // 2) // ((n - 2) // 2 + 1)   # Catalan C_{n/2-1}
    G = comb(n - 1, n // 2)
    mE += E / 2**n; mG += G / 2**n
    if n in (20, 60, 200, 2000):
        print(f"n={n}: |E|n/2^n={E*n/2**n:.4f}  |G-|n/2^n={G*n/2**n:.3f}  partial measures E={mE:.4f} G-={mG:.2f}")
