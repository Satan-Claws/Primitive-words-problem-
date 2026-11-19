"""S2X: computational probe of TILE_k (poly_S2P.md §3) at n=36, P_N=6, p in {2,3}.
mu_k = (1-T^{s_k}) prod_{j!=k}(1-T^{P p_j}) nu_k, nu_k random Gaussian on a window of length P p_k (so u_k
generic, touches all 6 fibres). Validity of an (unrooted) NC bichromatic tree T at omega in U_{>0} (R^6_{>0}):
for every edge e with side A_e containing endpoint a: sign(sum_{i in A_e} mu_i omega_{i mod 6}) = sign mu_a
(root-independent since mu ⊥ U; root/lex condition = u_k(delta)>0, automatic on R_k(u); generic omega => no
f(omega)=0 ties, so lex directions do not matter on the sampled set).
Family: LAM §2(b) greedy trees (random eligible merges) at sampled omega. Cover: min max-ply subfamily covering
the sample omegas (ILP, scipy milp/HiGHS, time limited) + LP lower bound (both relative to this family/sample).
Usage: python3 s2x_tile.py [seeds=3] [nsamp=1500]"""
import sys, numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds, linprog
n, P, ps = 36, 6, [2, 3]

def shift(v, s): return np.roll(v, s)
def make_mu(k, rng):
    p = ps[k]; s = n // p; nu = np.zeros(n); nu[:P * p] = rng.normal(size=P * p)
    mu = nu - shift(nu, s)
    for j, q in enumerate(ps):
        if j != k: mu = mu - shift(mu, P * q)
    mu[np.abs(mu) < 1e-12] = 0
    return mu

def greedy_tree(mu, om, rng, randomize=True):
    supp = [i for i in range(n) if mu[i] != 0]
    cur = list(supp); m = {i: mu[i] * om[i % P] for i in supp}; edges = []
    while len(cur) > 2:
        L = len(cur); el = []
        for t in range(L):
            x, y = cur[t], cur[(t + 1) % L]
            if m[x] * m[y] < 0: el.append((x, y) if abs(m[x]) < abs(m[y]) else (y, x))
        x, y = el[rng.integers(len(el))] if randomize else el[0]
        edges.append((min(x, y), max(x, y))); m[y] += m[x]; cur.remove(x)
    x, y = cur; edges.append((min(x, y), max(x, y)))
    return frozenset(edges)

def edge_forms(mu, edges):
    supp = sorted({v for e in edges for v in e}); adj = {v: [] for v in supp}
    for a, b in edges: adj[a].append(b); adj[b].append(a)
    G = []
    for a, b in edges:  # side of a after deleting edge
        side, st = {a}, [a]
        while st:
            x = st.pop()
            for y in adj[x]:
                if (x, y) in ((a, b), (b, a)) or y in side: continue
                side.add(y); st.append(y)
        f = np.zeros(P)
        for i in side: f[i % P] += mu[i]
        G.append(np.sign(mu[a]) * f)
    return np.array(G)

def run(k, seed, nsamp, extra=3):
    rng = np.random.default_rng(1000 * k + seed); mu = make_mu(k, rng)
    supp = np.flatnonzero(mu); fib = {r: int(np.sum(np.abs(mu[r::P]) > 0)) for r in range(P)}
    # samples: half uniform on simplex, half Dirichlet(0.3) (near boundary of U_{>0})
    om = np.vstack([rng.dirichlet(np.ones(P), nsamp // 2), rng.dirichlet(0.3 * np.ones(P), nsamp - nsamp // 2)])
    fam = {}
    for o in om:
        fam.setdefault(greedy_tree(mu, o, rng, False), None)
        for _ in range(extra): fam.setdefault(greedy_tree(mu, o, rng), None)
    trees = list(fam); Gs = [edge_forms(mu, t) for t in trees]
    V = np.array([(G @ om.T > 0).all(0) for G in Gs]).T.astype(float)  # samples x trees
    keep = V.any(1); om, V = om[keep], V[keep]  # drop float-tie samples (Dirichlet near boundary)
    natural = V.sum(1)  # ply of whole family
    # sign-vector chambers of all forms in family (on samples)
    allF = np.unique(np.round(np.vstack(Gs) / np.linalg.norm(np.vstack(Gs), axis=1, keepdims=True), 9), axis=0)
    ch = len({tuple(r) for r in (om @ allF.T > 0)})
    S, M = V.shape
    # LP lower bound: min z s.t. 1 <= V y <= z, 0<=y<=1
    c = np.zeros(M + 1); c[-1] = 1
    A1 = np.hstack([V, np.zeros((S, 1))]); A2 = np.hstack([V, -np.ones((S, 1))])
    lp = linprog(c, A_ub=np.vstack([-A1, A2]), b_ub=np.r_[-np.ones(S), np.zeros(S)],
                 bounds=[(0, 1)] * M + [(0, None)], method="highs")
    # greedy set cover then ILP
    cov = np.zeros(S, bool); chosen = []
    while not cov.all():
        g = V[~cov].sum(0); t = int(np.argmax(g)); chosen.append(t); cov |= V[:, t] > 0
    gply = V[:, chosen].sum(1).max()
    integ = np.r_[np.ones(M), 0]
    res = milp(c, constraints=[LinearConstraint(A1, 1, np.inf), LinearConstraint(A2, -np.inf, 0)],
               integrality=integ, bounds=Bounds(0, np.r_[np.ones(M), np.inf]), options={"time_limit": 40})
    ilp = res.x[-1] if res.x is not None else np.nan
    ilpb = getattr(res, "mip_dual_bound", np.nan)
    ilpn = int(round(res.x[:-1].sum())) if res.x is not None else -1
    sel = np.flatnonzero(res.x[:-1] > .5) if res.x is not None else np.array(chosen)
    omt = np.vstack([rng.dirichlet(np.ones(P), 2500), rng.dirichlet(0.3 * np.ones(P), 2500)])
    Vt = np.array([(Gs[t] @ omt.T > 0).all(0) for t in sel]).T
    Vf = np.array([(G @ omt.T > 0).all(0) for G in Gs]).T
    hold = f"holdout: ILP-cover covers {Vt.any(1).mean():.3f} (ply max {Vt.sum(1).max()}), full family covers {Vf.any(1).mean():.3f} (ply max {Vf.sum(1).max()})"
    print(f"k={k+1} p={ps[k]} seed={seed}: |supp mu|={len(supp)} fibre sizes {list(fib.values())} | trees {M} "
          f"| sample chambers {ch} (distinct forms {len(allF)}) | per-tree validity frac median {np.median(V.mean(0)):.4f} "
          f"| full-family ply max {natural.max():.0f} | greedy cover {len(chosen)} trees ply {gply:.0f} | "
          f"ILP ply {ilp:.0f} ({ilpn} trees, bound {ilpb:.2f}, {res.message[:20]}) | LP lb {lp.fun:.2f} | {hold}", flush=True)

if __name__ == "__main__":
    seeds = int(sys.argv[1]) if len(sys.argv) > 1 else 3; ns = int(sys.argv[2]) if len(sys.argv) > 2 else 1500
    for k in range(2):
        for s in range(seeds): run(k, s, ns)
