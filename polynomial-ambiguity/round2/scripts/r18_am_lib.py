"""r18_am_lib: single-nonterminal linear SCC X -> u X v | w with literal or block sides.
A side spec is a literal string or 'B' (prime Dyck block a D b, a=+1,b=-1; mass 1/2, tail ~ k^{-3/2}).
Tree mass 2^{-|M|}. Exact enumeration and exact-count sampling of the multiplicity m(W) and the
top-divergence pair mass D0."""
import random, sys
from functools import lru_cache
from collections import defaultdict
sys.setrecursionlimit(100000)

def dyck_prime(maxlen):
    # all prime Dyck words (a D b) by length
    D = {0: ['']}
    for n in range(2, maxlen + 1, 2):
        D[n] = []
        for k in range(0, n - 1, 2):  # D = a D1 b D2, |D1|=k
            for x in D[k]:
                for y in D[n - 2 - k]:
                    D[n].append('a' + x + 'b' + y)
    P = defaultdict(list)
    for n in range(2, maxlen + 1, 2):
        for x in D[n - 2]:
            P[n].append('a' + x + 'b')
    return P

def side_words(spec, maxlen, P):
    if spec == 'B':
        return [w for n in sorted(P) if n <= maxlen for w in P[n]]
    return [spec] if len(spec) <= maxlen else []

def tokens_upto(G, L):
    P = dyck_prime(L)
    toks = []
    for ti, (us, vs) in enumerate(G['tok']):
        for u in side_words(us, L, P):
            for v in side_words(vs, L - len(u), P):
                if u or v:
                    toks.append((ti, u, v))
    return toks

def enumerate_trees(G, K):
    """all trees with |M|<=K: dict word -> dict first-token -> count"""
    toks = tokens_upto(G, K)
    w = G['w']
    words = defaultdict(lambda: defaultdict(int))
    def rec(U, V, first, depth):
        M = U + w + V
        words[M][first] += 1
        for (ti, u, v) in toks:
            if len(M) + len(u) + len(v) <= K:
                rec(U + u, v + V, first if first is not None else (ti, u, v), depth + 1)
    rec('', '', None, 0)
    return words

def stats_from_enum(words, K):
    """per length k: u(k), D0(k), E_k[m]"""
    u = [0.0] * (K + 1); D0 = [0.0] * (K + 1); S2 = [0] * (K + 1); S1 = [0] * (K + 1); nw = [0.0] * (K + 1)
    for M, fd in words.items():
        k = len(M); A = sum(fd.values())
        u[k] += A * 2.0 ** -k
        S1[k] += A; S2[k] += A * A
        nw[k] += 2.0 ** -k
        D0[k] += (A * A - sum(c * c for c in fd.values())) * 2.0 ** -k
    Em = [S2[k] / S1[k] if S1[k] else 0 for k in range(K + 1)]
    return u, D0, Em, nw

# ---------- counting multiplicity on a given word ----------
def block_end(W, i):
    """prime Dyck word starting at i: return end index or -1"""
    if i >= len(W) or W[i] != 'a':
        return -1
    h = 0
    for j in range(i, len(W)):
        h += 1 if W[j] == 'a' else -1
        if h == 0:
            return j + 1
    return -1

def block_start(W, j):
    """prime Dyck word ending at j (exclusive): return start or -1"""
    if j <= 0 or W[j - 1] != 'b':
        return -1
    h = 0
    for i in range(j - 1, -1, -1):
        h += 1 if W[i] == 'b' else -1
        if h == 0:
            return i
    return -1

def count_trees(G, W):
    """returns (A_total, dict first-token-type-span -> count) for X =>* W"""
    w = G['w']; n = len(W)
    be = [block_end(W, i) for i in range(n + 1)]
    bs = [block_start(W, j) for j in range(n + 1)]
    memo = {}
    def moves(i, j):
        out = []
        for ti, (us, vs) in enumerate(G['tok']):
            if us == 'B':
                i2 = be[i]
                if i2 < 0: continue
            else:
                if W.startswith(us, i): i2 = i + len(us)
                else: continue
            if vs == 'B':
                j2 = bs[j]
                if j2 < 0: continue
            else:
                if j - len(vs) >= 0 and W[j - len(vs):j] == vs: j2 = j - len(vs)
                else: continue
            if (i2, j2) != (i, j) and j2 - i2 >= len(w):
                out.append(((ti, i2, j2), i2, j2))
        return out
    def A(i, j):
        key = (i, j)
        if key in memo: return memo[key]
        memo[key] = None
        s = 1 if W[i:j] == w else 0
        for _, i2, j2 in moves(i, j):
            s += A(i2, j2)
        memo[key] = s
        return s
    # iterative-ish: recursion depth <= number of tokens
    tot = A(0, n)
    first = {}
    if W == w: first['exit'] = 1
    for key, i2, j2 in moves(0, n):
        first[key] = A(i2, j2)
    return tot, first

# ---------- exact sampler of trees of length n ----------
def token_length_counts(G, L):
    """c[ti][l] = number of tokens of type ti with |u|+|v| = l"""
    from math import comb
    nb = [0] * (L + 1)
    for l in range(2, L + 1, 2):
        k = l // 2 - 1; nb[l] = comb(2 * k, k) // (k + 1)
    c = []
    for us, vs in G['tok']:
        cu = nb if us == 'B' else [1 if l == len(us) else 0 for l in range(L + 1)]
        cv = nb if vs == 'B' else [1 if l == len(vs) else 0 for l in range(L + 1)]
        cc = [0] * (L + 1)
        for a in range(L + 1):
            if cu[a]:
                for b in range(L + 1 - a):
                    if cv[b]: cc[a + b] += cu[a] * cv[b]
        c.append(cc)
    return c, nb

class Sampler:
    def __init__(self, G, L):
        self.G = G; self.L = L
        self.c, self.nb = token_length_counts(G, L)
        lw = len(G['w'])
        T = [0] * (L + 1)
        for n in range(L + 1):
            s = 1 if n == lw else 0
            for cc in self.c:
                for l in range(1, n + 1):
                    if cc[l]: s += cc[l] * T[n - l]
            T[n] = s
        self.T = T
        self.P = dyck_prime(0)  # lazy blocks: generate random prime Dyck uniformly
    def rand_block(self, l, rng):
        # uniform prime Dyck word of length l: a + uniform Dyck(l-2) + b, via cycle lemma
        k = (l - 2) // 2
        s = ['a'] * (k + 1) + ['b'] * k
        rng.shuffle(s)
        # cycle lemma on sequence of k+1 up, k down: unique rotation where all prefix sums >0
        p = [0]
        for ch in s: p.append(p[-1] + (1 if ch == 'a' else -1))
        mn = min(p[:-1]); pos = max(i for i in range(len(s)) if p[i] == mn)
        r = s[pos:] + s[:pos]
        # r = a + Dyck(2k)
        return 'a' + ''.join(r[1:]) + 'b'
    def sample(self, n, rng):
        G = self.G; U = []; V = []
        while True:
            tot = self.T[n]
            x = rng.randrange(tot)
            if n == len(G['w']):
                if x < 1: break
                x -= 1
            done = False
            for ti, cc in enumerate(self.c):
                for l in range(1, n + 1):
                    wgt = cc[l] * self.T[n - l]
                    if x < wgt:
                        us, vs = G['tok'][ti]
                        # split l into |u|,|v| proportional to counts
                        opts = []
                        for a in range(l + 1):
                            cu = (self.nb[a] if a < len(self.nb) else 0) if us == 'B' else (1 if a == len(us) else 0)
                            cv = (self.nb[l - a] if l - a < len(self.nb) else 0) if vs == 'B' else (1 if l - a == len(vs) else 0)
                            if cu * cv: opts.append((a, cu * cv))
                        y = rng.randrange(sum(o[1] for o in opts))
                        for a, wt in opts:
                            if y < wt: break
                            y -= wt
                        u = self.rand_block(a, rng) if us == 'B' else us
                        v = self.rand_block(l - a, rng) if vs == 'B' else vs
                        U.append(u); V.append(v); n -= l; done = True
                        break
                    x -= wgt
                if done: break
        return ''.join(U) + G['w'] + ''.join(reversed(V))

def check_IF(G, K):
    """search for two distinct token sequences with same interface (U,V), |U|+|V|<=K"""
    toks = tokens_upto(G, K)
    seen = {}
    bad = []
    def rec(U, V, seq):
        key = (U, V)
        if seq:
            if key in seen and seen[key] != seq:
                bad.append((seen[key], seq)); return
            seen[key] = seq
        if bad: return
        for t in toks:
            if len(U) + len(V) + len(t[1]) + len(t[2]) <= K:
                rec(U + t[1], t[2] + V, seq + (t,))
    rec('', '', ())
    return bad[:1]
