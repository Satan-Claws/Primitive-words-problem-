"""audit_r14_wedge.py -- independent exact DP for Lemma K (r13_padding.md).
Zipped walk (A,B) in doubled units, steps (+-1,+-1) uniform. Rotated coords s=(B-A)/2, t=(A+B)/2: each step
changes exactly one of s,t by +-1 => simple random walk on Z^2 (isotropic, uncorrelated).
Events (k=1..m): half: s>0 ; W1: s>0 and B>=-2C i.e. s+t>=-2C ; W2 (mirror) : s>0 and A<=2C i.e. t-s<=2C.
Also the TRUE event 'W1 or W2' is not needed (union bound). Prints survival + local exponents m vs m/2,
and the fitted constant m^{2/3} p_W1 (should stabilise if exponent is exactly 2/3)."""
import numpy as np, sys, math
M = int(sys.argv[1]) if len(sys.argv) > 1 else 2048
for C in (0, 3):
    R = M + 2*C + 2; S = 2*R + 1
    s = np.arange(S)[:, None] - R; t = np.arange(S)[None, :] - R
    mh = (s > 0); m1 = (s > 0) & (s + t >= -2*C); m2 = (s > 0) & (t - s <= 2*C)
    gs = []
    for mk in (mh, m1, m2):
        g = np.zeros((S, S)); g[R, R] = 1.0; gs.append([g, mk])
    res = {}
    for m in range(1, M + 1):
        for e in gs:
            g = e[0]; h = np.zeros_like(g)
            h[1:, :] += g[:-1, :]; h[:-1, :] += g[1:, :]; h[:, 1:] += g[:, :-1]; h[:, :-1] += g[:, 1:]
            e[0] = 0.25 * h * e[1]
        if m >= 16 and m & (m-1) == 0: res[m] = [e[0].sum() for e in gs]
    print(f"C={C}")
    ks = sorted(res)
    for a, b in zip(ks, ks[1:]):
        x0, x1 = res[a], res[b]
        ex = [math.log(x1[i]/x0[i])/math.log(2) for i in range(3)]
        print(f" m={b:5d} half={x1[0]:.4e}({ex[0]:+.4f}) W1={x1[1]:.4e}({ex[1]:+.4f}) W2={x1[2]:.4e}({ex[2]:+.4f}) m^(2/3)W1={x1[1]*b**(2/3):.4f}")
