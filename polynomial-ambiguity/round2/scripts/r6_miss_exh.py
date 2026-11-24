"""R6 fold-miss set: exhaustive sweep (uses r6_miss_lib.c via ctypes, threaded).

Usage: python r6_miss_exh.py [NMAX=24]
 1. soundness: every tier gives mask 0 on every NON-primitive word, n <= 20
 2. per n: |Q_n|, density of each tier inside Q_n, |miss| of the rotation tiers, classes
 3. E_n = Q_n minus (all fold tiers) minus (r4 gadget library) using r4_core_U.txt (complete U_n for n <= 28)
 4. structure of the Rot(F_max)-miss classes: gcd(#a,#b), omega(n), responsible primes, Hamming distance to nearest u^p, xhat(1)
Tier bits: see r6_miss_lib.c header.
"""
import ctypes, os, sys, subprocess, math, cmath
from multiprocessing.pool import ThreadPool
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
SO = os.path.join(os.environ.get('TMPDIR', '/tmp'), 'r6miss.so')
subprocess.check_call(['cc', '-O3', '-shared', '-fPIC', '-o', SO, os.path.join(HERE, 'r6_miss_lib.c')])
lib = ctypes.CDLL(SO)
lib.sweep_range.restype = ctypes.c_long
lib.eval_tiers.restype = ctypes.c_int
NAMES = ['F_K', 'F_max', 'Rot F_K', 'Rot F_K feat', 'Rot F_max', 'Rot F_max feat', 'F_.1', 'Rot F_.1', 'F_W', 'Rot F_W']

def mask_of(s):
    x = (ctypes.c_ubyte * len(s))(*[1 if c == 'a' else 0 for c in s])
    return lib.eval_tiers(x, len(s))

def is_prim(s):
    return (s + s).find(s, 1) == len(s)

def word(w, n):  # bit 1 = 'a' (r6 convention)
    return ''.join('a' if (w >> i) & 1 else 'b' for i in range(n))

def canon(s, swap=True):
    n = len(s); out = []
    vs = [s, s[::-1]]
    if swap:
        t = s.translate(str.maketrans('ab', 'ba')); vs += [t, t[::-1]]
    return min(v[i:] + v[:i] for v in vs for i in range(n))

def primes_of(n):
    return [p for p in range(2, n + 1) if n % p == 0 and all(p % q for q in range(2, int(p**.5) + 1))]

def ham_to_power(s):
    n = len(s); best = n
    for p in primes_of(n):
        m = n // p
        d = sum(min(c, p - c) for c in (sum(s[i + j * m] == 'a' for j in range(p)) for i in range(m)))
        best = min(best, d)
    return best

def responsible(s):
    """primes p such that SOME rotation has a palindromic p-block a-count vector"""
    n = len(s); res = []
    for p in primes_of(n):
        m = n // p
        for r in range(n):
            t = s[r:] + s[:r]
            c = [t[i * m:(i + 1) * m].count('a') for i in range(p)]
            if c == c[::-1]:
                res.append(p); break
    return res

def argext(s):
    """multiplicities of argmax / argmin of the drift-corrected cyclic walk nT(i) = n*S(i) - i*A, i in Z_n"""
    n = len(s); A = s.count('a'); S = 0; T = []
    for i in range(n):
        T.append(n * S - i * A); S += s[i] == 'a'
    return T.count(max(T)), T.count(min(T))

def xhat1(s):
    n = len(s)
    return abs(sum(cmath.exp(2j * math.pi * k / n) for k, c in enumerate(s) if c == 'a'))

def soundness(nmax=20):
    bad = 0
    for n in range(2, nmax + 1):
        seen = set()
        for d in range(1, n):
            if n % d: continue
            for u in range(1 << d):
                s = word(u, d) * (n // d)
                if s in seen: continue
                seen.add(s)
                if mask_of(s): bad += 1; print('UNSOUND', s, mask_of(s))
    print(f'soundness: non-primitive words n<=20 with nonzero tier mask: {bad}')

def sweep(n, dumpbit, cap=1 << 23, T=14):
    tot = 1 << n
    chunks = [(tot * i // T, tot * (i + 1) // T) for i in range(T)]
    def job(c):
        counts = (ctypes.c_long * 1025)()
        buf = (ctypes.c_uint32 * cap)()
        nd = lib.sweep_range(n, ctypes.c_uint32(c[0]), ctypes.c_uint32(c[1]), counts, dumpbit, buf, cap)
        return list(counts), [buf[i] for i in range(min(nd, cap))], nd
    with ThreadPool(T) as pool:
        res = pool.map(job, chunks)
    counts = [sum(r[0][i] for r in res) for i in range(1025)]
    dump = [w for r in res for w in r[1]]
    assert sum(r[2] for r in res) == len(dump)
    return counts, dump

if __name__ == '__main__':
    NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 24
    soundness(20)
    U = {}
    for line in open(os.path.join(HERE, 'r4_core_U.txt')):
        n, s = line.split(); U.setdefault(int(n), []).append(s)
    print('\nTier densities inside Q_n (exhaustive):')
    print('n |Q_n| ' + ' | '.join(NAMES) + ' || miss RotF_K (words/classes) | miss RotF_max (w/cl) | miss RotF_max feat (w/cl) | miss all (w/cl)')
    ALL = (1 << 10) - 1
    store = {}
    for n in range(2, NMAX + 1):
        counts, dump = sweep(n, 4)
        Q = counts[1024]
        dens = [sum(c for m, c in enumerate(counts[:1024]) if m >> b & 1) / Q for b in range(10)]
        words = [word(w, n) for w in dump]
        masks = [mask_of(s) for s in words]
        def cls(pred, swap=True):
            ws = [s for s, m in zip(words, masks) if pred(m)]
            return len(ws), sorted({canon(s, swap) for s in ws})
        mC = cls(lambda m: not m & 4)
        mD = cls(lambda m: not m & 16)
        mE = cls(lambda m: not m & 32, swap=False)
        mAll = cls(lambda m: m == 0, swap=False)
        store[n] = (mD, mE, mAll, mC)
        print(n, Q, ' '.join(f'{d:.4f}' for d in dens), '||', f'{mC[0]}/{len(mC[1])}', f'{mD[0]}/{len(mD[1])}',
              f'{mE[0]}/{len(mE[1])}', f'{mAll[0]}/{len(mAll[1])}', flush=True)
    print('\nE_n = Q_n minus (all fold tiers) minus (r4 gadget library), n <= 28 via r4_core_U.txt (U_n listed up to rotation/reversal/swap):')
    for n in sorted(U):
        for s in U[n]:
            m = mask_of(s)
            print(f'  n={n} {s} tiers={m:010b}[bit9..0] ' + ('E-class (no fold tier)' if m == 0 else
                  'certified by: ' + ', '.join(NAMES[b] for b in range(10) if m >> b & 1)))
    print('\nStructure of Rot(F_K)-miss classes (a-feature; up to rot/rev/swap):')
    for n in store:
        mC = store[n][3]
        if not mC[1]: continue
        st = Counter()
        for s in mC[1]:
            A = s.count('a'); g = math.gcd(A, n - A)
            st[(g, tuple(responsible(s)), ham_to_power(s), round(xhat1(s), 6) == 0, argext(s))] += 1
        print(f' n={n} omega={len(primes_of(n))} classes={len(mC[1])}: (g, primes p with a p-palindromic rotation, Hamming-to-power, xhat1==0, (#argmax T, #argmin T)) -> #classes')
        for k, v in sorted(st.items()):
            print('    ', k, v)
        for s in mC[1][:8]:
            print('     e.g.', s, 'mask', format(mask_of(s), '010b'))
    print('\nStructure of Rot(F_max)-miss classes (a-feature; up to rot/rev/swap):')
    for n in store:
        mD = store[n][0]
        if not mD[1]: continue
        st = Counter()
        for s in mD[1]:
            A = s.count('a'); g = math.gcd(A, n - A)
            st[(g, tuple(responsible(s)), ham_to_power(s), round(xhat1(s), 6) == 0)] += 1
        print(f' n={n} omega={len(primes_of(n))} classes={len(mD[1])}: (g, responsible primes, Hamming-to-power, xhat1==0) -> #classes')
        for k, v in sorted(st.items()):
            print('    ', k, v)
        for s in mD[1][:6]:
            print('     e.g.', s, 'mask', format(mask_of(s), '010b'))
    print('\nAll-tier miss classes (no fold tier at all, a/aa/ab features; up to rot/rev):')
    for n in store:
        if store[n][2][1]:
            print(f' n={n}:', store[n][2][0], 'words', len(store[n][2][1]), 'classes; e.g.', store[n][2][1][:4],
                  [ (math.gcd(s.count("a"), n - s.count("a")), responsible(s), ham_to_power(s)) for s in store[n][2][1][:4]])
