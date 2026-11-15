"""Exhaustive laminar-witness check over all words of length n with at most K letters b (scout).
usage: python3 -I laminar_lowweight.py n K [--mult] [--count]"""
import sys, os, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import laminar_witness as L
n, K = int(sys.argv[1]), int(sys.argv[2])
L.MULT = '--mult' in sys.argv; L.COUNT = '--count' in sys.argv
ps = L.primes_dividing(n)
tot = fail = 0; ex = None
for k in range(1, K + 1):
    for pos in itertools.combinations(range(n), k):
        w = [0] * n
        for i in pos: w[i] = 1
        r = L.has_laminar_family(w, n, ps)
        if r is None: continue
        tot += 1
        if not r:
            fail += 1
            if ex is None: ex = ''.join('ab'[x] for x in w)
print(f'n={n} primes={ps} weight<={K} mult={L.MULT} count={L.COUNT} primitive={tot} fail={fail} ex={ex}', flush=True)
