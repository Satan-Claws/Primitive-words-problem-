# N_inf = least N with N = E' U T(N)  (= Cyc(L'), L' = E' U sigma(L') U swap sigma(L')).
import sys, itertools, random
sys.path.insert(0, '../walk')
from walk import phi, primitive
def ninf(v, depth=0):
    if abs(sum(v)) == 1: return True, depth
    r = phi(v)
    if r is None or len(r[0]) == len(v): return False, depth
    return ninf(r[0], depth+1)
if sys.argv[1] == 'ex':
    for n in range(1, int(sys.argv[2])+1):
        c = 0; bad = 0; dep = {}
        for v in itertools.product((1, -1), repeat=n):
            ok, d = ninf(v)
            if ok:
                c += 1; dep[d] = dep.get(d, 0)+1
                if not primitive(v): bad += 1
        print(n, c, round(c/2**n, 4), 'nonprim', bad, 'depths', dict(sorted(dep.items())), flush=True)
else:
    random.seed(1)
    for n in map(int, sys.argv[2:]):
        S = 2000 if n < 10**5 else 300
        c = 0; dep = {}; fails = {}
        for _ in range(S):
            v = tuple(random.choice((1, -1)) for _ in range(n))
            ok, d = ninf(v)
            c += ok
            if ok: dep[d] = dep.get(d, 0)+1
        print(n, S, round(c/S, 4), dict(sorted(dep.items())), flush=True)
