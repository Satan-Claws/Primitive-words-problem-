"""r10_heavy_checks.py -- checks for r10_heavy.md.
(1) chord form d_k = P(k)+P(n-k)-P(n) (exhaustive n<=14);
(2) Sec.4 pair model P={(E,eps)} u {(b,E^k a)}: two-tape injectivity, outer-walk negativity, and whole-word
    injectivity / G- inclusion for every centre w of length <=3 and p,q in small set (N<=16);
(3) |Safe_n| * n / 2^n (two one-sided meanders)."""
import itertools
from math import comb
from collections import Counter
def P(w, j): return sum(c == 'a' for c in w[:j]) - j / 2
def inG(w):
    n = len(w); d = 0
    for k in range(n // 2):
        d += (w[k] == 'a') - (w[n - 1 - k] == 'a')
        if d >= 0: return False
    return True
bad = 0
for n in range(1, 15):
    for t in itertools.product('ab', repeat=n):
        w = ''.join(t)
        for k in range(1, n // 2 + 1):
            dk = sum(c == 'a' for c in w[:k]) - sum(c == 'a' for c in w[n - k:])
            if dk != P(w, k) + P(w, n - k) - P(w, n): bad += 1
print('(1) chord identity failures n<=14:', bad)

N = 16
def dyck(m):
    if m == 0: return ['']
    return ['b' + L + 'a' + R for i in range(m) for L in dyck(i) for R in dyck(m - 1 - i)]
E = ['b' + d + 'a' for m in range(N // 2) for d in dyck(m)]
pairs = [(e, '') for e in E]
def blocks(k, L):
    out = ['a']
    for _ in range(k): out = [e + x for e in E for x in out if len(e + x) <= L]
    return out
for k in range(N // 2):
    pairs += [('b', x) for x in blocks(k, N)]
seqs = [('', '')]; allUV = Counter(); fr = [('', '')]; outer_bad = 0
while fr:
    nf = []
    for U, V in fr:
        allUV[(U, V)] += 1
        for k in range(1, min(len(U), len(V)) + 1):
            if P(U, k) - (P(V, len(V)) - P(V, len(V) - k)) >= 0: outer_bad += 1
        for u, v in pairs:
            if len(U) + len(V) + len(u) + len(v) <= N: nf.append((U + u, v + V))
    fr = nf
print(f'(2) two-tape contexts {len(allUV)}, max multiplicity {max(allUV.values())}, outer-walk violations {outer_bad}')
res = Counter()
for p, q in [('', ''), ('b', 'a'), ('bb', 'aa')]:
    for m in range(0, 4):
        for t in itertools.product('ab', repeat=m):
            w = ''.join(t); words = Counter(); outG = 0
            for U, V in allUV:
                W = p + U + w + V + q
                if len(W) <= N:
                    words[W] += 1; outG += not inG(W)
            amb = sum(c > 1 for c in words.values())
            res[(outG == 0, amb == 0)] += 1
            if outG == 0: print(f'   p={p!r} w={w!r} q={q!r}: all in G-, ambiguous words={amb}')
print('   (allInG, injective) tally over centres:', dict(res))
for n in (20, 100, 400, 2000):
    m1, m2 = (n + 1) // 2, n // 2
    M = lambda m: comb(m, m // 2)   # weak one-sided meanders of length m
    print(f'(3) n={n}: |Safe_n| n/2^n = {M(m1) * M(m2) * n / 2**n:.4f}')
