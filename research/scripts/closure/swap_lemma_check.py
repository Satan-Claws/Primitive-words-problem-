"""Exhaustive check of the Swap Lemma (Lemma W in reports/closure.md).

Lemma W: if |x| = |y|, x != y and 6|x| <= |Yx|, then Yx or Yy is primitive.

We check it exhaustively over {a,b} for |Yx| <= NMAX, and we also report, for each
window length k = |x|, the largest total length n at which a counterexample
(Yx, Yy both non-primitive) exists, to see how sharp the constant 6 is.
"""
import itertools, sys

def primitive(w):
    n = len(w)
    if n == 0:
        return False
    return (w + w).find(w, 1) == n

NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 18

def words(k):
    for t in itertools.product('ab', repeat=k):
        yield ''.join(t)

# Precompute non-primitive words by length, then look for pairs with common prefix Y
violations = 0
worst = {}  # k -> max n with a counterexample
for n in range(1, NMAX + 1):
    nonprim = [w for w in words(n) if not primitive(w)]
    for k in range(1, n + 1):
        groups = {}
        for w in nonprim:
            groups.setdefault(w[:n - k], set()).add(w[n - k:])
        bad = any(len(s) >= 2 for s in groups.values())
        if bad:
            worst[k] = max(worst.get(k, 0), n)
            if 6 * k <= n:
                violations += 1
                print('VIOLATION', n, k)
print('violations of Lemma W for n <=', NMAX, ':', violations)
print('k -> largest n (<= NMAX) with Yx, Yy both non-primitive (x != y, |x|=|y|=k):')
for k in sorted(worst):
    print(' ', k, worst[k], ' ratio n/k =', round(worst[k] / k, 2))
