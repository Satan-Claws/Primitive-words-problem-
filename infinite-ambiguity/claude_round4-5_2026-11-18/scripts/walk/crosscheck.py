# Cross-check: Cyc(sigma(M)) u mirror, built LITERALLY by substitution + rotation,
# equals the set accepted by T(cert_M) of walk.py, for M = E' and M = T(E'), n<=14.
import itertools
from walk import certE, T
def pieces_upto(n):          # P = {z a : z in B}, B = walk<=0 returning to 0
    res = {}
    for L in range(1, n+1):
        for z in itertools.product((1,-1), repeat=L-1):
            s=0; ok=True
            for x in z:
                s+=x
                if s>0: ok=False;break
            if ok and s==0: res.setdefault(L,[]).append(z+(1,))
    return res
def sigma_words(n, Mtest, P):
    out=set()
    def rec(prefix, letters, L):
        if L==n:
            if Mtest(tuple(letters)): out.add(prefix)
            return
        for l in range(1,n-L+1):
            for p in P.get(l,[]):
                rec(prefix+p, letters+[1 if l==1 else -1], L+l)
    rec((),[],0); return out
for name, M in [("E'", certE), ("T(E')", T(certE))]:
    for n in range(1, 15):
        P = pieces_upto(n)
        S = sigma_words(n, M, P)
        C = set()
        for w in S:
            for i in range(n):
                r = w[i:]+w[:i]; C.add(r); C.add(tuple(-x for x in r))
        A = {v for v in itertools.product((1,-1),repeat=n) if T(M)(v)}
        assert A == C, (name, n)
    print(name, "ok n<=14")
