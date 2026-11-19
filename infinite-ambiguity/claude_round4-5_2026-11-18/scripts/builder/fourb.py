# Words with exactly K b's, given by cyclic gap vector (g1..gK) = numbers of a's between consecutive b's.
# Which ones are missed by Cyc(D2)?
import sys, itertools
from common import *
from fold2 import inD2

def word(g):
    w = []
    for x in g: w += [1] + [0] * x
    return tuple(w)

def canon(g):
    return min(g[i:] + g[:i] for i in range(len(g)))

K, N = int(sys.argv[1]), int(sys.argv[2])
for n in range(K, N + 1):
    seen = set(); miss = []
    for g in itertools.product(range(n - K + 1), repeat=K - 1):
        last = n - K - sum(g)
        if last < 0: continue
        g = canon(tuple(g) + (last,))
        if g in seen: continue
        seen.add(g)
        w = word(g)
        if not is_primitive(w): continue
        if not any(inD2(r) for r in rotations(w)):
            miss.append(g)
    print(n, len(miss), miss[:12], flush=True)
