# Near-constant family (Omega = R*1, D = all maximal divisors).
# Structures: NC perfect matchings (n even) or NC matchings of n-1 points + one singleton (n odd).
import sys, random, json
from arr2 import *

def structure_stream(n, rng):
    while True:
        if n % 2 == 0:
            yield random_nc_matching_points(list(range(n)), rng)
        else:
            k = rng.randrange(n)
            pts = [i for i in range(n) if i != k]
            # NC matching of remaining points (as a sequence on the line; crossing is about line order)
            yield random_nc_matching_points(pts, rng) + [(k,)]

if __name__ == '__main__':
    n = int(sys.argv[1]); maxsteps = int(sys.argv[2]); seed = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    ds = max_divs(n)
    rng = random.Random(seed)
    gen = structure_stream(n, rng)
    structs = [next(gen) for _ in range(maxsteps)]
    Fp = Field(2**31 - 1)
    ok, used, fam = run(Fp, n, ds, structs)
    print('n', n, 'ds', ds, 'mod-p: died' if ok else 'mod-p: SURVIVED', 'structures used', len(used))
    if ok:
        Fq = Field(None)
        ok2, used2, fam2 = run(Fq, n, ds, used)
        print('   exact rational verification with', len(used), 'structures:', 'died (no hard delta)' if ok2 else 'SURVIVED')
        with open(f'cert_nearconst_{n}.json', 'w') as f:
            json.dump({'n': n, 'ds': ds, 'structures': used, 'exact_died': ok2}, f)
    else:
        print('   surviving subspaces dims', sorted(len(U.basis) for U in fam.values()))
