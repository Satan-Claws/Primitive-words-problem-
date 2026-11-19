import random
from math import gcd
def best(x, vals=(1, 2, 3)):
    K = len(x); bestS = None
    for c in range(K):
        for v in vals:
            s = sum(1 for i in range(K) if x[i] - x[(c - i) % K] == v)
            if s >= 1 and gcd(s, K) == 1 and (bestS is None or s < bestS): bestS = s
    return bestS
rnd = random.Random(11)
for l in (20, 40, 80, 160):
    res = []
    for _ in range(30):
        c = [rnd.randint(1, 2) for _ in range(l)]
        x = c + c; x[0] += 1; res.append(best(x))
    res.sort(key=lambda s: (s is None, s))
    print(f'l={l}: min coprime level-set size over axes, values 1..3 (sorted, 30 samples):', res)
