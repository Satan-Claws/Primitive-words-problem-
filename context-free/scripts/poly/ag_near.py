"""Task G substitute (walk.md / builder3.md not found in repo or git history).
Near-grammars for Q: G_A = coPow_2 grammar (scripts/devil/copow_grammar.py, k=2);
G_B = length dispatch: even -> M_2, odd & 3|n -> M_3, n = ±1 mod 6 -> non-constant words.
Checks L(G) vs Q exhaustively to LMAX, verifies tree counts against closed formula, reports max amb."""
import sys, itertools, random
sys.path.insert(0, '../devil'); sys.path.insert(0, '.')
from copow_grammar import grammar as copow
from ag_common import count_trees, bar_hillel, primitive

def tag(G, start, t):
    ren = lambda X: (t, X) if X in G else X
    return {ren(A): [tuple(ren(x) for x in r) for r in rs] for A, rs in G.items()}, ren(start)

def mod_dfa(m, allowed):
    st = list(range(m)); d = {(q, c): (q + 1) % m for q in st for c in 'ab'}
    return st, d, 0, [r for r in allowed]

def build_B():
    G2 = copow(2); G3 = copow(3)
    M2 = {k: v for k, v in G2.items()}; 
    H1, s1 = tag(G2, 'M', 'm2')
    H2, s2 = bar_hillel(G3, 'M', *mod_dfa(2, [1]))
    H2, s2 = tag(H2, s2, 'm3')
    C = {'C': [('a', 'A1'), ('b', 'B1')], 'A1': [('a', 'A1'), ('b', 'R')], 'B1': [('b', 'B1'), ('a', 'R')],
         'R': [(), ('a', 'R'), ('b', 'R')]}
    H3, s3 = bar_hillel(C, 'C', *mod_dfa(6, [1, 5]))
    H3, s3 = tag(H3, s3, 'c')
    G = {}; G.update(H1); G.update(H2); G.update(H3); G['S'] = [(s1,), (s2,), (s3,)]
    return G, 'S'

def mism(w, k):
    n = len(w); m = n // k
    return sum(w[i] != w[i + m] for i in range(n - m))

def fA(w):
    n = len(w)
    return 1 if n % 2 else mism(w, 2)
def fB(w):
    n = len(w)
    if n % 2 == 0: return mism(w, 2)
    if n % 3 == 0: return mism(w, 3)
    return 0 if len(set(w)) < 2 else 1

if __name__ == '__main__':
    LV = int(sys.argv[1]); LM = int(sys.argv[2])
    GA = copow(2); GB, sB = build_B()
    for name, G, s, f in (('G_A', GA, 'S', fA), ('G_B', GB, sB, fB)):
        cex = []
        for n in range(1, LV + 1):
            for t in itertools.product('ab', repeat=n):
                w = ''.join(t); c = count_trees(G, s, w)
                assert c == f(w), (name, w, c, f(w))
                if (c > 0) != primitive(w): cex.append(w)
        rng = random.Random(1)
        for _ in range(300):
            n = rng.randint(LV + 1, LM); w = ''.join(rng.choice('ab') for _ in range(n))
            assert count_trees(G, s, w) == f(w)
        print(name, 'formula verified exhaustively n<=%d, 300 random n<=%d' % (LV, LM))
        print(name, 'counterexamples (L != Q) n<=%d: count=%d first=%s' % (LV, len(cex), cex[:6]))
        byn = {}
        for w in cex: byn.setdefault(len(w), []).append(w)
        print(name, 'cex per length', {k: len(v) for k, v in byn.items()})
        row = []
        for n in range(1, 25):
            best = max(f(''.join(t)) for t in itertools.product('ab', repeat=n)) if n <= 20 else None
            if best is None:
                best = f('a' * (n // 2) + 'b' * (n - n // 2)) if n % 2 == 0 else f(('a' * (n // 3) + 'b' * (n // 3)) + 'a' * (n - 2 * (n // 3)))
            ext = [ ''.join(t) for t in itertools.product('ab', repeat=n) if f(''.join(t)) == best][:1] if n <= 14 else ['-']
            row.append((n, best, ext[0]))
        print(name, 'maxamb', row)
