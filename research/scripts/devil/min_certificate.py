"""
Exact minimum certificate size of primitive words.
A certificate of w (|w| = n) is a set S of positions s.t. for every prime p | n there are i,j in S with
i = j mod n/p and w_i != w_j  (C0 in the report).  Theorem C1: |S| >= omega(n)+1 always.
Mode 'all n'   : exhaustive over all primitive binary words of length n (omega(n) <= 2 fast path, numpy):
                 counts words whose minimum is omega+1 ("star": one centre j lying in a non-constant class
                 mod n/p for every p) versus larger.
Mode 'sample n N': exact minimum (search over one mismatch pair per prime) on N random primitive words
                 plus structured hard words (powers with 1..3 flipped letters, xor of periodic words).
Usage: python3 min_certificate.py all 12 18 ...   |   python3 min_certificate.py sample 30 3000
"""
import sys, random, itertools
import numpy as np
from sympy import primefactors

def run_all(n):
    ps = primefactors(n); N = 1 << n
    w = np.arange(N, dtype=np.int64)
    bits = np.array([((w >> i) & 1) for i in range(n)], dtype=np.int8)   # n x N
    prim = np.ones(N, dtype=bool)
    star = np.zeros(N, dtype=bool)
    good = []
    for p in ps:
        d = n // p
        cls_sum = np.zeros((d, N), dtype=np.int8)
        for i in range(n):
            cls_sum[i % d] += bits[i]
        nonconst = (cls_sum != 0) & (cls_sum != p)          # d x N
        prim &= nonconst.any(axis=0)
        good.append(nonconst)
    for j in range(n):
        ok = np.ones(N, dtype=bool)
        for p, g in zip(ps, good):
            ok &= g[j % (n // p)]
        star |= ok
    nostar = prim & ~star
    ex = [''.join('ab'[(int(x) >> i) & 1] for i in range(n)) for x in np.nonzero(nostar)[0][:2]]
    print(f"n={n} omega={len(ps)}: primitive={int(prim.sum())}, min certificate = omega+1 for {int((prim&star).sum())}, "
          f"larger for {int(nostar.sum())} {ex}")

def min_cert(w):
    n = len(w); ps = primefactors(n)
    lists = []
    for p in ps:
        d = n // p; L = []
        for i in range(n):
            for a in range(1, p):
                j = (i + a * d) % n
                if i < j and w[i] != w[j]:
                    L.append((1 << i) | (1 << j))
        if not L: return None
        lists.append(L)
    lists.sort(key=len)
    best = [n + 1]
    def rec(t, mask):
        c = mask.bit_count()
        if c >= best[0]: return
        if t == len(lists):
            best[0] = c; return
        for m in sorted(lists[t], key=lambda m: (mask | m).bit_count()):
            rec(t + 1, mask | m)
            if best[0] == len(ps) + 1: return
    rec(0, 0)
    return best[0]

def run_sample(n, N):
    rng = random.Random(3); ps = primefactors(n)
    words = []
    for _ in range(N):
        words.append([rng.randint(0, 1) for _ in range(n)])
    for _ in range(N):                       # near-powers
        p = rng.choice(ps); d = n // p
        u = [rng.randint(0, 1) for _ in range(d)]
        w = u * p
        for _ in range(rng.randint(1, 3)):
            w[rng.randrange(n)] ^= 1
        words.append(w)
    for _ in range(N):                       # xor of periodic words (one per prime)
        w = [0] * n
        for p in ps:
            d = n // p
            u = [rng.randint(0, 1) for _ in range(d)]
            for i in range(n): w[i] ^= u[i % d]
        words.append(w)
    hist = {}
    worst = None
    for w in words:
        c = min_cert(w)
        if c is None: continue
        hist[c] = hist.get(c, 0) + 1
        if worst is None or c > worst[0]: worst = (c, ''.join('ab'[b] for b in w))
    print(f"n={n} omega={len(ps)} lower bound omega+1={len(ps)+1}: histogram of exact min certificate size {dict(sorted(hist.items()))}; worst {worst}")

if sys.argv[1] == 'all':
    for a in sys.argv[2:]: run_all(int(a))
else:
    run_sample(int(sys.argv[2]), int(sys.argv[3]))
