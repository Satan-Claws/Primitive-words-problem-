"""Task G helper: explicit CFG toolkit with tree-count-preserving transforms and a CYK counting DP.
Grammar = (start, rules) with rules: dict NT -> list of RHS tuples (duplicates = multiplicity, kept).
Terminals are single lowercase letters 'a','b'; everything else is a nonterminal.
All transforms below preserve amb_G(w) for every nonempty w (asserted preconditions):
  eps_removal : requires every nullable NT to have exactly ONE epsilon-tree;
  unit removal: requires the unit graph to be acyclic;
  binarize / terminal lifting: bijective on trees;
  cyc (PA/poly_S4C Theorem C): amb_cyc(w) = sum_{j<n} amb_G(rot_j w);
  sigma (walk.md): substitution a->X, b->Y with X->a, Y->Za, Z->bWaW, W->eps|bWaW (pieces unambiguous)."""
from collections import defaultdict
import itertools

def is_t(s): return s in ('a', 'b')

def eps_trees(G):
    S, R = G
    e = defaultdict(int)
    changed = True
    while changed:
        changed = False
        for A, rhss in R.items():
            tot = 0
            for r in rhss:
                p = 1
                for s in r:
                    p *= 0 if is_t(s) else e[s]
                tot += p
            tot = min(tot, 10)  # >1 suffices to flag
            if tot != e[A]:
                e[A] = tot; changed = True
    return e

def eps_removal(G):
    S, R = G
    e = eps_trees(G)
    assert all(v <= 1 for v in e.values()), "nullable NT with >1 eps-tree"
    NR = defaultdict(list)
    for A, rhss in R.items():
        for r in rhss:
            opts = [[(s,)] + ([()] if (not is_t(s) and e[s]) else []) for s in r]
            for choice in itertools.product(*opts):
                nr = tuple(x for c in choice for x in c)
                if nr: NR[A].append(nr)
    return (S, dict(NR))

def binarize(G, tag='B'):
    S, R = G
    NR = defaultdict(list); cnt = [0]
    T = {'a': tag + '_ta', 'b': tag + '_tb'}
    used = set()
    def lift(s):
        if is_t(s): used.add(s); return T[s]
        return s
    for A, rhss in R.items():
        for r in rhss:
            if len(r) == 1:
                NR[A].append(r); continue
            r = tuple(lift(s) for s in r)
            cur = A
            while len(r) > 2:
                cnt[0] += 1; nn = f"{tag}_{cnt[0]}"
                NR[cur].append((r[0], nn)); cur = nn; r = r[1:]
            NR[cur].append(r)
    for t in used: NR[T[t]].append((t,))
    return (S, dict(NR))

def unit_removal(G):
    S, R = G
    # topological order on unit graph
    order = []; state = {}
    def visit(A):
        st = state.get(A)
        if st == 1: raise AssertionError("unit cycle at " + A)
        if st == 2: return
        state[A] = 1
        for r in R.get(A, []):
            if len(r) == 1 and not is_t(r[0]): visit(r[0])
        state[A] = 2; order.append(A)
    for A in list(R): visit(A)
    NR = {}
    for A in order:  # children first
        out = []
        for r in R.get(A, []):
            if len(r) == 1 and not is_t(r[0]): out.extend(NR[r[0]])
            else: out.append(r)
        NR[A] = out
    return (S, NR)

def prune(G):
    S, R = G
    # productive
    prod = set(); ch = True
    while ch:
        ch = False
        for A, rhss in R.items():
            if A in prod: continue
            if any(all(is_t(s) or s in prod for s in r) for r in rhss): prod.add(A); ch = True
    R = {A: [r for r in rhss if all(is_t(s) or s in prod for s in r)] for A, rhss in R.items() if A in prod}
    reach = {S}; st = [S]
    while st:
        A = st.pop()
        for r in R.get(A, []):
            for s in r:
                if not is_t(s) and s not in reach: reach.add(s); st.append(s)
    return (S, {A: R[A] for A in R if A in reach})

def cnf(G, tag):
    return prune(unit_removal(binarize(prune(eps_removal(G)), tag)))

def rename(G, p):
    S, R = G
    f = lambda s: s if is_t(s) else p + s
    return (f(S), {f(A): [tuple(f(s) for s in r) for r in rhss] for A, rhss in R.items()})

def swap(G):
    S, R = G
    f = lambda s: {'a': 'b', 'b': 'a'}.get(s, s)
    return (S, {A: [tuple(f(s) for s in r) for r in rhss] for A, rhss in R.items()})

def union(G1, G2, S='U'):
    R = dict(G1[1]); R.update(G2[1]); assert not set(G1[1]) & set(G2[1])
    R[S] = [(G1[0],), (G2[0],)]
    return (S, R)

def cyc(G, tag):
    """PA/poly_S4C Theorem C construction on a CNF grammar."""
    S, R = G
    NR = defaultdict(list); br = lambda A: f"[{A}]"
    for B, rhss in R.items():
        for r in rhss:
            if len(r) == 2:
                A, C = r  # B -> A C
                NR[br(A)].append((C, br(B)))   # [A] -> C [B]
                NR[br(C)].append((br(B), A))   # [C] -> [B] A
            else:
                NR[tag + 'S0'].append((r[0], br(B)))
    NR[br(S)].append(())
    for A, rhss in R.items(): NR[A] = list(rhss)  # sibling subtrees use the original rules
    return cnf(rename((tag + 'S0', dict(NR)), ''), tag)

SIGMA_RULES = {'X': [('a',)], 'Y': [('Z', 'a')], 'Z': [('b', 'W', 'a', 'W')], 'W': [(), ('b', 'W', 'a', 'W')]}

def sigma(G, tag):
    S, R = rename(G, tag)
    f = lambda s: {'a': tag + 'X', 'b': tag + 'Y'}.get(s, s)
    NR = {A: [tuple(f(s) for s in r) for r in rhss] for A, rhss in R.items()}
    for A, rhss in SIGMA_RULES.items():
        NR[tag + A] = [tuple(s if is_t(s) else tag + s for s in r) for r in rhss]
    return (S, NR)

def T(G, tag):
    """walk.md T(M) = Cyc(sigma(M)) u swap(Cyc(sigma(M)))."""
    C = cyc(cnf(sigma(G, tag + 's'), tag + 'n'), tag + 'c')
    C1 = rename(C, tag + 'P'); C2 = rename(swap(C), tag + 'M')
    return cnf(union(C1, C2, tag + 'U'), tag + 'f')

# walk.md explicit grammar of E' = {Delta = +-1} written over {a,b} (S -> K a K | K b K, K -> eps | aKbK | bKaK)
EPRIME = ('S', {'S': [('K', 'a', 'K'), ('K', 'b', 'K')], 'K': [(), ('a', 'K', 'b', 'K'), ('b', 'K', 'a', 'K')]})

# Repaired E' grammar (same language): K = balanced words by first return, P/M = Dyck words (unambiguous).
EFIX = ('S', {'S': [('K', 'a', 'K'), ('K', 'b', 'K')], 'K': [(), ('a', 'P', 'b', 'K'), ('b', 'M', 'a', 'K')],
              'P': [(), ('a', 'P', 'b', 'P')], 'M': [(), ('b', 'M', 'a', 'M')]})

def cyk(G, w):
    """Exact tree count of a CNF grammar (no eps, no units) on w, big ints."""
    S, R = G
    n = len(w)
    term = defaultdict(list); binr = []
    for A, rhss in R.items():
        for r in rhss:
            if len(r) == 1: term[r[0]].append(A)
            else: binr.append((A, r[0], r[1]))
    t = {}
    for i in range(n):
        d = defaultdict(int)
        for A in term[w[i]]: d[A] += 1
        t[i, i + 1] = d
    for L in range(2, n + 1):
        for i in range(n - L + 1):
            j = i + L; d = defaultdict(int)
            for k in range(i + 1, j):
                l, r = t[i, k], t[k, j]
                if not l or not r: continue
                for A, B, C in binr:
                    x = l.get(B)
                    if x:
                        y = r.get(C)
                        if y: d[A] += x * y
            t[i, j] = d
    return t[0, n].get(S, 0) if n else 0

def size(G): return len(G[1]), sum(len(v) for v in G[1].values())
