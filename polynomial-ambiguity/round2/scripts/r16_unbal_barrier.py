"""R16-A: test the barrier product bound used by the separation reduction.
For the simple +-1 walk S (T steps) and a deterministic barrier g, compute exactly
  F(g) = P(S_k <= g(k) for 1<=k<=T),  Fbar(g) = P(S_k >= g(k) - c for 1<=k<=T)
and compare  sup_g F(g)*Fbar(g)  with  F(c/2)^2 ~ (c+1)^2/T  (Gaussian log-concavity predicts <= ).
"""
import numpy as np, math
rng = np.random.default_rng(1)

def surv(T, lo, hi):
    off = T + 2; p = np.zeros(2*T+5); p[off] = 1.0
    for k in range(1, T+1):
        q = np.zeros_like(p); q[1:] += 0.5*p[:-1]; q[:-1] += 0.5*p[1:]
        xs = np.arange(len(p)) - off
        q[(xs < lo[k]) | (xs > hi[k])] = 0.0; p = q
    return p.sum()

def prod(T, g, c):
    inf = 10**6
    F = surv(T, [-inf]*(T+1), [math.floor(g[k]) for k in range(T+1)])
    Fb = surv(T, [math.ceil(g[k]-c) for k in range(T+1)], [inf]*(T+1))
    return F*Fb

for T in (100, 400, 1600):
    c = 0
    base = prod(T, [0.0]*(T+1), c)
    best = (base, 'g=0')
    fams = {}
    for a in (-1.0, -0.5, -0.25, 0.25, 0.5, 1.0):
        fams['%.2f*sqrt k' % a] = [a*math.sqrt(k) for k in range(T+1)]
    for a in (-0.05, 0.05):
        fams['%.2f*k' % a] = [a*k for k in range(T+1)]
    for i in range(4):  # random-walk-shaped barriers (frozen samples)
        w = np.concatenate([[0], np.cumsum(rng.choice([-1, 1], T))]) * 0.5
        fams['rw%d' % i] = list(w)
    for i in range(3):  # sawtooth
        fams['saw%d' % i] = [((k % (10*(i+1))) - 5*(i+1)) * 0.3 for k in range(T+1)]
    for name, g in fams.items():
        v = prod(T, g, c)
        if v > best[0]: best = (v, name)
    print(f"T={T}: F(0)*Fbar(0)*T={base*T:.4f}  max ratio over {len(fams)+1} barriers = {best[0]/base:.4f} ({best[1]})")
