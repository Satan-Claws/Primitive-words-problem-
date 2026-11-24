"""construct2_ft.py -- Lemma FT (fibre transfer) check, n = pqr (default 30 = 2*3*5).
For x supported on one fibre F (class mod r) and primitive: take the pq-rectangle R_i on F
(fibre points f_i, f_i+n/p... i.e. chords {i, i+A+B}, {i+A, i+B} with A = n/p, B = n/q), dominant chord
(tau, a) with |w| != |u|, other chord (s2,t2); then
   T = (tau ; {a, tau+1} ; {(s2,t2), (s, s+1)}),  s = tau + k*p*q (k=1),
region  x_tau - x_a - x_{tau+1} > |d_(s2,t2)| + |x_{s+1} - x_s|   (= rectangle condition when x is fibre-supported),
certificates: rectangle forms (p, q) and x_tau - x_{tau+1} + x_{s+1} - x_s in V_r^perp.
Checks: every fibre-supported primitive class in the given test file and all 60 sparse vectors, for
every choice of fibre prime r, is covered by such a T with all cells laminar; plus the cell
realisation via construct2_verify for one instance.  usage: python construct2_ft.py W30_N10.npy"""
import sys, itertools, numpy as np
import construct2_transfer as T, construct2_verify as V
n = 30; PR = (2, 3, 5)
def ft_atoms(x, r):
    p, q = [u for u in PR if u != r]; Ap, Aq = n//p, n//q
    out = []
    for i in range(n):
        ch = [(i, (i+Ap+Aq) % n), ((i+Ap) % n, (i+Aq) % n)]
        d = [x[t]-x[s] for s, t in ch]
        for j in (0, 1):
            if abs(d[j]) <= abs(d[1-j]): continue
            s0, t0 = ch[j]; tau, a = (t0, s0) if d[j] > 0 else (s0, t0)
            for k in range(1, r):
                s = (tau + k*p*q) % n; s1 = (s+1) % n; g = (tau+1) % n
                o = tuple(sorted(ch[1-j])); c2 = tuple(sorted((s, s1)))
                pts = [tau, a, g, *o, *c2]
                if len(set(pts)) < len(pts): continue
                at = T.atom_from(x, tau, [])  # placeholder to reuse crosses
                cost = x[a] + x[g] + abs(x[o[1]]-x[o[0]]) + abs(x[c2[1]]-x[c2[0]])
                if x[tau] - cost <= 0: continue
                pairs = [(tau, a), (tau, g), o, c2] + [(tau, e) for e in (o + c2) if False]
                for (u, v) in (o, c2):
                    if x[u] != x[v]: pairs.append((tau, v if x[v] > x[u] else u))
                if any(T.crosses(P1, P2) for P1, P2 in itertools.combinations(pairs, 2)): continue
                out.append((tau, (a, g), (o, c2)))
    return out
def fibre(x):
    S = [i for i in range(n) if x[i]]
    return [r for r in PR if len({i % r for i in S}) == 1]
if __name__ == '__main__':
    X = [list(int(v) for v in x) for x in np.load(sys.argv[1])]
    fs = [(x, fibre(x)) for x in X if fibre(x)]
    bad = [x for x, rs in fs if not any(ft_atoms(x, r) for r in rs)]
    print('fibre-supported classes', len(fs), 'by r', {r: sum(r in rs for _, rs in fs) for r in PR}, 'not covered by a single FT atom', len(bad))
    # 60 sparse: one fibre mod 5, pattern rot of (2,0,1,1,1,0)/(2,1,1,1,2,0)
    cnt = 0; ok = 0
    for pat in ((2,0,1,1,1,0), (2,1,1,1,2,0)):
        for rot in range(6):
            for r0 in range(5):
                x = [0]*n
                for t in range(6): x[(r0 + 5*t) % n] = pat[(t+rot) % 6]
                cnt += 1; ok += bool(ft_atoms(x, 5))
    print('sparse 60:', cnt, 'covered by single FT atom', ok)
    x = [0]*n; x[0] = 2; x[10] = x[15] = x[20] = 1
    A0 = ft_atoms(x, 5); print('x0 FT atoms e.g.', A0[:2])
    tau, P, D = A0[0]; print('cell check', V.check(tau, P, D, B=3))
