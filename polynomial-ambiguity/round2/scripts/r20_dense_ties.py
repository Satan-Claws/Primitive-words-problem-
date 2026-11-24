"""r20_dense_ties.py -- Monte Carlo for the Extremal-Tie corollary (r20_dense.md, Cor ET).
For random cyclic words of length n, m = longest cyclic run of letter c.
 surv(g) = P(longest c-run unique  and  #other c-runs of length >= m-g  <= 1)  [UMR_cyc survivors]
 lsurv(g)= P(#other c-runs of length >= m-g <= 1)  (no uniqueness; Lyndon/LeadMax survivors)
Theorem ET: Rot(L) is contained in the survivors (up to m < M0), for any CF L inside UMR_cyc / Lyndon / LeadMax.
"""
import numpy as np, sys
rng = np.random.default_rng(20)
def runs_of(w, c):
    n = len(w)
    if w.all() == c or (w == c).all(): return None
    # rotate so w[0] != c
    k = int(np.argmax(w != c)); w = np.roll(w, -k)
    x = np.concatenate(([0], (w == c).astype(np.int8), [0]))
    d = np.diff(x); s = np.flatnonzero(d == 1); e = np.flatnonzero(d == -1)
    return np.sort(e - s)[::-1]
G = [1, 2, 3, 4, 6]
print("n  samples  P(UMR)  surv(g) for g=" + str(G) + "  | lsurv(g)")
for n in [256, 1024, 4096, 16384, 65536]:
    S = 3000 if n <= 4096 else 1000
    umr = 0; surv = np.zeros(len(G)); ls = np.zeros(len(G))
    for _ in range(S):
        w = rng.integers(0, 2, n).astype(np.int8)
        r = runs_of(w, 1)
        if r is None or len(r) == 0: continue
        m = r[0]; uniq = len(r) == 1 or r[1] < m
        umr += uniq
        for i, g in enumerate(G):
            k = int((r[1:] >= m - g).sum())
            ls[i] += (k <= 1); surv[i] += (uniq and k <= 1)
    print(n, S, round(umr / S, 3), [round(v / S, 3) for v in surv], "|", [round(v / S, 3) for v in ls])
