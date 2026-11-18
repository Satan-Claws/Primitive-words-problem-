#!/usr/bin/env python3
"""Exact tests of multi-pump (k=2) iteration conditions on Q (binary primitive words).

Conditions tested (EVIDENCE only: exponents are checked in a finite box):
  NEST2(W): w = u v1 v2 z x2 x1 y, |v1 v2 z x2 x1| <= W, v1x1 != eps, v2x2 != eps,
            u v1^i v2^j z x2^j x1^i y primitive for all 0<=i,j<=E.
  FREE2(W): same decomposition but loops at the SAME nonterminal: for every
            sequence c in {1,2}^r (r<=R), u v_c1..v_cr z x_cr..x_c1 y primitive.
  Marked variants: marks D = interval; each v_j x_j must meet D, and the
            window v1..x1 may contain at most W marked positions (unmarked parts free).
Usage: python3 multipump.py nmin nmax mode [E] [R]
"""
import sys, itertools

def prim(s):
    n = len(s)
    if n == 0:
        return False
    return (s + s).find(s, 1) == n

def nest_ok(u, v1, v2, z, x2, x1, y, E):
    for i in range(E + 1):
        a = u + v1 * i
        b = x1 * i + y
        for j in range(E + 1):
            if not prim(a + v2 * j + z + x2 * j + b):
                return False
    return True

def free_ok(u, v1, v2, z, x2, x1, y, R):
    V = (v1, v2); X = (x1, x2)
    for r in range(R + 1):
        for c in itertools.product((0, 1), repeat=r):
            s = ''.join(V[t] for t in c)
            t = ''.join(X[t] for t in reversed(c))
            if not prim(u + s + z + t + y):
                return False
    return True

def decomps(w, W, marks=None):
    """yield (u,v1,v2,z,x2,x1,y) nested decompositions.
    full marking: total window length <= W.
    marks (set): each v_j x_j meets marks, window has <= W marks."""
    n = len(w)
    for st in range(n):
        for en in range(st + 1, n + 1):
            win = en - st
            if marks is None:
                if win > W: break
            else:
                if sum(1 for p in range(st, en) if p in marks) > W: break
            # split window into v1 v2 z x2 x1 lengths
            for l1 in range(win + 1):
                for m1 in range(win - l1 + 1):
                    if l1 + m1 == 0: continue
                    rest = win - l1 - m1
                    for l2 in range(rest + 1):
                        for m2 in range(rest - l2 + 1):
                            if l2 + m2 == 0: continue
                            zl = rest - l2 - m2
                            a = st; b = a + l1; c = b + l2; d = c + zl; e = d + m2; f = e + m1
                            assert f == en
                            if marks is not None:
                                if not (any(p in marks for p in range(a, b)) or any(p in marks for p in range(e, f))):
                                    continue
                                if not (any(p in marks for p in range(b, c)) or any(p in marks for p in range(d, e))):
                                    continue
                            yield (w[:a], w[a:b], w[b:c], w[c:d], w[d:e], w[e:f], w[f:])

def minW(w, mode, E, R, marks=None, Wmax=None):
    test = nest_ok if mode == 'nest' else free_ok
    par = E if mode == 'nest' else R
    Wmax = Wmax or len(w)
    for W in range(2, Wmax + 1):
        for d in decomps(w, W, marks):
            # only consider decompositions using exactly budget W (smaller ones already tried)
            if test(*d, par):
                return W, d
    return None, None

if __name__ == '__main__':
    nmin, nmax, mode = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    E = int(sys.argv[4]) if len(sys.argv) > 4 else 4
    R = int(sys.argv[5]) if len(sys.argv) > 5 else 4
    for n in range(nmin, nmax + 1):
        worst = 0; ex = None; hist = {}
        for k in range(2 ** (n - 1)):  # w starts with 'a' (symmetry)
            w = 'a' + format(k, '0%db' % (n - 1)).replace('0', 'a').replace('1', 'b') if n > 1 else 'a'
            if not prim(w):
                continue
            W, d = minW(w, mode, E, R)
            hist[W] = hist.get(W, 0) + 1
            if W is None or W > worst:
                worst = W if W is not None else 10 ** 9; ex = (w, d)
        print(n, mode, 'hist', dict(sorted(hist.items(), key=lambda t: (t[0] is None, t[0] or 0))), 'worst', ex, flush=True)
