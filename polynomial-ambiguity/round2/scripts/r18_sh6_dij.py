"""r18_sh6_dij: EXACT minimal IF-violation length for X -> uXv | w with literal / prime-Dyck-block sides.
Dijkstra over lazy Sardinas-Patterson states (see r18_sh6_sp.py) with cost = |U|+|V| committed so far
(common prefix + leader surplus; a pending block of height h counts h, a fresh block 2, joint block-block
resolution uses the shortest joint path). Cost is monotone, so the first balanced state popped gives the minimal
|U|+|V| of two distinct pumping sequences with the same interface (= minimal IF witness), and if the frontier's
minimum cost exceeds K, there is NO IF violation with |U|+|V| <= K (exact certificate, not sampling).
Usage: r18_sh6_dij.py NAME KMAX [statecap]"""
import sys, heapq, itertools
from r18_sh6_sp import EX, gens, items, PLUS

def step(tape, q1, q2):
    """cancel heads; return (q1, q2, consumed_letters_lower_bound) or None"""
    p = PLUS[tape]; q1 = list(q1); q2 = list(q2); c = 0
    while q1 and q2:
        x, y = q1[0], q2[0]
        if isinstance(x, str) and isinstance(y, str):
            if x != y: return None
            q1.pop(0); q2.pop(0); c += 1; continue
        if isinstance(x, tuple) and isinstance(y, tuple):
            hx, hy = x[1], y[1]
            if hx == hy:
                q1.pop(0); q2.pop(0); c += max(hx, 2) if hx == 0 else hx
            elif hx < hy:
                q1.pop(0); q2[0] = ('K', hy - hx); c += 2 if hx == 0 else hx
                if hx == 0: q2[0] = ('K', hy)
            else:
                q2.pop(0); q1[0] = ('K', hx - hy); c += 2 if hy == 0 else hy
                if hy == 0: q1[0] = ('K', hx)
            continue
        sw = isinstance(y, tuple)
        if sw: q1, q2 = q2, q1; x, y = y, x
        h = x[1] + (1 if y == p else -1)
        if h < 0 or (x[1] == 0 and h == 0): return None
        q2.pop(0); c += 1
        if h == 0: q1.pop(0)
        else: q1[0] = ('K', h)
        if sw: q1, q2 = q2, q1
    return tuple(q1), tuple(q2), c

def sur(q):
    return sum(1 if isinstance(x, str) else (x[1] if x[1] else 2) for x in q)

def run(name, K, cap=5 * 10**6):
    G = gens(EX[name]); n = len(G); cnt = itertools.count()
    best = {}; par = {}; h = []
    def push(L, R, common, parent, move):
        st = (L[:2], R[:2]); cost = common + sur(L[0]) + sur(L[1]) + sur(R[0]) + sur(R[1])
        if cost > K: return
        if st not in best or cost < best[st][0]:
            best[st] = (cost, common); par[st] = (parent, move); heapq.heappush(h, (cost, next(cnt), st))
    for i in range(n):
        for j in range(n):
            if i == j: continue
            L = step('L', items(G[i][0]), items(G[j][0])); R = step('R', items(G[i][1]), items(G[j][1]))
            if L and R: push(L, R, L[2] + R[2], None, (i, j))
    while h:
        cost, _, st = heapq.heappop(h)
        if best[st][0] != cost: continue
        (l1, l2), (r1, r2) = st; common = best[st][1]
        if not (l1 or l2 or r1 or r2):
            s1, s2 = [], []; x = st
            while x is not None:
                parent, mv = par[x]
                if parent is None: s1.append(mv[0]); s2.append(mv[1])
                elif mv[0] == 1: s1.append(mv[1])
                else: s2.append(mv[1])
                x = parent
            return 'WITNESS', cost, s1[::-1], s2[::-1], len(best)
        p = 1 if ((not l1 and l2) or (not r1 and r2)) else 2
        for g in range(n):
            gl, gr = items(G[g][0]), items(G[g][1])
            if p == 1: L = step('L', l1 + gl, l2); R = step('R', r1 + gr, r2)
            else: L = step('L', l1, l2 + gl); R = step('R', r1, r2 + gr)
            if L and R:
                push(L, R, common + L[2] + R[2], st, (p, g))
        if len(best) > cap: return 'CAP at cost %d' % cost, cost, None, None, len(best)
    return 'NONE with |U|+|V| <= %d' % K, K, None, None, len(best)

if __name__ == '__main__':
    name, K = sys.argv[1], int(sys.argv[2]); cap = int(sys.argv[3]) if len(sys.argv) > 3 else 5 * 10**6
    res, c, s1, s2, ns = run(name, K, cap)
    print(name, res, 'cost', c, 'states', ns, flush=True)
    if s1:
        T = EX[name]
        print(' seq1:', ' '.join('(%s,%s)' % T[g] for g in s1)); print(' seq2:', ' '.join('(%s,%s)' % T[g] for g in s2))
