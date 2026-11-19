# audit5: float densities of T^k(E') at large odd n (truncated outer D <= C*sqrt(n): a LOWER bound)
import numpy as np, sys
from math import lgamma
gammaln=np.vectorize(lambda x: lgamma(x) if x>0 else 1e300)
from functools import lru_cache
C=12.0
def wvec(D,n):
    # vector over j=0..D of N(j,m)/4^m, m=(n-D)/2
    m=(n-D)//2; j=np.arange(D+1,dtype=float)
    if m==0: v=np.zeros(D+1); v[0]=1.0; return v
    with np.errstate(divide='ignore',invalid='ignore'):
        lg=np.log(np.maximum(j,1))-np.log(m)+gammaln(2*m+1)-gammaln(m-j+1)-gammaln(m+j+1)-m*np.log(4)
    v=np.exp(lg); v[0]=0.0; v[j>m]=0.0
    return v
def E_vec(D):
    v=np.zeros(D+1)
    for j in range(D+1):
        if abs(D-2*j)==1: v[j]=np.exp(gammaln(D+1)-gammaln(j+1)-gammaln(D-j+1)-D*np.log(2))
    return v
@lru_cache(None)
def F(k,n):
    """density vector over j (#b) for T^k(E') at length n"""
    if k==0: return tuple(E_vec(n))
    out=np.zeros(n+1)
    Dmax=min(n,int(C*np.sqrt(n))+3)
    for D in range(1,Dmax+1):
        if (n-D)%2: continue
        fm=np.array(F(k-1,D))
        if not fm.any(): continue
        s=(n/D)*float(fm@wvec(D,n))
        m=(n-D)//2
        out[m]+=s; out[n-m]+=s
    return tuple(out)
if __name__=='__main__':
    k=int(sys.argv[1])
    for n in map(int,sys.argv[2:]):
        d=sum(F(k,n)); print(k,n,round(d,4),'dens*n^(1/4)' if k==1 else '',round(d*n**0.25,4) if k==1 else '',flush=True)
