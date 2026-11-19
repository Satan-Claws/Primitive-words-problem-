# S4C: verify amb_{G'}(w) = sum_{j<|w|} amb_G(rot_j w) for the inverted-path cyclic-closure grammar G'.
import random, itertools, functools, sys
def rand_cnf(nt, seed):
    R=random.Random(seed); N=list(range(nt)); bin_=[]; term=[]
    for A in N:
        for _ in range(R.randint(1,3)): bin_.append((A,R.choice(N),R.choice(N)))
        for c in 'ab':
            if R.random()<0.5: term.append((A,c))
    return N,bin_,term
def amb_G(G,w):
    N,bin_,term=G; n=len(w)
    @functools.lru_cache(None)
    def c(X,i,j):
        if j-i==1: return sum(1 for (A,t) in term if A==X and t==w[i])
        return sum(c(Y,i,k)*c(Z,k,j) for (A,Y,Z) in bin_ if A==X for k in range(i+1,j))
    return c(0,0,n)
def amb_Gp(G,w):
    # [A] => beta alpha ; rules: B->A C gives [A]->C[B]; B->C A gives [A]->[B]C; [S]->eps; S'->a[A] for A->a
    N,bin_,term=G; n=len(w)
    @functools.lru_cache(None)
    def c(X,i,j):
        if j-i==1: return sum(1 for (A,t) in term if A==X and t==w[i])
        return sum(c(Y,i,k)*c(Z,k,j) for (A,Y,Z) in bin_ if A==X for k in range(i+1,j))
    @functools.lru_cache(None)
    def br(A,i,j):
        s=1 if (A==0 and i==j) else 0
        for (B,Y,Z) in bin_:
            if Y==A: s+=sum(c(Z,i,k)*br(B,k,j) for k in range(i+1,j+1))
            if Z==A: s+=sum(br(B,i,k)*c(Y,k,j) for k in range(i,j))
        return s
    return sum(br(A,1,n) for (A,t) in term if t==w[0])
bad=0;tot=0
for seed in range(40):
    G=rand_cnf(3,seed)
    for n in range(1,8):
        for w in itertools.product('ab',repeat=n):
            w=''.join(w); lhs=amb_Gp(G,w); rhs=sum(amb_G(G,w[j:]+w[:j]) for j in range(n))
            tot+=1; bad+=(lhs!=rhs)
print("words checked",tot,"mismatches",bad)
