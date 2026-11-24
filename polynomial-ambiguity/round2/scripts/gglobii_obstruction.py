"""gglobii_obstruction: the two exact obstructions of R2/gglob_ii.md §4 (per-facet tiling on d_M-space).

(O1) Separated support.  M = {a=(1,2), e=(0,3), b=(4,5)} on points 0..5 (e separates a from b), facet mu = z_a - z_b.
     Enumerate ALL rings with ||.||_1 <= 2 in original coordinates (one-point e_p, 2e_p, two-point e_p+e_q) that are
     non-crossing with every M-chord, map them by d_M (d_c = x_{c+} - x_{c-}), keep the mu-balanced ones, and
     report the rank of their span (needs to be dim mu^perp = 2 for a finite G1-type tiling; it is 1).
     Then the family z_k = (k+1, k, 0) (mu = 1) meets every piece c + N V within {mu >= 1} in <= 1 point.
(O2) Unequal weights.  mu = (1, 2) on two chords sharing a face: no nonzero mu-balanced d_M-image of a ring with
     ||.||_1 <= 2 exists at all.
(O3) Frequency: for random NC matchings of 2*mt points and random |S| = m subsets (the support of a +-1 facet),
     fraction with disconnected face graph G_M(S); and for the adjacent matchings M0, M1 (all chords on one face)
     it is always connected.
Usage: .venv/bin/python gglobii_obstruction.py
"""
import itertools, random
import numpy as np
from gglobii_signed_forest import random_nc_matching, interleave


def balanced_rank(npts, chords, plus, mu):
    m = len(chords)
    idx = {}
    for c, (p, q) in enumerate(chords):
        idx[p] = (c, 1 if p == plus[c] else -1); idx[q] = (c, 1 if q == plus[c] else -1)
    rings = [[(p, 1)] for p in range(npts)] + [[(p, 2)] for p in range(npts)] + \
            [[(p, 1), (q, 1)] for p, q in itertools.combinations(range(npts), 2)
             if not any(interleave((p, q), ch) for ch in chords)]
    imgs = []
    for r in rings:
        z = np.zeros(m)
        for p, k in r:
            c, s = idx[p]; z[c] += s * k
        if np.any(z) and abs(np.dot(mu, z)) < 1e-12: imgs.append(z)
    return len(rings), imgs, (np.linalg.matrix_rank(np.array(imgs)) if imgs else 0)


def face_connected(chords, S):
    mt = len(chords)
    def side(c, a):
        lo, hi = sorted(chords[c]); return lo < chords[a][0] < hi
    def same(a, b): return all(side(c, a) == side(c, b) for c in range(mt) if c not in (a, b))
    seen, st = {S[0]}, [S[0]]
    while st:
        a = st.pop()
        for b in S:
            if b not in seen and same(a, b): seen.add(b); st.append(b)
    return len(seen) == len(S)


if __name__ == '__main__':
    chords = [(1, 2), (0, 3), (4, 5)]           # a, e, b
    plus = [1, 0, 4]
    nr, imgs, rk = balanced_rank(6, chords, plus, np.array([1, 0, -1]))
    print("(O1) laminar rings:", nr, " balanced images:", sorted({tuple(int(t) for t in v) for v in imgs}), ' rank:', rk,
          '(need 2)')
    chords2 = [(0, 1), (2, 3)]
    nr, imgs, rk = balanced_rank(4, chords2, [0, 2], np.array([1, 2]))
    print('(O2) mu=(1,2): laminar rings:', nr, ' balanced images:', len(imgs), ' rank:', rk, '(need 1)')
    rng = random.Random(1)
    for mt, m in [(8, 2), (8, 4), (8, 6), (18, 2), (18, 6), (18, 12)]:
        bad = 0; T = 400
        for _ in range(T):
            ch = random_nc_matching(mt, rng)
            S = rng.sample(range(mt), m)
            bad += not face_connected(ch, S)
        M0 = [(2 * i, 2 * i + 1) for i in range(mt)]
        M1 = [(2 * i + 1, (2 * i + 2) % (2 * mt)) for i in range(mt)]
        M1 = [tuple(sorted(c)) for c in M1]
        ok01 = all(face_connected(M, rng.sample(range(mt), m)) for M in (M0, M1) for _ in range(50))
        print(f'(O3) |M|={mt} |S|={m}: random NC M, disconnected G_M(S): {bad}/{T};  M0,M1 always connected: {ok01}')
