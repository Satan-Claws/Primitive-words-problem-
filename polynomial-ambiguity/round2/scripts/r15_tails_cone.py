"""R15-B check 2: quadrant-then-wedge density (Lemma QW).
(A,B) independent +-1 walks (letters scaled by 2), C=0.
Phase 1 (k<=m): Q = {A<=0, B>=0, A<B}  (MS on both tapes: A<=C_U on U-region, B>=-C_V on V-region, plus G-).
Phase 2 (m<k<=T): W2 = {A<B, A<=0}  (one of the two Valley wedges, 3pi/4).
Claim: P ~ m^{-1/3} T^{-2/3}.  Also 1D: E[S_m^2; max S<=0] ~ sqrt m."""
import numpy as np
T=512; R=T+2; off=R
def run(m):
    P=np.zeros((2*R+1,2*R+1)); P[off,off]=1.0   # index [A,B]
    a=np.arange(-R,R+1)
    AA,BB=np.meshgrid(a,a,indexing='ij')
    Q=(AA<=0)&(BB>=0)&(AA<BB); W=(AA<BB)&(AA<=0)
    res={}
    for k in range(1,T+1):
        P=(np.roll(P,1,0)+np.roll(P,-1,0)); P=(np.roll(P,1,1)+np.roll(P,-1,1))/4
        P*= (Q if k<=m else W)
        if k in (T//4,T//2,T): res[k]=P.sum()
    return res
print("m   P(T=128) P(T=256) P(T=512)  m^{1/3}T^{2/3}P(T=512)")
for m in [0,4,8,16,32,64]:
    r=run(m); print(f"{m:3d} {r[128]:.3e} {r[256]:.3e} {r[512]:.3e}   {max(m,1)**(1/3)*512**(2/3)*r[512]:.3f}")
# 1D second moment under barrier
p=np.zeros(2*R+1); p[off]=1; a=np.arange(-R,R+1)
for k in range(1,T+1):
    p=(np.roll(p,1)+np.roll(p,-1))/2; p[a>0]=0
    if k in (64,128,256,512): print(f"1D m={k}: P(max<=0)*sqrt(m)={p.sum()*k**0.5:.3f}  E[S^2;surv]/sqrt(m)={(p*a**2).sum()/k**0.5:.3f}")
