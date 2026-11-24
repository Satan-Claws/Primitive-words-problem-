"""r17_oh_search_recheck.py -- re-check stage-2 survivors at larger N.
For each survivor X-grammar: unambiguity of X up to N2 (parse count == distinct count) and, for every pad (b^i, a^j),
i,j<=3, the first G- exit of b^i x a^j with |x| <= N2.  Then growth of |X_n| n / 2^n by float DP to n = 400."""
import sys, pickle, time
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from r17_oh_search_engine import words, parses, in_Gminus, scaled
from r17_oh_search_families import pad_survival, unamb
from collections import Counter
N2 = int(sys.argv[1]) if len(sys.argv) > 1 else 17
surv = pickle.load(open(__file__.replace('recheck', 'families_surv').replace('.py', '.pkl'), 'rb'))
print(f"{len(surv)} stage-2 survivors; re-check to |x| <= {N2}")
t0 = time.time(); out = []; killers = Counter()
for (sc, D, yr, ts, w, G) in surv:
    ok, n, W = unamb(G, 'X', N2)
    if not ok:
        killers['ambiguous'] += 1; out.append((n, 'amb', D, yr, ts, w)); continue
    ps = pad_survival(W['X'], N2, 3)
    best = max((99 if v is None else v[0] - i - j) for (i, j), v in ps.items())
    if best == 99:
        killers['SURVIVES'] += 1; out.append((99, 'surv', D, yr, ts, w, G))
    else:
        killers['G- exit'] += 1
        bp = max(ps, key=lambda k: ps[k][0] - k[0] - k[1])
        out.append((best, 'out', D, yr, ts, w, ps[bp]))
print(killers, f"({time.time()-t0:.0f}s)")
print("histogram of |x| at kill:", sorted(Counter(o[0] for o in out).items()))
for o in sorted(out, key=lambda z: -z[0])[:12]:
    print(o[:6], o[6] if o[1] == 'out' else '')
pickle.dump([o for o in out if o[1] == 'surv'], open(__file__.replace('.py', f'_surv{N2}.pkl'), 'wb'))
