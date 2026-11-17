"""
W_n = span_R { periodic vectors with period n/p : p prime, p | n }  (sum of the subspaces V_{n/p}).
x not in W_n  <=>  some linear form L with L ⊥ W_n has L(x) != 0  =>  x primitive ("one-counter certificate").
Count binary primitive words of length n lying IN W_n (those need a non-linear certificate).
Usage: python3 binary_W.py n1 n2 ...
"""
import sys
import numpy as np
from sympy import primefactors

def run(n):
    cols = []
    for p in primefactors(n):
        d = n // p
        for r in range(d):
            v = np.zeros(n); v[r::d] = 1; cols.append(v)
    B = np.array(cols).T
    U, S, Vt = np.linalg.svd(B, full_matrices=True)
    rank = int((S > 1e-9).sum())
    Wperp = U[:, rank:]          # orthonormal basis of W^perp
    ds = [n // p for p in primefactors(n)]
    total_prim = 0; inW = 0; ex = []
    N = 1 << n; chunk = 1 << 18
    for start in range(0, N, chunk):
        w = np.arange(start, min(N, start + chunk), dtype=np.int64)
        X = ((w[:, None] >> np.arange(n)) & 1).astype(np.float64)
        prim = np.ones(len(w), dtype=bool)
        for d in ds:
            prim &= ~np.all(X == np.roll(X, -d, axis=1), axis=1)
        proj = np.abs(X @ Wperp).max(axis=1) if Wperp.shape[1] else np.zeros(len(w))
        hit = prim & (proj < 1e-7)
        total_prim += prim.sum(); inW += hit.sum()
        for idx in np.nonzero(hit)[0][:max(0, 3 - len(ex))]:
            ex.append(''.join('ab'[int(b)] for b in X[idx]))
    print(f"n={n} primes={primefactors(n)} dimW={rank}: primitive={total_prim}, primitive in W={inW} e.g. {ex}")

for a in sys.argv[1:]:
    run(int(a))
