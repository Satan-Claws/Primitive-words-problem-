# Independent check of Theorem C: grammars for A1, A2 (as described in ambiguity.md, rebuilt from the
# text, CNF-converted here) are each unambiguous with language exactly A1 resp. A2 (checked on all
# words over {a,b} up to length Lmax, not only on (ab*)^p), and A1 u A2 = Q n (ab*)^p.
import itertools, sys
from functools import lru_cache
def prim(w):
    n=len(w); return all(w!=w[:d]*(n//d) for d in range(1,n) if n%d==0)
def grammar(p, first):
    G={}
    def r(A,*rhs): G.setdefault(A,[]).append(rhs)
    r('Bs'); r('Bs','b','Bs'); r('Bp','b'); r('Bp','b','Bp')
    r('F','a','Bs'); r('P','b','P','b'); r('P','a'); r('Eq','a','P')
    r('U','b','U','b'); r('U','Bp','a'); r('U','a','Bp'); r('Ne','a','U')
    pairs=[(i,i+1) for i in range(first,p,2)]
    for t in range(len(pairs)):
        rhs=[]; pos=1
        for j,(i1,i2) in enumerate(pairs):
            rhs += ['F']*(i1-pos); pos=i1
            rhs += ['Eq'] if j<t else (['Ne'] if j==t else ['F','F']); pos+=2
        rhs += ['F']*(p+1-pos)
        r('S',*rhs)
    return G
def binarize(G):
    # convert to rules with <=2 symbols (bijection on trees), keep epsilon rules (Bs->eps)
    H={}; k=[0]
    for A,rs in G.items():
        for rhs in rs:
            cur=A; rhs=list(rhs)
            while len(rhs)>2:
                k[0]+=1; N='_N%d'%k[0]
                H.setdefault(cur,[]).append((rhs[0],N)); cur=N; rhs=rhs[1:]
            H.setdefault(cur,[]).append(tuple(rhs))
    return H
def count(H,w):
    @lru_cache(None)
    def c(X,i,j):
        if X in 'ab': return int(j==i+1 and w[i]==X)
        tot=0
        for rhs in H[X]:
            if len(rhs)==0: tot+= int(i==j)
            elif len(rhs)==1: tot+=c(rhs[0],i,j)
            else:
                for m in range(i,j+1): 
                    a=c(rhs[0],i,m)
                    if a: tot+=a*c(rhs[1],m,j)
        return tot
    return c('S',0,len(w))
def exps(w,p):
    if w.count('a')!=p or not w.startswith('a'): return None
    return [len(s) for s in w.split('a')[1:]]
def inA(x,first):
    return any(x[i-1]!=x[i] for i in range(first,len(x),2))
p=int(sys.argv[1]); Lmax=int(sys.argv[2])
H1,H2=binarize(grammar(p,1)),binarize(grammar(p,2))
bad=0; n=0
for L in range(0,Lmax+1):
    for t in itertools.product('ab',repeat=L):
        w=''.join(t); x=exps(w,p); n+=1
        c1,c2=count(H1,w),count(H2,w)
        e1= int(x is not None and inA(x,1)); e2=int(x is not None and inA(x,2))
        if (c1,c2)!=(e1,e2): bad+=1; print("BAD",w,c1,c2,e1,e2)
        if x is not None and (e1 or e2)!=prim(w): bad+=1; print("UNION BAD",w)
print("p=%d all %d words of length<=%d: failures %d"%(p,n,Lmax,bad))
