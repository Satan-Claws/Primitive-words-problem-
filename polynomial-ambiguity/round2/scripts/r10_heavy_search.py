"""r10_heavy_search.py -- targeted search for Corollary-H-shaped counterexamples.
Grammar: S -> p X q,  X -> x X y  for (x,y) in a pair set P,  X -> w.
Components x,y are concatenations of <=2 tokens from {a,b,E} (E = b D a, strict negative excursions, mu(E)=1/2),
so every pair set is a linear SCC fed by the heavy-tailed block E.  We keep pair sets with context measure
sum mu(x)mu(y) == 1 exactly (critical) and at least one E, then test (i) inclusion in G- and (ii) unambiguity
(no word produced twice) for all words of length <= N."""
import itertools, sys
from fractions import Fraction as Fr
from collections import Counter
N = int(sys.argv[1]) if len(sys.argv) > 1 else 14

def dyck(m):  # Dyck words over b(up) a(down), length 2m
    if m == 0: return ['']
    out = []
    for i in range(m):
        for L in dyck(i):
            for R in dyck(m - 1 - i): out.append('b' + L + 'a' + R)
    return out
E = [w for m in range(N // 2) for w in ('b' + d + 'a' for d in dyck(m)) if len(w) <= N]
TOK = {'a': ['a'], 'b': ['b'], 'E': E}
MU = {'a': Fr(1, 2), 'b': Fr(1, 2), 'E': Fr(1, 2)}
def comp_words(c):
    out = ['']
    for t in c: out = [u + v for u in out for v in TOK[t] if len(u + v) <= N]
    return out
comps = [''] + [''.join(t) for k in (1, 2) for t in itertools.product('abE', repeat=k)]
def mu(c):
    m = Fr(1)
    for t in c: m *= MU[t]
    return m
pairs = [(x, y) for x in comps for y in comps if (x or y)]
pm = {p: mu(p[0]) * mu(p[1]) for p in pairs}
PW = {p: [(u, v) for u in comp_words(p[0]) for v in comp_words(p[1])] for p in pairs}

def inG(w):
    n = len(w); d = 0
    for k in range(n // 2):
        d += (w[k] == 'a') - (w[n - 1 - k] == 'a')
        if d >= 0: return False
    return True

def test(P, p, q, w):
    base = len(p) + len(q) + len(w)
    seen = Counter(); frontier = [('', '')]
    while frontier:
        nf = []
        for (U, V) in frontier:
            word = p + U + w + V + q
            seen[word] += 1
            if seen[word] > 1: return 'amb', word
            if not inG(word): return 'out', word
            for pr in P:
                for (u, v) in PW[pr]:
                    if base + len(U) + len(V) + len(u) + len(v) <= N: nf.append((U + u, v + V))
        frontier = nf
    return 'ok', len(seen)

ends = [('', ''), ('b', 'a'), ('bb', 'aa'), ('b', ''), ('', 'a')]
cent = ['', 'a', 'b', 'ab', 'ba', 'bb', 'aa']
stats = Counter(); survivors = []
for size in (1, 2, 3):
    for P in itertools.combinations(pairs, size):
        if sum(pm[x] for x in P) != 1: continue
        if not any('E' in x + y for x, y in P): continue
        for (p, q) in ends:
            for w in cent:
                r = test(P, p, q, w); stats[r[0]] += 1
                if r[0] == 'ok': survivors.append((P, p, q, w, r[1]))
print('N =', N, 'results:', dict(stats))
for s in survivors[:20]: print('SURVIVOR', s)

# second stage: re-test survivors at larger N2 (rebuilds token tables)
N2 = int(sys.argv[2]) if len(sys.argv) > 2 else 0
if N2:
    N = N2
    E[:] = [w for m in range(N // 2) for w in ('b' + d + 'a' for d in dyck(m)) if len(w) <= N]
    for pr in pairs: PW[pr] = [(u, v) for u in comp_words(pr[0]) for v in comp_words(pr[1])]
    st2 = Counter(); left = []
    for (P, p, q, w, _) in survivors:
        r = test(P, p, q, w); st2[r[0]] += 1
        if r[0] == 'ok': left.append((P, p, q, w, r[1]))
        elif len(left) < 0: pass
    print('stage2 N =', N, 'of', len(survivors), 'survivors:', dict(st2))
    for s in left: print('STILL OK', s)
