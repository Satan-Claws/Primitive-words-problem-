"""gglob_matching: checks for R2/gglob.md (matching reduction of the G4 criterion, K = 2).

Lemma G5 (gglob.md §1): for a K=2 laminar piece active near U, L1^perp is contained in A(M) = span{e_p - e_q : pq in M}
for a non-crossing (partial) matching M.  So prime k is certifiable at level t only if  y notin V_k + L(M),
L(M) = span{e_p + e_q : pq in M}, i.e. d_M(y) notin d_M(V_k)  (d_M(y)_pq = y_p - y_q).

Test:  y in V_k + L(M)  <=>  d_M(y) in rowspace(C_k), C_k[Z, pq] = [p in Z] - [q in Z] over the k-cycles Z
(a = coefficients on matching pairs; a _|_ V_k <=> a.C_k^T = 0).  Exact rank mod a large prime.

Part A (level t, 'exists M forall k'): fraction of uniform random NC perfect matchings M certifying all primes,
          for sparse mixed-type y; also the two adjacent matchings M0 = {(2b,2b+1)}, M1 = {(2b+1,2b+2)}.
Part B (G-glob two-level necessary condition): x = t1 + s*delta + eta, A = A(delta) != [N]:
          need M with  delta notin V_k + L(M) (k in A)  and  eta notin V_k + L(M) + R delta  (k notin A).
Part C (Lemma G6): dimension count showing {M0, M1} alone leave primitive y uncertified (explicit y, n = 36).
Usage: .venv/bin/python gglob_matching.py [samples36] [samples900]
"""
import sys, random
from math import prod
import numpy as np

PR = [2, 3, 5, 7, 11]
MOD = 2147483629


def rank_mod(A):
    A = np.array(A, dtype=np.int64) % MOD
    r = 0; rows, cols = A.shape
    for c in range(cols):
        if r == rows: break
        piv = np.nonzero(A[r:, c])[0]
        if len(piv) == 0: continue
        p = r + piv[0]
        if p != r: A[[r, p]] = A[[p, r]]
        inv = pow(int(A[r, c]), MOD - 2, MOD)
        A[r] = (A[r] * inv) % MOD
        nz = np.nonzero(A[:, c])[0]
        nz = nz[nz != r]
        if len(nz):
            A[nz] = (A[nz] - (A[nz, c][:, None] * A[r][None, :]) % MOD) % MOD
        r += 1
    return r


def random_nc_matching(n, rng):
    """uniform NC perfect matching of Z_n (cycle lemma on n/2 U, n/2+1 D), then a random rotation."""
    m = n // 2
    while True:
        seq = [1] * m + [-1] * (m + 1); rng.shuffle(seq)
        # rotate so that it is a Dyck path followed by a final -1
        s, mn, arg = 0, 0, 0
        for i, v in enumerate(seq):
            s += v
            if s < mn: mn, arg = s, i + 1
        seq = seq[arg:] + seq[:arg]
        seq = seq[:-1]
        st, M = [], []
        for i, v in enumerate(seq):
            if v == 1: st.append(i)
            else: M.append((st.pop(), i))
        rot = rng.randrange(n)
        return [((a + rot) % n, (b + rot) % n) for a, b in M]


def adjacent(n, off):
    return [((2 * b + off) % n, (2 * b + 1 + off) % n) for b in range(n // 2)]


def cyc_index(n, s):
    return np.arange(n) % s  # k-cycle of position i is i mod s_k


def in_VkLM(y, M, n, s):
    """y in V_k + L(M) ?  (s = s_k)"""
    cid = cyc_index(n, s)
    C = np.zeros((s, len(M)), dtype=np.int64)
    d = np.zeros(len(M), dtype=np.int64)
    for j, (p, q) in enumerate(M):
        C[cid[p], j] += 1; C[cid[q], j] -= 1
        d[j] = y[p] - y[q]
    r0 = rank_mod(C)
    return rank_mod(np.vstack([C, d[None, :]])) == r0


def in_VkLM_extra(y, M, n, s, extra):
    """y in V_k + L(M) + span(extra) ?  Work in the quotient by L(M): the image of extra must be added to V_k image."""
    cid = cyc_index(n, s)
    # basis of V_k image in d-space: for each cycle residue r, d_M(1_{cycle r}); plus d_M(extra)
    rows = np.zeros((s + len(extra), len(M)), dtype=np.int64)
    d = np.zeros(len(M), dtype=np.int64)
    for j, (p, q) in enumerate(M):
        rows[cid[p], j] += 1; rows[cid[q], j] -= 1
        for e, ev in enumerate(extra): rows[s + e, j] = ev[p] - ev[q]
        d[j] = y[p] - y[q]
    r0 = rank_mod(rows)
    return rank_mod(np.vstack([rows, d[None, :]])) == r0


def orbit_ind(n, start, step):
    v = np.zeros(n, dtype=np.int64); i = start
    while True:
        v[i % n] = 1; i += step
        if i % n == start % n: break
    return v


def periodic(y, n, s):
    return np.array_equal(y, np.roll(y, -s))


def test_vectors(N, rng):
    P = prod(PR[:N]); n = P * P; sk = [n // p for p in PR[:N]]
    out = []
    # G2 vector
    while True:
        z, w = rng.randrange(n), rng.randrange(n)
        y = orbit_ind(n, z, n // 2) + orbit_ind(n, w, n // 3)
        if y.max() == 1: break
    out.append(('G2: 1_D+1_T', y))
    # single orbits of each prime, summed (types [N]\{k} overlapping)
    y = sum(orbit_ind(n, rng.randrange(n), s) for s in sk)
    out.append(('sum_k 1_{s_k-orbit}', y))
    if N >= 3:
        # pairwise-intersection orbits: 1_{orbit n/(p1p3)} + 1_{orbit n/(p2p3)} + e_q  (delta in V_3; eta = e_q)
        y = orbit_ind(n, rng.randrange(n), n // (2 * 5)) + orbit_ind(n, rng.randrange(n), n // (3 * 5)) \
            + orbit_ind(n, rng.randrange(n), n // (2 * 3))
        out.append(('1_{X13}+1_{X23}+1_{X12}', y))
    # random sparse integer defect on 6 points
    y = np.zeros(n, dtype=np.int64)
    for q in rng.sample(range(n), 6): y[q] = rng.choice([-2, -1, 1, 2])
    out.append(('random 6-pt', y))
    return n, sk, out


def partA(N, samples, rng):
    n, sk, vecs = test_vectors(N, rng)
    print(f"\nPart A  N={N} n={n}  (samples={samples})")
    Ms = [random_nc_matching(n, rng) for _ in range(samples)]
    for name, y in vecs:
        prim = all(not periodic(y, n, s) for s in sk)
        res0 = [not any(in_VkLM(y, adjacent(n, o), n, s) for s in sk) for o in (0, 1)]
        good = 0; perk = [0] * N
        for M in Ms:
            bad = [in_VkLM(y, M, n, s) for s in sk]
            for k in range(N): perk[k] += (not bad[k])
            good += not any(bad)
        print(f"  {name:28s} prim={prim} |supp|={int((y!=0).sum()):4d}  M0,M1 ok={res0}  "
              f"random NC: all-k {good}/{samples}, per-k {perk}")


def partB(N, samples, rng):
    """two-level: delta in V_{k*} (A = [N]\\{k*}), eta sparse with eta notin V_{k*}."""
    P = prod(PR[:N]); n = P * P; sk = [n // p for p in PR[:N]]
    print(f"\nPart B  N={N} n={n}  (two-level necessary condition, samples={samples})")
    Ms = [random_nc_matching(n, rng) for _ in range(samples)] + [adjacent(n, 0), adjacent(n, 1)]
    kstar = N - 1
    cases = []
    # delta: orbits of shifts that are multiples of ... invariant under s_{k*}: sum over j != k* of orbit(n/(p_j p_k*))
    if N == 2:   # delta in V_{k*} only: one s_{k*}-orbit
        delta = orbit_ind(n, rng.randrange(n), sk[kstar])
    else:
        delta = sum(orbit_ind(n, rng.randrange(n), n // (PR[j] * PR[kstar])) for j in range(N) if j != kstar)
    for ename in ('e_q', 'orbit n/(prod others)'):
        if ename == 'e_q':
            eta = np.zeros(n, dtype=np.int64); eta[rng.randrange(n)] = 1
        else:
            eta = orbit_ind(n, rng.randrange(n), n // prod(PR[j] for j in range(N) if j != kstar))
        cases.append((ename, delta, eta))
    for ename, delta, eta in cases:
        A = [k for k in range(N) if not periodic(delta, n, sk[k])]
        prim = all(not periodic(1000 * delta + eta, n, s) for s in sk)
        good = 0
        for M in Ms:
            ok = all(not in_VkLM(delta, M, n, sk[k]) for k in A) and \
                 all(not in_VkLM_extra(eta, M, n, sk[k], [delta]) for k in range(N) if k not in A)
            good += ok
        lastok = good  # includes adjacent
        print(f"  delta=sum orbits (A={[PR[k] for k in A]}), eta={ename:22s} prim={prim}: "
              f"M satisfying 2-level condition {good}/{len(Ms)}")


def partC(rng):
    """Lemma G6: a primitive y in (V_2 + L(M0)) cap (V_3 + L(M1)) at n = 36 (dimension 27+24-36 >= 15)."""
    n = 36
    def basis_V(s): return [np.array([1 if i % s == r else 0 for i in range(n)]) for r in range(s)]
    def basis_L(M):
        out = []
        for p, q in M:
            v = np.zeros(n, dtype=np.int64); v[p] = v[q] = 1; out.append(v)
        return out
    import sympy as sp
    B1 = sp.Matrix(np.array(basis_V(18) + basis_L(adjacent(n, 0))).T)
    B2 = sp.Matrix(np.array(basis_V(12) + basis_L(adjacent(n, 1))).T)
    # intersection of column spaces: solve B1 a = B2 b
    K = sp.Matrix.hstack(B1, -B2).nullspace()
    found = None
    for _ in range(50):
        c = [rng.randint(-2, 2) for _ in K]
        sol = sum((ci * v for ci, v in zip(c, K)), sp.zeros(K[0].rows, 1))
        y = B1 * sol[:B1.cols, :]
        y = np.array([int(v) for v in y])
        if all(not periodic(y, n, s) for s in (18, 12)) and y.any():
            found = y; break
    dimI = len(K)
    print(f"\nPart C  n=36: dim of (V_2+L(M0)) cap (V_3+L(M1)) kernel = {dimI}; primitive y found: {found is not None}")
    if found is not None:
        print("  y =", found.tolist())
        print("  M0 certifies all k:", not any(in_VkLM(found, adjacent(n, 0), n, s) for s in (18, 12)),
              " M1:", not any(in_VkLM(found, adjacent(n, 1), n, s) for s in (18, 12)))
        Ms = [random_nc_matching(n, rng) for _ in range(300)]
        g = sum(not any(in_VkLM(found, M, n, s) for s in (18, 12)) for M in Ms)
        print(f"  random NC matchings certifying it: {g}/300")


if __name__ == '__main__':
    s36 = int(sys.argv[1]) if len(sys.argv) > 1 else 300
    s900 = int(sys.argv[2]) if len(sys.argv) > 2 else 40
    rng = random.Random(1)
    partA(2, s36, rng)
    partA(3, s900, rng)
    partB(2, s36, rng)
    partB(3, s900, rng)
    partC(rng)
