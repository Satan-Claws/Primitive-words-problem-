"""r9_packing_search.py -- random search for CFGs L with L ⊆ G⁻ (checked to NMAX) and large |L_n|.
Grammars: nonterminals S,A,B; every RHS is a single terminal or has length >= 2 (so lengths strictly grow).
For each grammar we compute word sets per nonterminal per length (n <= NMAX), derivation counts (ambiguity check),
and reject as soon as a start word is not in G⁻.  Output: best grammars by |L_NMAX| and growth ratio.
Usage: python r9_packing_search.py [trials] [seed]"""
import random, sys
NMAX = 14
NTS = "SAB"
def inG(w):
    n = len(w); pa = sa = 0
    for k in range(1, n // 2 + 1):
        pa += w[k-1] == 'a'; sa += w[n-k] == 'a'
        if pa - sa >= 0: return False
    return True
def rand_rhs(rng):
    L = rng.choice([1, 2, 2, 3, 3, 3])
    if L == 1: return (rng.choice("ab"),)
    return tuple(rng.choice("abSAB") for _ in range(L))
def splits(total, parts):
    if parts == 1:
        if total >= 1: yield (total,)
        return
    for f in range(1, total - parts + 2):
        for r in splits(total - f, parts - 1): yield (f,) + r
def run(G):
    W = {X: {} for X in NTS}; D = {X: {} for X in NTS}   # word sets and derivation counts
    for n in range(1, NMAX + 1):
        for X in NTS:
            cnt = {}
            for rhs in G[X]:
                if len(rhs) > n: continue
                for sp in splits(n, len(rhs)):
                    parts = []
                    ok = True
                    for sym, l in zip(rhs, sp):
                        if sym in "ab":
                            if l != 1: ok = False; break
                            parts.append({sym: 1})
                        else:
                            d = D[sym].get(l)
                            if not d: ok = False; break
                            parts.append(d)
                    if not ok: continue
                    cur = {"": 1}
                    for p in parts:
                        nxt = {}
                        for u, c in cur.items():
                            for v, e in p.items():
                                nxt[u + v] = nxt.get(u + v, 0) + c * e
                        cur = nxt
                        if len(cur) > 20000: return None
                    for u, c in cur.items(): cnt[u] = cnt.get(u, 0) + c
            D[X][n] = cnt
        if n >= 2 and any(not inG(w) for w in D['S'][n]): return None
    return D['S']
if __name__ == "__main__":
    trials = int(sys.argv[1]) if len(sys.argv) > 1 else 20000
    rng = random.Random(int(sys.argv[2]) if len(sys.argv) > 2 else 1)
    best = []
    for t in range(trials):
        G = {X: [rand_rhs(rng) for _ in range(rng.randint(1, 3))] for X in NTS}
        r = run(G)
        if r is None: continue
        sizes = [len(r.get(n, {})) for n in range(NMAX - 3, NMAX + 1)]
        if sizes[-1] < 3: continue
        amb = max((c for n in r for c in r[n].values()), default=0)
        best.append((sizes[-1], sizes, amb, G))
    best.sort(key=lambda x: -x[0])
    from math import comb
    print("|G-_%d| = %d" % (NMAX, comb(NMAX - 1, NMAX // 2)))
    seen = set()
    for s, sizes, amb, G in best:
        key = tuple(sizes)
        if key in seen: continue
        seen.add(key)
        print(sizes, "maxamb", amb, {X: [''.join(r) for r in G[X]] for X in NTS})
        if len(seen) >= 12: break
