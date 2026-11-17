# Redteam: scout F5 (conjecture): every primitive w of length n has, for each prime p|n, a p-witness
# (i, i+j n/p), 1<=j<p, w_i != w_{i+jn/p}, such that the chosen pairs are pairwise non-crossing.
import sys, random, itertools
from rt_common import *
def witnesses(bits,n,p):
    d=n//p
    return [(i,i+j*d) for j in range(1,p) for i in range(n-j*d) if bits[i]!=bits[i+j*d]]
def cross(x,y):
    a,b=x;c,d=y
    return a<c<b<d or c<a<d<b
def ok(bits,n,P):
    W=[witnesses(bits,n,p) for p in P]
    if any(not w for w in W): return None  # not primitive
    def rec(k,chosen):
        if k==len(W): return True
        for pr in W[k]:
            if all(not cross(pr,q) for q in chosen):
                if rec(k+1,chosen+[pr]): return True
        return False
    return rec(0,[])
mode=sys.argv[1]
if mode=='ex':
    for n in map(int,sys.argv[2:]):
        P=primes_of(n); fails=0; tot=0
        for w in range(1<<n):
            bits=[(w>>i)&1 for i in range(n)]
            r=ok(bits,n,P)
            if r is None: continue
            tot+=1
            if not r: fails+=1; print('FAIL',to_str(w,n))
        print('n',n,'primitive',tot,'fails',fails)
else:
    random.seed(5)
    for n in map(int,sys.argv[2:]):
        P=primes_of(n); fails=0; tot=0
        for t in range(3000):
            # near-periodic: sum (xor) of periodic words for different primes, plus few flips
            bits=[0]*n
            for p in P:
                if random.random()<0.7:
                    d=n//p; u=[random.randint(0,1) for _ in range(d)]
                    bits=[b^u[i%d] for i,b in enumerate(bits)]
            for _ in range(random.randint(0,2)):
                bits[random.randrange(n)]^=1
            r=ok(bits,n,P)
            if r is None: continue
            tot+=1
            if not r: fails+=1; print('FAIL',''.join('ab'[b] for b in bits))
        print('n',n,'sampled primitive',tot,'fails',fails)
