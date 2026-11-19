"""Cross-length fooling sets for a rotation-closed language L (here Q, and E' as sanity check).
F is fooling if for all distinct w,w' in F and ALL balanced conjugate factorizations (y,m) of w,
(y',m') of w' (n/3 < |y| <= 2n/3): y m' not in L or y' m not in L.
If L has a CNF grammar with g nonterminals, then |F| <= g (Lemma 4). We compute the maximum
fooling set among conjugacy classes of length <= N (exact max clique)."""
import sys, itertools
from fracpos import primitive, words

def facts(w):
    n=len(w); out=set()
    for r in range(n):
        v=w[r:]+w[:r]
        for l in range(n//3+1,2*n//3+1):
            if 3*l>n: out.add((v[:l],v[l:]))
    return list(out)

def run(N,inL,name):
    reps=[]; seen=set()
    for n in range(2,N+1):
        for w in words(n):
            if not inL(w): continue
            c=min(w[r:]+w[:r] for r in range(n))
            if c not in seen: seen.add(c); reps.append(c)
    F={c:facts(c) for c in reps}
    cache={}
    def ok(x):
        if x not in cache: cache[x]=inL(x)
        return cache[x]
    adj={c:set() for c in reps}
    for i,c in enumerate(reps):
        for d in reps[i+1:]:
            fool=True
            for (y,m) in F[c]:
                for (y2,m2) in F[d]:
                    if ok(y+m2) and ok(y2+m): fool=False;break
                if not fool:break
            if fool: adj[c].add(d); adj[d].add(c)
    # max clique (Bron-Kerbosch with pivot)
    best=[]
    def bk(R,P,X):
        nonlocal best
        if not P and not X:
            if len(R)>len(best): best=R[:]
            return
        u=max(P|X,key=lambda v:len(adj[v]&P))
        for v in list(P-adj[u]):
            bk(R+[v],P&adj[v],X&adj[v]); P.remove(v); X.add(v)
    bk([],set(reps),set())
    ne=sum(len(a) for a in adj.values())//2
    print(name,"N=",N,"classes",len(reps),"fooling edges",ne,"max fooling set",len(best),best)

if __name__=="__main__":
    N=int(sys.argv[1])
    run(N,primitive,"Q")
    run(N,lambda w: w.count('b')==w.count('a')+1,"E'")
