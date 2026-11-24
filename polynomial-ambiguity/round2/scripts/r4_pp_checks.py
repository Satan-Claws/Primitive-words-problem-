"""R4-B (r4_pp.md) computational checks.
(a) Block-morphism lemma: h_p(a)=a^p, h_p(b)=b^p. For non-unary u: h_p(u) in Q <=> u in Q, and g(h_p(u)) = p*g(u).
(b) L1 on prime-power classes: if g(w)=p^k (k>=1) then w in Q <=> w is not (n/p)-periodic.  Exhaustive n<=18.
(c) Theorem V (ray lemma), finite check of the proof mechanism: marked words a^x a' a^y b^z b' b^t of shape a^m b^m,
    chord span d = y+z+1, n = 2m.  A chord is valid at a prime-power class g = m = p^k iff (n/p) | d.  For every ray with
    prime base point m0 > v_m we exhibit an invalid prime-power point: by scanning, or at the point m* = q^(phi(v_m)+1)
    (q prime, q = m0 mod v_m) predicted by the proof.  Theorem V predicts 0 unresolved rays.
"""
import itertools, math, sys

def is_prim(w):
    n = len(w)
    return all(w != w[:d] * (n // d) for d in range(1, n) if n % d == 0)

def g_of(w):
    return math.gcd(w.count('a'), w.count('b'))

def prime_power(m):
    """return prime p if m = p^k, k>=1, else None"""
    if m < 2: return None
    for p in range(2, m + 1):
        if m % p == 0:
            while m % p == 0: m //= p
            return p if m == 1 else None

def check_a():
    bad = tot = 0
    for p, L in ((2, 14), (3, 12), (5, 10)):
        for n in range(1, L + 1):
            for t in itertools.product('ab', repeat=n):
                u = ''.join(t)
                if 'a' not in u or 'b' not in u: continue
                h = ''.join(c * p for c in u)
                tot += 1
                if is_prim(h) != is_prim(u) or g_of(h) != p * g_of(u): bad += 1
    print(f"(a) block-morphism lemma: {tot} non-unary words (p=2,3,5), {bad} failures")

def check_b(N=18):
    bad = tot = 0
    for n in range(2, N + 1):
        for t in itertools.product('ab', repeat=n):
            w = ''.join(t); g = g_of(w); p = prime_power(g)
            if p is None: continue
            tot += 1
            d = n // p
            periodic = all(w[i] == w[i + d] for i in range(n - d))
            if is_prim(w) == periodic: bad += 1
    print(f"(b) prime-power classes n<={N}: {tot} words, {bad} failures of [w in Q <=> not n/p-periodic]")

def primes_upto(M):
    s = [True] * (M + 1); s[0] = s[1] = False
    for i in range(2, int(M ** .5) + 1):
        if s[i]: s[i*i::i] = [False] * len(s[i*i::i])
    return s

def is_prime_int(q):
    if q < 2: return False
    i = 2
    while i * i <= q:
        if q % i == 0: return False
        i += 1
    return True

def phi(v):
    return sum(1 for k in range(1, v + 1) if math.gcd(k, v) == 1)

def check_c(M0=30, V=5, T=200):
    """For every ray (base point with prime m0 > v_m, direction with v_m>0), find an invalid point:
    first among the first T points; otherwise at the point predicted by the proof of Theorem V,
    m* = p^(phi(v_m)+1) with p prime, p = m0 mod v_m (Dirichlet), checked with exact integers."""
    rays = by_scan = by_pred = 0; unresolved = []
    for m0 in range(2, M0 + 1):
        if not is_prime_int(m0): continue
        for x in range(m0):
            y = m0 - 1 - x
            for z in range(m0):
                t = m0 - 1 - z
                for vx, vy, vz in itertools.product(range(V + 1), repeat=3):
                    vt = vx + vy - vz; vm = vx + vy
                    if vt < 0 or vm == 0 or m0 <= vm: continue
                    rays += 1; bad = False
                    for s in range(T):
                        m = m0 + s * vm; n = 2 * m; d = (y + s*vy) + (z + s*vz) + 1
                        p = prime_power(m)
                        if p is not None and d % (n // p): bad = True; break
                    if bad: by_scan += 1; continue
                    # predicted witness
                    found = False; q = m0 + vm; tries = 0
                    while tries < 6:
                        if is_prime_int(q):
                            tries += 1
                            M = q ** (phi(vm) + 1); s = (M - m0) // vm
                            assert (M - m0) % vm == 0
                            d = (y + s*vy) + (z + s*vz) + 1
                            if d % (2 * M // q): found = True; break
                        q += vm
                    if found: by_pred += 1
                    else: unresolved.append((m0, x, y, z, t, vx, vy, vz, vt))
    print(f"(c) rays (prime base m0 <= {M0}, |v| <= {V}): {rays}; invalid point in first {T}: {by_scan};"
          f" invalid only at predicted p^(phi(v_m)+1) point: {by_pred}; unresolved: {len(unresolved)} {unresolved[:3]}")

if __name__ == '__main__':
    check_a(); check_b(); check_c()
