"""r3_depth_localbound: Lemma D1 of R2/r3_depth.md, checked numerically.

Lemma D1 says that a facet-tuple family whose facets touch few fibres (residue classes mod P) has ply at least
(P/(2s))^N at one point of polynomial norm.

Model: n = P^2, positions x = r + P t, t in CRT coordinates.
  - Adversary points: f_{k,r,beta} = indicator{fibre r, t_k = beta}. It lies in V_j for every j != k and is not in V_k.
  - Local I0 options for prime k: (a, b = a + j s_k, eps), with facet mu = e_a - e_{a+1} - e_b + e_{b+1} and
    covering condition eps*mu(x) >= 1.
Steps:
  (1) Exact check: mu_k(f_{j,r,beta}) = 0 for j != k, for every I0 facet of prime k and every (r, beta).
  (2) For each k, the per-k universe U_k = {(r, beta, eps)}. Build the coverage matrix of the I0 options,
      compute the max coverage per option (<= 4), the greedy cover size tau_k, and the lower bound |U_k| / max.
  (3) The product family (one greedy option per prime). Its ply at x* = sum_{k,r,beta} c_{k,r,beta} f_{k,r,beta},
      with c iid +-1, is prod_k sat_k(x*). Report the max over samples, against n and the formula.
  (4) Asymptotics of the D1 bound (P/(2s))^N at s = 2 for primorial P, as a power of n.
Usage: r3_depth_localbound.py [samples]
"""
import sys, random, math
import numpy as np
from math import prod

PRIMORIALS = [(2, 3), (2, 3, 5), (2, 3, 5, 7)]

def setup(ps):
    P = prod(ps); n = P * P
    t = np.arange(n) // P; r = np.arange(n) % P
    crt = np.stack([t % p for p in ps], axis=1)  # CRT coordinate of each position
    return P, n, r, crt

def fvec(ps, P, n, r, crt, k, rr, beta):
    return ((r == rr) & (crt[:, k] == beta)).astype(np.int64)

def run(ps, samples, rng):
    P, n, r, crt = setup(ps); N = len(ps)
    s = [n // p for p in ps]
    # I0 options for prime k (positions a, offset j): mu(y) = z_a - z_b, z_x = y_x - y_{x+1}
    def mu_val(y, a, b):
        return (y[a] - y[(a + 1) % n]) - (y[b] - y[(b + 1) % n])
    a_all = np.arange(n)
    report = {}
    sat_counts = []
    # (1) exact orthogonality check (vectorised over all a, j)
    viol = 0
    for k in range(N):
        for j in range(N):
            if j == k: continue
            for rr in range(P):
                for beta in range(ps[j]):
                    y = fvec(ps, P, n, r, crt, j, rr, beta)
                    z = y - np.roll(y, -1)
                    for jj in range(1, ps[k]):
                        b = (a_all + jj * s[k]) % n
                        viol += int(np.count_nonzero(z[a_all] - z[b]))
    report['orth_violations'] = viol
    covers = []
    for k in range(N):
        U = [(rr, beta, e) for rr in range(P) for beta in range(ps[k]) for e in (1, -1)]
        Z = np.stack([(lambda y: y - np.roll(y, -1))(fvec(ps, P, n, r, crt, k, rr, beta)) for rr, beta, _ in U])
        E = np.array([e for *_, e in U])
        opts = []; cols = []
        for jj in range(1, ps[k]):
            b = (a_all + jj * s[k]) % n
            D = (Z[:, a_all] - Z[:, b]) * E[:, None]  # |U| x n : value of mu at signed adversary
            for eps in (1, -1):
                C = (eps * D >= 1)
                cols.append(C); opts.extend((int(a), int((a + jj * s[k]) % n), eps) for a in a_all)
        Cov = np.concatenate(cols, axis=1)  # |U| x #opts
        maxcov = int(Cov.sum(axis=0).max())
        # greedy cover
        unc = np.ones(len(U), bool); chosen = []
        while unc.any():
            g = (Cov[unc]).sum(axis=0); i = int(g.argmax())
            if g[i] == 0: raise RuntimeError('uncoverable')
            chosen.append(opts[i]); unc &= ~Cov[:, i]
        covers.append(chosen)
        report[f'k{k}'] = dict(U=len(U), maxcov=maxcov, LB=math.ceil(len(U) / maxcov), greedy=len(chosen))
    # (3) ply of the product family at random x*
    best = 0; tot = 0
    F = {(k, rr, beta): fvec(ps, P, n, r, crt, k, rr, beta) for k in range(N) for rr in range(P) for beta in range(ps[k])}
    for _ in range(samples):
        x = np.zeros(n, np.int64)
        for key, v in F.items(): x += rng.choice((-1, 1)) * v
        ply = 1
        for k in range(N):
            ply *= sum(1 for a, b, eps in covers[k] if eps * mu_val(x, a, b) >= 1)
        best = max(best, ply); tot += ply
    report['ply_max'] = best; report['ply_mean'] = tot / samples
    report['n'] = n; report['log_n_ply'] = math.log(max(best, 1)) / math.log(n)
    return report

def asymptotics():
    from sympy import prime
    rows = []
    for N in range(3, 16):
        ps = [prime(i) for i in range(1, N + 1)]; P = prod(ps); n = P * P
        lb = N * math.log(P / 4.0)  # (P/(2s))^N with s = 2 (I0 facets)
        rows.append((N, n, lb / math.log(n)))
    return rows

if __name__ == '__main__':
    samples = int(sys.argv[1]) if len(sys.argv) > 1 else 50
    rng = random.Random(1)
    for ps in PRIMORIALS[:2]:
        print(ps, run(ps, samples, rng))
    print('D1 bound exponent log_n[(P/4)^N] (s = 2) for primorial P (N, n, exponent):')
    for N, n, e in asymptotics():
        print(f'  N={N:2d} n={n:.3e} exponent={e:.3f}')
