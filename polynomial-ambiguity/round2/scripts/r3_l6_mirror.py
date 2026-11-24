"""r3_l6_mirror.py -- does the symmetric-pump attack (Theorem S lifted to ONE nested structure) ever bite?  [computational]

Run-word model: w = a^{L+r_0} b a^{L+r_1} b ... a^{L+r_{M-1}} b, M = 6N, L >> N*max|r|.
  w square <=> r is 3N-periodic (V2);  w cube <=> r is 2N-periodic (V3)   (cyclic run vector).
  A 2-chord (sigma, sigma+n/2) with letters differing exists with axis k (reflection R_k : a -> 2k+1-a mod M)
  iff h_k := sum_{i=k+1}^{k+3N} r_i - (sum r)/2 != 0.
In a G2 x (tree automaton) derivation with chord axis k, the only pumps are spine loops of the two folds; on long
a-runs they add equal amounts to mirror pairs {a, 2k+1-a}, i.e. a palindromic vector p >= 0 (w.r.t. R_k).
r + p in V3 for some palindromic p >= 0  <=>  anti_k(r) := (r - R_k r)/2 lies in V3.      (report, Lemma P1)
"attack works on r" <=> for EVERY chord axis k: anti_k(r) in V3.
Claim A (checked here): if r is not in V2 u V3 then the attack never works, i.e. some chord axis k has anti_k(r) not in V3.
Same check for the G3 analogue is done in r3_l6_mirror3.py (not needed for Claim A).
"""
import itertools, random, sys
import numpy as np

def periodic(r, p):
    return all(r[i] == r[(i + p) % len(r)] for i in range(len(r)))

def axes(r, N):
    M = 6 * N; tot = sum(r)
    out = []
    for k in range(3 * N):
        h2 = 2 * sum(r[(k + 1 + i) % M] for i in range(3 * N)) - tot
        if h2 != 0:
            out.append(k)
    return out

def anti_in_V3(r, k, N):
    M = 6 * N
    a = [r[i] - r[(2 * k + 1 - i) % M] for i in range(M)]   # 2*anti
    return periodic(a, 2 * N)

def attack_works(r, N):
    ax = axes(r, N)
    return len(ax) > 0 and all(anti_in_V3(r, k, N) for k in ax)

def run(N, vals, rand=None, seed=1):
    M = 6 * N; cnt = bad = 0
    rng = random.Random(seed)
    it = itertools.product(vals, repeat=M) if rand is None else \
        (tuple(rng.choice(vals) for _ in range(M)) for t in range(rand))
    for r in it:
        if periodic(r, 3 * N) or periodic(r, 2 * N):
            continue
        cnt += 1
        if attack_works(r, N):
            bad += 1
            if bad <= 3: print('  attack works on', r)
    print(f'N={N} vals={vals} {"exhaustive" if rand is None else f"random {rand}"}: L6 run-vectors {cnt}, attack works on {bad}')

if __name__ == '__main__':
    run(1, range(4))
    run(2, range(3))
    run(2, (-2, 0, 1, 3), rand=50000)
    run(3, range(3), rand=50000)
    # structured mixed words r = v + y, v in V3, y in V2
    for N in (2, 3, 4):
        rng = random.Random(N); cnt = bad = 0
        for t in range(50000):
            v = [rng.randint(-2, 2) for _ in range(2 * N)] * 3
            y = [rng.randint(-2, 2) for _ in range(3 * N)] * 2
            r = tuple(v[i] + y[i] for i in range(6 * N))
            if periodic(r, 3 * N) or periodic(r, 2 * N): continue
            cnt += 1; bad += attack_works(r, N)
        print(f'N={N} mixed r=v+y random: {cnt} words, attack works on {bad}')
