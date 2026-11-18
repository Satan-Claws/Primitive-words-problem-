# Necklace-level test of D (mirror dominance) closed under the decodings
#   cyclic word with no 'bb': a->x, ab->y   ;  no 'aa': b->x, ba->y  (Sturmian-type codes)
import sys
from common import *
from fold import inD
from collections import Counter

def cyc_has(w, x, y):
    n = len(w)
    return any(w[i] == x and w[(i + 1) % n] == y for i in range(n))

def decode(w, big):
    # w cyclic, no 'big big' factor, contains big. small letter = 1-big.
    # Rotate so that w starts with big... parse blocks: (small) big? each 'big' preceded by small.
    small = 1 - big
    n = len(w)
    # rotate to start right after a 'big' letter (so every block small[big] starts at small)
    k = next(i for i in range(n) if w[i] == big)
    r = w[k + 1:] + w[:k + 1]
    out = []; i = 0
    while i < n:
        assert r[i] == small
        if i + 1 < n and r[i + 1] == big:
            out.append(1); i += 2
        else:
            out.append(0); i += 1
    return tuple(out)

def depth(w, memo={}):
    if w in memo: return memo[w]
    n = len(w)
    if any(inD(r) for r in rotations(w)):
        res = 0
    elif 0 in w and 1 in w and not cyc_has(w, 1, 1):
        res = 1 + depth(decode(w, 1))
    elif 0 in w and 1 in w and not cyc_has(w, 0, 0):
        res = 1 + depth(decode(w, 0))
    else:
        res = float('inf')
    memo[w] = res
    return res

if __name__ == '__main__':
    N = int(sys.argv[1])
    for n in range(2, N + 1):
        c = Counter(); ex = {}
        for w in lyndon(n):
            d = depth(w); c[d] += 1; ex.setdefault(d, s(w))
        print(n, dict(c), {k: v for k, v in ex.items() if k != 0})
