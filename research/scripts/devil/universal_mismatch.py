"""
Candidate certificate C1 ("universal mismatch"): w (cyclic, length n) has a position i with
w_i != w_{i+n/p mod n} for EVERY prime p | n.  Sound (implies primitive).  Complete?
Counts primitive words of length n with no universal mismatch position.
Usage: python3 universal_mismatch.py n1 n2 ...
"""
import sys
import numpy as np
from sympy import primefactors

def run(n):
    N = 1 << n
    w = np.arange(N, dtype=np.int64)
    bits = [((w >> i) & 1).astype(np.int8) for i in range(n)]
    prim = np.ones(N, dtype=bool)
    ds = [n // p for p in primefactors(n)]
    for d in ds:
        per = np.ones(N, dtype=bool)
        for i in range(n):
            per &= bits[i] == bits[(i + d) % n]
        prim &= ~per
    has = np.zeros(N, dtype=bool)
    for i in range(n):
        ok = np.ones(N, dtype=bool)
        for d in ds:
            ok &= bits[i] != bits[(i + d) % n]
        has |= ok
    bad = prim & ~has
    ex = np.nonzero(bad)[0][:3]
    exs = [''.join('ab'[(int(x) >> i) & 1] for i in range(n)) for x in ex]
    print(f"n={n} primes={primefactors(n)}: primitive={prim.sum()}, without universal mismatch={bad.sum()}  e.g. {exs}")

for a in sys.argv[1:]:
    run(int(a))
