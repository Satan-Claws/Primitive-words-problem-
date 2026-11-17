"""Shared helpers for the 'rectangles' agent.

Words of length n over {a,b} are encoded as integers in [0, 2^n): bit j (value 1<<j)
is the letter at position j, with a = 0 and b = 1.
"""
import numpy as np


def prime_factors(n):
    ps, m, p = [], n, 2
    while p * p <= m:
        if m % p == 0:
            ps.append(p)
            while m % p == 0:
                m //= p
        p += 1
    if m > 1:
        ps.append(m)
    return ps


def rot(w, d, n):
    """Cyclic rotation of the n-bit word(s) w by d positions (works on numpy arrays)."""
    mask = (1 << n) - 1
    return ((w >> d) | (w << (n - d))) & mask


def primitive_mask(n):
    """Boolean array P of length 2^n with P[w] = (w is primitive). Exhaustive."""
    w = np.arange(1 << n, dtype=np.uint64)
    nonprim = np.zeros(1 << n, dtype=bool)
    for p in prime_factors(n):
        d = n // p
        nonprim |= (rot(w, np.uint64(d), n) == w)
    return ~nonprim


def is_primitive_int(w, n):
    mask = (1 << n) - 1
    for p in prime_factors(n):
        d = n // p
        if (((w >> d) | (w << (n - d))) & mask) == w:
            return False
    return True


def class_matrix_tests(n, rng):
    """Draw one random test tuple (s_p)_{p | n}, s_p uniform in S_p.

    S_p = { s in GF(2)^n : every residue class mod d_p = n/p has even weight }.
    Sampled as s_p = r + rot(r, d_p) with r uniform (the map r -> (1+sigma^{d}) r is
    linear and onto S_p, so the image of the uniform distribution is uniform on S_p).
    Returns list of python ints.
    """
    out = []
    for p in prime_factors(n):
        d = n // p
        r = int(rng.integers(0, 1 << n, dtype=np.uint64)) if n < 64 else int.from_bytes(rng.bytes((n + 7) // 8), 'little') & ((1 << n) - 1)
        s = r ^ rot(r, d, n)
        out.append(s)
    return out


def in_S_p(s, n, p):
    d = n // p
    for r in range(d):
        par = 0
        for j in range(p):
            par ^= (s >> (r + j * d)) & 1
        if par:
            return False
    return True


def parity_popcount(arr):
    return (np.bitwise_count(arr) & 1).astype(bool)
