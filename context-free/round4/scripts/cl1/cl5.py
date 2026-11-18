"""W_N = { w : n=|w| even, m=n/2, w_0 != w_m, w_j = w_{m+j} for 0<|j|<N (indices mod n) }  (linear CF).
Claim: T = {1y0y} subset W_N; non-primitive words of W_N are exactly odd powers v^q (q>=3 odd) with |v| even, |v| >= 2N.
Also: class-W closure: w in W_N  =>  w^q in W_N for every odd q (antipodal windows of w^q equal those of w)."""
import itertools
from refute import primitive
def inW(w, N):
    n = len(w)
    if n % 2 or n == 0: return False
    m = n // 2
    if w[0] == w[m]: return False
    return all(w[j % n] == w[(m + j) % n] for j in range(-N + 1, N) if j != 0)
def root(w):
    n = len(w)
    for d in range(1, n + 1):
        if n % d == 0 and w == w[:d] * (n // d): return d
for N in (1, 2, 3, 4):
    bad = []
    for n in range(2, 21, 2):
        for t in itertools.product('01', repeat=n):
            w = ''.join(t)
            if inW(w, N) and not primitive(w):
                d = root(w); q = n // d
                assert q % 2 == 1 and d % 2 == 0 and d >= 2 * N, (w, N)
                bad.append(d)
    print(f'N={N}: non-primitive words of W_N up to length 20: {len(bad)}, min root length {min(bad) if bad else None} (>= 2N={2*N})')
for y in itertools.product('01', repeat=8):
    y = ''.join(y); w = '1' + y + '0' + y
    assert inW(w, 4) and inW(w * 3, 4) and inW(w * 5, 4)
print('T subset W_4 and w^3, w^5 in W_4 for |y|=8 checked')
