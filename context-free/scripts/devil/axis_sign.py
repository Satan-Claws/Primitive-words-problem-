"""
Test the "axis sign-pattern" certificate for primitive integer sequences.

x in N^n (indices mod n).  For an axis s in Z_n let sigma^s_i = sign(x_{s-i} - x_i).
If x has period d (d | n) then sigma^s has period d (proved in report).
Certificate: exists s such that sigma^s is not (n/p)-periodic for every prime p | n.
Question: is the certificate COMPLETE, i.e. does every primitive x have one?

Only the weak order type of x matters, so we enumerate x in {0..K}^n.
Usage: python3 axis_sign.py n K   (exhaustive)   or  python3 axis_sign.py n K rand N
"""
import sys, itertools, random
from sympy import primefactors

def periodic(v, d):
    n = len(v)
    return all(v[i] == v[(i + d) % n] for i in range(n))

def primitive(v):
    n = len(v)
    return not any(periodic(v, n // p) for p in primefactors(n))

def sig(x, s):
    n = len(x)
    out = []
    for i in range(n):
        a, b = x[(s - i) % n], x[i]
        out.append((a > b) - (a < b))
    return tuple(out)

def certified(x, ds):
    n = len(x)
    for s in range(n):
        g = sig(x, s)
        if not any(periodic(g, d) for d in ds):
            return s
    return None

def main():
    n = int(sys.argv[1]); K = int(sys.argv[2])
    ds = [n // p for p in primefactors(n)]
    bad = []
    if len(sys.argv) > 3 and sys.argv[3] == 'rand':
        N = int(sys.argv[4]); rng = random.Random(1)
        it = (tuple(rng.randint(0, K) for _ in range(n)) for _ in range(N))
    else:
        it = itertools.product(range(K + 1), repeat=n)
    cnt = 0
    for x in it:
        if not primitive(x):
            continue
        cnt += 1
        if certified(x, ds) is None:
            bad.append(x)
            if len(bad) <= 10:
                print("UNCERTIFIED primitive:", x)
    print(f"n={n} K={K}: primitive tested={cnt}, uncertified={len(bad)}")

if __name__ == '__main__':
    main()
