"""tile2_muk: Theorem A/B of R2/tile2.md on the ACTUAL facets
    mu_k = (1 - T^{n/p_k}) prod_{j != k} (1 - T^{P p_j}) nu_k,   n = P^2, P = p_1...p_N, nu_k on a window of length P p_k.

(1) STRUCTURAL arc-genericity (exact integer arithmetic, as linear maps in nu; no randomness):
    omega-level: no proper arc I of supp mu_k has fold_P(mu|I) == 0 identically in nu;
    x-level   : no proper arc I has fold_{P p_j}(mu|I) == 0 for ALL j (i.e. mu|I vanishing on
                W = sum_j {period-(P p_j) vectors} = U + sum E_j for the natural E_j).
    (For large N a random-integer-nu projection is used: distinct prefix vectors CERTIFY non-balance exactly.)
(2) Rule test (N = 2, optionally N = 3): random integer nu; random generic base points (omega-level, and
    x = big*omega + delta with delta in W, root v0 absorbing tau = <mu,x>); the min-cost plan for the concave
    cost is computed by LP (float), its support is checked EXACTLY to be a spanning, non-crossing, bichromatic
    tree valid at the point; dual margins printed; and pairwise: T*(x') valid at x  =>  T*(x') == T*(x).
Usage: .venv/bin/python tile2_muk.py [N=2] [samples=40] [lp=1]
"""
import sys, random, time
import numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from tile2_core import make_cost, optimal_plan, is_spanning_tree, is_nc, valid_exact, dual_margin

PR = [2, 3, 5, 7, 11, 13]


def factor_poly(N, k):
    ps = PR[:N]; P = int(np.prod(ps)); n = P * P
    g = {0: 1}
    facs = [n // ps[k]] + [P * ps[j] for j in range(N) if j != k]
    for a in facs:
        h = dict(g)
        for t, v in g.items(): h[(t + a) % n] = h.get((t + a) % n, 0) - v
        g = {t: v for t, v in h.items() if v}
    return ps, P, n, g, P * ps[k]


def structure(N, k):
    """support and exact coefficient rows C_i in Z^w (mu_i = C_i . nu)."""
    ps, P, n, g, w = factor_poly(N, k)
    rows = {}
    for t, v in g.items():
        for q in range(w):
            i = (t + q) % n
            rows.setdefault(i, {}); rows[i][q] = rows[i].get(q, 0) + v
    supp = sorted(i for i, r in rows.items() if any(r.values()))
    return ps, P, n, w, supp, {i: {q: v for q, v in rows[i].items() if v} for i in supp}


def arc_generic(N, k, exact=True, seed=0):
    ps, P, n, w, supp, rows = structure(N, k)
    m = len(supp)
    mods = [P] + [P * p for p in ps]
    rng = random.Random(seed)
    nu = [rng.randint(-10**6, 10**6) for _ in range(w)]
    res = {}
    for name, mm in (('omega', [P]), ('x', [P * p for p in ps])):
        if exact and N <= 3:
            dim = sum(mm)
            cur = np.zeros((dim, w), dtype=np.int64)
            seen = {cur.tobytes(): 0}; coll = []
            for j in range(1, m):
                i = supp[j]; off = 0
                for M in mm:
                    for q, v in rows[i].items(): cur[off + (i % M), q] += v
                    off += M
                key = cur.tobytes()
                if key in seen: coll.append((seen[key], j))
                else: seen[key] = j
            res[name] = ('exact', coll)
        else:
            mu = {i: sum(v * nu[q] for q, v in rows[i].items()) for i in supp}
            dim = sum(mm); cur = np.zeros(dim, dtype=np.int64)  # |prefix| < 1e13: no overflow
            seen = {cur.tobytes(): 0}; coll = []
            for j in range(1, m):
                i = supp[j]; off = 0
                for M in mm: cur[off + (i % M)] += mu[i]; off += M
                key = cur.tobytes()
                if key in seen: coll.append((seen[key], j))
                else: seen[key] = j
            res[name] = ('random-nu certificate (distinct => exact)', coll)
    return dict(N=N, k=k + 1, p=ps[k], n=n, P=P, supp=m, zero_entries=n - m), res


def rule_test(N, k, samples, seed=1):
    ps, P, n, w, supp, rows = structure(N, k)
    rng = random.Random(seed)
    while True:
        nu = [rng.choice([-1, 1]) * rng.randint(1, 50) for _ in range(w)]
        mu = [sum(v * nu[q] for q, v in rows[i].items()) for i in supp]
        if all(mu): break
    m = len(supp); c = make_cost(m, seed)
    out = []
    t0 = time.time()
    for s in range(samples):
        om = [rng.randint(100, 1000) for _ in range(P)]
        if s % 2 == 0:  # omega-level
            mass = [mu[a] * om[supp[a] % P] for a in range(m)]; lvl = 'omega'
        else:  # x-level: x = B*omega + delta, delta = sum_j (period-P p_j vector)
            B = 10
            x = {i: B * om[i % P] for i in supp}
            for p in ps:
                d = [rng.randint(-60, 60) for _ in range(P * p)]
                for i in supp: x[i] += d[i % (P * p)]
            mass = [mu[a] * x[supp[a]] for a in range(m)]
            tau = sum(mass); mass[0] -= tau; lvl = 'x'
            if (mass[0] > 0) != (mu[0] > 0): continue  # outside the near-U cone {sgn(m_v0 - tau) = sgn mu_v0}
        assert sum(mass) == 0
        plan = optimal_plan(mass, c)
        E = sorted(plan)
        sp = is_spanning_tree(E, m); nc = is_nc(E); val = sp and valid_exact(E, mass)
        dm = dual_margin(E, c, mass) if sp else None
        zero_arc_comp = None
        if not sp:  # diagnose: components of the optimal support that are arcs, with their EXACT mass
            par = list(range(m))
            def fd(a):
                while par[a] != a: par[a] = par[par[a]]; a = par[a]
                return a
            for i, j in E: par[fd(i)] = fd(j)
            comps = {}
            for a in range(m): comps.setdefault(fd(a), []).append(a)
            zero_arc_comp = []
            for C in comps.values():
                C = sorted(C); gaps = sum(1 for t in range(len(C)) if (C[(t + 1) % len(C)] - C[t]) % m != 1)
                if gaps <= 1: zero_arc_comp.append((len(C), sum(mass[a] for a in C)))
        out.append((lvl, mass, frozenset(E), sp, nc, val, dm, zero_arc_comp))
    # pairwise uniqueness check
    viol = 0
    for a in range(len(out)):
        for b in range(len(out)):
            if a != b and out[b][3] and out[a][2] != out[b][2] and valid_exact(sorted(out[b][2]), out[a][1]):
                viol += 1
    by = {L: [o for o in out if o[0] == L] for L in ('omega', 'x')}
    return dict(N=N, k=k + 1, supp=m, samples=len(out),
                **{L + '_spanning_valid': f"{sum(o[5] for o in by[L])}/{len(by[L])}" for L in by},
                arc_components_of_failures=[o[7] for o in out if o[7] is not None][:4],
                noncrossing=sum(o[4] for o in out),
                min_dual_margin=min(o[6] for o in out if o[6] is not None),
                distinct_trees=len({o[2] for o in out}), pairwise_ply_violations=viol, secs=round(time.time() - t0, 1))


if __name__ == '__main__':
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    S = int(sys.argv[2]) if len(sys.argv) > 2 else 40
    lp = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    for k in range(N):
        info, res = arc_generic(N, k)
        print(info, {a: (b[0], 'balanced arcs:', len(b[1]), b[1][:5]) for a, b in res.items()}, flush=True)
    if lp:
        for k in range(N):
            print(rule_test(N, k, S), flush=True)
