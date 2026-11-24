"""r14_steep_checks.py -- checks for r14_steep.md.
(1) Steep heavy block T: grammar T -> b T T a | eps (binary trees, node = b..a around 2 children).
    - NEGATIVE RESULT: the grammar is ambiguous; as a LANGUAGE |T_l| = Motzkin(l/2) (growth sqrt3 < 2), NOT full entropy.
    - every nonempty word is a negative excursion (2P<0 strictly inside, ends at 0)  [T subset E].
    - min depth over T_l (depth = -min 2P) = tree-height lower bound ~ log2: steep (not level) but log-level.
    - all cycles (v,y) have D(v)<0<D(y) (checked on all pumps of words up to length L).
(2) Slack wedge: p_W1(m,C) = P(A<B, B>=-C for k<=m) vs C (predict ~ C^{4/3} m^{-2/3} for C << sqrt m).
Units: doubled walk 2P (b=-1, a=+1)."""
import sys, math, itertools, numpy as np
from functools import lru_cache
L = 18
@lru_cache(None)
def T(l):
    if l == 0: return frozenset([""])
    out = set()
    for l1 in range(0, l - 1, 2):
        for w1 in T(l1):
            for w2 in T(l - 2 - l1): out.add("b" + w1 + w2 + "a")
    return frozenset(out)
def walk(w):
    P = [0]
    for c in w: P.append(P[-1] + (1 if c == "a" else -1))
    return P
cat = lambda m: math.comb(2*m, m)//(m+1)
print("(1) l, |T_l|, Catalan, subset_E, min depth (2P units), #words depth<=4")
for l in range(2, L + 1, 2):
    ws = T(l); P = [walk(w) for w in ws]
    sub = all(max(p[1:-1]) < 0 and p[-1] == 0 for p in P)
    md = min(-min(p) for p in P); nd = sum(-min(p) <= 4 for p in P)
    print(f"  {l:3d} {len(ws):6d} {cat(l//2):6d} {sub} {md} {nd}")
# min depth by DP to large l: depth(b w1 w2 a) = 1 + max(depth w1, depth w2), depth(eps)=0
md = {0: 0}
for l in range(2, 4097, 2):
    md[l] = 1 + min(max(md[a], md[l - 2 - a]) for a in range(0, l - 1, 2))
print("  min depth at l=64,256,1024,4096:", [md[l] for l in (64, 256, 1024, 4096)], " log2(l):", [round(math.log2(l),1) for l in (64,256,1024,4096)])
print("  sum_l |T_l| 2^-l (l<=4000) ->", sum(cat(m) / 4**m for m in range(2001)), "(limit 2, slowly)")
# cycles: for words up to length 12, all pumps from derivation trees: compute via explicit trees
def trees(l):
    if l == 0: yield None; return
    for l1 in range(0, l - 1, 2):
        for t1 in trees(l1):
            for t2 in trees(l - 2 - l1): yield (t1, t2)
def yld(t): return "" if t is None else "b" + yld(t[0]) + yld(t[1]) + "a"
def subtrees(t, pre, suf):
    # yields (node, left context, right context) for every T-node
    yield t, pre, suf
    if t is None: return
    a, b = t
    yield from subtrees(a, pre + "b", yld(b) + "a" + suf)
    yield from subtrees(b, pre + "b" + yld(a), "a" + suf)
D = lambda s: s.count("a") - s.count("b")
bad = 0; cnt = 0
for l in range(2, 13, 2):
    for t in trees(l):
        nodes = list(subtrees(t, "", ""))
        for (t1, p1, s1) in nodes:
            for (t2, p2, s2) in nodes:
                if t2 is not t1 and p2.startswith(p1) and len(p2) > len(p1) and s2.endswith(s1) and len(p2) + len(yld(t2)) + len(s2) == l:
                    v = p2[len(p1):]; y = s2[:len(s2) - len(s1)]
                    if len(v) + len(y) == 0: continue
                    cnt += 1; bad += not (D(v) < 0 < D(y))
print(f"  pumps checked (l<=12): {cnt}, violating D(v)<0<D(y): {bad}")
# (2) slack wedge
M = int(sys.argv[1]) if len(sys.argv) > 1 else 512
def run(M, C):
    R = M + 2*C + 4; off = R; S = 2*R + 1
    g = np.zeros((S, S)); g[off, off] = 1.0
    A = np.arange(S)[:, None] - off; B = np.arange(S)[None, :] - off
    mk = (A < B) & (B >= -2*C); out = {}
    for m in range(1, M + 1):
        h = np.zeros_like(g)
        for da in (1, -1):
            for db in (1, -1): h += 0.25*np.roll(np.roll(g, da, 0), db, 1)
        g = h*mk
        if m in (M//4, M//2, M): out[m] = g.sum()
    return out
print(f"(2) slack wedge, M={M}: C, p(M/4), p(M/2), p(M), local exp, p(M)/p0(M), C^(4/3) ratio")
base = None
for C in (0, 2, 4, 8):
    o = run(M, C); e = math.log(o[M]/o[M//2])/math.log(2)
    if base is None: base = o[M]
    print(f"  C={C:2d} {o[M//4]:.3e} {o[M//2]:.3e} {o[M]:.3e} exp={e:+.3f} ratio={o[M]/base:.2f} (1+C)^(4/3)={(1+C)**(4/3):.2f}")
