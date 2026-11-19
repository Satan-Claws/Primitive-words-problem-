"""S3A: EXACT decision of Q1 (poly_S2Y) at n=36, P_N=6, p in {2,3} [computational].
Fact used: in a non-crossing (NC) spanning tree on points of a circle, deleting any edge leaves two cyclic arcs.
Rooting at the first support point v0, every subtree is a linear interval [l..r] of the remaining support points,
and chain-validity of edge (parent, c) depends only on the interval: sigma(I) = s in {+1,-1} iff
s*prefix_pi(fold(mu|I)) >= 0 coordinatewise and s*total > 0 (root-independent since fold(mu)=0).
Interval DP (exhaustive over ALL NC bichromatic spanning trees on supp mu_k in Z_n order, not only merge sequences):
  Sub(l,r)    : exists c in [l..r], sign(c) = sigma([l..r]), Part(l,c-1,-sign c), Part(c+1,r,-sign c)
  Part(l,r,t) : [l..r] is empty or a concatenation of intervals J with Sub(J), sigma(J) = t
  tree exists : Part(1,m-1,-sign v0).  Counts are computed the same way (each NC tree has a unique decomposition).
S2Q pi-monotonicity is a consequence of validity, hence automatically enforced (checked as an assertion on sigma).
Usage: python3 s3a_ncdp.py [seeds=2]"""
import sys, itertools, time, numpy as np
from functools import lru_cache
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from s2x_tile import make_mu, edge_forms, n, P, ps
from s2z_chain import chain_valid, cones_met_lp
TOL = 1e-9

def solve(pts, sg, sigma):
    """pts: list of points in circle order; sg[i] sign of pts[i]; sigma(l,r)->+1/-1/0. Returns (count, tree edges)."""
    m = len(pts)
    @lru_cache(None)
    def sub(l, r):
        s = sigma(l, r)
        if s == 0: return 0
        tot = 0
        for c in range(l, r + 1):
            if sg[c] == s: tot += part(l, c - 1, -s) * part(c + 1, r, -s)
        return tot
    @lru_cache(None)
    def part(l, r, t):
        if l > r: return 1
        return sum(sub(l, k) * part(k + 1, r, t) for k in range(l, r + 1) if sigma(l, k) == t)
    def build_sub(l, r, edges):
        s = sigma(l, r)
        for c in range(l, r + 1):
            if sg[c] == s and part(l, c - 1, -s) and part(c + 1, r, -s):
                build_part(l, c - 1, -s, c, edges); build_part(c + 1, r, -s, c, edges); return c
    def build_part(l, r, t, par, edges):
        while l <= r:
            for k in range(l, r + 1):
                if sigma(l, k) == t and sub(l, k) and part(k + 1, r, t):
                    c = build_sub(l, k, edges); edges.append((pts[par], pts[c])); l = k + 1; break
    cnt = part(1, m - 1, -sg[0]); edges = []
    if cnt: build_part(1, m - 1, -sg[0], 0, edges)
    return cnt, edges

def selftest():  # NC spanning trees on m convex points, unconstrained: 1,3,12,55,273,1428
    out = []
    for m in range(2, 8):
        # unconstrained: allow both signs -> emulate by alternating? use direct count with sigma=sg trick
        @lru_cache(None)
        def S(l, r):  # unconstrained NC trees on [l..r] rooted at some c (same recursion, no signs)
            return sum(Pt(l, c - 1) * Pt(c + 1, r) for c in range(l, r + 1))
        @lru_cache(None)
        def Pt(l, r):
            return 1 if l > r else sum(S(l, k) * Pt(k + 1, r) for k in range(l, r + 1))
        out.append(Pt(1, m - 1))
    return out

def brute(pts, sg, sigma_edge):  # brute force check on small instance
    m = len(pts); E = [(a, b) for a in range(m) for b in range(a + 1, m) if sg[a] != sg[b]]
    def cross(e, f):
        a, b = e; c, d = f
        return len({a, b, c, d}) == 4 and ((a < c < b) != (a < d < b))
    cnt = 0
    for T in itertools.combinations(E, m - 1):
        if any(cross(e, f) for e, f in itertools.combinations(T, 2)): continue
        par = list(range(m))
        def fd(x):
            while par[x] != x: x = par[x]
            return x
        okt = True
        for a, b in T:
            ra, rb = fd(a), fd(b)
            if ra == rb: okt = False; break
            par[ra] = rb
        if not okt: continue
        adj = {i: [] for i in range(m)}
        for a, b in T: adj[a].append(b); adj[b].append(a)
        good = True
        for a, b in T:  # side of b when rooted at 0 = subtree; compute side not containing 0
            side, st = {b}, [b]
            while st:
                x = st.pop()
                for y in adj[x]:
                    if {x, y} == {a, b} or y in side: continue
                    side.add(y); st.append(y)
            if 0 in side:
                side = set(range(m)) - side; v = a
            else: v = b
            l, r = min(side), max(side)
            if sigma_edge(l, r) != sg[v]: good = False; break
        cnt += good
    return cnt

def make_sigma(mu, supp, pi):
    perm = list(pi); m = len(supp)
    F = np.zeros((m + 1, P))
    for t, i in enumerate(supp): F[t + 1] = F[t]; F[t + 1][i % P] += mu[i]
    cache = {}
    def sigma(l, r):
        key = (l, r)
        if key in cache: return cache[key]
        f = F[r + 1] - F[l]; L = np.cumsum(f[perm]); s = 0
        if L[-1] > TOL and (L >= -TOL).all(): s = 1
        elif L[-1] < -TOL and (L <= TOL).all(): s = -1
        cache[key] = s; return s
    return sigma

if __name__ == "__main__":
    print("selftest unconstrained NC tree counts m=2..7:", selftest(), "(expect 1,3,12,55,273,1428)")
    rng0 = np.random.default_rng(5); bad = 0
    for trial in range(30):  # brute-force cross-check of constrained DP on random small instances
        m = 7; sg = list(rng0.choice([-1, 1], m)); tab = {(l, r): int(rng0.choice([-1, 1, 1, -1, 0]))
                                                           for l in range(m) for r in range(l, m)}
        sig = lambda l, r: tab[(l, r)]
        c1, _ = solve(list(range(m)), sg, sig); c2 = brute(list(range(m)), sg, sig); bad += (c1 != c2)
    print("DP vs brute force on 30 random 7-point instances: mismatches =", bad)
    seeds = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    perms = list(itertools.permutations(range(P)))
    for k in range(2):
        for s in range(seeds):
            t0 = time.time(); rng = np.random.default_rng(1000 * k + s); mu = make_mu(k, rng)
            supp = [i for i in range(n) if mu[i] != 0]; sg = [int(np.sign(mu[i])) for i in supp]
            yes, counts, certs = 0, [], {}
            for pi in perms:
                cnt, edges = solve(supp, sg, make_sigma(mu, supp, pi)); counts.append(cnt)
                if cnt:
                    yes += 1; G = edge_forms(mu, edges); assert len(edges) == len(supp) - 1 and chain_valid(G, pi)
                    certs[pi] = (edges, G)
            fib = sorted(i % P for i in supp)
            print(f"k={k+1} p={ps[k]} seed={s} |supp|={len(supp)} fibres used={sorted(set(fib))}: "
                  f"orders pi with a chain-valid NC tree: {yes}/720; tree-count max {max(counts)}", flush=True)
            if certs:
                pi0, (e0, G0) = next(iter(certs.items()))
                print("  certificate pi=", pi0, "edges=", e0)
                q2 = [cones_met_lp(G, perms) for pi, (e, G) in list(certs.items())[:10]]
                print("  Q2 cones met (exact LP) for first 10:", q2)
            print(f"  {time.time()-t0:.0f}s", flush=True)
