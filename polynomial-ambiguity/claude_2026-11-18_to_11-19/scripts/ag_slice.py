"""Task A: witness-union grammars for Q_n = Q ∩ (ab*)^n (n fixed).
A witness for prime p|n is a block pair (i, i+n/p) with e_i != e_{i+n/p}.  A system = one witness per
prime p|n; it is realizable by a CFG gadget (nested b^x [..] b^y, x!=y, unique parse) iff the pairs are
laminar: pairwise disjoint or strictly nested, all endpoints distinct.  Grammar G_n = union over laminar
systems; amb_{G_n}(w) = #valid laminar systems for e(w) (independent of the exponent sizes).
L(G_n) = Q_n iff every primitive exponent vector has >= 1 laminar system.
Enumerates exponent vectors over V values (only the equality pattern matters)."""
import sys, itertools
from math import gcd

def primes(n): return [p for p in range(2, n + 1) if n % p == 0 and all(p % q for q in range(2, p))]

def prim_seq(e):
    n = len(e); return all(e != e[:n // p] * p for p in primes(n))

def laminar(I, J):
    (a, b), (c, d) = I, J
    if len({a, b, c, d}) < 4: return False
    return b < c or d < a or (a < c and d < b) or (c < a and b < d)

MODE = 'adj'
def systems(e):
    n = len(e); P = primes(n)
    if MODE == 'adj':
        W = [[(i, i + n // p) for i in range(n - n // p) if e[i] != e[i + n // p]] for p in P]
    else:  # any pair in one residue class mod n/p (still a valid non-period-(n/p) certificate)
        W = [[(i, j) for i in range(n) for j in range(i + n // p, n, n // p) if e[i] != e[j]] for p in P]
    cnt = 0
    for combo in itertools.product(*W):
        if all(laminar(combo[x], combo[y]) for x in range(len(combo)) for y in range(x)):
            cnt += 1
    return cnt

def canon(e):
    m = {}; return tuple(m.setdefault(x, len(m)) for x in e)

if __name__ == '__main__':
    for n in [int(x) for x in sys.argv[1].split(',')]:
        V = int(sys.argv[2]) if len(sys.argv) > 2 else 3
        MODE = sys.argv[3] if len(sys.argv) > 3 else 'adj'
        seen = set(); fails = []; best = (0, ()); nprim = 0
        for e in itertools.product(range(V), repeat=n):
            c = canon(e)
            if c in seen: continue
            seen.add(c)
            if not prim_seq(list(c)): continue
            nprim += 1
            s = systems(list(c))
            if s == 0: fails.append(c)
            if s > best[0]: best = (s, c)
        print(f"{MODE} n={n} primes={primes(n)} V={V} primitive patterns={nprim} uncovered={len(fails)} "
              f"first_uncovered={[''.join(map(str,f)) for f in fails[:4]]} maxamb={best[0]} at {''.join(map(str,best[1]))}")
