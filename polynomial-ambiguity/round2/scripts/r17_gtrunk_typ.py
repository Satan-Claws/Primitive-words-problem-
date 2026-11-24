# Typical pair-family multiplicity m(W) for X -> abXab | bbXa | Xba | ab under i.i.d. random token sequences.
# m(W) = number of (centre, token sequence) giving W, computed by an O(n^2) two-sided parse DP.
import random,sys,functools,statistics
sys.setrecursionlimit(100000)
toks=[('ab','ab'),('bb','a'),('','ba')]; w='ab'
def mult(M):
    n=len(M)
    @functools.lru_cache(None)
    def c(i,k):  # ways to parse M[i:k] as (pumping...)+exit
        r=1 if M[i:k]==w else 0
        for u,v in toks:
            if M.startswith(u,i) and k-len(v)>=i+len(u) and M[k-len(v):k]==v and len(u)+len(v)>0:
                r+=c(i+len(u),k-len(v))
        return r
    return c(0,n)
random.seed(1)
for probs in ([1/3,1/3,1/3],[0.6,0.2,0.2],[0.2,0.2,0.6]):
    for r in (50,200,800):
        ms=[]
        for _ in range(200):
            seq=random.choices(range(3),probs,k=r)
            U=''.join(toks[i][0] for i in seq); V=''.join(toks[i][1] for i in reversed(seq))
            ms.append(mult(U+w+V))
        print(probs,r,'mean m',round(statistics.mean(ms),2),'max',max(ms),'P(m>=3)',sum(m>=3 for m in ms)/len(ms))
