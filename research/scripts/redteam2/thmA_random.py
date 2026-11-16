# Random test of Theorem A, Steps 1-2: for random CNF grammars G, form G_D (product with DFA of (ab*)^n),
# reduce, and for each useful SCC check:
#  Step 2: all members share one state pair (s,t); every side nonterminal Z (rule X->YZ / X->ZY, Y in C)
#          has annotation (t,.,t) resp. (s,.,s), i.e. generates b-words only.
#  Step 1: if a useful SCC has a rule with both children in it, then max_{|w|<=L} d(w) grows
#          at least like Catalan numbers (we check that max ambiguity at length <= L is >= C_r for the
#          r reachable, i.e. it is strictly increasing over L in a window).
import random, itertools, sys
from functools import lru_cache
def scc(nodes, edges):
    idx={};low={};st=[];on=set();out=[];c=[0]
    sys.setrecursionlimit(10000)
    def dfs(v):
        idx[v]=low[v]=c[0];c[0]+=1;st.append(v);on.add(v)
        for w in edges.get(v,()):
            if w not in idx: dfs(w); low[v]=min(low[v],low[w])
            elif w in on: low[v]=min(low[v],idx[w])
        if low[v]==idx[v]:
            comp=set()
            while True:
                w=st.pop();on.discard(w);comp.add(w)
                if w==v: break
            out.append(comp)
    for v in nodes:
        if v not in idx: dfs(v)
    return out
def delta(s,c,n):
    if s=='K': return 'K'
    if c=='a': return s+1 if s<n else 'K'
    return s if s>=1 else 'K'
def trial(rng,n=2,N=4):
    NT=list(range(N))
    bin_rules=[(A,rng.randrange(N),rng.randrange(N)) for A in NT for _ in range(rng.randint(1,3))]
    term=[(A,c) for A in NT for c in 'ab' if rng.random()<0.5]
    states=list(range(n+1))+['K']
    P_bin=set();P_term=set()
    for (A,B,C) in bin_rules:
        for s in states:
            for r in states:
                for t in states: P_bin.add(((s,A,t),(s,B,r),(r,C,t)))
    for (A,c) in term:
        for s in states: P_term.add(((s,A,delta(s,c,n)),c))
    # productive
    prod=set(X for X,c in P_term)
    ch=True
    while ch:
        ch=False
        for X,Y,Z in P_bin:
            if X not in prod and Y in prod and Z in prod: prod.add(X);ch=True
    S=(0,0,n)
    if S not in prod: return None
    P_bin={r for r in P_bin if all(x in prod for x in r)}
    reach={S};ch=True
    while ch:
        ch=False
        for X,Y,Z in P_bin:
            if X in reach:
                for W in (Y,Z):
                    if W not in reach: reach.add(W);ch=True
    P_bin={r for r in P_bin if r[0] in reach}; P_term={r for r in P_term if r[0] in reach}
    edges={}
    for X,Y,Z in P_bin: edges.setdefault(X,set()).update([Y,Z])
    comps=scc(sorted(reach,key=str),edges)
    where={v:i for i,cmp in enumerate(comps) for v in cmp}
    nonlinear=False
    for cmp in comps:
        pairs={(X[0],X[2]) for X in cmp}
        if len(cmp)>1 or any(X in edges.get(X,()) for X in cmp):
            assert len(pairs)==1,("step2 pairs",pairs)
        for X,Y,Z in P_bin:
            if X not in cmp: continue
            iy,iz=Y in cmp,Z in cmp
            if iy and iz: nonlinear=True
            elif iy: assert Z[0]==Z[2]==X[2],("step2 right",X,Y,Z)
            elif iz: assert Y[0]==Y[2]==X[0],("step2 left",X,Y,Z)
    # ambiguity profile
    def amb(w):
        @lru_cache(None)
        def c(X,i,j):
            if j==i+1: return int((X,w[i]) in P_term)
            return sum(c(Y,i,m)*c(Z,m,j) for (XX,Y,Z) in byX.get(X,()) for m in range(i+1,j))
        return c(S,0,len(w))
    byX={}
    for r in P_bin: byX.setdefault(r[0],[]).append(r)
    prof=[]
    for L in range(n,n+9):
        best=0
        for xs in itertools.product(range(L-n+1),repeat=n):
            if sum(xs)!=L-n: continue
            w=''.join('a'+'b'*x for x in xs); best=max(best,amb(w))
        prof.append(best)
    return nonlinear,prof
rng=random.Random(int(sys.argv[1]))
stats={'nl_growing':0,'nl_bounded':0,'lin':0,'none':0}
for _ in range(int(sys.argv[2])):
    res=trial(rng)
    if res is None: stats['none']+=1; continue
    nl,prof=res
    if nl:
        if prof[-1]>prof[-4]>0: stats['nl_growing']+=1
        else: stats['nl_bounded']+=1; print("nonlinear but bounded?",prof)
    else: stats['lin']+=1
print(stats)
