"""Audit R5-C of Prop H (R2/r4_pp.md section 2).
(a) block lemma: for all u, |u| <= M, p in {2,3,4,5}: h_p(u) primitive <=> u primitive or u unary of length 1 ... reported per case;
    unary edge cases: h_p(a^k) = a^{pk} is never primitive (so h_p^{-1}(L) has no unary words when L subset Q).
(b) coverage: g(u)=1 => g(h_p u) = p and h_p(u) in Q (u non-unary).
(c) tree-count identity for the literal pullback grammar G' (states = (block offset, block letter), leaves at
    offset 0 emit the u-letter, other leaves emit epsilon and check the letter), on random ambiguous CNF grammars:
    #trees_G'(u) == #trees_G(h_p(u)) for every u with |u| <= 6 (p=2), <= 4 (p=3)."""
import itertools, random
from functools import lru_cache
from math import gcd

def prim(w):
    n = len(w); return n > 0 and all(w != w[d:] + w[:d] for d in range(1, n) if n % d == 0)

def h(u, p): return ''.join(c * p for c in u)

def part_a():
    for p, M in ((2, 14), (3, 11), (4, 10), (5, 9)):
        fails = 0; tot = 0
        for n in range(1, M + 1):
            for t in itertools.product('ab', repeat=n):
                u = ''.join(t); tot += 1
                unary = len(set(u)) == 1
                hu = h(u, p)
                if unary:
                    if prim(hu): fails += 1; print('unary primitive image', u, p)
                    continue
                if prim(hu) != prim(u): fails += 1; print('BLOCK LEMMA FAIL', u, p)
                A, B = u.count('a'), u.count('b')
                if gcd(hu.count('a'), hu.count('b')) != p * gcd(A, B): fails += 1
                if gcd(A, B) == 1 and not prim(hu): fails += 1; print('coverage fail', u, p)
        print(f'(a,b) p={p} |u|<={M}: {tot} words, {fails} failures')

def rand_grammar(rng, nt=3):
    NT = list(range(nt)); rules = []
    for A in NT:
        for x in 'ab':
            if rng.random() < 0.6: rules.append((A, x))
        for B in NT:
            for C in NT:
                if rng.random() < 0.35: rules.append((A, B, C))
    return NT, rules

def count_G(rules, w):
    n = len(w)
    @lru_cache(None)
    def c(A, i, j):
        s = 0
        for r in rules:
            if r[0] != A: continue
            if len(r) == 2:
                s += (j == i + 1 and w[i] == r[1])
            else:
                for k in range(i + 1, j): s += c(r[1], i, k) * c(r[2], k, j)
        return s
    return c(0, 0, n)

def count_Gprime(rules, u, p):
    """literal pullback grammar: nonterminals (A, q, r), q,r in states (o, letter)."""
    states = [(0, None)] + [(o, x) for o in range(1, p) for x in 'ab']
    def step(q, x):
        o, c = q
        if o == 0: return (1 % p, x if p > 1 else None) if p > 1 else (0, None), x
        if x != c: return None, None
        return ((o + 1, c) if o + 1 < p else (0, None)), ''
    def gpos(q, i, end):
        o = q[0]
        if o == 0: return p * i
        return p * (i - 1) + o
    @lru_cache(None)
    def c(A, q, r, i, j):
        L = gpos(r, j, True) - gpos(q, i, False)
        if L < 1: return 0
        s = 0
        for rule in rules:
            if rule[0] != A: continue
            if len(rule) == 2:
                if L != 1: continue
                nq, emit = step(q, rule[1])
                if nq is None or nq != r: continue
                if emit == '': s += (j == i)
                else: s += (j == i + 1 and u[i] == emit)
            else:
                for st in states:
                    for k in range(i, j + 1):
                        if gpos(st, k, True) - gpos(q, i, False) < 1 or gpos(r, j, True) - gpos(st, k, False) < 1: continue
                        a1 = c(rule[1], q, st, i, k)
                        if a1: s += a1 * c(rule[2], st, r, k, j)
        return s
    return c(0, (0, None), (0, None), 0, len(u))

def part_c():
    rng = random.Random(20261124); mism = 0; tests = 0; nz = 0; mx = 0
    for gi in range(40):
        NT, rules = rand_grammar(rng)
        for p, M in ((2, 6), (3, 4)):
            for n in range(1, M + 1):
                for t in itertools.product('ab', repeat=n):
                    u = ''.join(t)
                    x = count_G(rules, h(u, p)); y = count_Gprime(rules, u, p)
                    tests += 1; nz += x > 0; mx = max(mx, x)
                    if x != y: mism += 1; print('MISMATCH', gi, p, u, x, y)
    print(f'(c) {tests} (grammar,p,u) tests, {nz} with nonzero count, max count {mx}, {mism} mismatches')

if __name__ == '__main__':
    part_a(); part_c()
