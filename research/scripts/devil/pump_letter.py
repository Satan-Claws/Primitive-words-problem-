"""
Single-letter pumping in Q.  For primitive w and position j, pumping w_j means
u c^i z in Q for all i>=0 (w = u c z).  By conjugacy u c^i z ~ c^i (z u) and, if c^i s = t^p (p>=2)
with s = zu not in c^*, then i < |s| (proof in report), so checking 0 <= i <= |s| is exhaustive.
Reports, per n: max over primitive w of the number of NON-pumpable positions, and
whether every primitive w has at least one pumpable position.
Usage: python3 pump_letter.py NMAX
"""
import sys, itertools
from rect_barrier import is_prim

def pumpable(w, j):
    c = w[j]; s = w[j+1:] + w[:j]
    if all(ch == c for ch in s):
        return False
    return all(is_prim(c * i + s) for i in range(0, len(s) + 1))

NMAX = int(sys.argv[1])
for n in range(2, NMAX + 1):
    worst = -1; worstw = None; nogood = 0
    for t in itertools.product('ab', repeat=n):
        w = ''.join(t)
        if not is_prim(w): continue
        nb = sum(1 for j in range(n) if not pumpable(w, j))
        if nb == n: nogood += 1
        if nb > worst: worst, worstw = nb, w
    print(f"n={n}: max #non-pumpable letters = {worst} (e.g. {worstw}); words with no pumpable letter = {nogood}")
