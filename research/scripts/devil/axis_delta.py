"""Variant: exact / quantized mirror differences delta^s_i = x_{s-i}-x_i, clipped to [-T,T].
Usage: python3 axis_delta.py n K T  (T=0 means exact)"""
import sys, itertools
from sympy import primefactors
from axis_sign import periodic, primitive
def dl(x, s, T):
    n = len(x); out = []
    for i in range(n):
        v = x[(s-i) % n] - x[i]
        if T: v = max(-T, min(T, v))
        out.append(v)
    return tuple(out)
n, K, T = map(int, sys.argv[1:4])
ds = [n//p for p in primefactors(n)]
bad = 0; cnt = 0
for x in itertools.product(range(K+1), repeat=n):
    if not primitive(x): continue
    cnt += 1
    if not any(not any(periodic(dl(x, s, T), d) for d in ds) for s in range(n)):
        bad += 1
        if bad <= 8: print("UNCERT", x)
print(f"n={n} K={K} T={T}: tested={cnt} uncertified={bad}")
