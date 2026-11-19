"""uniform: check that the fixed-size grammar G* = coPow_2 (non-squares) generates exactly
the primitive words of R = a(ab+)* a (ab+)* (union of all slices R_m of the finite-ambiguity proof),
and that G* is infinitely ambiguous already on one slice. Also brute-force the exponent claim for R6.
Exhaustive over all words of R up to length MAXLEN."""
import itertools, re, sys
from functools import lru_cache

MAXLEN = int(sys.argv[1]) if len(sys.argv) > 1 else 20

def primitive(w):
    n = len(w)
    if n == 0: return False
    return all(not (n % d == 0 and w == w[:d] * (n // d)) for d in range(1, n))

R = re.compile(r'^a(ab+)*a(ab+)*$')

# Grammar G* for non-squares (coPow_2):
#   S -> O | A B | B A ;  A -> X A X | a ;  B -> X B X | b ;  X -> a | b ;  O -> X | X X O
# We count derivation trees by memoised recursion over spans.
def count_trees(w):
    n = len(w)
    @lru_cache(None)
    def X(i, j): return 1 if j == i + 1 else 0
    @lru_cache(None)
    def A(i, j, c):   # Sigma^k c Sigma^k on w[i:j]
        L = j - i
        if L % 2 == 0: return 0
        if L == 1: return 1 if w[i] == c else 0
        return A(i + 1, j - 1, c)          # X A X: exactly one way (X fixed length 1)
    @lru_cache(None)
    def O(i, j):
        L = j - i
        if L % 2 == 0: return 0
        if L == 1: return 1
        return O(i + 2, j)                  # O -> X X O
    total = O(0, n)
    for k in range(1, n):
        total += A(0, k, 'a') * A(k, n, 'b') + A(0, k, 'b') * A(k, n, 'a')
    return total

bad = 0; checked = 0; maxamb = {}
for L in range(1, MAXLEN + 1):
    for t in itertools.product('ab', repeat=L):
        w = ''.join(t)
        if not R.match(w): continue
        checked += 1
        c = count_trees(w)
        if (c > 0) != primitive(w):
            bad += 1; print("MISMATCH", w, c)
        # slice size m = number of blocks per half
        m = w[1:].index('aa') + 1 if 'aa' in w[1:] else None
        maxamb[L] = max(maxamb.get(L, 0), c)
print(f"checked {checked} words of R up to length {MAXLEN}; mismatches: {bad}")
print("max #trees of G* per length:", maxamb)
# infinite ambiguity on the single slice R_2 = a(ab+)a(ab+): words a ab^x a ab^y
print("trees on a ab^x a ab^y, x=1, y growing:",
      [count_trees('aab' + 'aab' + 'b' * (y - 1)) for y in range(1, 12)])

# R6 = (a(ab+)+)^6 : every non-primitive word is u^k with k | 6 and k in {2,3,6};
# check both exponents 2 and 3 occur with primitive root (gcd = 1)
R6 = re.compile(r'^(a(ab+)+){6}$')
exps = set(); bad6 = 0
def root_exp(w):
    n = len(w)
    for d in range(1, n + 1):
        if n % d == 0 and w == w[:d] * (n // d): return n // d
for L in range(1, 37):
    pass
# enumerate words of R6 by blocks: z_i has c_i>=1 blocks, exponents small
import random
random.seed(1)
for trial in range(20000):
    zs = []
    base = [[random.randint(1, 2) for _ in range(random.randint(1, 2))] for _ in range(6)]
    mode = random.choice(['free', 'sq', 'cube'])
    if mode == 'sq': base = base[:3] * 2
    if mode == 'cube': base = base[:2] * 3
    w = ''.join('a' + ''.join('a' + 'b' * x for x in z) for z in base)
    assert R6.match(w)
    k = root_exp(w)
    if k > 1:
        exps.add(k)
        if 6 % k: bad6 += 1
print("root exponents seen in R6:", sorted(exps), "violations of k|6:", bad6)
