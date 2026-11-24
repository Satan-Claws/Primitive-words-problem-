"""audit_et_check.py -- audit of Theorem ET / Cor ET (r20_dense.md).
Part 1: Poisson model of c-run tops: eps(g) = sup_mu P(#runs >= M-g is <= 2), checked to be O(2^-g)
        (independent of the fractional part of log2 n, so the lattice oscillation of the max is harmless).
Part 2: mechanical execution of the ET proof (spine of leaf m, step-(g+1) pairs per block, pump down t=0)
        on explicit CNF grammars where the competitor runs are coupled to the leading run by nesting
        (adversarial: V covers one competitor).  Checks that w0 is in L (CYK) and has a competitor > leading run.
"""
import math, itertools
from functools import lru_cache

# ---------------- Part 1 ----------------
def eps(g, mu, K=80):
    # X_k ~ Poisson(mu 2^-k) independent counts of runs of exact level k (k = 1..K)
    lam = [mu * 2.0 ** (-k) for k in range(K + 2)]
    tail = [0.0] * (K + 3)
    for k in range(K, -1, -1): tail[k] = tail[k + 1] + lam[k]
    tot = 0.0
    for M in range(1, K):                    # top level = M  (X_M >= 1, nothing above)
        lo = max(M - g, 0)
        # P(no runs above M) * P(X_M>=1, sum_{lo..M} X <= 2)
        a = math.exp(-tail[M + 1])
        lm = lam[M]; rest = tail[lo] - tail[M]   # Poisson mass on levels lo..M-1
        p = 0.0
        for xm in (1, 2):
            for r in range(0, 3 - xm):
                p += math.exp(-lm) * lm ** xm / math.factorial(xm) * math.exp(-rest) * rest ** r / math.factorial(r)
        tot += a * p
    return tot

print("Part 1: eps(g) (sup/inf over mu = 2^(20+x), x in [0,1)) and 2^g*sup")
for g in [1, 2, 3, 4, 6, 8, 10]:
    vals = [eps(g, 2 ** (20 + x / 16)) for x in range(16)]
    print(f" g={g:2d} sup={max(vals):.4f} inf={min(vals):.4f} 2^g*sup={max(vals) * 2 ** g:.3f}")

# ---------------- Part 2 ----------------
def cyk_tree(G, start, w):
    """G: dict X -> list of rules (('t',c) or ('n',Y,Z)). Returns one parse tree (X,i,j,kids) or None."""
    n = len(w)
    @lru_cache(None)
    def P(X, i, j):
        for r in G[X]:
            if r[0] == 't':
                if j - i == 1 and w[i] == r[1]: return (X, i, j, None)
            else:
                for k in range(i + 1, j):
                    L = P(r[1], i, k)
                    if L:
                        R = P(r[2], k, j)
                        if R: return (X, i, j, (L, R))
        return None
    return P(start, 0, n)

def runs(w, c):
    out, i = [], 0
    while i < len(w):
        if w[i] == c:
            j = i
            while j < len(w) and w[j] == c: j += 1
            out.append((i, j)); i = j
        else: i += 1
    return out

def et_proof(G, start, w, c, g):
    t = cyk_tree(G, start, w); assert t
    m = runs(w, c)[0][1]
    # ancestors of leaf m whose left child lies inside [0,m)
    P, node = [], t
    while node[3]:
        L, R = node[3]
        if L[2] <= m: P.append(node); node = R
        else: node = L
    P = P[::-1]                                  # bottom-up
    NN = len(G); B = (g + 1) * NN + 1
    pairs = []
    for b0 in range(0, len(P) - B + 1, B):
        idx = list(range(b0, b0 + B, g + 1))
        found = None
        for i, j in itertools.combinations(idx, 2):
            if P[i][0] == P[j][0]: found = (i, j); break
        pairs.append(found)
    res = []
    for pr in pairs:
        if not pr: continue
        i, j = pr
        li, ri = P[i][1], P[i][2]; lj, rj = P[j][1], P[j][2]
        w0 = w[:lj] + w[li:ri] + w[rj:]
        ok = cyk_tree(G, start, w0) is not None
        r0 = runs(w0, c); lead = r0[0][1] - r0[0][0] if r0[0][0] == 0 else 0
        best = max(b - a for a, b in r0[1:])
        res.append(((i, j), (lj, li), (ri, rj), ok, lead, best, best > lead))
    return len(P), res

def cnf(rules):
    G = {}
    for X, rhs in rules:
        G.setdefault(X, []).append(('t', rhs) if len(rhs) == 1 and rhs.islower() else ('n', rhs[0], rhs[1]))
    return G

# G1: a^{k} a^{r} b a^k b a^q b   (k nested with first competitor; q free) -- not inside LeadMax, just exercises proof
# S -> A T ;  T -> core B Q ; core: a^k X b a^k  (nested) ; X = a^+ ; Q = a^+ b
G1 = cnf([('S', 'CY'), ('Y', 'BQ'), ('C', 'AD'), ('D', 'CA'), ('D', 'XB'), ('X', 'AX'), ('X', 'a'),
          ('Q', 'AQ'), ('Q', 'AB'), ('A', 'a'), ('B', 'b')])
# G2: a^{k+q} a^r b a^k b a^q b with q nested outside k (two partners, but both inside ONE V each: V_k, V_q)
G2 = cnf([('S', 'HB'), ('H', 'AJ'), ('J', 'HA'), ('H', 'CB'),   # S = a^q (C b) a^q b, C = a^{k+r} b a^k
 ('C', 'AD'), ('D', 'CA'), ('D', 'XB'), ('X', 'AX'), ('X', 'a'),
          ('A', 'a'), ('B', 'b')])
def word2(k, q, r): return 'a' * (k + q + r) + 'b' + 'a' * k + 'b' + 'a' * q + 'b'
print("Part 2: ET proof executed mechanically (g=2)")
for name, G, w in [('G1', G1, 'a' * 41 + 'b' + 'a' * 39 + 'b' + 'a' * 39 + 'b'),
                   ('G2', G2, None)]:
    if w is None:  # G2 cannot have near-ties with large m (k,q <= m/2); show its long words nonetheless
        w = word2(20, 19, 2)
    h, res = et_proof(G, 'S', w, 'a', 2)
    print(f" {name}: |w|={len(w)} h={h} pairs={len(res)}")
    for r in res: print("   pair", r[0], "U", r[1], "V", r[2], "w0 in L:", r[3], "lead", r[4], "best other", r[5], "VIOLATES LeadMax:", r[6])
