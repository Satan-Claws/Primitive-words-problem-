"""construct36_core.py -- n = 36 = (2*3)^2 (first S_N slice S_2): exhaustive primitive W_36 ∩ N^36 up to D_36,
and coverage by chord-dominance atoms (k<=2, construct_atoms.py) + transfer atoms (construct2_transfer.py).

Enumeration [written fact, used]: Phi_36(z) = Phi_6(z^6), so x(z) = sum_r z^r y_r(z^6) lies in W_36 iff every fibre
restriction y_r = (x_{r+6t})_{t in Z_6} lies in W_6 (fibre r = class r mod 6).  We enumerate W_6 ∩ N^6 by brute force
(Phi_6 test) and take products over the 6 fibres.  Primitive = not 18-periodic and not 12-periodic.

Coverage code is the construct/construct2 code with n=36, primes (2,3), A = {2:18, 3:12}; dom-atom holding test and
system search are vectorised (bitmask compatibility) but implement the same predicates:
  system = 1 atom with C ⊇ {2,3}, or 2 atoms with disjoint supports, mutually non-crossing pair sets, C1 ∪ C2 ⊇ {2,3}.
"""
import itertools, numpy as np
import construct_atoms as CA, construct2_transfer as T
n = 36; PR = (2, 3); A = {2: 18, 3: 12}
T.n = n; T.PR = PR; T.A = A
S = CA.Setup(n, list(PR))

# ---------- enumeration ----------
def w6_vectors(N):
    out = []
    for y in itertools.product(range(N + 1), repeat=6):
        if sum(y) > N: continue
        # Phi_6(z) = z^2 - z + 1: y(zeta)=0 for zeta = e^{i pi/3}; use exact: reduce mod z^2 - z + 1
        # z^0..z^5 mod Phi_6: 1, z, z-1, -1, -z, 1-z
        c0 = y[0] - y[2] - y[3] + y[5]; c1 = y[1] + y[2] - y[4] - y[5]
        if c0 == 0 and c1 == 0: out.append(y)
    return out
_G = np.array([[(s * i + r) % n for i in range(n)] for r in range(n) for s in (1, -1)])  # D_36 as index maps
def canon(x):
    """lexicographically smallest image of x under D_36 (entries < 64 assumed)."""
    Y = np.asarray(x)[_G]
    best = min(map(tuple, Y.tolist()))
    return best
def prim(x):
    x = np.asarray(x)
    return not np.array_equal(x, np.roll(x, 18)) and not np.array_equal(x, np.roll(x, 12))
def enumerate_W36(N):
    Y = w6_vectors(N); byn = {}
    for y in Y: byn.setdefault(sum(y), []).append(y)
    seen = set(); tot = 0
    def rec(r, left, fib):
        nonlocal tot
        if r == 6:
            x = np.zeros(n, int)
            for rr, y in enumerate(fib): x[rr::6] = y
            if x.sum() == 0 or not prim(x): return
            tot += 1; seen.add(canon(x)); return
        for m in range(left + 1):
            for y in byn.get(m, []):
                rec(r + 1, left - m, fib + [y])
    rec(0, N, [])
    return tot, sorted(seen)

# ---------- dominance atoms (k <= 2), vectorised ----------
ATOMS = CA.enumerate_atoms(S, 2)
PAIRS = [(a, b) for a in range(n) for b in range(a + 1, n)]; PIDX = {p: i for i, p in enumerate(PAIRS)}
NW = (len(PAIRS) + 63) // 64
CROSS = np.zeros((len(PAIRS), NW), np.uint64)
for i, p in enumerate(PAIRS):
    for j, q in enumerate(PAIRS):
        if CA.crosses(p, q): CROSS[i, j // 64] |= np.uint64(1) << np.uint64(j % 64)
def masks(pairs):
    pm = np.zeros(NW, np.uint64); fm = np.zeros(NW, np.uint64)
    for p in pairs:
        i = PIDX[tuple(sorted(p))]; pm[i // 64] |= np.uint64(1) << np.uint64(i % 64); fm |= CROSS[i]
    return pm, fm
def supmask(pts):
    m = 0
    for v in pts: m |= 1 << int(v)
    return m
K = np.array([len(a[1]) for a in ATOMS])
P4 = np.array([list(a[0]) + [a[0][0]] * (4 - len(a[0])) for a in ATOMS])
SH = []
for a in ATOMS:
    s = list(a[1]) + [(0, 0)] * (2 - len(a[1])); SH.append([s[0][0], s[0][1], s[1][0], s[1][1]])
SH = np.array(SH)
for a in ATOMS:  # all k<=2 shapes allow every dominant (construct.md §1); check
    assert len(CA.allowed_dominants(tuple(a[1]))[0]) == 2 * len(a[1])
D_PM = np.zeros((len(ATOMS), NW), np.uint64); D_FM = np.zeros((len(ATOMS), NW), np.uint64)
for i, a in enumerate(ATOMS): D_PM[i], D_FM[i] = masks(a[2])
D_SUP = np.array([supmask(a[0]) for a in ATOMS], dtype=np.uint64)
D_C2 = np.array([2 in a[3] for a in ATOMS]); D_C3 = np.array([3 in a[3] for a in ATOMS])
def dom_holding(x):
    x = np.asarray(x); X = x[P4]; r = np.arange(len(ATOMS))
    d1 = X[r, SH[:, 1]] - X[r, SH[:, 0]]; d2 = X[r, SH[:, 3]] - X[r, SH[:, 2]]
    return np.where(K == 1, d1 != 0, np.abs(d1) != np.abs(d2))

def atom_table(x, use_T):
    """returns arrays (C2, C3, SUP, PM, FM, labels) for all atoms holding at x."""
    h = dom_holding(x)
    C2, C3, SUP, PM, FM = D_C2[h], D_C3[h], D_SUP[h], D_PM[h], D_FM[h]
    lab = [('D', ATOMS[i][0], ATOMS[i][1]) for i in np.nonzero(h)[0]]
    if use_T:
        tr = T.transfer_atoms(list(int(v) for v in x))
        if tr:
            c2 = np.array([2 in a[2] for a in tr]); c3 = np.array([3 in a[2] for a in tr])
            sp = np.array([supmask(a[0]) for a in tr], dtype=np.uint64)
            mm = [masks(a[1]) for a in tr]
            C2 = np.concatenate([C2, c2]); C3 = np.concatenate([C3, c3]); SUP = np.concatenate([SUP, sp])
            PM = np.concatenate([PM, np.array([m[0] for m in mm])]); FM = np.concatenate([FM, np.array([m[1] for m in mm])])
            lab += [a[3] for a in tr]
    return C2, C3, SUP, PM, FM, lab

def systems(x, use_T=False, count=False):
    """first system (or number of systems if count) covering x."""
    C2, C3, SUP, PM, FM, lab = atom_table(x, use_T)
    both = np.nonzero(C2 & C3)[0]
    if not count and len(both): return [(lab[both[0]],)]
    tot = len(both); I2 = np.nonzero(C2)[0]; I3 = np.nonzero(C3 & ~C2)[0]
    # pairs: a certifies 2, b certifies 3 (b not certifying 2 to avoid double counting with both-atoms in I2)
    for i in I2:
        ok = (SUP[I3] & SUP[i]) == 0
        ok &= ~np.any((FM[I3] & PM[i]) != 0, axis=1)
        ok &= ~np.any((PM[I3] & FM[i]) != 0, axis=1)
        if ok.any():
            if not count: return [(lab[i], lab[I3[np.argmax(ok)]])]
            tot += int(ok.sum())
    return tot if count else []

def fibre_structure(x):
    """per fibre r mod 6: (norm, in V_2-part?, ...) -- 2-witness fibres: restriction not 3-periodic (t -> t+3),
    3-witness fibres: restriction not 2-periodic (t -> t+2)."""
    x = np.asarray(x); out = []
    for r in range(6):
        y = x[r::6]
        w2 = not np.array_equal(y, np.roll(y, 3)); w3 = not np.array_equal(y, np.roll(y, 2))
        out.append((r, tuple(int(v) for v in y), w2, w3))
    return out
