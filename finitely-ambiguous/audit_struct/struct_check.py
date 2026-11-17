"""Audit of Lemma 3 (Structure lemma) of PROOF.md.

For a CNF grammar G (rules A->BC, A->'a'|'b') and n, build the product with D_n
(states 0..n = number of a's read), reduce, then:
  * test the structural conclusions of Lemma 3 (a)-(c): linear SCCs, each nontrivial SCC
    a simple ring, every side child has exactly one tree, side children b-only;
  * if they hold: enumerate skeletons exactly as in (d), check (e) independence and
    (f) laminarity, and check (ii) amb(w) = sum_sigma 1[exp(w) in L_sigma] on all
    words with block sizes <= B against a CYK tree count;
  * if they fail: Lemma 3's proof predicts infinite ambiguity; we check that the max tree
    count over words with blocks <= B strictly grows with B (heuristic confirmation).
"""
import itertools, random, sys
from functools import lru_cache
from fractions import Fraction
sys.setrecursionlimit(10000)

def product(G, start, n):
    P = {}
    for A, rules in G.items():
        for s in range(n+1):
            for t in range(s, n+1):
                rs = []
                for r in rules:
                    if r[0] == 't':
                        c = r[1]
                        if c == 'a' and t == s+1: rs.append(r)
                        if c == 'b' and t == s and s >= 1: rs.append(r)
                    else:
                        for q in range(s, t+1):
                            rs.append(('n', (s, r[1], q), (q, r[2], t)))
                P[(s, A, t)] = rs
    S = (0, start, n)
    # productive
    prod = set(); ch = True
    while ch:
        ch = False
        for X, rs in P.items():
            if X in prod: continue
            if any(r[0] == 't' or (r[1] in prod and r[2] in prod) for r in rs):
                prod.add(X); ch = True
    if S not in prod: return None, S
    P = {X: [r for r in rs if r[0] == 't' or (r[1] in prod and r[2] in prod)] for X, rs in P.items() if X in prod}
    reach = {S}; st = [S]
    while st:
        X = st.pop()
        for r in P[X]:
            if r[0] == 'n':
                for Y in r[1:]:
                    if Y not in reach: reach.add(Y); st.append(Y)
    return {X: P[X] for X in reach}, S

def sccs(P):
    idx = {}; low = {}; on = set(); stack = []; out = []; c = [0]
    def strong(v):
        idx[v] = low[v] = c[0]; c[0] += 1; stack.append(v); on.add(v)
        for r in P[v]:
            if r[0] == 'n':
                for w in r[1:]:
                    if w not in idx: strong(w); low[v] = min(low[v], low[w])
                    elif w in on: low[v] = min(low[v], idx[w])
        if low[v] == idx[v]:
            comp = []
            while True:
                w = stack.pop(); on.discard(w); comp.append(w)
                if w == v: break
            out.append(frozenset(comp))
    for v in P:
        if v not in idx: strong(v)
    comp_of = {v: C for C in out for v in C}
    def nontriv(C):
        v = next(iter(C))
        return len(C) > 1 or any(r[0] == 'n' and v in r[1:] for r in P[v])
    return comp_of, nontriv

def word(x):
    return ''.join('a' + 'b'*v for v in x)

def count_trees(P, S, w):
    @lru_cache(None)
    def cnt(X, i, j):
        tot = 0
        for r in P.get(X, []):
            if r[0] == 't':
                if j == i+1 and w[i] == r[1]: tot += 1
            else:
                for k in range(i+1, j):
                    a = cnt(r[1], i, k)
                    if a: tot += a * cnt(r[2], k, j)
        return tot
    return cnt(S, 0, len(w))

def all_trees_vec(P, X, n, seen=()):
    """vectors of all trees of X (only called when X has no nontrivial SCC below)."""
    res = []
    for r in P[X]:
        if r[0] == 't':
            v = [0]*(n+1)
            if r[1] == 'b': v[X[0]] += 1
            res.append(tuple(v))
        else:
            for a in all_trees_vec(P, r[1], n):
                for b in all_trees_vec(P, r[2], n):
                    res.append(tuple(p+q for p, q in zip(a, b)))
    return res

def structure(P, S, n):
    comp_of, nontriv = sccs(P)
    rings = {}
    for C in set(comp_of.values()):
        if not nontriv(C): continue
        ringrule = {}
        for X in C:
            for r in P[X]:
                if r[0] == 'n':
                    k = sum(1 for Y in r[1:] if Y in C)
                    if k == 2: return 'nonlinear', None
                    if k == 1:
                        if X in ringrule: return 'two ring rules at %s' % (X,), None
                        ringrule[X] = r
        # side children: exactly one tree, b-only
        for X, r in ringrule.items():
            Z = r[2] if r[1] in C else r[1]
            below = reach_set(P, Z)
            if any(nontriv(comp_of[Y]) for Y in below):
                return 'side child with nontrivial SCC below', None
            tv = all_trees_vec(P, Z, n)
            if len(tv) != 1: return 'side child %s has %d trees' % (Z, len(tv)), None
        rings[C] = ringrule
    return 'ok', (comp_of, rings)

def reach_set(P, Z):
    R = {Z}; st = [Z]
    while st:
        X = st.pop()
        for r in P[X]:
            if r[0] == 'n':
                for Y in r[1:]:
                    if Y not in R: R.add(Y); st.append(Y)
    return R

def add(a, b): return tuple(p+q for p, q in zip(a, b))

def skeletons(P, S, n, comp_of, rings):
    memo = {}
    def sk(X):
        if X in memo: return memo[X]
        C = comp_of[X]
        res = []
        def exits(Y):
            out = []
            for r in P[Y]:
                if C in rings and r == rings[C].get(Y): continue
                if r[0] == 't':
                    v = [0]*(n+1)
                    if r[1] == 'b': v[Y[0]] += 1
                    out.append((tuple(v), ()))
                else:
                    for (c1, p1) in sk(r[1]):
                        for (c2, p2) in sk(r[2]):
                            out.append((add(c1, c2), p1 + p2))
            return out
        if C not in rings:
            res = exits(X)
        else:
            rr = rings[C]; rlen = len(C)
            # full-turn vector and walk
            cur = X; side = tuple([0]*(n+1)); full = None
            walk = []
            for j in range(rlen):
                walk.append((cur, side))
                r = rr[cur]
                Z, nxt = (r[2], r[1]) if r[1] in C else (r[1], r[2])
                side = add(side, all_trees_vec(P, Z, n)[0])
                cur = nxt
            assert cur == X
            full = side
            s, t = X[0], X[2]
            for (Y, sd) in walk:
                for (c, ps) in exits(Y):
                    res.append((add(c, sd), ps + ((full, (s, t)),)))
        memo[X] = res
        return res
    return sk(S)

def rank(vs):
    M = [[Fraction(x) for x in v] for v in vs]
    r = 0; cols = len(M[0]) if M else 0
    for c in range(cols):
        piv = next((i for i in range(r, len(M)) if M[i][c] != 0), None)
        if piv is None: continue
        M[r], M[piv] = M[piv], M[r]
        for i in range(len(M)):
            if i != r and M[i][c] != 0:
                f = M[i][c] / M[r][c]
                M[i] = [a - f*b for a, b in zip(M[i], M[r])]
        r += 1
    return r

def cross(p, q):
    (s, t), (u, v) = p, q
    return (s < u < t < v) or (u < s < v < t)

def in_lin(c, vs, x):
    # brute force: q_j <= sum(x)
    d = [xi - ci for xi, ci in zip(x, c)]
    if any(di < 0 for di in d) and not vs: return False
    bound = sum(x) + 1
    cnt = 0
    def rec(j, d):
        nonlocal cnt
        if j == len(vs):
            if all(di == 0 for di in d): cnt += 1
            return
        v = vs[j]; q = 0
        while all(di >= 0 for di in d) and q <= bound:
            rec(j+1, d)
            d = tuple(di - vi for di, vi in zip(d, v)); q += 1
    rec(0, tuple(d))
    return cnt

def analyse(G, start, n, B, verbose=False):
    P, S = product(G, start, n)
    if P is None: return 'empty', None
    st, data = structure(P, S, n)
    words = list(itertools.product(range(B+1), repeat=n))
    if st != 'ok':
        mx = []
        for b in range(1, B+1):
            mx.append(max(count_trees(P, S, word(x)) for x in itertools.product(range(b+1), repeat=n)))
        return st, mx
    comp_of, rings = data
    sks = skeletons(P, S, n, comp_of, rings)
    dep = [s for s in sks if rank([v for v, _ in s[1]]) < len(s[1])]
    lam_bad = [s for s in sks if any(cross(p[1], q[1]) for p, q in itertools.combinations(s[1], 2))]
    mism = []
    if not dep:
        for x in words:
            full = (0,) + x
            pred = sum(in_lin(c, [v for v, _ in ps], full) for c, ps in sks)
            act = count_trees(P, S, word(x))
            if pred != act: mism.append((x, pred, act))
    mxB = max(count_trees(P, S, word(x)) for x in words)
    return 'ok', dict(nsk=len(sks), dep=len(dep), lam_bad=len(lam_bad), mism=mism[:5], nmism=len(mism), maxamb=mxB,
                      maxper=max((len(s[1]) for s in sks), default=0))

def rand_grammar(rng, nN=4, nr=7):
    Ns = ['S'] + [chr(ord('A')+i) for i in range(nN-1)]
    G = {A: [] for A in Ns}
    G['S'].append(('n', rng.choice(Ns), rng.choice(Ns)))
    for _ in range(nr):
        A = rng.choice(Ns)
        if rng.random() < 0.35: r = ('t', rng.choice('ab'))
        else: r = ('n', rng.choice(Ns), rng.choice(Ns))
        if r not in G[A]: G[A].append(r)
    return G

if __name__ == '__main__':
    rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
    trials = int(sys.argv[2]) if len(sys.argv) > 2 else 3000
    stats = {}
    suspicious = []
    for it in range(trials):
        n = rng.choice([2, 3])
        G = rand_grammar(rng, nN=rng.choice([3, 4, 5]), nr=rng.choice([5, 7, 9]))
        B = 4 if n == 2 else 3
        st, info = analyse(G, 'S', n, B)
        key = st.split(' ')[0] if st != 'ok' else 'ok'
        stats[key] = stats.get(key, 0) + 1
        if st == 'ok':
            if info['dep']:
                stats['ok_dependent'] = stats.get('ok_dependent', 0) + 1
            if info['lam_bad'] or info['nmism']:
                suspicious.append((G, n, st, info))
            if info['maxper'] >= 2: stats['ok_>=2periods'] = stats.get('ok_>=2periods', 0) + 1
        elif st != 'empty':
            mx = info
            if not all(mx[i] < mx[i+1] for i in range(len(mx)-1)):
                suspicious.append((G, n, st, mx))
    print('stats', stats)
    print('suspicious', len(suspicious))
    for s in suspicious[:10]: print(s)
