"""R6 fold-miss set: Monte Carlo for large n (uses r6_miss_lib.c).

Usage: python r6_miss_mc.py [S=2000]
 (a) uniform random words: miss rate of every tier (1 - density)
 (b) conditional on gcd(#a,#b) having >= 2 distinct prime factors: #a = A fixed with omega(gcd(A, n-A)) >= 2
     (A = multiple of 6 nearest to n/2; word uniform among those with #a = A)
 (c) miss rate of F_K split by n mod 6 vs residue-dependent window F_W (r6_miss_windows.py)
"""
import ctypes, os, sys, subprocess, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
SO = os.path.join(os.environ.get('TMPDIR', '/tmp'), 'r6miss_mc.so')
subprocess.check_call(['cc', '-O3', '-shared', '-fPIC', '-o', SO, os.path.join(HERE, 'r6_miss_lib.c')])
lib = ctypes.CDLL(SO); lib.eval_tiers.restype = ctypes.c_int
NAMES = ['F_K', 'F_max', 'RotF_K', 'RotF_Kft', 'RotF_max', 'RotF_maxft', 'F_.1', 'RotF_.1', 'F_W', 'RotF_W']

def masks(X):
    out = []
    for x in X:
        buf = (ctypes.c_ubyte * len(x)).from_buffer_copy(np.ascontiguousarray(x, dtype=np.uint8).tobytes())
        out.append(lib.eval_tiers(buf, len(x)))
    return np.array(out)

def report(tag, n, M):
    S = len(M)
    miss = [(1 - ((M >> b) & 1).mean()) for b in range(10)]
    print(f'{tag:5s} n={n:6d} S={S:5d} miss: ' + ' '.join(f'{NAMES[b]}={miss[b]:.4f}' for b in range(10)), flush=True)

if __name__ == '__main__':
    S0 = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
    rng = np.random.default_rng(6)
    ns = [60, 120, 210, 256, 360, 1024, 2310, 4096, 9240, 10000]
    for n in ns:
        S = S0 if n <= 2400 else S0 // 4
        X = (rng.random((S, n)) < .5).astype(np.uint8)
        report('unif', n, masks(X))
        if n % 6 == 0:
            A = 6 * round(n / 12)
            Y = np.zeros((S, n), np.uint8); Y[:, :A] = 1
            Y = rng.permuted(Y, axis=1)
            report('g6|', n, masks(Y))

    # (d) decay of the Rot(F_K) miss rate (large samples, batch C), and the argmax/argmin bound
    lib.eval_batch.restype = None
    print('\n(d) n  S  miss(RotF_K)  miss(RotF_K | g has >=2 prime factors)  P(#argmax>=2 & #argmin>=2)  [Lemma A: RotF_K miss => both]')
    for n in [24, 30, 36, 48, 60, 90, 120, 210, 420]:
        S = 200000 if n <= 120 else 50000
        X = (rng.random((S, n)) < .5).astype(np.uint8)
        out = np.zeros(S, np.int32)
        lib.eval_batch(X.ctypes.data_as(ctypes.c_void_p), S, n, out.ctypes.data_as(ctypes.c_void_p))
        A = X.sum(1); g = np.gcd(A, n - A)
        two = np.array([sum(1 for p in (2, 3, 5, 7, 11, 13) if gg % p == 0) >= 2 for gg in g])
        mC = (out & 4) == 0; both = ((out >> 10) & 3) == 3
        assert not np.any(mC & ~both)
        # conditional sample with A multiple of 6
        A6 = 6 * round(n / 12)
        Y = np.zeros((S // 4, n), np.uint8); Y[:, :A6] = 1; Y = rng.permuted(Y, axis=1)
        o2 = np.zeros(S // 4, np.int32)
        lib.eval_batch(Y.ctypes.data_as(ctypes.c_void_p), S // 4, n, o2.ctypes.data_as(ctypes.c_void_p))
        print(f'   {n:4d} {S:6d}  {mC.mean():.2e}  {((o2 & 4) == 0).mean():.2e} (S={S//4}, #a={A6})  {both.mean():.3e}', flush=True)

    # (e) Lemma A bound: Rot(G^-) contains every word whose drift-corrected walk T has a UNIQUE argmax.
    print('\n(e) n  S  P(#argmax T >= 2)  [upper bound for the miss rate of Rot(G^-), G^- = {d_k<0 for all 1<=k<=n/2}]  sqrt(n)*P')
    for n in [30, 60, 120, 240, 480, 960, 1920, 3840, 7680]:
        S = 20000
        X = (rng.random((S, n)) < .5).astype(np.int64)
        A = X.sum(1, keepdims=True)
        Sp = np.concatenate([np.zeros((S, 1), np.int64), np.cumsum(X, 1)[:, :-1]], 1)
        T = n * Sp - np.arange(n)[None, :] * A
        c = (T == T.max(1, keepdims=True)).sum(1)
        P = (c >= 2).mean()
        print(f'   {n:5d} {S}  {P:.4f}  {P*math.sqrt(n):.3f}', flush=True)
