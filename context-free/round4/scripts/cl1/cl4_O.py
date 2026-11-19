"""Level-set certificate C_O^B (Lemma O of builder2.md at block level, bounded count):
w in (a*b)^+ with block vector x (length K) is certified iff for SOME reflection rho(i) = c - i of Z_K,
s := #{i : x_i - x_{rho i} = +1} satisfies 1 <= s <= B and gcd(s, K) = 1.
(Cyc of a linear CFL with finite control: count capped at B, K mod lcm(1..B); both fold types.)
Checks: soundness exhaustive to length NMAX; coverage of J = a.u.u random, and of phi(T)."""
import itertools, random
from math import gcd
from refute import primitive, blocks
B = 7
def cert(x):
    K = len(x)
    for c in range(K):
        s = sum(1 for i in range(K) if x[i] - x[(c - i) % K] == 1)
        if 1 <= s <= B and gcd(s, K) == 1: return True
    return False
NMAX = 18; cnt = 0
for n in range(1, NMAX + 1):
    for t in itertools.product('ab', repeat=n):
        w = ''.join(t); x = blocks(w)
        if x and cert(x):
            cnt += 1; assert primitive(w), w
print(f'C_O^{B}: {cnt} certified words up to length {NMAX}, all primitive')
rnd = random.Random(5)
for lo, hi in [(0, 30), (0, 8), (0, 2), (1, 2)]:
    for l in (5, 10, 20):
        cov = 0
        for _ in range(200):
            c = [rnd.randint(lo, hi) for _ in range(l)]
            x = c + c; x[0] += 1; cov += cert(x)
        print(f'J, block lengths in [{lo},{hi}], {l} blocks/period: covered {cov}/200')
