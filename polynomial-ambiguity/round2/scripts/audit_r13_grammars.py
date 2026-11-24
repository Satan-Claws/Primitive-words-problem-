"""Audit r13: independent rebuild of G_P (r9 Thm N), L_P2, G_2 and L** (r10 Thm N2).
Exact tree counts (Python big ints) by length-layered derivation enumeration, cross-checked
against a per-word CYK-style memo DP for |w| <= XC. Usage: audit_r13_grammars.py [L=16] [XC=10]"""
import sys
from collections import Counter
from functools import lru_cache
from itertools import product
from math import gcd

L = int(sys.argv[1]) if len(sys.argv) > 1 else 16
XC = int(sys.argv[2]) if len(sys.argv) > 2 else 10

def G(rules):  # "X -> A b C | ..." lines ; 'eps' = empty
    g = {}
    for line in filter(str.strip, rules.strip().splitlines()):
        lhs, rhs = line.split('->')
        g[lhs.strip()] = [tuple(s for s in alt.split() if s != 'eps') for alt in rhs.split('|')]
    return g

COMMON = """
ST -> a ST | b ST | eps
BS -> b BS | eps
BP -> b BS
"""
GP = G(COMMON + """
S -> ONEA | b | W1 | W2
ONEA -> BS a BS
W1 -> ST a K a ST
K -> K1 | K2
K1 -> b K1 b | BP a
K2 -> b K2 b | a BP
Z -> a | a ST a
A -> b A b | Z
C -> b C b | BP a
E -> b E b | a BP
F -> b F b | BP Z
W2 -> A C | A E | F a BS
""")
G2 = G(COMMON + """
S -> TWOA | W1 | W2
TWOA -> BS a BS a BS
W1 -> ST a K a ST
K -> K1 | K2
K1 -> b K1 b | BP a BS a
K2 -> b K2 b | a BS a BP
Z -> a | a ST a
A -> b A b | Z
C -> b C b | BP a BS a
E -> b E b | a BS a BP
F -> b F b | BP Z
W2 -> A C | A E | F a BS a BS
""")

def enumerate_counts(g, Lmax):
    @lru_cache(None)
    def nt(X, n):
        c = Counter()
        for body in g[X]:
            c.update(seq(body, n))
        return c
    @lru_cache(None)
    def sym(s, n):
        if s in g: return nt(s, n)
        return Counter({s: 1}) if n == 1 else Counter()
    @lru_cache(None)
    def seq(body, n):
        if not body: return Counter({'': 1}) if n == 0 else Counter()
        out = Counter()
        for n1 in range(n + 1):
            c1 = sym(body[0], n1)
            if not c1: continue
            c2 = seq(body[1:], n - n1)
            if not c2: continue
            for u, x in c1.items():
                for v, y in c2.items():
                    out[u + v] += x * y
        return out
    tot = {}
    for n in range(Lmax + 1):
        tot.update(nt('S', n))
    return tot

def cyk(g, w):  # independent per-word tree count
    @lru_cache(None)
    def nt(X, i, j):
        return sum(seq(b, i, j) for b in g[X])
    @lru_cache(None)
    def seq(body, i, j):
        if not body: return 1 if i == j else 0
        s, r = body[0], body[1:]
        if s not in g:
            return seq(r, i + 1, j) if i < j and w[i] == s else 0
        return sum(nt(s, i, k) * seq(r, k, j) for k in range(i, j + 1))
    return nt('S', 0, len(w))

def root(w):
    n = len(w)
    for d in range(1, n + 1):
        if n % d == 0 and w[:d] * (n // d) == w: return w[:d]
def prim(w): return len(w) > 0 and root(w) == w
def isNa(w): r = root(w); return len(w) > 0 and r != w and r.count('a') == 1
def isNb(w): r = root(w); return len(w) > 0 and r != w and r.count('b') == 1
def sw(w): return w.translate(str.maketrans('ab', 'ba'))
def LP(w): return len(w) > 0 and not (set(w) == {'b'} and len(w) >= 2) and not isNa(w)
def LP2(w): return len(w) > 0 and not isNa(w) and not isNb(w) and not (len(set(w)) == 1 and len(w) >= 2)
def gaps(w):  # cyclic gap sequence
    N = w.count('a'); i = w.index('a'); r = w[i:] + w[:i]
    return [len(x) for x in r[1:].split('a')] if N else None
def L2(w):
    N = w.count('a')
    if N == 2: return True
    if N >= 4 and N % 2 == 0:
        g_ = gaps(w); return any(g_[i] != g_[(i + 2) % N] for i in range(N))
    return False
def isprime(x): return x >= 2 and all(x % p for p in range(2, int(x ** .5) + 1))
def special(x): return isprime(x) or (x % 2 == 0 and isprime(x // 2)) or (x >= 1 and x & (x - 1) == 0)

words = [''.join(t) for n in range(L + 1) for t in product('ab', repeat=n)]
fails = Counter(); ex = {}
def bad(k, w):
    fails[k] += 1; ex.setdefault(k, w)

cP = enumerate_counts(GP, L); c2 = enumerate_counts(G2, L)
print('enumerated', len(cP), len(c2))
for w in words:
    if len(w) <= XC:
        if cyk(GP, w) != cP.get(w, 0): bad('cyk-GP', w)
        if cyk(G2, w) != c2.get(w, 0): bad('cyk-G2', w)
    na, nb = w.count('a'), w.count('b'); p = prim(w)
    # Theorem N
    aP = cP.get(w, 0)
    if (aP > 0) != LP(w): bad('N:lang', w)
    if aP > max(1, na - 1): bad('N:amb', w)
    if p and aP == 0: bad('N:Q-sub', w)
    if aP and not p and (na < 4 or isprime(na)): bad('N:composite', w)
    # L_P2 via regions
    AA, BB = 'aa' in w, 'bb' in w
    if AA and BB: a2 = 1
    elif BB: a2 = aP
    elif AA: a2 = cP.get(sw(w), 0)
    else: a2 = 1 if (len(w) > 0 and not (len(w) >= 4 and len(w) % 2 == 0 and root(w) in ('ab', 'ba'))) else 0
    if (a2 > 0) != LP2(w): bad('LP2:lang', w)
    if a2 > max(1, len(w)): bad('LP2:amb', w)
    if a2 and not p and (na < 4 or isprime(na) or nb < 4 or isprime(nb)): bad('LP2:composite', w)
    # G2
    a_2 = c2.get(w, 0)
    if na % 2 == 0 and (a_2 > 0) != L2(w): bad('G2:lang', w)
    if a_2 > max(1, na - 2) and na % 2 == 0: bad('G2:amb', w)
    # L**
    def eo_piece(x):
        xa, xb = x.count('a'), x.count('b')
        if not (xa % 2 == 0 and xb % 2 == 1): return 0
        return c2.get(x, 0) if 'bb' in x else cP.get(sw(x), 0)
    if na % 2 and nb % 2: s_ = a2
    elif na % 2 == 0 and nb % 2: s_ = eo_piece(w)
    elif na % 2 and nb % 2 == 0: s_ = eo_piece(sw(w))
    else: s_ = 0
    if s_ > max(1, len(w)): bad('N2:amb', w)
    if len(w) and gcd(na, nb) == 1 and not s_: bad('N2:Cop', w)
    if s_ and not p and (special(na) or special(nb)): bad('N2:special', w)
    if na % 2 == 0 and nb % 2 == 1 and na >= 2 and special(na) and na % 2 == 0 and isprime(na // 2) and p and not s_: bad('N2:(d)', w)
    if s_ and not p: fails['N2:extra(info)'] += 0; ex.setdefault('N2:first-extra', w)
print('L =', L, 'XC =', XC, 'words', len(words))
print('failures:', dict(fails) or 0)
print('examples:', ex)
