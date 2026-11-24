"""r20_dense_lyndon_fold.py -- are the non-fold dense certificates (Lyndon, canonical UMR) inside the fold region?
For a random word w, take its Lyndon rotation (a=0<b=1) and its canonical-UMR rotation (start at unique longest 1-run).
Report P(the canonical word, or one of its 4 dihedral/letter-swap images, lies in G^- )  (G^-: d_k<0, 1<=k<=n/2,
d_k = #a(prefix_k) - #a(suffix_k)).  Expect ~ c n^{-1/2}: these certificates are NOT fold-type.
"""
import numpy as np
rng = np.random.default_rng(7)
def inGm(w):
    n = len(w); a = (w == 0).astype(np.int64); h = n // 2
    pre = np.cumsum(a[:h]); suf = np.cumsum(a[::-1][:h])
    return bool(np.all(pre - suf < 0))
def imgs(w):
    return [w, 1 - w, w[::-1], 1 - w[::-1]]
def lyndon_rot(w):
    s = ''.join(map(str, w)); n = len(s); d = s + s
    k = min(range(n), key=lambda i: d[i:i + n]); return np.roll(w, -k)
def umr_rot(w):
    n = len(w)
    if (w == 1).all() or (w == 0).all(): return None
    k = int(np.argmax(w == 0)); v = np.roll(w, -k)
    x = np.concatenate(([0], v, [0])); d = np.diff(x); s = np.flatnonzero(d == 1); e = np.flatnonzero(d == -1)
    L = e - s; o = np.argsort(-L)
    if len(L) > 1 and L[o[0]] == L[o[1]]: return None
    return np.roll(v, -int(s[o[0]]))
for n in [64, 256, 1024]:
    S = 1500; ly = um = umn = 0
    for _ in range(S):
        w = rng.integers(0, 2, n).astype(np.int8)
        ly += any(inGm(x) for x in imgs(lyndon_rot(w)))
        u = umr_rot(w)
        if u is not None:
            umn += 1; um += any(inGm(x) for x in imgs(u))
    print(n, "Lyndon->fold", round(ly / S, 3), " UMR->fold", round(um / max(umn, 1), 3), " sqrt(n)*", round(ly / S * n ** .5, 2), round(um / max(umn, 1) * n ** .5, 2))
