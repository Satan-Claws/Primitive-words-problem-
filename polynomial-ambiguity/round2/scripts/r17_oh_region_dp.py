"""r17_oh_region: exact DPs.
(1) wedge W1={A<B, B>=-C}: P(survive m) * m^{2/3}  (the region of {MS+(b)} ∩ {G-} alone; 3pi/4 cone).
(2) region E_n(M) = {B>=-C for k<=T} ∩ {A<=max_{j<=M}B_j + C' for k<=T}, T=n/2  (adds back-insertion, §2):
    report T*P/ (sqrt(M) log M) and T*P at fixed M (should be bounded: exponent 1 in T).
Walks: 2A, 2B are independent simple +-1 walks (integer units)."""
import numpy as np, math
C=1; Cp=1
def wedge(mmax):
    # state (a,b) with a<b, b>=-C ; offset arrays
    W=2*mmax+3; off=mmax+1
    P=np.zeros((W,W)); P[off,off]=1.0  # start (0,0): allowed? use A<=B at k=0
    out={}
    for m in range(1,mmax+1):
        Q=np.zeros_like(P)
        for da in(-1,1):
            for db in(-1,1):
                Q+=0.25*np.roll(np.roll(P,da,0),db,1)
        a=np.arange(W)[:,None]-off; b=np.arange(W)[None,:]-off
        Q[~((a<b)&(b>=-C))]=0; P=Q
        if m in(16,64,256,1024): out[m]=P.sum()*m**(2/3)
    return out
def surv_above(T,lo,start_vals):
    # prob SRW from x stays >=lo for T steps, for x in start_vals (vector over x=lo..lo+T+..)
    pass
def ballot_table(T, H):
    # f[t][x] prob SRW from x stays >= 0 for t steps; returns f_T as array over x in 0..H
    f=np.ones(H+T+2)
    for _ in range(T):
        g=np.zeros_like(f); g[1:-1]=0.5*(f[:-2]+f[2:]); g[0]=0.5*f[1]; g[-1]=1.0; f=g
    return f
def region(T,M):
    # B: SRW from 0, stay >=-C. Track (B_M, max_{j<=M} B_j) up to time M.
    R=M+C+2
    D={ (0,0):1.0 }
    for _ in range(M):
        E={}
        for (b,h),p in D.items():
            for s in(-1,1):
                nb=b+s
                if nb< -C: continue
                k=(nb,max(h,nb)); E[k]=E.get(k,0)+0.5*p
        D=E
    fB=ballot_table(T-M, M+C+2)          # B from b stays >= -C : index b+C
    fA=ballot_table(T, M+Cp+C+2)          # A from 0 stays <= H : P = fA[H] (reflect)
    tot=0.0
    for (b,h),p in D.items(): tot+=p*fB[b+C]*fA[h+Cp]
    return tot
if __name__=="__main__":
    print("(1) wedge 3pi/4: P(tau>m)*m^(2/3):",{k:round(v,4) for k,v in wedge(1024).items()})
    for M in(4,16,64):
        row=[]
        for T in(256,1024,4096):
            P=region(T,M); row.append(f"T={T}: T*P={T*P:.3f} T*P/(sqrtM*logM)={T*P/(math.sqrt(M)*math.log(M)):.3f}")
        print(f"(2) M={M}: "+"; ".join(row))
