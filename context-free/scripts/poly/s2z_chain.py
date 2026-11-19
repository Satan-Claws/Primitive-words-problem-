"""S2Z: Q1/Q2 of poly_S2Y.md at n=36, P_N=6, p in {2,3} [computational].
Q1: for each order pi of the 6 residues, DFS over contraction sequences of NC bichromatic trees (LAM §2(b) style:
merge cyclically adjacent opposite-sign clusters x->y) requiring the absorbed cluster's fold vector F_x to be
chain-valid: s_x * (prefix sums of F_x along pi) >= 0 (all j). Final edge checked too (F_x=-F_y, s_x=-s_y). Node-limited.
Q2: for each found T(pi), count order cones O_pi' met by K_T: sampled omega, plus exact LP on a subset.
Usage: python3 s2z_chain.py [seeds=2] [nodelimit=5000] [npi=100]"""
import sys, itertools, time, numpy as np
from scipy.optimize import linprog
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from s2x_tile import make_mu, edge_forms, n, P, ps
TOL = 1e-9

def search(mu, pi, nodelimit, rng):
    supp = [i for i in range(n) if mu[i] != 0]
    perm = np.array(pi)
    F0 = {i: np.zeros(P) for i in supp}
    for i in supp: F0[i][i % P] = mu[i]
    pref = lambda f: np.cumsum(f[perm])
    om = np.array([0.0] * P); om[perm] = 2.0 ** -np.arange(P)   # lex-ish point of O_pi for move ordering
    dead = set(); cnt = [0]
    def ok(x, F): return (np.sign(mu[x]) * pref(F[x]) >= -TOL).all()
    def dfs(cur, F, edges):
        if len(cur) == 2: return edges + [tuple(sorted(cur))] if ok(cur[0], F) else None
        key = tuple(cur), tuple(np.round(np.concatenate([F[c] for c in cur]), 8))
        if key in dead or cnt[0] > nodelimit: return None
        cnt[0] += 1; L = len(cur); moves = []
        for t in range(L):
            a, b = cur[t], cur[(t + 1) % L]
            if mu[a] * mu[b] < 0:
                for x, y in ((a, b), (b, a)):
                    if ok(x, F): moves.append((abs(F[x] @ om), rng.random(), x, y))
        moves.sort()
        for _, _, x, y in moves:
            F2 = dict(F); F2[y] = F[y] + F[x]; cur2 = [c for c in cur if c != x]
            r = dfs(cur2, F2, edges + [tuple(sorted((x, y)))])
            if r is not None: return r
        dead.add(key); return None
    sys.setrecursionlimit(10000)
    return dfs(list(supp), F0, []), cnt[0]

def chain_valid(G, pi):
    return (np.cumsum(G[:, list(pi)], 1) >= -TOL).all()

def cones_met_lp(G, perms):
    m = 0
    for q in perms:  # omega_{q0}>=omega_{q1}+eps ...>=eps, G omega >= eps (scale-free)
        A = [-g for g in G]; b = [-1.0] * len(G)
        for t in range(P - 1):
            r = np.zeros(P); r[q[t + 1]] = 1; r[q[t]] = -1; A.append(r); b.append(-1.0)
        r = np.zeros(P); r[q[-1]] = -1; A.append(r); b.append(-1.0)
        if linprog(np.zeros(P), A_ub=A, b_ub=b, bounds=[(None, None)] * P, method="highs").status == 0: m += 1
    return m

if __name__ == "__main__":
    seeds = int(sys.argv[1]) if len(sys.argv) > 1 else 2; NL = int(sys.argv[2]) if len(sys.argv) > 2 else 5000
    NS = int(sys.argv[3]) if len(sys.argv) > 3 else 100
    perms = list(itertools.permutations(range(P)))
    for k in range(2):
        for s in range(seeds):
            t0 = time.time(); rng = np.random.default_rng(1000 * k + s); mu = make_mu(k, rng)
            found, fail, nodes, trees = 0, 0, [], {}
            samp = [perms[i] for i in np.random.default_rng(7 + s).choice(720, NS, replace=False)]
            for pi in samp:
                T, c = search(mu, pi, NL, rng); nodes.append(c)
                if T is None: fail += 1; continue
                G = edge_forms(mu, T); assert chain_valid(G, pi); found += 1; trees[pi] = G
            om = rng.dirichlet(np.ones(P), 20000); cone = [tuple(np.argsort(-o)) for o in om]
            ply_s = []
            for pi, G in trees.items():
                v = (G @ om.T > 0).all(0); ply_s.append(len({cone[i] for i in np.flatnonzero(v)}))
            sub = list(trees.items())[:: max(1, len(trees) // 6)]
            ply_lp = [cones_met_lp(G, perms) for _, G in sub]
            print(f"k={k+1} p={ps[k]} seed={s} |supp|={np.count_nonzero(mu)}: chain-valid T(pi) found {found}/{NS} sampled pi "
                  f"(DFS fail/limit {fail}; nodes median {int(np.median(nodes))} max {max(nodes)}) | "
                  f"cones met (sampled 20k) min/med/max {min(ply_s, default=0)}/{int(np.median(ply_s)) if ply_s else 0}/{max(ply_s, default=0)} "
                  f"| exact LP on {len(sub)} trees: {ply_lp} | {time.time()-t0:.0f}s", flush=True)
