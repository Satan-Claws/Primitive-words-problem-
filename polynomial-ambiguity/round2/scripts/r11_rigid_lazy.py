"""r11_rigid_lazy.py -- No-go 3: G^- (even lengths) is itself an injective, critical, heavy-tailed pair model.
Tokens (u,v), |u|=|v|=m, zipped steps s_j=[u_j=a]-[v_{m+1-j}=a] in {-1,0,+1}; token = one 0-step, one -1 step,
or a lazy negative excursion (first step -1, partial sums <=-1, ends at 0). p=b, q=a, w=eps.
Checks: (1) token measure sum_m 4^-m #tokens_m -> 1 with excursion tail ~ m^-3/2; (2) for even n<=N every generated
word is in G^-, each has exactly one pair sequence, and the generated set equals G^- cap {a,b}^n."""
import itertools, sys
from collections import Counter
N = int(sys.argv[1]) if len(sys.argv) > 1 else 16
def inG(x):
    n = len(x); d = 0
    for k in range(n // 2):
        d += (x[k] == 'a') - (x[n - 1 - k] == 'a')
        if d >= 0: return False
    return True
def steps(u, v):
    m = len(u); return [(u[j] == 'a') - (v[m - 1 - j] == 'a') for j in range(m)]
def is_token(u, v):
    s = steps(u, v)
    if len(s) == 1: return s[0] <= 0
    if s[0] != -1: return False
    t = 0
    for j, x in enumerate(s):
        t += x
        if j < len(s) - 1 and t > -1: return False
    return t == 0
M = (N - 2) // 2
tok = {m: [(''.join(u), ''.join(v)) for u in itertools.product('ab', repeat=m) for v in itertools.product('ab', repeat=m)
           if is_token(''.join(u), ''.join(v))] for m in range(1, M + 1)}
tot = 0.0
for m in range(1, M + 1):
    tot += len(tok[m]) * 4.0 ** -m
    print(f'm={m}: tokens {len(tok[m])}, weight {len(tok[m]) * 4.0 ** -m:.5f}, cumulative {tot:.5f}')
# exact excursion weight: lazy walk p(-1)=p(+1)=1/4, p(0)=1/2; excursion weight = 1/4 by F=4 (see report)
gen = Counter(); fr = [('', '')]
while fr:
    nf = []
    for U, V in fr:
        gen['b' + U + V + 'a'] += 1
        for m in range(1, M - len(U) + 1):
            for u, v in tok[m]: nf.append((U + u, v + V))
    fr = nf
ok = True
for n in range(2, N + 1, 2):
    G = {''.join(x) for x in itertools.product('ab', repeat=n) if inG(''.join(x))}
    Gen = {W for W in gen if len(W) == n}
    mult = max((gen[W] for W in Gen), default=0)
    eq = (G == Gen); ok &= eq and mult <= 1
    print(f'n={n}: |G-_n|={len(G)} generated={len(Gen)} equal={eq} max multiplicity={mult}')
print('ALL OK' if ok else 'FAIL')
