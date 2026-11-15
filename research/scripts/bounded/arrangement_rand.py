import sys, random
from arrangement import *

def random_nc_matching(n, rng):
    # uniform random Dyck word via cycle lemma
    m = n//2
    while True:
        s = [1]*m + [-1]*(m+1)
        rng.shuffle(s)
        # cycle lemma: rotate so that all partial sums >0 ... find rotation
        tot = 0; mn = 0; mi = 0
        for i, x in enumerate(s):
            tot += x
            if tot < mn:
                mn = tot; mi = i+1
        s = s[mi:] + s[:mi]
        s = s[:-1]  # drop final -1
        break
    stack = []; M = []
    for i, x in enumerate(s):
        if x == 1: stack.append(i)
        else: M.append((stack.pop(), i))
    return M

def run_rand(n, steps, seed=0):
    rng = random.Random(seed)
    ps = primes_of(n)
    ds = [n//p for p in ps]
    Vp = {d: Vd_perp(n, d) for d in ds}
    fam = {(): Sub([], n)}
    for t in range(steps):
        M = random_nc_matching(n, rng)
        Wp = [W_perp(n, M, d) for d in ds]
        new = {}
        for key, U in fam.items():
            if any(contained_in(U.basis, w) for w in Wp):
                new[key] = U; continue
            for w in Wp:
                V = Sub(U.cons + w, n)
                if any(contained_in(V.basis, Vp[d]) for d in ds):
                    continue
                new[V.key] = V
        items = list(new.values())
        keep = {}
        for U in items:
            if not any(U2 is not U and len(U2.basis) > len(U.basis) and contained_in(U.basis, U2.cons) for U2 in items):
                keep[U.key] = U
        fam = keep
        if t % 20 == 0 or not fam:
            print(t, len(fam), sorted(len(U.basis) for U in fam.values())[:12], flush=True)
        if not fam:
            break
    return fam

if __name__ == '__main__':
    n = int(sys.argv[1]); steps = int(sys.argv[2])
    fam = run_rand(n, steps)
    print('surviving', len(fam))
