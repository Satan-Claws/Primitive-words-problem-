# audit5: exact (small n) / float (large n) density of the even-n variant G
from math import comb, lgamma, log, exp, sqrt
import sys
def coefC(s,r):  # [y^r] C(y)^s
    if r<0: return 0
    if s==0: return 1 if r==0 else 0
    return s*comb(2*r+s,r)//(2*r+s)
def exactG(n):
    tot=0
    for D in range(1,n+1):
        if (n-D)%2: continue
        m=(n-D)//2; s=0
        for b in range(0,D+1):
            for a in (2*b+1,2*b-1):
                c=D-a-b
                if a<0 or c<0: continue
                mult=comb(D,a)*comb(D-a,b)
                s+=mult*coefC(b+3*c, m-b-2*c)
        assert (n*s)%D==0; tot+=n*s//D
    return 2*tot
def lcoefC(s,r):
    if r<0: return None
    if s==0: return 0.0 if r==0 else None
    return log(s)-log(2*r+s)+lgamma(2*r+s+1)-lgamma(r+1)-lgamma(r+s+1)
def fltG(n,Cc=12):
    tot=0.0; L2=n*log(2)
    for D in range(1,min(n,int(Cc*sqrt(n)))+1):
        if (n-D)%2: continue
        m=(n-D)//2
        for b in range(0,D+1):
            for a in (2*b+1,2*b-1):
                c=D-a-b
                if a<0 or c<0: continue
                lc=lcoefC(b+3*c,m-b-2*c)
                if lc is None: continue
                lm=lgamma(D+1)-lgamma(a+1)-lgamma(b+1)-lgamma(c+1)
                tot+=exp(log(n/D)+lm+lc-L2)
    return 2*tot
for n in range(1,21): print(n, exactG(n)/2**n)
for n in [1000,1001,10000,10001,100000]:
    d=fltG(n); print(n,round(d,4),'d*n^.25=',round(d*n**.25,3),flush=True)
