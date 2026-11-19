"""Fractional-position classes (Lemma 2 / Theorem 3 of crossing.md).
For a word x, minper(x) = least period. A class is given by a set of primes S (here {2} or {2,3}),
an aperiodicity threshold, choices j_p in [1,p) and letters c_p != c'_p.
  L = {y : minper(y) > tau*|y|, y[|y| - ceil(j_p|y|/p)] = c_p  for p in S}
  M = {m : minper(m) > tau*|m|, m[floor(j_p|m|/p)] = c'_p for p in S}
Part 1: verify L*M subset of Q for all |y|,|m| <= NMAX (exhaustive over pieces).
Part 2: coverage: which primitive words of length n have a balanced conjugate factorization
(y = rotation[0,l), m = rest, n/3 < l <= 2n/3) lying in some class."""
import sys, itertools
from math import ceil

def minper(x):
    n=len(x)
    for d in range(1,n+1):
        if all(x[i]==x[i+d] for i in range(n-d)): return d
    return n

def primitive(w):
    n=len(w)
    for d in range(1,n):
        if n%d==0 and w==w[:d]*(n//d): return False
    return n>0

FAMS=[((2,3),0.5),((2,),2/3)]   # (primes, tau)

def sig(x, primes, side):
    """letters at fractional positions; side 'L' or 'M'; returns dict over (p,j)."""
    l=len(x); out={}
    for p in primes:
        for j in range(1,p):
            if side=='L': out[(p,j)]=x[l-ceil(j*l/p)]
            else: out[(p,j)]=x[(j*l)//p]
    return out

def in_some_class(y,m):
    for primes,tau in FAMS:
        if minper(y)<=tau*len(y) or minper(m)<=tau*len(m): continue
        sy=sig(y,primes,'L'); sm=sig(m,primes,'M')
        # need for every p in primes some j with sy != sm
        if all(any(sy[(p,j)]!=sm[(p,j)] for j in range(1,p)) for p in primes):
            return True
    return False

def words(n): return (''.join(t) for t in itertools.product('ab',repeat=n))

def soundness(NMAX):
    # every class: for all y in L, m in M with |y|,|m|<=NMAX, ym primitive.
    # equivalent check: for all pairs (y,m) that are in a COMMON class.
    pieces=[w for k in range(1,NMAX+1) for w in words(k)]
    bad=0
    for primes,tau in FAMS:
        Ls=[(y,sig(y,primes,'L')) for y in pieces if minper(y)>tau*len(y)]
        Ms=[(m,sig(m,primes,'M')) for m in pieces if minper(m)>tau*len(m)]
        for y,sy in Ls:
            for m,sm in Ms:
                # common class exists iff for every p some j with sy!=sm
                if all(any(sy[(p,j)]!=sm[(p,j)] for j in range(1,p)) for p in primes):
                    if not primitive(y+m):
                        bad+=1; print("UNSOUND",primes,y,m)
    return bad

def coverage(n):
    unc=[]
    seen=set()
    for w in words(n):
        if not primitive(w): continue
        c=min(w[r:]+w[:r] for r in range(n))
        if c in seen: continue
        seen.add(c)
        ok=False
        for r in range(n):
            v=w[r:]+w[:r]
            for l in range(n//3+1, 2*n//3+1):
                if 3*l<=n: continue
                if in_some_class(v[:l],v[l:]): ok=True;break
            if ok:break
        if not ok: unc.append(c)
    return len(seen),unc

if __name__=="__main__":
    NS=int(sys.argv[1]); NC=int(sys.argv[2])
    print("soundness pieces up to",NS,": unsound pairs =",soundness(NS))
    for n in range(2,NC+1):
        tot,unc=coverage(n)
        print(n,"conj classes",tot,"uncovered",len(unc),unc[:6])
