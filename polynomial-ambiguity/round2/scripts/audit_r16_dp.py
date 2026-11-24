"""audit_r16: independent exact DPs for Lemma CM / J (r15_onesided) and Lemma QW (r15_tails).
Walk (a,b) = (2A,2B), steps (+-1,+-1) uniform, start (0,0), constraints for k>=1. C=0."""
import numpy as np
def step(P):
    Q = np.zeros_like(P)
    Q[1:,1:]+=P[:-1,:-1]; Q[1:,:-1]+=P[:-1,1:]; Q[:-1,1:]+=P[1:,:-1]; Q[:-1,:-1]+=P[1:,1:]
    return Q/4
def run(T, masks):
    """masks: function k -> boolean array of allowed states at time k. returns list of masses."""
    R=T+2; n=2*R+1; P=np.zeros((n,n)); P[R,R]=1.0; out=[]
    for k in range(1,T+1):
        P=step(P); P*=masks(k); out.append(P.copy())
    return out, R
def grids(T):
    R=T+2; x=np.arange(-R,R+1); a,b=np.meshgrid(x,x,indexing='ij'); return a,b
# ---- Lemma CM and J ----
print("Lemma CM/J: M1=E[(s_m+1);tau_W1>m], s=B-A (lazy units), J(m,4m)")
for m in [16,32,64,128,256]:
    T=4*m; a,b=grids(T); W1=(a<b)&(b>=0); H=(a<b)
    out,R=run(T, lambda k: W1 if k<=m else H)
    Pm=out[m-1]; s=(b-a)/2
    M1=(Pm*(s+1)).sum(); surv=Pm.sum(); J=out[-1].sum()
    print(f"m={m:4d} P*m^(2/3)={surv*m**(2/3):.4f} M1*m^(1/6)={M1*m**(1/6):.4f} E[s;tau>m]*m^(1/6)={(Pm*s).sum()*m**(1/6):.4f} J*m^(1/6)*(4m)^(1/2)={J*m**(1/6)*(4*m)**.5:.4f}")
# ---- Lemma QW ----
print("Lemma QW: P(Q for k<=m, then H and (b>=0 all k or a<=0 all k) for k<=T)")
for T in [256,512]:
    a,b=grids(T); H=(a<b); Qd=(a<=0)&(b>=0)
    def mk(extra): return lambda k: (Qd if k<=m else True)&H&extra
    for m in [4,8,16,32,64]:
        p1=run(T,mk(b>=0))[0][-1].sum(); p2=run(T,mk(a<=0))[0][-1].sum(); p12=run(T,mk((a<=0)&(b>=0)))[0][-1].sum()
        p=p1+p2-p12
        print(f"T={T} m={m:3d} P={p:.3e} m^(1/3)T^(2/3)P={p*m**(1/3)*T**(2/3):.4f}")
