"""
Seam slice K_m = Q ∩ (b*a)^m b*, coordinates x_0..x_m, y(x)=(x_1..x_{m-1},x_m+x_0).
Forbidden subspaces H_d = {x : y(x) in V_d}, d in D(m).  Family N h* + M delta, h* = (1,2,...,2,1) in H_1.
Coverer: P1 = ratio-1 pairs (any graph, MET_k class) + singletons, with h* strictly positive combination (LP).
Attacker beats P1 iff exists face P' ⊆ P1 and d: relint cone(P') meets H_d and delta in H_d + span(P').
(h* in H_1 ⊆ H_d, so the H_d-part of the family is automatic.)  All faces are used => 'coverer wins' is sound.
"""
import sys, itertools
from arr2 import Field, rref, nullspace, max_divs
from scipy.optimize import linprog
import numpy as np
P=2**61-1; F=Field(P)
def dot(f,v): return sum(a*b for a,b in zip(f,v))%P
def contained(basis,cons): return all(dot(f,v)==0 for f in cons for v in basis)
def Hbasis(m,d):
    N=m+1; B=[]
    # y index: y_j = x_j for j=1..m-1, y_m = x_0+x_m  (use y positions 1..m, classes mod d on 1..m)
    v=[0]*N; v[0]=1; v[m]=P-1; B.append(v)       # x_0 - x_m keeps y
    for c in range(d):
        v=[0]*N
        for j in range(1,m+1):
            if j%d==c: v[j]=1
        B.append(v)
    return B
def Hperp_rows(m,d): return nullspace(F,Hbasis(m,d),m+1)
def relint_meets(vecs,m,d):
    # exists c>=1 with sum c v in H_d : constraints f(sum)=0 for f in H_d^perp (use float of small ints)
    Hp=[[x if x<P//2 else x-P for x in f] for f in Hperp_rows(m,d)]
    A=[[sum(f[i]*v[i] for i in range(m+1)) for v in vecs] for f in Hp]
    r=linprog(np.zeros(len(vecs)),A_eq=np.array(A,dtype=float),b_eq=np.zeros(len(A)),bounds=[(1,None)]*len(vecs),method='highs')
    return r.status==0
def hstar_relint(vecs,h):
    A=[[v[i] for v in vecs] for i in range(len(h))]
    r=linprog(np.zeros(len(vecs)),A_eq=np.array(A,dtype=float),b_eq=np.array(h,dtype=float),bounds=[(1e-6,None)]*len(vecs),method='highs')
    return r.status==0
def metk_ok(pairs,m,k):
    def nested(a,b): return (a[0]<=b[0] and b[1]<=a[1]) or (b[0]<=a[0] and a[1]<=b[1])
    # exists 0=q0<=q1<=..<=qk=m with each pair inside some [q_{r-1},q_r] and nested within each
    for qs in itertools.combinations_with_replacement(range(m+1),k-1):
        bounds=[0]+list(qs)+[m]; ok=True; groups=[[] for _ in range(k)]
        for p in pairs:
            g=[r for r in range(k) if bounds[r]<=p[0] and p[1]<=bounds[r+1]]
            if not g: ok=False; break
            groups[g[0]].append(p)   # put in first possible (pairs inside a degenerate shared point impossible)
        if not ok: continue
        if all(nested(a,b) for gr in groups for a,b in itertools.combinations(gr,2)): return True
    return False
def structures(m,k,maxpairs):
    N=m+1; allp=[(i,j) for i in range(N) for j in range(i+1,N)]
    h=[1]+[2]*(m-1)+[1]
    res=[]
    def rec(start,cur):
        if cur or True:
            cov=set(x for p in cur for x in p)
            for extra in ('unc','all'):
                S=[x for x in range(N) if x not in cov] if extra=='unc' else list(range(N))
                vecs=[]
                for (i,j) in cur:
                    v=[0]*N; v[i]=1; v[j]=1; vecs.append(v)
                for x in S:
                    v=[0]*N; v[x]=1; vecs.append(v)
                if vecs and hstar_relint(vecs,h):
                    res.append(vecs); break
        if len(cur)>=maxpairs: return
        for idx in range(start,len(allp)):
            c2=cur+[allp[idx]]
            if not metk_ok(c2,m,k): continue
            rec(idx+1,c2)
    rec(0,[])
    res.sort(key=lambda s:-sum(sum(1 for x in v if x)==2 for v in s))
    return res
class Sub:
    def __init__(s,cons,N):
        s.cons,_=rref(F,cons,N) if cons else ([],[]); s.key=tuple(tuple(r) for r in s.cons); s.basis=nullspace(F,s.cons,N)
def run(m,k,maxpairs):
    N=m+1; D=max_divs(m)
    Hb={d:Hbasis(m,d) for d in D}; Hp={d:Hperp_rows(m,d) for d in D}
    S=structures(m,k,maxpairs)
    fam={():Sub([],N)}
    for t,vecs in enumerate(S):
        opts=[]
        for r in range(1,len(vecs)+1):
            for face in itertools.combinations(vecs,r):
                for d in D:
                    if relint_meets(list(face),m,d):
                        opts.append(nullspace(F,list(face)+Hb[d],N))
        new={}
        for key,U in fam.items():
            if any(contained(U.basis,o) for o in opts): new[key]=U; continue
            for o in opts:
                V=Sub(U.cons+o,N)
                if any(contained(V.basis,Hp[d]) for d in D): continue
                new[V.key]=V
        items=list(new.values()); keep={}
        for U in items:
            if not any(U2 is not U and len(U2.basis)>len(U.basis) and contained(U.basis,U2.cons) for U2 in items): keep[U.key]=U
        fam=keep
        if not fam: return True,t+1,len(S),None
    return False,len(S),len(S),fam
if __name__=='__main__':
    m=int(sys.argv[1]); k=int(sys.argv[2]); mp=int(sys.argv[3])
    ok,t,tot,fam=run(m,k,mp)
    print('m',m,'k',k,'structures',tot,('coverer wins after %d'%t) if ok else 'ATTACKER SURVIVES')
    if not ok:
        for U in list(fam.values())[:3]: print(' dim',len(U.basis),[[x if x<P//2 else x-P for x in v] for v in U.basis])
