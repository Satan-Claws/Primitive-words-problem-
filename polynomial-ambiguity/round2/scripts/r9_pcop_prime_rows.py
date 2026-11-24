r"""r9_pcop: verify the explicit linearly-ambiguous grammar G_P for
   L_P = Sigma+ \ ({b^m : m>=2} U {v^n : n>=2, #a(v)=1})
and the facts used in reports/r9_pcop.md:
  (a) L(G_P) = L_P (exhaustive, |w| <= NMAX)
  (b) Q subset L_P, and every w in L_P \ Q has #a(w) composite
  (c) amb_{G_P}(w) <= max(1, #a(w)-1)   (exact tree counts by DP)
  (d) two-letter version L_P2 = Sigma+ \ (N_a U N_b): L_P2 \ Q has #a,#b both composite,
      and the 4-piece decomposition used in the report gives the same language.
Usage: .venv/bin/python r9_pcop_prime_rows.py [NMAX]
"""
import sys
from functools import lru_cache
from itertools import product

NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 13

# ---- grammar G_P (terminals 'a','b'; nonterminals upper-case strings) ----
G = {
    'S':  [['ONEA'], ['b'], ['W1'], ['W2']],
    'ONEA': [['BS', 'a', 'BS']],            # b* a b*
    'BS': [['b', 'BS'], []],                 # b*
    'BP': [['b', 'BS']],                     # b+
    'ST': [['a', 'ST'], ['b', 'ST'], []],    # Sigma*
    # W1 = Sigma* a K a Sigma*,  K = b^x a b^y, x != y
    'W1': [['ST', 'a', 'K', 'a', 'ST']],
    'K':  [['K1'], ['K2']],
    'K1': [['b', 'K1', 'b'], ['BP', 'a']],   # b^{y+d} a b^y, d>=1
    'K2': [['b', 'K2', 'b'], ['a', 'BP']],   # b^x a b^{x+d}
    # W2 = { b^s Z b^x a b^t : x != s+t },  Z = a | a Sigma* a
    'Z':  [['a'], ['a', 'ST', 'a']],
    'A':  [['b', 'A', 'b'], ['Z']],          # b^s Z b^s
    'C':  [['b', 'C', 'b'], ['BP', 'a']],    # b^{t+d} a b^t       (x > s+t)
    'E':  [['b', 'E', 'b'], ['a', 'BP']],    # b^e a b^{e+d}       (s <= x < s+t)
    'F':  [['b', 'F', 'b'], ['BP', 'Z']],    # b^x b^d Z b^x       (x < s)
    'W2': [['A', 'C'], ['A', 'E'], ['F', 'a', 'BS']],
}


def count_trees(w):
    n = len(w)

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
        tot = 0
        for k in range(i, j + 1):
            c = nt(X, i, k)
            if c:
                tot += c * seq(rest, k, j)
        return tot
    return nt('S', 0, n)


def prim(w):
    n = len(w)
    return n > 0 and all(not (n % d == 0 and w == w[:d] * (n // d)) for d in range(1, n))


def root(w):
    n = len(w)
    for d in range(1, n + 1):
        if n % d == 0 and w == w[:d] * (n // d):
            return w[:d]


def composite(m):
    return m >= 4 and any(m % q == 0 for q in range(2, int(m ** 0.5) + 1))


def in_N(w, x):   # nonprimitive, root has exactly one letter x
    r = root(w)
    return len(r) < len(w) and r.count(x) == 1


def LP_def(w):
    if not w:
        return False
    if set(w) == {'b'} and len(w) >= 2:
        return False
    return not in_N(w, 'a')


def LP2_def(w):
    return bool(w) and not in_N(w, 'a') and not in_N(w, 'b')


def swap(w):
    return w.translate(str.maketrans('ab', 'ba'))


def LP2_pieces(w):   # decomposition by (contains aa, contains bb)
    A, B = 'aa' in w, 'bb' in w
    if A and B:
        return True
    if B and not A:
        return LP_def(w)
    if A and not B:
        return LP_def(swap(w))
    # alternating words
    return prim(w)


bad = 0
maxratio = 0
tot = 0
for n in range(1, NMAX + 1):
    for t in product('ab', repeat=n):
        w = ''.join(t)
        tot += 1
        c = count_trees(w)
        if (c > 0) != LP_def(w):
            bad += 1; print('lang mismatch', w, c)
        if prim(w) and c == 0:
            bad += 1; print('Q not covered', w)
        if c > 0 and not prim(w) and not composite(w.count('a')):
            bad += 1; print('bad extra word', w)
        if c > max(1, w.count('a') - 1):
            bad += 1; print('amb too big', w, c)
        if LP2_def(w) != LP2_pieces(w):
            bad += 1; print('LP2 pieces mismatch', w)
        if LP2_def(w) and not prim(w) and not (composite(w.count('a')) and composite(w.count('b'))):
            bad += 1; print('LP2 bad extra', w)
        if prim(w) and not LP2_def(w):
            bad += 1; print('LP2 misses Q', w)
print(f'NMAX={NMAX}: {tot} words checked, {bad} failures')


# ---- (e) section 4 L_M, definitional check (no grammar): L_M ⊇ Q, extras have root a-count not dividing M ----
def gaps(w):
    N = w.count('a'); idx = [i for i, ch in enumerate(w) if ch == 'a']
    g = [idx[i + 1] - idx[i] - 1 for i in range(N - 1)]
    return g + [idx[0] + len(w) - 1 - idx[-1]]


def LM_def(w, M):
    N = w.count('a')
    if N <= M:
        return True
    g = gaps(w)
    return any(g[i] != g[(i + M) % N] for i in range(N))


badM = 0
for M in (2, 3, 4, 6):
    for n in range(1, min(NMAX, 14) + 1):
        for t in product('ab', repeat=n):
            w = ''.join(t)
            if w.count('a') == 0 or w.count('a') <= M:
                continue
            inL = LM_def(w, M)
            if prim(w) and not inL:
                badM += 1; print('L_M misses Q', M, w)
            if inL and not prim(w) and M % root(w).count('a') == 0:
                badM += 1; print('L_M bad extra', M, w)
print(f'L_M check (M=2,3,4,6, |w|<={min(NMAX,14)}): {badM} failures')
