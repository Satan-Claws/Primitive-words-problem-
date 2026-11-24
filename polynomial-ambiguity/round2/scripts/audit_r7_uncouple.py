# Independent brute-force audit of r7_uncouple U1-U3 (n <= NMAX). Words as int bitmasks (bit i = 1 <=> letter a at position i).
import sys
from math import comb
NMAX=int(sys.argv[1]) if len(sys.argv)>1 else 18
def walk(w,n):
    h=[0]*(n+1)
    for i in range(n): h[i+1]=h[i]+(1 if (w>>i)&1 else -1)
    return h
def rot(w,n,i): return ((w>>i)|(w<<(n-i)))&((1<<n)-1)
def root(w,n):
    for d in range(1,n+1):
        if n%d==0 and rot(w,n,d)==w: return d
def inP(h,n): return n>0 and all(h[j]<h[n] for j in range(n))       # every nonempty suffix a-heavy
def inDbP(h,n):   # exists s: h<=0 on [0,s], h(s)=0, suffix from s nonempty and in P
    for s in range(n):
        if h[s]>0: return False
        if h[s]==0 and all(h[j]<h[n] for j in range(s,n)): return True
    return False
def inLA(h,n):    # split def of r6 Lemma SA: x b-first Dyck (h<=0, h(s)=0), y nonempty, all suffixes of y a-heavy, |x|>=|y|
    for s in range(n):
        if h[s]>0: return False
        if h[s]==0 and s>=n-s and all(h[j]<h[n] for j in range(s,n)): return True
    return False
def half(h,n): return all(h[j]<=0 for j in range((n+1)//2+1))
def blocks(w,n,h):  # parse (D_b a)^+ : cut at first passages to new maxima
    out=[];start=0;m=0
    for i in range(n):
        if h[i+1]>m: out.append((w>>start)&((1<<(i-start))-1) | ((i-start)<<40)); m=h[i+1]; start=i+1
    return out,start==n
err={}
def bad(k): err[k]=err.get(k,0)+1
for n in range(1,NMAX+1):
    cntP=0; classesA=set(); classesB=set()
    for w in range(1<<n):
        h=walk(w,n); p=inP(h,n); r=root(w,n); prim=(r==n)
        cntP+=p
        if inDbP(h,n)!=p: bad('U1 DbP!=P')
        bl,ok=blocks(w,n,h)
        if p and not (ok and len(bl)==h[n]): bad('U3 parse')
        if not p and ok and bl and h[n]>=1 and all(h[j]<h[n] for j in range(n)): bad('U3 parse2')
        if not prim:
            u=w&((1<<r)-1); hu=walk(u,r)
            if p!=inP(hu,r): bad('U1 u^p in P <=> u in P')
        if p:
            H=len(bl)
            bprim=all(bl!=bl[d:]+bl[:d] for d in range(1,H) if H%d==0)
            if bprim!=prim: bad('U3 PcapQ=prim blockseq')
            # rotations of w in P = block-boundary positions
            pos=[0];
            for i in range(1,n+1):
                if h[i]>max(h[:i]) : pos.append(i)
            pos=set(pos[:-1])
            rp={i for i in range(n) if inP(walk(rot(w,n,i),n),n)}
            if rp!=pos or len(rp)!=H: bad('U3 rotations in P')
        la=inLA(h,n); lb=h[n]>=1 and half(h,n)
        if la!=(p and half(h,n)): bad('U2(i)')
        if lb and not prim: bad('U2(ii) L_B not in Q')
        if la and not lb: bad('LA not sub LB')
        if la or lb:
            c=min(rot(w,n,i) for i in range(n))
            if la: classesA.add(c)
            if lb: classesB.add(c)
    if classesA!=classesB: bad('U2(iii) Rot')
    if cntP!=comb(n-1,(n-1)//2): bad('|P_n|')
    print(n,cntP,len(classesA),len(classesB),flush=True)
print('errors:',err if err else 'none')
