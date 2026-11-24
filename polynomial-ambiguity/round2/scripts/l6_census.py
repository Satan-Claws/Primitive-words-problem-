"""l6_census.py -- census of L6 = { w in {a,b}^{6N} : w != u^2, w != u^3 } by certificate type.  [computational]

n = 6m, A = n/2 = 3m, B = n/3 = 2m.  Fibre r (0<=r<m) = letters at r, r+m, ..., r+5m  (a vector in {0,1}^6).
  V2(6) = 3-periodic fibres (shift A),  V3(6) = 2-periodic fibres (shift B).
Lemma F: w in V_2 (square) iff every fibre in V2(6);  w in V_3 (cube) iff every fibre in V3(6).
  single-fibre  : some fibre not in V2(6) u V3(6)  (a <=6-point certificate inside one fibre exists;
                  this contains every rectangle {i,i+B,i+A,i+A+B} and shared-endpoint triangle certificate)
  mixed         : w in L6 but every fibre in V2(6) u V3(6)  (needs a 2-witness and a 3-witness in DIFFERENT fibres)
Count-split grammar C_k = (G_2 n R_{3,k}) u (G_3 n R_{2,k}) u (R_{2,k} n R_{3,k})  restricted to 6N,
  R_{p,k} = { w : some f, |f|<=k, has cyclic occurrence count not = 0 mod p }  (regular).
  L(C_k) = L6 n (R_{2,k} u R_{3,k});  uncovered U_k = L6 words all of whose cyclic <=k-factor counts are = 0 mod 6
  (well: = 0 mod 2 and = 0 mod 3).  amb_{C_k}(w) = A_2(w)[w in R_3k] + A_3(w)[w in R_2k] + [w in R_2k n R_3k].
Usage: l6_census.py           (exhaustive n=6,12,18; random n=24,30,36)
"""
import itertools, random, sys
from collections import Counter

def is_pow(w, p):
    n = len(w)
    if n % p: return False
    s = n // p
    return w == w[:s] * p

def in_L6(w):
    return len(w) % 6 == 0 and not is_pow(w, 2) and not is_pow(w, 3)

def fibres(w):
    m = len(w) // 6
    return [tuple(w[r + m*c] for c in range(6)) for r in range(m)]

def f_in_V2(f): return f[0:3] == f[3:6]
def f_in_V3(f): return f[0] == f[2] == f[4] and f[1] == f[3] == f[5]

def cyc_counts(w, k):
    n = len(w); ww = w + w[:k-1]
    c = Counter()
    for L in range(1, k+1):
        for i in range(n):
            c[ww[i:i+L]] += 1
    return c

def R(w, p, k):
    # some factor of length <= k (over all such factors, including absent ones -> count 0) has count not = 0 mod p
    return any(v % p for v in cyc_counts(w, k).values())

def A_p(w, p):
    n = len(w); s = n // p
    return sum(1 for i in range((p-1)*s) if w[i] != w[i+s])

def classify(w, K=(1, 2, 3)):
    fs = fibres(w)
    single = any(not f_in_V2(f) and not f_in_V3(f) for f in fs)
    out = {'single': single, 'mixed': not single}
    for k in K:
        r2, r3 = R(w, 2, k), R(w, 3, k)
        out[f'U{k}'] = not (r2 or r3)
        out[f'amb{k}'] = A_p(w, 2)*r3 + A_p(w, 3)*r2 + (r2 and r3)
    return out

def census(words, n, label):
    tot = Counter(); maxamb = Counter(); ex = {}
    for w in words:
        if not in_L6(w): continue
        tot['L6'] += 1
        c = classify(w)
        # sanity of Lemma F: in_L6 <=> (some fibre notin V2) and (some fibre notin V3)
        fs = fibres(w)
        assert (any(not f_in_V2(f) for f in fs) and any(not f_in_V3(f) for f in fs))
        for key in ('single', 'mixed', 'U1', 'U2', 'U3'):
            if c[key]:
                tot[key] += 1; ex.setdefault(key, w)
        for k in (1, 2, 3):
            maxamb[k] = max(maxamb[k], c[f'amb{k}'])
        if c['mixed'] and c['U3']: tot['mixed&U3'] += 1; ex.setdefault('mixed&U3', w)
    print(f"[{label}] n={n}: " + ", ".join(f"{k}={v}" for k, v in sorted(tot.items())) +
          f" | max amb C_k (k=1,2,3) = {maxamb[1]},{maxamb[2]},{maxamb[3]}")
    for k, w in sorted(ex.items()):
        if k in ('mixed', 'U1', 'U3', 'mixed&U3'): print(f"     e.g. {k}: {w}")
    return tot

def check_lemmaF(nmax=18):
    # exhaustive: in_L6 == fibre criterion, all words with 6 | n <= nmax
    for n in range(6, nmax+1, 6):
        for t in itertools.product('ab', repeat=n):
            w = ''.join(t); fs = fibres(w)
            crit = any(not f_in_V2(f) for f in fs) and any(not f_in_V3(f) for f in fs)
            assert crit == in_L6(w), w
    print(f"Lemma F verified exhaustively for 6|n<={nmax}")

def mixed_sampler(n, rng):
    # random word all of whose fibres lie in V2(6) u V3(6) (the hard core); half the time force #b = 0 mod 6
    m = n // 6
    cols = [[None]*6 for _ in range(m)]
    for r in range(m):
        if rng.random() < 0.5:
            x = [rng.choice('ab') for _ in range(3)]; f = x + x
        else:
            x = [rng.choice('ab') for _ in range(2)]; f = x * 3
        cols[r] = f
    return ''.join(cols[r][c] for c in range(6) for r in range(m))

if __name__ == '__main__':
    check_lemmaF(18)
    for n in (6, 12, 18):
        census((''.join(t) for t in itertools.product('ab', repeat=n)), n, 'exhaustive')
    rng = random.Random(1)
    for n in (24, 30, 36):
        census((''.join(rng.choice('ab') for _ in range(n)) for _ in range(20000)), n, 'uniform-random 20000')
        census((mixed_sampler(n, rng) for _ in range(20000)), n, 'fibre-mixed-random 20000')
