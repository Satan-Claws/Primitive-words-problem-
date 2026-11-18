import random, itertools
def prim(w):
    n=len(w); return n>0 and all(w!=w[d:]+w[:d] for d in range(1,n) if n%d==0)
def langs(G,T,NT,N):
    L={X:set() for X in NT}
    for X,a in T: L[X].add(a)
    ch=True
    while ch:
        ch=False
        for B,C,D in G:
            for y in list(L[C]):
                for z in list(L[D]):
                    if len(y)+len(z)<=N and y+z not in L[B]: L[B].add(y+z); ch=True
    return L
def test(G,T,NT,N):
    L=langs(G,T,NT,N)
    Ctx={X:set() for X in NT}; Ctx['S'].add(('',''))
    ch=True
    while ch:
        ch=False
        for B,C,D in G:
            for x,z in list(Ctx[B]):
                for yD in L[D]:
                    c=(x,yD+z)
                    if len(x)+len(yD+z)<=N and c not in Ctx[C]: Ctx[C].add(c); ch=True
                for yC in L[C]:
                    c=(x+yC,z)
                    if len(x+yC)+len(z)<=N and c not in Ctx[D]: Ctx[D].add(c); ch=True
    M={X:set(z+x for x,z in Ctx[X]) for X in NT}
    # bracket grammar
    Mg={X:set() for X in NT}; Mg['S'].add('')
    ch=True
    while ch:
        ch=False
        for B,C,D in G:
            for m in list(Mg[B]):
                for yD in L[D]:
                    v=yD+m
                    if len(v)<=N and v not in Mg[C]: Mg[C].add(v); ch=True
                for yC in L[C]:
                    v=m+yC
                    if len(v)<=N and v not in Mg[D]: Mg[D].add(v); ch=True
    return all(M[X]==Mg[X] for X in NT)
random.seed(1); NT=['S','A','B','C']; ok=0
for t in range(200):
    G=[tuple(random.choice(NT) for _ in range(3)) for _ in range(5)]
    T=[(X,random.choice('ab')) for X in NT if random.random()<.7]
    ok+=test(G,T,NT,7)
print('Lemma1(c) random grammars agree:',ok,'/200')
# Lemma 4 literal counterexample: L=Sigma^+, CNF S->SS|a|b (g=1), F={a,b}: no bcf, vacuous
def bcfs(w):
    n=len(w); out=[]
    for r in range(n):
        v=w[r:]+w[:r]
        for l in range(1,n):
            if n/3<l<=2*n/3: out.append((v[:l],v[l:]))
    return out
print('bcf of a:',bcfs('a'))
# fooling pairs among primitive necklaces lengths 2..10
nk=[]
for n in range(2,11):
    seen=set()
    for t in itertools.product('ab',repeat=n):
        w=''.join(t)
        if not prim(w): continue
        c=min(w[r:]+w[:r] for r in range(n))
        if c not in seen: seen.add(c); nk.append(c)
B={w:bcfs(w) for w in nk}
fool=0
for i in range(len(nk)):
    for j in range(i+1,len(nk)):
        w,v=nk[i],nk[j]
        # fooling pair iff for all bcf (y,m),(y',m'): not(prim(ym') and prim(y'm))
        if not any(prim(y+m2) and prim(y2+m) for y,m in B[w] for y2,m2 in B[v]):
            fool+=1; print('fooling pair',w,v); 
print('fooling pairs len<=10:',fool,'classes',len(nk))
