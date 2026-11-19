# Independent re-implementation of builder2's predicates D, GB, RD, RGB, G, RG.
import sys
from math import gcd
B=3
def prim(w):
    n=len(w)
    return all(w!=w[:d]*(n//d) for d in range(1,n) if n%d==0)
def pairs_counts(w,c):
    n=len(w); m=0
    for i in range(n):
        j=(c-i)%n
        if w[i]=='a' and w[j]=='b': m+=1   # D_i=+1 meaning one orientation; count mismatched pairs
    return m
def G(w,Bnd=None):
    n=len(w)
    for c in range(n):
        m=pairs_counts(w,c); r=n-2*m
        if Bnd is not None and not (m<=Bnd or r<=Bnd): continue
        if gcd(m,r)==1: return True
    return False
def Yprop(v):
    L=len(v); strict=False
    for i in range(L//2):
        x,y=v[i],v[L-1-i]
        if x>y: return False
        if x<y: strict=True
    return strict
def D(w):
    n=len(w)
    for s in range(n):
        v=w[s:]+w[:s]
        if Yprop(v) or (len(v)>=1 and Yprop(v[1:])): return True
    return False
def runs(w):
    n=len(w)
    if w.count(w[0])==n: return None
    s=0
    while w[s-1]==w[s]: s+=1   # rotate to run start
    v=w[s:]+w[:s]; out=[]; k=0
    while k<n:
        j=k
        while j<n and v[j]==v[k]: j+=1
        out.append(j-k); k=j
    return out
def RG_classes(l,Bnd):
    K=len(l)
    for c in range(0,K,2):
        E=[l[i]-l[(c-i)%K] for i in range(K)]
        mm=sum(1 for e in E if e>0)
        if Bnd is not None:
            if (mm<=Bnd or K-2*mm<=Bnd) and gcd(mm,K-2*mm)==1: return True
        else:
            from collections import Counter
            cl=Counter(E)
            if any(gcd(v,K)==1 for v in cl.values()) or gcd(mm,K)==1: return True
    return False
def RGB(w):
    l=runs(w); return l is not None and RG_classes(l,B)
def RG(w):
    l=runs(w); return l is not None and RG_classes(l,None)
def RD(w):
    l=runs(w)
    if l is None: return False
    K=len(l)
    for c in range(0,K,2):
        f1=c//2
        H=[(f1+t)%K for t in range(1,K//2)]
        for sgn in (1,-1):
            ok=True; st=False
            for i in H:
                d=sgn*(l[i]-l[(c-i)%K])
                if d>0: ok=False;break
                if d<0: st=True
            if ok and st: return True
    return False
def GB(w): return G(w,B)
def necklaces(n):
    seen=set()
    for x in range(2**n):
        w=format(x,'0%db'%n).replace('0','a').replace('1','b')
        r=min(w[i:]+w[:i] for i in range(n))
        if r==w: yield w
preds={'D':D,'GB':GB,'RD':RD,'RGB':RGB,'G':G,'RG':RG}
if __name__=='__main__':
    for n in map(int,sys.argv[1:]):
        miss=0; unsound={k:0 for k in preds}; gmiss=0; tot=0
        for w in necklaces(n):
            p=prim(w)
            res={k:f(w) for k,f in preds.items()}
            if not p:
                for k in preds:
                    if res[k]: unsound[k]+=1; print('UNSOUND',k,w)
                continue
            tot+=1
            if not(res['D'] or res['GB'] or res['RD'] or res['RGB']): miss+=1; 
            if not res['G']: gmiss+=1
        print(n,'primnecklaces',tot,'CFU-miss',miss,'G-miss',gmiss,'unsound',unsound,flush=True)
