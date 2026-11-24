"""R17b G-word: full-range ("both ends near the max") set F_n(c) vs quadrant Q_n(C).
Steps +-1 (a=+1, b=-1); P(0)=0.  F_n(c) := { max_{0<=j<=n} P(j) <= min(0,P(n)) + c }.
(1) exact reflection count of F_n(c), brute-force check n<=16, n^{3/2}*density table.
(2) exhaustive check of Lemma FR: W' , W'' in Q(C)  ==>  W in F_n(C + const)  (random contexts).
(3) shifted-quadrant family (task's 'all centre shifts'): H_n(C,h) = {P(j)<=C on [0,n-h], P(j)-P(n)<=C on [h,n]};
    n*density as a function of theta=h/n (exact DP).
"""
import itertools, random
from math import comb, pi, sqrt
import numpy as np

def N(n, y):
    if (n + y) % 2 or abs(y) > n: return 0
    return comb(n, (n + y) // 2)

def F_count(n, c):
    tot = 0
    for y in range(-c, c + 1):
        M = min(0, y) + c
        tot += N(n, y) - N(n, 2 * (M + 1) - y)
    return tot

def walk(w):
    P = [0]
    for ch in w: P.append(P[-1] + (1 if ch == 'a' else -1))
    return P

def inF(w, c):
    P = walk(w); return max(P) <= min(0, P[-1]) + c

def inQ(w, C):
    P = walk(w); n = len(w); h = n // 2
    return all(P[k] <= C for k in range(1, h + 1)) and all(P[n] - P[n - k] >= -C for k in range(1, h + 1))

print("(1) brute force F_n(c) vs reflection formula")
for n in range(1, 17):
    for c in range(0, 4):
        bf = sum(inF(w, c) for w in itertools.product('ab', repeat=n))
        assert bf == F_count(n, c), (n, c)
print("  match n<=16, c<=3: OK")
print("  n^{3/2}*|F_n(c)|/2^n  (even n; C=0 limit 2^{3/2}/sqrt(pi)=%.4f)" % (2**1.5 / sqrt(pi)))
for c in (0, 1, 2, 4):
    row = []
    for n in (100, 1000, 10000, 40000):
        from fractions import Fraction; row.append(n**1.5 * float(Fraction(F_count(n, c), 2**n)))
    print("  c=%d:" % c, " ".join("%.4f" % r for r in row))
print("  compare quadrant n*|Q_n(0)|/2^n -> 4/pi=%.4f (r16/audit_r17)" % (4 / pi))

print("(2) Lemma FR exhaustive check")
random.seed(1)
viol = tested = 0
for inst in range(150):
    C = random.randint(0, 2)
    rnd = lambda a, b: ''.join(random.choice('ab') for _ in range(random.randint(a, b)))
    g, d = rnd(0, 3), rnd(0, 3)          # bounded contexts gamma, delta
    al, be, v, u, al2, be2 = (rnd(0, 2) for _ in range(6))
    m = random.randint(1, 11)
    for M in itertools.product('ab', repeat=m):
        M = ''.join(M); W = g + M + d; n = len(W)
        x = 'ba' * (n + 3); y = 'ab' * (n + 3)            # flat words, |x|,|y| >= n
        W1 = g + al + x + be + M + v + d                   # outermost U-side insertion
        W2 = g + u + M + al2 + y + be2 + d                 # outermost V-side insertion
        if inQ(W, C) and inQ(W1, C) and inQ(W2, C):
            tested += 1
            cc = C + 1 + len(g) + len(d) + max(len(v), len(u)) + 1   # crude explicit constant
            if not inF(W, cc): viol += 1
print("  instances 150, words with W,W',W'' in Q(C): %d, violations of W in F(C+O(1)): %d" % (tested, viol))

print("(3) shifted-quadrant family H_n(C,h): n*density vs theta=h/n  (theta=1/2: quadrant, theta->0: full range)")
def H_density(n, C, h):
    # phase 1: j < h : track P (index P+n); constraint P<=C if j<=n-h
    off = n
    p = np.zeros(2 * n + 2); p[off] = 1.0
    for j in range(1, h + 1):
        q = np.zeros_like(p); q[1:] += 0.5 * p[:-1]; q[:-1] += 0.5 * p[1:]
        if j <= n - h: q[off + C + 1:] = 0
        p = q
    # phase 2: state (P, D), D = max_{[h,j]} P - P >= 0
    S = np.zeros((2 * n + 2, n + 2)); S[:, 0] = p
    for j in range(h + 1, n + 1):
        T = np.zeros_like(S)
        # up-step: P+1, D -> max(D-1,0)
        T[1:, 0] += 0.5 * (S[:-1, 0] + S[:-1, 1])
        T[1:, 1:-1] += 0.5 * S[:-1, 2:]
        # down-step: P-1, D+1
        T[:-1, 1:] += 0.5 * S[1:, :-1]
        if j <= n - h: T[off + C + 1:, :] = 0
        S = T
    return S[:, :C + 1].sum()

for C in (0, 2):
    for n in (200, 400, 800):
        vals = []
        for th in (0.5, 0.375, 0.25, 0.125, 0.0625):
            h = int(th * n); h += (n - h) % 1
            vals.append(n * H_density(n, C, h))
        hb = n * H_density(n, C, 2)
        print("  C=%d n=%4d theta=.5,.375,.25,.125,.0625: %s | h=2: n*d=%.4f n^1.5*d=%.4f" %
              (C, n, " ".join("%.3f" % v for v in vals), hb, sqrt(n) * hb))
