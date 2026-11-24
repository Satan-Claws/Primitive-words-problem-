r"""r10_2q: verify Theorem N2 (containment form) of reports/r10_2q.md.
 G2  : explicit grammar for L_2 = {#a = 2} U {#a >= 4 even, cyclic gap seq not 2-periodic}  (checked on even rows)
 L** : (oo ∩ L_P2) U (eo ∩ ([bb] ∩ L_2  U  [no bb] ∩ swap(L_P))) U (oe ∩ swap of that)
       Cop ⊆ L**,  L** ∩ {#a or #b in P ∪ 2P} ⊆ Q,  amb ≤ |w|  (trees counted exactly, pieces disjoint & regular-filtered)
Usage: .venv/bin/python r10_2q_grammar.py [NMAX] [ROWLEN]
"""
import sys
from functools import lru_cache
from itertools import product, combinations
from math import gcd
sys.setrecursionlimit(10000)
NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 12
ROWLEN = int(sys.argv[2]) if len(sys.argv) > 2 else 18

COMMON = {'BS': [['b', 'BS'], []], 'BP': [['b', 'BS']], 'ST': [['a', 'ST'], ['b', 'ST'], []]}
GP = dict(COMMON, **{   # r9 grammar G_P for L_P
    'S': [['ONEA'], ['b'], ['W1'], ['W2']], 'ONEA': [['BS', 'a', 'BS']],
    'W1': [['ST', 'a', 'K', 'a', 'ST']], 'K': [['K1'], ['K2']],
    'K1': [['b', 'K1', 'b'], ['BP', 'a']], 'K2': [['b', 'K2', 'b'], ['a', 'BP']],
    'Z': [['a'], ['a', 'ST', 'a']], 'A': [['b', 'A', 'b'], ['Z']],
    'C': [['b', 'C', 'b'], ['BP', 'a']], 'E': [['b', 'E', 'b'], ['a', 'BP']],
    'F': [['b', 'F', 'b'], ['BP', 'Z']], 'W2': [['A', 'C'], ['A', 'E'], ['F', 'a', 'BS']]})
G2 = dict(COMMON, **{   # new: distance-2 gap witnesses
    'S': [['TWOA'], ['W1'], ['W2']], 'TWOA': [['BS', 'a', 'BS', 'a', 'BS']],
    'W1': [['ST', 'a', 'K', 'a', 'ST']], 'K': [['K1'], ['K2']],          # a b^x a b* a b^y a, x != y
    'K1': [['b', 'K1', 'b'], ['BP', 'a', 'BS', 'a']], 'K2': [['b', 'K2', 'b'], ['a', 'BS', 'a', 'BP']],
    # wrap: b^s Z b^x a b* a b^t, Z = first..antepenultimate a, x = y_{N-2} != s+t
    'Z': [['a'], ['a', 'ST', 'a']], 'A': [['b', 'A', 'b'], ['Z']],
    'C': [['b', 'C', 'b'], ['BP', 'a', 'BS', 'a']],                     # x > s+t
    'E': [['b', 'E', 'b'], ['a', 'BS', 'a', 'BP']],                     # s <= x < s+t
    'F': [['b', 'F', 'b'], ['BP', 'Z']],                                # x < s
    'W2': [['A', 'C'], ['A', 'E'], ['F', 'a', 'BS', 'a', 'BS']]})


def counter(G):
    def count(w):
        @lru_cache(maxsize=None)
        def nt(A, i, j):
            return sum(seq(tuple(r), i, j) for r in G[A])

        @lru_cache(maxsize=None)
        def seq(rhs, i, j):
            if not rhs:
                return 1 if i == j else 0
            X, rest = rhs[0], rhs[1:]
            if X in ('a', 'b'):
                return seq(rest, i + 1, j) if i < j and w[i] == X else 0
            return sum(nt(X, i, k) * seq(rest, k, j) for k in range(i, j + 1) if nt(X, i, k))
        return nt('S', 0, len(w))
    return count


cP, c2 = counter(GP), counter(G2)
sw = lambda w: w.translate(str.maketrans('ab', 'ba'))


def prim(w):
    n = len(w)
    return n > 0 and all(not (n % d == 0 and w == w[:d] * (n // d)) for d in range(1, n))


def root(w):
    n = len(w)
    return next(w[:d] for d in range(1, n + 1) if n % d == 0 and w == w[:d] * (n // d))


def isprime(m):
    return m >= 2 and all(m % k for k in range(2, int(m ** .5) + 1))


def special(m):  # m in P or 2P
    return isprime(m) or (m % 2 == 0 and isprime(m // 2))


def gaps(w):
    idx = [i for i, ch in enumerate(w) if ch == 'a']; N = len(idx)
    return [idx[i + 1] - idx[i] - 1 for i in range(N - 1)] + [idx[0] + len(w) - 1 - idx[-1]]


def L2_def(w):
    N = w.count('a')
    if N == 2:
        return True
    if N < 4 or N % 2:
        return False
    g = gaps(w)
    return any(g[i] != g[(i + 2) % N] for i in range(N))


def inN(w, x):
    r = root(w); return len(r) < len(w) and r.count(x) == 1


def LP_def(w):
    return bool(w) and not (set(w) == {'b'} and len(w) >= 2) and not inN(w, 'a')


def amb_LP2(w):   # r9 4-piece decomposition
    A, B = 'aa' in w, 'bb' in w
    if A and B: return 1
    if B: return cP(w)
    if A: return cP(sw(w))
    return 1 if prim(w) else 0


def amb_eo(w):    # #a even, #b odd
    return c2(w) if 'bb' in w else cP(sw(w))


def amb_star(w):
    A, B = w.count('a') % 2, w.count('b') % 2
    if A and B: return amb_LP2(w)
    if not A and B: return amb_eo(w)
    if A and not B: return amb_eo(sw(w))
    return 0


def star_def(w):  # definitional membership of L**
    A, B = w.count('a') % 2, w.count('b') % 2
    if A and B: return not inN(w, 'a') and not inN(w, 'b')
    if not A and B: return L2_def(w) if 'bb' in w else LP_def(sw(w))
    if A and not B: return star_def(sw(w))
    return False


bad = tot = 0; mx = 0
for n in range(1, NMAX + 1):
    for t in product('ab', repeat=n):
        w = ''.join(t); tot += 1
        na = w.count('a')
        if na % 2 == 0 and c2(w) and not L2_def(w) or (na % 2 == 0 and L2_def(w) and not c2(w)):
            bad += 1; print('G2 lang', w)
        if na % 2 == 0 and c2(w) > max(1, na - 2):
            bad += 1; print('G2 amb', w, c2(w))
        m = amb_star(w); mx = max(mx, m - len(w))
        if (m > 0) != star_def(w): bad += 1; print('L** lang', w)
        if m > len(w): bad += 1; print('L** amb', w, m)
        if gcd(na, n - na) == 1 and not m: bad += 1; print('Cop miss', w)
        if m and not prim(w) and (special(na) or special(n - na)): bad += 1; print('L** bad extra', w)
print(f'grammar checks |w|<={NMAX}: {tot} words, {bad} failures, max(amb-|w|)={mx}')

# rows #a in {4,6,10,14}, |w| <= ROWLEN, definitional: containment everywhere, equality on #b odd
for N in (4, 6, 10, 14):
    rb = rows = eqodd = 0
    for n in range(N, ROWLEN + 1):
        for pos in combinations(range(n), N):
            s = ['b'] * n
            for p in pos: s[p] = 'a'
            w = ''.join(s); rows += 1
            inL, p_ = star_def(w), prim(w)
            if inL and not p_: rb += 1
            if (n - N) % 2 == 1 and inL != p_: rb += 1
            if (n - N) % 2 == 1: eqodd += 1
    print(f'row #a={N}, |w|<={ROWLEN}: {rows} words ({eqodd} with #b odd): {rb} failures')
