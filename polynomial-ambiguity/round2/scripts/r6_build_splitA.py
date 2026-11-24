"""R6-A: the split certificate L_A ⊆ G^- (Lemma SA) — soundness check and rotation density.

L_A = { w : H = h(n) >= 1 and exists s >= n/2 with h(s) = 0, h <= 0 on [0,s], h < H on (s,n) },
h(k) = #a(w[0,k)) - #b(w[0,k)).  Equivalently w = x y, x a b-first Dyck word (walk <= 0, ends at 0),
every nonempty suffix of y has more a's than b's, and |x| >= |y|.
"""
import itertools, random, sys
import numpy as np

def walk(w): 
    h = [0]
    for c in w: h.append(h[-1] + (1 if c == 'a' else -1))
    return h

def in_LA(w):
    n = len(w); h = walk(w); H = h[n]
    if H < 1: return False
    s = None
    for k in range(n + 1):
        if h[k] >= 1: break
        if h[k] == 0: s = k
    if s is None or 2 * s < n: return False
    return all(h[k] < H for k in range(s + 1, n))

def in_Gminus(w):
    n = len(w)
    pa = sa = 0
    for k in range(1, n // 2 + 1):
        pa += w[k - 1] == 'a'; sa += w[n - k] == 'a'
        if pa - sa >= 0: return False
    return True

def primitive(w):
    n = len(w); return all(w != w[:d] * (n // d) for d in range(1, n) if n % d == 0)

def exhaustive(N):
    for n in range(1, N + 1):
        cnt = bad = notG = 0
        for t in itertools.product('ab', repeat=n):
            w = ''.join(t)
            if in_LA(w):
                cnt += 1
                if not primitive(w): bad += 1
                if not in_Gminus(w): notG += 1
        print(f'n={n:2d} |L_A|={cnt:7d} nonprimitive={bad} not-in-G-={notG}')

def rot_hit_np(bits):
    """bits: 0/1 array (1=a). True if some rotation of w or of swap(w) is in L_A."""
    n = len(bits)
    for b in (bits, 1 - bits):
        st = 2 * b.astype(np.int64) - 1
        H = st.sum()
        if H < 1: continue
        dbl = np.concatenate([st, st]); c = np.concatenate([[0], np.cumsum(dbl)])
        for r in range(n):
            h = c[r:r + n + 1] - c[r]
            pos = np.nonzero(h >= 1)[0]; tau = pos[0]
            z = np.nonzero(h[:tau] == 0)[0]; s = z[-1]
            if 2 * s < n: continue
            if s + 1 < n and h[s + 1:n].max() >= H: continue
            return True
    return False

if __name__ == '__main__':
    exhaustive(int(sys.argv[1]) if len(sys.argv) > 1 else 18)
    rng = np.random.default_rng(7)
    for n in (64, 256, 1024):
        S = 400 if n <= 256 else 150
        hits = sum(rot_hit_np(rng.integers(0, 2, n)) for _ in range(S))
        print(f'MC n={n}: P(some rotation of w or swap(w) in L_A) ≈ {hits/S:.3f} (S={S})')
