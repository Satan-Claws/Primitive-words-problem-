"""Shared tools: exact parse-tree counting for a CFG (cycle-free, eps allowed), Bar-Hillel product
with a DFA, primitivity tests.  Grammar: dict NT -> list of rhs tuples; symbols not in dict are terminals."""
import sys
from functools import lru_cache
sys.setrecursionlimit(100000)

def is_power(w, k):
    n = len(w); return n % k == 0 and n > 0 and w == w[:n // k] * k

def primitive(w):
    n = len(w)
    return n > 0 and all(not is_power(w, p) for p in range(2, n + 1) if n % p == 0)

def count_trees(G, start, w):
    """number of derivation trees of w from start (exact int). Requires no unit/eps cycles."""
    n = len(w)
    memo = {}
    def nt(A, i, j):
        key = (A, i, j)
        if key in memo: return memo[key]
        memo[key] = None  # cycle guard
        tot = 0
        for rhs in G[A]:
            tot += seq(rhs, 0, i, j)
        memo[key] = tot
        return tot
    def seq(rhs, k, i, j):
        if k == len(rhs): return 1 if i == j else 0
        X = rhs[k]
        if X not in G:
            return seq(rhs, k + 1, i + 1, j) if i < j and w[i] == X else 0
        tot = 0
        for m in range(i, j + 1):
            c = nt(X, i, m)
            if c is None: raise RuntimeError("cycle at " + X)
            if c: tot += c * seq(rhs, k + 1, m, j)
        return tot
    return nt(start, 0, n)

def bar_hillel(G, start, dfa_states, delta, q0, finals, alphabet='ab'):
    """CFG for L(G) ∩ L(DFA); keeps tree counts (DFA is deterministic)."""
    H = {}
    def name(A, p, q): return (A, p, q)
    for A, rules in G.items():
        for p in dfa_states:
            for q in dfa_states:
                out = []
                for rhs in rules:
                    # enumerate state sequences
                    def rec(k, cur, acc):
                        if k == len(rhs):
                            if cur == q: out.append(tuple(acc))
                            return
                        X = rhs[k]
                        if X not in G:
                            nxt = delta[(cur, X)]
                            rec(k + 1, nxt, acc + [X])
                        else:
                            for r in dfa_states:
                                rec(k + 1, r, acc + [name(X, cur, r)])
                    rec(0, p, [])
                H[name(A, p, q)] = out
    H['S*'] = [(name(start, q0, f),) for f in finals]
    # prune unproductive
    prod = set(); changed = True
    while changed:
        changed = False
        for A, rules in H.items():
            if A in prod: continue
            if any(all((X not in H) or X in prod for X in r) for r in rules):
                prod.add(A); changed = True
    H2 = {A: [r for r in rules if all((X not in H) or X in prod for X in r)] for A, rules in H.items() if A in prod}
    return H2, 'S*'
