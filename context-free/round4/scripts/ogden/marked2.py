#!/usr/bin/env python3
"""NEST2 / FREE2 with Ogden marks = an interval D of length d (EVIDENCE, finite exponent box).
For each primitive w of length n and each interval D, the minimal number W of marked
positions in the window v1..x1 for which a good nested 2-pump exists (v_j x_j must meet D)."""
import sys
from multipump import prim, minW
nmin, nmax, d, mode = map(lambda t: t, sys.argv[1:5])
nmin, nmax, d = int(nmin), int(nmax), int(d)
for n in range(nmin, nmax + 1):
    hist = {}; worst = (0, None)
    for k in range(2 ** (n - 1)):
        w = 'a' + format(k, '0%db' % (n - 1)).replace('0', 'a').replace('1', 'b')
        if not prim(w): continue
        for s in range(n - d + 1):
            D = set(range(s, s + d))
            W, dec = minW(w, mode, 4, 4, marks=D, Wmax=d)
            hist[W] = hist.get(W, 0) + 1
            key = W if W is not None else 99
            if key > worst[0]: worst = (key, (w, s, dec))
    print(n, d, mode, hist, worst, flush=True)
