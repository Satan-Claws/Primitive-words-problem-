"""r3_sep_checks: exact checks for R2/r3_sep.md (G-glob' (ii) without (H2)).

Part A  S1 on the modified distribution D' (partial matching of isolated adjacent pairs, NO completion).
        n points on a cycle, A = isolated Bernoulli(1/3) points, M = {{x,x+1} : x in A}.  Every chord bounds the
        outer face, so G_M(S) is complete for every S.  Facets: random +-1 on random S, pair facets e_a - e_b, and the
        transversal facet (sum over one chord per residue class).  Checks (as gglobii_signed_forest): all cells
        |det| = 1, rooted forests, arcs pairwise NC, NC with all M-chords, ply 1 on {mu >= 1}, 0 elsewhere; plus the
        whole 2-point ring graph (M-edges + arcs) is a forest.
Part B  Criterion (N*): max rank of a pairwise non-crossing set of M-laminar rings (||.||_1 <= 2) whose d_M-images lie
        in the joint kernel  cap_k ker mu_k,  versus dim of that kernel.  Cases: O1 (separating chord), and for D'-type
        adjacent chords: J-nest (two pair facets, nested chords), J-disj, J-cross (interleaved), J-share (shared chord).
Part C  Original perfect D (with adjacent completion): how often two A-pairs a = b mod s are face-separated (H2 fails).
Part D  F1-laminarity: M = ballot matchings of balanced blocks, F1 = NC trees with a long chord B0B3 not in M;
        S1 arcs (faces of M) crossing a path edge, fraction of cells.
Usage: .venv/bin/python r3_sep_checks.py [A|B|C|D|all]
"""
import sys, itertools, random
import numpy as np
from gglobii_signed_forest import cells_bfs, check_cell, ply_check, interleave, random_nc_matching


def crosses(p, q):
    return interleave(tuple(p), tuple(q))


def instance(npts, chords, S, mu_S, seed, adj=None):
    """S1 instance on support S (indices into chords), all other chords outside supp mu."""
    rng = random.Random(seed)
    m = len(S)
    orient = [rng.random() < 0.5 for _ in chords]
    plus = [c[0] if o else c[1] for c, o in zip(chords, orient)]
    minus = [c[1] if o else c[0] for c, o in zip(chords, orient)]
    head = [plus[S[i]] if mu_S[i] == 1 else minus[S[i]] for i in range(m)]
    tail = [minus[S[i]] if mu_S[i] == 1 else plus[S[i]] for i in range(m)]
    pos = [i + 0.3 * rng.random() for i in range(npts)]
    cols, cost, kind = [], [], []
    for a in range(m):
        for b in range(m):
            if a == b or (adj is not None and (a, b) not in adj): continue
            v = np.zeros(m); v[a] = 1; v[b] = -1
            cols.append(v); cost.append(abs(pos[head[a]] - pos[tail[b]]) ** 0.5 + 1e-7 * rng.random()); kind.append(('arc', a, b))
    for a in range(m):
        v = np.zeros(m); v[a] = 1; cols.append(v); cost.append(1e-4 * rng.random()); kind.append(('loop', a))
    return dict(m=m, chords=chords, mu=mu_S, head=head, tail=tail, A=np.array(cols).T, c=np.array(cost), kind=kind, rng=rng)


def dprime(n, rng):
    while True:
        X = [rng.random() < 1 / 3 for _ in range(n)]
        A = [x for x in range(n) if X[x] and not X[x - 1] and not X[(x + 1) % n]]
        if len(A) >= 2: return A


def partA(trials=12):
    rng = random.Random(7)
    agg = dict(inst=0, cells=0, det1=True, rooted=True, ncarcs=True, ncM=True, forest=True, viol=0, pts=0)
    for t in range(trials):
        n = rng.choice([12, 16, 20, 24, 30])
        A = dprime(n, rng)
        chords = [(x, (x + 1) % n) if x + 1 < n else (0, n - 1) for x in A]
        kind = t % 3
        if kind == 0:                      # random +-1 facet on random support
            m = min(len(A), rng.randint(2, 6)); S = sorted(rng.sample(range(len(A)), m)); mu = [rng.choice([1, -1]) for _ in S]
        elif kind == 1:                    # pair facet
            S = sorted(rng.sample(range(len(A)), 2)); mu = [1, -1]
        else:                              # transversal-type facet: all +1 on up to 6 chords
            m = min(len(A), rng.randint(3, 6)); S = sorted(rng.sample(range(len(A)), m)); mu = [1] * m
        I = instance(n, chords, S, mu, t)
        cells = cells_bfs(I)
        st = [check_cell(I, C) for C in cells]
        agg['inst'] += 1; agg['cells'] += len(cells)
        agg['det1'] &= all(s[0] == 1 for s in st); agg['rooted'] &= all(s[1] for s in st)
        agg['ncarcs'] &= all(s[2] for s in st); agg['ncM'] &= all(s[3] for s in st)
        for C in cells:   # 2-point ring graph = M-edges + arcs (as point pairs) must be acyclic
            par = list(range(n))
            def f(x):
                while par[x] != x: par[x] = par[par[x]]; x = par[x]
                return x
            edges = list(chords) + [(I['head'][I['kind'][s][1]], I['tail'][I['kind'][s][2]]) for s in C if I['kind'][s][0] == 'arc']
            for p, q in edges:
                if f(p) == f(q): agg['forest'] = False
                par[f(p)] = f(q)
        v, P, _ = ply_check(I, cells, 3 if len(S) <= 4 else 2)
        agg['viol'] += v; agg['pts'] += P
        print(f'  n={n} |A|={len(A)} |S|={len(S)} mu={mu}: cells {len(cells)}, ply violations {v}/{P}', flush=True)
    print('Part A summary:', agg)


def laminar_rank(npts, chords, plus, mus):
    """max rank of a pairwise-NC set of M-laminar rings (||.||_1<=2) with d_M-image in cap ker mu (nonzero)."""
    m = len(chords); idx = {}
    for c, (p, q) in enumerate(chords):
        idx[p] = (c, 1 if p == plus[c] else -1); idx[q] = (c, 1 if q == plus[c] else -1)
    rings = [((p,), 1) for p in idx] + [((p,), 2) for p in idx] + \
            [((p, q), 1) for p, q in itertools.combinations(sorted(idx), 2) if not any(crosses((p, q), ch) for ch in chords)]
    bal = []
    for pts, k in rings:
        z = np.zeros(m)
        for p in pts: c, s = idx[p]; z[c] += s * k
        if np.any(z) and all(abs(mu @ z) < 1e-12 for mu in mus): bal.append((pts, z))
    # max-rank NC subset (greedy over all orders is enough for these tiny cases: brute force on subsets)
    best = 0; best_set = None
    two = [b for b in bal if len(b[0]) == 2]; one = [b for b in bal if len(b[0]) == 1]
    for r in range(len(two) + 1):
        for sub in itertools.combinations(two, r):
            if any(crosses(a[0], b[0]) for a, b in itertools.combinations(sub, 2)): continue
            vecs = [b[1] for b in sub] + [b[1] for b in one]
            rk = np.linalg.matrix_rank(np.array(vecs)) if vecs else 0
            if rk > best: best, best_set = rk, [b[0] for b in sub]
    K = np.array(mus); need = m - np.linalg.matrix_rank(K)
    return best, need, best_set


def partB():
    print('Part B: criterion (N*)  [max NC balanced laminar rank vs dim of joint kernel]')
    cases = []
    # O1: points 0..5, a=(1,2), e=(0,3), b=(4,5); mu = z_a - z_b
    cases.append(('O1 separating chord', 6, [(1, 2), (0, 3), (4, 5)], [1, 0, 4], [np.array([1, 0, -1])]))
    # D'-type: adjacent chords on 16 points, outer face only
    ch = [(0, 1), (3, 4), (6, 7), (9, 10), (12, 13)]
    pl = [0, 3, 6, 9, 12]
    def mu(a, b, s=(1, -1)):
        v = np.zeros(len(ch)); v[a] = s[0]; v[b] = s[1]; return v
    cases.append(('J-nest: (0,3),(1,2)', 16, ch, pl, [mu(0, 3), mu(1, 2)]))
    cases.append(('J-disj: (0,1),(2,3)', 16, ch, pl, [mu(0, 1), mu(2, 3)]))
    cases.append(('J-cross: (0,2),(1,3)', 16, ch, pl, [mu(0, 2), mu(1, 3)]))
    cases.append(('J-share: (0,1),(0,2)', 16, ch, pl, [mu(0, 1), mu(0, 2)]))
    cases.append(('J-share, opposite sign: (0,1),(2,0)', 16, ch, pl, [mu(0, 1), mu(2, 0)]))
    # shared chord repaired by a 4-chord +-1 facet: mu1 = e0 - e3, mu2 = e0 + e1 - e2 - e3 (nested arcs 0-3, 1-2)
    cases.append(('J-share repaired: mu2=e0+e1-e2-e3', 16, ch, pl, [mu(0, 3), np.array([1, 1, -1, -1, 0.])]))
    cases.append(('single pair facet (0,2)', 16, ch, pl, [mu(0, 2)]))
    cases.append(('single +-1 facet on all 5 (+,-,+,+,-)', 16, ch, pl, [np.array([1, -1, 1, 1, -1.])]))
    for name, npts, chords, plus, mus in cases:
        rk, need, S = laminar_rank(npts, chords, plus, mus)
        print(f'  {name:42s} laminar balanced rank {rk}, needed {need} -> {"OK" if rk == need else "OBSTRUCTED"}  arcs {S}')


def perfect_D(n, rng):
    A = dprime(n, rng)
    Ap = [(x, x + 1) for x in A if x + 1 < n]
    rest = [p for p in range(n) if not any(p in c for c in Ap)]
    off = rng.randrange(2)                       # completion parity in the reduced cycle
    rest = rest[off:] + rest[:off]
    comp = [tuple(sorted((rest[i], rest[i + 1]))) for i in range(0, len(rest), 2)]
    return Ap + comp, Ap


def face_sep(chords, a, b):
    def side(c, x):
        lo, hi = sorted(chords[c]); return lo < chords[x][0] < hi
    return any(side(c, a) != side(c, b) for c in range(len(chords)) if c not in (a, b))


def partC(T=4000):
    """original D (perfect, adjacent completion), n=36: two A-pairs in the same s-class face-separated?"""
    rng = random.Random(3); n = 36
    for s in (18, 12):
        sep = tot = 0
        for _ in range(T):
            chords, Apairs = perfect_D(n, rng)
            cand = [(a, b) for a, b in itertools.combinations(Apairs, 2) if (a[0] - b[0]) % s == 0]
            for a, b in cand:
                tot += 1; sep += face_sep(chords, chords.index(a), chords.index(b))
        print(f'Part C: n=36, s={s}: same-class A-pair facets with face-separated support: {sep}/{tot}')


def partD(trials=6):
    rng = random.Random(11)
    tot_cells = bad_cells = 0
    for t in range(trials):
        # points 0..npts-1, blocks = consecutive runs of length 4 or 2 (alternating signs), F1 = tree {B0B1,B0B3,B2B3},
        # M = ballot matching of each block (adjacent pairs inside a block), blocks nested randomly via NC matching skeleton
        nb = rng.randint(3, 4)
        sizes = [rng.choice([2, 4]) for _ in range(nb)]
        pts = []; cur = 0; blocks = []
        for sz in sizes:
            blocks.append(list(range(cur, cur + sz))); cur += sz
        npts = cur
        M = []; F1 = []
        for B in blocks:                   # signs + - + - ; tree {B0B1, B0B3, B2B3} (B0B3 encloses B1,B2)
            for i in range(0, len(B), 2): M.append((B[i], B[i + 1]))
            F1 += [(B[0], B[1])] + ([(B[0], B[3]), (B[2], B[3])] if len(B) == 4 else [])
        extra = [e for e in F1 if e not in M]
        S = list(range(len(M))); mu = [rng.choice([1, -1]) for _ in S]
        I = instance(npts, M, S, mu, t)
        I['chords'] = M
        cells = cells_bfs(I)
        for C in cells:
            arcs = [(I['head'][I['kind'][s][1]], I['tail'][I['kind'][s][2]]) for s in C if I['kind'][s][0] == 'arc']
            tot_cells += 1
            bad_cells += any(crosses(a, e) for a in arcs for e in extra)
        print(f'  blocks {sizes}: cells {len(cells)}', flush=True)
    print(f'Part D: cells whose arcs cross an F1 tree chord not in M: {bad_cells}/{tot_cells}')


if __name__ == '__main__':
    w = sys.argv[1] if len(sys.argv) > 1 else 'all'
    if w in ('A', 'all'): partA()
    if w in ('B', 'all'): partB()
    if w in ('C', 'all'): partC()
    if w in ('D', 'all'): partD()
