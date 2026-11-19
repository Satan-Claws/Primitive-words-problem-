import sys,itertools
from math import gcd
def blocks(w,one):
    # cyclic block vector: a-runs (letter !=one) before each 'one'
    n=len(w); idx=[i for i in range(n) if w[i]==one]
    K=len(idx)
    if K==0: return []
    return [ (idx[k]-idx[k-1]-1)%n if K>1 else n-1 for k in range(K)]
def Lstar(x,l):
    K=len(x)
    if K%l or K<2*l: return False
    for s in range(K):
        D=[x[i]-x[(s-i)%K] for i in range(K)]
        nf=0;ok=True
        for c in range(l):
            cl=[D[i] for i in range(c,K,l)]
            if (2*c-s)%l==0:
                nz=sum(1 for v in cl if v)
                if nz==0: continue
                if nz==2: nf+=1
                else: ok=False
            else:
                if any(v>0 for v in cl) and any(v<0 for v in cl): ok=False
        if ok and nf==1: return True
    return False
def BGB(x,B):
    K=len(x)
    for s in range(K):
        mm=sum(1 for i in range(K) if x[i]>x[(s-i)%K]); e=K-2*mm
        if mm>=1 and (mm<=B or e<=B) and gcd(mm,e)==1: return True
    return False
def PAR(w,B):
    b=w.count('b');a=len(w)-b
    if gcd(a,b)!=1: return False
    return min(a,b)<=B or any(abs(al*a-be*b)==1 for al in range(1,B+1) for be in range(1,B+1))
def fam(w,B=3,L=8):
    r={'PAR':PAR(w,B)}
    xs=[blocks(w,c) for c in 'ab']
    r['L']=any(x and Lstar(x,l) for x in xs for l in range(1,L+1))
    r['BGB']=any(len(x)>=2 and BGB(x,B) for x in xs)
    return r
if __name__=='__main__':
    N=int(sys.argv[1]); bad=0; cnt=0
    for n in range(2,N+1):
        for d in range(1,n):
            if n%d: continue
            for u in itertools.product('ab',repeat=d):
                w=''.join(u)*(n//d); cnt+=1
                r=fam(w)
                if any(r.values()): bad+=1; print('NONPRIM ACCEPTED',w,r)
    print('checked',cnt,'nonprimitive-or-dup words up to',N,'bad',bad)
