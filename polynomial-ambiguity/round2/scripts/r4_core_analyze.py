"""r4_core_analyze.py -- characterise uncovered words U (file of 'n word' lines, canonical reps).
Per word: n, #a, #b, g = gcd(#a,#b), Off (xhat(1) != 0, exact Moebius-cube test), zero set of xhat(j) (j=1..n-1, numeric),
run-length sequences, h_K = gcd of cyclic occurrence counts of all factors of length <= K."""
import sys, math, itertools
import numpy as np
from sympy import primefactors
def occ(w, L):
    n = len(w); ww = w * (L // n + 2)
    d = {}
    for i in range(n):
        f = ww[i:i+L]; d[f] = d.get(f, 0) + 1
    return d
def hK(w, K):
    g = 0
    for L in range(1, K+1):
        for v in occ(w, L).values(): g = math.gcd(g, v)
    return g
def off(w):
    n = len(w); x = np.array([c == 'b' for c in w], dtype=np.int64)
    for p in primefactors(n):
        x = x - np.roll(x, n // p)
    return bool(np.any(x))
def zeros(w):
    n = len(w); x = np.array([c == 'b' for c in w], float)
    F = np.fft.fft(x)
    return [j for j in range(1, n) if abs(F[j]) < 1e-9]
def runs(w):
    n = len(w); s = next(i for i in range(n) if w[i] == 'a' and w[i-1] == 'b')
    r = w[s:] + w[:s]
    import re
    return [(len(m.group(1)), len(m.group(2))) for m in re.finditer(r'(a+)(b+)', r)]
if __name__ == '__main__':
    K = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    for line in open(sys.argv[1]):
        n, w = line.split(); n = int(n)
        na, nb = w.count('a'), w.count('b')
        rl = runs(w)
        print(n, w, f'#b={nb} g={math.gcd(na,nb)} Off={int(off(w))} hK={hK(w,K)} r={len(rl)}',
              'alpha=' + ','.join(str(a) for a, b in rl), 'beta=' + ','.join(str(b) for a, b in rl),
              'zeros=' + ','.join(map(str, zeros(w))))
