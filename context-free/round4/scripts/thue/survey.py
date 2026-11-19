"""Survey: for near-powers W = (U^k with one defect), marks = interval R of length rho,
m = 3 free loops (x_j = eps), find a window with a UF or PAR certificate (=> all generated words primitive).
"""
import sys, time
from common import *

def defects(U, k):
    base = U * k; n = len(base)
    out = []
    for d in range(n):
        out.append(('flip', d, base[:d] + ('b' if base[d] == 'a' else 'a') + base[d+1:]))
        for c in 'ab':
            out.append(('ins' + c, d, base[:d] + c + base[d:]))
        out.append(('del', d, base[:d] + base[d+1:]))
    return out

def run(U, k, rho, m=3, maxwin=None, quick=True):
    stats = {'UF': 0, 'PAR': 0, 'none': 0}
    hard = []
    for (typ, d, W) in defects(U, k):
        if not primitive(W): continue
        n = len(W)
        for a0 in range(0, n - rho + 1, 1 if not quick else max(1, rho // 2)):
            marks = set(range(a0, a0 + rho))
            found = None
            for cuts in windows(W, marks, m, maxwin or rho + 4):
                loops = [W[cuts[j]:cuts[j+1]] for j in range(m)]
                r = W[cuts[-1]:] + W[:cuts[0]]
                if par_cert(r, loops):
                    found = ('PAR', cuts); break
            if not found:
                for cuts in windows(W, marks, m, maxwin or rho + 4):
                    loops = [W[cuts[j]:cuts[j+1]] for j in range(m)]
                    r = W[cuts[-1]:] + W[:cuts[0]]
                    dl = uf_cert(r, loops, maxlam=min(len(r)//2, 2*len(U)+4))
                    if dl:
                        found = ('UF', cuts, dl); break
            if found: stats[found[0]] += 1
            else:
                stats['none'] += 1; hard.append((typ, d, W, a0))
    return stats, hard

if __name__ == '__main__':
    t = time.time()
    for (U, k, rho) in [(tm(8), 2, 6), (tm(8), 3, 6), (tm(8), 4, 6), (tm(6), 3, 6), (tm(7), 3, 6),
                        (tm(10), 3, 8), (tm(12), 3, 8), (tm(16), 2, 8), (tm(16), 3, 8)]:
        st, hard = run(U, k, rho)
        print(U, k, rho, st, 'hard:', hard[:5], f'{time.time()-t:.0f}s', flush=True)
