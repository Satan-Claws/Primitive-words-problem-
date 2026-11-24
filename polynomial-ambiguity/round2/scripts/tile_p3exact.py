"""tile_p3exact: EXACT min-ply tiling of the omega-simplex by tree validity cones, P = 3 (2-dim simplex).
Instance: cyclic sequence of support points (residue r_i in Z_3, mu_i in Z\0) with every fibre sum 0, generic.
Rooted at point 0, every subtree of an NC tree is a linear interval I of points 1..m-1 (S3A); edge (parent,c)
with subtree I is valid at omega iff sgn<fold(mu|I),omega> = sgn mu_c. K_T = {omega>0 : all edges valid}.
Exact: chambers of the line arrangement {f_I = 0} in the open triangle are enumerated with rational arithmetic
(perturbation around every vertex, checked against the Euler count); K_T = set of chambers; ply on walls equals
ply of a chamber under the S2P(b) half-open rule, so min max-ply over subfamilies = ILP on chambers (CP-SAT).
Usage: .venv/bin/python tile_p3exact.py [trials=10] [m=9]"""
import sys, itertools, math, random
from fractions import Fraction as Fr
from functools import lru_cache
from ortools.sat.python import cp_model

def gen_instance(m, rng):
    while True:
        res = [rng.randrange(3) for _ in range(m)]
        if m == 9 and rng.random() < 0.5: res = [i % 3 for i in range(m)]
        if min(res.count(r) for r in range(3)) < 2: continue
        mu = [0] * m
        for r in range(3):
            idx = [i for i in range(m) if res[i] == r]
            vals = [rng.choice([-1, 1]) * rng.randint(1, 9) for _ in idx[:-1]]
            last = -sum(vals)
            if last == 0: break
            for i, v in zip(idx, vals + [last]): mu[i] = v
        else:
            # genericity: every linear interval of 1..m-1 and every fibre-subset of an interval: mu-sum != 0
            ok = True
            for l in range(1, m):
                for rr in range(l, m):
                    if sum(mu[l:rr + 1]) == 0: ok = False
            if ok: return res, mu

def fold(res, mu, l, r):
    f = [0, 0, 0]
    for i in range(l, r + 1): f[res[i]] += mu[i]
    return tuple(f)

def all_trees(res, mu):
    """all bichromatic NC trees rooted at 0, as frozensets of (interval, sign) constraints."""
    m = len(mu); sg = [1 if x > 0 else -1 for x in mu]
    @lru_cache(None)
    def sub(l, r):  # trees on [l..r] whose top c has subtree [l..r]; returns list of constraint frozensets
        out = []
        for c in range(l, r + 1):
            s = sg[c]
            for A in part(l, c - 1, -s):
                for B in part(c + 1, r, -s):
                    out.append(frozenset({((l, r), s)}) | A | B)
        return out
    @lru_cache(None)
    def part(l, r, t):
        if l > r: return [frozenset()]
        out = []
        for k in range(l, r + 1):
            for A in sub(l, k):
                if ((l, k), t) not in A: continue
                for B in part(k + 1, r, t): out.append(A | B)
        return out
    return list(set(part(1, m - 1, -sg[0])))

def chambers(forms):
    """forms: list of integer 3-vectors (distinct up to scaling). Chambers of the open triangle.
    coords (a,b): omega = (a, b, 1-a-b). line: (f0-f2) a + (f1-f2) b + f2 = 0."""
    lines = []
    seen = set()
    for f in forms:
        L = (f[0] - f[2], f[1] - f[2], f[2])
        g = math.gcd(math.gcd(abs(L[0]), abs(L[1])), abs(L[2])) or 1
        L = tuple(x // g for x in L)
        if L[0] < 0 or (L[0] == 0 and (L[1] < 0 or (L[1] == 0 and L[2] < 0))): L = tuple(-x for x in L)
        if (L[0], L[1]) == (0, 0): continue
        seen.add(L)
    lines = sorted(seen)
    bnd = [(1, 0, 0), (0, 1, 0), (-1, -1, 1)]  # a=0, b=0, 1-a-b=0
    allL = lines + bnd
    def inside_closed(p): return p[0] >= 0 and p[1] >= 0 and p[0] + p[1] <= 1
    def inside_open(p): return p[0] > 0 and p[1] > 0 and p[0] + p[1] < 1
    verts = {}
    for i, j in itertools.combinations(range(len(allL)), 2):
        a1, b1, c1 = allL[i]; a2, b2, c2 = allL[j]
        det = a1 * b2 - a2 * b1
        if det == 0: continue
        p = (Fr(-c1 * b2 + c2 * b1, det), Fr(-a1 * c2 + a2 * c1, det))
        if inside_closed(p): verts.setdefault(p, set()).update([i, j])
    # meets-interior lines
    def ev(L, p): return L[0] * p[0] + L[1] * p[1] + L[2]
    eps = Fr(1, 10**12)
    sigs = set()
    ndir = 0
    for p, Ls in verts.items():
        angs = []
        for i in Ls:
            a, b, _ = allL[i]
            th = math.atan2(-a, b) % math.pi  # direction of the line
            angs += [th, th + math.pi]
        angs = sorted(set(round(x, 12) for x in angs))
        for k in range(len(angs)):
            t0, t1 = angs[k], angs[(k + 1) % len(angs)] + (2 * math.pi if k + 1 == len(angs) else 0)
            th = (t0 + t1) / 2
            d = (Fr(round(math.cos(th) * 10**6), 10**6), Fr(round(math.sin(th) * 10**6), 10**6))
            q = (p[0] + eps * d[0], p[1] + eps * d[1])
            if not inside_open(q): continue
            s = tuple(ev(L, q) for L in lines)
            if any(x == 0 for x in s): continue
            sigs.add(tuple(1 if x > 0 else -1 for x in s)); ndir += 1
    # Euler check: regions = 1 + #lines meeting interior + sum over interior vertices (k_v - 1)
    nl = 0
    for L in lines:
        # line meets open triangle iff values at the 3 corners are not all >=0 or all <=0 (strictly mixed)
        vals = [ev(L, c) for c in [(0, 0), (1, 0), (0, 1)]]
        if max(vals) > 0 and min(vals) < 0: nl += 1
    extra = 0
    for p, Ls in verts.items():
        if inside_open(p): extra += len([i for i in Ls if i < len(lines)]) - 1
    expect = 1 + nl + extra
    assert len(sigs) == expect, (len(sigs), expect)
    return lines, sorted(sigs)

def solve_instance(res, mu, verbose=False):
    trees = all_trees(res, mu)
    m = len(mu)
    ivs = sorted({iv for T in trees for (iv, s) in T})
    forms = {iv: fold(res, mu, *iv) for iv in ivs}
    lines, ch = chambers(list(forms.values()))
    def lnorm(f):
        L = (f[0] - f[2], f[1] - f[2], f[2]); g = math.gcd(math.gcd(abs(L[0]), abs(L[1])), abs(L[2])) or 1
        L = tuple(x // g for x in L); fl = 1
        if L[0] < 0 or (L[0] == 0 and (L[1] < 0 or (L[1] == 0 and L[2] < 0))): L = tuple(-x for x in L); fl = -1
        return L, fl
    lidx = {L: i for i, L in enumerate(lines)}
    def sign_at(iv, c):
        f = forms[iv]
        if (f[0] - f[2], f[1] - f[2]) == (0, 0): return 1 if f[2] > 0 else -1
        L, fl = lnorm(f); return fl * ch[c][lidx[L]]
    masks = {}
    for T in trees:
        S = frozenset(c for c in range(len(ch)) if all(sign_at(iv, c) == s for (iv, s) in T))
        if S: masks[S] = T
    cones = list(masks)
    # every chamber covered?
    cov = set().union(*cones)
    assert len(cov) == len(ch), "uncovered chamber"
    # drop cones contained in others? not valid for min-ply in general; keep all.
    best = None
    for z in range(1, 6):
        mdl = cp_model.CpModel(); x = [mdl.NewBoolVar('') for _ in cones]
        for c in range(len(ch)):
            inc = [x[i] for i, S in enumerate(cones) if c in S]
            mdl.Add(sum(inc) >= 1); mdl.Add(sum(inc) <= z)
        sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = 120; sv.parameters.num_workers = 8
        st = sv.Solve(mdl)
        if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            best = (z, sum(sv.Value(v) for v in x)); break
        if st != cp_model.INFEASIBLE: best = ('timeout', z); break
    return dict(trees=len(trees), cones=len(cones), lines=len(lines), chambers=len(ch), minply=best)

if __name__ == '__main__':
    trials = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    m = int(sys.argv[2]) if len(sys.argv) > 2 else 9
    rng = random.Random(12345 + m)
    for t in range(trials):
        res, mu = gen_instance(m, rng)
        out = solve_instance(res, mu)
        print(t, 'res', ''.join(map(str, res)), 'mu', mu, out, flush=True)
