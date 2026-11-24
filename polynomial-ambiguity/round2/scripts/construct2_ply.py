"""construct2_ply.py -- (1) which test classes need transfer atoms, and whether the restricted family
T_R(tau;{a,g};{other}) = rectangle + zero-cost 5-star (report §2 Lemma FT) suffices for them;
(2) greedy D_30-invariant subfamily of systems covering all test classes, and its exact ply on the test set.
usage: python construct2_ply.py W30_N10.npy CAP"""
import sys, itertools, numpy as np
import construct_atoms as CA, construct_cover30 as cc, construct2_transfer as T
n = 30
def dom_rep(a):
    pts, sh = a[0], a[1]
    chords = tuple((pts[i], pts[j]) for i, j in sh)
    dom, _ = CA.allowed_dominants(tuple(sh))
    tops = tuple((j, pts[sh[j][1]] if sg == 1 else pts[sh[j][0]]) for j, sg in dom)
    return ('D', chords, tops, frozenset(tuple(sorted(p)) for p in a[2]), frozenset(a[3]))
def g_act(g, v): r, s = g; return (s*v + r) % n
def act(g, at):
    if at[0] == 'D':
        ch = tuple((g_act(g, s), g_act(g, t)) for s, t in at[1])
        return ('D', ch, tuple((j, g_act(g, tp)) for j, tp in at[2]),
                frozenset(tuple(sorted((g_act(g, a), g_act(g, b)))) for a, b in at[3]), at[4])
    _, tau, P, D, C = at
    return ('T', g_act(g, tau), frozenset(g_act(g, a) for a in P),
            frozenset(tuple(sorted((g_act(g, s), g_act(g, t)))) for s, t in D), C)
def key(at):
    if at[0] == 'D': return ('D', frozenset(frozenset(c) for c in at[1]), frozenset(tp for _, tp in at[2]))
    return at[:4]
def atom_eval(at, x):
    """None if region fails at x, else (support, pairs, C)."""
    if at[0] == 'D':
        ch = at[1]; d = [x[t]-x[s] for s, t in ch]; tot = sum(abs(v) for v in d)
        for j, tp in at[2]:
            s, t = ch[j]; other = s if tp == t else t
            if x[tp] - x[other] > tot - abs(d[j]):
                return (frozenset(v for c in ch for v in c), list(at[3]), at[4])
        return None
    _, tau, P, D, C = at
    cost = sum(x[a] for a in P) + sum(abs(x[t]-x[s]) for s, t in D)
    if x[tau] - cost <= 0: return None
    pairs = [(tau, a) for a in P] + list(D) + [(tau, t if x[t] > x[s] else s) for s, t in D if x[s] != x[t]]
    if any(T.crosses(p, q) for p, q in itertools.combinations(pairs, 2)): return None
    return (frozenset([tau]) | P | frozenset(v for c in D for v in c), pairs, C)
def sys_holds(S, x):
    ev = [atom_eval(a, x) for a in S]
    if any(e is None for e in ev): return False
    if frozenset().union(*[e[2] for e in ev]) != frozenset((2, 3, 5)): return False
    return all(T.compatible(e, f) for e, f in itertools.combinations(ev, 2))
G = [(r, s) for r in range(n) for s in (1, -1)]
def tr_rep(a): return ('T', a[3][1], frozenset(a[3][2]), frozenset(a[3][3]), a[2])
def systems_rep(x, cap):
    raw = cc.holds_all(x); dom = [(frozenset(a[0]), [tuple(sorted(p)) for p in a[2]], frozenset(a[3]), a) for a in raw]
    tr = T.transfer_atoms(x)
    out = []
    for S in T.find_systems(dom, cap=cap):
        out.append(tuple(dom_rep(a[3]) for a in S))
    if len(out) < cap:
        for S in T.find_systems(dom + tr, cap=cap):
            if all(a[3][0] == 'T' or True for a in S):
                out.append(tuple(dom_rep(a[3]) if a[3][0] != 'T' else tr_rep(a) for a in S))
            if len(out) >= cap: break
    return out
if __name__ == '__main__':
    X = [list(int(v) for v in x) for x in np.load(sys.argv[1])]; CAP = int(sys.argv[2])
    # (1) transfer-needing classes and restricted family T_R
    need = [x for x in X if not T.find_systems([(frozenset(a[0]), [tuple(sorted(p)) for p in a[2]], frozenset(a[3]), a) for a in cc.holds_all(x)])]
    print('classes needing transfer atoms:', len(need))
    for x in need:
        tr = T.transfer_atoms(x)
        # T_R: two partners (one 5-star partner g = tau+-6k with x_g=0 and one rectangle partner) and one chord
        tr_R = [a for a in tr if len(a[3][2]) == 2 and len(a[3][3]) == 1 and a[2] == frozenset((2, 3, 5))
                and any((g - a[3][1]) % 6 == 0 and x[g] == 0 for g in a[3][2])]
        print('  x =', [i for i in range(n) for _ in range(x[i])], ' T atoms', len(tr), ' T_R single-atom covers', len(tr_R),
              tr_R[0][3] if tr_R else None)
    # (2) greedy family
    cand = []
    for x in X: cand += systems_rep(x, CAP)
    cover = [set(i for i, x in enumerate(X) if sys_holds(S, x)) for S in cand]
    left = set(range(len(X))); chosen = []
    while left:
        b = max(range(len(cand)), key=lambda k: len(cover[k] & left))
        if not cover[b] & left: print('greedy stuck', len(left)); break
        chosen.append(cand[b]); left -= cover[b]
    print('chosen system orbits', len(chosen))
    fam = {}
    for S in chosen:
        for g in G:
            gS = tuple(act(g, a) for a in S); fam[frozenset(key(a) for a in gS)] = gS
    fam = list(fam.values()); print('family size (D_30-closure)', len(fam))
    plys = [sum(sys_holds(S, x) for S in fam) for x in X]
    print('ply on test classes: min', min(plys), 'max', max(plys), 'mean %.2f' % np.mean(plys))
    print('argmax x =', [i for i in range(n) for _ in range(X[int(np.argmax(plys))][i])])
