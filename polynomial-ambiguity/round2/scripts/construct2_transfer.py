"""construct2_transfer.py -- transfer atoms (shared-top star atoms) for Q ∩ (ab*)^30 and system search.

Transfer atom T = (tau; P; D): top tau, partner set P, chord set D = {(s_i,t_i)}, all points distinct.
  Region R_T = { x : x_tau - sum_{a in P} x_a  >  sum_i |x_{t_i} - x_{s_i}| }.
  Exact laminar realisation, one piece per cell delta in {+,0,-}^D (sign of d_i = x_t - x_s):
    c   = e_tau + sum_{delta_i=+} (e_{t_i}+e_tau) + sum_{delta_i=-} (e_{s_i}+e_tau)
    V   = {e_tau} ∪ {e_a+e_tau : a in P} ∪ {e_{s_i}+e_{t_i}} ∪ {e_{hi_i}+e_tau : delta_i != 0} ∪ {e_m : m outside}
    (hi_i = larger-valued endpoint).  Triangular => unimodular; d_sigma = 0; cells disjoint.
  Pairs of the cell: {tau,a}, {s_i,t_i}, {tau,hi_i}; the cell is *allowed* iff they are pairwise non-crossing.
  Certificates on R_T (valid on every cell): forms  F = x_tau - x_a + sum_{i in I} eps_i d_i  (a in P, I ⊆ D)
  since x_tau - x_a >= x_tau - sum_P x_a > sum |d_i|.  C(T) = {p : some such F in V_p^perp}.
|P|=1 recovers the chord-dominance atoms of construct_atoms.py (dominant chord = (tau, a)).
Here we use forms with |I| <= 1 and |P| <= 3 (one form per certified prime)."""
import itertools, numpy as np
n = 30; PR = (2, 3, 5); A = {2: 15, 3: 10, 5: 6}
def crosses(p, q):
    a, b = sorted(p); c, d = sorted(q)
    return (a < c < b < d) or (c < a < d < b)
def balanced(coef, p):
    bal = {}
    for v, c in coef.items(): bal[v % A[p]] = bal.get(v % A[p], 0) + c
    return all(c == 0 for c in bal.values())

def forms_at(x, tau):
    """single-form transfer certificates at top tau: (p, a, chord or None, eps) with cost < x_tau."""
    out = []; B = x[tau]
    for p in PR:
        m = A[p]
        for a in range(n):
            if a == tau or x[a] >= B: continue
            if (a - tau) % m == 0: out.append((p, a, None, 0, x[a])); continue
            # one chord (s,t): +tau -a + eps (x_t - x_s) balanced <=> {tau, hi} = {a, lo} mod m with
            # eps=+: hi=t, lo=s ; need s ≡ tau, t ≡ a  (other matching is trivial)
            for s in range(tau % m, n, m):
                for t in range(a % m, n, m):
                    if len({tau, a, s, t}) < 4: continue
                    cost = x[a] + abs(x[t] - x[s])
                    if cost < B:
                        lo, hi = min(s, t), max(s, t)
                        out.append((p, a, (lo, hi), 1, cost))
    return out

def atom_from(x, tau, fs):
    """combine forms (distinct primes) at top tau into one atom; return (support, pairs, C) or None."""
    P = set(); D = set()
    for f in fs:
        P.add(f[1])
        if f[2] is not None: D.add(f[2])
    pts = [tau] + sorted(P) + [v for c in sorted(D) for v in c]
    if len(set(pts)) != len(pts): return None
    cost = sum(x[a] for a in P) + sum(abs(x[t] - x[s]) for s, t in D)
    if cost >= x[tau]: return None
    pairs = [(tau, a) for a in P] + list(D)
    for s, t in D:
        if x[s] != x[t]: pairs.append((tau, t if x[t] > x[s] else s))
    if any(crosses(p, q) for p, q in itertools.combinations(pairs, 2)): return None
    return (frozenset(pts), pairs, frozenset(f[0] for f in fs), ('T', tau, tuple(sorted(P)), tuple(sorted(D))))

def transfer_atoms(x):
    out = []
    for tau in range(n):
        if x[tau] == 0: continue
        F = forms_at(x, tau)
        byp = {p: [f for f in F if f[0] == p] for p in PR}
        for r in (1, 2, 3):
            for ps in itertools.combinations(PR, r):
                for fs in itertools.product(*[byp[p] for p in ps]):
                    at = atom_from(x, tau, fs)
                    if at: out.append(at)
    # dedupe
    seen = {}; 
    for at in out:
        k = (at[0], frozenset(at[1]))
        if k not in seen or len(at[2]) > len(seen[k][2]): seen[k] = at
    return list(seen.values())

def compatible(a, b):
    if a[0] & b[0]: return False
    return not any(crosses(p, q) for p in a[1] for q in b[1])

def find_systems(atoms, stop=True, need=frozenset(PR), cap=None):
    found = []
    if cap: stop = False
    for a in atoms:
        if a[2] >= need:
            found.append((a,))
            if stop or (cap and len(found) >= cap): return found
    for a, b in itertools.combinations(atoms, 2):
        if (a[2] | b[2]) >= need and compatible(a, b):
            found.append((a, b))
            if stop or (cap and len(found) >= cap): return found
    single = {p: [a for a in atoms if a[2] == frozenset([p])] for p in PR}
    for a in single[2]:
        for b in single[3]:
            if not compatible(a, b): continue
            for c in single[5]:
                if compatible(a, c) and compatible(b, c):
                    found.append((a, b, c))
                    if stop or (cap and len(found) >= cap): return found
    return found
