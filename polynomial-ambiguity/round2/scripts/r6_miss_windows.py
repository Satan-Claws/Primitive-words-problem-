"""R6 fold windows: which intervals [alpha, beta] (subset of (0, 1/2]) are SOUND fold windows?

Lemma M (r6_miss.md): F_K is sound at length n  <=>  for every prime p | n, K contains some j*n/p, 1 <= j <= p/2.
So a uniform interval window [alpha n, beta n] is sound for all n whose prime divisors lie in P iff
for every p in P the interval [alpha, beta] contains a fraction j/p (1 <= j <= p/2).
For each residue class of n mod 6 (which primes 2, 3 are possible) we find
  (i)  the windows maximising alpha/beta  (the BM no-zero probability (2/pi) asin sqrt(alpha/beta) is increasing in alpha/beta),
  (ii) the shortest windows,
by exact search over Farey endpoints.  Primes p > 1/(beta-alpha) are automatic (gap 1/p).
Usage: python r6_miss_windows.py
"""
from fractions import Fraction as Fr
import math

def primes(a, b):
    return [p for p in range(a, b) if p > 1 and all(p % q for q in range(2, int(p**.5) + 1))]

PB = 400  # endpoints j/p with p < PB; primes checked up to the automatic bound
def pts(p):
    return [Fr(j, p) for j in range(1, p // 2 + 1)]

def ok(al, be, P):
    L = be - al
    if L < 0:
        return False
    bound = math.inf if L == 0 else 1 / float(L) + 1
    for p in P:
        if p > bound:
            break
        if not any(al <= f <= be for f in pts(p)):
            return False
    return True

def search(P):
    cands = sorted({Fr(j, p) for p in range(2, 60) for j in range(1, p // 2 + 1)})
    best_ratio, best_len = None, None
    for i, al in enumerate(cands):
        # minimal beta for this alpha
        for be in cands[i:]:
            if ok(al, be, P):
                r = al / be
                if best_ratio is None or r > best_ratio[0]:
                    best_ratio = (r, al, be)
                if best_len is None or be - al < best_len[0]:
                    best_len = (be - al, al, be)
                break
    return best_ratio, best_len

classes = {
    "n = 0 mod 6 (2,3 | n possible)": [2, 3] + primes(5, 3000),
    "n even, 3 !| n": [2] + primes(5, 3000),
    "n odd, 3 | n": [3] + primes(5, 3000),
    "gcd(n,6)=1": primes(5, 3000),
}
if __name__ == "__main__":
    for name, P in classes.items():
        (r, a, b), (L, a2, b2) = search(P)
        dens = 2 / math.pi * math.asin(math.sqrt(float(r)))
        print(f"{name:34s} max-ratio window [{a},{b}] ratio {float(r):.4f} BM density {dens:.4f} | shortest [{a2},{b2}] len {float(L):.4f}")
    # finite-exception statement: any [al,be] with be-al = L works for all p > 1/L
    print("any interval of length L>0 inside (0,1/2] is sound for every prime p > 1/L; [1/3,1/2] is the unique minimal window sound for ALL n")
    print("BM density of F_K, K=[1/3,1/2]:", round(2 / math.pi * math.asin(math.sqrt(2 / 3)), 4))
