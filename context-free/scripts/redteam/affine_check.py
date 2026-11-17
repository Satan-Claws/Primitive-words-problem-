# Redteam check of rectangles Thm B / Lemma 3.1 / Cor 3.3.
import sys, random, math
from rt_common import *
random.seed(7)
def span(gens):
    S={0}
    for g in gens:
        S|={x^g for x in S}
    return S
par=lambda x: bin(x).count('1')&1
for n in range(2,15):
    P=primes_of(n); k=len(P)
    prim=[is_primitive_str(to_str(w,n)) for w in range(1<<n)]
    Sp={}
    for p in P:
        d=n//p
        gens=[(1<<i)|(1<<((i+d)%n)) for i in range(n) if i+d<n]
        S=span(gens); assert len(S)==1<<(n-d)
        # direct definition of S_p: residue-class sums zero
        for s in range(1<<n):
            inS=all(sum((s>>(r+t*d))&1 for t in range(p))%2==0 for r in range(d))
            assert inS==(s in S)
        Sp[p]=sorted(S)
        for w in range(1<<n):
            Vp=all(((w>>i)&1)==((w>>((i+d)%n))&1) for i in range(n))
            ones=sum(par(w&s) for s in S)
            assert (ones==0) if Vp else (2*ones==len(S)), (n,p,w)
    # random cover; check T subset Q and union
    Nb=math.ceil(2**k*n*math.log(2))
    covered=set(); used=0
    target={w for w in range(1<<n) if prim[w]}
    tuples=[]
    while covered!=target and used<50*Nb:
        tup=[random.choice(Sp[p]) for p in P]; used+=1
        T={w for w in range(1<<n) if all(par(w&s) for s in tup)}
        assert T<=target
        covered|=T; tuples.append(tup)
    assert covered==target
    # build NFA as union of DFAs over (position, parity vector) and test acceptance of all words
    def accepts(w):
        for tup in tuples:
            vec=0
            for i in range(n):
                if (w>>i)&1:
                    for j,s in enumerate(tup):
                        if (s>>i)&1: vec^=1<<j
            if vec==(1<<k)-1: return True
        return False
    assert all(accepts(w)==prim[w] for w in range(1<<n))
    states=(n+1)*2**k*len(tuples)+1
    print(n,'k',k,'tuples used',len(tuples),'bound',Nb,'NFA states',states,'bound 1.85n^3+...',round(1.85*n**3+2.85*n**2+n+1))
print('ALL PASS')
