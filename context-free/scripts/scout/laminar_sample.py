"""Random sampling for laminar_witness (scout). Words of length n with |w|_a = c,
c chosen to be divisible by as many primes p|n as possible (the hardest case).
usage: python3 -I laminar_sample.py n trials seed [--mult] [--count] [--nearperiodic]
--nearperiodic: start from a random (n/p)-periodic word for a random p|n and flip/move few letters
"""
import sys, random, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import laminar_witness as L

def main():
    n, trials, seed = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    L.MULT = '--mult' in sys.argv
    L.COUNT = '--count' in sys.argv
    near = '--nearperiodic' in sys.argv
    rnd = random.Random(seed)
    ps = L.primes_dividing(n)
    best = max(range(1, n), key=lambda c: (sum(1 for p in ps if c % p == 0), -abs(c - n // 2)))
    cands = [c for c in range(1, n) if sum(1 for p in ps if c % p == 0) == sum(1 for p in ps if best % p == 0)]
    nprim = nfail = 0; ex = None
    for _ in range(trials):
        if near:
            # product-of-periodic-structure: w = u^p with swaps of a letters (keeps |w|_a)
            p = rnd.choice(ps); d = n // p
            c = rnd.choice(cands)
            # build periodic word with roughly c a's then adjust by swaps
            u = [0] * (c // p) + [1] * (d - c // p) if c % p == 0 else None
            if u is None:
                w = [0] * c + [1] * (n - c); rnd.shuffle(w)
            else:
                rnd.shuffle(u); w = u * p
                for _k in range(rnd.randint(1, 3)):
                    i, j = rnd.randrange(n), rnd.randrange(n)
                    w[i], w[j] = w[j], w[i]
        else:
            c = rnd.choice(cands)
            w = [0] * c + [1] * (n - c); rnd.shuffle(w)
        r = L.has_laminar_family(w, n, ps)
        if r is None: continue
        nprim += 1
        if not r:
            nfail += 1
            if ex is None: ex = ''.join('ab'[x] for x in w)
    print(f'n={n} primes={ps} counts={cands[:6]}.. mult={L.MULT} count={L.COUNT} near={near} primitive={nprim} fail={nfail} ex={ex}', flush=True)

main()
