"""tile2_core: the transport-LP ("min-cost non-crossing plan") selection rule for TILE_k (R2/tile2.md).

Masses m_0..m_{m-1} on support points in circle order (v0 = point 0), sum 0, signs fixed.
A bichromatic tree T is valid at m  <=>  the tree flows x_T (flow on edge {u,w} = mass of the side of u, oriented
pos->neg) are all > 0  <=>  x_T is a non-degenerate basic feasible solution of the transportation problem
  min sum c_ij x_ij,  x >= 0,  sum_j x_ij = m_i (i pos),  sum_i x_ij = -m_j (j neg).
Rule: cost c_ij = h(|pos_i - pos_j|), h strictly increasing strictly concave (sqrt), generic positions.
T*(m) := support of the unique optimal plan.  F_c := c-dual-feasible NC trees.  (Proofs in tile2.md.)
"""
import math, random
from fractions import Fraction as Fr
import numpy as np
from scipy.optimize import linprog


def make_cost(m, seed=0):
    rng = random.Random(seed)
    pos = [i + 0.3 * rng.random() for i in range(m)]
    return [[math.sqrt(abs(pos[i] - pos[j])) for j in range(m)] for i in range(m)]


def optimal_plan(mass, c):
    """float LP (HiGHS). returns dict {(i,j): flow} over pos i, neg j with flow > 1e-9*scale."""
    P = [i for i, v in enumerate(mass) if v > 0]; N = [j for j, v in enumerate(mass) if v < 0]
    nv = len(P) * len(N)
    cost = np.array([c[i][j] for i in P for j in N])
    rows, cols, vals = [], [], []
    for a, i in enumerate(P):
        for b, j in enumerate(N):
            k = a * len(N) + b
            rows += [a, len(P) + b]; cols += [k, k]; vals += [1.0, 1.0]
    from scipy.sparse import csr_matrix
    A = csr_matrix((vals, (rows, cols)), shape=(len(P) + len(N), nv))
    b = np.array([float(mass[i]) for i in P] + [float(-mass[j]) for j in N])
    r = linprog(cost, A_eq=A, b_eq=b, bounds=(0, None), method='highs')
    assert r.status == 0, r.message
    scale = max(abs(float(v)) for v in mass)
    out = {}
    for a, i in enumerate(P):
        for b_, j in enumerate(N):
            f = r.x[a * len(N) + b_]
            if f > 1e-7 * scale: out[(i, j)] = f
    return out


def is_spanning_tree(edges, m):
    if len(edges) != m - 1: return False
    par = list(range(m))
    def f(x):
        while par[x] != x: par[x] = par[par[x]]; x = par[x]
        return x
    for i, j in edges:
        a, b = f(i), f(j)
        if a == b: return False
        par[a] = b
    return True


def crossing(e, g):
    a, b = sorted(e); c, d = sorted(g)
    if len({a, b, c, d}) < 4: return False
    return (a < c < b < d) or (c < a < d < b)


def is_nc(edges):
    E = list(edges)
    return not any(crossing(E[s], E[t]) for s in range(len(E)) for t in range(s + 1, len(E)))


def tree_side_masses(edges, mass):
    """exact: for each edge {i,j} (i pos), mass of the component of i after deleting the edge."""
    m = len(mass); adj = {v: [] for v in range(m)}
    for i, j in edges: adj[i].append(j); adj[j].append(i)
    # root at 0, subtree sums
    order = [0]; parent = {0: None}
    for v in order:
        for w in adj[v]:
            if w not in parent: parent[w] = v; order.append(w)
    sub = {v: mass[v] for v in range(m)}
    for v in reversed(order):
        if parent[v] is not None: sub[parent[v]] += sub[v]
    out = {}
    for i, j in edges:
        # side of i
        out[(i, j)] = sub[i] if parent.get(i) == j else (-sub[j] if parent.get(j) == i else None)
    return out


def valid_exact(edges, mass):
    """tree validity (all subtree masses have the sign of their top), exact."""
    sm = tree_side_masses(edges, mass)
    return all(v > 0 for v in sm.values())


def dual_margin(edges, c, mass):
    """potentials alpha_i + beta_j = c_ij on tree edges; return min over pos-neg pairs of reduced cost
    c_ij - alpha_i - beta_j (>= 0 iff dual feasible; generic c => > 0 off-tree)."""
    m = len(mass); adj = {v: [] for v in range(m)}
    for i, j in edges: adj[i].append(j); adj[j].append(i)
    pot = {0: 0.0}; st = [0]
    while st:
        v = st.pop()
        for w in adj[v]:
            if w in pot: continue
            i, j = (v, w) if mass[v] > 0 else (w, v)
            pot[w] = c[i][j] - pot[v]; st.append(w)
    P = [i for i in range(m) if mass[i] > 0]; N = [j for j in range(m) if mass[j] < 0]
    E = set(edges)
    return min((c[i][j] - pot[i] - pot[j]) for i in P for j in N if (i, j) not in E)
