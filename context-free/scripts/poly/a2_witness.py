"""poly_A2: adversarial upper-bound attack on the S_N candidate (n = P_N^2, product region).
Usage: python3 a2_witness.py [part]   part in {small, prod36, lemmaA, all}

Witness model (AG strict, the only one-witness-per-prime model that is stratified, bounded.md L4/L5):
  system = one pair (i,j) per prime p | n with j-i = 0 mod n/p, x_i != x_j; pairs pairwise disjoint and
  non-crossing (nested or disjoint).  amb(x) = #systems.
Lex-canonical variant: prime p uses the FIRST mismatching pair in a fixed order; canonicity needs the
  equalities x_i = x_j on all earlier pairs of p.  The canonical piece is a stratified rigid/sign piece only
  if the union of all equality and mismatch pairs is pairwise disjoint and non-crossing (bounded.md L4, L7).
"""
import sys, itertools, random
from fractions import Fraction

def primes(n): return [p for p in range(2, n + 1) if n % p == 0 and all(p % q for q in range(2, p))]
def prim(e):
    n = len(e); return all(e != e[:n // p] * p for p in primes(n))
def lam(I, J):
    (a, b), (c, d) = I, J
    if len({a, b, c, d}) < 4: return False
    return b < c or d < a or (a < c and d < b) or (c < a and b < d)
def allpairs(n, p):
    s = n // p; return [(i, j) for i in range(n) for j in range(i + s, n, s)]

def systems(e, P, PAIRS):
    W = [[q for q in PAIRS[p] if e[q[0]] != e[q[1]]] for p in P]
    cnt = 0
    def rec(k, chosen):
        nonlocal cnt
        if k == len(W): cnt += 1; return
        for q in W[k]:
            if all(lam(q, c) for c in chosen): rec(k + 1, chosen + [q])
    rec(0, []); return cnt

def lex_ok(e, P, PAIRS):
    used = []
    for p in P:
        for q in PAIRS[p]:
            used.append(q)
            if e[q[0]] != e[q[1]]: break
    return all(lam(used[a], used[b]) for a in range(len(used)) for b in range(a))

def small(ns=(4, 9, 12)):
    print("| n | primes | primitive vectors in {0,1,2}^n | uncovered (AG strict) | min/mean/max #systems | lex-canonical realizable |")
    print("|---|---|---|---|---|---|")
    for n in ns:
        P = primes(n); PAIRS = {p: allpairs(n, p) for p in P}
        tot = unc = lexok = 0; mx = 0; s_sum = 0; mn = 10**9
        for e in itertools.product(range(3), repeat=n):
            if not prim(e): continue
            tot += 1; s = systems(e, P, PAIRS); s_sum += s
            mx = max(mx, s); mn = min(mn, s); unc += (s == 0); lexok += lex_ok(e, P, PAIRS)
        print(f"| {n} | {P} | {tot} | {unc} | {mn}/{s_sum/tot:.1f}/{mx} | {lexok} ({100*lexok/tot:.1f}%) |")

# ---- n = 36 product region: x = 2 + e2 + e3 (entries in {0..4}), fibers r = i mod 6, t = i // 6
PHI3 = [(0, 0, 0)] + list(set(itertools.permutations((1, -1, 0))))
def prod_vec(psi, phi):
    x = [2] * 36
    for i in range(36):
        r, t = i % 6, i // 6
        x[i] += psi[r] * (1 if t % 2 == 0 else -1) + phi[r][t % 3]
    return x
def prod36(samples=4000, seed=1):
    random.seed(seed); n = 36; P = [2, 3]; PAIRS = {p: allpairs(n, p) for p in P}
    rows = {}
    def one(psi, phi):
        x = prod_vec(psi, phi); assert min(x) >= 0 and max(x) <= 4
        m2 = sum(1 for r in range(6) if psi[r]); m3 = sum(1 for r in range(6) if any(phi[r]))
        assert prim(x) == (m2 > 0 and m3 > 0)
        return m2, m3, systems(x, P, PAIRS), lex_ok(x, P, PAIRS)
    # targeted: both perturbations in ONE common fiber / in two different fibers
    t1 = one([1, 0, 0, 0, 0, 0], [PHI3[1]] + [(0, 0, 0)] * 5)
    t2 = one([1, 0, 0, 0, 0, 0], [(0, 0, 0), PHI3[1]] + [(0, 0, 0)] * 4)
    print(f"same single fiber: systems={t1[2]}; different single fibers: systems={t2[2]}")
    unc_same = 0; cnt = 0
    for r in range(6):
        for s in (1, -1):
            for ph in PHI3[1:]:
                psi = [0] * 6; psi[r] = s; phi = [(0, 0, 0)] * 6; phi[r] = ph
                cnt += 1; unc_same += one(psi, phi)[2] == 0
    print(f"all {cnt} same-single-fiber vectors: uncovered {unc_same}")
    for _ in range(samples):
        psi = [random.choice((-1, 0, 1)) for _ in range(6)]
        phi = [random.choice(PHI3) for _ in range(6)]
        m2, m3, s, lx = one(psi, phi)
        if m2 == 0 or m3 == 0: continue
        R = rows.setdefault((m2, m3), [0, 0, 10**9, 0, 0])
        R[0] += 1; R[1] += s; R[2] = min(R[2], s); R[3] = max(R[3], s); R[4] += lx
    print("| m2 (#fibers e_2!=0) | m3 | samples | min/mean/max #systems | mean/(m2*m3) | lex-canonical ok |")
    print("|---|---|---|---|---|---|")
    for k in sorted(rows):
        c, ss, mn, mx, lx = rows[k]
        print(f"| {k[0]} | {k[1]} | {c} | {mn}/{ss/c:.1f}/{mx} | {ss/c/(k[0]*k[1]):.2f} | {lx} |")

# ---- Lemma A check: exact-equality certificate e_k^{(r)} = 0 inside one fiber of length L = P_N
def nc_partitions(S):
    if not S: yield []; return
    a = S[0]
    for k in range(len(S)):  # block of a ends... enumerate blocks containing a recursively (small L only)
        pass
    # generic: choose block B containing a as subset; remaining split into gaps (non-crossing)
    rest = S[1:]
    for r in range(len(rest) + 1):
        for comb in itertools.combinations(rest, r):
            B = (a,) + comb
            gaps = []; prev = a
            for b in comb:
                gaps.append([s for s in S if prev < s < b]); prev = b
            gaps.append([s for s in S if s > prev])
            def prod(i):
                if i == len(gaps): yield []; return
                for q in nc_partitions(gaps[i]):
                    for tail in prod(i + 1): yield q + tail
            for tail in prod(0): yield [B] + tail
def rank(rows):
    M = [list(map(Fraction, r)) for r in rows]; rk = 0; c = 0
    while M and c < len(M[0]):
        piv = next((i for i in range(rk, len(M)) if M[i][c] != 0), None)
        if piv is None: c += 1; continue
        M[rk], M[piv] = M[piv], M[rk]
        for i in range(len(M)):
            if i != rk and M[i][c] != 0:
                f = M[i][c] / M[rk][c]; M[i] = [a - f * b for a, b in zip(M[i], M[rk])]
        rk += 1; c += 1
    return rk
def lemmaA(L, p):
    basis = []  # F = p-periodic mean-zero functions on Z_L
    for a in range(p - 1):
        basis.append([(1 if t % p == a else 0) - (1 if t % p == p - 1 else 0) for t in range(L)])
    good = 0; total = 0
    for part in nc_partitions(list(range(L))):
        total += 1
        if any(len(B) < 2 for B in part): continue
        ok = True
        for B in part:
            R = [[f[t] for t in B] for f in basis]
            if rank(R) != 1: ok = False; break      # must carry exactly one functional g_C
            g = next(r for r in R if any(r))
            if sum(g) != 0: ok = False; break       # g_C fiber-balanced
        good += ok
    return total, good

if __name__ == '__main__':
    part = sys.argv[1] if len(sys.argv) > 1 else 'all'
    if part in ('small', 'all'): small()
    if part in ('prod36', 'all'): prod36()
    if part in ('lemmaA', 'all'):
        for L, p in [(6, 2), (6, 3), (10, 5), (10, 2), (12, 3)]:
            tot, good = lemmaA(L, p)
            print(f"Lemma A: fiber length {L}, p={p}: non-crossing partitions {tot}, admissible {good}")
