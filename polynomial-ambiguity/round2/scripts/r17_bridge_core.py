# r17_bridge: exact densities of G- and of its padding-stable core G- ∩ Q_n(C) (even n).
# A(k)=#a(pre_k)-k/2-ish: use integer walks a=+1,b=-1 on first half (A) and reversed last half (B).
# G-: A(k) < B(k) for 1<=k<=n/2 (A(k)-B(k) = 2*d_k).  Core: additionally A(k) <= C, B(k) >= -C (C in half-units*2).
import numpy as np, sys
def dens(n, C=None):
    m = n//2; off = m+1; S = 2*m+3
    P = np.zeros((S,S)); P[off,off] = 1.0
    for k in range(1, m+1):
        Q = np.zeros_like(P)
        for da in (1,-1):
            for db in (1,-1):
                Q += 0.25*np.roll(np.roll(P, da, 0), db, 1)
        a = np.arange(S)[:,None]-off; b = np.arange(S)[None,:]-off
        ok = a < b
        if C is not None: ok &= (a <= C) & (b >= -C)
        P = Q*ok
    return P.sum()
for n in [32,64,128,256,512]:
    g = dens(n); c = dens(n, 2)
    print(n, "sqrt(n)*dens(G-)=%.3f"%(g*n**0.5), "n*dens(core,C=2)=%.3f"%(c*n), "core/G-=%.4f"%(c/g), "sqrt(n)*core/G-=%.3f"%(c/g*n**0.5))
