"""Scout experiment: do primitive words always admit a NON-CROSSING family of
"mismatch witnesses", one per prime p | n?

For w in {a,b}^n and prime p | n, a p-witness is a pair (i, i+n/p), 0 <= i < n - n/p,
with w[i] != w[i+n/p].  w is primitive iff it has a p-witness for every prime p | n.
Two pairs (a,b),(c,d) with a<b, c<d CROSS iff a<c<b<d or c<a<d<b (shared endpoints allowed).

If every primitive word has a pairwise non-crossing witness family, then (see report)
Q ∩ {a,b}^n has a CFG with n^{2+o(1)} productions, which kills slice-size lower bounds.

Usage: python3 -I laminar_witness.py N1 N2 ...   (exhaustive over all 2^n words)
       python3 -I laminar_witness.py --sample N TRIALS SEED   (random abelian-hard words)
"""
import sys, itertools, random

def primes_dividing(n):
    ps, m, d = [], n, 2
    while d * d <= m:
        if m % d == 0:
            ps.append(d)
            while m % d == 0:
                m //= d
        d += 1
    if m > 1:
        ps.append(m)
    return ps

def crosses(x, y):
    a, b = x; c, d = y
    return (a < c < b < d) or (c < a < d < b)

MULT = False   # allow distances j*n/p, 1<=j<p
COUNT = False  # allow letter-count witness (p does not divide |w|_a)

def has_laminar_family(w, n, ps):
    wit = []
    na = sum(1 for x in w if x == 0)
    prim = True
    for p in ps:
        d = n // p
        if any(w[i] != w[i + d] for i in range(n - d)) is False:
            return None  # not primitive
    for p in ps:
        d = n // p
        if COUNT and na % p != 0:
            wit.append(['COUNT'])
            continue
        js = range(1, p) if MULT else [1]
        lst = [(i, i + j * d) for j in js for i in range(n - j * d) if w[i] != w[i + j * d]]
        wit.append(lst)
    # backtracking, smallest lists first
    order = sorted(range(len(ps)), key=lambda k: len(wit[k]))
    chosen = []
    def bt(k):
        if k == len(order):
            return True
        for pr in wit[order[k]]:
            if pr == 'COUNT' or all(q == 'COUNT' or not crosses(pr, q) for q in chosen):
                chosen.append(pr)
                if bt(k + 1):
                    return True
                chosen.pop()
        return False
    return bt(0)

def exhaustive(n):
    ps = primes_dividing(n)
    nprim = nfail = 0
    first_fail = None
    for bits in range(1 << n):
        w = [(bits >> i) & 1 for i in range(n)]
        r = has_laminar_family(w, n, ps)
        if r is None:
            continue
        nprim += 1
        if not r:
            nfail += 1
            if first_fail is None:
                first_fail = ''.join('ab'[x] for x in w)
    print(f'n={n} primes={ps} primitive={nprim} no-laminar-family={nfail} example={first_fail}', flush=True)

def sample(n, trials, seed):
    """Random words that are abelian p-th powers for every prime p | n
    (i.e. |w|_a divisible by every p | n) -- the 'hard' words; we sample by
    shuffling a fixed multiset of letters with |w|_a = rad(n)*k."""
    rnd = random.Random(seed)
    ps = primes_dividing(n)
    rad = 1
    for p in ps:
        rad *= p
    counts = [c for c in range(rad, n, rad)]
    nprim = nfail = 0
    ex = None
    for _ in range(trials):
        ca = rnd.choice(counts)
        w = [0] * ca + [1] * (n - ca)
        rnd.shuffle(w)
        r = has_laminar_family(w, n, ps)
        if r is None:
            continue
        nprim += 1
        if not r:
            nfail += 1
            if ex is None:
                ex = ''.join('ab'[x] for x in w)
    print(f'[sample] n={n} primes={ps} primitive={nprim} no-laminar-family={nfail} example={ex}', flush=True)

if __name__ == '__main__':
    if sys.argv[1] == '--mult':
        MULT = True; sys.argv.pop(1)
    if sys.argv[1] == '--count':
        COUNT = True; sys.argv.pop(1)
    if sys.argv[1] == '--sample':
        sample(int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
    else:
        for a in sys.argv[1:]:
            exhaustive(int(a))
