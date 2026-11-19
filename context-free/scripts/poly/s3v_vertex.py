"""S3V: base points near a vertex, omega_M = M*e_r + 1 (U-periodic weights), n=36, P_N=6 [computational].
Exact interval DP of s3a_ncdp.solve over ALL NC bichromatic trees on supp mu_k.
Targets: mu_k = make_mu-type with nu restricted to a fibre set F (|F| = s); the shift operators commute with
fibre restriction, so supp mu_k (hence the E_k-facet u_k) touches exactly the fibres F.
sigma(I) = s iff s*<fold(mu|I), w> > 0 for every w in the test set W (strict pointwise validity at all w in W;
K_T convex => validity on cone(W)).  Tests:
  A: W = {omega_M}               B: W = {1, omega_M} (segment)
  C: W = {omega_M^(r) : r in F}  D: W = {1} + C
  L: M = inf (lexicographic: sign of f_r, ties broken by total) together with 1.
Usage: python3 s3v_vertex.py [seeds=4]"""
import sys, numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from s2x_tile import n, P, ps, shift, edge_forms
from s3a_ncdp import solve
TOL = 1e-9

def make_mu_F(k, rng, F):
    p = ps[k]; s = n // p; nu = np.zeros(n); nu[:P * p] = rng.normal(size=P * p)
    for i in range(n):
        if i % P not in F: nu[i] = 0
    mu = nu - shift(nu, s)
    for j, q in enumerate(ps):
        if j != k: mu = mu - shift(mu, P * q)
    mu[np.abs(mu) < 1e-12] = 0
    return mu

def sigma_W(mu, supp, W):
    m = len(supp); F = np.zeros((m + 1, P))
    for t, i in enumerate(supp): F[t + 1] = F[t]; F[t + 1][i % P] += mu[i]
    Wm = np.array(W, float).T; cache = {}
    def sigma(l, r):
        if (l, r) in cache: return cache[(l, r)]
        v = (F[r + 1] - F[l]) @ Wm; s = 1 if (v > TOL).all() else (-1 if (v < -TOL).all() else 0)
        cache[(l, r)] = s; return s
    return sigma

def lexsig(mu, supp, rr):  # M = inf at e_r plus validity at 1
    m = len(supp); F = np.zeros((m + 1, P))
    for t, i in enumerate(supp): F[t + 1] = F[t]; F[t + 1][i % P] += mu[i]
    def sigma(l, r):
        f = F[r + 1] - F[l]; tot = f.sum()
        if abs(tot) < TOL: return 0
        s = int(np.sign(tot))
        return s if s * f[rr] >= -TOL else 0   # weak at e_r ray (closure), strict at 1
    return sigma

def om(M, r):
    w = np.ones(P); w[r] += M; return w

if __name__ == "__main__":
    seeds = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    Ms = [1, 10, 100, 1000]
    print("rows: k, |F|=s, M; entries = #(seed,r) feasible / total, tests A B C D; L = M=inf two-ray")
    for k in range(2):
        for s in range(1, P + 1):
            res = {M: [0, 0, 0, 0] for M in Ms}; tot = {M: [0, 0, 0, 0] for M in Ms}; Lc = [0, 0]
            for sd in range(seeds):
                rng = np.random.default_rng(7000 + 100 * k + 10 * s + sd)
                F = sorted(rng.choice(P, s, replace=False).tolist()); mu = make_mu_F(k, rng, F)
                supp = [i for i in range(n) if mu[i] != 0]; sg = [int(np.sign(mu[i])) for i in supp]
                assert sorted({i % P for i in supp}) == F
                for r in F:
                    Lc[1] += 1; Lc[0] += solve(supp, sg, lexsig(mu, supp, r))[0] > 0
                for M in Ms:
                    for r in F:
                        for t, W in enumerate([[om(M, r)], [np.ones(P), om(M, r)]]):
                            c, e = solve(supp, sg, sigma_W(mu, supp, W)); tot[M][t] += 1; res[M][t] += c > 0
                    for t, W in enumerate([[om(M, r) for r in F], [np.ones(P)] + [om(M, r) for r in F]]):
                        c, e = solve(supp, sg, sigma_W(mu, supp, W)); tot[M][2 + t] += 1; res[M][2 + t] += c > 0
            for M in Ms:
                print(f"k={k+1} p={ps[k]} s={s} M={M:5d}: A {res[M][0]}/{tot[M][0]}  B {res[M][1]}/{tot[M][1]}  "
                      f"C {res[M][2]}/{tot[M][2]}  D {res[M][3]}/{tot[M][3]}", flush=True)
            print(f"k={k+1} s={s} L(M=inf, weak e_r + strict 1): {Lc[0]}/{Lc[1]}", flush=True)
