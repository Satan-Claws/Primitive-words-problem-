# Hand-made finitely ambiguous grammars inside (ab*)^n, converted to CNF; check Lemma 3's formula.
from struct_check import *

def to_cnf(R, start):
    """R: dict A -> list of tuples of symbols ('a','b' terminals). No eps, no unit rules assumed."""
    G = {}; fresh = [0]
    def T(c):
        G.setdefault('T'+c, [('t', c)]); return 'T'+c
    def add(A, rhs):
        G.setdefault(A, [])
        if len(rhs) == 1:
            assert rhs[0] in 'ab', 'unit rule'; G[A].append(('t', rhs[0])); return
        syms = [T(s) if s in 'ab' else s for s in rhs]
        while len(syms) > 2:
            fresh[0] += 1; N = 'N%d' % fresh[0]
            G[N] = [('n', syms[-2], syms[-1])]; syms = syms[:-2] + [N]
        G[A].append(('n', syms[0], syms[1]))
    for A, rs in R.items():
        for rhs in rs: add(A, rhs)
    return G

cases = {
 # L_3 primitive slice as union of {x1!=x2} and {x2!=x3} (Theorem C of ambiguity.md): 1 or 2 trees
 'L3_2amb': (dict(S=[('a','U','F'), ('F','a','U')], U=[('b','U','b'), ('Bp','a'), ('a','Bp')],
                  Bp=[('b','Bp'), ('b',)], F=[('a',), ('F','b')]), 3, 6),
 # nested rings with the SAME pair {1,2}: a b^{p+q} a b^p
 'nested_same_pair': (dict(S=[('a','X')], X=[('b','X','b'), ('Y',)] , Y=[('b','Y'), ('a',)]), 2, 8),
 # disjoint rings: a b^i a b^i a b^j a b^j
 'two_disjoint': (dict(S=[('a','P','a','P')], P=[('b','P','b'), ('a',)]), 4, 3),
 # ring with s = 0 (only right side children): a b^k, and a ring touching the end
 's_zero': (dict(S=[('S','b'), ('a',)]), 1, 10),
 # ambiguity 3: x1 != x2 or x2 != x3 or x1 != x3 (nested pair {1,3} around {2})
 'three_way': (dict(S=[('a','U','F'), ('F','a','U'), ('a','V')],
                    U=[('b','U','b'), ('Bp','a'), ('a','Bp')], Bp=[('b','Bp'), ('b',)], F=[('a',), ('F','b')],
                    V=[('b','V','b'), ('Bp','a','Fb','a'), ('a','Fb','a','Bp')], Fb=[('b','Fb'), ('b',)]), 3, 5),
}
# fix unit rule in nested_same_pair: X -> Y replaced by copies of Y's rules
cases['nested_same_pair'][0]['X'] = [('b','X','b'), ('b','Y'), ('a',)]
cases['three_way'][0]['V'] += [('a','a','Bp'), ('Bp','a','a')]
for name, (R, n, B) in cases.items():
    G = to_cnf(R, 'S')
    st, info = analyse(G, 'S', n, B)
    print(name, st, info)
