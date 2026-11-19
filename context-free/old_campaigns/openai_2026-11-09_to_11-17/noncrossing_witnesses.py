"""Finite falsification checks for noncrossing mismatch certificates.

An edge (i,j), i<j, is eligible for prime p|n when n/p divides
j-i and the two input letters differ. One edge is selected per prime.
Endpoints may coincide. Edges cross exactly when i<k<j<l or k<i<l<j.
This program produces evidence only.
"""
from itertools import product
from random import Random


def primes(n):
    return [p for p in range(2, n + 1)
            if n % p == 0 and all(p % q for q in range(2, int(p**.5)+1))]


def crosses(e, f):
    a,b=e
    c,d=f
    return a<c<b<d or c<a<d<b


def candidates(w):
    n=len(w)
    return {p:[(i,j) for i in range(n) for j in range(i+n//p,n,n//p)
               if w[i]!=w[j]] for p in primes(n)}


def witness(w):
    c=candidates(w)
    if any(not edges for edges in c.values()):
        return None # Word is a proper power.
    def solve(left, chosen):
        if not left:
            return chosen
        p=min(left,key=lambda k:len(left[k]))
        for edge in left[p]:
            rest={q:[e for e in edges if not crosses(edge,e)]
                  for q,edges in left.items() if q!=p}
            if all(rest.values()):
                found=solve(rest,chosen+[(p,edge)])
                if found is not None:
                    return found
        return None
    return solve(c,[])


def test(w):
    c=candidates(w)
    if all(c.values()) and witness(w) is None:
        raise AssertionError('Primitive counterexample: '+''.join(map(str,w)))


if __name__=='__main__':
    rng=Random(90210)
    for n in [6,10,12,14,15,18]:
        for tail in product(range(2),repeat=n-1):
            test((0,)+tail) # Complementing letters preserves all edges.
        print('exhaustive length',n,'passed',flush=True)
    w=[int((i%2==0 and i%3==0) or (i%2==1 and i%5==0)) for i in range(30)]
    print('multiplexer-30 witness',witness(w),flush=True)
    for n,count in [(30,20000),(42,2000),(60,2000),(210,100)]:
        for _ in range(count):
            w=[rng.randrange(2) for i in range(n)]
            test(w)
        print('random length',n,'count',count,'passed',flush=True)
