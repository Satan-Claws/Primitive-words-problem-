# Random test of Lemma X: V laminar (non-crossing supports, size 1 or 2, positive entries) in R^{2M},
# W = span{e_i+e_{M+i}} subset span V  ==>  dim span V >= 2M-1.
# Also test the corollary used: if W subset span V, the coordinate functionals vanishing on W number <= 1
# when V is a basis.
import random, numpy as np
def crossing(p,q):
    a,b=sorted(p); c,d=sorted(q)
    return (a<c<b<d) or (c<a<d<b)
def rank(A): return np.linalg.matrix_rank(np.array(A,dtype=float)) if len(A) else 0
random.seed(1); found=0; tests=0; viol=0
for trial in range(200000):
    M=random.randint(2,5); n=2*M
    V=[];sup=[]
    for _ in range(random.randint(1,2*n)):
        if random.random()<0.3: s=(random.randrange(n),)
        else:
            p,q=random.sample(range(n),2); s=(min(p,q),max(p,q))
        if any(len(s)==2 and len(t)==2 and crossing(s,t) for t in sup): continue
        v=[0]*n
        for i in s: v[i]=random.randint(1,3)
        V.append(v); sup.append(s)
    r=rank(V)
    W=[[1 if j in (i,M+i) else 0 for j in range(n)] for i in range(M)]
    if rank(V+W)==r:   # W in span V
        tests+=1
        if r<2*M-1: viol+=1; print('VIOLATION',M,sup,V)
print('cases with W in span V:',tests,'violations:',viol)
