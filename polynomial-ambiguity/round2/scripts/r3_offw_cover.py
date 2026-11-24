"""r3_offw_cover.py -- coverage of the fold certificate vs Off and Q; structural spot checks.

Fold(w): exists m in 0..n-1 such that, with d = (x_l - x_r on mirror pairs of u = w[:m+1]) ++
(x_r - x_l on mirror pairs of v = w[m+1:]), d >= 0 with some d > 0, or d <= 0 with some d < 0.
(x = b-indicator.)  This is exactly L(G_fold) (checked against the grammar in r3_offw_fold.py).

Prints:
  1. exhaustive |Q_n|, |Off_n|, |Fold_n|, |Off_n \\ Fold_n|, max #certs, n <= NMAX
  2. Monte-Carlo fraction of uniform random words in Fold, n up to 400
  3. families from earlier reports: Thm W words a^{n-2}bb (6|n), l6 U_k words a^6(b^k a^k)^6
  4. min support of a nonzero vector in W_n^perp (= 2^omega(n) claimed), by MILP
[computational]
"""
import sys, random
import numpy as np, sympy
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from r3_offw_fold import off_mask, prim_mask

def fold_counts(X):
    N, n = X.shape
    cnt = np.zeros(N, dtype=np.int64)
    for m in range(n):
        L = n - m - 1
        du = [X[:, k] - X[:, m - k] for k in range((m + 1) // 2)]
        dv = [X[:, n - 1 - k] - X[:, m + 1 + k] for k in range(L // 2)]
        D = du + dv
        if not D:
            continue
        D = np.stack(D, 1)
        pos = np.all(D >= 0, 1) & np.any(D > 0, 1)
        neg = np.all(D <= 0, 1) & np.any(D < 0, 1)
        cnt += pos + neg
    return cnt

def xhat1(w):
    n = len(w)
    return sum(np.exp(2j * np.pi * k / n) for k in range(n) if w[k] == 'b')

def to_X(ws):
    return np.array([[1 if c == 'b' else 0 for c in w] for w in ws], dtype=np.int64)

if __name__ == '__main__':
    NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    print('1. exhaustive')
    print(' n   |Q_n|    |Off_n|  |Q-Off|  |Fold_n|  |Off-Fold|  Fold/Off  maxcerts')
    for n in range(2, NMAX + 1):
        off, X = off_mask(n); prim = prim_mask(n, X)
        c = fold_counts(X); fold = c > 0
        assert not np.any(fold & ~off) and not np.any(off & ~prim)
        print(f'{n:2d} {int(prim.sum()):8d} {int(off.sum()):8d} {int((prim & ~off).sum()):6d} {int(fold.sum()):9d} '
              f'{int((off & ~fold).sum()):8d}  {fold.sum() / off.sum():8.4f} {int(c.max()):6d}')
        if n in (9, 12):
            miss = np.where(off & ~fold)[0][:6]
            print('     sample Off\\Fold:', [''.join('b' if X[i, k] else 'a' for k in range(n)) for i in miss])
    print('2. Monte Carlo (uniform random words, 4000 samples)')
    rng = np.random.default_rng(0)
    for n in (24, 32, 48, 64, 96, 128, 200, 400):
        X = rng.integers(0, 2, size=(4000, n))
        f = (fold_counts(X) > 0).mean()
        print(f'   n={n:4d}  Pr[Fold] = {f:.4f}')
    print('3. families')
    for m in range(1, 8):
        n = 6 * m; w = 'a' * (n - 2) + 'bb'
        print(f'   ThmW a^(n-2)bb n={n}: |xhat(1)|={abs(xhat1(w)):.3f}  fold certs={int(fold_counts(to_X([w]))[0])}')
    for k in range(1, 6):
        w = 'a' * 6 + ('b' * k + 'a' * k) * 6
        n = len(w)
        print(f'   l6 U_k k={k} n={n}: |xhat(1)|={abs(xhat1(w)):.3f}  fold certs={int(fold_counts(to_X([w]))[0])}')
    print('4. min support of nonzero y in W_n^perp (MILP; y_0 = 1 by rotation)')
    from scipy.optimize import milp, LinearConstraint, Bounds
    for n in (6, 10, 12, 15, 18, 30, 42, 60):
        z = sympy.symbols('z')
        g = sympy.Poly(sympy.cancel((z**n - 1) / sympy.cyclotomic_poly(n, z)), z)
        # W_n^perp = { y : yhat(j) = 0 for gcd(j,n) > 1 } ; real constraints: y orthogonal to all
        # n/p-periodic vectors, p | n  <=> class sums mod n/p vanish
        rows = []
        for p in sympy.primefactors(n):
            s = n // p
            for r in range(s):
                row = np.zeros(n); row[r::s] = 1; rows.append(row)
        A = np.array(rows)
        M = 1000.0
        # vars: y (n, free in [-M,M]), s (n, binary); minimize sum s
        cobj = np.concatenate([np.zeros(n), np.ones(n)])
        cons = [LinearConstraint(np.hstack([A, np.zeros_like(A)]), 0, 0)]
        I = np.eye(n)
        cons.append(LinearConstraint(np.hstack([I, -M * I]), -np.inf, 0))
        cons.append(LinearConstraint(np.hstack([-I, -M * I]), -np.inf, 0))
        e0 = np.zeros(2 * n); e0[0] = 1
        cons.append(LinearConstraint(e0[None, :], 1, 1))
        lb = np.concatenate([-M * np.ones(n), np.zeros(n)]); ub = np.concatenate([M * np.ones(n), np.ones(n)])
        res = milp(cobj, constraints=cons, bounds=Bounds(lb, ub),
                   integrality=np.concatenate([np.zeros(n), np.ones(n)]))
        om = len(sympy.primefactors(n))
        print(f'   n={n:3d} omega={om}  min support={round(res.fun)}  2^omega={2**om}')
