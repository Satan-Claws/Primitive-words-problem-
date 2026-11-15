"""Checks for Section 6 (analytic / counting angle).

(1) psi(n) = #primitive binary words of length n = sum_{d|n} mu(d) 2^{n/d}.
    Check psi(n) <= 2^n <= 2 psi(n) for 1 <= n <= NMAX (the report proves it for all n).
(2) Bivariate: psi(i,j) = #primitive words with i a's and j b's
               = sum_{g | gcd(i,j)} mu(g) C((i+j)/g, i/g).
    Check C(i+j,i) <= 2 psi(i,j) for all i,j >= 1 with i+j <= MMAX
    (the report proves it analytically for i+j >= 16).
(3) Evaluate the analytic bound f(m) = X^{-1/2} + (m/2) X^{-2/3}, X = m(m-1)/2, at m = 16..20
    (must be <= 1/2).
(4) Check psi(n) against brute force for n <= 16, and psi(i,j) for i+j <= 14.
"""
from math import comb, gcd
import itertools


def mobius(n):
    res, m, p = 1, n, 2
    while p * p <= m:
        if m % p == 0:
            m //= p
            if m % p == 0:
                return 0
            res = -res
        p += 1
    if m > 1:
        res = -res
    return res


def divisors(n):
    return [d for d in range(1, n + 1) if n % d == 0]


def psi(n):
    return sum(mobius(d) * 2 ** (n // d) for d in divisors(n))


def psi2(i, j):
    g = gcd(i, j)
    m = i + j
    return sum(mobius(d) * comb(m // d, i // d) for d in divisors(g))


def brute(n):
    from common import is_primitive_int
    cnt = 0
    by = {}
    for w in range(1 << n):
        if is_primitive_int(w, n):
            cnt += 1
            b = bin(w).count("1")
            by[b] = by.get(b, 0) + 1
    return cnt, by


if __name__ == "__main__":
    NMAX, MMAX = 3000, 400
    assert all(psi(n) <= 2 ** n <= 2 * psi(n) for n in range(1, NMAX + 1))
    print(f"(1) psi(n) <= 2^n <= 2 psi(n) holds for 1 <= n <= {NMAX}")
    worst = 0.0
    for m in range(2, MMAX + 1):
        for i in range(1, m):
            j = m - i
            c, q = comb(m, i), psi2(i, j)
            assert q <= c <= 2 * q, (i, j, c, q)
            worst = max(worst, (c - q) / c)
    print(f"(2) C(i+j,i) <= 2 psi(i,j) for all i,j>=1, i+j <= {MMAX}; max fraction of non-primitive = {worst:.4f}")
    for m in range(14, 21):
        X = m * (m - 1) / 2
        print(f"(3) m={m}: f = {X**-0.5 + (m/2) * X**(-2/3):.4f}  (need <= 0.5 for m >= 16)")
    for n in range(1, 17):
        cnt, by = brute(n)
        assert cnt == psi(n)
        for b, v in by.items():
            assert v == psi2(n - b, b), (n, b)
    print("(4) brute-force agreement for n <= 16 (both psi(n) and psi(i,j))")
