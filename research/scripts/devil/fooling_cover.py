"""
(1) Exact maximum fooling set for Q_n w.r.t. a fixed split (k,m)  [theorem: <= 2*omega(n)+1 when 2m<=n]
(2) Explicit rectangle cover of Q_n with that split via random colourings of the inner words
    (theorem: <= 2*omega(n)*(n+1) rectangles suffice; we report how many were actually needed).
Usage: python3 fooling_cover.py n k m
"""
import sys, random, itertools
from sympy import primefactors
from rect_barrier import is_prim

def maxclique(adj):
    best = [0]
    def bk(R, P, X):
        if not P and not X:
            best[0] = max(best[0], R); return
        if R + len(P) <= best[0]: return
        u = max(P | X, key=lambda v: len(adj[v] & P))
        for v in list(P - adj[u]):
            bk(R + 1, P & adj[v], X & adj[v]); P = P - {v}; X = X | {v}
    bk(0, set(adj), set())
    return best[0]

def main():
    n, k, m = map(int, sys.argv[1:4])
    om = len(primefactors(n))
    words = [''.join(t) for t in itertools.product('ab', repeat=n)]
    Qn = [w for w in words if is_prim(w)]
    split = lambda w: ((w[:k], w[k + m:]), w[k:k + m])
    join = lambda o, x: o[0] + x + o[1]
    # fooling graph
    adj = {i: set() for i in range(len(Qn))}
    sp = [split(w) for w in Qn]
    # for efficiency: for each outer o, Bad(o)
    inners = [''.join(t) for t in itertools.product('ab', repeat=m)]
    outers = sorted(set(o for o, x in sp))
    bad = {o: set(x for x in inners if not is_prim(join(o, x))) for o in outers}
    byinner = {}
    for idx, (o, x) in enumerate(sp):
        byinner.setdefault(x, []).append(idx)
    for i, (o, x) in enumerate(sp):
        for xb in bad[o]:
            for j in byinner.get(xb, []):
                if j != i: adj[i].add(j); adj[j].add(i)
    mc = maxclique(adj)
    print(f"n={n} split k={k} m={m}: |Q_n|={len(Qn)}, omega={om}, max fooling set={mc}, bound={2*om+1 if 2*m<=n else 2*om+3}")
    # rectangle cover by random colourings
    rng = random.Random(0)
    t = max(2, 2 * om)
    uncovered = set(range(len(Qn)))
    rects = 0
    rounds = 0
    while uncovered:
        rounds += 1
        col = {x: rng.randrange(t) for x in inners}
        for c in range(t):
            I = {x for x in inners if col[x] == c}
            O = {o for o in outers if not (bad[o] & I)}
            cov = {i for i in uncovered if sp[i][0] in O and sp[i][1] in I}
            # sanity: rectangle inside Q_n
            for o in O:
                for x in I:
                    assert is_prim(join(o, x))
            if cov:
                rects += 1
                uncovered -= cov
    print(f"   cover: {rects} rectangles (t={t} colours, {rounds} rounds); theorem bound {t*(n+1)}")

if __name__ == '__main__':
    main()
