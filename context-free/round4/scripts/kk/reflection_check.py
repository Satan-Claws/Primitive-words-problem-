"""Exact check of Theorem A/B (weighted reflection escape) in kk.md.
For n, h>0 (integer, period set D_h), delta: delta' = delta/h (Fractions).
B_p = {c in Z_n : (1-rho_c) delta' in V_{n/p}}, rho_c: i -> c-i mod n.
Checks: (i) B_p lies in a single residue class mod p^{a_p}; (ii) some c is in no B_p (p in P_h);
(iii) for that c, the set delta + N P_{c,h} meets V_{n/p} for no p in P_h along the family (spot check).
Usage: python3 reflection_check.py  (runs exhaustive small cases + random large cases)"""
import random, itertools, sys
from fractions import Fraction as Fr

def primes_of(n):
    ps=[];m=n;q=2
    while q*q<=m:
        if m%q==0:
            ps.append(q)
            while m%q==0: m//=q
        q+=1
    if m>1: ps.append(m)
    return ps

def vpow(n,p):
    a=0
    while n%p==0: n//=p;a+=1
    return a

def periodic(v,d):
    n=len(v); return all(v[i]==v[(i+d)%n] for i in range(n))

def check(n,h,delta):
    dp=[Fr(delta[i],h[i]) for i in range(n)]
    Ph=[p for p in primes_of(n) if periodic(h,n//p)]
    if any(periodic(delta,n//p) for p in Ph): return None  # family not in E_n
    B={}
    for p in Ph:
        B[p]=[c for c in range(n) if periodic([dp[i]-dp[(c-i)%n] for i in range(n)], n//p)]
        pa=p**vpow(n,p)
        assert len({c%pa for c in B[p]})<=1, ('B_p not in one class',n,h,delta,p,B[p])
    good=[c for c in range(n) if all(c not in B[p] for p in Ph)]
    assert good, ('no good c',n,h,delta,B)
    return good

def rand_hard(n,rng,B=3):
    # random element of W_n = sum of periodic subspaces, plus small noise sometimes
    v=[0]*n
    for p in primes_of(n):
        d=n//p; pat=[rng.randint(0,B) for _ in range(d)]
        for i in range(n): v[i]+=pat[i%d]
    return v

if __name__=='__main__':
    rng=random.Random(1)
    # exhaustive: h=1, delta in {0,1,2}^n, n=6; delta in {0,1}^n for n=10,12
    for n,B in [(6,2),(10,1),(12,1),(15,1)]:
        cnt=0
        for delta in itertools.product(range(B+1),repeat=n):
            if check(n,[1]*n,list(delta)) is not None: cnt+=1
        print('exhaustive n=%d delta in {0..%d}^n: %d primitive deltas, all escaped'%(n,B,cnt),flush=True)
    # exhaustive with nonconstant periodic h, n=6, h of period 3 / 2
    for hpat in [(1,2,4),(1,3),(2,1,1)]:
        h=[hpat[i%len(hpat)] for i in range(6)]
        cnt=0
        for delta in itertools.product(range(3),repeat=6):
            if check(6,h,list(delta)) is not None: cnt+=1
        print('exhaustive n=6 h=%s delta in {0..2}^6: %d family-deltas, all escaped'%(h,cnt),flush=True)
    # random hard deltas (in W_n) and random periodic h for large n
    for n in [30,42,60,210]:
        tot=0
        for t in range(300 if n<210 else 60):
            delta=rand_hard(n,rng)
            if rng.random()<0.5:
                h=[1]*n
            else:
                ps=primes_of(n); p=rng.choice(ps); d=n//p
                pat=[rng.randint(1,5) for _ in range(d)]; h=[pat[i%d] for i in range(n)]
            if check(n,h,delta) is not None: tot+=1
        print('random n=%d: %d hard families checked, all escaped'%(n,tot),flush=True)
