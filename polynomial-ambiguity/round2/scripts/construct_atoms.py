"""construct_atoms.py -- dominance atoms and laminar certificate systems for Q ∩ (ab*)^n, n squarefree.

Atom = k non-crossing chords (s_i<t_i), d_i = x_{t_i}-x_{s_i}.  Region of atom =
  U_{allowed (j,sg)} { sg*d_j > sum_{i!=j} |d_i| }.
Piece realisation (exact, disjoint, simplicial): base e_{top}, generators e_{s_i}+e_{t_i} (all i),
transfer e_{end_i}+e_{top} (end_i = t_i if d_i>=0 else s_i, i != j), slack e_{top}; top = t_j (sg=+) / s_j (sg=-);
(j,sg) is *allowed* iff for every sign pattern these pairs are pairwise non-crossing.
Certified primes: p such that some signed sum sum_i eps_i d_i lies in V_p^perp (balanced on every
shift-(n/p) orbit); on the region every such signed sum is nonzero.
System = atoms with disjoint supports and mutually non-crossing pair sets whose certified primes cover all p.
"""
import itertools, numpy as np
from functools import lru_cache

def crosses(p, q):
    a, b = sorted(p); c, d = sorted(q)
    return (a < c < b < d) or (c < a < d < b)

def matchings(m):
    """non-crossing perfect matchings of range(2m) as list of pairs (index-level)."""
    if m == 0: return [[]]
    out = []
    for k in range(1, 2*m, 2):  # 0 matched with k
        for L in matchings((k-1)//2):
            for R in matchings((2*m-k-1)//2):
                out.append([(0, k)] + [(a+1, b+1) for a, b in L] + [(a+k+1, b+k+1) for a, b in R])
    return out

@lru_cache(None)
def allowed_dominants(shape):
    """shape: tuple of index pairs on 0..2k-1. returns list of (j,sg) and union pair set (index level)."""
    k = len(shape); res = []; allpairs = set(shape)
    for j in range(k):
        for sg in (1, -1):
            top = shape[j][1] if sg == 1 else shape[j][0]
            ok = True; used = set()
            for signs in itertools.product((0, 1), repeat=k):
                pairs = list(shape)
                for i in range(k):
                    if i == j: continue
                    end = shape[i][1] if signs[i] == 0 else shape[i][0]
                    pairs.append(tuple(sorted((end, top))))
                prs = [p for p in pairs if p[0] != p[1]]
                if any(crosses(p, q) for p, q in itertools.combinations(prs, 2)):
                    ok = False; break
                used |= set(prs)
            if ok: res.append((j, sg)); allpairs |= used
    return tuple(res), frozenset(allpairs)

class Setup:
    def __init__(self, n, primes):
        self.n = n; self.primes = primes; self.A = {p: n//p for p in primes}
    def certified(self, pts, shape):
        """set of primes certified by the atom on sorted points pts with index-level shape."""
        k = len(shape); C = set()
        for eps in itertools.product((1, -1), repeat=k-1):
            eps = (1,) + eps
            coef = {}
            for (a, b), e in zip(shape, eps):
                coef[pts[b]] = coef.get(pts[b], 0) + e
                coef[pts[a]] = coef.get(pts[a], 0) - e
            for p in self.primes:
                A = self.A[p]; bal = {}
                for v, c in coef.items(): bal[v % A] = bal.get(v % A, 0) + c
                if all(c == 0 for c in bal.values()): C.add(p)
        return frozenset(C)
    def inE(self, x):
        x = np.asarray(x)
        return all(not np.array_equal(x, np.roll(x, self.A[p])) for p in self.primes)
    def W(self, comps):
        """x = sum_p periodic extension of comps[p] (length A_p ... period n/p)."""
        x = np.zeros(self.n, dtype=int)
        for p, c in comps.items():
            x += np.tile(np.asarray(c), p)
        return x

def atom_holds(x, pts, shape):
    d = [x[pts[b]] - x[pts[a]] for a, b in shape]
    dom, _ = allowed_dominants(tuple(shape))
    tot = sum(abs(v) for v in d)
    return any(sg*d[j] > tot - abs(d[j]) for j, sg in dom)

def atom_pairs(pts, shape):
    _, P = allowed_dominants(tuple(shape))
    return [(pts[a], pts[b]) for a, b in P]

def compatible(at1, at2):
    if set(at1[0]) & set(at2[0]): return False
    return not any(crosses(p, q) for p in at1[2] for q in at2[2])

def enumerate_atoms(S, kmax=2, need=None):
    """all atoms with <=kmax chords certifying a nonempty prime set. returns list (pts, shape, pairs, C)."""
    out = []
    for k in range(1, kmax+1):
        shapes = [tuple(m) for m in matchings(k)]
        for pts in itertools.combinations(range(S.n), 2*k):
            for sh in shapes:
                dom, _ = allowed_dominants(sh)
                if not dom: continue
                C = S.certified(pts, sh)
                if not C: continue
                if need is not None and not need(C, k): continue
                out.append((pts, sh, atom_pairs(pts, sh), C))
    return out
