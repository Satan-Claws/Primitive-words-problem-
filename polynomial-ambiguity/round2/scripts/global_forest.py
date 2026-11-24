"""global_forest: Theorem G1 of R2/global.md (slack-transport forests tile {x in N^S : mu(x) >= 1} with ply 1).

Instance: m points on a line (positions y_0<...<y_{m-1}, cyclic order irrelevant for crossing), signs mu in {+-1}^m.
LP (per facet):  vertices q with mu_q = -1 :  sum_p f_pq        = x_q
                 vertices p with mu_p = +1 :  sum_q f_pq + r_p  = x_p      (r_p = root slack, ring e_p)
variables f_pq >= 0 (ring e_p+e_q), r_p >= 0 (ring e_p).  Cost h(|y_p-y_q|), h strictly concave increasing,
plus a generic perturbation; root slacks get tiny generic costs.
A basis = m columns forming a rooted spanning forest (each component exactly one root, at a + vertex).
Exhaustive check:
  (i)   enumerate ALL bases, keep the c-dual-feasible ones (reduced costs >= 0) -> these are the cells;
  (ii)  every dual-feasible basis is non-crossing (laminar) and unimodular (|det| = 1);
  (iii) half-open rule with eta > 0 coordinatewise, mu(eta) < 0: for EVERY lattice point x in [0,B]^m,
        #cells containing x (x+eps*eta in open cone) == 1 if mu(x) >= 1, == 0 otherwise.
        Cell membership: q = B^{-1}x, q' = B^{-1}eta; x in cell iff for all v: q_v > 0 or (q_v == 0 and q'_v > 0).
        Integer points of the cell = c + N V with c = sum of v with q'_v < 0  (offsets in {0,1}).
No near-U condition anywhere: points with mu(x) >> max_p x_p (far from U) are included.
Usage: .venv/bin/python global_forest.py [m=6] [B=3] [trials=3]
"""
import sys, itertools, random
import numpy as np
from fractions import Fraction as Fr


def run(m, B, seed):
    rng = random.Random(seed)
    while True:
        mu = [rng.choice([1, -1]) for _ in range(m)]
        if 0 < mu.count(1) < m: break
    y = sorted(rng.sample(range(1, 4 * m), m))
    plus = [i for i in range(m) if mu[i] == 1]; minus = [i for i in range(m) if mu[i] == -1]
    cols, cost, kind = [], [], []
    for p in plus:
        for q in minus:
            v = [0] * m; v[p] = 1; v[q] = 1
            cols.append(v); cost.append(abs(y[p] - y[q]) ** 0.5 + 1e-7 * rng.random()); kind.append(('e', p, q))
    for p in plus:
        v = [0] * m; v[p] = 1
        cols.append(v); cost.append(1e-4 * rng.random()); kind.append(('r', p))
    A = np.array(cols, dtype=float).T            # m x ncols
    c = np.array(cost)
    cells = []
    nb = 0
    for S in itertools.combinations(range(len(cols)), m):
        AB = A[:, S]
        if abs(np.linalg.det(AB)) < 0.5: continue
        nb += 1
        yd = np.linalg.solve(AB.T, c[list(S)])   # dual
        red = c - A.T @ yd
        if red.min() < -1e-12: continue
        cells.append(S)
    # (ii) NC + unimodular
    def crosses(a, b):
        (i, j), (k, l) = sorted(a), sorted(b)
        return (i < k < j < l) or (k < i < l < j)
    nc_ok = True; uni_ok = True
    for S in cells:
        es = [(kind[s][1], kind[s][2]) for s in S if kind[s][0] == 'e']
        if any(crosses(a, b) for a, b in itertools.combinations(es, 2) if len({*a, *b}) == 4): nc_ok = False
        if round(abs(np.linalg.det(A[:, S]))) != 1: uni_ok = False
    # (iii) ply on the box
    eta = np.array([1.0 + rng.random() if mu[i] == 1 else 3.0 * m + rng.random() for i in range(m)])
    assert eta @ np.array(mu) < 0
    inv = [np.linalg.inv(A[:, S]) for S in cells]
    qe = [Mi @ eta for Mi in inv]
    bad = 0; npts = 0; far = 0
    for x in itertools.product(range(B + 1), repeat=m):
        xv = np.array(x, dtype=float); tau = int(np.dot(mu, x))
        cnt = 0
        for Mi, qq in zip(inv, qe):
            q = Mi @ xv
            if all((q[v] > 1e-9) or (abs(q[v]) <= 1e-9 and qq[v] > 0) for v in range(m)): cnt += 1
        want = 1 if tau >= 1 else 0
        if cnt != want: bad += 1
        npts += 1
        if tau >= 1 and tau > max(x[p] for p in plus): far += 1
    return dict(mu=mu, y=y, bases=nb, cells=len(cells), NC=nc_ok, unimod=uni_ok, points=npts,
                far_from_U_points=far, ply_violations=bad)


if __name__ == '__main__':
    m = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    B = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    T = int(sys.argv[3]) if len(sys.argv) > 3 else 3
    for s in range(T):
        print(run(m, B, s))
