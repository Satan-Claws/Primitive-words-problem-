# Builds an explicit CFG for Q ∩ (ab*)^p (p odd prime) as the union of two unambiguous grammars
# A1 (pairs (1,2),(3,4),...) and A2 (pairs (2,3),(4,5),...), and counts parse trees by
# memoised dynamic programming. Checks: every word of (ab*)^p with all b-blocks <= B gets
# 0 trees if non-primitive, 1 or 2 trees if primitive; and no word outside (ab*)^p is derivable
# (by construction every derivable word has exactly p a's and starts with a; we also check all
# words over {a,b} of length <= Lmax).
import sys, itertools
from functools import lru_cache
def is_primitive(w):
    n = len(w)
    return all(w != w[:d] * (n // d) for d in range(1, n) if n % d == 0)
def build(p):
    R = {}  # nonterminal -> list of right-hand sides (tuples); terminals are 'a','b'
    def add(A, *rhs): R.setdefault(A, []).append(tuple(rhs))
    # Bs = b*, Bp = b+
    add('Bs'); add('Bs', 'b', 'Bs'); add('Bp', 'b'); add('Bp', 'b', 'Bp')
    add('F', 'a', 'Bs')                  # one free block a b^x
    add('P', 'b', 'P', 'b'); add('P', 'a')  # b^n a b^n
    add('Eq', 'a', 'P')                  # a b^n a b^n
    add('U', 'b', 'U', 'b'); add('U', 'Bp', 'a'); add('U', 'a', 'Bp')  # b^n a b^m, n != m
    add('Ne', 'a', 'U')
    for name, first in (('A1', 1), ('A2', 2)):
        pairs = [(i, i + 1) for i in range(first, p, 2) if i + 1 <= p]
        for t in range(len(pairs)):
            rhs = []
            pos = 1
            for j, (i1, i2) in enumerate(pairs):
                while pos < i1: rhs.append('F'); pos += 1
                if j < t: rhs.append('Eq'); pos += 2
                elif j == t: rhs.append('Ne'); pos += 2
                else: rhs += ['F', 'F']; pos += 2
            while pos <= p: rhs.append('F'); pos += 1
            add(name, *rhs)
    add('S', 'A1'); add('S', 'A2')
    return R
def counter(R, w):
    @lru_cache(None)
    def cnt(X, i, j):
        if X in ('a', 'b'): return 1 if j == i + 1 and w[i] == X else 0
        return sum(seq(rhs, 0, i, j) for rhs in R[X])
    @lru_cache(None)
    def seq_(rhs, k, i, j):
        if k == len(rhs): return 1 if i == j else 0
        tot = 0
        for m in range(i, j + 1):
            c = cnt(rhs[k], i, m)
            if c: tot += c * seq_(rhs, k + 1, m, j)
        return tot
    def seq(rhs, k, i, j): return seq_(rhs, k, i, j)
    return cnt('S', 0, len(w))
p, B, Lmax = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
R = build(p)
bad = 0; hist = {}
for xs in itertools.product(range(B + 1), repeat=p):
    w = ''.join('a' + 'b' * x for x in xs)
    c = counter(R, w)
    ok = (c == 0) if not is_primitive(w) else (1 <= c <= 2)
    hist[c] = hist.get(c, 0) + 1
    if not ok: bad += 1; print('FAIL', xs, c)
for L in range(1, Lmax + 1):
    for t in itertools.product('ab', repeat=L):
        w = ''.join(t)
        if w.count('a') == p and w[0] == 'a': continue
        if counter(R, w): bad += 1; print('FAIL outside', w)
print('p=%d B=%d: tree-count histogram %s, failures %d' % (p, B, hist, bad))
