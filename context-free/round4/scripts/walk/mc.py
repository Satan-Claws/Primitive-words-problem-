# Monte Carlo density of T^k(E') (odd n) and T^k(E'uG) (all n), numpy.
import numpy as np, sys
rng = np.random.default_rng(1)
def phi(v):
    D = int(v.sum())
    if D == 0: return None
    if D < 0: v = -v
    S = np.concatenate(([0], np.cumsum(v)))[:-1]
    arg = int(np.argmax(S))
    u = np.roll(v, -arg)
    S = np.cumsum(u)
    prevmax = np.maximum.accumulate(np.concatenate(([0], S[:-1])))
    rec = np.nonzero(S > prevmax)[0]           # piece end times
    starts = np.concatenate(([0], rec[:-1] + 1))
    out = np.where(rec == starts, 1, -1)
    # g-weight: piece 'a' ->1 ; starts 'ba' -> -2 ; 'bb' -> 0
    second = np.where(rec > starts, u[np.minimum(starts + 1, len(u)-1)], 0)
    g = np.where(rec == starts, 1, np.where(second == 1, -2, 0))
    return out, int(g.sum())
def certE(v): return abs(int(v.sum())) == 1
def certEG(v):
    if abs(int(v.sum())) == 1: return True
    r = phi(v); return r is not None and abs(r[1]) == 1
def T(c):
    def f(v):
        r = phi(v); return r is not None and c(r[0])
    return f
K = 3
for n in [int(x) for x in sys.argv[2:]]:
    reps = int(sys.argv[1])
    hits = np.zeros((2, K+1))
    for _ in range(reps):
        v = rng.choice(np.array([1, -1]), n)
        for base in range(2):
            c = certE if base == 0 else certEG
            for k in range(K+1):
                if c(v): hits[base, k] += 1
                c = T(c)
    d = hits / reps
    print(n, "T^k(E'),k=0..3:", ' '.join(f"{x:.3f}" for x in d[0]),
          "| T^k(E'uG):", ' '.join(f"{x:.3f}" for x in d[1]), flush=True)
