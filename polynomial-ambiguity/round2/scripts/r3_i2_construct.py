"""r3_i2_construct: constructive proof of Lemma I2 (R2/r3_i2.md), implemented and checked.

Given z on Z_n, n = P^2, P = prod(ps) (squarefree, contains 2 or not -- not needed), builds S exactly as in the
proof: residue coordinates x = r + P t, K_r = coordinates u_r depends on, a MINIMUM cover I of [N] by the K_r,
then (A) |I|=1 hub, (B) |I|=2 adjacent: projection trick, (C) otherwise: path 2-colouring of a shared free
coordinate on each adjacent pair.  Verifies independently: no two cyclically consecutive points, |S| <= 2N,
a k-witness for every k.  Inputs: random structured adversarial z (cylinder point masses / one-coordinate
functions on runs of adjacent residues, incl. the wrap), sparse random z, small-alphabet random z.
Usage: r3_i2_construct.py trials seed p1 p2 ...
"""
import sys, random, itertools
from math import prod

def setup(ps):
    P = prod(ps); n = P * P
    coords = [tuple(t % p for p in ps) for t in range(P)]
    index = {c: t for t, c in enumerate(coords)}
    return P, n, coords, index

def construct(z, ps):
    N = len(ps); P, n, coords, index = setup(ps)
    u = [[z[r + P * t] for t in range(P)] for r in range(P)]
    def depends(r, k):
        step = P // ps[k]  # shift changing only coord k
        return any(u[r][t] != u[r][(t + step) % P] for t in range(P))
    K = [frozenset(k for k in range(N) if depends(r, k)) for r in range(P)]
    if set().union(*K) != set(range(N)):
        return None  # not primitive
    cand = sorted({k for k in K if k}, key=len, reverse=True)
    rep = {}
    for r in range(P):
        if K[r]: rep.setdefault(K[r], r)
    # minimum cover over residues (search over subsets of residues; dedupe by K-set but keep adjacency info)
    full = frozenset(range(N))
    I = None
    for size in range(1, N + 1):
        # residues with distinct, non-dominated useful K sets; brute force over residues with nonempty K
        rs = [r for r in range(P) if K[r]]
        # reduce: for size<=2 brute force is fine; for larger sizes pick any cover (minimality only needs
        # inclusion-minimal + no covering adjacent pair, enforced below)
        if size <= 2:
            for comb in itertools.combinations(rs, size):
                if frozenset().union(*(K[r] for r in comb)) == full:
                    I = list(comb); break
        else:
            # greedy cover then prune to inclusion-minimal
            cov, I = set(), []
            for r in sorted(rs, key=lambda r: -len(K[r])):
                if not K[r] <= cov: I.append(r); cov |= K[r]
                if cov == full: break
            changed = True
            while changed:
                changed = False
                for r in list(I):
                    rest = [s for s in I if s != r]
                    if frozenset().union(*(K[s] for s in rest)) == full:
                        I = rest; changed = True; break
        if I: break
    # assignment of primes to residues (each k to one r in I with k in K_r)
    def witness(r, k, fixed):
        """k-witness in R_r with coords outside K_r set to `fixed` (dict coord->value); returns (t,t')."""
        step = P // ps[k]
        for t in range(P):
            c = coords[t]
            if any(c[j] != v for j, v in fixed.items()): continue
            for j in range(1, ps[k]):
                t2 = (t + j * step) % P
                if u[r][t] != u[r][t2]: return (t, t2)
        raise AssertionError('no witness')
    pairs = {}  # k -> (x, x')
    def emit(r, k, fixed):
        t, t2 = witness(r, k, fixed)
        pairs[k] = (r + P * t, r + P * t2)
    if len(I) == 1:
        case = 'A'
        for k in range(N): emit(I[0], k, {})
    elif len(I) == 2 and (I[1] - I[0]) % P in (1, P - 1):
        case = 'B'
        r, rho = (I[0], I[1]) if (I[1] - I[0]) % P == 1 else (I[1], I[0])  # rho = r+1
        eps = 1 if r == P - 1 else 0
        A, B = K[r], K[rho]
        Bo, Ao = sorted(full - A), sorted(full - B)
        def try_side(first, second, Fo, sign):
            # second handles Fo = K[second] \ K[first] with free coords set arbitrarily (0);
            # first handles all of K[first] with free coords Fo set to phi avoiding projection of second's points
            sec = {}
            freeS = {j: 0 for j in sorted(full - K[second])}
            for k in Fo: sec[k] = witness(second, k, freeS)
            proj = {tuple(coords[t][j] for j in Fo) for pr in sec.values() for t in pr}
            # adjacency: x in R_r, x+1 in R_rho; t(x+1) = t(x) + eps
            shift = eps * sign
            for phi in itertools.product(*[range(ps[j]) for j in Fo]):
                img = tuple((phi[i] - shift) % ps[j] for i, j in enumerate(Fo))
                if img not in proj:
                    for k, (t, t2) in sec.items(): pairs[k] = (second + P * t, second + P * t2)
                    fixed = dict(zip(Fo, phi))
                    for k in sorted(K[first]): emit(first, k, fixed)
                    return True
            return False
        # side 1: r handles A, rho handles Bo, phi on Bo for points of R_r;
        # point t in R_r adjacent to t+eps in R_rho, so need phi + eps not in proj  -> phi - (-eps)
        ok = try_side(r, rho, Bo, -1) or try_side(rho, r, Ao, +1)
        assert ok, 'case B failed'
    else:
        case = 'C'
        Iset = set(I)
        assign = {}
        for k in range(N):
            assign[k] = next(r for r in I if k in K[r])
        phi = {r: {j: 0 for j in sorted(full - K[r])} for r in I}
        # paths: start at residues whose predecessor is not in I
        for r0 in I:
            if (r0 - 1) % P in Iset: continue
            r = r0
            while (r + 1) % P in Iset:
                s = (r + 1) % P; eps = 1 if r == P - 1 else 0
                m = min(full - K[r] - K[s])  # exists by minimality
                phi[s][m] = (phi[r][m] + eps + 1) % ps[m]  # differs from t_m(r)+eps
                r = s
        for k in range(N): emit(assign[k], k, phi[assign[k]])
    S = sorted({x for pr in pairs.values() for x in pr})
    return case, S, pairs

def verify(z, ps, S, pairs):
    N = len(ps); P, n, _, _ = setup(ps)
    Ss = set(S)
    assert len(S) <= 2 * N
    assert all((x + 1) % n not in Ss for x in S), 'adjacent points'
    for k in range(N):
        a, b = pairs[k]
        assert (a - b) % (n // ps[k]) == 0 and z[a] != z[b]
    return True

def gen(rng, ps, mode):
    N = len(ps); P, n, coords, _ = setup(ps)
    z = [0] * n
    if mode == 'struct':
        L = rng.randint(1, min(N + 2, P)); r0 = rng.choice([0, P - 1, P - 2, rng.randrange(P)])
        for i in range(L):
            r = (r0 + i) % P
            for _ in range(rng.choice([1, 1, 2])):
                Kk = [k for k in range(N) if rng.random() < 0.4] or [rng.randrange(N)]
                c = [rng.randrange(p) for p in ps]; a = rng.choice([1, 2, -1])
                one = rng.random() < 0.3
                for t in range(P):
                    if (coords[t][Kk[0]] == c[Kk[0]]) if one else all(coords[t][k] == c[k] for k in Kk):
                        z[r + P * t] += a
    elif mode == 'private':  # each prime private to its own adjacent residue, point mass on that coordinate
        r0 = rng.randrange(P); perm = list(range(N)); rng.shuffle(perm)
        for i, k in enumerate(perm):
            r = (r0 + i) % P; c = rng.randrange(ps[k])
            for t in range(P):
                if coords[t][k] == c: z[r + P * t] = 1
    elif mode == 'sparse':
        for _ in range(rng.randint(1, 2 * N)): z[rng.randrange(n)] += rng.choice([1, -1, 2])
    else:
        for x in range(n): z[x] = rng.randrange(2) if rng.random() < 0.05 else 0
    return z

if __name__ == '__main__':
    trials, seed = int(sys.argv[1]), int(sys.argv[2]); ps = list(map(int, sys.argv[3:]))
    rng = random.Random(seed); from collections import Counter
    cnt = Counter()
    for i in range(trials):
        mode = ['struct', 'private', 'sparse', 'rand'][i % 4]
        z = gen(rng, ps, mode)
        res = construct(z, ps)
        if res is None: cnt['nonprim'] += 1; continue
        case, S, pairs = res
        verify(z, ps, S, pairs); cnt[(mode, case)] += 1
    print('ps', ps, dict(cnt), 'ALL VERIFIED')
