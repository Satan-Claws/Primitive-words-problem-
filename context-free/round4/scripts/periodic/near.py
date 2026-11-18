# (1) Hamming lemma: distinct non-primitive words of equal length differ in >=2 positions.
# (2) Insertion near-powers: c inserted anywhere into u^k (k>=2): list non-primitive cases.
import itertools,sys
from common import primitive
N=int(sys.argv[1])
for n in range(1,N+1):
    np_=[ ''.join(t) for t in itertools.product('ab',repeat=n) if not primitive(''.join(t))]
    S=set(np_)
    bad=0
    for w in np_:
        for i in range(n):
            w2=w[:i]+('a' if w[i]=='b' else 'b')+w[i+1:]
            if w2 in S: bad+=1
    print('n',n,'nonprim',len(np_),'ham1 pairs among nonprim',bad)
# insertion
ex=[]
for L in range(1,N):
    for t in itertools.product('ab',repeat=L):
        u=''.join(t)
        if not primitive(u): continue
        for k in range(2, (N)//L+1):
            P=u*k
            for i in range(len(P)+1):
                for c in 'ab':
                    w=P[:i]+c+P[i:]
                    if not primitive(w): ex.append((u,k,i,c,w))
print('insertion counterexamples (u primitive,k>=2):',len(ex)); print(ex[:20])
