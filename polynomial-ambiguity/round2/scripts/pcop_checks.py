"""P_cop sanity checks (round2, pcop.md).
(a) Lemma P2: for linear sets c+N p1+N p2 (independent periods) and non-radial rays c+N p in N^2,
    'every point has gcd>=2' <=> 'one prime q divides c and all periods'.  Checked on a finite box
    (box membership is a necessary condition only; the box is large enough for the CRT witness here).
(b) Theorem U inputs: e(p,j) := #{non-primitive words with Parikh (p,j)} is 0 iff gcd(p,j)=1,
    and >=1 iff p|j for prime p (so the 'missing-word' series [x^p]G is supported on pN).
"""
import itertools, math, random
from math import gcd, comb

def primes_dividing(v):
    g = 0
    for t in v: g = gcd(g, t)
    return g

def all_noncoprime(points):
    return all(gcd(x, y) >= 2 for (x, y) in points)

def common_prime(vecs):
    g = 0
    for (x, y) in vecs: g = gcd(gcd(g, x), y)
    return g >= 2

random.seed(1)
bad = 0; tested = 0
for _ in range(20000):
    c = (random.randint(0, 12), random.randint(0, 12))
    p1 = (random.randint(0, 9), random.randint(0, 9))
    p2 = (random.randint(0, 9), random.randint(0, 9))
    if p1[0]*p2[1]-p1[1]*p2[0] == 0: continue
    pts = [(c[0]+s*p1[0]+t*p2[0], c[1]+s*p1[1]+t*p2[1]) for s in range(40) for t in range(40)]
    pts = [q for q in pts if q != (0, 0)]
    tested += 1
    if all_noncoprime(pts) != common_prime([c, p1, p2]): bad += 1
print("2-period linear sets tested", tested, "mismatches", bad)

bad = 0; tested = 0
for _ in range(20000):
    c = (random.randint(0, 30), random.randint(0, 30))
    p = (random.randint(0, 12), random.randint(0, 12))
    if p == (0, 0) or c[0]*p[1]-c[1]*p[0] == 0: continue   # radial rays excluded
    pts = [(c[0]+s*p[0], c[1]+s*p[1]) for s in range(400)]
    pts = [q for q in pts if q != (0, 0)]
    tested += 1
    if all_noncoprime(pts) != common_prime([c, p]): bad += 1
print("non-radial rays tested", tested, "mismatches", bad)

# (b) non-primitive counts via Moebius: #primitive words with Parikh (i,j) = sum_{d|g} mu(d) C((i+j)/d, i/d)
def mu(n):
    r, m, q = 1, n, 2
    while q*q <= m:
        if m % q == 0:
            m //= q
            if m % q == 0: return 0
            r = -r
        q += 1
    return -r if m > 1 else r

ok = True
for i in range(0, 25):
    for j in range(0, 25):
        if i+j == 0: continue
        g = gcd(i, j)
        prim = sum(mu(d)*comb((i+j)//d, i//d) for d in range(1, g+1) if g % d == 0)
        e = comb(i+j, i) - prim
        if (e == 0) != (g == 1): ok = False; print("fail", i, j, e)
for p in [2, 3, 5, 7, 11, 13]:
    for j in range(0, 60):
        g = gcd(p, j)
        prim = sum(mu(d)*comb((p+j)//d, p//d) for d in range(1, g+1) if g % d == 0)
        e = comb(p+j, p) - prim
        if (e >= 1) != (j % p == 0): ok = False; print("fail p", p, j)
print("missing-word support check (e=0 iff coprime; for prime p: e>=1 iff p|j):", ok)
