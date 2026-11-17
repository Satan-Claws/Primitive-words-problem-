# Fully generic flat family: u* = 1 + eps*v, v generic (a total order).
# Coverer strategy class: NC perfect matching M, pairs oriented by v (upper->lower),
# needs a directed cycle in Gamma_d(M) for every d.
import itertools, sys, random
from nc_match import nc_matchings, max_divs

def has_dicycle(nv, edges):
    # edges: list of (a,b) directed; loops count
    adj = {a: [] for a in range(nv)}
    for a, b in edges:
        if a == b: return True
        adj[a].append(b)
    color = [0]*nv
    def dfs(u):
        color[u] = 1
        for w in adj[u]:
            if color[w] == 1: return True
            if color[w] == 0 and dfs(w): return True
        color[u] = 2
        return False
    return any(color[u] == 0 and dfs(u) for u in range(nv))

def good(M, v, ds):
    for d in ds:
        edges = []
        for (i, j) in M:
            a, b = (i, j) if v[i] > v[j] else (j, i)
            edges.append((a % d, b % d))
        if not has_dicycle(d, edges):
            return False
    return True

if __name__ == '__main__':
    n = int(sys.argv[1])
    Ms = list(nc_matchings(0, n)); ds = max_divs(n)
    bad = []
    for v in itertools.permutations(range(n)):
        if not any(good(M, v, ds) for M in Ms):
            bad.append(v)
    print(n, 'bad orders', len(bad), 'of', len(list(itertools.permutations(range(n)))))
    print(bad[:10])
