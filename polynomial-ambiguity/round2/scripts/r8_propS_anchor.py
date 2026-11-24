"""r8_propS_anchor.py
(1) exact |G^-_n|/2^n via fold DP (threshold check).
(2) end-anchored single-spine rectangle: for g(k)=k/2+lam*sqrt(k),
    PY(m) = P(y in Sigma^m : b.y in G^- and R_y(k) > g(k), k<=m/2)       [x0 = empty, c = b]
    PX(m) = P(x in Sigma^m : x.a in G^- and F_x(k) <= g(k), k<=m/2)      [y0 = empty, c = a]
    report exponent of max_lam PX*PY in m (Lemma R alone gives -1)."""
import numpy as np, math, sys
def gminus(N):
    p=np.zeros(2*N+3); o=N+1; p[o]=1.0; out=[]
    for k in range(1,N+1):
        q=0.25*np.roll(p,1)+0.5*p+0.25*np.roll(p,-1); q[o:]=0; p=q; out.append(p.sum())
    return out
def side(m,lam,which):
    K=m//2; Kp=(m+1)//2; T=max(K,Kp)
    P=np.zeros((T+2,T+2)); P[0,0]=1.0   # P[F,R]: F=#a prefix len k, R=#a suffix len k
    for k in range(1,T+1):
        Q=np.zeros_like(P)
        for fa in (0,1):
            for ra in (0,1):
                Q[fa:,ra:]+=0.25*P[:P.shape[0]-fa,:P.shape[1]-ra]
        F=np.arange(T+2)[:,None]; R=np.arange(T+2)[None,:]
        g=k/2+lam*math.sqrt(k)
        if which=='Y':
            # b.y in G^-: prefix_k(b y)=F_y(k-1) < R_y(k). Use F(k)-a(y_{k-1}) ; approximate safely by F(k)-1 <= F(k-1): weaker => upper bound
            ok=np.ones_like(Q,bool)
            if k<=Kp: ok&=(F-1<R)
            if k<=K: ok&=(R>g)
        else:
            # x.a in G^-: F_x(k) < 1+#a(suf_{k-1} x) >= R(k)-1+1 ... weaker: F < R+1
            ok=np.ones_like(Q,bool)
            if k<=Kp: ok&=(F<R+1)
            if k<=K: ok&=(F<=g)
        P=Q*ok
    return P.sum()
if __name__=="__main__":
    g=gminus(2000)
    for N in (125,250,500,1000,2000): print("G- N=%d P=%.5f P*sqrt(N)=%.4f"%(N,g[N-1],g[N-1]*math.sqrt(N)))
    lams=[-1,-0.5,-0.25,0,0.25,0.5,1]
    ms=[50,100,200,400]
    best=[]
    for m in ms:
        vals=[side(m,l,'X')*side(m,l,'Y') for l in lams]
        best.append(max(vals)); print("m=%d "%m+" ".join("%.2e"%v for v in vals))
    for i in range(1,len(ms)):
        print("exp m=%d: %.3f"%(ms[i],math.log(best[i]/best[i-1])/math.log(2)))
