"""For instances without UF/PAR certificate: bounded attack search over all x=eps windows.
Report whether every window admits a sigma (|sigma|<=maxsig) with sigma r a proper power."""
import sys
from common import *
from survey import run

def mirror(U):
    R = U[::-1]; return R in U + U

for (U, k, rho) in [(tm(8), 2, 6), (tm(8), 3, 6), (tm(8), 4, 6), (tm(6), 3, 6), (tm(7), 3, 6),
                    (tm(10), 3, 8), (tm(12), 3, 8)]:
    st, hard = run(U, k, rho)
    print('U', U, 'mirror-symmetric:', mirror(U), 'k', k)
    for (typ, d, W, a0) in hard:
        marks = set(range(a0, a0 + rho))
        inside = a0 <= d < a0 + rho or (typ.startswith('ins') and a0 <= d <= a0 + rho)
        allfail = True; esc = None
        for cuts in windows(W, marks, 3, rho + 4):
            loops = [W[cuts[j]:cuts[j+1]] for j in range(3)]
            r = W[cuts[-1]:] + W[:cuts[0]]
            s = bounded_attack(r, loops, min(2 * len(W), 40))
            if s is None:
                allfail = False; esc = (cuts, loops); break
        print('  ', typ, d, W, 'R=', a0, 'defect in R' if inside else 'defect outside R',
              '| no-attack window (bounded):' if not allfail else '| EVERY window attacked (bounded)', esc if esc else '')
