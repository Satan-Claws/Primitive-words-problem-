"""construct_k3.py -- vectorised 3-chord dominance atoms for n=30; test them on the 60 uncovered sparse vectors.
usage: python construct_k3.py  (reads uncovered list produced by construct_cover30.py)"""
import itertools, sys, pickle, os, numpy as np
from construct_atoms import *
n = 30; primes = [2, 3, 5]; A = {2: 15, 3: 10, 5: 6}
S = Setup(n, primes); PR = frozenset(primes)
comb = np.array(list(itertools.combinations(range(n), 6)), dtype=np.int16)
shapes = [tuple(m) for m in matchings(3)]
def cert_mask(sh):
    """returns dict p -> bool array (some eps with balanced signed sum)."""
    out = {p: np.zeros(len(comb), bool) for p in primes}
    for eps in itertools.product((1, -1), repeat=2):
        eps = (1,) + eps
        sgn = np.zeros(6, int)
        for (a, b), e in zip(sh, eps): sgn[b] += e; sgn[a] -= e
        for p in primes:
            res = comb % A[p]; ok = np.ones(len(comb), bool)
            for r in range(A[p]):
                ok &= ((res == r) * sgn).sum(1) == 0
            out[p] |= ok
    return out
CM = {sh: cert_mask(sh) for sh in shapes}
def holds_vec(x, sh):
    dom, _ = allowed_dominants(sh)
    X = x[comb]
    d = np.stack([X[:, b] - X[:, a] for a, b in sh], 1)
    tot = np.abs(d).sum(1); h = np.zeros(len(comb), bool)
    for j, sg in dom: h |= sg*d[:, j] > tot - np.abs(d[:, j])
    return h
def atoms3_at(x, want=None):
    out = []
    for sh in shapes:
        h = holds_vec(x, sh)
        if not h.any(): continue
        for i in np.nonzero(h)[0]:
            C = frozenset(p for p in primes if CM[sh][p][i])
            if C and (want is None or want(C)):
                pts = tuple(int(v) for v in comb[i]); out.append((pts, sh, atom_pairs(pts, sh), C))
    return out
if __name__ == '__main__':
    import construct_cover30 as cc
    unc = pickle.load(open(sys.argv[1], 'rb'))
    full = [sh for sh in shapes]
    tot3 = {sh: int(np.all([CM[sh][p] for p in primes], 0).sum()) for sh in shapes}
    print('3-chord atoms certifying {2,3,5} per shape:', tot3)
    still = []
    for u in unc:
        x = np.array(u)
        A3 = atoms3_at(x, want=lambda C: len(C) >= 2)
        ok = any(a[3] == PR for a in A3)
        if not ok:
            H = cc.holds_all(x) + A3
            for a in A3:
                miss = next(iter(PR - a[3]))
                if any(miss in b[3] and compatible(a, b) for b in H): ok = True; break
        if not ok: still.append(u)
    print('uncovered after 3-chord atoms:', len(still), 'of', len(unc))
    pickle.dump(still, open(sys.argv[2], 'wb'))
