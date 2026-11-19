#!/usr/bin/env python3
"""mu(w): least N such that w has a binary tree with internal labels in [N] whose rule-grammar
G_w (rules read off the tree, start = root label) generates only primitive words
(checked up to length Lmax -> this gives an UPPER-bound-side test; a word with no good tree
at truncation Lmax certainly has mu > N).  Theorem B: Q is CF iff mu is bounded on Q."""
import sys, itertools
from functools import lru_cache
def prim(s): return len(s) > 0 and (s + s).find(s, 1) == len(s)

def shapes(i, j):
    # all binary trees over leaves i..j-1 ; represented as nested tuples, leaf = int position
    if j - i == 1:
        return [i]
    out = []
    for k in range(i + 1, j):
        for L in shapes(i, k):
            for R in shapes(k, j):
                out.append((L, R))
    return out

def internal(t, acc):
    if isinstance(t, int): return
    acc.append(t); internal(t[0], acc); internal(t[1], acc)

cache = {}
def closure_ok(rules, start, Lmax):
    key = (rules, start)
    if key in cache: return cache[key]
    labs = {x for x, _ in rules}
    W = {X: [set() for _ in range(Lmax + 1)] for X in labs}
    def opts(c, l):
        if isinstance(c, str): return [c] if l == 1 else []
        return W[c][l]
    for l in range(2, Lmax + 1):
        for X, (c1, c2) in rules:
            for l1 in range(1, l):
                A = opts(c1, l1)
                if not A: continue
                B = opts(c2, l - l1)
                if not B: continue
                for a in A:
                    for b in B:
                        W[X][l].add(a + b)
        for s in W[start][l]:
            if not prim(s):
                cache[key] = False; return False
    cache[key] = True; return True

def mu_le(w, N, Lmax):
    n = len(w)
    for t in shapes(0, n):
        nodes = []; internal(t, nodes)
        k = len(nodes)
        # canonical labelings: root label 0, labels introduced in order (symmetry breaking)
        def rec(i, lab, used):
            if i == k:
                yield tuple(lab); return
            for x in range(min(used + 1, N)):
                lab.append(x)
                yield from rec(i + 1, lab, max(used, x + 1))
                lab.pop()
        for lab in rec(0, [], 0):
            idx = {id(nd): lab[q] for q, nd in enumerate(nodes)}
            rules = set()
            for nd in nodes:
                ch = tuple(w[c] if isinstance(c, int) else idx[id(c)] for c in nd)
                rules.add((idx[id(nd)], ch))
            if closure_ok(frozenset(rules), 0, Lmax):
                return True, (t, lab)
    return False, None

if __name__ == '__main__':
    nmax, Nmax, extra = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    for n in range(2, nmax + 1):
        hist = {}; hard = []
        for k in range(2 ** (n - 1)):
            w = 'a' + format(k, '0%db' % (n - 1)).replace('0', 'a').replace('1', 'b')
            if not prim(w): continue
            m = None
            for N in range(1, Nmax + 1):
                if mu_le(w, N, n + extra)[0]:
                    m = N; break
            hist[m] = hist.get(m, 0) + 1
            if m is None or m == Nmax: hard.append(w)
        print(n, hist, hard[:12], flush=True)
