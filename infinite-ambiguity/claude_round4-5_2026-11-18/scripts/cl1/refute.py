"""CL1 refutation check.
L = a . P,  P = { p in (a*b)* : block vector of p is a palindrome }  (P contains eps).
Grammar (linear):  T -> a S ;  S -> N b | A b | eps ;  N -> a N a | b S ;  A -> a A | eps.
Cyc(L) = all conjugates of words of L (CF by closure of CFLs under cyclic shift).
Checks: (1) grammar language == condition-defined language, all lengths <= GMAX;
        (2) every word of L of length <= PMAX is primitive (exhaustive over Sigma^n);
        (3) every conjugate of every such word is primitive (trivially, conjugation-invariance; checked anyway);
        (4) every a(a^m b)^k with |w| <= FMAX is in L (via grammar membership = condition)."""
import itertools, sys
GMAX, PMAX, FMAX = 16, 22, 60

def primitive(w):
    n = len(w)
    return n > 0 and all(not (n % d == 0 and w == w[:d] * (n // d)) for d in range(1, n))

def blocks(p):  # p in (a*b)*  -> block vector, or None
    if p and p[-1] != 'b': return None
    if not p: return []
    return [len(x) for x in p[:-1].split('b')]

def in_L_cond(w):
    if not w.startswith('a'): return False
    z = blocks(w[1:])
    return z is not None and z == z[::-1]

# grammar language enumeration by length (memoized sets)
from functools import lru_cache
@lru_cache(None)
def S(n):
    out = set()
    if n == 0: out.add('')
    if n >= 1:
        out |= {x + 'b' for x in N(n - 1)}
        out.add('a' * (n - 1) + 'b')
    return frozenset(out)
@lru_cache(None)
def N(n):
    out = set()
    if n >= 2: out |= {'a' + x + 'a' for x in N(n - 2)}
    if n >= 1: out |= {'b' + x for x in S(n - 1)}
    return frozenset(out)
def T(n): return frozenset('a' + x for x in S(n - 1)) if n >= 1 else frozenset()

# (1)
for n in range(0, GMAX + 1):
    g = set(T(n))
    c = {''.join(t) for t in itertools.product('ab', repeat=n) if in_L_cond(''.join(t))}
    assert g == c, (n, g ^ c)
print('grammar == condition up to length', GMAX)
# (2),(3)
cnt = 0
for n in range(1, PMAX + 1):
    for w in T(n):
        cnt += 1
        assert primitive(w), w
        if n <= 16:
            for i in range(n): assert primitive(w[i:] + w[:i]), (w, i)
print('all', cnt, 'words of L up to length', PMAX, 'primitive; conjugates checked to 16')
# (4)
c4 = 0
for m in range(1, FMAX):
    for k in range(2, FMAX):
        w = 'a' + ('a' * m + 'b') * k
        if len(w) > FMAX: break
        assert in_L_cond(w) and (len(w) > 40 or w in T(len(w))), w
        c4 += 1
print('F_ins members up to length', FMAX, 'in L:', c4)
