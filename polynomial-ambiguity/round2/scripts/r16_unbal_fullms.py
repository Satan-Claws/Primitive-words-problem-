"""R16-A: (1) bookkeeping check of Lemma MS+ (outermost flat loop transports A/B of W for ALL k<=n/2);
(2) exact density of the quadrant set Q_n(C) = {A(k)<=C, B(k)>=-C, 1<=k<=n/2} (should be ~ c_C/n)."""
import random
from fractions import Fraction
def P(w):  # centred prefix walk, a=+1/2, b=-1/2
    s=[Fraction(0)]
    for ch in w: s.append(s[-1]+(Fraction(1,2) if ch=='a' else Fraction(-1,2)))
    return s
def AB(w):
    s=P(w); n=len(w)
    return [s[k] for k in range(n+1)], [s[n]-s[n-k] for k in range(n+1)]
random.seed(0); bad=0
for trial in range(2000):
    rw=lambda m:''.join(random.choice('ab') for _ in range(m))
    p,q=rw(random.randint(0,3)),rw(random.randint(0,3))
    mid=rw(random.randint(0,30)); W=p+mid+q; n=len(W)
    al,be,vr=rw(2),rw(2),rw(3)            # rho: U-part al+x+be (x flat, long), V-part vr (fixed)
    x='ba'*(n+5)                           # U-level flat word: prefix >= -1/2
    W1=p+al+x+be+mid+vr+q                  # outermost rho, flat on U side
    A,B=AB(W); A1,B1=AB(W1); n1=len(W1); sV=sum(Fraction(1,2) if c=='a' else Fraction(-1,2) for c in vr)
    for k in range(len(q),n-len(p)+1):     # B transport: B1(k+|vr|) = B(k)+wt(vr)
        if B1[k+len(vr)]!=B[k]+sV: bad+=1
        kk=k+len(vr)
        if kk<=n1//2 and kk<=len(p+al+x) and not (A1[kk]>=-Fraction(len(p)+len(al)+1,2)): bad+=1   # A1 frozen >= -K there
    y='ab'*(n+5)                           # V-level flat word on V side: suffix excess <= 1/2
    W2=p+al+mid+vr+y+be+q; A2,B2=AB(W2); n2=len(W2); sU=P(al)[-1]
    for k in range(len(p),n-len(q)+1):     # A transport: A2(k+|al|) = A(k)+wt(al)
        if A2[k+len(al)]!=A[k]+sU: bad+=1
print("bookkeeping violations:",bad)
# exact quadrant density
for C in (0,1):
    out=[]
    for n in (64,256,1024,4096):
        m=n//2; dist={0:1.0}
        for _ in range(m):
            nd={}
            for v,pr in dist.items():
                for d in (1,-1):
                    u=v+d
                    if u<=2*C: nd[u]=nd.get(u,0)+pr/2
            dist=nd
        pa=sum(dist.values())   # A<=C (units of 1/2); B>=-C has the same law by symmetry
        out.append(f"n={n}: n*dens={n*pa*pa:.4f}")
    print(f"C={C}:", "; ".join(out))
