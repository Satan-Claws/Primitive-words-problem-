"""tile2_fan_check: exact cross-check of Theorem A (R2/tile2.md) on the abstract P = 3 instances of tile_p3exact.

For each instance: enumerate ALL bichromatic NC trees WITH their edges (S3A interval recursion), compute every
cone K_T as an exact set of chambers (tile_p3exact.chambers, rational arithmetic + Euler check), select
F_c = {T : T is dual-feasible for the concave cost c} and check that every chamber lies in EXACTLY ONE K_T, T in F_c.
(The chamber/cone part is exact; dual feasibility uses floats with generic c, margins are printed.)
Usage: .venv/bin/python tile2_fan_check.py [trials=20] [m=9] [P=3]   (P=3 only exact)
"""
import sys, math, random
from functools import lru_cache
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from tile_p3exact import gen_instance, fold, chambers
from tile2_core import make_cost, dual_margin, is_nc, is_spanning_tree


def all_trees_edges(mu):
    m = len(mu); sg = [1 if x > 0 else -1 for x in mu]

    @lru_cache(None)
    def sub(l, r):  # -> list of (edges, constraints) for trees spanning [l..r] (top inside), plus top
        out = []
        for c in range(l, r + 1):
            s = sg[c]
            for EA, CA, TA in part(l, c - 1, -s):
                for EB, CB, TB in part(c + 1, r, -s):
                    E = EA | EB | frozenset((c, t) for t in TA + TB)
                    out.append((E, CA | CB | frozenset({((l, r), s)}), c))
        return out

    @lru_cache(None)
    def part(l, r, t):
        if l > r: return [(frozenset(), frozenset(), ())]
        out = []
        for k in range(l, r + 1):
            for E1, C1, c1 in sub(l, k):
                if sg[c1] != t: continue
                for E2, C2, T2 in part(k + 1, r, t):
                    out.append((E1 | E2, C1 | C2, (c1,) + T2))
        return out

    res = []
    for E, C, T in part(1, m - 1, -sg[0]):
        E = E | frozenset((0, t) for t in T)
        res.append((frozenset(tuple(sorted(e)) for e in E), C))
    return res


def run(res, mu, seed=0):
    trees = all_trees_edges(mu)
    m = len(mu)
    for E, C in trees[:50]:
        assert is_spanning_tree(list(E), m) and is_nc(E)
    ivs = sorted({iv for _, C in trees for (iv, s) in C})
    forms = {iv: fold(res, mu, *iv) for iv in ivs}
    lines, ch = chambers(list(forms.values()))

    def lnorm(f):
        L = (f[0] - f[2], f[1] - f[2], f[2]); g = math.gcd(math.gcd(abs(L[0]), abs(L[1])), abs(L[2])) or 1
        L = tuple(x // g for x in L); fl = 1
        if L[0] < 0 or (L[0] == 0 and (L[1] < 0 or (L[1] == 0 and L[2] < 0))): L = tuple(-x for x in L); fl = -1
        return L, fl
    lidx = {L: i for i, L in enumerate(lines)}

    def sign_at(iv, cix):
        f = forms[iv]
        if (f[0] - f[2], f[1] - f[2]) == (0, 0): return 1 if f[2] > 0 else -1
        L, fl = lnorm(f); return fl * ch[cix][lidx[L]]
    c = make_cost(m, seed)
    signed_mu = mu
    Fc = []
    margins = []
    for E, C in trees:
        # orient edges (pos, neg)
        Eo = [(i, j) if mu[i] > 0 else (j, i) for i, j in E]
        dm = dual_margin(Eo, c, signed_mu)
        if dm >= -1e-9:
            Fc.append(C); margins.append(dm)
    ply = [0] * len(ch)
    for C in Fc:
        for cix in range(len(ch)):
            if all(sign_at(iv, cix) == s for (iv, s) in C): ply[cix] += 1
    return dict(trees=len(trees), chambers=len(ch), Fc=len(Fc),
                Fc_nonempty=None, ply_min=min(ply), ply_max=max(ply),
                min_offtree_margin=min(margins) if margins else None)


if __name__ == '__main__':
    trials = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    m = int(sys.argv[2]) if len(sys.argv) > 2 else 9
    rng = random.Random(12345 + m)  # same instances as tile_p3exact
    ok = 0
    for t in range(trials):
        res, mu = gen_instance(m, rng)
        for seed in (0, 1):
            out = run(res, mu, seed)
            good = out['ply_min'] == 1 and out['ply_max'] == 1
            ok += good
            print(t, 'seed', seed, 'res', ''.join(map(str, res)), 'mu', mu, out, 'EXACT-PARTITION' if good else 'FAIL', flush=True)
    print('exact partitions:', ok, '/', 2 * trials)
