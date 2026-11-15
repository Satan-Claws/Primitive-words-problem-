# Near-constant family test, matchings only.
import itertools, sys
from fractions import Fraction
import numpy as np

def nc_matchings(lo, hi):
    # non-crossing perfect matchings of range(lo,hi)
    if lo >= hi:
        yield []
        return
    for j in range(lo+1, hi, 2):
        for left in nc_matchings(lo+1, j):
            for right in nc_matchings(j+1, hi):
                yield [(lo, j)] + left + right

def max_divs(n):
    ps = [p for p in range(2, n+1) if n % p == 0 and all(p % q for q in range(2, p))]
    return [n//p for p in ps]

def is_periodic(x, d):
    n = len(x)
    return all(x[i] == x[(i+d) % n] for i in range(n))

def primitive(x):
    return not any(is_periodic(x, d) for d in max_divs(len(x)))

def rank(M):
    return np.linalg.matrix_rank(np.array(M, dtype=float)) if len(M) else 0

def caught(M, delta, d):
    # b in rowspace(A_d)?
    m = len(M)
    A = [[0]*m for _ in range(d)]
    b = []
    for c, (i, j) in enumerate(M):
        A[i % d][c] += 1
        A[j % d][c] -= 1
        b.append(delta[i] - delta[j])
    return rank(A + [b]) == rank(A)

if __name__ == '__main__':
    n = int(sys.argv[1]); B = int(sys.argv[2])
    Ms = list(nc_matchings(0, n))
    ds = max_divs(n)
    print('n', n, 'matchings', len(Ms), 'ds', ds)
    hard = []
    for delta in itertools.product(range(B), repeat=n):
        if delta[0] != 0: continue  # normalize min? shift invariance: fix delta[0]=0 ok (b invariant under constant shift)
        if not primitive(delta): continue
        if all(any(caught(M, delta, d) for d in ds) for M in Ms):
            hard.append(delta)
    print('hard count', len(hard))
    print(hard[:20])
