"""Exhaustive check of THEOREM A (linear rectangle cover) for 2 <= n <= NMAX.

Theorem A: let L = floor(2n/3), s = n - L = ceil(n/3).  For every y in {a,b}^L there is
AT MOST ONE z in {a,b}^s such that yz is not primitive.  Writing pi(y) for that z (or None),
    Q_n = union over j < s, c in {a,b} of  R_{j,c} = {y : pi(y) is None or pi(y)_j != c} x {z : z_j = c},
2s = 2 ceil(n/3) rectangles, each inside Q.

The script checks, for each n:
  (1) max_y #{z : yz non-primitive} at the split L = floor(2n/3)   (Theorem A says <= 1);
  (2) the same maximum at the other splits l = 1..n-1, to show where uniqueness fails
      (it must fail when the long side is too short, e.g. the middle split for n = 6);
  (3) that the 2s rectangles R_{j,c} are inside Q_n and cover Q_n exactly.
Usage: python3 unique_completion.py [NMAX]
"""
import sys
import numpy as np
from common import primitive_mask


def forb_counts(P, n, l):
    R, C = 1 << l, 1 << (n - l)
    M = P[(np.arange(R)[:, None] | (np.arange(C)[None, :] << l))]
    return (~M).sum(axis=1), M


def check(n):
    P = primitive_mask(n)
    L = (2 * n) // 3
    s = n - L
    cnt, M = forb_counts(P, n, L)
    assert cnt.max() <= 1, (n, cnt.max())
    # pi(y)
    pi = np.full(1 << L, -1, dtype=np.int64)
    ys, zs = np.nonzero(~M)
    pi[ys] = zs
    covered = np.zeros_like(M)
    zarr = np.arange(1 << s)
    for j in range(s):
        for c in (0, 1):
            A = (pi < 0) | (((pi >> j) & 1) != c)
            B = ((zarr >> j) & 1) == c
            rect = A[:, None] & B[None, :]
            assert not (rect & ~M).any()
            covered |= rect
    assert (covered == M).all()
    per_split = [int(forb_counts(P, n, l)[0].max()) for l in range(1, n)]
    # max number of forbidden completions of a ROW (prefix of length l)
    return L, s, per_split


if __name__ == "__main__":
    NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 22
    print("n  L=floor(2n/3)  #rects=2ceil(n/3)   max #forbidden completions of a prefix of length l, l=1..n-1")
    for n in range(2, NMAX + 1):
        L, s, ps = check(n)
        print(f"{n:2d}  {L:2d}  {2*s:3d}   {ps}")
    print("Theorem A verified (uniqueness at L = floor(2n/3), exact cover by 2 ceil(n/3) rectangles).")
