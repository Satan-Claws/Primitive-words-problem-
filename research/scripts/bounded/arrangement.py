# Subspace-arrangement computation of the "hard" set for the near-constant family,
# against non-crossing perfect matchings only.
# Hard set H = { delta : for all NC perfect matchings M, exists d with delta in span(M)+V_d } \ union V_d
# Represented as a union of subspaces (each given by a basis), exact arithmetic mod a large prime
import sys, random
P = 2**31 - 1

def nc_matchings(lo, hi):
    if lo >= hi:
        yield []
        return
    for j in range(lo+1, hi, 2):
        for left in nc_matchings(lo+1, j):
            for right in nc_matchings(j+1, hi):
                yield [(lo, j)] + left + right

def primes_of(n):
    return [p for p in range(2, n+1) if n % p == 0 and all(p % q for q in range(2, p))]

def rref(rows, ncols):
    rows = [r[:] for r in rows]
    piv = []
    r = 0
    for c in range(ncols):
        pr = None
        for i in range(r, len(rows)):
            if rows[i][c] % P:
                pr = i; break
        if pr is None: continue
        rows[r], rows[pr] = rows[pr], rows[r]
        inv = pow(rows[r][c], P-2, P)
        rows[r] = [(x*inv) % P for x in rows[r]]
        for i in range(len(rows)):
            if i != r and rows[i][c] % P:
                f = rows[i][c]
                rows[i] = [(a - f*b) % P for a, b in zip(rows[i], rows[r])]
        piv.append(c)
        r += 1
        if r == len(rows): break
    return rows[:r], piv

def nullspace(rows, ncols):
    R, piv = rref(rows, ncols)
    free = [c for c in range(ncols) if c not in piv]
    basis = []
    for f in free:
        v = [0]*ncols
        v[f] = 1
        for i, c in enumerate(piv):
            v[c] = (-R[i][f]) % P
        basis.append(v)
    return basis

def W_perp(n, M, d):
    # functionals f with f(e_i+e_j)=0 for pairs and f(1_class)=0 for classes mod d
    rows = []
    for (i, j) in M:
        r = [0]*n; r[i] = 1; r[j] = 1; rows.append(r)
    for c in range(d):
        r = [0]*n
        for i in range(c, n, d): r[i] = 1
        rows.append(r)
    return nullspace(rows, n)

def Vd_perp(n, d):
    rows = []
    for c in range(d):
        r = [0]*n
        for i in range(c, n, d): r[i] = 1
        rows.append(r)
    return nullspace(rows, n)

class Sub:
    # subspace given by constraint rows (functionals) in rref
    def __init__(self, cons, n):
        self.n = n
        self.cons, _ = rref(cons, n) if cons else ([], [])
        self.key = tuple(tuple(r) for r in self.cons)
        self.basis = nullspace(self.cons, n) if self.cons else [[int(i==j) for j in range(n)] for i in range(n)]

def contained_in(basis, cons):
    # basis vectors all satisfy cons?
    for f in cons:
        for v in basis:
            if sum(a*b for a, b in zip(f, v)) % P:
                return False
    return True

def run(n, order='random', seed=0, verbose=True):
    ps = primes_of(n)
    ds = [n//p for p in ps]
    Vp = {d: Vd_perp(n, d) for d in ds}
    Ms = list(nc_matchings(0, n))
    if order == 'random':
        random.Random(seed).shuffle(Ms)
    fam = {(): Sub([], n)}
    for t, M in enumerate(Ms):
        Wp = [W_perp(n, M, d) for d in ds]
        new = {}
        for key, U in fam.items():
            if any(contained_in(U.basis, w) for w in Wp):
                new[key] = U
                continue
            for w in Wp:
                V = Sub(U.cons + w, n)
                # prune if V subset of some V_d (non-primitive)
                if any(contained_in(V.basis, Vp[d]) for d in ds):
                    continue
                new[V.key] = V
        # remove redundant (contained in another)
        items = list(new.values())
        keep = {}
        for U in items:
            red = False
            for U2 in items:
                if U2 is not U and len(U2.basis) > len(U.basis) and contained_in(U.basis, U2.cons):
                    red = True; break
            if not red:
                keep[U.key] = U
        fam = keep
        if verbose and (t % 50 == 0 or not fam):
            print(t, len(fam), sorted(len(U.basis) for U in fam.values())[:10], flush=True)
        if not fam:
            return t, fam
    return len(Ms), fam

if __name__ == '__main__':
    n = int(sys.argv[1])
    t, fam = run(n)
    print('n', n, 'processed', t, 'surviving subspaces', len(fam))
    for U in list(fam.values())[:5]:
        print('dim', len(U.basis))
