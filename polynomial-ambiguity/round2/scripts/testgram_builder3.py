"""Task G (builder3.md, union U). builder3 gives NO grammar: U is defined by membership tests (cov.c) with CF-ness
argued by closure properties. This script computes a WITNESS-COUNT PROXY for the natural 'guess the witness, then
verify' grammar of each family (rotation r / axis c / sign / (one,l,s) / Parikh line / T-level rotation), summed
over the 13 families of cov.c (union grammar S -> S_1 | ... | S_13 adds tree counts). It is a tree count of an
explicit grammar only under the assumption that each per-witness verifier grammar is unambiguous.
Port of cov.c with B=3, LMAX=8, ANYT=1, TAK=2 (the report's final parameters). Words: a=0, b=1.
Membership (W>0) is cross-checked against primitivity for all n <= NMAX (cov.c reports full coverage for n <= 25)."""
import sys
from math import gcd
from functools import lru_cache
B, LMAX, ANYT = 3, 8, 1

def domv(v):
    m = len(v); st = 0
    for i in range(m // 2):
        if v[i] > v[m - 1 - i]: return 0
        if v[i] < v[m - 1 - i]: st = 1
    return st

def W_D(w):
    n = len(w); c = 0
    for r in range(n):
        v = w[r:] + w[:r]; c += domv(v) + domv(v[1:])
    return c

def W_GB(w):
    n = len(w); c = 0
    for s in range(n):
        m = sum(1 for i in range(n) if w[i] == 1 and w[(s - i) % n] == 0); r = n - 2 * m
        if (m <= B or r <= B) and gcd(m, r) == 1: c += 1
    return c

def runs(w):
    n = len(w); st = next((i for i in range(n) if w[i] != w[i - 1]), None)
    if st is None: return []
    L = []; i = 0
    while i < n:
        j = i
        while j < n and w[(st + j) % n] == w[(st + i) % n]: j += 1
        L.append(j - i); i = j
    return L

def W_RD(w):
    L = runs(w); K = len(L); c = 0
    if not K: return 0
    for cc in range(0, K, 2):
        for sg in (1, -1):
            st = 0; ok = 1
            for t in range(1, K // 2):
                i = (cc // 2 + t) % K; x, y = L[i], L[(cc - i) % K]
                if sg < 0: x, y = y, x
                if x > y: ok = 0; break
                if x < y: st = 1
            if ok and st: c += 1
    return c

def W_RGB(w):
    L = runs(w); K = len(L); c = 0
    for cc in range(0, K, 2):
        nz = sum(1 for i in range(K) if L[i] != L[(cc - i) % K]); mm = nz // 2; r = K - 2 * mm
        if mm >= 1 and (mm <= B or r <= B) and gcd(mm, r) == 1: c += 1
    return c

def W_EP(w):
    b = sum(w); d = 2 * b - len(w); return int(d in (1, -1))

def W_PAR(w):
    b = sum(w); a = len(w) - b
    if gcd(a, b) != 1: return 0
    c = int(a <= B or b <= B)
    c += sum(1 for al in range(1, B + 1) for be in range(1, B + 1) if al * a - be * b in (1, -1))
    return c

def blocks(w, one):
    n = len(w); st = next((i for i in range(n) if w[i] == one), None)
    if st is None: return []
    x = []; cnt = 0
    for j in range(1, n + 1):
        if w[(st + j) % n] == one: x.append(cnt); cnt = 0
        else: cnt += 1
    return x

def Cl_count(x, l):
    K = len(x)
    if K % l or K < 2 * l: return 0
    tot = 0
    for s in range(K):
        D = [x[i] - x[(s - i) % K] for i in range(K)]; ok = 1; f = -1
        for c in range(l):
            cr = (s - c) % l
            if cr == c:
                np_ = nn = 0
                for i in range(c, K, l):
                    if D[i] == 0: pass
                    elif D[i] == 1 or (ANYT and D[i] > 0): np_ += 1
                    elif D[i] == -1 or (ANYT and D[i] < 0): nn += 1
                if np_ == 0 and nn == 0: continue
                if np_ == 1 and nn == 1 and f < 0: f = c
                else: ok = 0; break
            elif c < cr:
                pos = any(D[i] > 0 for i in range(c, K, l)); neg = any(D[i] < 0 for i in range(c, K, l))
                if pos and neg: ok = 0; break
        if ok and f >= 0: tot += 1
    return tot

def W_L(w):
    return sum(Cl_count(x, l) for one in (0, 1) for x in [blocks(w, one)] if x for l in range(1, LMAX + 1))

def W_BGB(w):
    c = 0
    for one in (0, 1):
        x = blocks(w, one); K = len(x)
        if K < 2: continue
        for s in range(K):
            mm = sum(1 for i in range(K) if x[i] > x[(s - i) % K]); r = K - 2 * mm
            if mm >= 1 and (mm <= B or r <= B) and gcd(mm, r) == 1: c += 1
    return c

def pieces(w):
    """type word (tuple, 0='a'-piece, 1='z a'-piece) of the canonical rotation (after swap); None if Delta=0."""
    n = len(w); v = [1 if c == 0 else -1 for c in w]; D = sum(v)
    if D == 0: return None
    if D < 0: v = [-x for x in v]
    s = best = arg = 0
    for t in range(n):
        if s > best: best, arg = s, t
        s += v[t]
    u = v[arg:] + v[:arg]; out = []; s = rec = 0; start = 0
    for t, x in enumerate(u):
        s += x
        if s > rec: rec = s; out.append(0 if t == start else 1); start = t + 1
    return tuple(out)

def G_member(w):
    p = pieces(w)
    if p is None: return 0
    # need piece kinds a / ba.. / bb.. : recompute pieces' second letters
    n = len(w); v = [1 if c == 0 else -1 for c in w]; D = sum(v)
    if D < 0: v = [-x for x in v]
    s = best = arg = 0
    for t in range(n):
        if s > best: best, arg = s, t
        s += v[t]
    u = v[arg:] + v[:arg]; g = 0; s = rec = 0; start = 0
    for t, x in enumerate(u):
        s += x
        if s > rec:
            rec = s
            if t == start: g += 1
            elif u[start + 1] == 1: g -= 2
            start = t + 1
    return int(g in (1, -1))

def W_Gfam(w):            # Cyc of a one-counter test on pieces: one tree per canonical rotation
    p = pieces(w); return len(p) * G_member(w) if p else 0

def W_Efix(v):            # walk E' grammar, repaired (unambiguous K)
    D = len(v) - 2 * sum(v)
    if D not in (1, -1): return 0
    maj = 0 if D == 1 else 1; h = cnt = 0
    for c in v:
        if h == 0 and c == maj: cnt += 1
        h += 1 if c == 0 else -1
    return cnt

def Tcount(w, inner):
    p = pieces(w)
    if p is None: return 0
    return sum(inner(p[t:] + p[:t]) for t in range(len(p)))

@lru_cache(maxsize=None)
def W_Tk(w, k):           # T^k(E'), repaired grammar
    if k == 0: return W_Efix(w)
    return Tcount(w, lambda u: W_Tk(u, k - 1))

@lru_cache(maxsize=None)
def W_TG(w, k):           # cov.c inT(.,k,useG=1): G  u  (k==0 ? E' : T(TG_{k-1}))
    return W_Gfam(w) + (W_Efix(w) if k == 0 else Tcount(w, lambda u: W_TG(u, k - 1)))

@lru_cache(maxsize=None)
def W_BASE(w):
    return (W_D(w) + W_GB(w) + W_RD(w) + W_RGB(w) + W_EP(w) + W_PAR(w) + W_L(w) + W_BGB(w) + W_Gfam(w))

@lru_cache(maxsize=None)
def W_TA(w, k):
    c = W_BASE(w)
    if k == 0: return c
    p = pieces(w)
    if p is None or len(p) == len(w): return c
    return c + Tcount(w, lambda u: W_TA(u, k - 1))

FAM = [('D', W_D), ('GB', W_GB), ('RD', W_RD), ('RGB', W_RGB), ('EP', W_EP), ('PAR', W_PAR), ('L*', W_L), ('BGB', W_BGB),
       ('T1', lambda w: W_Tk(w, 1)), ('T2', lambda w: W_Tk(w, 2)), ('T3', lambda w: W_Tk(w, 3)),
       ('TG2', lambda w: W_TG(w, 2)), ('TA', lambda w: W_TA(w, 2))]

def lyndon(n):
    w = [-1]
    while w:
        w[-1] += 1
        if len(w) == n: yield tuple(w)
        m = len(w)
        while len(w) < n: w.append(w[len(w) - m])
        while w and w[-1] == 1: w.pop()

def primitive(w):
    n = len(w); return all(w[d:] + w[:d] != w for d in range(1, n) if n % d == 0)

if __name__ == '__main__':
    NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 16
    A = 0
    for n in range(1, NMAX + 1):
        best = (0, None, None); miss = 0; tot = 0; fammax = {f: 0 for f, _ in FAM}
        for w in lyndon(n):               # W is rotation invariant; swap: evaluate both
            for u in (w, tuple(1 - c for c in w)):
                vals = {f: g(u) for f, g in FAM}; W = sum(vals.values()); tot += 1
                for f in vals: fammax[f] = max(fammax[f], vals[f])
                if W == 0: miss += 1
                if W > best[0]: best = (W, ''.join('ab'[c] for c in u), {f: v for f, v in vals.items() if v})
        if best[0] > A: A = best[0]
        print(f"n={n} primitive-classes(x2 swap)={tot} uncovered={miss} maxW(n)={best[0]} A(n)={A} arg={best[1]} parts={best[2]} fammax={fammax}", flush=True)
