import random, sys, itertools
from struct_check import *
rng = random.Random(int(sys.argv[1])); trials = int(sys.argv[2])
stats = {}; okbad = []; flag_unconfirmed = []
for it in range(trials):
    n = rng.choice([2, 3])
    G = rand_grammar(rng, nN=rng.choice([3, 4, 5]), nr=rng.choice([5, 7, 9]))
    B = 4 if n == 2 else 3
    st, info = analyse(G, 'S', n, B)
    key = st.split(' ')[0]
    stats[key] = stats.get(key, 0) + 1
    if st == 'ok':
        if info['dep']: stats['ok_dep'] = stats.get('ok_dep', 0) + 1; continue
        stats['ok_indep'] = stats.get('ok_indep', 0) + 1
        if info['maxper'] >= 2: stats['ok_indep_>=2per'] = stats.get('ok_indep_>=2per', 0) + 1
        if info['maxamb'] >= 2: stats['ok_indep_amb>=2'] = stats.get('ok_indep_amb>=2', 0) + 1
        if info['lam_bad'] or info['nmism']: okbad.append((G, n, info))
    elif st != 'empty':
        P, S = product(G, 'S', n)
        Bmax = 9 if n == 2 else 5
        mx = [max(count_trees(P, S, word(x)) for x in itertools.product(range(b+1), repeat=n)) for b in range(Bmax-2, Bmax+1)]
        if not (mx[0] < mx[1] < mx[2]): flag_unconfirmed.append((G, n, st, mx))
print('stats', stats)
print('ok but laminar/formula failure:', len(okbad))
for x in okbad[:5]: print(x)
print('flagged (lemma predicts infinite ambiguity) but no growth seen at large B:', len(flag_unconfirmed))
for x in flag_unconfirmed[:10]: print(x)
