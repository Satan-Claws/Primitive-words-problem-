"""Which words are NOT in Q.Q (product of two primitive words)?  Exhaustive for n <= 16."""
import itertools
def primitive(w):
    return len(w) > 0 and (w + w).find(w, 1) == len(w)
for n in range(1, 17):
    miss = []
    for t in itertools.product('ab', repeat=n):
        w = ''.join(t)
        if not any(primitive(w[:i]) and primitive(w[i:]) for i in range(1, n)):
            miss.append(w)
    print(n, miss if len(miss) < 8 else (len(miss), miss[:8]))
