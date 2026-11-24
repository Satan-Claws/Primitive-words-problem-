"""tile_pgen: min-ply tiling of the omega-simplex by NC-tree validity cones for general P (default 4).
Same model as tile_p3exact.py (rooted at point 0, subtrees = linear intervals, edge valid iff
sgn<fold(mu|I),omega> = sgn mu_top). Chambers of {f_I = 0} inside the open simplex are enumerated incrementally
by LP (HiGHS; max slack delta, floating point -> [computational]); K_T = set of chambers; min max-ply subfamily
by CP-SAT. Usage: .venv/bin/python tile_pgen.py [trials=5] [m=9] [P=4]"""
import sys, math, random
import numpy as np
from scipy.optimize import linprog
from ortools.sat.python import cp_model
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from tile_p3exact import all_trees

def gen_instance(m, P, rng):
    while True:
        res = [rng.randrange(P) for _ in range(m)]
        if min(res.count(r) for r in range(P)) < 2: continue
        mu = [0] * m; bad = False
        for r in range(P):
            idx = [i for i in range(m) if res[i] == r]
            vals = [rng.choice([-1, 1]) * rng.randint(1, 9) for _ in idx[:-1]]
            if sum(vals) == 0: bad = True; break
            for i, v in zip(idx, vals + [-sum(vals)]): mu[i] = v
        if bad: continue
        if all(sum(mu[l:r + 1]) != 0 for l in range(1, m) for r in range(l, m)): return res, mu

def fold(res, mu, l, r, P):
    f = np.zeros(P)
    for i in range(l, r + 1): f[res[i]] += mu[i]
    return f

def interior(H, s, P):
    """max delta s.t. s_i <H_i,w> >= delta, w_j >= delta, sum w = 1. returns (delta, w)."""
    k = len(s)
    A = []; b = []
    for i in range(k): A.append(np.r_[-s[i] * H[i], 1.0]); b.append(0.0)
    for j in range(P): e = np.zeros(P + 1); e[j] = -1; e[P] = 1; A.append(e); b.append(0.0)
    c = np.zeros(P + 1); c[P] = -1
    r = linprog(c, A_ub=np.array(A), b_ub=b, A_eq=[np.r_[np.ones(P), 0]], b_eq=[1], bounds=[(None, None)] * P + [(None, 1)], method='highs')
    if r.status != 0: return -1, None
    return -r.fun, r.x[:P]

def chambers(H, P, tol=1e-9):
    ch = [((), None)]
    for i in range(len(H)):
        new = []
        for s, w in ch:
            for t in (1, -1):
                d, ww = interior(H[:i + 1], list(s) + [t], P)
                if d > tol: new.append((tuple(s) + (t,), ww))
        ch = new
    return ch

def solve_instance(res, mu, P):
    trees = all_trees(res, mu)
    ivs = sorted({iv for T in trees for (iv, s) in T})
    F = {iv: fold(res, mu, *iv, P) for iv in ivs}
    # distinct hyperplanes up to positive/negative scaling; drop forms of constant sign on the orthant
    H = []; key = {}
    for iv, f in F.items():
        if (f >= 0).all() or (f <= 0).all(): key[iv] = None; continue
        g = f / np.abs(f).max()
        for j, h in enumerate(H):
            if np.allclose(g, h): key[iv] = (j, 1); break
            if np.allclose(g, -h): key[iv] = (j, -1); break
        else: H.append(g); key[iv] = (len(H) - 1, 1)
    ch = chambers(H, P)
    def sgn(iv, c):
        if key[iv] is None: return 1 if F[iv].sum() > 0 else -1
        j, fl = key[iv]; return fl * ch[c][0][j]
    masks = set()
    for T in trees:
        S = frozenset(c for c in range(len(ch)) if all(sgn(iv, c) == s for (iv, s) in T))
        if S: masks.add(S)
    cones = list(masks)
    assert len(set().union(*cones)) == len(ch), 'uncovered chamber'
    for z in range(1, 8):
        mdl = cp_model.CpModel(); x = [mdl.NewBoolVar('') for _ in cones]
        for c in range(len(ch)):
            inc = [x[i] for i, S in enumerate(cones) if c in S]
            mdl.Add(sum(inc) >= 1); mdl.Add(sum(inc) <= z)
        sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = 300; sv.parameters.num_workers = 8
        st = sv.Solve(mdl)
        if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            return dict(trees=len(trees), cones=len(cones), hyper=len(H), chambers=len(ch), single_chamber_cones=sum(len(S) == 1 for S in cones), minply=z, used=sum(sv.Value(v) for v in x))
        if st != cp_model.INFEASIBLE: return dict(trees=len(trees), cones=len(cones), hyper=len(H), chambers=len(ch), minply=f'timeout>{z-1}')

if __name__ == '__main__':
    trials = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    m = int(sys.argv[2]) if len(sys.argv) > 2 else 9
    P = int(sys.argv[3]) if len(sys.argv) > 3 else 4
    rng = random.Random(777 + 31 * m + P)
    for t in range(trials):
        res, mu = gen_instance(m, P, rng)
        print(t, 'res', ''.join(map(str, res)), 'mu', mu, solve_instance(res, mu, P), flush=True)
