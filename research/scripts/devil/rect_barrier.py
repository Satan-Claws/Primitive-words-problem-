"""
Checks for the rectangle / fooling-set / interchange barriers.

Split of a length-n word: inner = positions [k, k+m), outer = the rest.
Bad(o) = { inner words x : o∘x is NOT primitive }.
Theorem (report): m <= n/2  =>  |Bad(o)| <= omega(n)  (number of distinct primes of n).
                  n even, m = n/2+1 => |Bad(o)| <= omega(n)+1.
Also: exact maximum fooling set for small n (fooling: pairwise, some cross pair is non-primitive),
and a greedy rectangle cover using colour classes 'inner restricted to a set of positions'.
Usage: python3 rect_barrier.py NMAX
"""
import sys, itertools
from sympy import primefactors

def is_prim(w):
    n = len(w)
    if n == 0: return False
    for p in primefactors(n):
        d = n // p
        if w == w[:d] * p: return False
    return True

def maxbad(n, k, m):
    best = 0
    outer_len = n - m
    for o in range(1 << outer_len):
        ob = format(o, f'0{outer_len}b') if outer_len else ''
        pre, suf = ob[:k], ob[k:]
        cnt = 0
        for x in range(1 << m):
            xb = format(x, f'0{m}b')
            if not is_prim(pre + xb + suf):
                cnt += 1
        best = max(best, cnt)
    return best

def main():
    NMAX = int(sys.argv[1])
    for n in range(2, NMAX + 1):
        om = len(primefactors(n))
        res = []
        for m in sorted(set([max(1, n // 3), n // 2, (n // 2 + 1) if n % 2 == 0 else n // 2])):
            if m < 1 or m > n: continue
            for k in sorted(set([0, (n - m) // 2, n - m])):
                b = maxbad(n, k, m)
                bound = om if 2 * m <= n else om + 1
                res.append((k, m, b, bound))
                assert b <= bound, (n, k, m, b, bound)
        print(f"n={n} omega={om} (k,m,maxBad,bound): {res}")

if __name__ == '__main__':
    main()
