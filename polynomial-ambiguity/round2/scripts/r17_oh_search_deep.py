"""r17_oh_search_deep.py -- deep check of the stage-3 survivors: exact unambiguity + per-pad G- exit up to |x| <= N3,
listing the survival length for every pad (b^i, a^j), i, j <= 4; float DP growth of |L_n| n/2^n to n = 800."""
import sys, pickle, time
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from r17_oh_search_engine import in_Gminus, scaled, first_violation_k
from r17_oh_search_families import pad_survival, unamb
N3 = int(sys.argv[1]) if len(sys.argv) > 1 else 24
src = sys.argv[2] if len(sys.argv) > 2 else __file__.replace('deep', 'recheck').replace('.py', '_surv20.pkl')
surv = pickle.load(open(src, 'rb'))
for o in surv:
    G = o[6]; t0 = time.time()
    print('=== Y:', o[2], o[3], '| tokens', o[4], '| w =', repr(o[5]))
    print('   grammar X:', G['X'], ' Y:', G['Y'])
    ok, n, W = unamb(G, 'X', N3)
    print(f'   unambiguous up to |x| <= {N3}: {ok} (first ambiguous length {n})  [{time.time()-t0:.0f}s]')
    ps = pad_survival(W['X'], N3, 4)
    for (i, j), v in sorted(ps.items()):
        if v is None:
            print(f'   pad (b^{i}, a^{j}): NO G- exit for |x| <= {N3}')
        else:
            print(f'   pad (b^{i}, a^{j}): first exit n={v[0]} (|x|={v[0]-i-j}) word {v[1]} at k={first_violation_k(v[1])}')
    C = scaled(G, 800)['X']
    print('   |X_n| n/2^n (float DP; = word count only if unambiguous):',
          ', '.join(f'n={m}: {max(C[m], C[m-1])*m:.4g}' for m in (50, 100, 200, 400, 800)))
