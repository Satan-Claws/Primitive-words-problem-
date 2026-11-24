"""newslice_check: do variants (a) deeper prime powers and (b)/(c) fibre-restricted sub-slices escape the
transport tiling of R2/tile2.md?  (R2/newslice.md section 3.)

n = P^a (P = p_1...p_N), U = period u = P^(a-1) (= n/rad n), g_j = u*p_j, s_k = n/p_k.
Facet (natural generalisation of LAM 2(a)):  mu_k = (1 - T^{s_k}) prod_{j != k} (1 - T^{g_j}) nu_k,
nu_k supported on (window of length g_k) intersected with J, J = union of fibres (residues mod u) in Fset.
x-level region W^J = sum_j {period-g_j vectors} restricted to J (contains U^J + sum E_k^J).
Checks:
 (1) mu_k _|_ V_{p_k}, U, period-g_j (j != k)  [exact, random integer nu];
 (2) W-arc-genericity: no proper arc I of supp mu_k with fold_{g_j}(mu|I) = 0 for all j
     (random-integer-nu certificate: distinct prefix vectors => non-balanced EXACTLY);
 (3) transport rule at x-level points x = B*omega + delta (delta in W^J): LP plan support is a spanning NC
     bichromatic tree, valid (exact), and pairwise ply-1 among sampled points.
Usage: .venv/bin/python newslice_check.py
"""
import sys, random, time
import numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from tile2_core import make_cost, optimal_plan, is_spanning_tree, is_nc, valid_exact

PR = [2, 3, 5, 7, 11, 13]


def facet(N, a, k, Fset, rng):
    ps = PR[:N]; P = int(np.prod(ps)); n = P ** a; u = P ** (a - 1)
    g = {0: 1}
    for sh in [n // ps[k]] + [u * ps[j] for j in range(N) if j != k]:
        h = dict(g)
        for t, v in g.items(): h[(t + sh) % n] = h.get((t + sh) % n, 0) - v
        g = {t: v for t, v in h.items() if v}
    w = u * ps[k]
    nu = {q: rng.choice([-1, 1]) * rng.randint(1, 10 ** 5) for q in range(w) if q % u in Fset}
    mu = {}
    for t, v in g.items():
        for q, c in nu.items():
            i = (t + q) % n; mu[i] = mu.get(i, 0) + v * c
    mu = {i: v for i, v in mu.items() if v}
    return ps, P, n, u, mu


def orth_checks(ps, n, u, mu, k):
    def fold(M):
        f = [0] * M
        for i, v in mu.items(): f[i % M] += v
        return f
    ok_Vp = not any(fold(n // ps[k]))
    ok_U = not any(fold(u))
    ok_gj = all(not any(fold(u * ps[j])) for j in range(len(ps)) if j != k)
    ok_gk_nonzero = any(fold(u * ps[k]))
    return ok_Vp and ok_U and ok_gj and ok_gk_nonzero


def arc_balanced(ps, u, mu):
    supp = sorted(mu); mods = [u * p for p in ps]
    cur = np.zeros(sum(mods), dtype=object); seen = {tuple(cur): 0}; coll = 0
    for j in range(1, len(supp)):
        i = supp[j]; off = 0
        for M in mods: cur[off + i % M] += mu[i]; off += M
        key = tuple(cur)
        if key in seen: coll += 1
        else: seen[key] = j
    return coll  # number of (cyclic) proper arcs with W-balanced mass (0 => certificate)


def rule(ps, n, u, mu, Fset, samples, rng):
    supp = sorted(mu); m = len(supp); c = make_cost(m, 7)
    muv = [mu[i] for i in supp]
    out = []
    while len(out) < samples:
        om = [rng.randint(100, 1000) for _ in range(u)]
        x = {i: 20 * om[i % u] for i in supp}
        for p in ps:
            d = [rng.randint(-60, 60) for _ in range(u * p)]
            for i in supp: x[i] += d[i % (u * p)]
        mass = [muv[a] * x[supp[a]] for a in range(m)]
        tau = sum(mass); mass[0] -= tau
        if (mass[0] > 0) != (muv[0] > 0) or tau <= 0: continue
        E = sorted(optimal_plan(mass, c))
        sp = is_spanning_tree(E, m)
        out.append((mass, frozenset(E), sp, sp and is_nc(E), sp and valid_exact(E, mass)))
    viol = sum(1 for A in out for B in out if B[2] and A[1] != B[1] and valid_exact(sorted(B[1]), A[0]))
    return dict(m=m, spanning=sum(o[2] for o in out), nc=sum(o[3] for o in out), valid=sum(o[4] for o in out),
                samples=len(out), distinct=len({o[1] for o in out}), ply_violations=viol)


if __name__ == '__main__':
    rng = random.Random(2026)
    cases = [(2, 2, None, 12), (2, 3, None, 12), (2, 4, None, 0), (3, 2, None, 4), (3, 3, None, 0),
             (2, 3, 'half', 12), (3, 2, 'half', 4)]
    for N, a, mode, S in cases:
        u = int(np.prod(PR[:N])) ** (a - 1)
        Fset = set(range(u)) if mode is None else set(rng.sample(range(u), max(2, u // 2)))
        for k in range(N):
            t0 = time.time()
            ps, P, n, u, mu = facet(N, a, k, Fset, rng)
            r = dict(N=N, a=a, n=n, fibres=len(Fset), k=k + 1, supp=len(mu), orth=orth_checks(ps, n, u, mu, k),
                     W_balanced_arcs=arc_balanced(ps, u, mu))
            if S and len(mu) <= 700: r['rule'] = rule(ps, n, u, mu, Fset, S, rng)
            r['secs'] = round(time.time() - t0, 1)
            print(r, flush=True)
