"""Independent check of Theorem C (PA/poly_S4C.md):
amb_{G'}(w) = sum_j amb_G(rot_j w) for random CNF G, where G' is the inverted-path
cyclic closure with the eps-rule [S]->eps eliminated (so G' is eps-free, unit-free, cycle-free).
Tree counts of G' are computed by a generic CYK-style counter for rules with RHS length <= 2."""
import random, itertools, functools, sys

def count_cnf(rules_bin, rules_term, S, w):
    n=len(w); T={}
    for i in range(n):
        for A,x in rules_term:
            if x==w[i]: T[(i,i+1,A)]=T.get((i,i+1,A),0)+1
    for L in range(2,n+1):
        for i in range(n-L+1):
            j=i+L
            for (A,B,C) in rules_bin:
                s=0
                for k in range(i+1,j):
                    s+=T.get((i,k,B),0)*T.get((k,j,C),0)
                if s: T[(i,j,A)]=T.get((i,j,A),0)+s
    return T.get((0,n,S),0)

def closure(N, rules_bin, rules_term, S):
    # G' rules: symbols are ('n',A) original, ('o',A) = [A], 'S1'; terminals strings
    R=[]  # (lhs, rhs tuple)
    for (B,A,C) in rules_bin:           # B -> A C
        # [A] -> C [B]   ; [C] -> [B] A
        R.append((('o',A),(('n',C),('o',B))))
        R.append((('o',C),(('o',B),('n',A))))
    for (A,x) in rules_term:
        R.append(('S1',(x,('o',A))))
    for (A,B,C) in rules_bin: R.append((('n',A),(('n',B),('n',C))))
    for (A,x) in rules_term: R.append((('n',A),(x,)))
    # eliminate [S] -> eps: [S] derives eps uniquely; add copies with [S] dropped
    R2=[]
    for lhs,rhs in R:
        R2.append((lhs,rhs))
        if ('o',S) in rhs:
            r=tuple(s for s in rhs if s!=('o',S))
            if r: R2.append((lhs,r))
    return R2  # note: occurrences of ('o',S) kept for non-eps derivations

def count_general(R, start, w):
    n=len(w)
    @functools.lru_cache(None)
    def c(X,i,j):
        if isinstance(X,str) and X in 'ab': return 1 if j==i+1 and w[i]==X else 0
        tot=0
        for lhs,rhs in R:
            if lhs!=X: continue
            if len(rhs)==1:
                tot+=c(rhs[0],i,j)   # only terminal unit rules or [A]->C (C original, no cycle)
            else:
                for k in range(i+1,j): tot+=c(rhs[0],i,k)*c(rhs[1],k,j)
        return tot
    return c(start,0,n)

random.seed(int(sys.argv[1]) if len(sys.argv)>1 else 1)
mism=tot=0
for g in range(40):
    N=list(range(3)); S=0
    rb=[(A,B,C) for A in N for B in N for C in N if random.random()<0.25]
    rt=[(A,x) for A in N for x in 'ab' if random.random()<0.6]
    R=closure(N,rb,rt,S)
    for n in range(1,8):
        for t in itertools.product('ab',repeat=n):
            w=''.join(t)
            lhs=count_general(R,'S1',w)
            rhs=sum(count_cnf(rb,rt,S,w[j:]+w[:j]) for j in range(n))
            tot+=1; mism+= (lhs!=rhs); nz=globals().get("nz",0)+(rhs>0); globals()["nz"]=nz; mx=max(globals().get("mx",0),rhs); globals()["mx"]=mx
print(f"Theorem C check: {tot} pairs, {nz} nonzero, max mass {mx}, {mism} mismatches")
