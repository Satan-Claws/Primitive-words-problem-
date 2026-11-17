# Exhaustive (over support patterns) check of Lemma 4.2 for M=2,3 with several weightings incl. multi-edges.
# Checks: (a) W subset span V => dim span V >= 2M-1;
#         (b) at most one component of the support graph contains a pair {i, M+i};
#         (c) corollary used in section 5: for V linearly independent with W in span V,
#             #{v : n_v vanishes on W} <= dim span V - (2M-1)   (i.e. |V_0| >= 2M-1).
import itertools, random
from common import crossing, components, rank
random.seed(7)

def vecs_for(n, edges, loops, wmode):
    V = []
    for p in loops:
        v = [0]*n; v[p] = random.randint(1, 3) if wmode else 1; V.append(v)
    for (p, q) in edges:
        a, b = ((random.randint(1, 3), random.randint(1, 3)) if wmode else (1, 1))
        v = [0]*n; v[p] = a; v[q] = b; V.append(v)
        if wmode == 2 and random.random() < 0.3:   # multi-edge
            v = [0]*n; v[p] = random.randint(1, 3); v[q] = random.randint(1, 3); V.append(v)
    return V

def independent_subset(V):
    B = []
    for v in V:
        if rank(B + [v]) > len(B): B.append(v)
    return B

def coord_functional_vanishing(B, M):
    # number of v in basis B with n_v(e_i+e_{M+i}) = 0 for all i
    # solve w = sum a_v v for each w in W; use least-squares-free exact elimination
    from fractions import Fraction as Fr
    n = 2*M; k = len(B)
    vanish = [True]*k
    for i in range(M):
        w = [0]*n; w[i] = 1; w[M+i] = 1
        # solve B^T a = w   (n equations, k unknowns), consistent by assumption
        A = [[Fr(B[j][r]) for j in range(k)] + [Fr(w[r])] for r in range(n)]
        row = 0; pivcols = []
        for col in range(k):
            piv = next((r for r in range(row, n) if A[r][col] != 0), None)
            if piv is None: continue
            A[row], A[piv] = A[piv], A[row]
            p = A[row][col]; A[row] = [x/p for x in A[row]]
            for r in range(n):
                if r != row and A[r][col] != 0:
                    f = A[r][col]; A[r] = [x - f*y for x, y in zip(A[r], A[row])]
            pivcols.append(col); row += 1
        sol = [Fr(0)]*k
        for r, col in enumerate(pivcols): sol[col] = A[r][k]
        for j in range(k):
            if sol[j] != 0: vanish[j] = False
    return sum(vanish)

for M in (2, 3):
    n = 2*M
    pairs = list(itertools.combinations(range(n), 2))
    edgesets = []
    def rec(i, ch):
        if i == len(pairs): edgesets.append(ch); return
        rec(i+1, ch)
        if all(not crossing(pairs[i], e) for e in ch): rec(i+1, ch + [pairs[i]])
    rec(0, [])
    W = [[1 if j in (i, M+i) else 0 for j in range(n)] for i in range(M)]
    tests = viol_a = viol_b = viol_c = 0; mindim = {}
    for E in edgesets:
        for mask in range(1 << n):
            loops = [p for p in range(n) if mask >> p & 1]
            for wmode in ((0, 1, 2) if M == 2 else (0, 2)):
                V = vecs_for(n, E, loops, wmode)
                r = rank(V)
                if rank(V + W) != r: continue
                tests += 1
                if r < n - 1: viol_a += 1; print('VIOL a', M, E, loops, V)
                comps = components(n, E)
                withpair = [C for C in comps if any(i in C and M+i in C for i in range(M))]
                if len(withpair) > 1: viol_b += 1; print('VIOL b', M, E)
                B = independent_subset(V)
                z = coord_functional_vanishing(B, M)
                if z > r - (n - 1): viol_c += 1; print('VIOL c', M, E, loops, B, z)
    print(f'M={M}: non-crossing edge sets {len(edgesets)}, weighted families with W in span V: {tests}, '
          f'violations (a) {viol_a} (b) {viol_b} (c) {viol_c}')

# Contrast: the crossing family {e1+e3, e2+e4, e4} (M=2, the 'x1=y1, x2<y2' piece) violates (a)/(c):
V = [[1,0,1,0],[0,1,0,1],[0,0,0,1]]
print('crossing example: dim', rank(V), '(needs >= 3: ok), W in span:', rank(V+[[1,0,1,0],[0,1,0,1]]) == rank(V),
      ' #vanishing functionals', coord_functional_vanishing(V, 2), '> dim-(2M-1) =', rank(V) - 3)
