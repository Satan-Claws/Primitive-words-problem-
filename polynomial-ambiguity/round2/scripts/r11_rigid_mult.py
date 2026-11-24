"""r11_rigid_mult.py -- Centre-count bound in the r10 Sec.4 model P={(E,eps)} u {(b,E^k a)}: each word's parses have
pairwise distinct centres c=|pU| (split-uniqueness), so multiplicity <= #admissible centres <= n. Prints, per length,
max multiplicity and whether any two parses share a centre. argv: p w q N."""
import sys
from collections import defaultdict
p, w, q, N = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
def dyck(m):
    if m == 0: return ['']
    return ['b' + L + 'a' + R for i in range(m) for L in dyck(i) for R in dyck(m - 1 - i)]
M = N - len(p + w + q)
E = ['b' + d + 'a' for m in range(M // 2) for d in dyck(m)]
def blocks(k):
    out = ['a']
    for _ in range(k): out = [e + x for e in E for x in out if len(e + x) <= M]
    return out
pairs = [(e, '') for e in E] + [('b', x) for k in range(M // 2) for x in blocks(k)]
words = defaultdict(list); fr = [('', '')]
while fr:
    nf = []
    for U, V in fr:
        words[p + U + w + V + q].append(len(U))
        for u, v in pairs:
            if len(U) + len(V) + len(u) + len(v) <= M: nf.append((U + u, v + V))
    fr = nf
byn = defaultdict(lambda: [0, False])
for W, cs in words.items():
    b = byn[len(W)]; b[0] = max(b[0], len(cs)); b[1] |= len(cs) != len(set(cs))
for n in sorted(byn): print(f'n={n}: max multiplicity {byn[n][0]}, shared-centre collision {byn[n][1]}')
