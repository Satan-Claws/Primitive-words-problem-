#!/usr/bin/env python3
"""S4S [computational]: smallest CNF grammars agreeing with Q (primitive words over {a,b})
on all lengths <= L.  CEGAR SAT synthesis (pysat/CaDiCaL): encode CYK derivability only for
substrings of a growing sample of words; verify candidate by exact vectorised CYK on all words
of length <= L; add first disagreements to the sample.  Start symbol = 0.
Usage: s4s_sat_grammar.py NMIN NMAX LMAX TIMEOUT_PER_SOLVE"""
import sys, time, itertools, numpy as np
from pysat.solvers import Solver
from threading import Timer

def Qmask(n):
    x = np.arange(1 << n, dtype=np.int64); prim = np.ones(1 << n, bool)
    for d in range(1, n):
        if n % d: continue
        p = x >> (n - d); rep = np.zeros_like(x)
        for i in range(n // d): rep |= p << (d * i)
        prim &= (rep != x)
    return prim

QM = {}
def Q(n):
    if n not in QM: QM[n] = Qmask(n)
    return QM[n]

def s2(x, n): return ''.join('ab'[(x >> (n - 1 - i)) & 1] for i in range(n))

def cyk_all(N, rules, term, L):
    """masks[n][x] = bitmask of nonterminals deriving word x of length n."""
    T = np.zeros((1 << N, 1 << N), np.int64)
    for m1 in range(1 << N):
        for m2 in range(1 << N):
            r = 0
            for (A, B, C) in rules:
                if (m1 >> B) & 1 and (m2 >> C) & 1: r |= 1 << A
            T[m1, m2] = r
    M = {1: np.array([sum(1 << A for A in range(N) if (A, 0) in term),
                      sum(1 << A for A in range(N) if (A, 1) in term)], np.int64)}
    for n in range(2, L + 1):
        x = np.arange(1 << n, dtype=np.int64); acc = np.zeros(1 << n, np.int64)
        for k in range(1, n):
            acc |= T[M[k][x >> (n - k)], M[n - k][x & ((1 << (n - k)) - 1)]]
        M[n] = acc
    return M

def first_disagreements(N, rules, term, L, maxper=6):
    M = cyk_all(N, rules, term, L)
    for n in range(1, L + 1):
        bad = np.nonzero(((M[n] & 1) == 1) != Q(n))[0]
        if len(bad): return n, [s2(int(x), n) for x in bad[:maxper]], len(bad)
    return None, [], 0

def count_trees(N, rules, term, L):
    """max and mean #derivation trees from S over Q-words, per length (exact ints, memo)."""
    from functools import lru_cache
    byA = {}
    for (A, B, C) in rules: byA.setdefault(A, []).append((B, C))
    @lru_cache(None)
    def cnt(u, A):
        if len(u) == 1: return 1 if (A, 'ab'.index(u)) in term else 0
        s = 0
        for (B, C) in byA.get(A, []):
            for k in range(1, len(u)):
                c1 = cnt(u[:k], B)
                if c1: s += c1 * cnt(u[k:], C)
        return s
    out = []
    for n in range(1, L + 1):
        q = Q(n); mx = 0; tot = 0; c = 0
        for x in range(1 << n):
            if q[x]:
                v = cnt(s2(x, n), 0); mx = max(mx, v); tot += v; c += 1
        out.append((n, mx, tot / c))
        cnt.cache_clear() if n % 4 == 0 else None
    return out

class Enc:
    def __init__(s, N):
        s.N = N; s.nv = 0; s.cl = []
        s.r = {(A, B, C): s.new() for A in range(N) for B in range(N) for C in range(N)}
        s.t = {(A, x): s.new() for A in range(N) for x in (0, 1)}
        s.D = {}; s.solver = Solver(name='cadical153')
        # length-1: S must derive a,b (both primitive)
        s.add([s.t[(0, 0)]]); s.add([s.t[(0, 1)]])
        # mild symmetry breaking: nonterminal 1..N-1 ordered by first usage is costly; skip
    def new(s): s.nv += 1; return s.nv
    def add(s, c): s.solver.add_clause(c)
    def d(s, u):
        """return list of vars D(u,A); build encoding lazily (shared across words)."""
        if u in s.D: return s.D[u]
        N = s.N
        if len(u) == 1:
            s.D[u] = [s.t[(A, 'ab'.index(u))] for A in range(N)]; return s.D[u]
        subs = [(s.d(u[:k]), s.d(u[k:])) for k in range(1, len(u))]
        D = [s.new() for _ in range(N)]
        G = {}
        for B in range(N):
            for C in range(N):
                g = s.new(); G[(B, C)] = g; hs = []
                for (d1, d2) in subs:
                    h = s.new(); hs.append(h)
                    s.add([-h, d1[B]]); s.add([-h, d2[C]]); s.add([h, -d1[B], -d2[C]])
                s.add([-g] + hs)
                for h in hs: s.add([g, -h])
        for A in range(N):
            fs = []
            for B in range(N):
                for C in range(N):
                    g = G[(B, C)]; r = s.r[(A, B, C)]
                    s.add([-r, -g, D[A]])
                    f = s.new(); fs.append(f); s.add([-f, r]); s.add([-f, g])
            s.add([-D[A]] + fs)
        s.D[u] = D; return D
    def require(s, w):
        v = s.d(w)[0]; s.add([v] if Q(len(w))[int(w.replace('a','0').replace('b','1'),2)] else [-v])
    def solve(s, timeout):
        timer = Timer(timeout, lambda: s.solver.interrupt()); timer.start()
        res = s.solver.solve_limited(expect_interrupt=True); timer.cancel()
        if res is None: s.solver.clear_interrupt()
        return res
    def model(s):
        m = set(x for x in s.solver.get_model() if x > 0)
        rules = [k for k, v in s.r.items() if v in m]; term = [k for k, v in s.t.items() if v in m]
        return rules, set(term)

def show(N, rules, term):
    nm = lambda A: 'S' if A == 0 else 'ABCDEFGH'[A - 1]
    lines = []
    for A in range(N):
        rhs = [nm(B) + nm(C) for (X, B, C) in sorted(rules) if X == A] + \
              ['ab'[x] for (X, x) in sorted(term) if X == A]
        if rhs: lines.append(f"  {nm(A)} -> " + ' | '.join(rhs))
    return '\n'.join(lines)

def run(N, LMAX, TO, t_total):
    e = Enc(N); best = None; L = 1; t0 = time.time()
    # seed sample: all words of length <= 2
    for n in range(1, 3):
        for x in range(1 << n): e.require(s2(x, n))
    while L <= LMAX:
        while True:
            if time.time() - t0 > t_total: return best, L, 'TIME'
            res = e.solve(TO)
            if res is None: return best, L, 'TIMEOUT'
            if res is False: return best, L, 'UNSAT'
            rules, term = e.model()
            n, bad, nb = first_disagreements(N, rules, term, L)
            if n is None: break
            for w in bad: e.require(w)
        # grammar agrees through L; record and try to push further
        n, bad, nb = first_disagreements(N, rules, term, max(LMAX + 2, L + 2))
        reach = (n - 1) if n else max(LMAX + 2, L + 2)
        best = (rules, term, reach, n, bad, nb)
        print(f"  N={N}: agrees through L={reach} (#samples {len(e.D)}), first disagree len {n}: {bad[:4]} (#{nb})", flush=True)
        print(show(N, rules, term), flush=True)
        L = reach + 1
    return best, L, 'LMAX'

if __name__ == '__main__':
    NMIN, NMAX, LMAX, TO = map(int, sys.argv[1:5]); TT = float(sys.argv[5]) if len(sys.argv) > 5 else 300
    for N in range(NMIN, NMAX + 1):
        t = time.time()
        best, L, why = run(N, LMAX, TO, TT)
        print(f"N={N}: RESULT max-agreement L={best[2] if best else 0}; L={L} status {why} ({time.time()-t:.0f}s)")
        if best:
            rules, term, reach, n, bad, nb = best
            print(show(N, rules, term)); print(f"  first disagreement at length {n}: {bad} (total {nb} at that length)")
            if reach <= 14:
                for (n_, mx, mean) in count_trees(N, rules, term, reach):
                    print(f"   amb len {n_}: max #trees {mx}, mean {mean:.2f}")
        print(flush=True)
