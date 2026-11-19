"""fold agent: line certificates n - 4 m_c = R over all reflection axes c.
m_c = |w|_b - (w circconv w)[c]  (number of mismatched mirror pairs of axis i <-> c-i).
Usage: python3 lines.py exact NMAX | mc N1,N2,... SAMPLES"""
import sys, math, numpy as np
from math import gcd

def targets(n):
    """line certificates (one or two values of m with gcd(m,n)=1 guaranteed by n=4m+R)."""
    r = n % 8
    if n % 2 == 1:
        T = [m for m in ((n-1)//4, (n+1)//4) if 4*m in (n-1, n+1)]
    elif r == 2: T = [(n+2)//4]
    elif r == 6: T = [(n-2)//4]
    elif r == 0: T = [n//4 - 1, n//4 + 1]
    else: T = [n//4 - 2, n//4 + 2]
    for m in T: assert gcd(m, n) == 1, (n, m)
    return T

def mvals_all(n):
    """array (2^n, n) of m_c for every word (bit i of the index = w_i)."""
    N = 1 << n
    idx = np.arange(N, dtype=np.int64)
    bits = [((idx >> i) & 1).astype(np.int8) for i in range(n)]
    nb = sum(b.astype(np.int16) for b in bits)
    M = np.empty((N, n), dtype=np.int16)
    for c in range(n):
        conv = np.zeros(N, dtype=np.int16)
        for i in range(n):
            conv += bits[i] & bits[(c - i) % n]
        M[:, c] = nb - conv
    return M, idx

def is_prim(w, n):
    for d in range(1, n):
        if n % d == 0 and all(w[i] == w[i % d] for i in range(n)):
            return False
    return True

def exact(nmax):
    print("n  targets  P(central axis c=n-1 on line)  P(some axis on line)  P(some axis on line, vertex-type only)  P(G: some gcd(m_c,n)=1)  #nonprim-hit")
    for n in range(3, nmax + 1):
        T = targets(n)
        M, idx = mvals_all(n)
        hit = np.isin(M, T)
        anyhit = hit.any(axis=1)
        vt = hit[:, 0::2].any(axis=1) if n % 2 == 0 else anyhit
        cop = np.vectorize(lambda x: gcd(int(x), n) == 1)(np.arange(n + 1))
        G = cop[M].any(axis=1)
        # soundness: non-primitive words never hit
        bad = 0
        for d in range(1, n):
            if n % d == 0:
                for u in range(1 << d):
                    x = 0
                    for k in range(n // d): x |= u << (k * d)
                    if anyhit[x]: bad += 1
        N = 1 << n
        print(n, T, round(hit[:, n-1].sum()/N, 4), round(anyhit.sum()/N, 4), round(vt.sum()/N, 4), round(G.sum()/N, 4), bad, flush=True)

def mc(ns, S, seed=1):
    rng = np.random.default_rng(seed)
    print("n  targets  sqrt(n)*P(fixed axis)  P(some axis)  1-P(some)  sqrt(n)*(1-P)  P(some vertex-type axis)  mean#axes-on-line/sqrt(n)")
    for n in ns:
        T = targets(n)
        W = rng.integers(0, 2, size=(S, n)).astype(np.float64)
        F = np.fft.rfft(W, axis=1)
        conv = np.rint(np.fft.irfft(F * F, n=n, axis=1)).astype(np.int64)
        M = W.sum(axis=1, keepdims=True).astype(np.int64) - conv
        hit = np.isin(M, T)
        p_fix = hit[:, n-1].mean()
        anyp = hit.any(axis=1).mean()
        vt = hit[:, 0::2].any(axis=1).mean() if n % 2 == 0 else anyp
        print(n, T, round(p_fix*math.sqrt(n), 3), round(anyp, 4), round(1-anyp, 4), round((1-anyp)*math.sqrt(n), 3), round(vt, 4), round(hit.sum(axis=1).mean()/math.sqrt(n), 3), flush=True)

if __name__ == "__main__":
    if sys.argv[1] == "exact": exact(int(sys.argv[2]))
    else: mc([int(x) for x in sys.argv[2].split(",")], int(sys.argv[3]))
