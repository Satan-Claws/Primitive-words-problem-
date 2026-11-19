"""Exact (all sigma in M, unbounded) escape check for all instances in the survey families:
for each (W, R) find an x=eps window with full_escape True."""
import time
from common import *
from survey import defects

def mirror(U): return U[::-1] in U + U
t0 = time.time()
for (U, k, rho) in [(tm(8), 2, 6), (tm(8), 3, 6), (tm(6), 3, 6), (tm(7), 3, 6), ('aababb', 3, 6),
                    ('abaabb', 4, 6), (tm(10), 3, 8), (tm(12), 3, 8), ('aabababb', 3, 6), (tm(16), 2, 8)]:
    tot = esc = 0; bad = []
    for (typ, d, W) in defects(U, k):
        if not primitive(W): continue
        for a0 in range(0, len(W) - rho + 1):
            marks = set(range(a0, a0 + rho)); tot += 1
            ok = False
            for cuts in windows(W, marks, 3, rho + 4):
                loops = [W[cuts[j]:cuts[j+1]] for j in range(3)]
                r = W[cuts[-1]:] + W[:cuts[0]]
                if full_escape(r, loops) is True:
                    ok = True; break
            if ok: esc += 1
            else: bad.append((typ, d, W, a0))
    print(U, 'mirror' if mirror(U) else 'non-mirror', 'k', k, 'rho', rho, 'instances', tot,
          'certified escapes', esc, 'uncertified', bad[:3], f'{time.time()-t0:.0f}s', flush=True)
