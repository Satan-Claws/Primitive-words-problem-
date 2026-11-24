"""gglobi_struct: structured adversarial test of Lemma I2 (R2/gglob_i.md).

Residue decomposition x = r + P t (r, t in Z_P), u_r(t) = z_{r+Pt}.  V_k restricted to R_r = functions of t
not depending on the k-th CRT coordinate of t.  Adversarial z: on a run of consecutive residues r0..r0+L-1
(including the wrap P-1 -> 0) put 'cylinder point masses' u_r = alpha * 1[t_K = c_K] (sparsest function depending
exactly on the coordinate set K = K_r), sums of two such, or pure one-coordinate functions; other residues constant.
This forces the residue-level transversal problem to fail as often as possible (adjacent private residues).
Reports: #instances, #primitive, #with NO admissible witness set (Lemma I2 failures).
Usage: gglobi_struct.py N trials seed
"""
import sys, random, itertools
from math import prod
from gglobi_csp import solve, PR

def crt(t, P, ps):
    return tuple(t % p for p in ps)

def run(N, trials, seed):
    rng = random.Random(seed)
    ps = PR[:N]; P = prod(ps); n = P * P; sk = [n // p for p in ps]
    coords = [crt(t, P, ps) for t in range(P)]
    stats = dict(inst=0, prim=0, fail=0)
    fails = []
    for _ in range(trials):
        L = rng.randint(1, min(N + 1, P))
        r0 = rng.choice([0, P - 1, P - 2, rng.randrange(P)])
        z = [0] * n
        for i in range(L):
            r = (r0 + i) % P
            u = [0] * P
            for _rep in range(rng.choice([1, 1, 2])):
                K = [k for k in range(N) if rng.random() < 0.5] or [rng.randrange(N)]
                c = [rng.randrange(p) for p in ps]
                a = rng.choice([1, 2, -1])
                kind = rng.random()
                for t in range(P):
                    if kind < 0.7:
                        if all(coords[t][k] == c[k] for k in K): u[t] += a
                    else:  # function of one coordinate
                        k = K[0]; u[t] += a * (coords[t][k] == c[k])
            for t in range(P): z[r + P * t] = u[t]
        stats['inst'] += 1
        c = solve(z, n, sk, count_cap=1)
        if c is None: continue
        stats['prim'] += 1
        if c == 0:
            stats['fail'] += 1; fails.append(z)
    return stats, fails

if __name__ == '__main__':
    N, trials, seed = map(int, sys.argv[1:4])
    st, fails = run(N, trials, seed)
    print(st)
    for z in fails[:3]:
        print('FAIL z support', [(i, v) for i, v in enumerate(z) if v])
