from fractions import Fraction as F
import itertools

def crossing(p, q):
    if len(p) < 2 or len(q) < 2: return False
    a, b = sorted(p); c, d = sorted(q)
    return (a < c < b < d) or (c < a < d < b)

def rank(rows):
    A = [[F(x) for x in r] for r in rows]
    if not A: return 0
    n = len(A[0]); r = 0
    for col in range(n):
        piv = next((i for i in range(r, len(A)) if A[i][col] != 0), None)
        if piv is None: continue
        A[r], A[piv] = A[piv], A[r]
        for i in range(len(A)):
            if i != r and A[i][col] != 0:
                f = A[i][col] / A[r][col]
                A[i] = [x - f*y for x, y in zip(A[i], A[r])]
        r += 1
    return r

def inv(Mx):
    n = len(Mx); A = [[F(x) for x in r] + [F(int(i == j)) for j in range(n)] for i, r in enumerate(Mx)]
    for col in range(n):
        piv = next(i for i in range(col, n) if A[i][col] != 0)
        A[col], A[piv] = A[piv], A[col]
        p = A[col][col]; A[col] = [x / p for x in A[col]]
        for i in range(n):
            if i != col and A[i][col] != 0:
                f = A[i][col]; A[i] = [x - f*y for x, y in zip(A[i], A[col])]
    return [r[n:] for r in A]

def det(Mx):
    n = len(Mx); A = [[F(x) for x in r] for r in Mx]; d = F(1)
    for col in range(n):
        piv = next((i for i in range(col, n) if A[i][col] != 0), None)
        if piv is None: return F(0)
        if piv != col: A[col], A[piv] = A[piv], A[col]; d = -d
        d *= A[col][col]
        for i in range(col+1, n):
            f = A[i][col] / A[col][col]; A[i] = [x - f*y for x, y in zip(A[i], A[col])]
    return d

def components(n, edges):
    par = list(range(n))
    def f(x):
        while par[x] != x: par[x] = par[par[x]]; x = par[x]
        return x
    for e in edges:
        if len(e) == 2: par[f(e[0])] = f(e[1])
    comps = {}
    for v in range(n): comps.setdefault(f(v), set()).add(v)
    return list(comps.values())
