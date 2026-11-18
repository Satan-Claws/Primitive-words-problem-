"""GLAM2: exact search for fold-dominant bichromatic trees (G-LAM', poly_GLAM.md §4).
Fold-dominant: rooted tree on supp(mu), edges join opposite signs, every non-root subtree S_u has
fold_r(mu|S_u) = sum_{i in S_u, i = r mod P} mu_i  >= 0 for all r (<= 0 if mu_u < 0), not all 0;
total fold(mu) = 0 (mu ⊥ U).
Part A (abstract, any n, any positions; crossing ignored, so stronger): all rooted labelled trees on
  m <= M vertices, all residue labellings (set partitions), LP feasibility in mu. Counts feasible with
  >= 2 residues.
Part B (concrete toys, mu forced by u): n=4 (P=2,p=2) and n=9 (P=3,p=3): admissible mu = u (fibre sums 0),
  all non-crossing trees x all roots, random generic u.
Part C (N=2, P=6, n=36): build admissible space for k=1,2, check fibre decomposition (E_k* = ⊕_r fibre
  parts) and that every generic u_k forces mu to meet all 6 fibres.
Usage: python3 glam2_search.py [M=5]"""
import sys, itertools, numpy as np
from scipy.optimize import linprog

def prufer_trees(m):
    if m == 1: yield []; return
    if m == 2: yield [(0, 1)]; return
    for seq in itertools.product(range(m), repeat=m - 2):
        deg = [1] * m
        for x in seq: deg[x] += 1
        edges, s = [], list(seq)
        for x in s:
            leaf = min(i for i in range(m) if deg[i] == 1)
            edges.append((leaf, x)); deg[leaf] -= 1; deg[x] -= 1
        u, v = [i for i in range(m) if deg[i] == 1]
        edges.append((u, v)); yield edges

def rooted(edges, m, root=0):
    adj = [[] for _ in range(m)]
    for a, b in edges: adj[a].append(b); adj[b].append(a)
    par, order, st = [-1] * m, [], [root]; seen = {root}
    while st:
        x = st.pop(); order.append(x)
        for y in adj[x]:
            if y not in seen: seen.add(y); par[y] = x; st.append(y)
    sub = {x: {x} for x in range(m)}
    for x in reversed(order):
        if par[x] >= 0: sub[par[x]] |= sub[x]
    depth = [0] * m
    for x in order:
        if par[x] >= 0: depth[x] = depth[par[x]] + 1
    return par, sub, depth

def setparts(m):
    def rec(i, cur, mx):
        if i == m: yield tuple(cur); return
        for c in range(mx + 2):
            yield from rec(i + 1, cur + [c], max(mx, c))
    yield from rec(1, [0], 0)

def lp_feasible(m, res, par, sub, sign):
    R = max(res) + 1
    A, b, Aeq, beq = [], [], [], []
    for v in range(m):  # sign[v]*mu_v >= 1
        row = np.zeros(m); row[v] = -sign[v]; A.append(row); b.append(-1)
    for u in range(m):
        if par[u] < 0: continue
        tot = np.zeros(m)
        for r in range(R):
            row = np.zeros(m)
            for i in sub[u]:
                if res[i] == r: row[i] = 1
            if row.any(): A.append(-sign[u] * row); b.append(0); tot += row
        A.append(-sign[u] * tot); b.append(-1)  # nonzero (scale-free strictness)
    for r in range(R):
        row = np.array([1.0 if res[i] == r else 0.0 for i in range(m)]); Aeq.append(row); beq.append(0)
    out = linprog(np.zeros(m), A_ub=A, b_ub=b, A_eq=Aeq, b_eq=beq, bounds=[(None, None)] * m, method="highs")
    return out.status == 0

def partA(M):
    for m in range(2, M + 1):
        tot = feas = feas_multi = 0
        for edges in prufer_trees(m):
            par, sub, depth = rooted(edges, m)
            sign = [(-1) ** d for d in depth]
            for res in setparts(m):
                tot += 1
                if lp_feasible(m, res, par, sub, sign):
                    feas += 1
                    if len(set(res)) > 1: feas_multi += 1
        print(f"A m={m}: (tree,root,residue) cases {tot}, fold-dominant feasible {feas}, with >=2 residues {feas_multi}")

def noncrossing_trees(pts):
    """all non-crossing spanning trees on points in convex position (cyclic order pts)."""
    pts = tuple(pts)
    from functools import lru_cache
    @lru_cache(None)
    def T(i, j):  # trees on pts[i..j] containing edge (i,j) not required; standard: spanning NC trees on interval
        if i == j: return [frozenset()]
        out = []
        # vertex i is connected to some k in (i,j]; pick the largest neighbour k of i
        for k in range(i + 1, j + 1):
            for L in Tij(i, k):         # trees on [i..k] with edge (i,k)
                for Rr in T(k, j) if k < j else [frozenset()]:
                    out.append(L | Rr)
        return out
    @lru_cache(None)
    def Tij(i, k):  # NC trees on [i..k] containing edge (i,k): split at m: [i..m] tree, [m+1..k] tree
        if k == i + 1: return [frozenset({(i, k)})]
        out = []
        for mm in range(i, k):
            for A_ in T(i, mm):
                for B_ in T(mm + 1, k):
                    out.append(A_ | B_ | {(i, k)})
        return out
    return [{(pts[a], pts[b]) for a, b in t} for t in T(0, len(pts) - 1)]

def check_tree_fixed_mu(mu, P, edges, root):
    n = len(mu); verts = sorted({x for e in edges for x in e}) or [root]
    idx = {v: t for t, v in enumerate(verts)}
    par, sub, depth = rooted([(idx[a], idx[b]) for a, b in edges], len(verts), idx[root])
    for a, b in edges:
        if mu[a] * mu[b] >= 0: return False
    for u in range(len(verts)):
        if par[u] < 0: continue
        s = np.sign(mu[verts[u]]); f = np.zeros(P)
        for i in sub[u]: f[verts[i] % P] += mu[verts[i]]
        if (s * f < -1e-12).any() or not (s * f > 1e-12).any(): return False
    return True

def partB(P, trials=3, rng=np.random.default_rng(1)):
    n = P * P
    trees = noncrossing_trees(range(n))
    for t in range(trials):
        mu = rng.normal(size=n)
        for r in range(P):  # fibre sums 0 (admissible: here mu ≅ u exactly)
            fib = list(range(r, n, P)); mu[fib] -= mu[fib].mean()
        if P == 2:  # p=2: mu_{i+2} = -mu_i
            mu = np.array([mu[0], mu[1], -mu[0], -mu[1]])
        good = sum(check_tree_fixed_mu(mu, P, list(e), root) for e in trees for root in range(n))
        bich = sum(all(mu[a] * mu[b] < 0 for a, b in e) for e in trees)
        print(f"B n={n} trial {t}: NC trees {len(trees)}, bichromatic {bich}, fold-dominant (any root) {good}")

def partC():
    P, n = 6, 36; ps = [2, 3]
    F = np.fft.fft(np.eye(n))
    for k, p in enumerate(ps):
        sk = n // p
        def keep(f):  # mode of image of (1-T^{s_k}) prod_{j!=k}(1-T^{P p_j})
            if (f * sk) % n == 0: return False
            return all((f * P * q) % n != 0 for j, q in enumerate(ps) if j != k)
        modes = [f for f in range(n) if keep(f)]
        Ek = [f for f in modes if (f * P * p) % n == 0]  # period P*p_k part
        # fibre decomposition: operators T^6 preserve fibres -> check E_k basis splits by fibre
        B = np.real_if_close(np.linalg.qr(np.real(np.concatenate([F[:, Ek].real, F[:, Ek].imag], 1)))[0])
        rk = np.linalg.matrix_rank(np.concatenate([F[:, Ek].real, F[:, Ek].imag], 1), 1e-9)
        per_fibre = []
        for r in range(P):
            mask = np.zeros(n); mask[r::P] = 1
            X = np.concatenate([F[:, Ek].real, F[:, Ek].imag], 1) * mask[:, None]
            per_fibre.append(np.linalg.matrix_rank(X, 1e-9))
        print(f"C k={k+1} p={p}: admissible mu-space dim {len(modes)}, dim E_k {rk}, E_k|fibre ranks {per_fibre} (sum {sum(per_fibre)})")

if __name__ == "__main__":
    M = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    partC(); partB(2); partB(3); partA(M)
