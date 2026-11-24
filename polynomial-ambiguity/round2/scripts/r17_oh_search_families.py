"""r17_oh_search_families.py -- systematic one-sided heavy pair-model families.

Family A ("tower pair"):
  D- -> eps | b D- a D-        (Dyck, critical, tail n^-3/2)
  D+ -> eps | a D+ b D+
  Y  -> eps | interleave(3 letters, [D, Y, Y])     (critical stacked nonlinear SCC, tail n^-5/4, beta0 = 1/4)
  X  -> u_i X v_i | w        tokens (u_i, v_i): u_i = alpha H beta (H = Y) or letters, v_i letters only (light V side),
                             sum of token weights 2^{-|letters|} * 2^{#H} = 1 exactly (critical linear SCC)
  S  -> b^i X a^j            (b^i / a^j dominate every pad p,q with |p|=i, |q|=j; see report)
Stage 1: Y-variants unambiguous up to length LY.
Stage 2: X unambiguous up to N1 (parse count == distinct count), then first G- exit for each pad (i,j), i,j<=PADMAX.
"""
import sys, itertools, time, json
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from r17_oh_search_engine import words, parses, in_Gminus

LETTERS = ('a', 'b')

def interleavings(lets, nts):
    m = len(lets) + len(nts)
    for pos in itertools.combinations(range(m), len(lets)):
        r = []; li = 0; ni = 0
        for i in range(m):
            if i in pos:
                r.append(lets[li]); li += 1
            else:
                r.append(nts[ni]); ni += 1
        yield tuple(r)

DM = {'Dm': [('b', 'Dm', 'a', 'Dm'), ()]}
DP = {'Dp': [('a', 'Dp', 'b', 'Dp'), ()]}

def y_variants():
    out = []
    seen = set()
    for D in ('Dm', 'Dp'):
        for lets in itertools.product(LETTERS, repeat=3):
            for ntorder in set(itertools.permutations([D, 'Y', 'Y'])):
                for r in interleavings(lets, list(ntorder)):
                    if (D, r) in seen:
                        continue
                    seen.add((D, r))
                    out.append((D, r))
    return out

def base_grammar(D, yrule):
    G = {}
    G.update(DM if D == 'Dm' else DP)
    G['Y'] = [(), yrule]
    return G

def unamb(G, X, N):
    W = words(G, N)
    P = parses(G, N)
    for n in range(N + 1):
        if P[X][n] != len(W[X][n]):
            return False, n, W
    return True, None, W

def words_of_len_upto(seq):
    s = ''
    return s

def all_words(n):
    for t in itertools.product(LETTERS, repeat=n):
        yield ''.join(t)

def token_sets(maxtok=3):
    """critical token sets. token = (alpha, nH, beta, gamma) meaning u = alpha H beta (nH in {0,1}), v = gamma."""
    toks = []
    for c in range(1, 4):           # H tokens, |alpha beta gamma| = c, weight 2^(1-c)
        for la in range(c + 1):
            for lb in range(c - la + 1):
                lg = c - la - lb
                for al in itertools.product(LETTERS, repeat=la):
                    for be in itertools.product(LETTERS, repeat=lb):
                        for ga in itertools.product(LETTERS, repeat=lg):
                            toks.append((''.join(al), 1, ''.join(be), ''.join(ga), 2.0 ** (1 - c)))
    for c in range(1, 3):           # letter tokens
        for la in range(c + 1):
            lg = c - la
            for al in itertools.product(LETTERS, repeat=la):
                for ga in itertools.product(LETTERS, repeat=lg):
                    toks.append((''.join(al), 0, '', ''.join(ga), 2.0 ** (-c)))
    sets = []
    for k in range(1, maxtok + 1):
        for comb in itertools.combinations(range(len(toks)), k):
            T = [toks[i] for i in comb]
            if abs(sum(t[4] for t in T) - 1) > 1e-12:
                continue
            if not any(t[1] for t in T):
                continue
            sets.append(T)
    return sets

def pair_grammar(base, T, w, H='Y'):
    G = dict(base)
    rules = []
    for (al, nh, be, ga, _) in T:
        r = tuple(al) + ((H,) if nh else ()) + tuple(be) + ('X',) + tuple(ga)
        rules.append(r)
    rules.append(tuple(w))
    G['X'] = rules
    return G

def tokstr(T):
    return ' | '.join(f"({al}{'H' if nh else ''}{be}, {ga or 'e'})" for (al, nh, be, ga, _) in T)

def pad_survival(Xwords, N, PADMAX):
    """for each pad (i,j): first n (total length) where b^i x a^j leaves G-, scanning x by length."""
    res = {}
    for i in range(PADMAX + 1):
        for j in range(PADMAX + 1):
            first = None
            for m in range(N + 1):
                for x in Xwords[m]:
                    if not in_Gminus('b' * i + x + 'a' * j) and m + i + j >= 2:
                        first = (m + i + j, 'b' * i + x + 'a' * j); break
                if first:
                    break
            res[(i, j)] = first
    return res

if __name__ == '__main__':
    LY = int(sys.argv[1]) if len(sys.argv) > 1 else 14
    N1 = int(sys.argv[2]) if len(sys.argv) > 2 else 13
    PADMAX = 3
    t0 = time.time()
    ys = y_variants()
    goodY = []; nun = 0
    for (D, r) in ys:
        G = base_grammar(D, r)
        ok, n, W = unamb(G, 'Y', LY)
        if not ok:
            continue
        nun += 1
        # necessary: a single giant token with pads of length <= 6 each side must stay in G-
        if all(in_Gminus('b' * 6 + y + 'a' * 6) for m in range(LY + 1) for y in W['Y'][m]):
            goodY.append((D, r))
    print(f"Y variants: {len(ys)}, unambiguous to length {LY}: {nun}; pass single-token pad-6 G- filter: {len(goodY)}  ({time.time()-t0:.1f}s)")
    print("  kept Y:", [D + ':' + ''.join(r) for (D, r) in goodY])
    TS = token_sets(2) + [t for t in token_sets(3) if len(t) == 3 and sum(x[1] for x in t) == 1
                          and all(len(x[0]) + len(x[2]) + len(x[3]) <= 2 for x in t)]
    print(f"critical token sets (<=2 tokens, or 3 tokens with |letters|<=2 each; >=1 H-token; q_V>0 OR one-tape): {len(TS)}"
          f", of which one-tape (q_V=0): {sum(1 for T in TS if not any(t[3] for t in T))}")
    centres = ['', 'a', 'b', 'ab', 'ba']
    stats = {'amb': 0, 'unamb': 0}
    best = []
    for (D, r) in goodY:
        base = base_grammar(D, r)
        for T in TS:
            for w in centres:
                G = pair_grammar(base, T, w)
                ok, n, W = unamb(G, 'X', N1)
                if not ok:
                    stats['amb'] += 1
                    continue
                stats['unamb'] += 1
                ps = pad_survival(W['X'], N1, PADMAX)
                # survival score: best pad; None = no exit found up to N1 + pads
                sc = max((N1 + 99 if v is None else v[0] - i - j) for (i, j), v in ps.items())
                best.append((sc, D, ''.join(r), tokstr(T) + ('' if any(t[3] for t in T) else '  [ONE-TAPE q_V=0]'), w, {f"{k}": v for k, v in ps.items()}, G))
    print(f"X grammars: ambiguous(<= {N1}) {stats['amb']}, unambiguous {stats['unamb']}  ({time.time()-t0:.1f}s)")
    best.sort(key=lambda z: -z[0])
    surv = [b for b in best if b[0] > N1]
    print(f"survivors (some pad with no G- exit for |x| <= {N1}): {len(surv)}")
    from collections import Counter
    print("histogram of max x-length survived:", sorted(Counter(min(b[0], N1 + 1) for b in best).items()))
    for b in best[:15]:
        print(b[0], b[1], b[2], '|', b[3], '| w =', repr(b[4]))
    json.dump([b[:5] for b in best[:200]], open(__file__.replace('.py', '_top.json'), 'w'))
    import pickle
    pickle.dump([b[:5] + (b[6],) for b in surv], open(__file__.replace('.py', '_surv.pkl'), 'wb'))
