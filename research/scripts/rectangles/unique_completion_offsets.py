"""Exhaustive check of Corollary 2.4 (all offsets), 2 <= n <= NMAX.

For every span (i, l) with l <= ceil(n/3) or l >= floor(2n/3) (0 <= i, i + l <= n, 1 <= l < n):
the LONG side (inner y if l >= floor(2n/3), else the outer context (x, z)) has at most one
completion on the short side making x y z non-primitive.  This is what makes Q_n a union of
<= 2*min(l, n-l) rectangles at that span.
"""
import sys
import numpy as np
from common import primitive_mask

def check(n):
    P = primitive_mask(n)
    w = np.arange(1 << n, dtype=np.int64)
    nonprim = w[~P]
    worst = 0
    for l in range(1, n):
        if not (l <= -(-n // 3) or l >= (2 * n) // 3):
            continue
        for i in range(0, n - l + 1):
            inner_mask = ((1 << l) - 1) << i
            inner = nonprim & inner_mask
            outer = nonprim & ~inner_mask
            long_side = inner if l >= n - l else outer
            # number of non-primitive words sharing the same long side must be 1
            _, counts = np.unique(long_side, return_counts=True)
            worst = max(worst, int(counts.max()))
    return worst

if __name__ == "__main__":
    NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 18
    for n in range(2, NMAX + 1):
        wst = check(n)
        assert wst == 1, (n, wst)
        print(f"n={n}: max #completions of the long side over all admissible spans = {wst}")
    print("Corollary 2.4 verified for all offsets.")
