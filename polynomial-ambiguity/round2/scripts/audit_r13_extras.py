"""Audit r13: semantic check (grammars already matched to definitions by audit_r13_grammars.py) of
Thm N / L_P2 / Thm N2(c) on ALL non-primitive words |w| <= M (default 32). Also lists first extras of L**."""
import sys, importlib.util
from itertools import product
from collections import Counter
M = int(sys.argv[1]) if len(sys.argv) > 1 else 32
def root(w):
    n = len(w)
    for d in range(1, n + 1):
        if n % d == 0 and w[:d] * (n // d) == w: return w[:d]
def isprime(x): return x >= 2 and all(x % p for p in range(2, int(x ** .5) + 1))
def special(x): return isprime(x) or (x % 2 == 0 and isprime(x // 2)) or (x >= 1 and x & (x - 1) == 0)
def sw(w): return w.translate(str.maketrans('ab', 'ba'))
def LP(w):
    r = root(w); return not (set(w) == {'b'} and len(w) >= 2) and not (r != w and r.count('a') == 1)
def LP2(w):
    r = root(w)
    return not (r != w and (r.count('a') == 1 or r.count('b') == 1)) and not (len(set(w)) == 1 and len(w) >= 2)
def L2(w):
    N = w.count('a')
    if N == 2: return True
    if N >= 4 and N % 2 == 0:
        i = w.index('a'); g = [len(x) for x in (w[i:] + w[:i])[1:].split('a')]
        return any(g[i] != g[(i + 2) % N] for i in range(N))
    return False
def eo(w): return (L2(w) if 'bb' in w else LP(sw(w)))
def Lss(w):
    na, nb = w.count('a'), w.count('b')
    if na % 2 and nb % 2: return LP2(w)
    if na % 2 == 0 and nb % 2: return eo(w)
    if na % 2 and nb % 2 == 0: return eo(sw(w))
    return False
fails = Counter(); first = []; cnt = Counter()
for lv in range(1, M // 2 + 1):
    for t in product('ab', repeat=lv):
        v = ''.join(t)
        if root(v) != v: continue
        for d in range(2, M // lv + 1):
            w = v * d; na, nb = w.count('a'), w.count('b')
            if LP(w):
                cnt['LP-extra'] += 1
                if na < 4 or isprime(na): fails['N'] += 1
            if LP2(w) and (na < 4 or isprime(na) or nb < 4 or isprime(nb)): fails['LP2'] += 1
            if Lss(w):
                cnt['L**-extra'] += 1
                if len(first) < 3 or len(w) < len(first[0]): first.append(w)
                if special(na) or special(nb): fails['N2c'] += 1; print('N2c fail', w)
print('M =', M, 'counts', dict(cnt), 'failures', dict(fails) or 0)
print('shortest L** extras:', sorted(first, key=len)[:3])
