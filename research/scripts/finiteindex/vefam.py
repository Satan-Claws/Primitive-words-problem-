"""
Full-dimensional V_e family criterion (bounded L8) WITH the face condition, for class LIN (pairwise nested pair supports).
Coverer P1: set of 2-sparse nonneg integer vectors (entries <= R), LIN-nested supports, with
  (i) V_e subset span(P1); (ii) some strictly positive combination of ALL of P1 lies in V_e.
Attacker beats P1 iff exists face P' (subset) and d in D(n): relint cone(P') meets V_d, V_e subset V_d+span(P'), delta in V_d+span(P').
We enumerate P1 up to size S and compute the attacker set (union of subspaces) for delta.
"""
import sys, itertools
from fractions import Fraction
from arr2 import Field, rref, nullspace, class_rows, max_divs
from scipy.optimize import linprog
import numpy as np
P=2**61-1; F=Field(P)
def dot(f,v): return sum(a*b for a,b in zip(f,v))%P
def rank(rows,n): return len(rref(F,rows,n)[0]) if rows else 0
def Vbasis(n,d):
    return [[1 if i%d==c else 0 for i in range(n)] for c in range(d)]
def nested(a,b): return (a[0]<=b[0] and b[1]<=a[1]) or (b[0]<=a[0] and a[1]<=b[1])
def supp(v): return tuple(i for i,x in enumerate(v) if x)
def relint_meets(vecs,n,d):
    # exists c>0 (>=1) with sum c_j v_j in V_d
    m=len(vecs); A=[]
    for c0 in range(d):
        cl=list(range(c0,n,d))
        for a,b in zip(cl,cl[1:]):
            A.append([v[a]-v[b] for v in vecs])
    r=linprog(np.zeros(m),A_eq=np.array(A,dtype=float),b_eq=np.zeros(len(A)),bounds=[(1,None)]*m,method='highs')
    return r.status==0
def perp(rows,n): return nullspace(F,rows,n)
def contained_sub(Abasis,Bperp): return all(dot(f,v)==0 for f in Bperp for v in Abasis)

def gen_vectors(n,R):
    vs=[]
    for i in range(n):
        v=[0]*n; v[i]=1; vs.append(v)
    for i in range(n):
        for j in range(i+1,n):
            for a in range(1,R+1):
                for b in range(1,R+1):
                    from math import gcd
                    if gcd(a,b)!=1: continue
                    v=[0]*n; v[i]=a; v[j]=b; vs.append(v)
    return vs

def ok_class(vs):
    ps=[supp(v) for v in vs if len(supp(v))==2]
    return all(nested(a,b) for a,b in itertools.combinations(ps,2))

def attacker_W(vs,n,e,D):
    Ve=Vbasis(n,e); out=[]
    for r in range(1,len(vs)+1):
        for face in itertools.combinations(vs,r):
            for d in D:
                if not relint_meets(list(face),n,d): continue
                Wp=perp(list(face)+Vbasis(n,d),n)   # functionals vanishing on V_d+span(face)
                if not contained_sub(Ve,Wp): continue
                out.append(Wp)
    return out

def enum_P1(n,e,R,S):
    vs=gen_vectors(n,R); Ve=Vbasis(n,e)
    res=[]
    def rec(start,cur):
        if cur:
            rk=rank(cur,n)
            if rank(cur+Ve,n)==rk and relint_meets(cur,n,e): res.append(list(cur)); return  # minimal-ish: stop extending
        if len(cur)>=S: return
        for i in range(start,len(vs)):
            c2=cur+[vs[i]]
            if not ok_class(c2): continue
            if rank(c2,n)<len(c2): continue   # independent sets suffice? (keep independent for size)
            rec(i+1,c2)
    rec(0,[])
    return res

if __name__=='__main__':
    n=int(sys.argv[1]); e=int(sys.argv[2]); R=int(sys.argv[3]); S=int(sys.argv[4])
    D=max_divs(n)
    P1s=enum_P1(n,e,R,S)
    print('P1 candidates',len(P1s),flush=True)
    # attacker set: delta must be outside V_e (family primitive wrt divisors d with e|d) -- excl = V_d for e|d, plus V_d+V_e for others
    excl=[]
    for d in D:
        excl.append(perp(Vbasis(n,d)+Vbasis(n,e),n))
    class Sub:
        def __init__(s,cons):
            s.cons,_=rref(F,cons,n) if cons else ([],[]); s.key=tuple(tuple(r) for r in s.cons); s.basis=nullspace(F,s.cons,n)
    fam={():Sub([])}
    for t,P1 in enumerate(P1s):
        opts=attacker_W(P1,n,e,D)
        new={}
        for k,U in fam.items():
            if any(contained_sub(U.basis,o) for o in opts): new[k]=U; continue
            for o in opts:
                V=Sub(U.cons+o)
                if any(contained_sub(V.basis,x) for x in excl): continue
                new[V.key]=V
        items=list(new.values()); keep={}
        for U in items:
            if not any(U2 is not U and len(U2.basis)>len(U.basis) and contained_sub(U.basis,U2.cons) for U2 in items): keep[U.key]=U
        fam=keep
        if not fam:
            print('coverer wins after',t+1,'P1; last P1',P1); break
    else:
        print('ATTACKER SURVIVES; family dims',[len(U.basis) for U in fam.values()][:10])
        for U in list(fam.values())[:3]: print([[x if x<P//2 else x-P for x in v] for v in U.basis])
