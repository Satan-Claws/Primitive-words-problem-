"""r3_sep_i2nc: Lemma I2-NC (R2/r3_sep.md section 4) -- witness systems whose chords are pairwise non-crossing.

z = Dy (z_x = y_x - y_{x+1}), n = P^2, s_k = n/p_k.  A k-witness is a pair {a,b}, a = b mod s_k, z_a != z_b.
I2    : choose one k-witness per k, union has no two cyclically consecutive points.       (gglob_i)
I2-NC : additionally the 2N points are distinct and the N chords {a_k,b_k} are pairwise non-crossing.
(Needed by Lemma C1 of r3_sep.md for a single laminar piece certifying all k with pair facets.)
Modes:
  climb N iters restarts seed  : hill-climb over y (small alphabet, sparse start) minimising #I2-NC systems
                                  (capped), report any y with I2 but not I2-NC, or with neither.
  struct N                     : structured defects (orbit indicators, 1_D+1_T, random sparse) -> existence.
"""
import sys, random, itertools
from math import prod
PR = [2, 3, 5, 7, 11]


def wits(z, n, s):
    W = []
    for r in range(s):
        cl = list(range(r, n, s))
        for a, b in itertools.combinations(cl, 2):
            if z[a] != z[b]: W.append((a, b))
    return W


def cross(p, q, n):
    a, b = sorted(p); c, d = sorted(q)
    return (a < c < b) != (a < d < b)


def count(z, n, sk, nc=True, cap=10**5):
    Ws = [wits(z, n, s) for s in sk]
    if any(not W for W in Ws): return None
    order = sorted(range(len(sk)), key=lambda k: len(Ws[k]))
    cnt = 0
    def rec(i, pts, chords):
        nonlocal cnt
        if cnt >= cap: return
        if i == len(order): cnt += 1; return
        for w in Ws[order[i]]:
            if nc and (w[0] in pts or w[1] in pts): continue
            ps = pts | set(w)
            if any(((p + 1) % n) in ps for p in ps): continue
            if nc and any(cross(w, c, n) for c in chords): continue
            rec(i + 1, ps, chords + [w])
    rec(0, frozenset(), [])
    return cnt


def setup(N):
    P = prod(PR[:N]); n = P * P
    return n, [n // p for p in PR[:N]]


def climb(N, iters, restarts, seed):
    rng = random.Random(seed); n, sk = setup(N)
    worst = None; bad_nc = 0; bad_i2 = 0
    for R in range(restarts):
        alph = rng.choice([2, 3])
        y = [0] * n
        for _ in range(rng.randint(1, 5)): y[rng.randrange(n)] = rng.randrange(1, alph + 1)
        def f(y):
            z = [y[i] - y[(i + 1) % n] for i in range(n)]
            return count(z, n, sk, True), z
        c, z = f(y)
        while c is None:
            y[rng.randrange(n)] = rng.randrange(alph + 1); c, z = f(y)
        for it in range(iters):
            y2 = y[:]
            for _ in range(rng.randint(1, 3)): y2[rng.randrange(n)] = rng.randrange(alph + 1)
            c2, z2 = f(y2)
            if c2 is None: continue
            if c2 <= c: y, c, z = y2, c2, z2
            if c == 0: break
        if c == 0:
            c_i2 = count(z, n, sk, False)
            bad_nc += 1; bad_i2 += (c_i2 == 0)
            print('I2-NC FAILS: y =', y, ' I2 systems:', c_i2, flush=True)
        if worst is None or c < worst[0]: worst = (c, y)
    print(f'N={N} n={n} restarts={restarts}: I2-NC failures {bad_nc}, I2 failures {bad_i2}, min #NC systems {worst[0]}')


def struct(N, trials=200, seed=1):
    rng = random.Random(seed); n, sk = setup(N)
    tot = fail = 0
    fams = []
    for _ in range(trials):
        typ = rng.choice(['orbits', 'sparse', 'DT'])
        y = [0] * n
        if typ == 'orbits':     # sum of indicators of random s-orbits (s = n/(product of a subset of primes))
            for _ in range(rng.randint(1, 4)):
                sub = [p for p in PR[:N] if rng.random() < 0.5] or [PR[rng.randrange(N)]]
                s = n // prod(sub); r = rng.randrange(n)
                for j in range(prod(sub)): y[(r + j * s) % n] += rng.choice([1, 1, 2])
        elif typ == 'sparse':
            for _ in range(rng.randint(2, 6)): y[rng.randrange(n)] += rng.choice([1, -1, 2])
        else:                   # 1_D + 1_T with D a 2-cycle (s_1 orbit), T a 3-cycle (s_2 orbit)
            r = rng.randrange(n); y[r] += 1; y[(r + n // 2) % n] += 1
            r = rng.randrange(n)
            for j in range(3): y[(r + j * n // 3) % n] += 1
        z = [y[i] - y[(i + 1) % n] for i in range(n)]
        c = count(z, n, sk, True, cap=1)
        if c is None: continue
        tot += 1
        if c == 0:
            fail += 1; print('I2-NC FAILS', typ, [i for i in range(n) if y[i]], flush=True)
    print(f'struct N={N} n={n}: primitive {tot}, I2-NC failures {fail}')


if __name__ == '__main__':
    if sys.argv[1] == 'climb': climb(*map(int, sys.argv[2:6]))
    else: struct(int(sys.argv[2]), int(sys.argv[3]) if len(sys.argv) > 3 else 200)
