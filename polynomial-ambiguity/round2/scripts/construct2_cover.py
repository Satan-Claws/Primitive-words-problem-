"""construct2_cover.py -- coverage of primitive W_30 points (dihedral classes, |x|_1<=N) and of the 60 sparse
vectors by (i) chord-dominance atoms k<=2 (construct_atoms), (ii) + transfer atoms (construct2_transfer).
usage: python construct2_cover.py W30_N8.npy"""
import sys, numpy as np, itertools
import construct_cover30 as cc, construct2_transfer as T
def dom_atoms(x):
    return [(frozenset(a[0]), [tuple(sorted(p)) for p in a[2]], frozenset(a[3]), ('D',) + tuple(a[0])) for a in cc.holds_all(x)]
def covered(x, use_T=True):
    ats = dom_atoms(x)
    if T.find_systems(ats): return 'dom'
    if use_T:
        ats2 = ats + T.transfer_atoms(list(x))
        if T.find_systems(ats2): return 'transfer'
    return None
def fibre_supported(x):
    S = [i for i in range(30) if x[i]]
    return len({i % 5 for i in S}) == 1
if __name__ == '__main__':
    X = np.load(sys.argv[1])
    res = {}
    unc = []
    for x in X:
        r = covered(list(int(v) for v in x)); res[r] = res.get(r, 0) + 1
        if r is None: unc.append(x)
    print('classes', len(X), res)
    for u in unc: print(' uncovered', [i for i in range(30) for _ in range(u[i])], 'fibre-supp', fibre_supported(u))
    np.save(sys.argv[1].replace('.npy', '_unc.npy'), np.array(unc))
