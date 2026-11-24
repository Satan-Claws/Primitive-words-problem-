"""r3_offw_fold.py -- the uniform FOLD grammar G_fold and the word-level off-W set Off.

Off := { w in {a,b}^+ : xhat_w(1) != 0 },  xhat_w(1) = sum_{k : w[k]=b} zeta_n^k,  n = |w|
     = { w : Phi_n(z) does not divide B_w(z) = sum_{w[k]=b} z^k }        (exact integer test used below)
     = { w : prod_{p|n} (1 - T^{n/p}) x != 0 }  (Moebius-cube transform; checked below)

G_fold (start S, uniform, no counting):
  A  -> a A a | b A b | b A a | eps | a | b      pairs (outer-in) never (a,b)   [left-dominant]
  A1 -> a A1 a | b A1 b | b A a                  ... with >= 1 strict pair (b,a)
  A0 -> a A0 a | b A0 b | eps | a | b            palindromes
  A0p-> a A0 a | b A0 b | a | b                  nonempty palindromes
  B, B1, B0p: same with the roles of (a,b) and (b,a) swapped.
  S  -> A1 B | A0p B1 | B1 A | B0p A1
Claim [proof in r3_offw.md]: amb(w) = #{ (m, orientation) : fold certificate at reflection k -> m-k }  <= n,
and L(G_fold) subset Off subset Q.
Checks: exhaustive n <= NMAX; random long words.  [computational]
"""
import itertools, random, sys
from functools import lru_cache
import numpy as np
import sympy

T = ('a', 'b')
G = {
    'A':  [('a','A','a'), ('b','A','b'), ('b','A','a'), (), ('a',), ('b',)],
    'A1': [('a','A1','a'), ('b','A1','b'), ('b','A','a')],
    'A0': [('a','A0','a'), ('b','A0','b'), (), ('a',), ('b',)],
    'A0p':[('a','A0','a'), ('b','A0','b'), ('a',), ('b',)],
    'B':  [('a','B','a'), ('b','B','b'), ('a','B','b'), (), ('a',), ('b',)],
    'B1': [('a','B1','a'), ('b','B1','b'), ('a','B','b')],
    'B0': [('a','B0','a'), ('b','B0','b'), (), ('a',), ('b',)],
    'B0p':[('a','B0','a'), ('b','B0','b'), ('a',), ('b',)],
    'S':  [('A1','B'), ('A0p','B1'), ('B1','A'), ('B0p','A1')],
}

def count(w):
    """exact number of derivation trees of S for w (grammar has eps but no unit cycles)"""
    n = len(w)
    @lru_cache(None)
    def X(A, i, j):
        if A in T:
            return 1 if j == i + 1 and w[i] == A else 0
        return sum(seq(r, 0, i, j) for r in G[A])
    @lru_cache(None)
    def seq(r, k, i, j):
        if k == len(r):
            return 1 if i == j else 0
        if k == len(r) - 1:
            return X(r[k], i, j)
        tot = 0
        for l in range(i + (r[k] in T), j + 1):
            x = X(r[k], i, l)
            if x:
                tot += x * seq(r, k + 1, l, j)
        return tot
    return X('S', 0, n)

def certs(w):
    """direct count of fold certificates: m in 0..n-1, u=w[:m+1], v=w[m+1:]"""
    n = len(w); c = 0
    def pairs(s):
        return [(s[k], s[len(s) - 1 - k]) for k in range(len(s) // 2)]
    for m in range(n):
        uP = pairs(w[:m + 1]); vP = pairs(w[m + 1:])
        for L, R in (('b', 'a'), ('a', 'b')):        # orientation: u never (R,L)... see below
            # orientation 1 (L='b'): u in A (never (a,b)), v in B (never (b,a)); strict somewhere
            okU = all(p != (R, L) for p in uP); okV = all(p != (L, R) for p in vP)
            strict = any(p == (L, R) for p in uP) or any(p == (R, L) for p in vP)
            c += okU and okV and strict
    return c

def off_mask(n):
    """boolean array over all 2^n words (bit k = 1 <-> w[k]='b'): xhat(1) != 0, exact via mod Phi_n"""
    z = sympy.symbols('z')
    phi = sympy.Poly(sympy.cyclotomic_poly(n, z), z)
    d = phi.degree()
    M = np.zeros((n, d), dtype=np.int64)
    for k in range(n):
        r = sympy.Poly(z**k, z).rem(phi).all_coeffs()[::-1]
        M[k, :len(r)] = [int(c) for c in r]
    idx = np.arange(2**n, dtype=np.int64)
    X = ((idx[:, None] >> np.arange(n)) & 1).astype(np.int64)
    return np.any(X @ M != 0, axis=1), X

def prim_mask(n, X):
    idx = np.arange(2**n, dtype=np.int64)
    full = (1 << n) - 1
    power = np.zeros(2**n, bool)
    for p in sympy.primefactors(n):
        s = n // p
        rot = ((idx >> s) | (idx << (n - s))) & full
        power |= rot == idx
    return ~power

def mobius_mask(n, X):
    Y = X.copy()
    for p in sympy.primefactors(n):
        Y = Y - np.roll(Y, -(n // p), axis=1)
    return np.any(Y != 0, axis=1)

def word(i, n):
    return ''.join('b' if (i >> k) & 1 else 'a' for k in range(n))

if __name__ == '__main__':
    NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 14
    print(' n  |Q_n|   |Off_n| |Q\\Off| |Fold_n|  Fold/Off  maxamb  argmax       grammar==certs  Fold<=Off')
    for n in range(1, NMAX + 1):
        off, X = off_mask(n) if n > 1 else (np.array([False, True]), None)   # n=1: Off_1 = {b}
        if n == 1:
            prim = np.array([True, True]); X = np.array([[0], [1]])
        else:
            prim = prim_mask(n, X)
            assert np.array_equal(off, mobius_mask(n, X))
        assert not np.any(off & ~prim)          # Off subset Q
        nf = 0; mx = -1; arg = None; agree = True; sound = True
        for i in range(2**n):
            w = word(i, n); g = count(w)
            if g != certs(w): agree = False
            if g:
                nf += 1
                if not off[i]: sound = False
            if g > mx: mx, arg = g, w
        print(f'{n:2d} {int(prim.sum()):6d} {int(off.sum()):8d} {int((prim & ~off).sum()):6d} {nf:8d} '
              f'{nf / off.sum():8.4f} {mx:6d}  {arg:12s} {agree!s:>6} {sound!s:>9}')
    # random long words
    random.seed(1); bad = 0; mxr = 0
    for _ in range(300):
        n = random.randint(15, 60)
        # biased words so that certificates exist often: fold a random half-dominant pattern
        w = ''.join(random.choice('ab') for _ in range(n))
        if random.random() < 0.7:
            m = random.randrange(n); u = list(w[:m + 1]); v = list(w[m + 1:])
            for k in range(len(u) // 2):
                if (u[k], u[-1 - k]) == ('a', 'b'): u[k], u[-1 - k] = 'b', 'a'
            for k in range(len(v) // 2):
                if (v[k], v[-1 - k]) == ('b', 'a'): v[k], v[-1 - k] = 'a', 'b'
            w = ''.join(u + v)
        g = count(w); c = certs(w)
        xh = sum(np.exp(2j * np.pi * k / n) for k in range(n) if w[k] == 'b')
        if g != c or (g and abs(xh) < 1e-9): bad += 1
        mxr = max(mxr, g / n)
    print('random n in [15,60], 300 words: disagreements/unsound =', bad, ' max amb/n =', round(mxr, 3))
