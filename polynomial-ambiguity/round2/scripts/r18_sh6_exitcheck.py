"""r18_sh6_exitcheck: for sampled SH6 words, count trees PER EXIT POSITION (forward path count over spine states
(i,j)). Any exit position carrying >=2 trees is an IF violation (two token sequences with the same interface).
Reports E_n[m], and max trees per exit (1 => all multiplicity is pure exit-slide). Usage: n1,n2 R seed"""
import sys, random
import r18_am_lib as L
G = {'tok': [('ab','ab'),('bb','a'),('','ba'),('a','B'),('B','bb'),('a','bb'),('ab','aa')], 'w': 'ab'}
def per_exit(W):
    n = len(W); be = [L.block_end(W, i) for i in range(n + 1)]; bs = [L.block_start(W, j) for j in range(n + 1)]
    F = {(0, n): 1}; order = [(0, n)]; k = 0
    # BFS layer by span; process states in decreasing span
    import heapq
    h = [(-n, 0, n)]; done = set()
    exits = {}
    while h:
        _, i, j = heapq.heappop(h)
        if (i, j) in done: continue
        done.add((i, j)); f = F[(i, j)]
        if W[i:j] == G['w']: exits[i] = exits.get(i, 0) + f
        for us, vs in G['tok']:
            i2 = be[i] if us == 'B' else (i + len(us) if W.startswith(us, i) else -1)
            if i2 < 0: continue
            if vs == 'B': j2 = bs[j]
            else: j2 = j - len(vs) if j - len(vs) >= 0 and W[j - len(vs):j] == vs else -1
            if j2 < 0 or (i2, j2) == (i, j) or j2 - i2 < 2: continue
            F[(i2, j2)] = F.get((i2, j2), 0) + f; heapq.heappush(h, (-(j2 - i2), i2, j2))
    return sum(exits.values()), max(exits.values())
ns = [int(x) for x in sys.argv[1].split(',')]; R = int(sys.argv[2]); rng = random.Random(int(sys.argv[3]))
S = L.Sampler(G, max(ns))
for n in ns:
    tot = 0; mx = 0; mm = 0
    for _ in range(R):
        W = S.sample(n, rng); m, e = per_exit(W); tot += m; mx = max(mx, e); mm = max(mm, m)
    print('n=%d R=%d E_n[m]=%.3f max m=%d  max trees at one exit=%d' % (n, R, tot / R, mm, mx), flush=True)
