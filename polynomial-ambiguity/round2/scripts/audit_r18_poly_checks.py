"""audit_r18_poly: independent checks of r17_gword FR, |F_n(c)|, rotation density, r17_gwordp FR-pos / T-tol,
r17_gstruct SU, r18_gend Step 2 (lambda=0 finite tokens). Steps +-1 (a=+1, b=-1)."""
import itertools, random, math
from math import comb

def walk(w):
    P = [0]
    for ch in w: P.append(P[-1] + (1 if ch == 'a' else -1))
    return P

def inQ(w, C):
    n = len(w); P = walk(w)
    return all(P[k] <= C and P[n] - P[n - k] >= -C for k in range(1, n // 2 + 1))

def inF(w, c):
    P = walk(w); return max(P) <= min(0, P[-1]) + c

def rnd(L): return ''.join(random.choice('ab') for _ in range(L))

random.seed(1)
# (1) FR: W = g M d ; W' = g al x be M v d ; W'' = g u M al2 y be2 d ; if W',W'' in Q(C) then W in F(C + c0 + 2h0)
viol = tested = 0
for _ in range(200000):
    C = random.randint(0, 2); h0 = random.randint(0, 2); c0 = random.randint(0, 2)
    M = rnd(random.randint(1, 9)); g = rnd(random.randint(0, h0)); d = rnd(random.randint(0, h0))
    W = g + M + d; n = len(W)
    al, be, v, u, al2, be2 = (rnd(random.randint(0, c0)) for _ in range(6))
    # x adversarial: start with a walk hugging the ceiling (b-heavy then random) so W' can be in Q
    x = ''.join(random.choice('abb') for _ in range(n + c0 + random.randint(0, 3)))
    y = ''.join(random.choice('aab') for _ in range(n + c0 + random.randint(0, 3)))
    W1 = g + al + x + be + M + v + d; W2 = g + u + M + al2 + y + be2 + d
    if inQ(W1, C) and inQ(W2, C):
        tested += 1
        if not inF(W, C + c0 + 2 * h0): viol += 1
print(f"(1) FR random: {tested} instances with W',W'' in Q(C); violations of W in F(C+c0+2h0): {viol}")

# (2) reflection formula for |F_n(c)| vs brute force, and normalised bound
def N(n, y):
    return comb(n, (n + y) // 2) if (n + y) % 2 == 0 and abs(y) <= n else 0
def Fform(n, c):
    return sum(N(n, y) - N(n, 2 * (min(0, y) + c + 1) - y) for y in range(-c, c + 1))
bad = 0
for n in range(1, 17):
    words = [''.join(t) for t in itertools.product('ab', repeat=n)]
    for c in range(0, 4):
        bf = sum(inF(w, c) for w in words)
        if bf != Fform(n, c): bad += 1
print("(2) reflection formula mismatches n<=16, c<=3:", bad)
mx = max(float(__import__("fractions").Fraction(Fform(n, c), 2 ** n)) * n ** 1.5 / (c + 1) ** 3 for n in range(2, 3001, 7) for c in range(0, 9))
print(f"    max n^1.5 |F_n(c)| 2^-n /(c+1)^3 over n<=3000, c<=8: {mx:.3f} (bounded)")

# (3) rotation image of F_n(c) and of E_n(C,h) exactly, compare with T-tol bound
def rot_density(n, pred):
    words = [''.join(t) for t in itertools.product('ab', repeat=n)]
    S = set(w for w in words if pred(w))
    R = set()
    for w in S:
        for i in range(n): R.add(w[i:] + w[:i])
    return len(S) / 2 ** n, len(R) / 2 ** n, R
for n in (12, 16):
    for c in (0, 1, 2):
        dS, dR, R = rot_density(n, lambda w: inF(w, c))
        ok = all(abs(walk(w)[-1]) <= c for w in R)
        print(f"(3) n={n} c={c}: |F|/2^n={dS:.4f} |Rot F|/2^n={dR:.4f}  Rot(F) in {{|P(n)|<=c}}: {ok}")
def inE(w, C, h):
    P = walk(w); n = len(w)
    return all(P[j] <= min(C, P[n] + C) for j in range(h, n - h + 1))
viol = 0
for n in (12, 16):
    for C in (0, 1):
        for h in (0, 1, 2, 3):
            _, dR, R = rot_density(n, lambda w: inE(w, C, h))
            pmax = max(N(n, y) for y in range(-n, n + 1)) / 2 ** n
            best = min((2 * K + 1) * pmax + 2 * n * math.exp(-((K - C) ** 2) / (2 * h)) if h else (2 * K + 1) * pmax
                       for K in range(C, n + 1))
            # also check |P(n)| <= C + h on E
            okP = all(abs(walk(w)[-1]) <= C + h for w in R)
            if dR > best + 1e-12 or not okP: viol += 1
print("(3') T-tol bound and |P(n)|<=C+h on E_n(C,h), n in {12,16}: violations", viol)

# (5) Lemma SU toy: X -> B X | c ; B -> b | D ; D -> b  (B ambiguous on 'b', B on side of loop)  => 2^m trees for b^m c
def count_trees(word):
    from functools import lru_cache
    rules = {'X': [('B', 'X'), ('c',)], 'B': [('b',), ('D',)], 'D': [('b',)]}
    @lru_cache(None)
    def cnt(A, i, j):
        tot = 0
        for r in rules[A]:
            tot += seq(r, i, j)
        return tot
    @lru_cache(None)
    def seq(r, i, j):
        if not r: return 1 if i == j else 0
        s, rest = r[0], r[1:]
        tot = 0
        for k in range(i + 1, j + 1 - len(rest)):
            if s in rules: a = cnt(s, i, k)
            else: a = 1 if (k == i + 1 and word[i] == s) else 0
            if a: tot += a * seq(rest, k, j)
        return tot
    return cnt('X', 0, len(word))
print("(5) SU toy: trees(b^m c) for m=1..8:", [count_trees('b' * m + 'c') for m in range(1, 9)])

# (6) r18_gend Step 2, lambda=0, finite light tokens: a set T of balanced (D=0) words with Kraft sum >= 1
# must fail unique decodability (=> exponential ambiguity of Z -> Z t | w). Sardinas-Patterson.
def is_code(T):
    T = set(T)
    def quot(A, B):
        return {b[len(a):] for a in A for b in B if b.startswith(a) and len(b) > len(a)}
    S = quot(T, T); seen = set()
    while S:
        if '' in S or S & T: return False
        key = frozenset(S)
        if key in seen: return True
        seen.add(key)
        S = quot(T, S) | quot(S, T)
    return True
bal = [''.join(t) for L in (2, 4, 6) for t in itertools.product('ab', repeat=L) if t.count('a') * 2 == L]
random.seed(2); found = 0; trials = 0
for _ in range(20000):
    k = random.randint(4, len(bal))
    T = random.sample(bal, k)
    if sum(2.0 ** -len(t) for t in T) >= 1:
        trials += 1
        if is_code(T): found += 1
print(f"(6) balanced token sets (len<=6) with Kraft>=1: {trials} sampled, uniquely decodable: {found}")
