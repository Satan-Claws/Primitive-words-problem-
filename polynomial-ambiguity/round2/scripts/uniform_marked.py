"""uniform_marked.py -- two exposed witness chords (span n/p and span n/q, p<q primes) in one word.
For every relative order of the marked positions i < i+n/p, j < j+n/q (incl. one coincidence),
segment lengths l_0..l_k >= 0 satisfy two linear equations. We list the minimal-support (= extreme)
rays of the homogeneous cone {l >= 0, p*span_p = n, q*span_q = n} (constants dropped) and report the
largest support among them. Support >= 3 on an extreme ray => the length set is not stratified
(Ginsburg), i.e. the marked bounded language is not CF.  [computational illustration; the proof in
uniform.md section 3 is by hand on one pattern]."""
import itertools, sympy as sp

def patterns():
    labs = ['A1', 'A2', 'B1', 'B2']
    seen = set()
    for perm in itertools.permutations(labs):
        if perm.index('A1') > perm.index('A2') or perm.index('B1') > perm.index('B2'): continue
        seen.add(tuple((x,) for x in perm))
        for k in range(3):               # merge adjacent A/B pair into one position
            a, b = perm[k], perm[k+1]
            if a[0] != b[0]:
                seen.add(tuple((x,) for x in perm[:k]) + ((a, b),) + tuple((x,) for x in perm[k+2:]))
    return sorted(seen)

def analyse(p, q, pat):
    k = len(pat)                         # positions; segments 0..k
    L = sp.symbols(f'l0:{k+1}', nonnegative=True)
    pos = {}
    for idx, grp in enumerate(pat):
        for g in grp: pos[g] = idx
    n = sum(L)                          # homogeneous: marks dropped
    def span(a, b):                     # sum of segments strictly between position a and b
        return sum(L[pos[a]+1: pos[b]+1])
    eqs = [p*span('A1', 'A2') - n, q*span('B1', 'B2') - n]
    A = sp.Matrix([[sp.diff(e, v) for v in L] for e in eqs])
    rays = []
    for r in range(1, k+2):
        for S in itertools.combinations(range(k+1), r):
            sub = A[:, list(S)]
            ns = sub.nullspace()
            if len(ns) != 1: continue
            v = ns[0]; v = v / max(abs(x) for x in v if x != 0)
            if all(x > 0 for x in v) or all(x < 0 for x in v):
                if not any(set(R) < set(S) for R, _ in rays):
                    rays.append((S, [abs(x) for x in v]))
    return rays

if __name__ == '__main__':
    for p, q in [(2, 3), (2, 5), (3, 5)]:
        print(f'--- p={p}, q={q}')
        for pat in patterns():
            rays = analyse(p, q, pat)
            name = ' '.join('='.join(g) for g in pat)
            if not rays:
                print(f'{name:24s} infeasible (no nonzero cone)'); continue
            ms = max(len(S) for S, _ in rays)
            print(f'{name:24s} extreme rays {[(S, [str(x) for x in v]) for S, v in rays]}  max support {ms}')

def markings_single_defect(p, q, m):
    """All (i, j) with w[i]!=w[i+n/p], w[j]!=w[j+n/q] for w = a^{n-2} b b, n = p*q*m.
    Returns block lengths (x, y, z) = a-runs before/between/after the two a-marks (before the bb)."""
    n = p*q*m; w = 'a'*(n-2) + 'bb'
    I = [i for i in range(n - n//p) if w[i] != w[i + n//p]]
    J = [j for j in range(n - n//q) if w[j] != w[j + n//q]]
    out = []
    for i in I:
        for j in J:
            lo, hi = sorted((i, j))
            out.append((i, j, (lo, hi - lo - 1, n - 3 - hi)))
    return out

if __name__ == '__main__':
    print('--- markings of a^{n-2}bb (every marking has 3 a-blocks ~ linear in m with positive slopes)')
    for p, q in [(2, 3), (2, 5), (3, 5)]:
        for m in (3, 10):
            print(p, q, m, markings_single_defect(p, q, m))
