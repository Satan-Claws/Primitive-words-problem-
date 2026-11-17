"""Exact FRACTIONAL rectangle-cover number of Q_n at a single split, small n.

Matrix M[y, z] = [ y z is primitive ],  y in {a,b}^l (positions 0..l-1), z in {a,b}^{n-l}.
A (1-)rectangle is A x B with A x B subset of the 1-entries.  We compute

    C*(n, l) = min sum_R x_R  s.t.  sum_{R containing e} x_R >= 1 for each 1-entry e,  x >= 0

by column generation.  Pricing (max_R sum_{e in R} mu_e) is solved exactly by a MILP
(scipy.optimize.milp / HiGHS) once a fast local-search heuristic fails, so the final value
is certified optimal: at termination the LP dual mu is a distribution-like weighting with
max_R mu(R) <= 1 (checked by the exact MILP) and sum mu = C*.

Equivalently 1/C* = max over probability distributions mu on Q_n of min over ... no:
1/C* = min_mu max_R mu(R) (LP duality), the best possible "hard distribution" bound
for this split.  Theorem 3 of the report says C* <= 4^{omega(n)}.

Also reports a greedy integer cover size (upper bound on the cover number).
Usage: python3 split_lp.py n l
"""
import sys, time, math
import numpy as np
from scipy.optimize import linprog, milp, LinearConstraint, Bounds
from scipy.sparse import csr_matrix, lil_matrix
from common import primitive_mask, prime_factors


def build(n, l):
    P = primitive_mask(n)
    R, C = 1 << l, 1 << (n - l)
    y = np.arange(R)[:, None]
    z = np.arange(C)[None, :]
    M = P[(y | (z << l))]
    return M


def heuristic_price(M, mu, rng, starts=60, iters=8, collect=None):
    """Local search for a 1-rectangle with large mu-weight. mu given as matrix (0 on 0-entries).
    If collect is a list, every found rectangle of weight > 1 + 1e-7 is appended to it."""
    R, C = M.shape
    zero = ~M
    best_val, best = -1.0, None
    for s in range(starts):
        # random seed: pick a random 1-entry with positive weight
        pos = np.argwhere(mu > 0)
        if len(pos) == 0:
            return 0.0, None
        y0, z0 = pos[rng.integers(len(pos))]
        A = np.zeros(R, bool); A[y0] = True
        for _ in range(iters):
            # best columns given A: compatible columns with positive gain
            compat = ~zero[A].any(axis=0)
            gain = mu[A].sum(axis=0)
            B = compat & (gain > 0)
            if not B.any():
                break
            compatr = ~zero[:, B].any(axis=1)
            gainr = mu[:, B].sum(axis=1)
            A2 = compatr & (gainr > 0)
            if (A2 == A).all():
                break
            A = A2
        compat = ~zero[A].any(axis=0)
        B = compat & (mu[A].sum(axis=0) > 0)
        val = mu[np.ix_(A, B)].sum()
        if collect is not None and val > 1 + 1e-7:
            collect.append((A.copy(), B.copy()))
        if val > best_val:
            best_val, best = val, (A.copy(), B.copy())
    return best_val, best


def exact_price(M, mu):
    """MILP: max sum mu_e z_e, z_e <= a_y, z_e <= b_z, a_y + b_z <= 1 on 0-entries."""
    R, C = M.shape
    pos = np.argwhere((mu > 1e-12) & M)
    m = len(pos)
    nv = R + C + m
    c = np.zeros(nv)
    c[R + C:] = -mu[pos[:, 0], pos[:, 1]]
    rows = []
    # z_e - a_y <= 0 ; z_e - b_z <= 0
    A = lil_matrix((2 * m + int((~M).sum()), nv))
    r = 0
    for i, (yy, zz) in enumerate(pos):
        A[r, R + C + i] = 1; A[r, yy] = -1; r += 1
        A[r, R + C + i] = 1; A[r, R + zz] = -1; r += 1
    for (yy, zz) in np.argwhere(~M):
        A[r, yy] = 1; A[r, R + zz] = 1; r += 1
    ub = np.concatenate([np.zeros(2 * m), np.ones(r - 2 * m)])
    cons = LinearConstraint(csr_matrix(A), -np.inf, ub)
    integrality = np.concatenate([np.ones(R + C), np.zeros(m)])
    res = milp(c, constraints=cons, integrality=integrality, bounds=Bounds(0, 1),
               options={"time_limit": 600})
    a = res.x[:R] > 0.5
    b = res.x[R:R + C] > 0.5
    return -res.fun, (a, b), res


def rect_to_col(M, A, B, idx):
    """Column vector over 1-entries."""
    sub = np.zeros_like(M)
    sub[np.ix_(A, B)] = True
    assert not (sub & ~M).any()
    return sub[M]


def parity_rectangles(n, l, rng, ntests):
    """Rectangles from the affine-cover construction at split l (Theorem 3)."""
    from common import class_matrix_tests
    R, C = 1 << l, 1 << (n - l)
    ys = np.arange(R, dtype=np.uint64)
    zs = np.arange(C, dtype=np.uint64)
    out = []
    for _ in range(ntests):
        tup = class_matrix_tests(n, rng)
        k = len(tup)
        py = np.stack([(np.bitwise_count(ys & np.uint64(s & (R - 1))) & 1) for s in tup])  # k x R
        pz = np.stack([(np.bitwise_count(zs & np.uint64(s >> l)) & 1) for s in tup])
        for alpha in range(1 << k):
            al = np.array([(alpha >> i) & 1 for i in range(k)])[:, None]
            A = (py == al).all(axis=0)
            B = (pz == 1 - al).all(axis=0)
            if A.any() and B.any():
                out.append((A, B))
    return out


def solve(n, l, seed=1, verbose=True):
    rng = np.random.default_rng(seed)
    M = build(n, l)
    ones = M.sum()
    cols = []
    for A, B in parity_rectangles(n, l, rng, 8 * 4 ** len(prime_factors(n))):
        cols.append(rect_to_col(M, A, B, None))
    # make sure everything is covered (add singleton rectangles if needed)
    covered = np.zeros(ones, bool)
    for cvec in cols:
        covered |= cvec
    if not covered.all():
        # add row-singleton rectangles
        for yy in range(M.shape[0]):
            A = np.zeros(M.shape[0], bool); A[yy] = True
            cols.append(rect_to_col(M, A, M[yy], None))
    it = 0
    t0 = time.time()
    while True:
        it += 1
        Amat = csr_matrix(np.array(cols).T.astype(float))
        res = linprog(np.ones(len(cols)), A_ub=-Amat, b_ub=-np.ones(ones), bounds=(0, None), method="highs")
        val = res.fun
        mu_vec = -res.ineqlin.marginals
        mu = np.zeros(M.shape)
        mu[M] = mu_vec
        found = []
        hv, hr = heuristic_price(M, mu, rng, starts=200, collect=found)
        if hv > 1 + 1e-7:
            seen = set()
            for (A, B) in found:
                key = (A.tobytes(), B.tobytes())
                if key not in seen:
                    seen.add(key)
                    cols.append(rect_to_col(M, A, B, None))
            continue
        ev, er, _ = exact_price(M, mu)
        if verbose:
            print(f"  iter {it}: LP={val:.6f}, heuristic={hv:.6f}, exact pricing={ev:.6f}, cols={len(cols)}, {time.time()-t0:.0f}s", flush=True)
        if ev > 1 + 1e-7:
            cols.append(rect_to_col(M, er[0], er[1], None))
            continue
        return val, mu, M, cols


def greedy_integer_cover(M, rng, rounds=400):
    """Greedy cover where each step takes the best of many heuristic rectangles (uniform weights on uncovered)."""
    unc = M.copy()
    cnt = 0
    while unc.any():
        mu = unc.astype(float)
        v, (A, B) = heuristic_price(M, mu, rng, starts=rounds)
        unc[np.ix_(A, B)] = False
        cnt += 1
    return cnt


if __name__ == "__main__":
    n = int(sys.argv[1]); l = int(sys.argv[2])
    k = len(prime_factors(n))
    val, mu, M, cols = solve(n, l)
    rng = np.random.default_rng(5)
    g = greedy_integer_cover(M, rng)
    print(f"RESULT n={n} l={l} k={k}: C*={val:.6f}  (bound 4^k={4**k}),  1/C*={1/val:.6f};  greedy integer cover={g};  "
          f"#1-entries={M.sum()}  #0-entries={(~M).sum()}")
