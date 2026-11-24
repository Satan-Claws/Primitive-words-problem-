"""gglobi_dist: the explicit distribution D of R2/gglob_i.md (Thm I1), exact checks.

D: X_x iid Bernoulli(1/3) on Z_n; A = {x : X_x = 1, X_{x-1} = X_{x+1} = 0}; M = {(x,x+1) : x in A} plus the
adjacent matching of the remaining cyclic sequence (random one of its two adjacent matchings).  M is NC.
For primitive y: z = Dy; S = admissible witness set (gglobi_csp.solve); Pr_D[S subset A] = 3^-|S| (2/3)^|N(S)|.
Checks (exact rank mod 2^31-19, via gglob_matching.in_VkLM):
  (1) for every sampled M with S subset A, all k are certified (Lemma I0 sanity);
  (2) empirical Pr_D[all k certified] vs the lower bound and vs uniform NC matchings.
Usage: gglobi_dist.py N ny nM seed
"""
import sys, random
from math import prod
import numpy as np
from gglob_matching import in_VkLM, random_nc_matching, PR
import gglobi_csp as C

G6 = [-2,-1,1,-4,4,0,0,3,3,2,3,-1,-2,-1,1,-2,6,3,3,4,4,-1,0,-4,-5,-2,0,-1,7,3,3,4,4,1,2,-1]

def sample_D(n, rng):
    X = [rng.random() < 1/3 for _ in range(n)]
    A = [x for x in range(n) if X[x] and not X[x-1] and not X[(x+1) % n]]
    used = set(); M = []
    for x in A: M.append((x, (x+1) % n)); used |= {x, (x+1) % n}
    rest = [x for x in range(n) if x not in used]
    off = rng.randrange(2) if rest else 0
    rest = rest[off:] + rest[:off]
    M += [(rest[2*i], rest[2*i+1]) for i in range(len(rest)//2)]
    return set(A), M

def find_S(z, n, sk):
    Ws = [C.witnesses(z, n, s) for s in sk]
    order = sorted(range(len(sk)), key=lambda k: len(Ws[k]))
    def rec(i, pts):
        if i == len(order): return pts
        for w in Ws[order[i]]:
            ps = pts | set(w)
            if not any(((p+1) % n) in ps for p in ps):
                r = rec(i+1, ps)
                if r is not None: return r
        return None
    return rec(0, set())

def certifies(y, M, n, sk):
    return all(not in_VkLM(y, M, n, s) for s in sk)

if __name__ == '__main__':
    N, ny, nM, seed = map(int, sys.argv[1:5]); rng = random.Random(seed)
    ps = PR[:N]; P = prod(ps); n = P*P; sk = [n//p for p in ps]
    ys = []
    if N == 2: ys.append(('G6', np.array(G6)))
    while len(ys) < ny:
        y = np.zeros(n, dtype=np.int64)
        kind = rng.choice(['sparse', 'orbits'])
        if kind == 'sparse':
            for _ in range(rng.randint(1, 6)): y[rng.randrange(n)] = rng.choice([1, 2, -1])
        else:
            for _ in range(rng.randint(2, 4)):
                d = rng.choice([s for s in sk] + [n // (ps[0]*ps[1])]); st = rng.randrange(n)
                y[[(st + j*d) % n for j in range(n//d)]] += 1
        if all(not np.array_equal(y, np.roll(y, -s)) for s in sk): ys.append((kind, y))
    for name, y in ys:
        z = [int(y[x] - y[(x+1) % n]) for x in range(n)]
        S = find_S(z, n, sk)
        nbr = {(x+d) % n for x in S for d in (-1, 1)} - S
        lb = (1/3)**len(S) * (2/3)**len(nbr)
        # deterministic check: M_S = adjacent pairs on S + adjacent completion (both offsets)
        detok = []
        for off in (0, 1):
            used = set(); M = []
            for x in S: M.append((x, (x+1) % n)); used |= {x, (x+1) % n}
            rest = [x for x in range(n) if x not in used]; rest = rest[off:] + rest[:off]
            M += [(rest[2*i], rest[2*i+1]) for i in range(len(rest)//2)]
            detok.append(certifies(y, M, n, sk))
        hitD = hitS = viol = 0
        for _ in range(nM):
            A, M = sample_D(n, rng)
            ok = certifies(y, M, n, sk); hitD += ok
            if S <= A:
                hitS += 1; viol += (not ok)
        hitU = sum(certifies(y, random_nc_matching(n, rng), n, sk) for _ in range(nM))
        print(f'{name:7s} M_S ok={detok} |S|={len(S)} bound={lb:.2e}  Pr_D[cert]={hitD}/{nM}  [S in A]={hitS} (violations {viol})  uniformNC={hitU}/{nM}', flush=True)
