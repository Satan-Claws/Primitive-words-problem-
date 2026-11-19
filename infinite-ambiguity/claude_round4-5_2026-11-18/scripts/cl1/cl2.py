"""CL2 refutation and its generalisation.
For an offset vector c0 (length l >= 2) the family F(c0) = { a . (a^{m+c0[0]} b ... a^{m+c0[l-1]} b)^k : m>=m0, k>=2 }
has block vector x = (m*1 + c0)^k + e_1.  Certificate:
  L(c0) = { w in (a*b)^+ : K := #blocks, K = 0 mod l, K >= 2l, x - Rx = T }   (R = reversal, 1-indexed)
  T_i = c0[(i-1)%l] - c0[(-i)%l] + [i=1] - [i=K].
CF: linear grammar, nonterminal (r = next pair index mod l, first?, count capped at l); pair i emits a^p b ... a^q b
with p - q = T_i (bounded constant).  Checks: grammar == condition (exhaustive, small n); all words of L(c0)
up to length PMAX primitive; family members up to length FMAX in L(c0)."""
import itertools, sys
from functools import lru_cache
from refute import primitive, blocks

def T(c0, K, i):  # 1-indexed
    l = len(c0)
    return c0[(i-1) % l] - c0[(-i) % l] + (i == 1) - (i == K)

def in_cond(c0, w):
    x = blocks(w); l = len(c0)
    if not x: return False
    K = len(x)
    if K % l or K < 2*l: return False
    return all(x[i-1] - x[K-i] == T(c0, K, i) for i in range(1, K+1))

def make_gen(c0):
    l = len(c0)
    @lru_cache(None)
    def A(n):  # a^n b ... a^n wrapped:  a^j  S  a^j with inner 'b'-prefixed S ; returns words a^j b S' a^j
        raise NotImplementedError
    @lru_cache(None)
    def S(n, p, cnt):  # p = number of pairs emitted so far (mod l), cnt = min(pairs, l)
        out = set()
        # stop: K = 2*pairs (+1 middle).  pairs mod l = p, need pairs >= l (K>=2l)
        if cnt >= l:
            if (2*p) % l == 0 and n == 0: out.add('')
            if (2*p+1) % l == 0 and n >= 1: out.add('a'*(n-1) + 'b')
        # emit pair i = pairs+1 with offset d = T_i (i != K guaranteed since inner pair)
        i_mod = (p + 1) % l
        first = (cnt == 0)
        d = c0[(i_mod-1) % l] - c0[(-i_mod) % l] + (1 if first else 0) - (1 if first else 0)*0
        # for i=1, its partner is K: T_1 = c0[0]-c0[(-1)%l] + 1 ; partner value q = p_left - T_1
        if first: d = c0[0] - c0[(-1) % l] + 1
        np_, nc = (p + 1) % l, min(cnt + 1, l)
        # word = a^P b  INNER  a^Q b  with P - Q = d, P,Q >= 0
        for P in range(0, n):
            Q = P - d
            if Q < 0: continue
            rest = n - P - Q - 2
            if rest < 0: break
            for inner in S(rest, np_, nc):
                out.add('a'*P + 'b' + inner + 'a'*Q + 'b')
        return frozenset(out)
    return lambda n: S(n, 0, 0)

def check(c0, GMAX=14, PMAX=22, FMAX=60):
    gen = make_gen(c0)
    for n in range(GMAX + 1):
        c = {''.join(t) for t in itertools.product('ab', repeat=n) if in_cond(c0, ''.join(t))}
        assert set(gen(n)) == c, (c0, n)
    tot = 0
    for n in range(1, PMAX + 1):
        for w in gen(n):
            tot += 1; assert primitive(w), (c0, w)
    fam = 0
    m0 = max(0, -min(c0))
    for m in range(m0, FMAX):
        for k in range(2, FMAX):
            w = 'a' + ''.join('a'*(m+c) + 'b' for c in c0) * k
            if len(w) > FMAX: break
            assert in_cond(c0, w), w; fam += 1
    print(f'c0={c0}: grammar==condition to n={GMAX}; {tot} words up to {PMAX} all primitive; {fam} family members <= {FMAX} in L')

if __name__ == '__main__':
    check((0, 1, 3))                      # CL2 family
    for c0 in [(0, 1), (0, 0, 1), (0, 2, 1, 5), (1, 0, 0, 2), (0, 1, 3, 2, 0)]:
        check(c0, GMAX=12, PMAX=18, FMAX=50)
