# builder2: reflection/orbit-count certificates. a=0,b=1. One core.
import sys
from math import gcd
sys.path.insert(0, '../builder')
from common import lyndon, is_primitive, all_words, s

def letter_axes(w):
    """yield (c, D) with D_i = w_i - w_{c-i} on Z_n."""
    n = len(w)
    for c in range(n):
        yield c, [w[i] - w[(c - i) % n] for i in range(n)]

def runs(w):
    n = len(w)
    if len(set(w)) < 2: return None
    st = next(i for i in range(n) if w[i] != w[i - 1])
    v = w[st:] + w[:st]
    R = []; i = 0
    while i < n:
        j = i
        while j < n and v[j] == v[i]: j += 1
        R.append((v[i], j - i)); i = j
    return R

def dom_on(vals, K, c, half):
    # half arc H = c/2+1 .. c/2+half (indices), compare vals[i] <= vals[c-i]
    st = False
    for t in range(1, half + 1):
        i = (c // 2 + t) % K if c % 2 == 0 else None
        x, y = vals[i], vals[(c - i) % K]
        if x > y: return False
        if x < y: st = True
    return st

def cert_D(w):  # builder's Theorem D, via rotations of the literal predicate
    from grammar_check import pred
    n = len(w)
    return any(pred(w[i:]+w[:i]) for i in range(n))

def cert_G(w):  # orbit-count: exists axis with gcd(#mismatch pairs, n) == 1
    n = len(w)
    for c, D in letter_axes(w):
        m = sum(1 for x in D if x == 1)
        if gcd(m, n) == 1: return True
    return False

def cert_GB(w, B=3):  # CF bounded part: m<=B or r=n-2m<=B, gcd(m,r)=1
    n = len(w)
    for c, D in letter_axes(w):
        m = sum(1 for x in D if x == 1); r = n - 2 * m
        if (m <= B or r <= B) and gcd(m, r) == 1: return True
    return False

def run_axes(w):
    R = runs(w)
    if R is None: return
    K = len(R); L = [l for _, l in R]
    for c in range(0, K, 2):
        yield K, c, L

def cert_RD(w):  # run-length dominance on run cycle
    for K, c, L in run_axes(w):
        for sgn in (1, -1):
            st = False; ok = True
            for t in range(1, K // 2):
                i = (c // 2 + t) % K; x, y = L[i], L[(c - i) % K]
                if sgn < 0: x, y = y, x
                if x > y: ok = False; break
                if x < y: st = True
            if ok and st: return True
    return False

def run_counts(w):
    for K, c, L in run_axes(w):
        D = [L[i] - L[(c - i) % K] for i in range(K)]
        cnt = {}
        for x in D: cnt[x] = cnt.get(x, 0) + 1
        yield K, cnt

def cert_RG(w):  # run orbit-count ceiling: some value class of D has count coprime to K
    for K, cnt in run_counts(w):
        if any(gcd(v, K) == 1 for v in cnt.values()): return True
    return False

def cert_RGB(w, B=3):  # CF bounded: #mismatched run pairs s <= B, and one value count coprime: use s
    for K, cnt in run_counts(w):
        s0 = cnt.get(0, 0); mm = (K - s0) // 2
        if 1 <= mm <= B and any(gcd(v, K) == 1 for x, v in cnt.items() if x != 0): return True
        if K - 2 * mm <= B and gcd(mm, K) == 1 and mm > 0: return True
    return False

CERTS = dict(D=cert_D, G=cert_G, GB=cert_GB, RD=cert_RD, RG=cert_RG, RGB=cert_RGB)

if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'sound':
        for n in range(1, int(sys.argv[2]) + 1):
            for w in all_words(n):
                if is_primitive(w): continue
                for k, f in CERTS.items():
                    assert not f(w), (k, s(w))
        print('sound: no certificate accepts a non-primitive word, n <=', sys.argv[2])
    else:
        N = int(sys.argv[2])
        names = sys.argv[3].split(',')
        for n in range(int(sys.argv[4]) if len(sys.argv)>4 else 2, N + 1):
            tot = 0; miss = {k: 0 for k in names}; ex = {}
            for w in lyndon(n):
                tot += 1
                res = {k: CERTS[k](w) for k in ('D','G','GB','RD','RG','RGB')}
                res['CFU'] = res['D'] or res['GB'] or res['RD'] or res['RGB']
                res['ALL'] = res['CFU'] or res['G'] or res['RG']
                for k in names:
                    if not res[k]:
                        miss[k] += 1; ex.setdefault(k, s(w))
            print(n, tot, ' '.join('%s:%d(%.3f)' % (k, miss[k], miss[k]/tot) for k in names), ' ex:', ex.get('CFU',''), ex.get('ALL',''), flush=True)
