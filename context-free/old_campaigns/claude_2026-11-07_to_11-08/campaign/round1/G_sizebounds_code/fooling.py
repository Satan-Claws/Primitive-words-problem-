"""For candidate fooling sets F ⊆ Q_n, compute exactly
    rho(F) = max over balanced intervals I=[i,i+l), n/3<=l<=2n/3,
             of max |S|, S ⊆ F, with f_I g_{~I} primitive for all f,g in S
(i.e. the largest subset of F inside one balanced Q-rectangle).
A fooling-set lower bound needs rho(F) small; the cover theorem predicts
rho(F) >= |F| / (#rectangles in the explicit cover).
"""
import random, sys, itertools
import networkx as nx

def primes_of(n):
    return [p for p in range(2, n + 1) if n % p == 0 and all(p % q for q in range(2, p))]

def is_prim(w):
    n = len(w)
    return all(w[n // p:] + w[:n // p] != w for p in primes_of(n))

def cross(f, g, i, l):
    return f[:i] and None or (g[:i] + f[i:i + l] + g[i + l:])

def rho(F):
    n = len(F[0])
    best = (0, None)
    for l in range((n + 2) // 3, (2 * n) // 3 + 1):
        for i in range(0, n - l + 1):
            G = nx.Graph()
            G.add_nodes_from(range(len(F)))
            for a in range(len(F)):
                for b in range(a + 1, len(F)):
                    f, g = F[a], F[b]
                    if is_prim(g[:i] + f[i:i + l] + g[i + l:]) and is_prim(f[:i] + g[i:i + l] + f[i + l:]):
                        G.add_edge(a, b)
            c, _ = nx.max_weight_clique(G, weight=None)
            if len(c) > best[0]:
                best = (len(c), (i, l))
    return best

def flip(u, j):
    return u[:j] + (1 - u[j],) + u[j + 1:]

def near_squares(n, nu, rng):
    m = n // 2
    F = []
    while len(F) < nu * m:
        u = tuple(rng.randrange(2) for _ in range(m))
        for j in range(m):
            w = u + flip(u, j)
            if is_prim(w):
                F.append(w)
    return F[:nu * m]

def near_powers(n, rng, per=4):
    # u^p with one flipped letter, for every prime p | n, random u
    F = []
    for p in primes_of(n):
        d = n // p
        for _ in range(per):
            u = tuple(rng.randrange(2) for _ in range(d))
            w = list(u * p)
            j = rng.randrange(n)
            w[j] = 1 - w[j]
            w = tuple(w)
            if is_prim(w):
                F.append(w)
    return F

def sparse(n, k):
    F = []
    for S in itertools.combinations(range(n), k):
        w = tuple(1 if t in S else 0 for t in range(n))
        if is_prim(w):
            F.append(w)
    return F

if __name__ == "__main__":
    rng = random.Random(1)
    for n in [12, 18, 24, 30]:
        for name, F in [("near-squares", near_squares(n, 3, rng)),
                        ("near-p-powers", near_powers(n, rng, per=6)),
                        ("random primitive", [w for w in (tuple(rng.randrange(2) for _ in range(n)) for _ in range(60)) if is_prim(w)][:40])]:
            r, where = rho(F)
            print(f"n={n} {name:16s} |F|={len(F):3d} max-in-one-rectangle={r:3d} at (i,l)={where}", flush=True)
    for n, k in [(12, 2), (12, 3), (18, 2)]:
        F = sparse(n, k)
        F = F[:45]
        r, where = rho(F)
        print(f"n={n} sparse k={k}      |F|={len(F):3d} max-in-one-rectangle={r:3d} at (i,l)={where}", flush=True)
