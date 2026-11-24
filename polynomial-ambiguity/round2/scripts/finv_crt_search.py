"""finv: search full-rank laminar pair-supported bases B_D (entries <= K, l1-norm <= K) with
   ZB_D = Lambda_D := {x in Z^m : l.x = 0 mod D},  l = (1,2,...,m),  D prime,
   and the all-ones vector in the open cone of B_D (common interior direction).
Used for the CRT construction in reports/finv.md section 4."""
import itertools, sys
from sympy import Matrix, primerange

def cands(m, K, D, l):
    out = []
    for s in range(m):
        for a in range(1, K + 1):
            v = [0] * m; v[s] = a
            if sum(li * vi for li, vi in zip(l, v)) % D == 0: out.append(((s, s), tuple(v)))
        for t in range(s + 1, m):
            for a in range(1, K):
                for b in range(1, K - a + 1):
                    v = [0] * m; v[s] = a; v[t] = b
                    if sum(li * vi for li, vi in zip(l, v)) % D == 0: out.append(((s, t), tuple(v)))
    return out

def crosses(p, q):
    (s, t), (u, w) = p, q
    return (s < u < t < w) or (u < s < w < t)

def search(m, K, D):
    l = list(range(1, m + 1))
    C = cands(m, K, D, l)
    # greedy-ish DFS over laminar independent subsets of size m with |det| = D and ones in open cone
    best = None
    def dfs(start, chosen):
        nonlocal best
        if best: return
        if len(chosen) == m:
            M = Matrix([list(C[i][1]) for i in chosen]).T
            d = M.det()
            if abs(d) != D: return
            lam = M.LUsolve(Matrix([1] * m))
            if all(x > 0 for x in lam): best = [C[i] for i in chosen]
            return
        for i in range(start, len(C)):
            if any(crosses(C[i][0], C[j][0]) for j in chosen): continue
            M = Matrix([list(C[j][1]) for j in chosen + [i]])
            if M.rank() < len(chosen) + 1: continue
            dfs(i + 1, chosen + [i])
            if best: return
    dfs(0, [])
    return best

if __name__ == "__main__":
    m, K = int(sys.argv[1]), int(sys.argv[2])
    for D in primerange(2, m * K + 1):
        B = search(m, K, D)
        print(D, "FOUND" if B else "none", [v for _, v in B] if B else "")
