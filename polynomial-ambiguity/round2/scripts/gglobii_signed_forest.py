"""gglobii_signed_forest: signed slack-forest tiling on d_M-space (R2/gglob_ii.md, Theorem S1).

Instance.  M = random non-crossing perfect matching of 2m points 0..2m-1 on a line (chords a = 0..m-1).
Each chord a = {a+, a-} (orientation of d_M, random); d_M(x)_a = x_{a+} - x_{a-}.  Facet mu in {+-1}^m on d_M-space.
Ports: head h(a) = a^{mu_a} (endpoint with sign mu_a), tail t(a) = a^{-mu_a}.
w := D_mu z  (w_a = mu_a z_a), so mu(z) = sum(w).
Columns (w-coordinates):
   arc a->b (a != b): e_a - e_b  = image of the original ring e_{h(a)} + e_{t(b)}  (z-ring mu_a e_a - mu_b e_b),
   loop a:            e_a        = image of the one-point ring e_{h(a)}           (z-ring mu_a e_a).
   ||ring||_1 <= 2 in z-coordinates.  Network (digraph + root) matrix => TU.
Cost: arc a->b: sqrt|pos h(a) - pos t(b)| + generic noise; loop: tiny generic.
Modes:  'all'    : every ordered pair a != b;
        'sub'    : as 'region', but M has extra chords outside supp mu (face graph G_M(S) must be connected);
        'region' : only pairs a, b bounding a common face of the chord diagram M (dual-tree adjacency);
                   then arc chords are inside that face, hence non-crossing with M as well.
Checks (exhaustive):
  (1) all c-dual-feasible bases (cells), found by exact dual-simplex wall-crossing BFS from one optimal basis
      (complete because the cells form a triangulation of the convex cone {sum w >= 0}); for m <= 5 cross-checked
      against brute-force enumeration of all m-subsets of columns.
  (2) every cell: |det| = 1, rooted forest (one loop per component), arcs pairwise non-crossing as chords
      h(a)-t(b); in 'region' mode also non-crossing with every M-chord.
  (3) half-open rule with generic eta, sum(eta) < 0: every lattice w in [-B,B]^m lies in exactly one cell iff
      sum(w) >= 1, and in none otherwise.  (z = D_mu w is a bijection of the box.)  All box points if
      (2B+1)^m <= 70000, else 5000 uniform random box points.
Extra (4) 'mass2' demo: adding the mu-unbalanced rings e_a + e_b (mass 2; made cheap, loops made expensive)
      produces dual-feasible bases with |det| = 2 (odd cycle) and box lattice points with half-integral
      coordinates in their cell => c + N V != (c + cone V) ∩ Z^m.
Usage: .venv/bin/python gglobii_signed_forest.py [m=6] [B=2] [trials=3] [mode=region|all|both] [mass2=0|1]
"""
import sys, itertools, random
import numpy as np


def random_nc_matching(m, rng):
    # random balanced parenthesis word -> NC matching on 0..2m-1
    while True:
        s = [1] * m + [-1] * m
        rng.shuffle(s)
        h, ok = 0, True
        for v in s:
            h += v
            if h < 0: ok = False; break
        if ok: break
    st, ch = [], []
    for i, v in enumerate(s):
        if v == 1: st.append(i)
        else: ch.append((st.pop(), i))
    return ch


def interleave(p, q):
    (i, j), (k, l) = sorted(p), sorted(q)
    if len({i, j, k, l}) < 4: return False
    return (i < k < j < l) or (k < i < l < j)


def build(m, seed, mode, mass2=False):
    """mode 'sub': M has m + extra chords, mu is supported on S = the first m chords only (the others are
    M-chords outside supp mu, still required to be uncrossed); instances with disconnected face graph G_M(S)
    are redrawn (counted in I['rejected'])."""
    rng = random.Random(seed)
    rejected = 0
    while True:
        mt = m + (rng.randint(1, m) if mode == 'sub' else 0)
        chords = random_nc_matching(mt, rng)
        rng.shuffle(chords)

        def side(c, a):  # is chord a inside chord c
            lo, hi = sorted(chords[c]); return lo < chords[a][0] < hi
        def same_face(a, b):
            return all(side(c, a) == side(c, b) for c in range(mt) if c not in (a, b))
        adj = {(a, b) for a in range(m) for b in range(m) if a != b and same_face(a, b)}
        seen, st = {0}, [0]
        while st:
            a = st.pop()
            for b in range(m):
                if (a, b) in adj and b not in seen: seen.add(b); st.append(b)
        if mode != 'sub' or len(seen) == m: break
        rejected += 1
    mu = [rng.choice([1, -1]) for _ in range(m)]
    orient = [rng.random() < 0.5 for _ in range(m)]          # True: first endpoint is a+
    plus = [c[0] if o else c[1] for c, o in zip(chords, orient)]
    minus = [c[1] if o else c[0] for c, o in zip(chords, orient)]
    head = [plus[a] if mu[a] == 1 else minus[a] for a in range(m)]
    tail = [minus[a] if mu[a] == 1 else plus[a] for a in range(m)]
    pos = [i + 0.3 * rng.random() for i in range(2 * mt)]
    cols, cost, kind = [], [], []
    for a in range(m):
        for b in range(m):
            if a == b: continue
            if mode in ('region', 'sub') and (a, b) not in adj: continue
            v = np.zeros(m); v[a] = 1; v[b] = -1
            cols.append(v); cost.append(abs(pos[head[a]] - pos[tail[b]]) ** 0.5 + 1e-7 * rng.random())
            kind.append(('arc', a, b))
    for a in range(m):
        v = np.zeros(m); v[a] = 1
        cols.append(v); cost.append((1.0 if mass2 else 1e-4) * rng.random() + (1.0 if mass2 else 0.0))
        kind.append(('loop', a))
    if mass2:   # mass-2 rings made cheap so that the LP actually uses them
        for a, b in itertools.combinations(range(m), 2):
            v = np.zeros(m); v[a] = 1; v[b] = 1
            cols.append(v); cost.append(1e-3 * rng.random())
            kind.append(('mass2', a, b))
    A = np.array(cols).T
    return dict(m=m, rejected=rejected, chords=chords, mu=mu, head=head, tail=tail, A=A, c=np.array(cost), kind=kind, rng=rng)


def optimal_basis(I, w):
    from scipy.optimize import linprog
    A, c = I['A'], I['c']
    r = linprog(c, A_eq=A, b_eq=w, bounds=(0, None), method='highs')
    assert r.status == 0
    S = tuple(sorted(np.nonzero(r.x > 1e-9)[0]))
    assert len(S) == I['m'], S
    return S


def dual_feasible(I, S):
    A, c = I['A'], I['c']
    AB = A[:, S]
    if abs(np.linalg.det(AB)) < 0.5: return False
    y = np.linalg.solve(AB.T, c[list(S)])
    return (c - A.T @ y).min() >= -1e-12


def cells_bfs(I):
    A, c, m = I['A'], I['c'], I['m']
    rng = I['rng']
    w0 = np.array([1.0 + rng.random() for _ in range(m)])
    S0 = optimal_basis(I, w0)
    assert dual_feasible(I, S0)
    seen = {S0}; todo = [S0]
    while todo:
        S = todo.pop()
        Binv = np.linalg.inv(A[:, S])
        y = Binv.T @ c[list(S)]
        red = c - A.T @ y
        for i in range(m):
            alpha = Binv[i] @ A
            cand = [(red[j] / -alpha[j], j) for j in range(A.shape[1]) if j not in S and alpha[j] < -1e-9]
            if not cand: continue          # boundary wall of the feasible cone
            _, j = min(cand)
            T = tuple(sorted([s for k, s in enumerate(S) if k != i] + [j]))
            if T not in seen:
                assert dual_feasible(I, T)
                seen.add(T); todo.append(T)
    return sorted(seen)


def cells_brute(I):
    return sorted(S for S in itertools.combinations(range(I['A'].shape[1]), I['m']) if dual_feasible(I, S))


def check_cell(I, S):
    A, kind, m = I['A'], I['kind'], I['m']
    det = round(abs(np.linalg.det(A[:, S])))
    arcs = [kind[s] for s in S if kind[s][0] == 'arc']
    loops = [kind[s][1] for s in S if kind[s][0] == 'loop']
    # forest with one loop per component
    par = list(range(m))
    def f(x):
        while par[x] != x: par[x] = par[par[x]]; x = par[x]
        return x
    forest = True
    for _, a, b in arcs:
        ra, rb = f(a), f(b)
        if ra == rb: forest = False
        par[ra] = rb
    comps = {f(a) for a in range(m)}
    rooted = forest and sorted(f(a) for a in loops) == sorted(comps) and len(loops) == len(comps)
    ch = [(I['head'][a], I['tail'][b]) for _, a, b in arcs]
    nc_arcs = not any(interleave(p, q) for p, q in itertools.combinations(ch, 2))
    nc_M = not any(interleave(p, q) for p in ch for q in I['chords'])
    return det, rooted, nc_arcs, nc_M


def ply_check(I, cells, B):
    A, m, rng = I['A'], I['m'], I['rng']
    eta = np.array([rng.random() for _ in range(m)]); eta -= eta.mean() + 0.37   # generic, sum < 0
    if (2 * B + 1) ** m <= 70000:
        X = np.array(list(itertools.product(range(-B, B + 1), repeat=m)), dtype=float).T
    else:   # m >= 9: uniform random sample of 5000 lattice points of the box, plus the sum-0/1/-1 layers bias
        X = np.array([[rng.randint(-B, B) for _ in range(m)] for _ in range(5000)], dtype=float).T
    cnt = np.zeros(X.shape[1], dtype=int)
    for S in cells:
        Binv = np.linalg.inv(A[:, S])
        Q = Binv @ X; qe = Binv @ eta
        ok = (Q > 1e-9) | ((np.abs(Q) <= 1e-9) & (qe[:, None] > 0))
        cnt += ok.all(axis=0)
    want = (X.sum(axis=0) >= 1 - 1e-9).astype(int)
    return int((cnt != want).sum()), X.shape[1], int(want.sum())


def run(m, B, seed, mode, mass2=False, brute=False):
    I = build(m, seed, mode, mass2)
    cells = cells_bfs(I)
    out = dict(m=m, seed=seed, mode=mode, extra_chords=len(I['chords']) - m, rejected=I['rejected'], mu=I['mu'], ncols=I['A'].shape[1], cells=len(cells))
    if brute:
        out['brute_equal'] = (cells == cells_brute(I))
    stats = [check_cell(I, S) for S in cells]
    out['dets'] = sorted({d for d, *_ in stats})
    if not mass2:
        out['rooted_forests'] = all(s[1] for s in stats)
        out['NC_arcs'] = all(s[2] for s in stats)
        out['NC_with_M'] = sum(s[3] for s in stats), len(stats)
        out['ply_viol'], out['points'], out['region_pts'] = ply_check(I, cells, B)
    else:
        out['det2_cells'] = sum(1 for d, *_ in stats if d == 2)
        out['cells_using_mass2'] = sum(1 for S in cells if any(I['kind'][s][0] == 'mass2' for s in S))
        # lattice points of the box whose (unique, half-open) cell gives them NON-integral coordinates:
        # these are in (c + cone V) but in no c + N V  ->  exactness fails.
        A = I['A']; rng = I['rng']
        X = np.array(list(itertools.product(range(-B, B + 1), repeat=m)), dtype=float).T
        eta = np.array([rng.random() for _ in range(m)]); eta -= eta.mean() + 0.37
        frac = 0; ex = None
        for S in cells:
            Binv = np.linalg.inv(A[:, S]); Q = Binv @ X; qe = Binv @ eta
            inside = ((Q > 1e-9) | ((np.abs(Q) <= 1e-9) & (qe[:, None] > 0))).all(axis=0)
            nonint = (np.abs(Q - np.round(Q)) > 1e-9).any(axis=0)
            hit = inside & nonint
            frac += int(hit.sum())
            if hit.any() and ex is None:
                k = int(np.nonzero(hit)[0][0]); ex = (X[:, k].astype(int).tolist(), [I['kind'][s] for s in S], Q[:, k].round(3).tolist())
        out['lattice_pts_nonintegral'] = frac; out['example'] = ex
    return out


if __name__ == '__main__':
    m = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    B = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    T = int(sys.argv[3]) if len(sys.argv) > 3 else 3
    mode = sys.argv[4] if len(sys.argv) > 4 else 'both'
    mass2 = len(sys.argv) > 5 and sys.argv[5] == '1'
    modes = ['region', 'all', 'sub'] if mode == 'both' else [mode]
    for s in range(T):
        for md in modes:
            print(run(m, B, s, md, mass2, brute=(m <= 5)), flush=True)
