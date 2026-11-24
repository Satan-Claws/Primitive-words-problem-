"""construct_cover30.py -- coverage test of E ∩ W_30 by laminar certificate systems (atoms of construct_atoms).
usage: python construct_cover30.py [kmax]"""
import sys, itertools, random, pickle, os, numpy as np
from construct_atoms import *
S = Setup(30, [2, 3, 5]); P = frozenset(S.primes)
kmax = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 2
cache = f'/tmp/atoms30_k{kmax}.pkl' if False else None
ATOMS = enumerate_atoms(S, kmax)
print('atoms', len(ATOMS), {k: sum(1 for a in ATOMS if len(a[1]) == k) for k in range(1, kmax+1)})
# vectorised data per atom
def holds_all(x):
    return [a for a in ATOMS if atom_holds(x, a[0], a[1])]

def systems(x, stop=False):
    H = holds_all(x); found = []
    for a in H:
        if a[3] == P: found.append((a,));  
        if stop and found: return found
    two = [a for a in H if len(a[3]) == 2]; one = [a for a in H if len(a[3]) >= 1]
    for a in two:
        miss = next(iter(P - a[3]))
        for b in one:
            if miss in b[3] and compatible(a, b):
                found.append((a, b))
                if stop: return found
    single = {p: [a for a in H if a[3] == frozenset([p])] for p in S.primes}
    for a in single[2]:
        for b in single[3]:
            if not compatible(a, b): continue
            for c in single[5]:
                if compatible(a, c) and compatible(b, c):
                    found.append((a, b, c))
                    if stop: return found
    return found

def sparse_vectors():
    def sub(L, k): return [s for j in range(k+1) for s in itertools.combinations(range(L), j)]
    def vec(L, s): return [1 if t in s else 0 for t in range(L)]
    seen = set()
    for ks in ((2, 1, 1), (1, 2, 1), (1, 1, 2)):
        for sa in sub(15, ks[0]):
            for sb in sub(10, ks[1]):
                for sc in sub(6, ks[2]):
                    x = S.W({2: vec(15, sa), 3: vec(10, sb), 5: vec(6, sc)})
                    t = tuple(x)
                    if t in seen or not S.inE(x): continue
                    seen.add(t); yield x

if __name__ == '__main__':
    unc = []; tot = 0
    for x in sparse_vectors():
        tot += 1
        if not systems(x, stop=True): unc.append(tuple(int(v) for v in x))
    print('sparse W30 primitive', tot, 'uncovered', len(unc))
    for u in unc[:10]: print(' ', [i for i in range(30) for _ in range(u[i])])
    pickle.dump(unc, open(os.environ.get('OUT','unc.pkl'), 'wb'))
