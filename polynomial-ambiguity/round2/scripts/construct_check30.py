"""construct_check30.py -- (1) exhaustive: all x in W_30 ∩ N^30 with |x|_1 <= NMAX primitive -> covered?
(2) random W_30 points: coverage and ply (#systems containing x) for the k<=2 dominance-atom family."""
import itertools, random, sys, numpy as np
import construct_cover30 as cc
S = cc.S; n = 30
# W^perp basis: order-30 Fourier component; x in W iff sum_j x_j zeta^{jk}=0 for all k with gcd(k,30)=1
ks = [k for k in range(30) if np.gcd(k, 30) == 1]
F = np.exp(2j*np.pi*np.outer(ks, np.arange(30))/30)
def inW(x): return np.abs(F @ x).max() < 1e-8
NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 5
tot = unc = 0; U = []
def comps(N, k):
    if k == 1: yield (N,); return
    for a in range(N+1):
        for r in comps(N-a, k-1): yield (a,)+r
for N in range(1, NMAX+1):
    # supports of size <= N
    for sz in range(1, N+1):
        for sup in itertools.combinations(range(n), sz):
            for vals in comps(N-sz, sz):
                x = np.zeros(n, int); x[list(sup)] = 1+np.array(vals)
                if not inW(x) or not S.inE(x): continue
                tot += 1
                if not cc.systems(x, stop=True): unc += 1; U.append([i for i in range(n) for _ in range(x[i])])
print(f'exhaustive |x|<= {NMAX}: primitive W30 points {tot}, uncovered {unc}', U[:4])
rng = random.Random(1); plys = []; un = 0
for _ in range(int(sys.argv[2]) if len(sys.argv) > 2 else 100):
    x = S.W({2: [rng.randint(0, 3) for _ in range(15)], 3: [rng.randint(0, 3) for _ in range(10)], 5: [rng.randint(0, 3) for _ in range(6)]})
    if not S.inE(x): continue
    k = len(cc.systems(x)); plys.append(k); un += (k == 0)
print('random W30: n', len(plys), 'uncovered', un, 'ply min/median/max', min(plys), int(np.median(plys)), max(plys))
