import sys, itertools
from functools import lru_cache
sys.setrecursionlimit(10000)
def prim(w):
    n=len(w)
    if n==0: return False
    return all(w!=w[d:]+w[:d] for d in range(1,n) if n%d==0)
@lru_cache(None)
def Y(s):
    if len(s)<2: return False
    if s[0]==s[-1] and Y(s[1:-1]): return True
    return s[0]=='a' and s[-1]=='b' and Z(s[1:-1])
@lru_cache(None)
def Z(s):
    if s in ('','a','b'): return True
    if len(s)<2: return False
    return (s[0],s[-1])!=('b','a') and Z(s[1:-1])
def S(s): return Y(s) or (len(s)>=1 and Y(s[1:]))
def side(i,c,n):
    D=(2*i-c)%(2*n)
    if D==0 or D==n: return 0
    return 1 if D<n else 2
def cycpred(w):
    n=len(w)
    for c in range(n):
        sides=set(); mixed=False
        for i in range(n):
            j=(c-i)%n
            if w[i]=='b' and w[j]=='a':
                mixed=True; sides.add(side(i,c,n))
        if mixed and len(sides)==1: return True
    return False
def words(n): return (''.join(t) for t in itertools.product('ab',repeat=n))
NMAX=int(sys.argv[1]) if len(sys.argv)>1 else 13
for n in range(1,NMAX+1):
    LS=set(w for w in words(n) if S(w))
    assert all(prim(w) for w in LS), n
    cyc=set(w[r:]+w[:r] for w in LS for r in range(n))
    pred=set(w for w in words(n) if cycpred(w))
    assert cyc==pred,(n,len(cyc),len(pred))
    # density bound
    assert len(cyc)<=2*n*2**n*(0.75)**((n-1)//2)
    # missed primitive necklaces
    seen=set(); miss=0; tot=0
    for w in words(n):
        if not prim(w): continue
        can=min(w[r:]+w[:r] for r in range(n))
        if can in seen: continue
        seen.add(can); tot+=1
        if can not in cyc: miss+=1
    print(n,len(LS),len(cyc),'missed necklaces',miss,'of',tot,flush=True)
# F1 family
for m in range(2,61):
    w='bb'+'a'*m+'bab'+'a'*m
    assert prim(w) and not cycpred(w),m
print('F1 ok m<=60')
# F1 m=0,1 ?
for m in range(0,2):
    w='bb'+'a'*m+'bab'+'a'*m; print('F1 m=',m,w,prim(w),cycpred(w))
# imbalance n/6
def imbmax(n):
    best=0
    for p in range(2,n+1):
        if n%p: continue
        q=n//p
        for u in itertools.product('ab',repeat=q):
            w=''.join(u)*p; x,y=w[:n//2],w[n//2:]
            best=max(best,abs(x.count('b')-y.count('b')))
    return best
for n in range(2,25,2): 
    b=imbmax(n); assert b<=n/6+1e-9,(n,b); print('imb',n,b,n/6)
