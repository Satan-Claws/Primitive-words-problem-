"""Audit r13: Lemma F (F_K subset Q, K_n=[ceil(n/3),floor(n/2)]) and Lemma M (exact criterion, ALL K subsets of [1,n/2])
for n <= NF (exhaustive over all non-primitive words = all u^p, p prime), plus Lemma A on ALL words n <= NA (numpy).
Also G- subset Q and the g=1 => unique argmax claim. Usage: audit_r13_fold.py [NF=24] [NA=20]"""
import sys
import numpy as np
from math import gcd
NF = int(sys.argv[1]) if len(sys.argv) > 1 else 24
NA = int(sys.argv[2]) if len(sys.argv) > 2 else 20
def primes(n): return [p for p in range(2, n + 1) if n % p == 0 and all(p % q for q in range(2, p))]
def dvec(w):  # w: tuple of 0/1 (1 = a); d_k for k = 1..n//2
    n = len(w); return [sum(w[:k]) - sum(w[n - k:]) for k in range(1, n // 2 + 1)]
fail = 0
for n in range(1, NF + 1):
    h = n // 2; Kn = set(range(-(-n // 3), h + 1))
    masks = set()
    for p in primes(n):
        m = n // p
        for x in range(2 ** m):
            u = tuple((x >> i) & 1 for i in range(m)); w = u * p
            z = frozenset(k for k, d in enumerate(dvec(w), 1) if d == 0)
            masks.add(z)
            if not (z & Kn): fail += 1; print('LemmaF FAIL', n, w)
    # Lemma M over all K subset [1,h]
    for Kb in range(2 ** h):
        K = {k for k in range(1, h + 1) if Kb >> (k - 1) & 1}
        sound = all(z & K for z in masks)
        crit = all(any(k % (n // p) == 0 for k in K) for p in primes(n))
        if sound != crit: fail += 1; print('LemmaM FAIL', n, sorted(K)); break
print('F/M: n<=%d failures=%d' % (NF, fail))
# Lemma A, exhaustive
failA = failG = failg = 0; ties = 0
for n in range(1, NA + 1):
    W = ((np.arange(2 ** n)[:, None] >> np.arange(n)[None, :]) & 1).astype(np.int32)
    A = W.sum(1)
    P = np.concatenate([np.zeros((2 ** n, 1), np.int32), np.cumsum(W, 1)], 1)[:, :n]  # #a(w[0,i)), i=0..n-1
    T = n * P - np.arange(n)[None, :] * A[:, None]
    mx = T.max(1); nmax = (T == mx[:, None]).sum(1); r = T.argmax(1)
    uniq = nmax == 1; ties += (~uniq).sum()
    idx = (r[:, None] + np.arange(n)[None, :]) % n
    V = np.take_along_axis(W, idx, 1)
    h = n // 2
    if h:
        C = np.cumsum(V, 1); Cr = np.cumsum(V[:, ::-1], 1)
        D = C[:, :h] - Cr[:, :h]  # d_k, k=1..h
        inG = (D < 0).all(1)
        failA += int((uniq & ~inG).sum())
        # also weak form: d_k <= 0 at ANY argmax rotation (checked at first argmax)
        failA += int((D > 0).any(1).sum())
    else:
        inG = np.ones(2 ** n, bool)
    # G- subset Q: check every word v in G- is primitive
    Gw = ((np.arange(2 ** n)[:, None] >> np.arange(n)[None, :]) & 1)
    if h:
        Cg = np.cumsum(Gw, 1); Cgr = np.cumsum(Gw[:, ::-1], 1)
        inGm = ((Cg[:, :h] - Cgr[:, :h]) < 0).all(1)
    else:
        inGm = np.ones(2 ** n, bool)
    nonprim = np.zeros(2 ** n, bool)
    for p in primes(n):
        m = n // p; nonprim |= (Gw == np.roll(Gw, m, 1)).all(1)
    failG += int((inGm & nonprim).sum())
    g1 = np.array([gcd(int(a), n) == 1 for a in A])
    failg += int((g1 & ~uniq).sum())
print('LemmaA: n<=%d failures=%d; G- nonprimitive members=%d; g=1 but tie=%d; total tie words=%d' % (NA, failA, failG, failg, ties))
