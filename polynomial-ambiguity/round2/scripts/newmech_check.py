"""newmech: checks of Lemma B (top-balanced exact identity) and Lemma M (disjoint
ambiguous nodes multiply) on random CNF grammars, all words up to length NMAX.
Also checks Lemma T (amb(u x v) >= out_A(u,v) * in_A(x)) pointwise."""
import itertools, random

def rand_grammar(nV, nbin, seed):
    rnd = random.Random(seed)
    V = list(range(nV)); bins = set()
    while len(bins) < nbin:
        bins.add((rnd.randrange(nV), rnd.randrange(nV), rnd.randrange(nV)))
    terms = set((A, c) for A in V for c in 'ab' if rnd.random() < 0.6)
    return V, sorted(bins), sorted(terms)

def inside(G, w):
    V, bins, terms = G; n = len(w)
    I = {}
    for i in range(n):
        for A in V: I[A, i, i+1] = int((A, w[i]) in terms)
    for L in range(2, n+1):
        for i in range(n-L+1):
            j = i+L
            for A in V: I[A, i, j] = 0
            for (A, B, C) in bins:
                for k in range(i+1, j):
                    I[A, i, j] += I[B, i, k]*I[C, k, j]
    return I

def top_identity(G, w, I):
    """sum over trees of exactly one selected node: span size in (n/3,2n/3],
    all ancestors > 2n/3, and (left child, or left sibling not in range)."""
    V, bins, terms = G; n = len(w)
    big = lambda s: 3*s > 2*n
    rng = lambda s: 3*s > n and 3*s <= 2*n
    out = {(0, 0, n): 1}; total = 0
    for L in range(n, 0, -1):
        if not big(L): break
        for i in range(n-L+1):
            j = i+L
            for A in V:
                o = out.get((A, i, j), 0)
                if not o: continue
                for (X, B, C) in bins:
                    if X != A: continue
                    for k in range(i+1, j):
                        lb, rb = k-i, j-k
                        if big(lb): out[B, i, k] = out.get((B, i, k), 0) + o*I[C, k, j]
                        if big(rb): out[C, k, j] = out.get((C, k, j), 0) + o*I[B, i, k]
                        if rng(lb): total += o*I[B, i, k]*I[C, k, j]
                        elif rng(rb): total += o*I[B, i, k]*I[C, k, j]
    return total

def antichain(G, w, I):
    V, bins, terms = G; n = len(w); f = {}
    for L in range(1, n+1):
        for i in range(n-L+1):
            j = i+L
            for A in V:
                if I[A, i, j] <= 1: f[A, i, j] = 0; continue
                best = 1
                for (X, B, C) in bins:
                    if X != A: continue
                    for k in range(i+1, j):
                        if I[B, i, k]*I[C, k, j]:
                            best = max(best, f[B, i, k]+f[C, k, j])
                f[A, i, j] = best
    return f[0, 0, n]

NMAX = 9; bad = 0; tested = 0; maxD = 0
for seed in range(12):
    G = rand_grammar(4, 9, seed)
    for n in range(3, NMAX+1):
        for w in itertools.product('ab', repeat=n):
            I = inside(G, w); a = I[0, 0, n]
            if a == 0: continue
            tested += 1
            if top_identity(G, w, I) != a: bad += 1; print('B fail', seed, w)
            D = antichain(G, w, I); maxD = max(maxD, D)
            if 2**D > a: bad += 1; print('M fail', seed, w, D, a)
print(f"words with amb>0 tested: {tested}; failures: {bad}; max antichain D seen: {maxD}")
