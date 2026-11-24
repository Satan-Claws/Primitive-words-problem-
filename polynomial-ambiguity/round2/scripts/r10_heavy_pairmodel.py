"""r10_heavy_pairmodel.py -- the Sec.4 critical pair model P={(E,eps)} u {(b,E^k a)} with chosen p,w,q:
list ambiguous words and first G- violations up to N (argv: p w q N)."""
import sys
from collections import Counter, defaultdict
p, w, q, N = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
def inG(x):
    n = len(x); d = 0
    for k in range(n // 2):
        d += (x[k] == 'a') - (x[n - 1 - k] == 'a')
        if d >= 0: return False
    return True
def dyck(m):
    if m == 0: return ['']
    return ['b' + L + 'a' + R for i in range(m) for L in dyck(i) for R in dyck(m - 1 - i)]
M = N - len(p + w + q)
E = ['b' + d + 'a' for m in range(M // 2) for d in dyck(m)]
def blocks(k):
    out = ['a']
    for _ in range(k): out = [e + x for e in E for x in out if len(e + x) <= M]
    return out
pairs = [(e, '', 'E') for e in E] + [('b', x, 'b%d' % k) for k in range(M // 2) for x in blocks(k)]
words = defaultdict(list); fr = [('', '', ())]; outs = []
while fr:
    nf = []
    for U, V, s in fr:
        W = p + U + w + V + q; words[W].append((U, V))
        if not inG(W) and len(outs) < 3: outs.append((W, U, V))
        for u, v, t in pairs:
            if len(U) + len(V) + len(u) + len(v) <= M: nf.append((U + u, v + V, s + (t,)))
    fr = nf
amb = {W: d for W, d in words.items() if len(d) > 1}
byn = Counter(len(W) for W in amb)
print(f'p={p} w={w} q={q} N={N}: words {len(words)}, ambiguous {len(amb)} by length {dict(sorted(byn.items()))}')
for W in sorted(amb, key=len)[:3]: print('  amb', W, amb[W])
print('  G- violations (first 3):', outs)
