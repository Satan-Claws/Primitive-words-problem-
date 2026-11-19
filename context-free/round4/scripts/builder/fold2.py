# Candidate D2: dominance w.r.t. ANY reflection of the cycle.
#   type E (edge axis):  w_i <= w_{n-1-i}, i < n/2            (= fold.inD)
#   type V (vertex axis, n even): w_i <= w_{n-i}, 1 <= i < n/2 (w_0, w_{n/2} free)
# strict somewhere.  Rotations taken in the harness.  Grammar: S -> X Y | Y,  Y -> a Y a | b Y b | a Z b | X | eps,
# Z -> a Z a | b Z b | a Z b | X | eps  (Y: still no strict pair seen; Z: strict seen).  See report.
import sys
from common import *

def dom(pairs):
    strict = False
    for x, y in pairs:
        if x > y: return False
        if x < y: strict = True
    return strict

def inD2(w):
    n = len(w)
    if dom((w[i], w[n - 1 - i]) for i in range(n // 2)): return True
    if n % 2 == 0 and dom((w[i], w[n - i]) for i in range(1, n // 2)): return True
    return False

if __name__ == '__main__':
    N = int(sys.argv[1])
    for n in range(1, N + 1):
        if n <= 16:
            bad = [w for w in all_words(n) if inD2(w) and not is_primitive(w)]
            assert not bad, (n, s(bad[0]))
        miss = [w for w in lyndon(n) if not any(inD2(r) for r in rotations(w))]
        print(n, 'missed:', len(miss), [s(m) for m in miss[:8]], flush=True)
