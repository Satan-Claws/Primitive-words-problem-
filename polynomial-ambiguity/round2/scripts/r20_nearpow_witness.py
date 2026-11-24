"""r20_nearpow: (a) every near-power (u^p, one letter flipped, p>=2) is primitive, n<=16;
(b) witness counts: for w of length n and prime q|n, W_q(w) = #{j in Z_n : w_j != w_{j+n/q}}.
w primitive iff W_q(w)>0 for all prime q|n. Compare near-powers (min over q) with all primitive words."""
from itertools import product
def prim(w):
    n=len(w); return all(w!=w[k:]+w[:k] for k in range(1,n) if n%k==0)
def primes(n): return [q for q in range(2,n+1) if n%q==0 and all(q%r for r in range(2,q))]
def W(w,q):
    n=len(w); e=n//q; return sum(w[j]!=w[(j+e)%n] for j in range(n))
bad=0
for n in range(2,17):
    NP=set()
    for d in range(1,n//2+1):
        if n%d: continue
        for u in product('ab',repeat=d):
            base=list(u)*(n//d)
            for i in range(n):
                w=base[:]; w[i]='b' if w[i]=='a' else 'a'; NP.add(''.join(w))
    bad+=sum(not prim(w) for w in NP)
    if n in (12,16):
        allw=[''.join(t) for t in product('ab',repeat=n)]
        Qn=[w for w in allw if prim(w)]
        mn=lambda w:min(W(w,q) for q in primes(n))
        tot=lambda w:sum(W(w,q) for q in primes(n))
        print(f"n={n} |Q|={len(Qn)} |NP|={len(NP)} NP: max min_q W={max(map(mn,NP))} max sum_q W={max(map(tot,NP))}; "
              f"Q: mean min_q W={sum(map(mn,Qn))/len(Qn):.2f}")
print("non-primitive near-powers found:",bad)
