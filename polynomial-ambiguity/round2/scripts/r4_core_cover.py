"""r4_core_cover.py -- R4-A coverage loop driver (uses r4_core_lib.c via ctypes).
Usage: python r4_core_cover.py NMAX [K KP R]
 - soundness check: all gadgets give 0 trees on every NON-primitive word, n <= 16  [computational check of the proofs]
 - fold cross-check against r3_offw_fold.certs for n <= 12
 - exhaustive coverage table n = 2..NMAX, stages: S0 = LIN+FOLD, S1 = +FL_K, S2 = +LF_K, S3 = +PF_KP
 - writes uncovered words U_n (stage 3) to r4_core_U.txt
"""
import ctypes, os, sys, subprocess, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
SO = os.path.join(os.environ.get('TMPDIR', '/tmp'), 'r4core.so')
subprocess.check_call(['cc', '-O3', '-shared', '-fPIC', '-o', SO, os.path.join(HERE, 'r4_core_lib.c')])
lib = ctypes.CDLL(SO)
lib.sweep.restype = ctypes.c_long
lib.canon.restype = ctypes.c_uint32
NMAX = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 18
K = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[1].isdigit() else 3
KP = int(sys.argv[3]) if len(sys.argv) > 3 and sys.argv[1].isdigit() else 2
R = int(sys.argv[4]) if len(sys.argv) > 4 and sys.argv[1].isdigit() else 3
STAGE = int(os.environ.get("STAGE", 4))
lib.init_table(R)

def gadgets(w, n, stage=STAGE):
    g = (ctypes.c_int * 8)()
    lib.eval1(ctypes.c_uint32(w), n, K, KP, stage, g)
    return list(g)

def word(w, n):
    return ''.join('b' if (w >> i) & 1 else 'a' for i in range(n))

def is_prim(w, n):
    s = word(w, n)
    return (s + s).find(s, 1) == n

if __name__ == '__main__' and True:
    # soundness on non-primitive words
    bad = 0
    for n in range(2, 17 if NMAX < 30 else 2):
        for w in range(1 << n):
            if not is_prim(w, n):
                if any(gadgets(w, n)):
                    bad += 1; print('UNSOUND', n, word(w, n), gadgets(w, n))
    print('soundness check n<=16: violations =', bad)
    sys.path.insert(0, HERE)
    from r3_offw_fold import certs
    mism = sum(1 for n in range(1, 13) for w in range(1 << n) if gadgets(w, n, 0)[1] != certs(word(w, n)))
    print('fold count vs r3_offw_fold.certs, n<=12: mismatches =', mism)
    cap = 1 << 22
    unc = (ctypes.c_uint32 * cap)()
    counts = (ctypes.c_long * 8)(); maxamb = (ctypes.c_int * 8)()
    out = open(os.path.join(HERE, 'r4_core_U.txt'), 'w')
    print(f'K={K} KP={KP} R={R}')
    print('n |Q_n| S0 S1 S2 S3 |U_n| classes maxamb(S0..S3 or lazy)')
    for n in range(int(os.environ.get("NMIN", 2)), NMAX + 1):
        t = time.time()
        full = 1 if n <= 16 else 0
        nu = lib.sweep(n, K, KP, STAGE, full, counts, maxamb, unc, cap)
        U = [unc[i] for i in range(min(nu, cap))]
        cl = sorted(set(lib.canon(ctypes.c_uint32(w)) for w in U)) if U else []
        lib.setn(n)
        cl = sorted(set(lib.canon(ctypes.c_uint32(w)) for w in U))
        Q = counts[0]
        print(n, Q, *[f'{counts[1+s]/Q:.4f}' for s in range(STAGE+1)], nu, len(cl),
              list(maxamb)[:STAGE+1] if full else 'lazy', f'{time.time()-t:.1f}s', flush=True)
        for c in cl:
            out.write(f'{n} {word(c, n)}\n')
    out.close()
