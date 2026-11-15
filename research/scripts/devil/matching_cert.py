"""
Non-crossing labelled-matching certificates for primitive integer sequences
(the Kaszonyi-Katsura language Q_n = Q ∩ (ab*)^n, exponent set E_n ⊆ N^n).

A certificate for x is a set M of pairwise vertex-disjoint, pairwise non-crossing chords
of the n-cycle; the labels are the true relations (<,=,>) of x on the chords.
The certificate is SOUND iff for every prime p | n no (n/p)-periodic vector satisfies the
labels; then the set C(M,labels) is a stratified linear-set union (CF), contained in E_n.
Question: is every primitive x certified by some M?   (If yes for all n: KK conjecture.)

Usage: python3 matching_cert.py n K            exhaustive over {0..K}^n
       python3 matching_cert.py n K rand N     random sample
       python3 matching_cert.py n K W N        random sample from W = sum of periodic subspaces
"""
import sys, itertools, random
from functools import lru_cache
from sympy import primefactors

def noncrossing_matchings(n):
    """all non-crossing partial matchings on vertices 0..n-1 (linear order = cycle cut)"""
    @lru_cache(None)
    def rec(lo, hi):  # matchings on interval [lo, hi)
        if hi - lo <= 1:
            return [()]
        res = []
        # lo unmatched
        for m in rec(lo + 1, hi):
            res.append(m)
        # lo matched with j
        for j in range(lo + 1, hi):
            for m1 in rec(lo + 1, j):
                for m2 in rec(j + 1, hi):
                    res.append(((lo, j),) + m1 + m2)
        return res
    return rec(0, n)

def maximal(M, n):
    used = set(v for e in M for v in e)
    free = [v for v in range(n) if v not in used]
    # can we add chord (u,v) between free vertices without crossing?
    for a in range(len(free)):
        for b in range(a + 1, len(free)):
            u, v = free[a], free[b]
            ok = True
            for (i, j) in M:
                if (u < i < v < j) or (i < u < j < v):
                    ok = False; break
            if ok:
                return False
    return True

def periodic(v, d):
    n = len(v)
    return all(v[i] == v[(i + d) % n] for i in range(n))

def primitive(v):
    n = len(v)
    return not any(periodic(v, n // p) for p in primefactors(n))

def inconsistent(rels, d):
    """rels: list of (i,j,s) with s in {-1,0,1} meaning sign(x_j - x_i) = s.
    Project to residues mod d; return True iff no vector y in Z^d satisfies them."""
    parent = list(range(d))
    def f(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]; a = parent[a]
        return a
    for i, j, s in rels:
        if s == 0:
            parent[f(i % d)] = f(j % d)
    edges = {}
    for i, j, s in rels:
        if s == 0: continue
        a, b = f(i % d), f(j % d)
        if s < 0: a, b = b, a  # now x_a < x_b strictly
        if a == b:
            return True
        edges.setdefault(a, set()).add(b)
    # cycle detection
    color = {}
    def dfs(u):
        color[u] = 1
        for w in edges.get(u, ()):
            c = color.get(w, 0)
            if c == 1: return True
            if c == 0 and dfs(w): return True
        color[u] = 2
        return False
    for u in list(edges):
        if color.get(u, 0) == 0 and dfs(u):
            return True
    return False

def certify(x, Ms, ds):
    for M in Ms:
        rels = []
        for (i, j) in M:
            rels.append((i, j, (x[j] > x[i]) - (x[j] < x[i])))
        if all(inconsistent(rels, d) for d in ds):
            return M
    return None

def main():
    n = int(sys.argv[1]); K = int(sys.argv[2])
    ds = [n // p for p in primefactors(n)]
    Ms = [M for M in noncrossing_matchings(n) if maximal(M, n)]
    print(f"n={n}: {len(Ms)} maximal non-crossing matchings")
    mode = sys.argv[3] if len(sys.argv) > 3 else 'all'
    rng = random.Random(7)
    if mode == 'all':
        it = itertools.product(range(K + 1), repeat=n)
    elif mode == 'rand':
        N = int(sys.argv[4])
        it = (tuple(rng.randint(0, K) for _ in range(n)) for _ in range(N))
    else:  # W
        N = int(sys.argv[4])
        def gen():
            for _ in range(N):
                x = [0] * n
                for d in ds:
                    y = [rng.randint(0, K) for _ in range(d)]
                    for i in range(n):
                        x[i] += y[i % d]
                yield tuple(x)
        it = gen()
    cnt = bad = 0
    for x in it:
        if not primitive(x):
            continue
        cnt += 1
        if certify(x, Ms, ds) is None:
            bad += 1
            if bad <= 10:
                print("UNCERTIFIED", x)
    print(f"n={n} K={K} mode={mode}: primitive tested={cnt}, uncertified={bad}")

if __name__ == '__main__':
    main()
