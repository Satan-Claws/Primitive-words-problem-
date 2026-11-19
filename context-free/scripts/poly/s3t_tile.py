"""S3T: TILE_k redone at n=36 (P_N=6, p in {2,3}) with the exact NC-tree interval DP of s3a_ncdp [computational].
For a NC bichromatic tree T on supp mu_k, its exact open cone (U_{>0} slice) is K_T = {w in R^6_{>0}: G_T w > 0},
G_T = edge_forms (signed subtree folds).  sigma_W(I) = s iff s<fold(mu|I), w> > 0 for all w in W; by convexity a tree
found by the DP with test set W is valid on cone(W).
Pipeline per target: training omegas (Dirichlet(1), Dirichlet(0.3), near-vertex M e_r + 1, barycentre, near-edge);
(1) pool: at each training point, DP-uniform random valid trees (exact sampler) + 'maximal cone' trees obtained by
greedily growing W from an uncovered point (one DP feasibility call per candidate); (2) ILP (scipy milp/HiGHS):
min z s.t. each training w covered >=1, ply(w) <= z; tie-break min #trees; (3) fresh validation omegas.
Usage: python3 s3t_tile.py [Ntrain=300] [seeds=2] [k]"""
import sys, time, numpy as np
from functools import lru_cache
from scipy.optimize import milp, LinearConstraint, Bounds
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from s2x_tile import make_mu, edge_forms, n, P, ps
from s3v_vertex import sigma_W

def sample_tree(pts, sg, sigma, rng):
    """uniform random tree among those the DP admits (None if none)."""
    m = len(pts)
    @lru_cache(None)
    def sub(l, r):
        s = sigma(l, r)
        if s == 0: return 0
        return sum(part(l, c - 1, -s) * part(c + 1, r, -s) for c in range(l, r + 1) if sg[c] == s)
    @lru_cache(None)
    def part(l, r, t):
        if l > r: return 1
        return sum(sub(l, k) * part(k + 1, r, t) for k in range(l, r + 1) if sigma(l, k) == t)
    def pick(ws):
        tot = sum(ws); x = int(rng.integers(0, 2**62)) * tot // 2**62
        for i, w in enumerate(ws):
            if x < w: return i
            x -= w
        return len(ws) - 1
    def bsub(l, r, E):
        s = sigma(l, r); cs = [c for c in range(l, r + 1) if sg[c] == s]
        c = cs[pick([part(l, c - 1, -s) * part(c + 1, r, -s) for c in cs])]
        bpart(l, c - 1, -s, c, E); bpart(c + 1, r, -s, c, E); return c
    def bpart(l, r, t, par, E):
        while l <= r:
            ks = [k for k in range(l, r + 1) if sigma(l, k) == t]
            k = ks[pick([sub(l, k) * part(k + 1, r, t) for k in ks])]
            c = bsub(l, k, E); E.append((pts[par], pts[c])); l = k + 1
    cnt = part(1, m - 1, -sg[0])
    if not cnt: return 0, None
    E = []; bpart(1, m - 1, -sg[0], 0, E); return cnt, E

def omegas(N, rng):
    out = [np.ones(P)]
    for i in range(N - 1):
        t = i % 4
        if t == 0: w = rng.dirichlet(np.ones(P))
        elif t == 1: w = rng.dirichlet(0.3 * np.ones(P))
        elif t == 2: w = np.ones(P) * 10 ** rng.uniform(-3, -1); w[rng.integers(P)] += 1   # near vertex
        else: w = rng.dirichlet(0.3 * np.ones(P)); w[rng.choice(P, 3, replace=False)] *= 1e-3  # near 3-face/edge
        out.append(w / w.sum())
    return np.array(out)

def cover_mat(Gs, W):  # A[i,j] = 1 iff W[i] in K_{T_j}
    return np.array([(W @ G.T > 1e-12).all(1) for G in Gs]).T.astype(int)

def ilp(A, zmax=None):
    Nw, Nt = A.shape; best = None
    for z in range(1, (zmax or 8) + 1):  # feasibility for each z, minimise #trees
        c = np.ones(Nt); cons = [LinearConstraint(A, 1, z)]
        r = milp(c, constraints=cons, integrality=np.ones(Nt), bounds=Bounds(0, 1), options={"time_limit": 20})
        if r.x is not None and r.status in (0, 1):
            return z, np.round(r.x).astype(bool), r.status
    return None, None, None

def run(k, seed, Ntr, Nfresh=4000):
    t0 = time.time(); rng = np.random.default_rng(1000 * k + seed); mu = make_mu(k, rng)
    supp = [i for i in range(n) if mu[i] != 0]; sg = [int(np.sign(mu[i])) for i in supp]
    Wtr = omegas(Ntr, np.random.default_rng(50 + seed + 10 * k)); Wfr = omegas(Nfresh, np.random.default_rng(999 + seed + 10 * k))
    Gs = []; cnts = []
    for w in Wtr:  # (a) exact random valid trees at each training point
        cnt, E = sample_tree(supp, sg, sigma_W(mu, supp, [w]), rng); cnts.append(cnt)
        if E: Gs.append(edge_forms(mu, E))
    nrand = len(Gs)
    covered = np.zeros(Ntr, bool)  # (b) maximal-cone trees
    order = rng.permutation(Ntr); calls = 0; nocov = []
    for i0 in order:
        if covered[i0]: continue
        W = [Wtr[i0]]; cand = np.argsort(np.linalg.norm(Wtr - Wtr[i0], axis=1)); fails = 0
        for j in cand[1:]:
            if covered[j] and rng.random() < 0.7: continue
            calls += 1
            if solve_ok(supp, sg, mu, W + [Wtr[j]]): W.append(Wtr[j]); fails = 0
            else:
                fails += 1
                if fails >= 25: break
        _, E = sample_tree(supp, sg, sigma_W(mu, supp, W), rng)
        if E is None: covered[i0] = True; nocov.append(i0); continue   # no valid tree at this w (tie/degenerate)
        G = edge_forms(mu, E); Gs.append(G)
        covered |= (Wtr @ G.T > 1e-12).all(1)
    nmax = len(Gs) - nrand
    keep = np.ones(Ntr, bool); keep[nocov] = False; Wtr = Wtr[keep]
    A = cover_mat(Gs, Wtr); Af = cover_mat(Gs, Wfr)
    fam_ply_tr = A.sum(1).max()
    z, x, st = ilp(A)
    sel = Af[:, x]; plyf = sel.sum(1)
    # greedy-maximal subfamily alone
    xm = np.zeros(len(Gs), bool); xm[nrand:] = True; plym = Af[:, xm].sum(1)
    vol = np.median(Af[:, :nrand].mean(0)); volm = np.median(Af[:, nrand:].mean(0))
    print(f"k={k+1} p={ps[k]} seed={seed} |supp|={len(supp)} Ntr={Ntr}: valid-tree counts at w: min {min(cnts):.2e} "
          f"#w with no valid tree {len(nocov)} median {np.median([float(c) for c in cnts]):.2e}; pool {nrand} random + {nmax} max-cone ({calls} DP calls); "
          f"median fresh-vol random {vol:.4f}, max-cone {volm:.3f}", flush=True)
    print(f"   max-cone family: {nmax} trees, fresh cover {np.mean(plym>0):.4f}, fresh max ply {plym.max()}, mean {plym[plym>0].mean():.2f}")
    print(f"   ILP (status {st}): min max-ply on training = {z} with {x.sum()} trees; fresh cover {np.mean(plyf>0):.4f}, "
          f"fresh max ply {plyf.max()}, ply hist {np.bincount(plyf)[:8].tolist()}; full-pool train ply {fam_ply_tr}  [{time.time()-t0:.0f}s]", flush=True)
    return dict(k=k, seed=seed, Ntr=Ntr, z=z, ntree=int(x.sum()), cov=float(np.mean(plyf > 0)), ply=int(plyf.max()),
                nmax=nmax, covm=float(np.mean(plym > 0)), plym=int(plym.max()))

def solve_ok(supp, sg, mu, W):
    from s3a_ncdp import solve
    return solve(supp, sg, sigma_W(mu, supp, W))[0] > 0

if __name__ == "__main__":
    Ntr = int(sys.argv[1]) if len(sys.argv) > 1 else 300; seeds = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    ks = [int(sys.argv[3])] if len(sys.argv) > 3 else range(2)
    for k in ks:
        for s in range(seeds): run(k, s, Ntr)
