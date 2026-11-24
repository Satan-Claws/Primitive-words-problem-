"""Audit R5-C: independent re-implementation of the r4_core gadgets (LIN, FOLD, FL_3, LF_3, PF_2, RLF)
from the definitions in R2/r4_core.md and R2/r3_offw.md section 4. Not derived from r4_core_*.
(1) soundness: no gadget certifies any non-primitive word, n <= NMAX (default 18), every word;
(2) every pure-sign fold certificate found is checked to give a nonzero weighted sum (Lemma S identity);
(3) coverage cross-check on primitive words n <= NCOV (default 13) against r4_core.md section 2.
Usage: python audit_r4_gadgets.py [NMAX] [NCOV]"""
import sys, math, itertools
from math import gcd

def primitive(w):
    n = len(w)
    return all(w != w[d:] + w[:d] for d in range(1, n) if n % d == 0) if n else False

def fold_certs(x):
    """list of (m, sign) pure-sign fold certificates on integer vector x over Z_N (r3_offw.md section 4)."""
    N = len(x); out = []
    for m in range(N):
        prs = []
        i, j = 0, m
        while i < j: prs.append((i, j)); i += 1; j -= 1           # mirror pairs in u = [0..m]
        i, j = m + 1, N - 1
        uprs = len(prs)
        while i < j: prs.append((i, j)); i += 1; j -= 1           # mirror pairs in v = [m+1..N-1]
        for sg in (1, -1):
            ok = True; strict = False
            for t, (i, j) in enumerate(prs):
                d = (x[i] - x[j]) if t < uprs else (x[j] - x[i])
                d *= sg
                if d < 0: ok = False; break
                if d > 0: strict = True
            if ok and strict:
                s = sum(x[k] * math.sin(2 * math.pi * (k - m / 2) / N) for k in range(N))
                assert abs(s) > 1e-9, ("fold identity violated", x, m, sg)
                out.append((m, sg))
    return out

def windows(w, K):
    n = len(w); return [''.join(w[(k + t) % n] for t in range(K)) for k in range(n)]

FACT = {L: [''.join(p) for p in itertools.product('ab', repeat=L)] for L in (1, 2, 3)}
COEF = [(c1, c2) for c1 in range(1, 4) for c2 in range(1, 4) if gcd(c1, c2) == 1]

def runs(w):
    """cyclic a-run and b-run sequences, starting from a canonical cut; None if unary."""
    n = len(w)
    if 'a' not in w or 'b' not in w: return None
    s = next(k for k in range(n) if w[k] == 'a' and w[k - 1] == 'b')   # start of an a-run
    v = w[s:] + w[:s]
    al, be = [], []
    i = 0
    while i < n:
        j = i
        while j < n and v[j] == v[i]: j += 1
        (al if v[i] == 'a' else be).append(j - i); i = j
    return al, be

def gadgets(w):
    n = len(w); A = w.count('a'); B = n - A; res = {}
    res['LIN'] = (A == 1 or B == 1 or any(abs(r * A - s * B) == 1 for r in range(1, 4) for s in range(1, 4) if gcd(r, s) == 1))
    res['FOLD'] = len(fold_certs([c == 'b' for c in w])) > 0
    win = {L: windows(w, L) for L in (1, 2, 3)}
    occ = {f: sum(1 for c in win[len(f)] if c == f) for L in (1, 2, 3) for f in FACT[L]}
    fl = any(o == 1 for o in occ.values())
    if not fl:
        fl = any(abs(c1 * occ[f] - c2 * occ[h]) == 1 for f in occ for h in occ for c1, c2 in COEF)
    res['FL'] = fl
    res['LF'] = any(fold_certs([int(c == f) for c in win[len(f)]]) for L in (2, 3) for f in FACT[L] if occ[f])
    res['PF'] = any(fold_certs([int(c == f) - int(c == h) for c in win[2]]) for f, h in itertools.combinations(FACT[2], 2))
    rr = runs(w)
    res['RLF'] = bool(rr) and len(rr[0]) >= 2 and bool(fold_certs(rr[0]) or fold_certs(rr[1]))
    return res

def main():
    NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 18
    NCOV = int(sys.argv[2]) if len(sys.argv) > 2 else 13
    bad = 0; checked = 0
    for n in range(1, NMAX + 1):
        # non-primitive words of length n = u^p, enumerate u of length n/p
        seen = set()
        for d in range(1, n):
            if n % d: continue
            for t in itertools.product('ab', repeat=d):
                w = ''.join(t) * (n // d)
                if w in seen: continue
                seen.add(w); checked += 1
                g = gadgets(w)
                if any(g.values()): bad += 1; print('UNSOUND', w, g)
    print(f'soundness: {checked} non-primitive words n<={NMAX}, {bad} accepted by some gadget')
    for n in range(1, NCOV + 1):
        tot = 0; s0 = 0; s4 = 0
        for t in itertools.product('ab', repeat=n):
            w = ''.join(t)
            if not primitive(w): continue
            tot += 1; g = gadgets(w)
            s0 += g['LIN'] or g['FOLD']; s4 += any(g.values())
        print(f'n={n}: |Q_n|={tot} S0={s0/tot:.4f} S4={s4/tot:.4f} uncovered={tot - s4}')

if __name__ == '__main__':
    main()
