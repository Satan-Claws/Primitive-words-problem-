# Exhaustive check of Lemma 4.1: in a non-crossing graph on points 0..N-1, two distinct components never interleave.
import itertools
from common import crossing, components
for N in range(2, 9):
    pairs = list(itertools.combinations(range(N), 2))
    count = 0; bad = 0
    # enumerate non-crossing edge sets by backtracking
    def rec(i, chosen):
        global count, bad
        if i == len(pairs):
            count += 1
            comps = components(N, chosen)
            lab = {v: k for k, C in enumerate(comps) for v in C}
            for p, q, r, s in itertools.combinations(range(N), 4):
                if lab[p] == lab[r] and lab[q] == lab[s] and lab[p] != lab[q]:
                    bad += 1; print('VIOLATION', N, chosen); return
            return
        rec(i+1, chosen)
        if all(not crossing(pairs[i], e) for e in chosen):
            rec(i+1, chosen + [pairs[i]])
    rec(0, [])
    print(f'N={N}: non-crossing graphs {count}, violations {bad}')
