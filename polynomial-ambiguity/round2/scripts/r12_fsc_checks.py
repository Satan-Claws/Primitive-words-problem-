"""r12_fsc_checks.py -- checks for r12_fsc.md.
A. Lemma Ori: E_l (primitive negative excursions) and D_l (bridges <= 0) have a pointwise-maximal walk.
B. Lemma Env/No-go 4: s E_l t subset G-  <=>  s xhat_l t in G-   (all |s|,|t|<=5, l<=12).
C. Lemma SF: non-oriented heavy block E u E+ (excursions of either sign): no context (|s|,|t|<=5)
   keeps s B_l t in G- for all l <= 14.
D. Height-coupled critical model {(b E^i, E^j a)}: G- inclusion and word multiplicity, N <= 18.
"""
import itertools, sys
from collections import Counter

def walk(w):
    P = [0];
    for c in w: P.append(P[-1] + (1 if c == 'a' else -1))   # doubled walk 2P
    return P

def inG(w):
    n = len(w); pa = [0]
    for c in w: pa.append(pa[-1] + (c == 'a'))
    return all(pa[k] - (pa[n] - pa[n - k]) < 0 for k in range(1, n // 2 + 1))

def words(l):
    for t in itertools.product('ab', repeat=l): yield ''.join(t)

def E(l):   # primitive negative excursions
    return [w for w in words(l) if (P := walk(w))[-1] == 0 and all(x < 0 for x in P[1:-1])] if l >= 2 else []
def Epos(l):
    return [w for w in words(l) if (P := walk(w))[-1] == 0 and all(x > 0 for x in P[1:-1])] if l >= 2 else []
def Dneg(l):
    return [w for w in words(l) if (P := walk(w))[-1] == 0 and all(x <= 0 for x in P)]

out = []
# A
okA = True; xhat = {}
for l in range(2, 21, 2):
    for name, cls in (('E', E), ('D', Dneg)):
        C = cls(l); W = [walk(w) for w in C]
        env = [max(P[j] for P in W) for j in range(l + 1)]
        att = [w for w, P in zip(C, W) if P == env]
        okA &= len(att) == 1
        if name == 'E': xhat[l] = att[0]
out.append(f"A: pointwise max attained (unique) for E_l, D_l, l<=20: {okA}; xhat_8={xhat[8]}")
# B
ctx = [''.join(t) for m in range(6) for t in itertools.product('ab', repeat=m)]
Ecache = {l: E(l) for l in range(2, 13, 2)}
mism = 0; tot = 0; safe = 0
for s in ctx:
    for t in ctx:
        for l in range(2, 13, 2):
            a = all(inG(s + x + t) for x in Ecache[l]); b = inG(s + xhat[l] + t)
            tot += 1; mism += (a != b); safe += a
out.append(f"B: monotone reduction, {tot} (s,t,l) triples, mismatches={mism}, safe triples={safe}")
# C
Bc = {l: E(l) + Epos(l) for l in range(2, 15, 2)}
surv = [(s, t) for s in ctx for t in ctx if all(inG(s + x + t) for l in Bc for x in Bc[l])]
survE = [(s, t) for s in ctx for t in ctx if all(inG(s + x + t) for l in Bc for x in E(l) if l <= 14)] if False else None
out.append(f"C: contexts (|s|,|t|<=5) with s(E u E+)_l t in G- for all l<=14: {len(surv)}")
# D
N = int(sys.argv[1]) if len(sys.argv) > 1 else 18
Eall = {l: E(l) for l in range(2, N + 1, 2)}
def seqs(maxlen):  # sequences of E-blocks with total length <= maxlen -> list of strings
    res = ['']; frontier = ['']
    while frontier:
        nf = []
        for u in frontier:
            for l, C in Eall.items():
                if len(u) + l <= maxlen:
                    for x in C: nf.append(u + x)
        res += nf; frontier = nf
    return res
Es = seqs(N)
for (p, w, q) in [('b', '', 'a'), ('bb', 'ab', 'aa'), ('b', 'b', 'a'), ('bb', 'aab', 'aa')]:
    mult = Counter(); bad = 0
    def rec(U, V):
        global bad
        W = p + U + w + V + q
        if len(W) > N: return
        mult[W] += 1
        if not inG(W): bad += 1
        for u2 in Es:
            if len(W) + 2 + len(u2) > N: break
            for v2 in Es:
                if len(W) + 2 + len(u2) + len(v2) > N: break
                rec(U + 'b' + u2, v2 + 'a' + V)
    Es.sort(key=len); rec('', '')
    amb = sum(1 for m in mult.values() if m > 1); mx = max(mult.values())
    out.append(f"D: (p,w,q)=({p},{w},{q}) N<={N}: words={len(mult)} G-violations={bad} ambiguous words={amb} max mult={mx}")
print('\n'.join(out))
