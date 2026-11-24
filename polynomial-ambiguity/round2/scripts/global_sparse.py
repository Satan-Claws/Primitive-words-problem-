"""global_sparse: checks for R2/global.md §§3-4 (sparse multi-type defects near U; matching pieces; spread lemma).

x = t*1 + 1_D + 1_T on (ab*)^n, n = P_N^2:  D = {z, z+n/2} (a V_2-cycle), T = {w, w+n/3, w+2n/3} (a V_3-cycle).
 (a) x in W_n, x primitive (for every k some b with x_b != x_{b+n/p_k}), delta = 1_D+1_T has 5-point support,
     delta not in (+)E_k (+) U  (it has a nonzero component in ANOVA sets T with |T| <= N-2 once N >= 3).
 (b) Prop G2 (pigeonhole) is a proof; we print |supp delta| = 5 < N for N >= 6.
 (c) Prop G3: matching piece P* = 1_{D u T} + N M, M = {e_{2b}+e_{2b+1}}: for every k an explicit certificate
     mu_k = (1-T^{m s_k})(delta_{b0} - delta_{b0+1})  (b0 even): mu_k _|_ V_{p_k}, mu_k(M) = 0, mu_k(1_{DuT}) != 0.
     Then mu_k is constant != 0 on P*, so P* misses V_{p_k}.  Done symbolically for N = 2..8 (no length-n arrays).
 (d) exact small check n = 36 (N=2) and n = 900 (N=3): rank test 1_{DuT} not in span(M) + V_p for all p, and
     brute force: no point of 1_{DuT} + {0..3}^M-combinations (random sample) is periodic.
 (e) spread lemma: deg lcm_{k in K}(X^{n/p_k}-1) = n(1 - prod_{k in K}(1-1/p_k))  (sympy, n = 36, 900).
Usage: .venv/bin/python global_sparse.py
"""
import random, itertools
from math import prod
import numpy as np
import sympy as sp

PR = [2, 3, 5, 7, 11, 13, 17, 19]


def setup(N, rng):
    P = prod(PR[:N]); n = P * P
    while True:
        z = rng.randrange(n); w = rng.randrange(n)
        D = {z, (z + n // 2) % n}; T = {w, (w + n // 3) % n, (w + 2 * n // 3) % n}
        if len(D | T) == 5: return P, n, D, T


def xval(b, D, T, t):
    return t + (b in D) + (b in T)


def part_ac(N, rng, t=10 ** 6):
    P, n, D, T = setup(N, rng)
    S = D | T
    prim = []
    for k in range(N):
        s = n // PR[k]
        prim.append(any(xval(b, D, T, t) != xval((b + s) % n, D, T, t) for b in S))
    # (c) certificates
    certs = []
    for k in range(N):
        s = n // PR[k]; ok = False
        for b in sorted(S):
            b0 = b - (b % 2)
            for mm in range(1, PR[k]):
                sh = (mm * s) % n
                pts = {b0: 1, b0 + 1: -1, (b0 + sh) % n: -1, (b0 + 1 + sh) % n: 1}
                if len(pts) < 4: continue
                # mu _|_ V_{p_k}: the two k-cycle pairs (b0, b0+sh), (b0+1, b0+1+sh) carry +1/-1  [sh = mm*n/p_k]
                # mu(M)=0: pairs (b0,b0+1) and (b0+sh, b0+sh+1) are M-pairs since b0, sh even
                assert b0 % 2 == 0 and sh % 2 == 0
                val = sum(c * ((q in D) + (q in T)) for q, c in pts.items())
                if val != 0: ok = True; certs.append((k, b0, mm, val)); break
            if ok: break
        if not ok: certs.append((k, None))
    return dict(N=N, n=n, supp_delta=len(S), primitive=all(prim), cert_all_k=all(c[1] is not None for c in certs),
                pigeonhole_blocks_pair_facets=(len(S) < N))


def part_d(N, rng, samples=2000):
    P, n, D, T = setup(N, rng)
    S = D | T
    r = np.zeros(n); r[list(S)] = 1
    M = np.zeros((n, n // 2))
    for b in range(n // 2): M[2 * b, b] = 1; M[2 * b + 1, b] = 1
    out = {}
    for p in PR[:N]:
        s = n // p
        Vp = np.zeros((n, s))
        for j in range(n): Vp[j, j % s] = 1
        A = np.hstack([M, Vp])
        r1 = np.linalg.matrix_rank(A); r2 = np.linalg.matrix_rank(np.hstack([A, r[:, None]]))
        out[p] = (r2 > r1)
    # brute force sample of points of P*
    viol = 0
    for _ in range(samples):
        q = np.array([rng.randrange(4) for _ in range(n // 2)])
        x = r + np.repeat(q, 2)
        for p in PR[:N]:
            s = n // p
            if np.array_equal(x, np.roll(x, s)): viol += 1
    return dict(N=N, n=n, outside_spanM_plus_Vp=out, periodic_hits_in_sample=viol)


def part_e(N):
    P = prod(PR[:N]); n = P * P; X = sp.symbols('X')
    res = []
    for r in range(1, N + 1):
        for K in itertools.combinations(range(N), r):
            L = sp.Integer(1)
            for k in K: L = sp.lcm(L, X ** (n // PR[k]) - 1)
            d = sp.degree(L, X)
            pred = n * (1 - prod(sp.Rational(PR[k] - 1, PR[k]) for k in K))
            res.append(d == pred)
    return dict(N=N, n=n, spread_degree_formula_ok=all(res), cases=len(res))


if __name__ == '__main__':
    rng = random.Random(7)
    for N in range(2, 9):
        print(part_ac(N, rng))
    for N in (2, 3):
        print(part_d(N, rng, samples=2000 if N == 2 else 300))
    for N in (2, 3):
        print(part_e(N))
