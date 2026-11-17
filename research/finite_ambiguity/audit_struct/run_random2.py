# Larger grammars, n in {3,4}; record nontrivial laminarity instances (skeletons with >=2 distinct
# two-element pairs) and formula checks.
import random, sys, itertools
from struct_check import *
rng = random.Random(int(sys.argv[1])); trials = int(sys.argv[2])
stats = {}; okbad = []
for it in range(trials):
    n = rng.choice([3, 4])
    G = rand_grammar(rng, nN=rng.choice([5, 6, 7]), nr=rng.choice([9, 11, 13]))
    B = 3 if n == 3 else 2
    try:
        st, info = analyse(G, 'S', n, B)
    except RecursionError:
        continue
    key = st.split(' ')[0]
    stats[key] = stats.get(key, 0) + 1
    if st == 'ok' and not info['dep']:
        stats['ok_indep'] = stats.get('ok_indep', 0) + 1
        if info['lam_bad'] or info['nmism']: okbad.append((G, n, info))
        P, S = product(G, 'S', n)
        comp_of, rings = structure(P, S, n)[1]
        sks = skeletons(P, S, n, comp_of, rings)
        if any(len({p for _, p in ps if p[0] < p[1]}) >= 2 for _, ps in sks):
            stats['ok_indep_2distinct_pairs'] = stats.get('ok_indep_2distinct_pairs', 0) + 1
        if any(len(ps) >= 2 for _, ps in sks):
            stats['ok_indep_>=2per'] = stats.get('ok_indep_>=2per', 0) + 1
print('stats', stats)
print('ok/independent but laminarity or formula failure:', len(okbad))
for x in okbad[:5]: print(x)
