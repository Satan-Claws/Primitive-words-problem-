# Certificate refuting CL3: linear CFG G with F_2 subset L(G) subset Q.
# G:  S -> a A Y ; A -> a A a | N ; N -> Y | Y B Y ; B -> a B a | N | C ; C -> a C | eps ;
#     Y -> b D b a b ; D -> a D | eps
import sys, itertools
from functools import lru_cache
NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 30

def primitive(w):
    n = len(w)
    if n == 0: return False
    return (w + w).find(w, 1) == n

# grammar language up to length NMAX, as sets of strings per nonterminal (fixpoint)
NT = {'S': [['a','A','Y']], 'A': [['a','A','a'], ['N']], 'N': [['Y'], ['Y','B','Y']],
      'B': [['a','B','a'], ['N'], ['C']], 'C': [['a','C'], []], 'Y': [['b','D','b','a','b']],
      'D': [['a','D'], []]}
lang = {X: set() for X in NT}
changed = True
while changed:
    changed = False
    for X, rules in NT.items():
        for r in rules:
            parts = [[s] if s not in NT else sorted(lang[s]) for s in r]
            # combine with length pruning
            cur = {''}
            for p in parts:
                cur = {u + v for u in cur for v in p if len(u) + len(v) <= NMAX}
            new = cur - lang[X]
            if new:
                lang[X] |= new; changed = True
LG = lang['S']

def blocks(w):
    # w in (a*b)^+ -> exponent vector
    assert w.endswith('b')
    return [len(t) for t in w.split('b')[:-1]]

def cond(w):
    if not w or not w.endswith('b') or set(w) - set('ab'): return False
    x = blocks(w); K = len(x)
    if K % 3 or K < 6: return False
    k = K // 3
    if any(x[3*i+2] != 1 for i in range(k)): return False
    P = [x[3*i] for i in range(k)]
    if P[0] - P[k-1] != 1: return False
    return all(P[i] == P[k-1-i] for i in range(1, k-1))

# condition-defined set up to NMAX (enumerate via block vectors)
CD = set()
def gen(prefix_len, xs):
    pass
# brute-force over all words of (a*b)^+ up to NMAX is 2^NMAX; instead enumerate block vectors
def compositions(total, parts):
    if parts == 1:
        yield (total,); return
    for f in range(total + 1):
        for rest in compositions(total - f, parts - 1):
            yield (f,) + rest
for K in range(6, NMAX + 1, 3):
    k = K // 3
    # length = sum(x) + K, ones contribute k; free a's: NMAX - K - k
    for tot in range(0, NMAX - K - k + 1):
        for c in compositions(tot, 2 * k):
            x = []
            for i in range(k):
                x += [c[2*i], c[2*i+1], 1]
            w = ''.join('a' * e + 'b' for e in x)
            if cond(w): CD.add(w)
print('NMAX', NMAX, '|L(G)|', len(LG), '|cond|', len(CD), 'equal', LG == CD)
bad = [w for w in LG if not primitive(w)]
print('non-primitive in L(G):', len(bad), bad[:5])
# F_2 membership
cnt = 0; miss = []
for p in range(1, NMAX):
    for q in range(1, NMAX):
        for k in range(2, NMAX):
            w = 'a' + ('a'*p + 'b' + 'a'*q + 'b' + 'ab') * k
            if len(w) > NMAX: break
            cnt += 1
            if w not in LG: miss.append(w)
print('F_2 members <= NMAX:', cnt, 'missing:', len(miss))
# control: drop the +1 offset -> powers appear
ctrl = [w for w in CD]
