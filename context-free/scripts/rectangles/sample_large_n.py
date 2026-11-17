"""Sampling sanity checks of the affine-cover theorem for n with many prime factors.

For n in {30, 210, 2310, 30030} (omega = 3,4,5,6) we check, with random test tuples
s_p = r + rot(r, n/p) in S_p:
  (1) KEY LEMMA: <u^p, s_p> = 0 for random p-th powers u^p (so T never contains a power);
  (2) Pr[w in T] = 2^{-k} for several word families in Q_n, including the 'hard'
      ones (abelian p-th powers for every p | n that are primitive), e.g.
        - u^{n/e} with one a<->b transposition inside one block (letter counts kept),
        - single-flip near powers,
        - uniformly random words.
Python ints are used as bit vectors (bit j = letter at position j, b = 1).
"""
import random, math, sys
from common import prime_factors, is_primitive_int


def rotl(w, d, n):
    mask = (1 << n) - 1
    return ((w >> d) | (w << (n - d))) & mask


def power(u, e, m):
    w = 0
    for i in range(m):
        w |= u << (i * e)
    return w


def par(x):
    return bin(x).count("1") & 1


def draw_tuple(n, rnd):
    return {p: (lambda r: r ^ rotl(r, n // p, n))(rnd.getrandbits(n)) for p in prime_factors(n)}


def families(n, rnd):
    ps = prime_factors(n)
    rad = math.prod(ps)
    e = n // rad if n // rad >= 2 else 2 * (n // rad)
    # ensure e | n
    while n % e:
        e += 1
    fam = {}
    # (a) transposition-perturbed powers (abelian power for every p, not a power)
    def transp():
        while True:
            u = rnd.getrandbits(e)
            w = power(u, e, n // e)
            # swap an a and a b inside the first block (keeps every block-of-length-n/p Parikh vector)
            i, j = rnd.randrange(e), rnd.randrange(e)
            if ((w >> i) & 1) != ((w >> j) & 1):
                w ^= (1 << i) | (1 << j)
                if is_primitive_int(w, n):
                    return w
    fam["transposed power (abelian power, primitive)"] = transp
    def flip():
        while True:
            p = rnd.choice(ps)
            u = rnd.getrandbits(n // p)
            w = power(u, n // p, p) ^ (1 << rnd.randrange(n))
            if is_primitive_int(w, n):
                return w
    fam["single-flip near power"] = flip
    def unif():
        while True:
            w = rnd.getrandbits(n)
            if is_primitive_int(w, n):
                return w
    fam["uniform primitive"] = unif
    return fam


def main(ns=(30, 210, 2310, 30030), trials=4000):
    rnd = random.Random(2026)
    for n in ns:
        ps = prime_factors(n)
        k = len(ps)
        # (1) key lemma
        bad = 0
        for _ in range(trials):
            tup = draw_tuple(n, rnd)
            p = rnd.choice(ps)
            u = rnd.getrandbits(n // p)
            w = power(u, n // p, p)
            if par(w & tup[p]):
                bad += 1
        print(f"n={n} k={k}: powers u^p with <u^p,s_p>=1 : {bad}/{trials} (must be 0)")
        for name, gen in families(n, rnd).items():
            hit = 0
            for _ in range(trials):
                w = gen()
                tup = draw_tuple(n, rnd)
                if all(par(w & s) for s in tup.values()):
                    hit += 1
            print(f"    {name:45s} Pr[w in T] = {hit/trials:.4f}   (2^-k = {2**-k:.4f})")


if __name__ == "__main__":
    main()
