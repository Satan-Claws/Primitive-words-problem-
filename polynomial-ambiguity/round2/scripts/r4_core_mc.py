"""r4_core_mc.py -- Monte Carlo coverage of the R4-A library on uniform random words of length n (n up to ~512).
Pure numpy re-implementation of the gadgets of r4_core_lib.c (cross-checked against the C code for n <= 14)."""
import sys, math, random, ctypes, os
import numpy as np
K, KP, R = 3, 2, 3
def foldcount(x):
    x = np.asarray(x, dtype=np.int64); n = len(x)
    if n < 2: return 0
    m = np.arange(n)[:, None]; k = np.arange(n)[None, :]
    a = (2 * k - m) % (2 * n)
    sg = np.where((a > 0) & (a < n), 1, np.where(a > n, -1, 0))
    d = sg * (x[k] - x[(m - k) % n])
    pos = (d > 0).any(1); neg = (d < 0).any(1)
    return int((pos != neg).sum())
def cyc_ind(w, L):
    n = len(w); ww = np.concatenate([w] * (L // n + 2))
    code = np.zeros(n, dtype=np.int64)
    for t in range(L): code |= ww[t:t + n].astype(np.int64) << t
    return code
def lines_count(o1, o2):
    c = 0
    for c1 in range(1, R + 1):
        for c2 in range(1, R + 1):
            if math.gcd(c1, c2) == 1 and abs(c1 * o1 - c2 * o2) == 1: c += 1
    return c
def gadgets(w, lazy=True):
    """w: np int array of 0/1 (1=b). returns list of tree counts [LIN, FOLD, FL, LF, PF, RLF]"""
    n = len(w); g = [0] * 6
    nb = int(w.sum()); na = n - nb
    g[0] = lines_count(na, nb) + (na == 1) + (nb == 1)
    if lazy and g[0]: return g
    g[1] = foldcount(w)
    if lazy and g[1]: return g
    counts = [na, nb]; inds = {}
    for L in range(2, K + 1):
        code = cyc_ind(w, L); inds[L] = code
        counts += list(np.bincount(code, minlength=1 << L))
    c = sum(1 for v in counts[2:] if v == 1)
    for i in range(len(counts)):
        for j in range(max(i + 1, 2), len(counts)):
            c += lines_count(counts[i], counts[j])
    g[2] = c
    if lazy and c: return g
    for L in range(2, K + 1):
        for f in np.unique(inds[L]):
            g[3] += foldcount((inds[L] == f).astype(np.int64))
            if lazy and g[3]: return g
    for L in range(2, KP + 1):
        code = inds[L]
        for f in range(1 << L):
            for h in range(f + 1, 1 << L):
                g[4] += foldcount((code == f).astype(np.int64) - (code == h))
                if lazy and g[4]: return g
    if 0 < nb < n:
        s = next(i for i in range(n) if w[i] == 0 and w[i - 1] == 1)
        r = np.roll(w, -s); al, be = [], []
        i = 0
        while i < n:
            la = 0
            while i < n and r[i] == 0: la += 1; i += 1
            lb = 0
            while i < n and r[i] == 1: lb += 1; i += 1
            al.append(la); be.append(lb)
        if len(al) >= 2: g[5] = foldcount(al) + foldcount(be)
    return g
def stage_of(g):
    for s, idx in enumerate([[0, 1], [2], [3], [4], [5]]):
        if any(g[i] for i in idx): return s
    return None
if __name__ == '__main__':
    if sys.argv[1:2] == ['check']:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import r4_core_cover as C
        bad = 0
        for n in range(2, 13):
            for x in range(1 << n):
                w = np.array([(x >> i) & 1 for i in range(n)])
                a = gadgets(w, lazy=False); b = C.gadgets(x, n, 4)[:6]
                if a != b: bad += 1
        print('numpy vs C gadget counts, all words n<=12: mismatches =', bad); sys.exit()
    random.seed(1); rng = np.random.default_rng(1)
    T = int(sys.argv[2]) if len(sys.argv) > 2 else 400
    for n in [int(v) for v in sys.argv[1].split(',')]:
        st = [0] * 6; tot = 0
        while tot < T:
            w = rng.integers(0, 2, n)
            s = ''.join('ab'[v] for v in w)
            if (s + s).find(s, 1) != n: continue
            tot += 1; k = stage_of(gadgets(w))
            st[5 if k is None else k] += 1
        cum = np.cumsum(st[:5]) / tot
        print(n, tot, 'cumulative S0..S4:', ' '.join(f'{v:.3f}' for v in cum), 'uncovered', st[5] / tot, flush=True)

def fl_only(n, T, rng):
    """fraction of random words covered by LIN or FL (counting gadgets only); fold gadgets are ~0 at these n"""
    hit = 0
    for _ in range(T):
        w = rng.integers(0, 2, n)
        g = gadgets.__wrapped__(w) if hasattr(gadgets, '__wrapped__') else None
        nb = int(w.sum()); counts = [n - nb, nb]
        for L in range(2, K + 1): counts += list(np.bincount(cyc_ind(w, L), minlength=1 << L))
        ok = lines_count(counts[0], counts[1]) > 0 or any(v == 1 for v in counts[2:]) or any(
            lines_count(counts[i], counts[j]) for i in range(len(counts)) for j in range(max(i + 1, 2), len(counts)))
        hit += ok
    return hit / T
