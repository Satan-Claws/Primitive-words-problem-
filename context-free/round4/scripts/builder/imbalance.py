# Half-imbalance certificate: n even, w = xy, |x|=|y|, ||y|_b-|x|_b| > n/6  ==> primitive?
# Compute the max imbalance over non-primitive words of each even length.
from common import *
for n in range(2, 25, 2):
    best = 0
    for d in range(1, n):
        if n % d: continue
        for u in range(1 << d):
            uu = [(u >> k) & 1 for k in range(d)]
            w = (uu * (n // d))
            best = max(best, abs(sum(w[n // 2:]) - sum(w[:n // 2])))
    print(n, 'max imbalance of non-primitive:', best, ' n/6 =', round(n / 6, 2))
