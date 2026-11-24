r"""r11_eq2q: checks for reports/r11_eq2q.md.
(1) Sorted decomposition on rows #a = 2q:
    q odd prime: Prim ∩ row = ({D != 0} ∩ Not2P) ⊔ ({D = 0} ∩ NonSq)   (all #b, not only even)
    q = 2      : Prim ∩ row 4 = Not2P ∩ row 4
    Not2P = cyclic gap sequence not 2-periodic; NonSq = not of the form uu.
(2) Theorem T witnesses (gap-saturation orbit) for small N, M and q in {3,5,7}.
Usage: .venv/bin/python r11_eq2q_sorted.py [MAXLEN]"""
import sys
from itertools import combinations
MAXLEN = int(sys.argv[1]) if len(sys.argv) > 1 else 20


def prim(w):
    n = len(w); return all(not (n % d == 0 and w == w[:d] * (n // d)) for d in range(1, n))


def D(w):
    par = 0; d = 0
    for ch in w:
        if ch == 'a': par ^= 1
        else: d += 1 if par else -1
    return d


def gaps(w):  # cyclic gap sequence (number of b's after each a, wrapping)
    i = w.index('a'); r = w[i:] + w[:i]
    return [len(g) for g in r.split('a')[1:]]


def not2p(w):
    g = gaps(w); return any(g[k] != g[(k + 2) % len(g)] for k in range(len(g)))


def nonsq(w):
    n = len(w); return n % 2 == 1 or w[:n // 2] != w[n // 2:]


tot_bad = 0
for N in (4, 6, 10, 14):
    q = N // 2; bad = cnt = 0
    for n in range(N, MAXLEN + 1):
        for pos in combinations(range(n), N):
            s = ['b'] * n
            for p in pos: s[p] = 'a'
            w = ''.join(s); cnt += 1
            if q == 2: rhs = not2p(w)
            else: rhs = (D(w) != 0 and not2p(w)) or (D(w) == 0 and nonsq(w))
            if rhs != prim(w): bad += 1; print('FAIL', w) if bad < 5 else None
    tot_bad += bad
    print(f'(1) row {N}, |w|<={MAXLEN}: {cnt} words, {bad} failures')


def word(g): return ''.join('a' + 'b' * x for x in g)


for q in (3, 5, 7):
    for Nst, M in ((1, 1), (2, 2), (3, 6)):
        g = [Nst] * (2 * q); g[-1] += M; w = word(g)
        gp = [Nst + M if k % 2 == 0 else Nst + 2 * M for k in range(2 * q)]   # q-th power, gap ≡ g mod M, >= g
        gs = [Nst + (M if (k + 1) % q == 0 else 0) for k in range(2 * q)]     # square, not 2-periodic
        ok = (prim(w) and all(x >= y and (x - y) % M == 0 for x, y in zip(gp, g))
              and all(x >= y and (x - y) % M == 0 for x, y in zip(gs, g))
              and not prim(word(gp)) and nonsq(word(gp)) and not not2p(word(gp))
              and not prim(word(gs)) and not2p(word(gs)) and not nonsq(word(gs)))
        tot_bad += not ok
        print(f'(2) q={q} N={Nst} M={M}: witness ok={ok}')
print('TOTAL failures:', tot_bad)
