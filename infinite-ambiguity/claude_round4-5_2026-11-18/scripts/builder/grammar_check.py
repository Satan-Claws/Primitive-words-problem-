# Literal grammar for D2 and checks:
#   S -> Y | X Y ;  X -> a | b
#   Y -> a Y a | b Y b | a Z b            (outer pairs equal until first strict pair (a,b))
#   Z -> a Z a | b Z b | a Z b | X | eps   (after a strict pair: no (b,a) pair allowed)
# (1) L(S) computed by DP equals the predicate "some reflection of type i->n-1-i on w or on w[1:]
#     has no (b,a) mirror pair and >=1 (a,b) pair"; (2) L(S) subset of Q, n<=16;
# (3) Cyc(L(S)) misses (necklaces) up to N; (4) family F1_m = b b a^m b a b a^m missed, m=2..M.
import sys
from functools import lru_cache
from common import *

def gen_Y(w):
    @lru_cache(None)
    def Z(i, j):  # w[i:j]
        L = j - i
        if L <= 1: return True
        x, y = w[i], w[j - 1]
        return x <= y and Z(i + 1, j - 1)
    @lru_cache(None)
    def Y(i, j):
        if j - i < 2: return False
        x, y = w[i], w[j - 1]
        if x == y: return Y(i + 1, j - 1)
        if x < y: return Z(i + 1, j - 1)
        return False
    return Y

def inS(w):
    Y = gen_Y(w); n = len(w)
    return Y(0, n) or (n >= 1 and Y(1, n))

def pred(w):
    def dom(v):
        m = len(v); st = False
        for i in range(m // 2):
            if v[i] > v[m - 1 - i]: return False
            if v[i] < v[m - 1 - i]: st = True
        return st
    return dom(w) or dom(w[1:])

if __name__ == '__main__':
    N, M = int(sys.argv[1]), int(sys.argv[2])
    for n in range(1, 17):
        for w in all_words(n):
            a = inS(w)
            assert a == pred(w), s(w)
            if a: assert is_primitive(w), s(w)
    print('grammar == predicate and L(S) subset Q for all words of length <= 16')
    tot = 0
    for n in range(1, N + 1):
        miss = 0; neck = 0
        for w in lyndon(n):
            neck += 1
            if not any(inS(r) for r in rotations(w)): miss += 1
        print('n=%d necklaces=%d missed=%d fraction_missed=%.3f' % (n, neck, miss, miss / neck), flush=True)
    for m in range(2, M + 1):
        w = (1, 1) + (0,) * m + (1, 0, 1) + (0,) * m
        assert is_primitive(w)
        assert not any(inS(r) for r in rotations(w)), m
    print('F1_m = bba^m bab a^m missed by Cyc(L(S)) for m = 2..%d' % M)
