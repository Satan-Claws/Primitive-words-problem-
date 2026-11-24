"""construct2_n12.py -- does adding transfer atoms repair the p^a q^b failure?  n = 12 (g = 2) exhaustive
over {0,1,2,3}^12 ∩ W_12 primitive (W_12 = V_2+V_3), coverage by dom atoms k<=2 vs dom + transfer atoms."""
import itertools, numpy as np
import construct_atoms as CA, construct2_transfer as T
n = 12; T.n = n; T.PR = (2, 3); T.A = {2: 6, 3: 4}
S = CA.Setup(n, [2, 3]); ATOMS = CA.enumerate_atoms(S, 2)
def dom(x): return [(frozenset(a[0]), [tuple(sorted(p)) for p in a[2]], frozenset(a[3]), a) for a in ATOMS if CA.atom_holds(x, a[0], a[1])]
need = frozenset((2, 3)); res = {}; ex = []
for a in itertools.product(range(4), repeat=6):
    for b in itertools.product(range(4), repeat=4):
        x = list(np.tile(a, 2) + np.tile(b, 3))
        if max(x) > 6 or not S.inE(np.array(x)): continue
        if T.find_systems(dom(x), need=need): r = 'dom'
        elif T.find_systems(dom(x) + T.transfer_atoms(x), need=need): r = 'transfer'
        else: r = None; ex.append(x)
        res[r] = res.get(r, 0) + 1
print('n=12, x = a(6-per,0..3)+b(4-per,0..3):', res); print('examples uncovered', ex[:3])
x = [1,2,3,3,1,3,3,2,1,3,3,3]; print('S2K example covered by dom+transfer:', bool(T.find_systems(dom(x) + T.transfer_atoms(x), need=need)))
