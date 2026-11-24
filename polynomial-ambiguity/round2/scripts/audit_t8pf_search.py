"""audit_t8pf_search.py -- adversarial search for a poly-ambiguous grammar with L ⊆ G⁻ that fits no row of
r19_fixes §4's case table.

Random reduced, ε-free, unit-free CFGs over {a,b}; S-rules biased to b...a. Filter:
  - L_n ⊆ G⁻ for all n <= NW (word-level DP with tree multiplicities),
  - L infinite with |L_NW| >= 4, max amb(w) <= NW^2 at every length (poly-ambiguity proxy),
Classify every recursive SCC reachable from S by the table's criteria (left side; mirror is symmetric):
  nonlinear: heavy -> 3a ; light & NC -> 3c ; light & not NC -> 3h
  linear: heavy left part -> 3b ; NC -> 3c ; pure-left (not NC) -> 3e ; pure-right -> PR (no left letters) ;
          heavy right & not NC -> VIOL_RH (claimed impossible: Prop NC) ;
          two-sided light critical -> VIOL_LL (claimed impossible: Thm LL, regardless of NC) ;
          else -> 3g
Heaviness / criticality are estimated from tree-count GFs truncated at length M (crude, flagged near-threshold).
NC (no cycle with D(s) >= 1) is tested with side-yield maxima over words of length <= NW (lower bound on max D,
so 'NC fails' is certain, 'NC holds' is up to NW).
"""
import random, sys, itertools
from collections import Counter, defaultdict
import numpy as np

NW = 13      # word-level bound
M = 70       # tree-count GF truncation
random.seed(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
TRIALS = int(sys.argv[2]) if len(sys.argv) > 2 else 3000

def D(w):
    return sum(1 if c == 'a' else -1 for c in w)

def in_Gminus(w):
    n = len(w)
    pa = sa = 0
    for k in range(1, n // 2 + 1):
        pa += w[k - 1] == 'a'; sa += w[n - k] == 'a'
        if not pa < sa:
            return False
    return True

def rand_grammar():
    nts = ['S', 'A', 'B', 'C'][:random.choice([2, 3, 3, 4])]
    G = {}
    for X in nts:
        rules = set()
        for _ in range(random.randint(1, 5)):
            L = random.randint(1, 3)
            rhs = tuple(random.choice(['a', 'b'] + nts + nts) for _ in range(L))
            if L == 1 and rhs[0] in nts:
                continue
            if X == 'S' and random.random() < 0.8:
                rhs = ('b',) + rhs[:2] + ('a',)
            rules.add(rhs)
        if not any(all(s in 'ab' for s in r) for r in rules) and random.random() < 0.7:
            rules.add(random.choice([('a',), ('b',), ('b', 'a'), ('a', 'b')]))
        G[X] = sorted(rules)
    return G

def reduce(G):
    prod = set()
    ch = True
    while ch:
        ch = False
        for X, rs in G.items():
            if X not in prod and any(all(s in 'ab' or s in prod for s in r) for r in rs):
                prod.add(X); ch = True
    if 'S' not in prod:
        return None
    G2 = {X: [r for r in rs if all(s in 'ab' or s in prod for s in r)] for X, rs in G.items() if X in prod}
    reach = {'S'}; st = ['S']
    while st:
        X = st.pop()
        for r in G2[X]:
            for s in r:
                if s not in 'ab' and s not in reach:
                    reach.add(s); st.append(s)
    return {X: G2[X] for X in G2 if X in reach}

def words(G):
    W = {X: [Counter() for _ in range(NW + 1)] for X in G}
    for l in range(1, NW + 1):
        for X, rs in G.items():
            for r in rs:
                # combine symbol by symbol
                cur = {0: Counter({'': 1})}
                for i, s in enumerate(r):
                    rem = len(r) - i - 1
                    nxt = defaultdict(Counter)
                    for pl, cw in cur.items():
                        if s in 'ab':
                            if pl + 1 + rem <= l:
                                for w, c in cw.items():
                                    nxt[pl + 1][w + s] += c
                        else:
                            for sl in range(1, l - pl - rem + 1):
                                if sl >= l:  # unit-free: a NT inside rule of len>=2 has len < l
                                    continue
                                src = W[s][sl]
                                if not src:
                                    continue
                                for w, c in cw.items():
                                    for v, d in src.items():
                                        nxt[pl + sl][w + v] += c * d
                    cur = nxt
                if l in cur:
                    W[X][l].update(cur[l])
    return W

def treegf(G):
    F = {X: np.zeros(M + 1, dtype=object) for X in G}
    for l in range(1, M + 1):
        for X, rs in G.items():
            tot = 0
            for r in rs:
                poly = np.zeros(l + 1, dtype=object); poly[0] = 1
                for s in r:
                    g = np.zeros(l + 1, dtype=object)
                    if s in 'ab':
                        g[1:] = poly[:-1]
                    else:
                        f = F[s]
                        for i in range(l + 1):
                            if poly[i]:
                                for j in range(1, min(l - i, l - 1) + 1):
                                    if f[j]:
                                        g[i + j] += poly[i] * f[j]
                    poly = g
                tot += poly[l]
            F[X][l] = tot
    return F

def growth(f):
    v = [float(f[l]) for l in range(M - 20, M + 1)]
    if v[-1] == 0:
        return 0.0
    nz = [(l, x) for l, x in zip(range(M - 20, M + 1), v) if x > 0]
    if len(nz) < 2:
        return 0.0
    (l0, x0), (l1, x1) = nz[0], nz[-1]
    if l1 == l0:
        return 0.0
    return (x1 / x0) ** (1.0 / (l1 - l0))

def sccs(G):
    adj = {X: {s for r in G[X] for s in r if s not in 'ab'} for X in G}
    reach = {}
    for X in G:
        seen = set(); st = [X]
        while st:
            Y = st.pop()
            for Z in adj[Y]:
                if Z not in seen:
                    seen.add(Z); st.append(Z)
        reach[X] = seen
    comps = []
    done = set()
    for X in G:
        if X in done:
            continue
        C = {X} | {Y for Y in reach[X] if X in reach[Y]}
        done |= C
        rec = X in reach[X]
        comps.append((frozenset(C), rec))
    return comps

def classify(G, W, F):
    gr = {X: growth(F[X]) for X in G}
    heavy = lambda X: gr[X] > 1.9
    F_half = {X: float(sum(F[X][l] / 2 ** l for l in range(1, M + 1))) for X in G}
    maxD = {X: max([D(w) for l in range(1, NW + 1) for w in W[X][l]] or [-99]) for X in G}
    minD = {X: min([D(w) for l in range(1, NW + 1) for w in W[X][l]] or [99]) for X in G}
    out = []
    for C, rec in sccs(G):
        if not rec:
            continue
        C = sorted(C)
        idx = {X: i for i, X in enumerate(C)}
        rules = [(X, r, [i for i, s in enumerate(r) if s in idx]) for X in C for r in G[X]]
        inrules = [t for t in rules if t[2]]
        linear = all(len(t[2]) <= 1 for t in rules)
        # left-drift max-weight graph (for nonlinear: each T-occurrence can be the spine child)
        n = len(C)
        NEG = -10 ** 9
        Wl = [[NEG] * n for _ in range(n)]; Wr = [[10 ** 9] * n for _ in range(n)]
        lh = rh = False; pure_left = pure_right = True
        for X, r, occ in inrules:
            for k in occ:
                al, be = r[:k], r[k + 1:]
                dl = sum(1 if s == 'a' else -1 if s == 'b' else maxD[s] for s in al)
                dr = sum(1 if s == 'a' else -1 if s == 'b' else minD[s] for s in be)
                i, j = idx[X], idx[r[k]]
                Wl[i][j] = max(Wl[i][j], dl); Wr[i][j] = min(Wr[i][j], dr)
                if al: pure_right = False
                if be: pure_left = False
                lh |= any(s not in 'ab' and heavy(s) for s in al)
                rh |= any(s not in 'ab' and heavy(s) for s in be)
        # max cycle weight via n-step closure
        best = [row[:] for row in Wl]
        for _ in range(n + 1):
            new = [row[:] for row in best]
            for i in range(n):
                for j in range(n):
                    for k in range(n):
                        if best[i][k] > NEG and Wl[k][j] > NEG:
                            new[i][j] = max(new[i][j], best[i][k] + Wl[k][j])
            best = new
        NC = all(best[i][i] <= 0 for i in range(n))
        Th = max(gr[X] for X in C)
        if not linear:
            row = '3a' if Th > 1.9 else ('3c' if NC else '3h')
            rho = None
        else:
            Mh = np.zeros((n, n))
            for X, r, occ in inrules:
                k = occ[0]; w = 1.0
                for i, s in enumerate(r):
                    if i == k: continue
                    w *= 0.5 if s in 'ab' else F_half[s]
                Mh[idx[X], idx[r[k]]] += w
            rho = max(abs(np.linalg.eigvals(Mh)))
            crit = rho > 0.97
            if lh: row = '3b'
            elif crit and not pure_left and not pure_right and not rh: row = 'VIOL_LL'
            elif NC: row = '3c'
            elif pure_left: row = '3e'
            elif pure_right: row = 'PR'
            elif rh: row = 'VIOL_RH'
            else: row = '3g'
        out.append((''.join(C), 'lin' if linear else 'nonlin', round(Th, 3), None if rho is None else round(rho, 3),
                    'NC' if NC else 'posCyc', row))
    return out

stats = Counter(); kept = 0; viol = []
examples = defaultdict(list)
for t in range(TRIALS):
    G = reduce(rand_grammar())
    if not G:
        continue
    if any(len(r) == 1 and r[0] not in 'ab' for rs in G.values() for r in rs):
        continue
    W = words(G)
    ok = True; sizes = []
    for l in range(1, NW + 1):
        Wl = W['S'][l]
        if any(not in_Gminus(w) for w in Wl) or (Wl and max(Wl.values()) > max(4, l * l)):
            ok = False; break
        sizes.append(len(Wl))
    if not ok or sizes[-1] < 4:
        continue
    # poly-ambiguity proxy for EVERY nonterminal (a sub-grammar can be exponentially ambiguous on few words)
    if any(W[X][l] and max(W[X][l].values()) > max(4, l * l // 2) for X in G for l in range(1, NW + 1)):
        stats['rej_amb_nt'] += 1; continue
    kept += 1
    F = treegf(G)
    if max(growth(F[X]) for X in G) > 2.03:   # tree growth > 2 => exponential ambiguity: not admissible
        stats['rej_expamb'] += 1; continue
    cl = classify(G, W, F)
    for c in cl:
        stats[c[-1]] += 1
        if len(examples[c[-1]]) < 2:
            examples[c[-1]].append((G, c, sizes[-1]))
        if c[-1].startswith('VIOL'):
            viol.append((G, c))
print(f"trials={TRIALS} kept(L⊆G⁻ to n={NW}, amb<=n², |L_n|>=4)={kept}")
print("row counts:", dict(stats))
for k, ex in sorted(examples.items()):
    for G, c, s in ex:
        print(k, c, '|L_13|=%d' % s, {X: [''.join(r) for r in rs] for X, rs in G.items()})
print("violations:", len(viol))
for G, c in viol[:5]:
    print("  VIOL", c, {X: [''.join(r) for r in rs] for X, rs in G.items()})
