"""r13_padding_cone.py -- numerics for Thm PR2 (r13_padding.md).
(1) Zipped walk (A,B), A=P(k), B=P(n)-P(n-k), steps (+-1/2,+-1/2) iid uniform (k <= n/2).
    p_half(m)  = P(A<B for k=1..m)                 (G- event, half-plane: ~ m^-1/2)
    p_W1(m,C)  = P(A<B and B>=-C for k=1..m)       (wedge 3pi/4: predicted ~ m^-2/3)
    p_W2(m,C)  = P(A<B and A<= C for k=1..m)       (mirror wedge; equal to p_W1 by symmetry A->-B)
    Local exponents log-ratio at m vs m/2.
(2) Exact check, n<=N: |G-_n cap Valley_C| / |G-_n| -> 0, Valley_C = {max P <= max(0,P(n)) + C}.
Units: doubled walk (integers)."""
import numpy as np, sys, itertools, math
M = int(sys.argv[1]) if len(sys.argv) > 1 else 1024
def run(M, C):
    R = M + 2*C + 4; off = R
    S = 2*R + 1
    def init():
        g = np.zeros((S, S)); g[off, off] = 1.0; return g
    gh, g1 = init(), init()
    A = np.arange(S)[:, None] - off; B = np.arange(S)[None, :] - off
    mask_h = (A < B); mask_1 = (A < B) & (B >= -2*C)
    out = {}
    for m in range(1, M + 1):
        new = []
        for g, mk in ((gh, mask_h), (g1, mask_1)):
            h = np.zeros_like(g)
            for da in (1, -1):
                for db in (1, -1):
                    h += 0.25 * np.roll(np.roll(g, da, 0), db, 1)
            new.append(h * mk)
        gh, g1 = new
        if m & (m - 1) == 0 and m >= 8: out[m] = (gh.sum(), g1.sum())
    return out
for C in (0, 2):
    out = run(M, C); ms = sorted(out)
    print(f"C={C}")
    for a, b in zip(ms, ms[1:]):
        ph0, p10 = out[a]; ph1, p11 = out[b]
        print(f"  m={b:5d} p_half={ph1:.3e} exp={math.log(ph1/ph0)/math.log(2):+.3f}  p_W1={p11:.3e} exp={math.log(p11/p10)/math.log(2):+.3f}  ratio W1/half={p11/ph1:.3f}")
# (2) exact small-n check of Valley cap G- fraction
N = int(sys.argv[2]) if len(sys.argv) > 2 else 22
print("exact: n, |G-_n|, |G- cap Valley_0|, |G- cap Valley_2|")
for n in range(4, N + 1, 2):
    g = v0 = v2 = 0
    for bits in itertools.product((1, -1), repeat=n):  # 1=a
        P = [0]
        for x in bits: P.append(P[-1] + x)
        if any(P[k] + P[n-k] >= P[n] for k in range(1, n//2 + 1)): continue
        g += 1; mx = max(P); t = max(0, P[n])
        v0 += mx <= t; v2 += mx <= t + 4
    print(f"  {n:3d} {g:8d} {v0:8d} {v2:8d}  frac0={v0/g:.3f} frac2={v2/g:.3f}")
