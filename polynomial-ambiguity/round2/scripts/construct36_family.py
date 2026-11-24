"""construct36_family.py -- the explicit Lemma-36 family for E ∩ W_36 and its ply.

F36 = (a) fibre rectangles: for each fibre r (class mod 6) and i in Z_6, the n=6 rectangle R_i = chords
        {i, i+5}, {i+3, i+2} (fibre indices; A=3, B=2) lifted to positions r+6t   (36 atoms, each certifies {2,3})
    + (b) cross pairs: a 3-chord {j, j+12} in fibre r' and the unique diameter {i, i+18} of a fibre r != r'
        that does not cross it                                                    (36*5 = 180 two-atom systems)
Every member is a k<=2 chord-dominance system of construct.md §1 (ply 1 each).  Checks:
  1. membership/validity of each system with construct_atoms predicates;
  2. coverage + ply (= number of members holding) on all D_36 classes |x|_1 <= N (from construct36_cover.py);
  3. random large-norm tests: general W_36 ∩ N^36 (fibrewise random polygon sums) and the A2 product region
     x = B + e_2 + e_3 (B fibre-constant, large), including disjoint-witness-fibre configurations;
  4. greedy / ILP D_36-invariant subfamily of F36 minimising max ply on the test set.
usage: python construct36_family.py N  (needs scratchpad W36_N{N}.npy)"""
import sys, itertools, random, numpy as np
import construct_atoms as CA, construct36_core as C
n = 36; SP = '/private/tmp/claude-501/-Users-shoru-Desktop-Test4/0ed9f581-4f02-4fb6-a7db-5e10049bb620/scratchpad/'
def pos(r, t): return r + 6 * (t % 6)
def atom(chords):
    """chord list -> (pts sorted, shape) in construct_atoms format."""
    pts = sorted(v for c in chords for v in c); ix = {v: k for k, v in enumerate(pts)}
    sh = tuple(sorted(tuple(sorted((ix[a], ix[b]))) for a, b in chords))
    return tuple(pts), sh
FAM = []  # each member: tuple of atoms
for r in range(6):
    for i in range(6):
        FAM.append(('rect', r, i, (atom([(pos(r, i), pos(r, i + 5)), (pos(r, i + 3), pos(r, i + 2))]),)))
for rp in range(6):
    for t in range(6):
        j, k = pos(rp, t), pos(rp, t + 2)
        for r in range(6):
            if r == rp: continue
            ok = [tt for tt in range(3) if not CA.crosses((pos(r, tt), pos(r, tt + 3)), (j, k))]
            assert len(ok) == 1
            tt = ok[0]
            FAM.append(('pair', (r, tt), (rp, t), (atom([(pos(r, tt), pos(r, tt + 3))]), atom([(j, k)]))))
def _key(m): return frozenset(frozenset(frozenset((m3[0][a], m3[0][b])) for a, b in m3[1]) for m3 in m[3])
_seen = {}
for m in FAM: _seen.setdefault(_key(m), m)
NRAW = len(FAM); FAM = list(_seen.values())   # R_i and R_{i+3} coincide in Z_6 -> 18 distinct rectangles
S = C.S
def check_member(m):
    ats = m[3]; Cs = []
    for pts, sh in ats:
        assert len(CA.allowed_dominants(sh)[0]) == 2 * len(sh)
        Cs.append(S.certified(pts, sh))
    assert frozenset().union(*Cs) >= {2, 3}, m
    if len(ats) == 2:
        (p1, s1), (p2, s2) = ats
        assert not set(p1) & set(p2)
        assert not any(CA.crosses(a, b) for a in CA.atom_pairs(p1, s1) for b in CA.atom_pairs(p2, s2))
for m in FAM: check_member(m)
def holds(m, x): return all(CA.atom_holds(x, pts, sh) for pts, sh in m[3])
def ply_vec(x): return np.array([holds(m, x) for m in FAM], bool)

def rand_general(rng, M):
    x = np.zeros(n, int)
    for r in range(6):
        y = np.zeros(6, int)
        for t in range(3): y[[t, t + 3]] += rng.randint(0, M)          # diameters (2-gons)
        for t in range(2): y[[t, t + 2, t + 4]] += rng.randint(0, M)   # triangles (3-gons)
        x[r::6] = y
    return x
def rand_product(rng, Bmax, amp, disjoint):
    """x_{r+6t} = B_r + alpha_r (-1)^t + beta_{r, t mod 3}; fibres R2 carry alpha, R3 carry beta."""
    while True:
        B = [rng.randint(2 * amp + 1, Bmax) for _ in range(6)]
        fib = list(range(6)); rng.shuffle(fib)
        if disjoint:
            k = rng.randint(1, 5); R2, R3 = fib[:k], fib[k:k + rng.randint(1, 6 - k)]
        else:
            R2 = rng.sample(range(6), rng.randint(1, 6)); R3 = rng.sample(range(6), rng.randint(1, 6))
        x = np.zeros(n, int)
        for r in range(6):
            al = rng.randint(-amp, amp) if r in R2 else 0
            be = [rng.randint(-amp, amp) for _ in range(3)] if r in R3 else [0, 0, 0]
            be = [b - sum(be) // 3 for b in be]; be[0] -= sum(be)                  # mean zero
            for t in range(6): x[pos(r, t)] = B[r] + al * (-1) ** t + be[t % 3]
        if x.min() >= 0 and C.prim(x): return x

if __name__ == '__main__':
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 12
    print('raw members', NRAW, '-> distinct', len(FAM))
    print('family F36:', sum(m[0] == 'rect' for m in FAM), 'rectangles +', sum(m[0] == 'pair' for m in FAM), 'cross pairs; all valid')
    X = [np.array(x) for x in np.load(SP + f'W36_N{N}.npy')]
    rng = random.Random(36)
    tests = {f'exhaustive |x|<= {N}': X,
             'random general (polygon mult 0..9)': [rand_general(rng, 10) for _ in range(3000)],
             'product B<=60, |pert|<=3, disjoint fibres': [rand_product(rng, 60, 3, True) for _ in range(3000)],
             'product B<=60, |pert|<=3, arbitrary fibres': [rand_product(rng, 60, 3, False) for _ in range(3000)],
             'product B<=1000, |pert|<=40, disjoint': [rand_product(rng, 1000, 40, True) for _ in range(2000)]}
    allH = {}
    for name, xs in tests.items():
        xs = [x for x in xs if C.prim(x)]
        H = np.array([ply_vec(list(int(v) for v in x)) for x in xs]); allH[name] = H
        pl = H.sum(1)
        print(f'{name}: {len(xs)} pts, uncovered {int((pl == 0).sum())}, F36 ply min/mean/max {pl.min()}/{pl.mean():.1f}/{pl.max()}', flush=True)
    # ---- 4. D_36-invariant subfamily minimising max ply (ILP over orbits) ----
    G = [(r, s) for r in range(n) for s in (1, -1)]
    def key(m): return frozenset(frozenset(frozenset((m3[0][a], m3[0][b])) for a, b in m3[1]) for m3 in m[3])
    def img(g, m):
        r0, s = g
        return frozenset(frozenset(frozenset(((s * m3[0][a] + r0) % n, (s * m3[0][b] + r0) % n)) for a, b in m3[1]) for m3 in m[3])
    K = [key(m) for m in FAM]; kidx = {k: i for i, k in enumerate(K)}
    orb = [-1] * len(FAM); O = 0
    for i in range(len(FAM)):
        if orb[i] >= 0: continue
        for g in G:
            j = kidx[img(g, FAM[i])]; orb[j] = O
        O += 1
    orb = np.array(orb); print('D_36 orbits of F36 members:', O, [int((orb == o).sum()) for o in range(O)])
    from ortools.sat.python import cp_model
    Hall = np.concatenate(list(allH.values()))
    Ho = np.stack([Hall[:, orb == o].sum(1) for o in range(O)], 1)    # holding count per orbit
    md = cp_model.CpModel(); y = [md.NewBoolVar(f'y{o}') for o in range(O)]; z = md.NewIntVar(0, 1000, 'z')
    rows = {tuple(r) for r in Ho}
    for row in rows:
        md.Add(sum(int(c) * y[o] for o, c in enumerate(row) if c) >= 1)
        md.Add(sum(int(c) * y[o] for o, c in enumerate(row) if c) <= z)
    md.Minimize(z); sol = cp_model.CpSolver(); sol.parameters.max_time_in_seconds = 60
    st = sol.Solve(md); ch = [o for o in range(O) if sol.Value(y[o])]
    print('ILP status', sol.StatusName(st), ' chosen orbits', ch, ' sizes', [int((orb == o).sum()) for o in ch],
          ' min max-ply on test set', sol.Value(z))
    mask = np.isin(orb, ch)
    # member-level (not symmetric) minimum subfamily of F36 covering the test set
    md2 = cp_model.CpModel(); u = [md2.NewBoolVar(f'u{i}') for i in range(len(FAM))]
    for row in {tuple(np.nonzero(r)[0]) for r in Hall}: md2.AddBoolOr([u[i] for i in row])
    md2.Minimize(sum(u)); s2 = cp_model.CpSolver(); s2.parameters.max_time_in_seconds = 120; st2 = s2.Solve(md2)
    sel = np.array([bool(s2.Value(v)) for v in u])
    print('min-size covering subfamily of F36:', s2.StatusName(st2), int(sel.sum()), 'members (',
          int(sum(sel[i] for i in range(len(FAM)) if FAM[i][0] == 'rect')), 'rect ), max ply on tests', int(Hall[:, sel].sum(1).max()))
    for name, H in allH.items():
        pl = H[:, mask].sum(1); print(f'  subfamily on {name}: uncovered {int((pl == 0).sum())}, ply max {pl.max()} mean {pl.mean():.1f}')

# ---- 5. the reduced provable family F36* (Lemma 36 (c)): 2 rectangles per fibre + 2 cross pairs per ordered fibre pair ----
def fstar():
    out = []
    for m in FAM:
        if m[0] == 'rect' and m[2] in (0, 1): out.append(m)
        if m[0] == 'pair' and m[2][1] in (0, 1): out.append(m)
    return out
if __name__ == '__main__':
    FS = fstar(); idx = [FAM.index(m) for m in FS]
    print('F36*:', sum(m[0] == 'rect' for m in FS), 'rectangles +', sum(m[0] == 'pair' for m in FS), 'pairs')
    for name, H in allH.items():
        pl = H[:, idx].sum(1); print(f'  F36* on {name}: uncovered {int((pl == 0).sum())}, ply min/mean/max {pl.min()}/{pl.mean():.1f}/{pl.max()}')
    rng2 = random.Random(2026); fresh = []
    for _ in range(4000):
        x = rand_product(rng2, 200, 5, True)
        # force minimal witness sets: keep one 2-fibre and one 3-fibre with a zero difference class
        fresh.append(x)
    # structured: B + alpha on fibre r, beta pattern with one zero difference on fibre r'
    for r in range(6):
        for rp in range(6):
            if r == rp: continue
            for beta in ([1, 1, -2], [1, -2, 1], [-2, 1, 1], [2, -1, -1], [-1, 2, -1], [-1, -1, 2], [1, 0, -1], [0, 1, -1]):
                for al in (1, -1, 3):
                    x = np.full(n, 10)
                    for t in range(6): x[pos(r, t)] += al * (-1) ** t; x[pos(rp, t)] += beta[t % 3]
                    fresh.append(x)
    Hf = np.array([ply_vec(list(int(v) for v in x)) for x in fresh])
    print(f'fresh/structured test ({len(fresh)} pts): F36 uncovered {int((Hf.sum(1) == 0).sum())}, F36* uncovered {int((Hf[:, idx].sum(1) == 0).sum())}, '
          f'ILP-48 (test-tuned) uncovered {int((Hf[:, sel].sum(1) == 0).sum())}, F36* ply max {Hf[:, idx].sum(1).max()}')
