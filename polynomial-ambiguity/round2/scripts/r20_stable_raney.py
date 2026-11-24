"""r20: explicit failure fragment H_R = cyclic closure of Raney words.
(a) exhaustive n<=16: L_R={w: 1<=|D(w)|<=R, gcd(|D|,n)=1} is inside Q; amb (Theorem C) = #cyclic shifts with all
    partial sums of sign(D) positive = |D| (cycle lemma); and every Dyck-factor substitution keeps D (so stays in Q).
(b) exact fold DP (weights (1,-1),(1,-2),(2,-1); cycle lemma amb<=R each): fraction of G^- covered by L_R, times sqrt(n) (expect ~ const*R)."""
from math import gcd
from itertools import product
def D(w): return sum(1 if c=='a' else -1 for c in w)
def prim(w):
    n=len(w); return all(not(n%p==0 and w==w[:p]*(n//p)) for p in range(1,n))
def inGm(w):
    n=len(w); P=[0]
    for c in w: P.append(P[-1]+(1 if c=='a' else -1))
    return all(P[k]+P[n-k]-P[n]<0 for k in range(1,n//2+1))
def amb(w):
    d=D(w); s=1 if d>0 else -1; n=len(w); cnt=0
    for j in range(n):
        v=w[j:]+w[:j]; p=0; ok=True
        for c in v:
            p+=s*(1 if c=='a' else -1)
            if p<=0: ok=False;break
        cnt+=ok
    return cnt
R=3; bad=0; ambbad=0; tot=0
for n in range(1,17):
    for t in product('ab',repeat=n):
        w=''.join(t); d=abs(D(w))
        if 1<=d<=R and gcd(d,n)==1:
            tot+=1
            if not prim(w): bad+=1
            if amb(w)!=d: ambbad+=1
print(f"(a) n<=16, R={R}: |L_R|={tot}, non-primitive={bad}, amb!=|D|: {ambbad}")
# check G^- words exhaustively are primitive & fraction for small n
def dp(n,R):
    # fold DP over pairs; state (d,sigma)
    from collections import defaultdict
    st={(0,0):1}
    for k in range(n//2):
        ns=defaultdict(int)
        for (d,s),c in st.items():
            for dd,ds in ((-2,0),(2,0),(0,2),(0,-2)):
                if d+dd<0: ns[(d+dd,s+ds)]+=c
        st=ns
    tot=0; cov=0
    mids=[1,-1] if n%2 else [0]
    for (d,s),c in st.items():
        for m in mids:
            tot+=c; Dt=s+m; A=(n+Dt)//2; B=n-A
            if any(1<=abs(r)<=R and gcd(abs(r),n)==1 for r in (A-B,A-2*B,2*A-B)): cov+=c
    return tot,cov
for n in (63,64,255,256,1023,1024):
    for R in (1,3,9):
        t,c=dp(n,R)
        print(f"(b) n={n:5d} R={R}: sqrt(n)*dens(G-)={t/2**n*n**.5:.3f}  |L_R∩G-|/|G-|={c/t:.4f}  *sqrt(n)={c/t*n**.5:.2f}")
