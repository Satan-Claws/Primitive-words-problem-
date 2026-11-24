"""Checks for cyclic.md:
 (A) sigma: x->ab, y->aabb.  sigma(u) in Q  <=>  u in Q, and gcd(#a,#b)(sigma(u)) = |sigma(u)|/2  (|u|<=14).
 (B) Active-prime lemma: w non-primitive <=> w is a p-th power for some prime p | gcd(#a,#b)   (|w|<=16).
 (C) gcd monotonicity: for random binary codes tau, gcd(Parikh tau(u)) is a multiple of gcd(Parikh u)."""
import itertools, random
from math import gcd
def prim(w):
    n=len(w); return n>0 and all(not(n%d==0 and w==w[:d]*(n//d)) for d in range(1,n))
def primes(m): return [p for p in range(2,m+1) if m%p==0 and all(p%q for q in range(2,p))]
bad=0
for n in range(1,15):
    for t in itertools.product('xy',repeat=n):
        u=''.join(t); s=''.join('ab' if c=='x' else 'aabb' for c in u)
        if prim(u)!=prim(s) or gcd(s.count('a'),s.count('b'))!=len(s)//2: bad+=1
print("(A) sigma mismatches:",bad)
bad=0
for n in range(1,17):
    for t in itertools.product('ab',repeat=n):
        w=''.join(t); g=gcd(w.count('a'),w.count('b'))
        pw=any(w==w[:n//p]*p for p in primes(g)) if g>1 else False
        if prim(w)==pw: bad+=1
print("(B) active-prime mismatches:",bad)
random.seed(0); bad=0
for _ in range(300):
    tx=''.join(random.choice('ab') for _ in range(random.randint(1,5)))
    ty=''.join(random.choice('ab') for _ in range(random.randint(1,5)))
    for _ in range(50):
        u=''.join(random.choice('xy') for _ in range(random.randint(1,12)))
        v=''.join(tx if c=='x' else ty for c in u)
        g0=gcd(u.count('x'),u.count('y')); g1=gcd(v.count('a'),v.count('b'))
        if g1%g0: bad+=1
print("(C) gcd-monotonicity violations:",bad)
