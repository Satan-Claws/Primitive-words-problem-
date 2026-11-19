#!/usr/bin/env python3
"""FREE_m test (EVIDENCE): m consecutive loops at one nonterminal (Theorem A' shape).
w = u v1..vm z xm..x1 y ; each vj xj meets the mark set D ; window v1..x1 has <= W marks.
Defender (Q) wins if all u s z t y are primitive, s = v_{c1}..v_{cr}, t = x_{cr}..x_{c1},
for all sequences c in [m]^r, r <= R.  Reports minimal W (or None if no good decomposition
with window marks <= Wmax).
usage: freeloops.py mode args  (mode 'all' n d m R  |  'word' w D(comma list) m R)"""
import sys, itertools
def prim(s):
    return len(s) > 0 and (s + s).find(s, 1) == len(s)

def compositions(total, parts):
    if parts == 1:
        yield (total,); return
    for f in range(total + 1):
        for r in compositions(total - f, parts - 1):
            yield (f,) + r

def good(w, cuts, m, R):
    # cuts: positions a0<=..; parts: v1..vm, z, xm..x1
    u = w[:cuts[0]]; y = w[cuts[-1]:]
    P = [w[cuts[i]:cuts[i + 1]] for i in range(2 * m + 1)]
    V = P[:m]; z = P[m]; X = list(reversed(P[m + 1:]))  # X[j] = x_{j+1}
    seqs = [()]
    for r in range(1, R + 1):
        seqs += list(itertools.product(range(m), repeat=r))
    for c in seqs:
        s = ''.join(V[j] for j in c); t = ''.join(X[j] for j in reversed(c))
        if not prim(u + s + z + t + y):
            return False
    return True

def minW(w, D, m, R, Wmax, Lmax=None):
    n = len(w); Lmax = Lmax or n
    for W in range(1, Wmax + 1):
        for st in range(n):
            for en in range(st + 1, min(n, st + Lmax) + 1):
                if sum(1 for p in range(st, en) if p in D) != W: continue
                win = en - st
                for comp in compositions(win, 2 * m + 1):
                    V = comp[:m]; X = comp[m + 1:][::-1]
                    if any(V[j] + X[j] == 0 for j in range(m)): continue
                    cuts = [st]
                    for f in comp: cuts.append(cuts[-1] + f)
                    ok = True
                    for j in range(m):
                        a, b = cuts[j], cuts[j + 1]
                        e, f = cuts[2 * m - j], cuts[2 * m - j + 1]
                        if not (any(p in D for p in range(a, b)) or any(p in D for p in range(e, f))):
                            ok = False; break
                    if not ok: continue
                    if good(w, cuts, m, R):
                        return W, [w[cuts[0]:cuts[0]]] + [w[cuts[i]:cuts[i+1]] for i in range(2*m+1)]
    return None, None

if __name__ == '__main__':
    if sys.argv[1] == 'all':
        n, d, m, R = map(int, sys.argv[2:6])
        hist = {}; worst = (0, None)
        for k in range(2 ** (n - 1)):
            w = 'a' + format(k, '0%db' % (n - 1)).replace('0', 'a').replace('1', 'b')
            if not prim(w): continue
            for s in range(n - d + 1):
                D = set(range(s, s + d))
                W, dec = minW(w, D, m, R, d)
                hist[W] = hist.get(W, 0) + 1
                key = 99 if W is None else W
                if key > worst[0]: worst = (key, (w, s, dec))
        print(n, d, m, R, hist, worst, flush=True)
    else:
        w = sys.argv[2]; D = set(map(int, sys.argv[3].split(','))); m, R = int(sys.argv[4]), int(sys.argv[5])
        print(w, minW(w, D, m, R, len(D)))
