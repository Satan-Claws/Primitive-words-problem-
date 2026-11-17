# M=2: (1) the natural grammar pieces and their behaviour on P(t,delta);
#      (2) search for a ply-1 (exact) cover of the window {P(t,delta): 0<|delta|_inf<=R} by laminar simple
#          linear sets avoiding the diagonal (refuting the M=2 consequence of the theorem would need one).
import random, itertools, sys
from math import lcm
import section5_classify as S   # reuses classify/member (module runs its own test on import; that is fine)
from section5_classify import classify, member, rand_laminar, omega, deltas, n

def pattern(c, V, Lm, T=10**6):
    t = Lm*T
    return frozenset(d for d in deltas
                     if member(c, V, [t*omega[0], t*omega[1], t*omega[0]+Lm*d[0], t*omega[1]+Lm*d[1]]))

def meets_diag(c, V, B=25):
    r = len(V)
    for a in itertools.product(range(B), repeat=r):
        P = [c[i] + sum(a[j]*V[j][i] for j in range(r)) for i in range(n)]
        if P[0] == P[2] and P[1] == P[3]: return True
    return False

def e(i, k=1): v = [0]*4; v[i] = k; return v
def s(i, j): v = [0]*4; v[i] = 1; v[j] = 1; return v
natural = {
 'x1<y1': ([1,1,2,1], [s(0,2), e(2), e(1), e(3)]),
 'x1>y1': ([2,1,1,1], [s(0,2), e(0), e(1), e(3)]),
 'x2<y2': ([1,1,1,2], [e(0), e(2), s(1,3), e(3)]),
 'x2>y2': ([1,2,1,1], [e(0), e(2), s(1,3), e(1)]),
 'x1<y2 (cross-index, meets diagonal)': ([1,1,1,2], [s(0,3), e(1), e(2), e(3)]),
 'y2>=x1+1,y1>=x2 (nested, sum-type)': ([1,1,1,2], [s(0,3), s(1,2), e(2), e(3)]),
 'x1=y1,x2<y2 (CROSSING periods, not laminar)': ([1,1,1,2], [s(0,2), s(1,3), e(3)]),
}
Lm = lcm(*range(1, 41))
print('--- natural / structured pieces, omega =', omega)
for name, (c, V) in natural.items():
    cls, psi = classify(V)
    pat = pattern(c, V, Lm)
    desc = 'empty' if not pat else ('half-plane psi=%s' % (tuple(str(x) for x in psi),) if psi and
             pat == {d for d in deltas if psi[0]*d[0]+psi[1]*d[1] > 0} else 'pattern=%s' % sorted(pat))
    print(f'{name:45s} case {cls:3s} on window: {desc}; meets diagonal: {meets_diag(c, V)}')

def exact_cover(universe, sets):
    universe = set(universe)
    by = {u: [S_ for S_ in sets if u in S_] for u in universe}
    sol = []
    def rec(unc):
        if not unc: return list(sol)
        u = min(unc, key=lambda x: len(by[x]))
        for S_ in by[u]:
            if S_ <= unc:
                sol.append(S_); r = rec(unc - S_)
                if r: return r
                sol.pop()
        return None
    return rec(frozenset(universe))

for Lm_, label in ((Lm, 'scaled (Lm=lcm(1..40), as in the proof)'), (1, 'UNscaled (Lm=1)')):
    random.seed(11)
    pats = {}
    for c, V in natural.values():
        if len(V) == 4 and not meets_diag(c, V):
            p = pattern(c, V, Lm_); 
            if p: pats.setdefault(p, (c, V))
    tries = 0
    while tries < 6000:
        tries += 1
        V = rand_laminar(random.choice([3, 4, 4]))
        if V is None: continue
        c = [random.randint(1, 4) for _ in range(4)]
        p = pattern(c, V, Lm_)
        if not p or p in pats: continue
        if meets_diag(c, V, 18): continue
        pats[p] = (c, V)
    halfplanes = sum(1 for p in pats if any(p == {d for d in deltas if a*d[0]+b*d[1] > 0}
                                           for a in range(-9, 10) for b in range(-9, 10)))
    print(f'--- {label}: distinct non-empty window patterns of diagonal-free laminar sets: {len(pats)}; '
          f'of which open half-planes through 0: {halfplanes}')
    sol = exact_cover(deltas, list(pats))
    if sol:
        print('  EXACT COVER of window found with', len(sol), 'sets:')
        for p in sol: print('   ', pats[p], sorted(p))
    else:
        print('  no exact (ply-1) cover of the window exists from this pool')
