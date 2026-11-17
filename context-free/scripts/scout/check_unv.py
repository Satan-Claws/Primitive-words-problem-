"""Brute-force checks of folklore statements quoted in the briefing (scout agent).

1. Shyr-Yu / Shyr-Thierrin type statement: for u,v nonempty with uv != vu,
   how many n >= 1 make u^n v non-primitive?  Report max count and examples.
2. For primitive p != q: number of non-primitive words in p^i q^j (i,j>=1, small range).
3. Morphism h(a_i) = a b^i preserves primitivity both ways (sanity check on small words).
4. Q = Cyc(Q ∩ a{a,b}*) ∪ {b} on all words up to length L.
Run: python3 -I check_unv.py
"""
import itertools, sys

def is_primitive(w):
    n = len(w)
    if n == 0:
        return False
    # w primitive iff w not found in (w+w)[1:-1]
    return (w + w).find(w, 1) == n

def words(alpha, maxlen, minlen=1):
    for L in range(minlen, maxlen + 1):
        for t in itertools.product(alpha, repeat=L):
            yield ''.join(t)

def check1(maxlen=6, nmax=12):
    worst = 0
    examples = []
    hist = {}
    for u in words('ab', maxlen):
        for v in words('ab', maxlen):
            if u + v == v + u:
                continue
            bad = [n for n in range(1, nmax + 1) if not is_primitive(u * n + v)]
            hist[len(bad)] = hist.get(len(bad), 0) + 1
            if len(bad) > worst:
                worst = len(bad); examples = [(u, v, bad)]
            elif len(bad) == worst and len(examples) < 5:
                examples.append((u, v, bad))
    # which n occur as the bad exponent?
    bad_ns = {}
    for u in words('ab', maxlen):
        for v in words('ab', maxlen):
            if u + v == v + u:
                continue
            for n in range(1, nmax + 1):
                if not is_primitive(u * n + v):
                    bad_ns[n] = bad_ns.get(n, 0) + 1
    print('[1] uv!=vu, |u|,|v|<=%d, n<=%d: histogram #bad n:' % (maxlen, nmax), hist)
    print('    max #bad n =', worst, 'examples:', examples[:5])
    print('    bad exponents n that occur (n: count):', dict(sorted(bad_ns.items())))
    # examples with bad n >= 2
    ex2 = []
    for u in words('ab', maxlen):
        for v in words('ab', maxlen):
            if u + v == v + u: continue
            for n in range(2, nmax + 1):
                if not is_primitive(u * n + v):
                    ex2.append((u, v, n));
                    break
            if len(ex2) >= 8: break
        if len(ex2) >= 8: break
    print('    examples with a bad n>=2:', ex2)

def check2(maxlen=5, emax=8):
    prims = [w for w in words('ab', maxlen) if is_primitive(w)]
    worst = 0; ex = None
    for p in prims:
        for q in prims:
            if p == q: continue
            bad = [(i, j) for i in range(1, emax + 1) for j in range(1, emax + 1)
                   if not is_primitive(p * i + q * j)]
            if len(bad) > worst:
                worst = len(bad); ex = (p, q, bad)
    print('[2] primitive p!=q, |p|,|q|<=%d, i,j<=%d: max #non-primitive p^i q^j =' % (maxlen, emax), worst, 'example', ex)

def check3(n_letters=4, maxlen=7):
    def h(w):
        return ''.join('a' + 'b' * (int(c)) for c in w)
    alpha = ''.join(str(i) for i in range(n_letters))
    bad = 0
    for w in words(alpha, maxlen):
        if is_primitive(w) != is_primitive(h(w)):
            bad += 1
    print('[3] h(i)=a b^i, alphabet size %d, |w|<=%d: violations =' % (n_letters, maxlen), bad)

def check4(L=14):
    Q = set(w for w in words('ab', L) if is_primitive(w))
    Qa = [w for w in Q if w[0] == 'a']
    cyc = set()
    for w in Qa:
        for i in range(len(w)):
            cyc.add(w[i:] + w[:i])
    cyc.add('b')
    print('[4] Q == Cyc(Q ∩ a{a,b}*) ∪ {b} up to length %d:' % L, cyc == Q)

if __name__ == '__main__':
    check1()
    check2()
    check3()
    check4()
