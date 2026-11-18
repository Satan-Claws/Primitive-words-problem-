# Mixed-depth substitution: X -> b | Z a, Z = nonempty Dyck word over (X open, a close).
# Language MIX = Cyc( E'[b := X] ) U swap.  Test soundness exhaustively.
import sys
N = int(sys.argv[1]) if len(sys.argv) > 1 else 16
from functools import lru_cache
def cat(A, B, n):  # A,B: dict len->set ; return set of length n concatenations
    out = set()
    for i in range(n+1):
        for x in A.get(i, ()):
            for y in B.get(n-i, ()):
                out.add(x+y)
    return out
# languages as dict length -> set of strings
X = {1: {'b'}}; W = {0: {''}}; K = {0: {''}}
# iterate to fixed point per length increasing
for n in range(1, N+1):
    # W -> eps | X W a W  ; X -> b | Z a with Z = W nonempty
    # need W up to n, X up to n. X_n depends on W_{n-1}; W_n depends on X_{<n}, W_{<n}
    if n >= 2:
        X.setdefault(n, set()).update(w+'a' for w in W.get(n-1, ()) if w)
    s = set()
    for i in range(1, n):          # X part length i
        for j in range(0, n-i):    # W part
            k = n-i-j-1
            if k < 0: continue
            for x in X.get(i, ()):
                for w1 in W.get(j, ()):
                    for w2 in W.get(k, ()):
                        s.add(x+w1+'a'+w2)
    W[n] = s
    # X_n again (W_{n-1} done earlier) fine
# E'-shaped over tokens: K -> eps | a K X K | X K a K ; S -> K a K | K X K
A = {1: {'a'}}
for n in range(1, N+1):
    s = set()
    for (P1, P2) in ((A, X), (X, A)):
        for i in P1:
            for j in range(0, n):
                for l in P2:
                    k = n - i - j - l
                    if k < 0: continue
                    for p in P1[i]:
                        for k1 in K.get(j, ()):
                            for q in P2[l]:
                                for k2 in K.get(k, ()):
                                    s.add(p+k1+q+k2)
    K[n] = s
def prim(w):
    n = len(w)
    return all(not (n % d == 0 and w[d:]+w[:d] == w) for d in range(1, n))
sw = str.maketrans('ab', 'ba')
for n in range(1, N+1):
    S = set()
    for (P,) in ((A,), (X,)):
        for i in P:
            for j in range(0, n-i+1):
                k = n - i - j
                for k1 in K.get(j, ()):
                    for p in P[i]:
                        for k2 in K.get(k, ()):
                            S.add(k1+p+k2)
    C = set()
    for w in S:
        for r in range(n):
            u = w[r:]+w[:r]; C.add(u); C.add(u.translate(sw))
    bad = [w for w in C if not prim(w)]
    print(n, len(S), len(C), round(len(C)/2**n, 4), 'nonprim', len(bad), sorted(bad)[:3], flush=True)
