"""lemmaC_blocks: exact check of Lemma C (R2/tile2.md §3) for all k, via the reduction of R2/lemmaC.md.

Reduction (R2/lemmaC.md Thm 1): Lemma C(N,k)  <=>  BLOCK(N,k):
  h(X) = (1 - X^s) rho0(X)  in Z[X]/(X^P - 1),  s = P/p_k,  rho0 = prod_{j!=k} (1 - X^{p_j}).
  Blocks of h := maximal groups of support points of h on the circle Z_P in which consecutive points are at
  distance < p_k (cyclic). BLOCK: no proper nonempty cyclically-consecutive union B of blocks has
  fold_{p_j}(B) = 0 for all j (x-level, i.e. L = (X-1) prod_j Phi_{p_j} | B).
  omega-level analogue: fold_1(B) = sum of coefficients = 0  (used only as a sanity check vs tile2_muk).
Exact integer arithmetic (Python ints for positions; P is huge for large N, h is sparse).
Reports: #blocks, #bad unions (all cyclic unions; this is the strong, root-independent form).
Usage: .venv/bin/python lemmaC_blocks.py [Nmin=2] [Nmax=20] [omega=0]
"""
import sys
from sympy import prime


def rho0(ps, k):
    c = {0: 1}
    for j, p in enumerate(ps):
        if j == k: continue
        d = dict(c)
        for e, v in c.items(): d[e + p] = d.get(e + p, 0) - v
        c = {e: v for e, v in d.items() if v}
    return c


def h_sparse(ps, k):
    P = 1
    for p in ps: P *= p
    s = P // ps[k]
    r = rho0(ps, k)
    h = {}
    for e, v in r.items():
        h[e % P] = h.get(e % P, 0) + v
        h[(e + s) % P] = h.get((e + s) % P, 0) - v
    return P, {e: v for e, v in h.items() if v}


def blocks(P, h, pk):
    pos = sorted(h)
    m = len(pos)
    # cyclic gaps; start at a point preceded by a gap >= pk
    big = [i for i in range(m) if (pos[i] - pos[i - 1]) % P >= pk]
    if not big: return [pos]  # one cyclic block: nothing proper to test
    st = big[0]; order = pos[st:] + pos[:st]
    B = [[order[0]]]
    for a, b in zip(order, order[1:]):
        if (b - a) % P >= pk: B.append([b])
        else: B[-1].append(b)
    return B


def check(N, k, mods_kind='x'):
    ps = [prime(i + 1) for i in range(N)]
    P, h = h_sparse(ps, k)
    pk = ps[k]
    Bl = blocks(P, h, pk)
    mods = ps if mods_kind == 'x' else [1]
    def fv(block):
        out = []
        for M in mods:
            f = [0] * M
            for e in block: f[e % M] += h[e]
            out.extend(f)
        return tuple(out)
    F = [fv(b) for b in Bl]
    nb = len(F); dim = len(F[0])
    total = tuple(sum(f[i] for f in F) for i in range(dim))
    # prefix sums over block order; union of blocks a+1..b  (0<=a<b<=nb) linear; complements = wrapping unions
    pre = [tuple([0] * dim)]
    for f in F: pre.append(tuple(x + y for x, y in zip(pre[-1], f)))
    seen = {}
    bad_lin, bad_wrap = [], []
    for b, v in enumerate(pre):
        if v in seen:
            for a in seen[v]:
                if not (a == 0 and b == nb): bad_lin.append((a, b))
        w = tuple(x - y for x, y in zip(v, total))  # pre_b - pre_a = total -> complement balanced
        if w in seen:
            for a in seen[w]:
                if not (a == 0 and b == nb): bad_wrap.append((a, b))
        seen.setdefault(v, []).append(b)
    return dict(N=N, k=k + 1, p_k=pk, supp_h=len(h), blocks=nb, bad_all=len(bad_lin) + len(bad_wrap),
                ex=(bad_lin + bad_wrap)[:3],
                block_sizes=[len(b) for b in Bl][:12])


if __name__ == '__main__':
    a = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    b = int(sys.argv[2]) if len(sys.argv) > 2 else 20
    om = int(sys.argv[3]) if len(sys.argv) > 3 else 0
    for N in range(a, b + 1):
        for k in range(N):
            r = check(N, k, 'omega' if om else 'x')
            if om or r['bad_all'] or r['blocks'] > 2 or N <= 4: print(r, flush=True)
        print(f'N={N} done', flush=True)
