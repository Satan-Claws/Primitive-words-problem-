"""
Check Theorem R2 (report): for n>=2, m=ceil(n/3), every primitive w of length n has a split
w = u y v, |y| = m, |u| <= m-1, such that u y' v is primitive for EVERY y' in Sigma^m whose first
letter equals the first letter of y.  Also check Lemma R1: for windows of length m<=n - ceil(2n/3)... i.e.
outer length >= 2n/3, |Bad(outer)| <= 1.
Usage: python3 first_letter_split.py NMAX
"""
import sys, itertools
from rect_barrier import is_prim

def main():
    NMAX = int(sys.argv[1])
    for n in range(2, NMAX + 1):
        m = -(-n // 3)
        inners = {c: [c + ''.join(t) for t in itertools.product('ab', repeat=m - 1)] for c in 'ab'}
        allin = inners['a'] + inners['b']
        maxbad = 0
        fail = 0; tot = 0
        cache = {}
        for t in itertools.product('ab', repeat=n):
            w = ''.join(t)
            if not is_prim(w): continue
            tot += 1
            ok = False
            for k in range(0, m):
                u, y, v = w[:k], w[k:k + m], w[k + m:]
                key = (u, v)
                if key not in cache:
                    cache[key] = [x for x in allin if not is_prim(u + x + v)]
                bad = cache[key]
                maxbad = max(maxbad, len(bad))
                if all(x[0] != y[0] for x in bad):
                    ok = True; break
            if not ok:
                fail += 1
                print("FAIL", w)
        print(f"n={n} m={m}: primitive={tot}, failures={fail}, max|Bad| over tried splits={maxbad}")

if __name__ == '__main__':
    main()
