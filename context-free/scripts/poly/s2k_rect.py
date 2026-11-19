"""S2K: rectangle-cone cover of E_n = primitive exponent vectors, n = p^a q^b.
Rectangle R(i;A,B) = {i, i+A, i+A+B, i+B} (A in (n/p)Z, B in (n/q)Z, nonzero mod n).
u = x[i+A]-x[i+B], w = x[i+A+B]-x[i]. On V_p: u=-w; on V_q: u=w. So |u|!=|w| => x in E.
Cone pieces (4 per rectangle): w>|u|, w<-|u|, u>|w|, u<-|w|; each a stratified linear set
(diagonals non-crossing; extra periods from one endpoint of the dominant diagonal to both
endpoints of the other). Plus B1 pieces sign(L(x)) for L in a basis of W_n^perp.
Usage: python3 s2k_rect.py box6 B   (exhaustive n=6, entries<=B: cover, ply, linear-set==region)
       python3 s2k_rect.py sample n p q T   (W_n samples: uncovered E∩W_n points?)"""
import sys, itertools, random
from fractions import Fraction

def periodic(x, d):
    n = len(x); return all(x[i] == x[(i+d) % n] for i in range(n))
def inE(x, primes):
    n = len(x); return not any(periodic(x, n//p) for p in primes)
def rects(n, p, q, multiples=False):
    As = [k*(n//p) % n for k in range(1, p)] if multiples else [n//p]
    Bs = [k*(n//q) % n for k in range(1, q)] if multiples else [n//q]
    out = set()
    for A in As:
        for B in Bs:
            for i in range(n):
                out.add((i, (i+A) % n, (i+A+B) % n, (i+B) % n))
    return sorted(out)
def cones(x, R):
    i, j, k, l = R; u = x[j]-x[l]; w = x[k]-x[i]; c = []
    if w > abs(u): c.append('w+')
    if -w > abs(u): c.append('w-')
    if u > abs(w): c.append('u+')
    if -u > abs(w): c.append('u-')
    return c

def perp_basis(n, p, q):
    # rows spanning W_n^perp, W_n = V_p + V_q ; exact rational nullspace
    gens = []
    for d in (n//p, n//q):
        for r in range(d):
            gens.append([1 if t % d == r else 0 for t in range(n)])
    M = [list(map(Fraction, g)) for g in gens]
    # nullspace of M (vectors L with M L = 0)
    rows, piv = [r[:] for r in M], []
    rr = 0
    for c in range(n):
        pr = next((r for r in range(rr, len(rows)) if rows[r][c] != 0), None)
        if pr is None: continue
        rows[rr], rows[pr] = rows[pr], rows[rr]
        pv = rows[rr][c]; rows[rr] = [v/pv for v in rows[rr]]
        for r in range(len(rows)):
            if r != rr and rows[r][c] != 0:
                f = rows[r][c]; rows[r] = [a-f*b for a, b in zip(rows[r], rows[rr])]
        piv.append(c); rr += 1
    free = [c for c in range(n) if c not in piv]; basis = []
    for f in free:
        v = [Fraction(0)]*n; v[f] = Fraction(1)
        for r, c in enumerate(piv): v[c] = -rows[r][f]
        basis.append(v)
    return basis

def linset_members(R, cone, n, Bx):
    """enumerate the stratified linear set (base + N-periods) inside box, return set"""
    i, j, k, l = R
    e = lambda *ps: tuple(sum(1 for t in ps if t == s) for s in range(n))
    free = [s for s in range(n) if s not in R]
    # dominant diagonal (a,b) with sign: value b-a must exceed |other|
    if cone == 'w+': a, b, oth = i, k, (l, j)
    elif cone == 'w-': a, b, oth = k, i, (l, j)
    elif cone == 'u+': a, b, oth = l, j, (i, k)
    else: a, b, oth = j, l, (i, k)
    c0, d0 = oth
    # x_b - x_a > |x_d0 - x_c0| ; periods: a+b, b, c0+d0, b+c0, b+d0, singletons free
    base = e(b)
    per = [e(a, b), e(b), e(c0, d0), e(b, c0), e(b, d0)] + [e(s) for s in free]
    out = set()
    for lam in itertools.product(range(Bx+1), repeat=len(per)):
        v = list(base)
        for L, P in zip(lam, per):
            if L:
                for s in range(n): v[s] += L*P[s]
        if max(v) <= Bx: out.add(tuple(v))
    return out, per

def noncross(per, n):
    ch = [tuple(s for s in range(n) if P[s]) for P in per]
    ch = [c for c in ch if len(c) == 2]
    for (a, b) in ch:
        for (c, d) in ch:
            if a < c < b < d: return False
    return True

def box6(Bx):
    n, p, q = 6, 2, 3; Rs = rects(n, p, q); L = perp_basis(n, p, q)
    E = [x for x in itertools.product(range(Bx+1), repeat=n) if inE(x, (p, q))]
    print('rectangles', Rs, ' perp basis', [[int(t) for t in v] for v in L])
    # linear-set == region, and stratification
    ok = True
    for R in Rs:
        for cn in ('w+', 'w-', 'u+', 'u-'):
            S, per = linset_members(R, cn, n, Bx)
            reg = {x for x in itertools.product(range(Bx+1), repeat=n) if cn in cones(x, R)}
            ok &= (S == reg) and noncross(per, n) and all(inE(x, (p, q)) for x in S)
    print('linear sets == cone regions, stratified, inside E:', ok)
    unc, ply, plyW, nW = 0, 0, 0, 0
    for x in E:
        c = sum(len(cones(x, R)) for R in Rs)
        b = sum(1 for v in L if sum(a*t for a, t in zip(v, x)) != 0)
        if c + b == 0: unc += 1
        ply = max(ply, c+b)
        if b == 0: nW += 1; plyW = max(plyW, c)
    print(f'|E∩box|={len(E)} uncovered={unc} maxply(all)={ply} |E∩W6∩box|={nW} maxply on W6={plyW}')

def sample(n, p, q, T, mult):
    Rs = rects(n, p, q, mult); A, B = n//p, n//q; unc = 0; tot = 0; ex = None
    for _ in range(T):
        a = [random.randint(0, 3) for _ in range(A)]; b = [random.randint(0, 3) for _ in range(B)]
        x = tuple(a[t % A]+b[t % B] for t in range(n))
        if not inE(x, (p, q)): continue
        tot += 1
        if sum(len(cones(x, R)) for R in Rs) == 0:
            unc += 1; ex = ex or (x, a, b)
    print(f'n={n} rects={len(Rs)} multiples={mult}: E∩W samples={tot} uncovered={unc} example={ex}')

if __name__ == '__main__':
    if sys.argv[1] == 'box6': box6(int(sys.argv[2]))
    else: sample(int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), len(sys.argv) > 6)
