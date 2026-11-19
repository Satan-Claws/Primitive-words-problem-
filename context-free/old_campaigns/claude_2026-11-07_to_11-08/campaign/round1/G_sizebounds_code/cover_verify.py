r"""Exhaustive verification (binary alphabet) of the O(n) balanced-rectangle cover
of Q ∩ Σ^n.

Words: integers 0..2^n-1, bit i = letter at position i.
Window J_t = cyclic arc [t, t+lam). Window word read along the arc.

Rectangles:
  A_t      = { w : w|J_t has no (linear) period in D }            (D = proper divisors of n)
  B_{t,i,a}= { w : w|J_t has no period in E, w_i = a, w_{i+n/2} != a }   (n even, E = D\{n/2},
             i in J_t, i+n/2 not in J_t)
Claim: union of all rectangles == primitive words of length n, exactly.
"""
import numpy as np, sys
from math import gcd

def divisors(n):
    return [d for d in range(1, n) if n % d == 0]

def rot(words, t, n):
    # rotate so that position t becomes position 0 (cyclic)
    mask = (1 << n) - 1
    return ((words >> t) | (words << (n - t))) & mask if t else words

def has_period(x, L, d):
    # x: array of L-bit words (positions 0..L-1). linear period d (< L)?
    m = (1 << (L - d)) - 1
    return ((x ^ (x >> d)) & m) == 0

def primitive_mask(words, n):
    nonprim = np.zeros(len(words), dtype=bool)
    for p in [p for p in range(2, n + 1) if n % p == 0 and all(p % q for q in range(2, p))]:
        d = n // p
        r = rot(words, d, n)
        nonprim |= (r == words)
    return ~nonprim

def params(n, lam=None):
    D = divisors(n)
    E = [d for d in D if 2 * d != n]
    Es = sorted(E, reverse=True)
    M1 = Es[0] if Es else 0
    M2 = Es[1] if len(Es) > 1 else 0
    if lam is None:
        lam = (2 * n) // 3
    need = max(M1 + M2 - 1, M1)
    s = lam - need
    return D, E, M1, M2, lam, s

def verify(n, lam=None, verbose=True):
    D, E, M1, M2, lam, s = params(n, lam)
    if s < 1:
        return None
    T = list(range(0, n, s))   # gaps <= s (last gap n - T[-1] <= s)
    words = np.arange(1 << n, dtype=np.int64)
    prim = primitive_mask(words, n)
    covered = np.zeros(len(words), dtype=bool)
    nrect = 0
    wmask = (1 << lam) - 1
    for t in T:
        x = rot(words, t, n) & wmask           # window word
        perE = np.zeros(len(words), dtype=bool)
        for d in E:
            if d < lam:
                perE |= has_period(x, lam, d)
            else:
                perE |= True
        avoidE = ~perE
        if n % 2 == 1:
            covered |= avoidE; nrect += 1
        else:
            h = n // 2
            avoidD = avoidE & ~has_period(x, lam, h) if h < lam else np.zeros_like(avoidE)
            covered |= avoidD; nrect += 1
            for o in range(lam):
                i = (t + o) % n
                j = (i + h) % n
                oj = (j - t) % n
                if oj < lam:
                    continue  # partner inside window
                wi = (words >> i) & 1
                wj = (words >> j) & 1
                for a in (0, 1):
                    covered |= avoidE & (wi == a) & (wj != a)
                    nrect += 1
    sound = not np.any(covered & ~prim)
    complete = not np.any(prim & ~covered)
    if verbose:
        print(f"n={n:2d} D={D} M1={M1} M2={M2} lam={lam} s={s} windows={len(T)} "
              f"rects={nrect} sound={sound} complete={complete} |Q_n|={prim.sum()}")
    return sound, complete, nrect

if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    for n in range(2, N + 1):
        r = verify(n)
        if r is None:
            print(f"n={n:2d}: parameters fail (s<1) with lam=floor(2n/3)")
