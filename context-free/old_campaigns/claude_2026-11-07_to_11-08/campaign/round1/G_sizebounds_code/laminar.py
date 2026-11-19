"""Does every primitive word w of length n admit a choice of one mismatch pair
(j, j+n/p), w_j != w_{j+n/p}, 0<=j<j+n/p<n, for each prime p | n, such that the
chosen closed intervals [j, j+n/p] form a laminar family (pairwise nested or
disjoint; touching at an endpoint allowed)?  If yes for all w, Q_n has a CFG of
size poly(n)*2^{omega(n)}.  We report counterexamples.
"""
import sys, itertools

def primes_of(n):
    return [p for p in range(2, n + 1) if n % p == 0 and all(p % q for q in range(2, p))]

def lam_ok(a, b):
    (x1, y1), (x2, y2) = a, b
    if y1 <= x2 or y2 <= x1:
        return True  # disjoint (touching ok)
    if x1 <= x2 and y2 <= y1:
        return True
    if x2 <= x1 and y1 <= y2:
        return True
    return False

def is_prim(w, n, ps):
    return all(w[n // p:] + w[:n // p] != w for p in ps)

def search(cands, chosen):
    if not cands:
        return True
    for iv in cands[0]:
        if all(lam_ok(iv, c) for c in chosen):
            if search(cands[1:], chosen + [iv]):
                return True
    return False

def run(n, alph=2):
    ps = primes_of(n)
    bad = []
    total = 0
    for w in itertools.product(range(alph), repeat=n):
        if not is_prim(w, n, ps):
            continue
        total += 1
        cands = []
        for p in ps:
            d = n // p
            cands.append([(j, j + d) for j in range(n - d) if w[j] != w[j + d]])
        cands.sort(key=len)
        if not search(cands, []):
            bad.append(w)
    return total, bad

if __name__ == "__main__":
    for n in [int(a) for a in sys.argv[1:]]:
        total, bad = run(n)
        print(f"n={n} primes={primes_of(n)} primitive={total} non-laminar={len(bad)}",
              ("e.g. " + "".join(map(str, bad[0]))) if bad else "")
