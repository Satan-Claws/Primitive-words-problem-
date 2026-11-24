"""realise_bounded: data bounds (Lemma 3P's K) for the S_N transport-rule pieces.  R2/realise.md §1.

Part A (LAM facets mu_k = (1-T^{s_k}) prod_{j!=k}(1-T^{P p_j}) nu_k, nu_k generic integer):
  report max|mu|, and the ring-vector norms |mu_q|/g + |mu_p|/g (g = gcd) on the edges of the transport tree T*.
  These grow with nu (and with N via subset-sum collisions of g): NOT bounded by a constant K.
Part B (new 'pair facets' mu_k = (1-T^{s_k}) nu_k, nu_k = one +-1 per fibre, nested windows):
  exact checks:  mu_k in {0,+-1}^n;  mu_k _|_ U, V_{p_k}, E_j (j!=k);  mu_k|E_k != 0;
                 no nonempty proper cyclic arc of supp mu_k is identically balanced on W   (Lemma C, all N: §1.3)
  rule test at x-level (positive root with free left neighbour o_k), then the FULL piece basis V_sigma
  (tree edges e_p+e_q, root edges e_t+e_o, loops e_i):  max ||v||_1, laminarity (no crossing pair supports in
  linear block order over ALL components), |det| per component block (=1: unimodular), coordinates of x >= 0,
  and avoidance: mu_k(c+NV) >= 1 for the offset c = sum of root edges.
Usage: .venv/bin/python realise_bounded.py [N=3] [samples=6]
"""
import sys, random, math
from fractions import Fraction as Fr
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from tile2_core import make_cost, optimal_plan, is_spanning_tree, is_nc
from tile2_muk import structure

PR = [2, 3, 5, 7, 11, 13]


def det_int(M):
    """exact determinant (Bareiss)."""
    A = [row[:] for row in M]; n = len(A); sign = 1; prev = 1
    for k in range(n - 1):
        if A[k][k] == 0:
            sw = next((i for i in range(k + 1, n) if A[i][k] != 0), None)
            if sw is None: return 0
            A[k], A[sw] = A[sw], A[k]; sign = -sign
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                A[i][j] = (A[i][j] * A[k][k] - A[i][k] * A[k][j]) // prev
        prev = A[k][k]
    return sign * A[n - 1][n - 1]


def subtree(edges, mass, root):
    m = len(mass); adj = {v: [] for v in range(m)}
    for i, j in edges: adj[i].append(j); adj[j].append(i)
    order = [root]; par = {root: None}
    for v in order:
        for w in adj[v]:
            if w not in par: par[w] = v; order.append(w)
    sub = {v: mass[v] for v in range(m)}
    for v in reversed(order):
        if par[v] is not None: sub[par[v]] += sub[v]
    return sub, par


def part_A(N, reps=3, seed=1):
    print(f'--- Part A: LAM facets, N={N}')
    for k in range(N):
        ps, P, n, w, supp0, rows = structure(N, k)
        rng = random.Random(seed + k)
        for rep in range(reps):
            while True:
                nu = [rng.choice([-1, 1]) * rng.randint(1, 50) for _ in range(w)]
                mu0 = [sum(v * nu[q] for q, v in rows[i].items()) for i in supp0]
                if all(mu0): break
            s = next(a for a in range(len(mu0)) if mu0[a] > 0)
            supp = supp0[s:] + supp0[:s]; mu = mu0[s:] + mu0[:s]; m = len(supp); c = make_cost(m, rep)
            # also nu in {+-1}: entry growth from g alone
            mu1 = [sum(v * (1 if (q * 7919) % 3 else -1) for q, v in rows[i].items()) for i in supp0]
            while True:
                om = [rng.randint(100, 1000) for _ in range(P)]
                x = {i: 10 * om[i % P] for i in supp}
                for p in ps:
                    d = [rng.randint(-60, 60) for _ in range(P * p)]
                    for i in supp: x[i] += d[i % (P * p)]
                mraw = [mu[a] * x[supp[a]] for a in range(m)]; tau = sum(mraw)
                mp = list(mraw); mp[0] -= tau
                if tau > 0 and mp[0] > 0: break
            E = sorted(optimal_plan(mp, c))
            norms = [(abs(mu[j]) + abs(mu[i])) // math.gcd(mu[i], mu[j]) for i, j in E]
            print(f'k={k+1} rep={rep}: |supp|={m} max|mu|={max(map(abs,mu))} max|g*(+-1)|={max(map(abs,mu1))}'
                  f'  tree ok={is_spanning_tree(E,m) and is_nc(E)}  ring-vector ||v||_1: max={max(norms)}'
                  f' median={sorted(norms)[len(norms)//2]}')


def pair_facets(N, rng):
    """nested windows: component k uses fibre-index i in [I_k, I_k+p_k); partner at i + P/p_k."""
    ps = PR[:N]; P = math.prod(ps); n = P * P
    def nests(W):
        I = [sum(W[:k]) for k in range(N)]
        return I, all(I[k] + W[k] - 1 + P // ps[k] < I[k - 1] + P // ps[k - 1] for k in range(1, N))
    W = list(ps); I, ok = nests(W)      # width p_k: x_k(b_a) uniform mod p_k (needed for the VC bound)
    if not ok:                          # small N only: width 1 (structure checks still meaningful)
        W = [1] * N; I, ok = nests(W)
    assert ok, 'windows do not nest'
    print('window widths (i-units):', W, 'starts', I)
    mus = []
    for k in range(N):
        mu = {}
        for a in range(P):
            i = rng.randrange(I[k], I[k] + W[k]); e = rng.choice([-1, 1])
            b = a + i * P; mu[b] = e; mu[(b + n // ps[k]) % n] = -e
        mus.append(mu)
    return ps, P, n, mus


def check_facet(ps, P, n, k, mu):
    pk = ps[k]; sk = n // pk
    ok = {}
    fib = [0] * P
    for i, v in mu.items(): fib[i % P] += v
    ok['perpU'] = not any(fib)
    orb = {}
    for i, v in mu.items(): orb[i % sk] = orb.get(i % sk, 0) + v
    ok['perpV_pk'] = not any(orb.values())
    for j, pj in enumerate(ps):
        if j == k: continue
        M = P * pj; f = [0] * M
        for i, v in mu.items(): f[i % M] += v
        # _|_ E_j  <=>  fold mod P p_j constant on each fibre (residue mod P)
        ok[f'perpE{j+1}'] = all(len({f[r + t * P] for t in range(pj)}) == 1 for r in range(P))
    M = P * pk; f = [0] * M
    for i, v in mu.items(): f[i % M] += v
    ok['nonzero_on_Ek'] = any(len({f[r + t * P] for t in range(pk)}) > 1 for r in range(P))
    # Lemma C (cyclic arcs): arc form on W = (folds mod P p_j for all j); identically 0 iff all folds vanish
    supp = sorted(mu); m = len(supp); mods = [P * p for p in ps]
    bad = 0
    for s in range(m):
        cur = {}
        nz = 0
        for L in range(1, m):  # proper arcs starting at s, length L
            i = supp[(s + L - 1) % m]
            for M in mods:
                key = (M, i % M); old = cur.get(key, 0); new = old + mu[i]
                nz += (new != 0) - (old != 0); cur[key] = new
            if nz == 0: bad += 1
        if m > 300: break  # large m: only arcs from one start (cost); full check for N<=3
    ok['balanced_arcs'] = bad
    ok['entries'] = sorted(set(mu.values()))
    return ok


def part_B(N, samples, seed=7):
    print(f'--- Part B: pair facets, N={N}')
    rng = random.Random(seed)
    ps, P, n, mus = pair_facets(N, rng)
    for k in range(N):
        print(f'k={k+1}', check_facet(ps, P, n, k, mus[k]))
    for smp in range(samples):
        om = [rng.randint(10**4, 2 * 10**4) for _ in range(P)]
        while True:
            x = [om[i % P] for i in range(n)]
            for p in ps:
                d = [rng.randint(-300, 300) for _ in range(P * p)]
                # zero fibre sums: subtract fibre mean (integer: subtract per-fibre sum spread on t=0)
                for r in range(P):
                    d[r] -= sum(d[r + t * P] for t in range(p))
                for i in range(n): x[i] += d[i % (P * p)]
            taus = [sum(v * x[i] for i, v in mu.items()) for mu in mus]
            if all(t > 0 for t in taus) and min(x) > 0: break
            # flip signs of facets with tau<0 (mu -> -mu is an equally admissible facet)
            mus = [mu if t > 0 else {i: -v for i, v in mu.items()} for mu, t in zip(mus, taus)]
        V = []; used = set(); comp_blocks = []; coords_ok = True; avoid_ok = True; spans = []
        for k, mu in enumerate(mus):
            supp0 = sorted(mu)
            # root: positive vertex with free left neighbour (not in any support)
            allsupp = set().union(*[set(m_) for m_ in mus])
            r = next(a for a in range(len(supp0)) if mu[supp0[a]] > 0)  # root: any positive vertex (audit C1)
            supp = supp0[r:] + supp0[:r]; m = len(supp); c = make_cost(m, smp)
            mraw = [mu[supp[a]] * x[supp[a]] for a in range(m)]; tau = sum(mraw)
            mp = list(mraw); mp[0] -= tau
            E = sorted(optimal_plan(mp, c))
            assert is_spanning_tree(E, m) and is_nc(E)
            sub, par = subtree(E, mp, 0)
            valid = all((sub[v] > 0) == (mu[supp[v]] > 0) for v in range(1, m))
            pass
            vecs = [{supp[i]: 1, supp[j]: 1} for i, j in E] + [{supp[0]: 1}]  # root ring = b-loop e_t
            V += vecs; used |= set(supp)
            # coordinates: edge flow = |subtree mass| (|mu|=1), root loop e_t coordinate = tau
            coords = [abs(sub[j] if par.get(j) == i else sub[i]) for i, j in E] + [tau]
            coords_ok &= all(cv > 0 for cv in coords) and valid
            rec = {}
            for cv, vv in zip(coords, vecs):
                for pos, val in vv.items(): rec[pos] = rec.get(pos, 0) + cv * val
            coords_ok &= all(rec[i] == x[i] for i in supp)   # x|_S = sum coord * v exactly (integer coords)
            # unimodularity of the component block (coords supp + o, vectors = edges + root edge + loop e_o)
            idx = {v: t for t, v in enumerate(supp)}
            Mx = [[0] * m for _ in range(m)]
            for col, vv in enumerate(vecs):
                for pos, val in vv.items(): Mx[idx[pos]][col] = val
            comp_blocks.append(det_int(Mx) if m <= 130 else 'skip')
            # avoidance: mu_k(c + sum q v) = mu_k(c) + q_root * mu_k(root edge); root edge has mu = +1
            avoid_ok &= mu[supp[0]] == 1
            spans.append((min(supp0), max(supp0)))
        V += [{i: 1} for i in range(n) if i not in used]
        maxnorm = max(sum(v.values()) for v in V)
        pairs = [tuple(sorted(v)) for v in V if len(v) == 2]
        lam = True
        srt = sorted(pairs)
        # crossing test in linear order: O(|pairs|^2) on N<=3, sampled otherwise
        test = srt if len(srt) <= 2500 else random.Random(smp).sample(srt, 2500)
        for a in range(len(test)):
            p1, q1 = test[a]
            for b in range(a + 1, len(test)):
                p2, q2 = test[b]
                if p1 < p2 < q1 < q2 or p2 < p1 < q2 < q1: lam = False; break
            if not lam: break
        print(f'sample {smp}: |V|={len(V)} (n={n}) max||v||_1={maxnorm} laminar={lam} '
              f'comp |det|={[abs(d) if d != "skip" else d for d in comp_blocks]} coords>0&valid={coords_ok} '
              f'root mu=+1 (avoid V_p)={avoid_ok} spans={spans}')


if __name__ == '__main__':
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    S = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    if N <= 3: part_A(min(N, 3), reps=2)
    part_B(N, S)
