"""r17_oh_search_engine.py -- generic exact tools for small CFGs over {a,b}.

Grammar: dict NT -> list of rules; a rule is a tuple of symbols ('a','b' terminals, other strings NTs).
Every non-empty rule must contain >= 1 terminal (so length-n data depends only on shorter lengths).

  words(G, N)        -> {NT: [set of words of length n] for n<=N}   (distinct words)
  parses(G, N)       -> {NT: [parse-tree count, exact int]}
  scaled(G, N)       -> {NT: numpy array c_n = (#parses of length n) * 2^-n}   (float, fast, N ~ 400+)
  in_Gminus(w)       -> True iff d_k(w) < 0 for all 1<=k<=n/2
  check(G, N)        -> dict(first_out=(n,word) or None, first_amb=(n,word) or None, counts=[...])
"""
import numpy as np
from collections import Counter

def in_Gminus(w):
    n = len(w); d = 0
    for k in range(1, n // 2 + 1):
        d += (w[k - 1] == 'a') - (w[n - k] == 'a')
        if d >= 0:
            return False
    return True

def first_violation_k(w):
    n = len(w); d = 0
    for k in range(1, n // 2 + 1):
        d += (w[k - 1] == 'a') - (w[n - k] == 'a')
        if d >= 0:
            return k
    return None

def _nts(G):
    return list(G.keys())

def _split(rule):
    """terminal count, list of NTs, and template for building words."""
    t = sum(1 for s in rule if s in ('a', 'b'))
    return t

def words(G, N, keep_multi_for=None):
    W = {X: [set() for _ in range(N + 1)] for X in G}
    for X, rules in G.items():
        for r in rules:
            if len(r) == 0:
                W[X][0].add('')
    for n in range(1, N + 1):
        for X, rules in G.items():
            acc = W[X][n]
            for r in rules:
                if len(r) == 0:
                    continue
                t = _split(r)
                if t > n:
                    continue
                # distribute remaining length n-t among NT slots
                partial = [('', 0)]
                for s in r:
                    new = []
                    if s in ('a', 'b'):
                        for (pw, L) in partial:
                            new.append((pw + s, L))
                    else:
                        for (pw, L) in partial:
                            # budget for this NT: n - t - L_used - (min of rest, assume 0)
                            for m in range(0, n - t - L + 1):
                                for y in W[s][m]:
                                    new.append((pw + y, L + m))
                    partial = new
                for (pw, L) in partial:
                    if L == n - t:
                        acc.add(pw)
    return W

def words_multi(G, X, N, W):
    """list (with multiplicity at top level only) of words of X of length N given sets W of sub-NTs."""
    out = []
    n = N
    for r in G[X]:
        if len(r) == 0:
            if n == 0:
                out.append('')
            continue
        t = _split(r)
        if t > n:
            continue
        partial = [('', 0)]
        for s in r:
            new = []
            if s in ('a', 'b'):
                for (pw, L) in partial:
                    new.append((pw + s, L))
            else:
                for (pw, L) in partial:
                    for m in range(0, n - t - L + 1):
                        for y in W[s][m]:
                            new.append((pw + y, L + m))
            partial = new
        out.extend(pw for (pw, L) in partial if L == n - t)
    return out

def parses(G, N):
    P = {X: [0] * (N + 1) for X in G}
    for X, rules in G.items():
        P[X][0] = sum(1 for r in rules if len(r) == 0)
    for n in range(1, N + 1):
        for X, rules in G.items():
            tot = 0
            for r in rules:
                if len(r) == 0:
                    continue
                t = _split(r)
                if t > n:
                    continue
                nts = [s for s in r if s not in ('a', 'b')]
                poly = [1] + [0] * (n - t)
                for s in nts:
                    new = [0] * (n - t + 1)
                    for i, c in enumerate(poly):
                        if c:
                            for m in range(0, n - t - i + 1):
                                v = P[s][m]
                                if v:
                                    new[i + m] += c * v
                    poly = new
                tot += poly[n - t]
            P[X][n] = tot
    return P

def scaled(G, N):
    """c_n(X) = parses_n(X) 2^-n as floats; O(N^2) via incremental chain products."""
    names = list(G)
    C = {X: np.zeros(N + 1) for X in names}
    for X in names:
        C[X][0] = sum(1 for r in G[X] if len(r) == 0)
    chains = []  # (X, t, [prefix-product arrays], nts)
    for X in names:
        for r in G[X]:
            if len(r) == 0:
                continue
            nts = [s for s in r if s not in ('a', 'b')]
            t = _split(r)
            prods = [np.zeros(N + 1) for _ in nts]
            chains.append((X, t, nts, prods))
    def upd(m):
        for (X, t, nts, prods) in chains:
            for j, s in enumerate(nts):
                if j == 0:
                    prods[0][m] = C[s][m]
                else:
                    a = prods[j - 1][:m + 1]; b = C[s][:m + 1][::-1]
                    prods[j][m] = float(np.dot(a, b))
    upd(0)  # products at index 0 (nullable parts)
    for n in range(1, N + 1):
        for X in names:
            pass
        newvals = {X: 0.0 for X in names}
        for (X, t, nts, prods) in chains:
            m = n - t
            if m < 0:
                continue
            val = prods[-1][m] if nts else (1.0 if m == 0 else 0.0)
            newvals[X] += val * 2.0 ** (-t)
        for X in names:
            C[X][n] = newvals[X]
        upd(n)
    return C

def check(G, N, start='S', verbose=False):
    W = words(G, N - 1) if N >= 1 else None
    P = parses(G, N)
    res = {'first_out': None, 'first_amb': None, 'counts': []}
    for n in range(0, N + 1):
        if n < N:
            S = W[start][n]
            multi = None
        else:
            multi = words_multi(G, start, N, W)
            S = set(multi)
        res['counts'].append(len(S))
        if res['first_out'] is None:
            for w in sorted(S):
                if not in_Gminus(w) and n >= 2:
                    res['first_out'] = (n, w); break
        if res['first_amb'] is None and P[start][n] != len(S):
            ex = None
            if multi is not None:
                c = Counter(multi); ex = next((w for w, k in c.items() if k > 1), None)
            else:
                ml = words_multi(G, start, n, W)
                c = Counter(ml); ex = next((w for w, k in c.items() if k > 1), None)
                if ex is None:
                    ex = 'sub-NT ambiguity'
            res['first_amb'] = (n, ex)
        if res['first_out'] and res['first_amb']:
            break
    return res
