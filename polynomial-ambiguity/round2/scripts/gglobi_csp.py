"""gglobi_csp: the adjacent-pair witness lemma (R2/gglob_i.md, Lemma I2) -- adversarial search.

z = Dy, z_x = y_x - y_{x+1}.  A k-witness is a pair x != x' with x = x' mod s_k and z_x != z_x'.
Question (Lemma I2): is there, for every z notin U V_k, a set X of positions with no two cyclically
consecutive (gaps >= 2) containing a k-witness for every k?  |X| <= 2N automatically.
count_solutions(z) = number of tuples (w_1..w_N) of witnesses whose union has no consecutive pair.
We hill-climb over small-alphabet z to MINIMISE the count (looking for 0 with z primitive).
Usage: gglobi_csp.py N iters restarts seed
"""
import sys, random, itertools
from math import prod
PR = [2, 3, 5, 7, 11]

def witnesses(z, n, s):
    W = []
    for r in range(s):
        cl = list(range(r, n, s))
        for a, b in itertools.combinations(cl, 2):
            if z[a] != z[b]: W.append((a, b))
    return W

def ok(pts, n):
    S = sorted(set(pts))
    return all((S[(i+1) % len(S)] - S[i]) % n not in (1, n-1) for i in range(len(S))) if len(S) > 1 else True

def solve(z, n, sk, count_cap=None):
    Ws = [witnesses(z, n, s) for s in sk]
    if any(len(W) == 0 for W in Ws): return None  # not primitive
    order = sorted(range(len(sk)), key=lambda k: len(Ws[k]))
    cnt = 0
    def rec(i, pts):
        nonlocal cnt
        if count_cap and cnt >= count_cap: return
        if i == len(order): cnt += 1; return
        for w in Ws[order[i]]:
            ps = pts | set(w)
            bad = any(((p+1) % n) in ps for p in ps)
            if not bad: rec(i+1, ps)
    rec(0, set())
    return cnt

if __name__ == '__main__':
    N = int(sys.argv[1]); iters = int(sys.argv[2]); restarts = int(sys.argv[3]); seed = int(sys.argv[4])
    rng = random.Random(seed)
    P = prod(PR[:N]); n = P*P; sk = [n//p for p in PR[:N]]
    cap = 10**6
    best_overall = None
    for R in range(restarts):
        alph = rng.choice([2, 3])
        # sparse start: mostly 0
        z = [0]*n
        for _ in range(rng.randint(1, 4)): z[rng.randrange(n)] = rng.randrange(1, alph)
        c = solve(z, n, sk, cap)
        while c is None:
            z[rng.randrange(n)] = rng.randrange(alph); c = solve(z, n, sk, cap)
        for it in range(iters):
            z2 = z[:]
            for _ in range(rng.randint(1, 3)):
                z2[rng.randrange(n)] = rng.randrange(alph)
            c2 = solve(z2, n, sk, cap)
            if c2 is None: continue
            if c2 <= c: z, c = z2, c2
            if c == 0: break
        if best_overall is None or c < best_overall[0]: best_overall = (c, z)
        print(f'restart {R}: min #solutions {c}  support {sum(1 for v in z if v)}', flush=True)
        if c == 0:
            print('COUNTEREXAMPLE z =', z); break
    print('best', best_overall[0], best_overall[1] if best_overall[0] < 50 else '')
