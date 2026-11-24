"""g3 checks (round 2, G3** on S_N).

(A) Lemma F_S: on (ab+)^n, n even, J = [1..r] u [n/2+1..n/2+r], ones elsewhere, r <= n/6:
    x non-primitive  <=>  z_x == z_y.   Brute force for n = 36 (S_2), r <= 3, z in {1,2}^{2r}.
(B) Exact refinement: N^2 = {(2i ,..)} partition into three laminar K<=3 pieces, one of index 2
    (chain piece N{e1, e1+2e2} with offsets (0,0),(1,1), and (0,1)+N{e2, e1+2e2}).
(C) Forward/backward chain lattices: index of the joint lattice vs its l_inf covering radius
    (index 2^{Theta(rho)}, covering radius O(1)): exponential index alone is not a length obstruction.
"""
import itertools
import numpy as np


def is_primitive(x):
    n = len(x)
    for d in range(1, n):
        if n % d == 0 and all(x[i] == x[(i + d) % n] for i in range(n)):
            return False
    return True


def check_A(n=36, rmax=3):
    for r in range(1, rmax + 1):
        assert r <= n // 6
        for z in itertools.product([1, 2], repeat=2 * r):
            x = [1] * n
            for i in range(r):
                x[i] = z[i]
                x[n // 2 + i] = z[r + i]
            assert is_primitive(x) == (z[:r] != z[r:]), (r, z)
    print(f"(A) Lemma F_S face check OK for n={n}, r<= {rmax}")


def check_B(B=40):
    cnt = {}
    pieces = [((0, 0), [(1, 0), (1, 2)]), ((1, 1), [(1, 0), (1, 2)]), ((0, 1), [(0, 1), (1, 2)])]
    for c, V in pieces:
        for a in range(B):
            for b in range(B):
                p = (c[0] + a * V[0][0] + b * V[1][0], c[1] + a * V[0][1] + b * V[1][1])
                if p[0] < 20 and p[1] < 20:
                    cnt[p] = cnt.get(p, 0) + 1
    assert all(cnt.get((x, y), 0) == 1 for x in range(20) for y in range(20))
    print("(B) N^2 = exact disjoint union of 3 laminar pieces (one of lattice index 2): OK")


def chain_phi(rho, backward=False):
    # quotient map Z^{rho+1} -> Z/2^rho of the chain {e1} u {e_i + 2 e_{i+1}}
    phi = [(-2) ** (rho - j) for j in range(rho + 1)]  # phi(e_{j+1})
    phi[0] = 0  # e_1 in lattice; check e_i+2e_{i+1} -> phi_i + 2 phi_{i+1} = 0 mod 2^rho
    phi = [p % 2 ** rho for p in phi]
    if backward:
        phi = phi[::-1]
    return phi


def check_C(rhos=(3, 4, 5, 6, 7, 8)):
    for rho in rhos:
        m = 2 ** rho
        f, g = chain_phi(rho), chain_phi(rho, True)
        d = rho + 1
        for i in range(1, rho):  # sanity: chain vectors in kernel
            assert (f[i - 1] + 2 * f[i]) % m == 0 or i == 0
        classes = {}
        R = 0
        # smallest l_inf radius R such that every class (f(x),g(x)) is hit by some |x|_inf <= R
        reach = {(int(np.dot(f, x)) % m, int(np.dot(g, x)) % m)
                 for x in itertools.product(range(-0, 1), repeat=d)}
        image = set()
        # image of Z^d in (Z/m)^2
        for x in itertools.product(range(m), repeat=1):
            pass
        img = {(0, 0)}
        gens = [(f[j] % m, g[j] % m) for j in range(d)]
        frontier = [(0, 0)]
        while frontier:
            new = []
            for a in frontier:
                for gg in gens:
                    b = ((a[0] + gg[0]) % m, (a[1] + gg[1]) % m)
                    if b not in img:
                        img.add(b)
                        new.append(b)
            frontier = new
        index = len(img)
        while len(reach) < index:
            R += 1
            reach = {(int(np.dot(f, x)) % m, int(np.dot(g, x)) % m)
                     for x in itertools.product(range(-R, R + 1), repeat=d)} if (2 * R + 1) ** d < 3e6 else None
            if reach is None:
                break
        print(f"(C) rho={rho}: joint index {index} = 2^{np.log2(index):.0f}, l_inf covering radius "
              f"{'>' + str(R - 1) + ' (search cut)' if reach is None else R}")


if __name__ == "__main__":
    check_A()
    check_B()
    check_C()
