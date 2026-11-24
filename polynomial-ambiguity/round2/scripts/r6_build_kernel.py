"""R6-A: Kernel obstruction for finite-state fold certificates (Prop K).

For a DFA D over the pair alphabet Pi = {aa,ab,ba,bb} read outside-in along the fold
(pair i = (w_i, w_{n-1-i})), with acceptance depending on (final state, centre letter),
we build y in L(D) whose transformation lies in the minimal ideal K of the transition
monoid, take j with (phi(y ybar))^j idempotent, and output u with u^{2j+1} accepted.
Checks: u^{2j+1} is non-primitive and its fold is accepted, for many random DFAs.
Also: the toy certificate 'd_{n/2} != 0 mod 3' and its witness.
"""
import random, itertools, sys

PI = [('a','a'),('a','b'),('b','a'),('b','b')]

def fold_pairs(w):
    n = len(w); return [(w[i], w[n-1-i]) for i in range(n//2)], (w[n//2] if n % 2 else '')

def primitive(w):
    n = len(w)
    return all(w != w[:d]*(n//d) for d in range(1, n) if n % d == 0)

class DFA:
    def __init__(s, k, rng):
        s.k = k
        s.d = {c: tuple(rng.randrange(k) for _ in range(k)) for c in PI}
        # acceptance on (state, centre in {'', 'a', 'b'})
        s.F = {(q, c) for q in range(k) for c in ('', 'a', 'b') if rng.random() < 0.5}
    def phi(s, z):
        t = tuple(range(s.k))
        for c in z: t = tuple(s.d[c][q] for q in t)
        return t
    def accepts_word(s, w):
        z, c = fold_pairs(w); return (s.phi(z)[0], c) in s.F

def compose(t1, t2): return tuple(t2[q] for q in t1)  # apply t1 then t2

def swaprev(y): return [(b, a) for (a, b) in reversed(y)]

def rank(t): return len(set(t))

def min_rank(D):
    # minimal ideal = elements of minimal rank among reachable transformations (BFS on monoid)
    seen = {tuple(range(D.k))}; fr = list(seen)
    while fr:
        nf = []
        for t in fr:
            for c in PI:
                u = compose(t, D.d[c])
                if u not in seen: seen.add(u); nf.append(u)
        fr = nf
    return min(rank(t) for t in seen)

def word_from_pairs(y, centre=''):
    # u with pairseq(u) = y . [centre pair] . swaprev(y); |u| = 2|y| (+1)
    left = [a for a, _ in y]; right = [b for _, b in y]
    return ''.join(left) + centre + ''.join(reversed(right))

def trial(rng, k):
    D = DFA(k, rng); r = min_rank(D)
    for _ in range(4000):
        L = rng.randrange(1, 12); y = [rng.choice(PI) for _ in range(L)]
        c = rng.choice(['', 'a', 'b'])
        t = D.phi(y)
        if rank(t) != r or (t[0], c) not in D.F: continue
        ybar = swaprev(y); mid = [(c, c)] if c else []
        g = D.phi(y + mid + ybar)
        j, gj = 1, g
        while compose(gj, gj) != gj: j += 1; gj = compose(gj, g)
        u = word_from_pairs(y, c); p = 2*j + 1; w = u * p
        assert not primitive(w)
        assert fold_pairs(w)[1] == c
        return ('fooled' if D.accepts_word(w) else 'NOT-fooled'), len(w)
    return 'no-kernel-accepted-y', 0

if __name__ == '__main__':
    rng = random.Random(1)
    from collections import Counter
    C = Counter(); mx = 0
    for k in (2, 3, 4, 5, 6, 8):
        for _ in range(500):
            res, n = trial(rng, k); C[(k, res)] += 1; mx = max(mx, n)
    for key in sorted(C): print(key, C[key])
    print('max witness length', mx)
    # toy: R3 = {sum c_i != 0 mod 3}: rejects every u^p with p even; fooled by p = 7
    w = 'ab' * 7; z, _ = fold_pairs(w)
    d = sum((x == 'a') - (y == 'a') for x, y in z)
    print('toy (ab)^7: d_{n/2} =', d, 'mod 3 =', d % 3, 'primitive?', primitive(w))
    # exhaustive: R3 contains no u^p with p even, n <= 20
    bad = 0
    for n in range(2, 21, 2):
        for bits in itertools.product('ab', repeat=n//2):
            u = ''.join(bits); w = u + u
            z, _ = fold_pairs(w); d = sum((x == 'a') - (y == 'a') for x, y in z)
            bad += (d % 3 != 0)
    print('squares accepted by R3 (n<=20):', bad)
