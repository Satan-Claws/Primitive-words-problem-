r"""r10_2q: check the D-invariant lemma of reports/r10_2q.md on rows #a = 2q (q odd prime).
D(w) = #b in odd gaps - #b in even gaps (gap of a b = parity of #a in its prefix; odd -> +1).
Claims on row 2q: (i) squares have D = 0; (ii) w = v^q with #a(v)=2 has D = q(x-y) != 0, so |D| >= q,
and |D| in 2q*N+ when #b even; (iii) hence Prim∩row∩{#b even} = {D notin 2qZ} ∪ ({D=0}∩NonSq) ∪ ({D in 2qZ\0}∩Not2P).
Usage: .venv/bin/python r10_2q_dinv.py [MAXLEN]"""
import sys
from itertools import combinations
MAXLEN = int(sys.argv[1]) if len(sys.argv) > 1 else 18


def root(w):
    n = len(w); return next(w[:d] for d in range(1, n + 1) if n % d == 0 and w == w[:d] * (n // d))


def D(w):
    par = 0; d = 0
    for ch in w:
        if ch == 'a': par ^= 1
        else: d += 1 if par else -1
    return d


for N in (6, 10, 14):
    q = N // 2; bad = cnt = 0
    for n in range(N, MAXLEN + 1):
        for pos in combinations(range(n), N):
            s = ['b'] * n
            for p in pos: s[p] = 'a'
            w = ''.join(s); cnt += 1
            r = root(w); e = len(w) // len(r); d = D(w)
            sq = len(w) % 2 == 0 and w[:len(w) // 2] == w[len(w) // 2:]
            p2 = e > 1 and r.count('a') == 2
            if sq and d != 0: bad += 1; print('square D!=0', w)
            if p2 and (d == 0 or d % q): bad += 1; print('P2 D', w, d)
            if p2 and (n - N) % 2 == 0 and d % N: bad += 1; print('P2 even-b D', w, d)
            # decomposition (iii) on #b even
            if (n - N) % 2 == 0:
                rhs = (d % N != 0) or (d == 0 and not sq) or (d != 0 and d % N == 0 and not p2)
                if rhs != (e == 1): bad += 1; print('decomp', w)
    print(f'row {N}, |w|<={MAXLEN}: {cnt} words, {bad} failures')
