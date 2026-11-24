"""uniform_nonpow.py -- exact parse-tree counts for the mismatch grammar G_p of
NonPow_p = { w in {a,b}^* : w is not a p-th power }  (p prime, any length).

Grammar G_p (start S; C -> a | b):
  S   -> R_r                          r = 1..p-1          (|w| not = 0 mod p)
  R_r -> C^r | C^p R_r
  S   -> P[c,s] M[p-2-c,t]            s != t in {a,b}, c = 0..p-2
  P[c,s] -> C^{p-1} P[c,s] C | C^c s      ( {x s y : |x| = (p-1)|y| + c} )
  M[d,t] -> C M[d,t] C^{p-1} | t C^d      ( {z t u : |u| = (p-1)|z| + d} )
Claim: amb(w) = 1 if p !| |w|, else A_p(w) = #{ i < (p-1)m : w[i] != w[i+m] }, m=|w|/p.
Checks the claim exhaustively for all binary words up to length L.  [computational]
"""
import itertools, sys
from functools import lru_cache

def grammar(p):
    G = {'C': [('a',), ('b',)], 'S': []}
    for r in range(1, p):
        G['S'].append((f'R{r}',))
        G[f'R{r}'] = [('C',)*r, ('C',)*p + (f'R{r}',)]
    for c in range(p-1):
        d = p-2-c
        for s in 'ab':
            for t in 'ab':
                if s != t:
                    G['S'].append((f'P{c}{s}', f'M{d}{t}'))
        for s in 'ab':
            G[f'P{c}{s}'] = [('C',)*(p-1) + (f'P{c}{s}',) + ('C',), ('C',)*c + (s,)]
            G[f'M{c}{s}'] = [('C',) + (f'M{c}{s}',) + ('C',)*(p-1), (s,) + ('C',)*c]
    return G

def count(G, w):
    n = len(w)
    @lru_cache(None)
    def X(A, i, j):           # trees of A deriving w[i:j]
        if A not in G:        # terminal
            return 1 if j == i+1 and w[i] == A else 0
        return sum(seq(rhs, 0, i, j) for rhs in G[A])
    @lru_cache(None)
    def seq(rhs, k, i, j):    # rhs[k:] derives w[i:j]; every symbol yields >= 1 letter
        rest = len(rhs) - k
        if rest == 0: return 1 if i == j else 0
        if j - i < rest: return 0
        if rest == 1: return X(rhs[k], i, j)
        return sum(X(rhs[k], i, l) * seq(rhs, k+1, l, j) for l in range(i+1, j-rest+2))
    return X('S', 0, n)

def predicted(p, w):
    n = len(w)
    if n % p: return 1
    m = n // p
    return sum(w[i] != w[i+m] for i in range((p-1)*m))

if __name__ == '__main__':
    for p, lens in [(2, range(1, 13)), (3, range(1, 13)), (5, range(1, 11)), (7, [1, 6, 7, 13, 14])]:
        G = grammar(p); bad = 0; tot = 0; mx = {}
        for n in lens:
            for t in itertools.product('ab', repeat=n):
                w = ''.join(t); c = count(G, w); tot += 1
                if c != predicted(p, w): bad += 1
                mx[n] = max(mx.get(n, 0), c)
        print(f'p={p}: lengths {list(lens)}: {tot}, mismatches vs formula: {bad}; max amb by length (n%p==0):',
              {n: mx[n] for n in mx if n % p == 0}, flush=True)
