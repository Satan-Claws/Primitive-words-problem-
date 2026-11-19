# Variant: only windows that contain the seam (positions n-1,0), so the yield side
# (complement, a linear interval of length n-lam) is UNCONSTRAINED (type A) or carries one letter (type B).
import numpy as np
from verify_general import all_words, prim, has_period, params
def check(n,k):
    D,E,lam,s=params(n)
    if 2*lam-n < max(E+[0]): return None
    W=all_words(n,k); P=prim(W); h=n//2
    T=sorted(set([(n-lam+j*s)%n for j in range((lam)//s+1) if n-lam+j*s<=n]+[0]))
    cov=np.zeros(len(W),bool); nr=0
    for t in T:
        idx=[(t+o)%n for o in range(lam)]; X=W[:,idx]
        aE=np.ones(len(W),bool)
        for d in E: aE&=~has_period(X,d)
        if n%2: cov|=aE; nr+=1; continue
        cov|=aE&~has_period(X,h); nr+=1
        for o in range(lam):
            i=idx[o]; j=(i+h)%n
            if (j-t)%n<lam: continue
            for a in range(k): cov|=aE&(W[:,i]==a)&(W[:,j]!=a); nr+=1
    return (not np.any(cov&~P)),(not np.any(P&~cov)),T,nr
for k,N in [(2,20),(3,11)]:
    for n in range(4,N+1):
        r=check(n,k)
        print(k,n,r if r is None else (r[0],r[1],len(r[2]),r[3]))
