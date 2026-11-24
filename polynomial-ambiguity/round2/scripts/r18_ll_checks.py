"""r18_ll_checks.py -- sanity checks for r18_lightlight.md (Theorem LL).
(1) Case I: exact fraction of length-n +-1 words visiting level 0 at >= eps*n positions (exponential decay).
(2) Step 3: CLT variance formula for d_inf(N) vs Monte Carlo (mean-zero symmetric token laws).
(3) Case II.2(iii): two-phase adversary tau+^m tau-^inf with tau+=(aab,a), tau-=(b,abb).
(4) Step 3 empirically: random mean-zero nondegenerate token laws -> d_inf becomes >= 0 on one sampled sequence.
"""
import random, math
from fractions import Fraction
random.seed(18)
val = {'a': 1, 'b': -1}
D = lambda s: sum(val[c] for c in s)

def visits_frac(n, eps):
    # dp[h][v] = #walks at height h with v visits to 0 (positions 1..t)
    from collections import defaultdict
    dp = {(0, 0): 1}
    for t in range(n):
        nd = defaultdict(int)
        for (h, v), c in dp.items():
            for s in (1, -1):
                h2 = h + s; nd[(h2, v + (h2 == 0))] += c
        dp = nd
    need = math.ceil(eps * n)
    return Fraction(sum(c for (h, v), c in dp.items() if v >= need), 2 ** n)

def dinf(seq, p='', q='', N=None):
    U = p + ''.join(u for u, v in seq)
    V = ''.join(v for u, v in reversed(seq)) + q  # word ... v2 v1 q
    N = N or min(len(U), len(V))
    A = B = 0; out = []
    for k in range(1, N + 1):
        A += val[U[k - 1]]; B += val[V[-k]]; out.append(A - B)
    return out

def rand_word(L):
    return ''.join(random.choice('ab') for _ in range(L))

def sym_law(ntok):
    toks = []
    for _ in range(ntok):
        u = rand_word(random.randint(0, 3)); v = rand_word(random.randint(1, 3))
        toks.append((u, v))
    sw = lambda s: s.translate(str.maketrans('ab', 'ba'))
    toks = toks + [(sw(u), sw(v)) for u, v in toks]
    return toks  # uniform law: E D(u)=E D(v)=0

def sigma2(toks):
    m = len(toks); mu_u = sum(len(u) for u, v in toks) / m; mu_v = sum(len(v) for u, v in toks) / m
    du = [D(u) for u, v in toks]; dv = [D(v) for u, v in toks]
    vdiff = sum((x - y) ** 2 for x, y in zip(du, dv)) / m
    if mu_u < mu_v: vslow = sum(x * x for x in du) / m
    else: vslow = sum(y * y for y in dv) / m
    return vdiff / max(mu_u, mu_v) + vslow * abs(1 / mu_u - 1 / mu_v)

if __name__ == '__main__':
    print('(1) Case I: fraction of words with >= eps*n visits to 0, eps=0.15')
    for n in (50, 100, 200, 300):
        f = visits_frac(n, 0.15)
        print(f'  n={n}: frac={float(f):.3e}  -log(frac)/n={-math.log(float(f))/n:.4f}')
    phi=lambda t: 1-math.sqrt(1-math.exp(-2*t))
    rate=max(-(t+0.15*math.log(phi(t))) for t in [i*1e-4 for i in range(1,20000)])
    print(f'  Chernoff rate bound (eps=0.15): frac <= exp(-{rate:.4f} n)')
    print('(2) CLT variance: formula vs MC Var(d(N))/N, N=600, 1500 samples')
    for trial in range(4):
        toks = sym_law(3); s2 = sigma2(toks); N = 600; vals = []
        mu = sum(len(u) + len(v) for u, v in toks) / len(toks)
        for _ in range(1500):
            seq = [random.choice(toks) for _ in range(int(3 * N / max(0.5, min(sum(len(u) for u,v in toks), sum(len(v) for u,v in toks)) / len(toks))) + 50)]
            vals.append(dinf(seq, N=N)[-1])
        mean = sum(vals) / len(vals); var = sum((x - mean) ** 2 for x in vals) / len(vals)
        print(f'  law {trial}: sigma2={s2:.3f}  MC={var/N:.3f}  mean/sqrtN={mean/math.sqrt(N):+.3f}')
    print('(3) two-phase adversary tau+=(aab,a), tau-=(b,abb); single-token slopes A<=B?')
    tp, tm = ('aab', 'a'), ('b', 'abb')
    for t in (tp, tm):
        print(f'  token {t}: slope A={D(t[0])/len(t[0]):+.3f} slope B={D(t[1])/len(t[1]):+.3f}')
    for m in (1, 2, 5, 10, 20, 40):
        seq = [tp] * m + [tm] * (4 * m + 10)
        d = dinf(seq, N=3 * m)  # K = m*|u+| = 3m
        print(f'  m={m}: d(K=3m)={d[-1]}  max_k<=K d={max(d)}')
    print('(4) random mean-zero nondegenerate laws: first k with d_inf(k)>=0 on one sampled sequence')
    hits = 0; tot = 0
    for trial in range(200):
        toks = sym_law(random.randint(2, 4))
        if all(u == "" for u, v in toks): continue
        if sigma2(toks) < 1e-9: continue
        tot += 1
        seq = [random.choice(toks) for _ in range(4000)]
        d = dinf(seq, N=2000) if min(sum(len(u) for u,v in seq), sum(len(v) for u,v in seq))>=2000 else dinf(seq)
        ks = [k for k, x in enumerate(d, 1) if x >= 0]
        hits += bool(ks)
    print(f'  {hits}/{tot} nondegenerate laws hit d>=0 within k<=2000 (offset D(p)-D(q)=0)')
