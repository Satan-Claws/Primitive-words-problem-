"""construct2_random.py -- random primitive W_30 points (sums of random polygon indicators, random
multiplicities, plus random copies of the exotic 6-term sum e5+e6+e12+e18+e24+e25 rotated) and of
fibre-perturbed points (fibre pattern + small W-noise): coverage by dom (k<=2) / + transfer atoms.
usage: python construct2_random.py TRIALS SEED"""
import sys, random, numpy as np
import construct2_cover as C
n = 30; rng = random.Random(int(sys.argv[2]) if len(sys.argv) > 2 else 0)
EX = np.zeros(n, int); EX[[5, 6, 12, 18, 24, 25]] = 1
def poly(d, r): v = np.zeros(n, int); v[r::d] = 1; return v
def rand_W(kind):
    x = np.zeros(n, int)
    if kind == 'fibre':
        r0 = rng.randrange(5); y = [rng.randint(0, 4) for _ in range(6)]
        # make y in W_6: add 2- and 3-periodic parts only
        a = [rng.randint(0, 3) for _ in range(3)]; b = [rng.randint(0, 3) for _ in range(2)]
        for t in range(6): x[(r0+5*t) % n] = a[t % 3] + b[t % 2]
        for _ in range(rng.randint(0, 2)):
            x += poly(rng.choice((15, 10, 6)), rng.randrange(30) % 6)  # small off-fibre noise
        return x
    for _ in range(rng.randint(2, 9)):
        d = rng.choice((15, 10, 6)); x += rng.randint(1, 3) * poly(d, rng.randrange(d))
    if kind == 'exotic':
        for _ in range(rng.randint(1, 2)): x += np.roll(EX, rng.randrange(n))
    return x
if __name__ == '__main__':
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    stats = {}
    for kind in ('generic', 'exotic', 'fibre'):
        tot = 0; res = {}
        while tot < N:
            x = rand_W(kind)
            if not C.cc.S.inE(x): continue
            tot += 1; r = C.covered(list(int(v) for v in x)); res[r] = res.get(r, 0) + 1
            if r is None: print('UNCOVERED', kind, list(x))
        print(kind, N, res, flush=True)
