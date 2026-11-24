"""r15_onesided_moment.py -- numerics for Thm PR1s (r15_onesided.md), the conditional-moment step.
Walk (A,B) in doubled units, steps (+-1,+-1) iid uniform; s=(B-A)/2 is the lazy walk {-1,0,0,+1}.
W1 = {A<B, B>=-2C} (opening 3pi/4).  H = {A<B} (half-plane).
 p(m)   = P(tau_W1 > m)                       predicted ~ m^-2/3
 M1(m)  = E[(s_m+1) ; tau_W1 > m]             predicted ~ m^-1/6 (proof gives m^-1/6 sqrt(log m))
 J(m,K) = P(tau_W1 > m, tau_H > K)            predicted <= c m^-1/6 K^-1/2 (sqrt log)
Prints local exponents and the normalised quantities M1*m^(1/6), J*m^(1/6)*K^(1/2)."""
import numpy as np, sys, math
M = int(sys.argv[1]) if len(sys.argv) > 1 else 512
C = 0
def step(g):
    h = np.zeros_like(g)
    for da in (1, -1):
        for db in (1, -1):
            h += 0.25*np.roll(np.roll(g, da, 0), db, 1)
    return h
Kmax = 8*M
R = Kmax + 2*C + 4; off = R; S = 2*R + 1
A = np.arange(S)[:, None] - off; B = np.arange(S)[None, :] - off
mask_h = (A < B); mask_w = mask_h & (B >= -2*C)
sval = (B - A)/2
g = np.zeros((S, S)); g[off, off] = 1.0
res = {}
for m in range(1, M + 1):
    g = step(g)*mask_w
    if m & (m-1) == 0 and m >= 8:
        p = g.sum(); m1 = (g*(sval+1)).sum()
        J = {}
        h = g.copy(); k = m
        while k < 8*m:
            h = step(h)*mask_h; k += 1
            if k in (2*m, 4*m, 8*m): J[k//m] = h.sum()
        res[m] = (p, m1, J)
        print(f"m={m:4d} p={p:.4e} p*m^(2/3)={p*m**(2/3):.4f} M1={m1:.4e} M1*m^(1/6)={m1*m**(1/6):.4f} "
              + " ".join(f"J(K={r}m)*m^(1/6)*K^(1/2)={J[r]*m**(1/6)*(r*m)**0.5:.4f}" for r in sorted(J)), flush=True)
ms = sorted(res)
for a, b in zip(ms, ms[1:]):
    print(f"exponents m={b}: p {math.log(res[b][0]/res[a][0],2):+.3f}  M1 {math.log(res[b][1]/res[a][1],2):+.3f}  "
          f"J(K=4m) {math.log(res[b][2][4]/res[a][2][4],2):+.3f} (pred -1/6-1/2=-0.667)")
