"""audit_r3_i2_sat: independent SAT check of Lemma I2 (audit of r3_i2.md).
For z on Z_n (n=P^2) decides by SAT whether there is S with one k-witness {a,b} (a = b mod n/p_k, z_a != z_b)
per k and no two cyclically consecutive points of S.  Does not use residue/CRT structure for the check.
Adversarial generator: residue runs (adjacent, incl. wrap) with u_r = small-alphabet functions of random
coordinate subsets K_r (point masses / one-coord / random), other residues constant.
Usage: audit_r3_i2_sat.py trials seed p1 p2 ...
"""
import sys, random, itertools
from math import prod
from pysat.solvers import Minisat22

def i2_sat(z, ps):
    n = len(z); N = len(ps)
    pv = {}; nv = [0]
    def var(key):
        if key not in pv: nv[0] += 1; pv[key] = nv[0]
        return pv[key]
    cl = []
    for k, p in enumerate(ps):
        s = n // p; lits = []
        for a in range(n):
            for j in range(1, p):
                b = (a + j * s) % n
                if a < b and z[a] != z[b]:
                    v = var(('w', k, a, b)); lits.append(v)
                    cl.append([-v, var(('x', a))]); cl.append([-v, var(('x', b))])
        if not lits: return None  # z in V_k
        cl.append(lits)
    for x in range(n):
        if ('x', x) in pv and ('x', (x + 1) % n) in pv:
            cl.append([-pv[('x', x)], -pv[('x', (x + 1) % n)]])
    with Minisat22(bootstrap_with=cl) as s:
        return s.solve()

def gen(ps, rng):
    N = len(ps); P = prod(ps); n = P * P
    coords = [tuple(t % p for p in ps) for t in range(P)]
    z = [0] * n
    mode = rng.choice(['private', 'run', 'pm', 'pair'])
    L = rng.randint(1, min(P, 2 * N + 1)); r0 = rng.randrange(P)
    for i in range(L):
        r = (r0 + i) % P
        if mode == 'private':
            K = [i % N]
        elif mode == 'pair':
            K = rng.sample(range(N), min(2, N)) if N > 2 else [rng.randrange(N)]
        else:
            K = rng.sample(range(N), rng.randint(1, max(1, N - 1)))
        if mode in ('pm', 'private') or rng.random() < .5:
            tgt = tuple(rng.randrange(ps[k]) for k in K)
            f = lambda c, K=K, tgt=tgt: 1 if tuple(c[k] for k in K) == tgt else 0
        else:
            tab = {}
            f = lambda c, K=K, tab=tab: tab.setdefault(tuple(c[k] for k in K), rng.randrange(2))
        for t in range(P):
            z[r + P * t] = f(coords[t])
    return z

if __name__ == '__main__':
    T, seed = int(sys.argv[1]), int(sys.argv[2]); ps = list(map(int, sys.argv[3:]))
    rng = random.Random(seed); prim = fail = 0
    for _ in range(T):
        z = gen(ps, rng); r = i2_sat(z, ps)
        if r is None: continue
        prim += 1
        if not r:
            fail += 1; print('COUNTEREXAMPLE', z); break
    print(ps, 'primitive', prim, 'I2 failures', fail)
