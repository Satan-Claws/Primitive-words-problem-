"""Exhaustive check of the AFFINE COVER THEOREM for small n.

Theorem (see reports/rectangles.md, Thm 2): for a test tuple (s_p)_{p|n}, s_p in S_p,
    T = { w in {0,1}^n : <w, s_p> = 1 for all primes p | n }
is contained in Q_n, and a uniformly random tuple contains a fixed w in Q_n with
probability exactly 2^{-k}, k = omega(n). Hence Q_n is a union of
<= ceil(2^k n ln 2) such affine subspaces.

This script, for each n in the list:
  (a) checks T subset Q_n exhaustively for many random tuples,
  (b) checks Pr[w in T] = 2^{-k} for random w in Q_n (empirically),
  (c) covers Q_n greedily by random T's (keep a T only if it covers something new)
      and reports the number used versus the probabilistic bound ceil(2^k n ln 2),
  (d) also runs a *greedy-best-of-B* cover to see how small the cover can get.
Usage: python3 affine_cover.py [nmax]
"""
import sys, math, time
import numpy as np
from common import prime_factors, primitive_mask, class_matrix_tests, in_S_p, parity_popcount


def run(n, rng, ntest_subset=200, best_of=8):
    k = len(prime_factors(n))
    P = primitive_mask(n)
    allw = np.arange(1 << n, dtype=np.uint64)
    # (a) T subset of Q_n
    for _ in range(ntest_subset):
        tup = class_matrix_tests(n, rng)
        for p, s in zip(prime_factors(n), tup):
            assert in_S_p(s, n, p)
        inT = np.ones(1 << n, dtype=bool)
        for s in tup:
            inT &= parity_popcount(allw & np.uint64(s))
        assert not np.any(inT & ~P), "T not inside Q_n !"
    # (b) empirical probability
    Qidx = np.nonzero(P)[0]
    sample = rng.choice(Qidx, size=min(2000, len(Qidx)), replace=False).astype(np.uint64)
    hits = 0
    trials = 400
    for _ in range(trials):
        tup = class_matrix_tests(n, rng)
        ok = np.ones(len(sample), dtype=bool)
        for s in tup:
            ok &= parity_popcount(sample & np.uint64(s))
        hits += ok.sum()
    emp = hits / (trials * len(sample))
    # (c) random greedy cover
    uncovered = P.copy()
    used = 0
    draws = 0
    while uncovered.any():
        tup = class_matrix_tests(n, rng)
        draws += 1
        inT = np.ones(1 << n, dtype=bool)
        for s in tup:
            inT &= parity_popcount(allw & np.uint64(s))
        if (inT & uncovered).any():
            used += 1
            uncovered &= ~inT
    # (d) greedy best-of-B
    uncovered = P.copy()
    used_best = 0
    while uncovered.any():
        best, bestc = None, -1
        for _ in range(best_of):
            tup = class_matrix_tests(n, rng)
            inT = np.ones(1 << n, dtype=bool)
            for s in tup:
                inT &= parity_popcount(allw & np.uint64(s))
            c = int((inT & uncovered).sum())
            if c > bestc:
                best, bestc = inT, c
        used_best += 1
        uncovered &= ~best
    bound = math.ceil(2 ** k * n * math.log(2))
    return dict(n=n, k=k, Qn=int(P.sum()), emp_prob=emp, exact_prob=2.0 ** -k,
                random_cover=used, random_draws=draws, greedy_cover=used_best, bound=bound)


if __name__ == "__main__":
    nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    rng = np.random.default_rng(12345)
    print("n  k  |Q_n|      Pr[w in T] (emp vs 2^-k)  #T random-greedy (draws)  #T best-of-8  bound ceil(2^k n ln2)")
    for n in range(2, nmax + 1):
        t = time.time()
        r = run(n, rng, ntest_subset=50 if n > 16 else 200)
        print(f"{r['n']:2d} {r['k']}  {r['Qn']:9d}  {r['emp_prob']:.4f} vs {r['exact_prob']:.4f}"
              f"            {r['random_cover']:4d} ({r['random_draws']:5d})         {r['greedy_cover']:4d}        {r['bound']:5d}"
              f"   [{time.time()-t:.1f}s]", flush=True)
