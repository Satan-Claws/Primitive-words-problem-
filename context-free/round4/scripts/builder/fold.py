# Candidate D ("mirror dominance"): w in D iff  w_i <= w_{n-1-i} for all i < n/2, with strict for some i.
# (a=0 < b=1).  Sound claim: D subset of Q.  Test soundness on all words and completeness on necklaces.
import sys
from common import *

def inD(w):
    n = len(w); strict = False
    for i in range(n // 2):
        x, y = w[i], w[n - 1 - i]
        if x > y: return False
        if x < y: strict = True
    return strict

if __name__ == '__main__':
    N = int(sys.argv[1])
    for n in range(1, N + 1):
        if n <= 16:
            bad = [w for w in all_words(n) if inD(w) and not is_primitive(w)]
            assert not bad, (n, s(bad[0]))
        miss = [w for w in lyndon(n) if not any(inD(r) for r in rotations(w))]
        print(n, 'missed necklaces:', len(miss), [s(m) for m in miss[:6]])
