r"""finv CRT construction check (reports/finv.md section 4).
Blocks 0..m-1, l(x) = sum_j (-2)^j x_j. Chain C = {2e_j + e_{j+1}} spans ker l /\ Z^m exactly.
For odd prime t < m: w_t = e_0 + e_t, l(w_t) = 1 - 2^t = -D_t, D_t = 2^t - 1 (pairwise coprime).
B_t = C + {w_t}: laminar (pairs {j,j+1} and {0,t} never cross), entries <= 2, ||v||_1 <= 3, d = 0, full rank,
Z B_t = {x : l(x) = 0 mod D_t}.  Checks: |det B_t| = D_t; omega = 2*(2,3,..,3,1) + e_1 in open cone of every B_t;
offsets c_t (negabinary digits, +1) with random residues; max f over a box vs number of pieces."""
import itertools, random
import numpy as np
from sympy import Matrix, isprime

def basis(m, t):
    V = []
    for j in range(m - 1):
        v = [0] * m; v[j] = 2; v[j + 1] = 1; V.append(v)
    w = [0] * m; w[0] = 1; w[t] = 1; V.append(w)
    return V

def ell(x):
    return sum(((-2) ** j) * xj for j, xj in enumerate(x))

def crosses(p, q):
    (s, t), (u, w) = p, q
    return (s < u < t < w) or (u < s < w < t)

def main(m=30, seed=1, box=3):
    random.seed(seed)
    ts = [t for t in range(3, m) if isprime(t)]
    lam_star = [1] * (m - 1)
    omega = [0] * m
    for j in range(m - 1):
        omega[j] += 2 * 2; omega[j + 1] += 2 * 1
    omega[1] += 1
    pieces = []
    for t in ts:
        V = basis(m, t)
        supp = [tuple(i for i in range(m) if v[i]) for v in V]
        supp = [(s[0], s[-1]) for s in supp]
        assert not any(crosses(a, b) for a in supp for b in supp)
        M = Matrix(V).T
        D = 2 ** t - 1
        assert abs(M.det()) == D, (t, M.det())
        lam = M.LUsolve(Matrix(omega))
        assert all(x > 0 for x in lam), (t, lam)
        # offset: c = 1 + negabinary rep of a random residue r mod D (digits 0/1)
        r = random.randrange(D)
        # find c in {0,1}^m with l(c) = r (mod D) by brute force over negabinary
        target = r
        c = None
        for val in (r, r - D, r + D, r - 2 * D):
            x, digs = val, []
            while x != 0:
                rem = x % 2; digs.append(rem); x = (x - rem) // -2
            if len(digs) <= m:
                c = digs + [0] * (m - len(digs)); break
        assert c is not None and ell(c) % D == r % D
        c = [ci + 1 for ci in c]
        Minv = np.array(M.inv().tolist(), dtype=object)
        pieces.append((t, D, c, Minv))
    print(f"m={m}: pieces t={ts}, D={[2**t-1 for t in ts]}; all laminar, |det|=D_t, omega interior: OK")
    # f(x) = #{t : x - c_t in N B_t}; evaluate on x = s*omega + small box, many s
    def f(x):
        cnt = 0
        for t, D, c, Minv in pieces:
            y = [xi - ci for xi, ci in zip(x, c)]
            if ell(y) % D: continue
            q = Minv.dot(np.array(y, dtype=object))
            if all(qi >= 0 and qi == int(qi) for qi in q): cnt += 1
        return cnt
    best = {}
    for s in range(1, 3):
        base = [s * o for o in omega]
        for d in itertools.product(range(box), repeat=3):
            x = list(base); x[0] += d[0]; x[2] += d[1]; x[4] += d[2]
            v = f(x); n1 = sum(x)
            best[v] = min(best.get(v, 10 ** 9), n1)
    print("value -> min l1-norm seen:", dict(sorted(best.items())))
    L = 1
    for t in ts: L *= 2 ** t - 1
    # far point: x = S*omega + k*e0 with l(x - c_t) = 0 mod D_t for all t (CRT), S huge
    from sympy.ntheory.modular import crt
    lo = ell(omega)
    for S in [2 ** 170, 2 ** 200]:
        # need l(S*omega) + k - l(c_t) = 0 mod D_t
        res = [(ell(c) - S * lo) % D for t, D, c, _ in pieces]
        k, _ = crt([D for _, D, _, _ in pieces], res)
        x = [S * o for o in omega]; x[0] += int(k)
        print(f"far point S={S}: f = {f(x)} (of {len(pieces)}), l1-norm ~ 2^{np.log2(float(sum(x))):.1f}")
    # near: congruence-count upper bound on f over random x with l1-norm <= R
    for R in [10, 100, 1000, 10 ** 4, 10 ** 5]:
        mx = 0
        for _ in range(3000):
            x = [0] * m
            for _ in range(R):
                x[random.randrange(m)] += 1
            cnt = sum(1 for t, D, c, _ in pieces if ell([a - b for a, b in zip(x, c)]) % D == 0)
            mx = max(mx, cnt)
        print(f"R={R}: max congruence count (>= f) over 3000 random x of norm R: {mx}")
    print(f"all {len(ts)} pieces meet only where l(x) is in one class mod L = {L} (log2 L = {np.log2(float(L)):.1f})")

if __name__ == "__main__":
    main()
