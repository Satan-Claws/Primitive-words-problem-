"""R5-B DENSE-SOUND: the interval fold certificate F_K and the Bezout window lemma.

d_k(w) = #a(w[0,k)) - #a(w[n-k,n))   (prefix vs suffix a-count), 1 <= k <= n/2.
F_K = { w : d_k(w) != 0 for all k in K_n },  K_n = [ceil(n/3), floor(n/2)].
Lemma F: F_K subset of Q (if w=u^p, k=floor(p/2)*n/p in K_n and prefix_k = suffix_k).
Variant F_delta: K = [ceil((1/2-delta) n), floor(n/2)] plus k = floor(p/2) n/p for primes p | n, p <= 1/delta.
Usage: python r5_dense_fold.py [nmax_exh=22] [mc_samples=4000]
"""
import sys, itertools, math
import numpy as np

def is_prim(s):
    n = len(s)
    return all(s != s[:d] * (n // d) for d in range(1, n) if n % d == 0)

def primes_upto(m):
    return [p for p in range(2, m + 1) if all(p % q for q in range(2, int(p**.5) + 1))]

def Kset(n, delta=None):
    if delta is None:
        return list(range(-(-n // 3), n // 2 + 1))
    lo = math.ceil((0.5 - delta) * n)
    K = set(range(max(lo, 1), n // 2 + 1))
    for p in primes_upto(int(1 / delta) + 2):
        if n % p == 0:
            K.add((p // 2) * (n // p))
    return sorted(K)

def dvec(x):
    """x: (..., n) 0/1 array of a-indicators. returns d_k for k = 0..n//2"""
    n = x.shape[-1]
    pre = np.concatenate([np.zeros(x.shape[:-1] + (1,), int), np.cumsum(x, -1)], -1)
    suf = np.concatenate([np.zeros(x.shape[:-1] + (1,), int), np.cumsum(x[..., ::-1], -1)], -1)
    return (pre - suf)[..., : n // 2 + 1]

def in_F(x, K):
    d = dvec(x)
    return np.all(d[..., K] != 0, -1)

def exhaustive(nmax):
    print("n  |F_K|/2^n  |F_K|/|Q_n|  sound   |F_.1|/2^n")
    for n in range(2, nmax + 1):
        X = ((np.arange(2**n)[:, None] >> np.arange(n)[::-1]) & 1).astype(np.int8)
        K = Kset(n)
        m = in_F(X, K)
        m2 = in_F(X, Kset(n, 0.1))
        # soundness: every accepted word primitive
        bad = 0
        nonprim = set()
        for d in range(1, n):
            if n % d == 0:
                for u in range(2**d):
                    s = format(u, f'0{d}b') * (n // d)
                    nonprim.add(int(s, 2))
        idx = np.nonzero(m | m2)[0]
        bad = sum(1 for i in idx if int(i) in nonprim)
        Qn = 2**n - len(nonprim)
        print(f"{n:2d}  {m.mean():.4f}   {m.sum()/Qn:.4f}    {'OK' if bad==0 else 'BAD %d'%bad}   {m2.mean():.4f}")

def mc(ns, S, rng):
    print("MC: n  dens(F_K)  dens(F_0.1)  dens(F_0.02)  [BM limit F_K: %.4f]" % (2/math.pi*math.asin(math.sqrt(2/3))))
    for n in ns:
        X = (rng.random((S, n)) < .5).astype(np.int8)
        r = [in_F(X, Kset(n, dl)).mean() for dl in (None, .1, .02)]
        se = math.sqrt(r[0]*(1-r[0])/S)
        print(f"   {n:6d}  {r[0]:.4f}+-{se:.4f}  {r[1]:.4f}  {r[2]:.4f}")

def bezout_window_check(nmax):
    """gcd(A,B)=1  <=>  exists cyclic factor x with n*#a(x) - A*|x| = +-1  (Lemma B)."""
    for n in range(2, nmax + 1):
        bad = 0
        for u in range(2**n):
            s = [(u >> i) & 1 for i in range(n)]
            A = sum(s); B = n - A
            ss = s + s
            hit = False
            for i in range(n):
                c = 0
                for l in range(1, n):
                    c += ss[i + l - 1]
                    if abs(n * c - A * l) == 1:
                        hit = True; break
                if hit: break
            if hit != (math.gcd(A, B) == 1):
                bad += 1
        print(f"Lemma B check n={n}: {'OK' if bad==0 else 'BAD %d'%bad}")

if __name__ == "__main__":
    nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 22
    S = int(sys.argv[2]) if len(sys.argv) > 2 else 4000
    exhaustive(nmax)
    mc([64, 256, 1024, 4096, 10000, 16384], S, np.random.default_rng(1))
    bezout_window_check(14)
