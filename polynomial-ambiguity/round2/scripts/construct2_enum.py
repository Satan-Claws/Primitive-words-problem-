"""construct2_enum.py -- exhaustive list of primitive x in W_30 ∩ N^30 with |x|_1 <= NMAX, up to the
dihedral group D_30 (rotations/reflections preserve chord crossing, V_p, primitivity, hence every
coverage question below).  W_30 = V_2+V_3+V_5 = {x : Phi_30(z) | sum x_j z^j}.  Meet-in-the-middle on
the two halves 0..14 / 15..29.  usage: python construct2_enum.py NMAX  -> writes W30_N{NMAX}.npy"""
import sys, itertools, numpy as np, sympy as sp
n = 30; NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 8
z = sp.symbols('z'); Phi = sp.Poly(sp.cyclotomic_poly(n, z), z)
M = np.zeros((8, n), dtype=np.int64)
for j in range(n):
    r = sp.Poly(z**j, z).rem(Phi).all_coeffs()[::-1]
    M[:len(r), j] = [int(c) for c in r]
def half_vectors(L, N):
    out = []
    def rec(i, left, cur):
        if i == L: out.append(tuple(cur)); return
        for v in range(left+1):
            cur.append(v); rec(i+1, left-v, cur); cur.pop()
    rec(0, N, []); return np.array(out, dtype=np.int64)
H = half_vectors(15, NMAX)
KL = H @ M[:, :15].T; KR = H @ M[:, 15:].T; nl = H.sum(1)
from collections import defaultdict
idx = defaultdict(list)
for i, k in enumerate(map(tuple, KR)): idx[k].append(i)
def prim(x): return all(not np.array_equal(x, np.roll(x, n//p)) for p in (2, 3, 5))
def canon(x):
    best = None
    for y in (x, x[::-1]):
        for r in range(n):
            t = tuple(np.roll(y, r))
            if best is None or t < best: best = t
    return best
seen = set(); tot = 0
for i in range(len(H)):
    k = tuple(-KL[i])
    for j in idx.get(k, ()):
        if nl[i] + nl[j] == 0 or nl[i] + nl[j] > NMAX: continue
        x = np.concatenate([H[i], H[j]])
        if not prim(x): continue
        tot += 1; seen.add(canon(x))
print(f'NMAX={NMAX}: primitive W30 points {tot}, dihedral classes {len(seen)}')
np.save(f'/private/tmp/claude-501/-Users-shoru-Desktop-Test4/0ed9f581-4f02-4fb6-a7db-5e10049bb620/scratchpad/W30_N{NMAX}.npy', np.array(sorted(seen)))
