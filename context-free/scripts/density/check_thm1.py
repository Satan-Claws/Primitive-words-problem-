"""Computer check of Theorem 1 (fixed-rate linear languages).

Random (p,q)-fixed-rate linear languages L are given by a complete DFA over
Gamma = Sigma^p x Sigma^q and a finite set C of middle words, with a final-state set F_c for each c.
For each L the script:
  1. computes the transition monoid and a word kappa whose transformation is
     an idempotent of minimal rank r;
  2. builds a word u0 in L whose fold has the form P kappa S;
  3. checks that u0 (v u0)^{(p+q) g j} is in L for g = r!, several random v, and j = 0..2.
It also checks the proof's identity fold(x) = (fold(u0) X)^m fold(u0).
"""
import random, itertools, math, sys
from collections import deque

def fold(w, p, q, c):
    n = len(w)
    if (n - len(c)) < 0 or (n - len(c)) % (p + q):
        return None
    t = (n - len(c)) // (p + q)
    if w[p*t:p*t+len(c)] != c:
        return None
    ys = []
    for i in range(1, t+1):
        left = w[p*(i-1):p*i]
        right = w[n-q*i:n-q*(i-1)]
        ys.append((left, right))
    return ys

def letter_index(pair):
    left, right = pair
    s = left + right
    return int(s, 2) if s else 0

def run(dfa, q0, ys):
    s = q0
    for y in ys:
        s = dfa[s][letter_index(y)]
    return s

def member(w, L):
    p, q, dfa, q0, C = L
    for c, F in C.items():
        ys = fold(w, p, q, c)
        if ys is not None and run(dfa, q0, ys) in F:
            return True
    return False

def unfold(ys, c):
    return ''.join(l for l, r in ys) + c + ''.join(r for l, r in reversed(ys))

def letters(p, q):
    return [(format(a, '0%db' % (p+q))[:p] if p else '', format(a, '0%db' % (p+q))[p:] if q else '')
            for a in range(2**(p+q))]

def compose(f, g):  # first f then g
    return tuple(g[f[i]] for i in range(len(f)))

def monoid(dfa, nstates, p, q):
    G = letters(p, q)
    ident = tuple(range(nstates))
    seen = {ident: []}
    dq = deque([ident])
    gens = [(tuple(dfa[s][letter_index(a)] for s in range(nstates)), a) for a in G]
    while dq:
        f = dq.popleft()
        for g, a in gens:
            h = compose(f, g)
            if h not in seen:
                seen[h] = seen[f] + [a]
                dq.append(h)
    return seen

def trial(rng):
    p = rng.randint(0, 2); q = rng.randint(0, 2)
    if p + q == 0:
        p = 1
    k = 2**(p+q)
    ns = rng.randint(2, 4)
    dfa = [[rng.randrange(ns) for _ in range(k)] for _ in range(ns)]
    q0 = 0
    C = {}
    for c in ['', '0', '1', '01']:
        if rng.random() < 0.6:
            C[c] = set(s for s in range(ns) if rng.random() < 0.4)
    C = {c: F for c, F in C.items() if F}
    if not C:
        return None
    L = (p, q, dfa, q0, C)
    M = monoid(dfa, ns, p, q)
    r = min(len(set(f)) for f in M)
    f0 = next(f for f in M if len(set(f)) == r)
    # idempotent power
    w = M[f0]; f = f0; e = f0; kap = list(w)
    pw = f0; word = list(w)
    while compose(pw, pw) != pw:
        pw = compose(pw, f0); word = word + list(w)
    kappa = word
    # find P, S, c with q0 . P kappa S in F_c
    reach = {}  # state -> word P
    dq = deque([q0]); reach[q0] = []
    G = letters(p, q)
    while dq:
        s = dq.popleft()
        for a in G:
            t = dfa[s][letter_index(a)]
            if t not in reach:
                reach[t] = reach[s] + [a]; dq.append(t)
    found = None
    for s, P in reach.items():
        s2 = run(dfa, s, kappa)
        # BFS for S
        back = {s2: []}; dq = deque([s2])
        while dq:
            u = dq.popleft()
            for a in G:
                t = dfa[u][letter_index(a)]
                if t not in back:
                    back[t] = back[u] + [a]; dq.append(t)
        for c, F in C.items():
            for fstate in F:
                if fstate in back:
                    found = (P + kappa + back[fstate], c); break
            if found: break
        if found: break
    if not found:
        return 'nokappa'
    y0, c = found
    u0 = unfold(y0, c)
    assert member(u0, L)
    g = math.factorial(r)
    D = (p + q) * g
    for _ in range(3):
        v = ''.join(rng.choice('01') for _ in range(rng.randint(0, 5)))
        for j in range(3):
            x = u0 + (v + u0) * (D * j)
            assert member(x, L), (p, q, u0, v, j)
            # identity: fold(x) = (fold(u0) X)^m fold(u0)
            ys = fold(x, p, q, c)
            d = len(v) + len(u0); m = D * j // (p + q)
            assert ys == (ys[:d] * m + fold(u0, p, q, c)) if m else ys == fold(u0, p, q, c)
            assert ys[:len(y0)] == y0
    return 'ok'

if __name__ == '__main__':
    rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
    stats = {}
    for _ in range(int(sys.argv[2]) if len(sys.argv) > 2 else 300):
        res = trial(rng)
        stats[res] = stats.get(res, 0) + 1
    print(stats)
