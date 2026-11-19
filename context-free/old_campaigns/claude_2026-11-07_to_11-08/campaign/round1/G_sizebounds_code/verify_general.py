r"""Alphabet-general exhaustive check (digit arrays) of
 (1) the cyclic O(n) balanced cover  (Theorem 2), and
 (2) the LINEAR window identity (Theorem 3):
     n odd : Q_n = U_{t in T} Sigma^t L(lam,D) Sigma^{n-lam-t}
     n even: Q_n = U_t [ Sigma^t (L(lam,D)) Sigma^* ]  U  U_{t,i,a} [window avoids E, w_i=a, w_{i+n/2}!=a]
   with non-wrapping windows [t,t+lam), T = {0,s,2s,...} ∪ {n-lam}.
"""
import numpy as np, itertools, sys

def divisors(n): return [d for d in range(1, n) if n % d == 0]

def all_words(n, k):
    idx = np.arange(k ** n, dtype=np.int64)
    W = np.empty((k ** n, n), dtype=np.int8)
    for j in range(n):
        W[:, j] = idx % k; idx //= k
    return W

def prim(W):
    n = W.shape[1]
    ok = np.ones(len(W), bool)
    for p in [p for p in range(2, n + 1) if n % p == 0 and all(p % q for q in range(2, p))]:
        ok &= np.any(W != np.roll(W, -(n // p), axis=1), axis=1)
    return ok

def has_period(X, d):
    L = X.shape[1]
    if d >= L: return np.ones(len(X), bool)
    return np.all(X[:, :L - d] == X[:, d:], axis=1)

def params(n):
    D = divisors(n); E = [d for d in D if 2 * d != n]
    Es = sorted(E, reverse=True)
    M1 = Es[0] if Es else 0; M2 = Es[1] if len(Es) > 1 else 0
    lam = (2 * n) // 3
    s = lam - max(M1 + M2 - 1, M1)
    return D, E, lam, s

def check(n, k, linear):
    D, E, lam, s = params(n)
    W = all_words(n, k); P = prim(W)
    if linear:
        T = sorted(set(list(range(0, n - lam + 1, s)) + [n - lam]))
    else:
        T = list(range(0, n, s))
    cov = np.zeros(len(W), bool); nrect = 0
    h = n // 2
    for t in T:
        idxs = [(t + o) % n for o in range(lam)]
        X = W[:, idxs]
        aE = np.ones(len(W), bool)
        for d in E: aE &= ~has_period(X, d)
        if n % 2:
            cov |= aE; nrect += 1; continue
        cov |= aE & ~has_period(X, h); nrect += 1
        for o in range(lam):
            i = idxs[o]
            if linear:
                for j in (i + h, i - h):
                    if 0 <= j < n and not (t <= j < t + lam):
                        for a in range(k):
                            cov |= aE & (W[:, i] == a) & (W[:, j] != a); nrect += 1
            else:
                j = (i + h) % n
                if (j - t) % n < lam: continue
                for a in range(k):
                    cov |= aE & (W[:, i] == a) & (W[:, j] != a); nrect += 1
    return (not np.any(cov & ~P)), (not np.any(P & ~cov)), len(T), nrect

if __name__ == "__main__":
    for k, N in [(2, 20), (3, 12)]:
        for n in range(2, N + 1):
            for linear in (False, True):
                snd, cmp_, r, nr = check(n, k, linear)
                print(f"|Sigma|={k} n={n:2d} {'linear' if linear else 'cyclic'}: windows={r} rects={nr} sound={snd} complete={cmp_}", flush=True)
