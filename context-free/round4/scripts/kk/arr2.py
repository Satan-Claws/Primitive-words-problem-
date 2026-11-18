"""
Subspace-arrangement test for the sign-fixing obstruction criterion.

Given n, a set Dset of maximal proper divisors d, and a generator of "structures"
(each structure = list of blocks; we use pairs (rigid ratio-1 pairs) and singletons),
compute the set
   H = { delta : for every structure P, exists d in Dset with delta in span(P)+V_d } minus union_{d in Dset} V_d
as a union of subspaces.  If H becomes empty, no delta satisfies the criterion
for the structures tried (so the criterion cannot prove non-CF).

Field: mod prime (fast search) or exact rationals (verification).
"""
import sys, random
from fractions import Fraction

class Field:
    def __init__(self, p=None):
        self.p = p
    def norm(self, x):
        return x % self.p if self.p else x
    def inv(self, x):
        return pow(x, self.p - 2, self.p) if self.p else Fraction(1) / x
    def zero(self, x):
        return (x % self.p == 0) if self.p else (x == 0)
    def conv(self, x):
        return x % self.p if self.p else Fraction(x)

def rref(F, rows, ncols):
    rows = [[F.conv(v) for v in r] for r in rows]
    piv = []; r = 0
    for c in range(ncols):
        pr = None
        for i in range(r, len(rows)):
            if not F.zero(rows[i][c]): pr = i; break
        if pr is None: continue
        rows[r], rows[pr] = rows[pr], rows[r]
        iv = F.inv(rows[r][c])
        rows[r] = [F.norm(x * iv) for x in rows[r]]
        for i in range(len(rows)):
            if i != r and not F.zero(rows[i][c]):
                f = rows[i][c]
                rows[i] = [F.norm(a - f * b) for a, b in zip(rows[i], rows[r])]
        piv.append(c); r += 1
        if r == len(rows): break
    return rows[:r], piv

def nullspace(F, rows, ncols):
    if not rows:
        return [[F.conv(int(i == j)) for j in range(ncols)] for i in range(ncols)]
    R, piv = rref(F, rows, ncols)
    free = [c for c in range(ncols) if c not in piv]
    basis = []
    for f in free:
        v = [F.conv(0)] * ncols; v[f] = F.conv(1)
        for i, c in enumerate(piv):
            v[c] = F.norm(-R[i][f])
        basis.append(v)
    return basis

def class_rows(n, d):
    rows = []
    for c in range(d):
        r = [0] * n
        for i in range(c, n, d): r[i] = 1
        rows.append(r)
    return rows

def Wperp(F, n, blocks, d):
    """functionals vanishing on span(P) + V_d.  blocks: list of tuples; pair (i,j) -> vector e_i+e_j;
    singleton (k,) -> e_k."""
    rows = []
    for b in blocks:
        r = [0] * n
        for i in b: r[i] = 1
        rows.append(r)
    rows += class_rows(n, d)
    return nullspace(F, rows, n)

def dot(F, f, v):
    return F.norm(sum(a * b for a, b in zip(f, v)))

def contained(F, basis, cons):
    return all(F.zero(dot(F, f, v)) for f in cons for v in basis)

class Sub:
    def __init__(self, F, cons, n):
        self.cons, _ = rref(F, cons, n) if cons else ([], [])
        self.key = tuple(tuple(r) for r in self.cons)
        self.basis = nullspace(F, self.cons, n)

def run(F, n, Dset, structures, verbose=False, Vextra=None):
    Vp = {d: nullspace(F, class_rows(n, d), n) for d in Dset}   # V_d^perp
    fam = {(): Sub(F, [], n)}
    used = []
    for t, P in enumerate(structures):
        Wp = [Wperp(F, n, P, d) for d in Dset]
        new = {}
        split = False
        for key, U in fam.items():
            if any(contained(F, U.basis, w) for w in Wp):
                new[key] = U; continue
            split = True
            for w in Wp:
                V = Sub(F, U.cons + w, n)
                if any(contained(F, V.basis, Vp[d]) for d in Dset):
                    continue
                new[V.key] = V
        if split: used.append(P)
        items = list(new.values())
        keep = {}
        for U in items:
            if not any(U2 is not U and len(U2.basis) > len(U.basis) and contained(F, U.basis, U2.cons) for U2 in items):
                keep[U.key] = U
        fam = keep
        if verbose and (t % 10 == 0 or not fam):
            print(' step', t, 'family', len(fam), sorted(len(U.basis) for U in fam.values())[:8], flush=True)
        if not fam:
            return True, used, fam
    return False, used, fam

def random_nc_matching_points(pts, rng):
    """uniform random non-crossing perfect matching of the ordered list pts (even length)"""
    m = len(pts) // 2
    s = [1] * m + [-1] * (m + 1)
    rng.shuffle(s)
    tot = 0; mn = 0; mi = 0
    for i, x in enumerate(s):
        tot += x
        if tot < mn: mn = tot; mi = i + 1
    s = (s[mi:] + s[:mi])[:-1]
    stack = []; M = []
    for i, x in enumerate(s):
        if x == 1: stack.append(pts[i])
        else: M.append((stack.pop(), pts[i]))
    return M

def max_divs(n):
    ps = [p for p in range(2, n + 1) if n % p == 0 and all(p % q for q in range(2, p))]
    return [n // p for p in ps]
