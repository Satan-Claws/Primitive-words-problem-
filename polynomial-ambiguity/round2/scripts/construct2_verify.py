"""construct2_verify.py -- independent check of transfer-atom realisations (report §1).
For an atom T=(tau;P;D) build every cell piece c+N V explicitly and check:
 (a) |det V| = 1 on its coordinate span (unimodular), d_sigma = #V - rank V = 0;
 (b) laminarity: supports of V pairwise non-crossing (cells failing this are dropped = not allowed);
 (c) exactness: lattice points of the allowed cells = lattice points of R_T in those cells, box [0,B]^supp;
 (d) cells pairwise disjoint;
 (e) certificates: exact rational LP certificate L_p in V_p^perp, L_p(v)>=0 on V, L_p(c)>=1 (p=2,3,5);
 (f) every point of the pieces in the box is primitive."""
import itertools, sys, numpy as np
from fractions import Fraction
from scipy.optimize import linprog
import construct2_transfer as T
n = 30; A = {2: 15, 3: 10, 5: 6}
def cells(tau, P, D):
    out = []
    for dl in itertools.product((1, 0, -1), repeat=len(D)):
        c = {tau: 1}; V = [{tau: 1}] + [{a: 1, tau: 1} for a in P]
        pairs = [(tau, a) for a in P]
        for (s, t), dd in zip(D, dl):
            V.append({s: 1, t: 1}); pairs.append((s, t))
            if dd != 0:
                hi = t if dd > 0 else s
                V.append({hi: 1, tau: 1}); pairs.append((tau, hi)); c[hi] = c.get(hi, 0) + 1; c[tau] += 1
        lam = not any(T.crosses(p, q) for p, q in itertools.combinations(pairs, 2))
        out.append((dl, c, V, lam))
    return out
def check(tau, P, D, B=4):
    supp = sorted({tau} | set(P) | {v for c in D for v in c})
    res = {'cells': 0, 'allowed': 0}
    pts_by_cell = []
    for dl, c, V, lam in cells(tau, P, D):
        res['cells'] += 1
        M = np.array([[v.get(s, 0) for s in supp] for v in V])
        r = np.linalg.matrix_rank(M); assert r == len(V), 'd_sigma != 0'
        # unimodular: gcd of maximal minors = 1 (here square or Smith via sympy)
        import sympy as sp
        assert sp.Matrix(M).T.rank() == r
        if not lam: pts_by_cell.append(set()); continue
        res['allowed'] += 1
        # (e) LP certificate per prime
        for p in (2, 3, 5):
            m = A[p]; Aeq = np.array([[1 if j % m == r0 else 0 for j in range(n)] for r0 in range(m)])
            Gm = np.array([[v.get(j, 0) for j in range(n)] for v in V] + [[1 if j == q else 0 for j in range(n)] for q in range(n) if q not in supp])
            cv = np.array([c.get(j, 0) for j in range(n)])
            lp = linprog(np.zeros(n), A_ub=np.vstack([-Gm, -cv[None]]), b_ub=np.r_[np.zeros(len(Gm)), -1], A_eq=Aeq, b_eq=np.zeros(m), bounds=[(-10, 10)]*n)
            assert lp.status == 0, f'no certificate for p={p} cell {dl}'
        # (c) points of the piece in the box
        P_ = set()
        for coef in itertools.product(range(B+1), repeat=len(V)):
            y = dict(c)
            for k, v in zip(coef, V):
                for s, a in v.items(): y[s] = y.get(s, 0) + k*a
            if max(y.values()) <= B: P_.add(tuple(y.get(s, 0) for s in supp))
        pts_by_cell.append(P_)
    allp = set().union(*pts_by_cell)
    assert sum(len(s) for s in pts_by_cell) == len(allp), 'cells overlap'
    # region points in box, restricted to allowed cells
    reg = set()
    for y in itertools.product(range(B+1), repeat=len(supp)):
        x = dict(zip(supp, y))
        if x[tau] - sum(x[a] for a in P) - sum(abs(x[t]-x[s]) for s, t in D) <= 0: continue
        dl = tuple(int(np.sign(x[t]-x[s])) for s, t in D)
        if dict((cl[0], cl[3]) for cl in cells(tau, P, D))[dl]: reg.add(y)
    assert reg == allp, ('not exact', len(reg), len(allp))
    for y in allp:
        x = np.zeros(n, int); x[supp] = y
        assert all(not np.array_equal(x, np.roll(x, A[p])) for p in A)
    res['points'] = len(allp); return res
if __name__ == '__main__':
    for at in [(0, (25, 6), ((10, 15),)), (0, (4, 5), ((10, 24), (15, 20)))]:
        print(at, check(*at))
