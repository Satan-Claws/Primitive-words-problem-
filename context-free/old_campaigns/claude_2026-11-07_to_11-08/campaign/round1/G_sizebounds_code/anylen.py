# Theorem 4 check: for every long-side length L in [ceil(5n/8), n-1] (i.e. middle length l=L or l=n-L),
# cyclic windows of length L with spacing s=L-max(M1+M2-1,M1) give an exact cover of Q_n.
import numpy as np
from verify_general import all_words, prim, has_period, divisors
def check(n,k,L,W,P):
    D=divisors(n); E=[d for d in D if 2*d!=n]; Es=sorted(E,reverse=True)
    M1=Es[0] if Es else 0; M2=Es[1] if len(Es)>1 else 0
    s=L-max(M1+M2-1,M1); assert s>=1
    T=list(range(0,n,s)); h=n//2
    cov=np.zeros(len(W),bool); nr=0
    for t in T:
        idx=[(t+o)%n for o in range(L)]; X=W[:,idx]
        aE=np.ones(len(W),bool)
        for d in E: aE&=~has_period(X,d)
        if n%2: cov|=aE; nr+=1; continue
        cov|=aE&~has_period(X,h); nr+=1
        for o in range(L):
            i=idx[o]; j=(i+h)%n
            if (j-t)%n<L: continue
            for a in range(k): cov|=aE&(W[:,i]==a)&(W[:,j]!=a); nr+=1
    return (not np.any(cov&~P)) and (not np.any(P&~cov)), len(T), nr
for n in range(16,21):
    W=all_words(n,2); P=prim(W)
    res=[]
    for L in range(-(-5*n//8), n):
        ok,r,nr=check(n,2,L,W,P); res.append((L,ok,r,nr))
    print(n, all(x[1] for x in res), "max windows",max(x[2] for x in res),"max rects",max(x[3] for x in res), flush=True)
