"""
Ray-family face criterion for restricted classes (LIN = nested pairs, METk).
Family: y_N = N*w + L*delta.  Coverer structure P1 = (nested) matching M + singletons, pair (i,j) vector w_i e_i + w_j e_j
(this is forced if w in relint cone(P1) and the components are single pairs).
Attacker beats P1 iff exists face P' of P1 and d with (a) relint cone(P') meets V_d, (b) w, delta in V_d + span(P').
Coverer restricted to these P1 => if attacker set empty, the criterion cannot fire (coverer wins).
Arithmetic mod a large prime (search); exact verification separately.
"""
import sys, itertools
from arr2 import Field, rref, nullspace, class_rows, max_divs
from scipy.optimize import linprog
import numpy as np
P=2**61-1; F=Field(P)

def nested_matchings(n, cls='LIN', k=1):
    # all sets of pairwise disjoint pairs; LIN: pairwise nested;  METk: k consecutive intervals [s_r,s_{r+1}) each nested chain
    allp=[(i,j) for i in range(n) for j in range(i+1,n)]
    res=[]
    def nested(a,b): return (a[0]<=b[0] and b[1]<=a[1]) or (b[0]<=a[0] and a[1]<=b[1])
    def rec(start, cur, used):
        res.append(list(cur))
        for idx in range(start,len(allp)):
            p=allp[idx]
            if p[0] in used or p[1] in used: continue
            if cls=='LIN' and not all(nested(p,q) for q in cur): continue
            cur.append(p); used|={p[0],p[1]}
            rec(idx+1,cur,used)
            cur.pop(); used-={p[0],p[1]}
    rec(0,[],set())
    if cls=='LIN': return res
    raise NotImplementedError

def face_feasible(n, w, face, d):
    # exists c>0 with sum c_p p in V_d ; face: list of tuples (pairs/singletons)
    supp=set(x for b in face for x in b)
    for c0 in range(d):
        cl=set(range(c0,n,d))
        if cl & supp and not cl <= supp: return False
    if not supp: return False
    m=len(face)
    # equations: for each class, values equal: value at coordinate i = c_b * w_i
    A=[];
    for c0 in range(d):
        cl=list(range(c0,n,d))
        if not (set(cl)&supp): continue
        for a,b in zip(cl,cl[1:]):
            row=[0.0]*m
            for t,bl in enumerate(face):
                if a in bl: row[t]+=w[a]
                if b in bl: row[t]-=w[b]
            A.append(row)
    # c >= 1 (scale)
    if not A: return True
    r=linprog(np.zeros(m),A_eq=np.array(A),b_eq=np.zeros(len(A)),bounds=[(1,None)]*m,method='highs')
    return r.status==0

def W_perp(n,w,face,d):
    rows=[]
    for b in face:
        r=[0]*n
        for i in b: r[i]=w[i]
        rows.append(r)
    rows+=class_rows(n,d)
    return nullspace(F,rows,n)   # functionals vanishing on span(face)+V_d

def dot(f,v): return sum(a*b for a,b in zip(f,v))%P

def attacker_options(n,w,M,D):
    used=set(x for p in M for x in p)
    P1=[tuple(p) for p in M]+[(k,) for k in range(n) if k not in used]
    opts=[]
    for r in range(1,len(P1)+1):
        for face in itertools.combinations(P1,r):
            for d in D:
                if not face_feasible(n,w,face,d): continue
                Wp=W_perp(n,w,face,d)
                if all(dot(f,w)==0 for f in Wp):
                    opts.append(Wp)
    return opts

class Sub:
    def __init__(self, cons, n):
        self.cons,_=rref(F,cons,n) if cons else ([],[])
        self.key=tuple(tuple(r) for r in self.cons)
        self.basis=nullspace(F,self.cons,n)
def contained(basis,cons): return all(dot(f,v)==0 for f in cons for v in basis)

def run(n,w,cls='LIN'):
    D=max_divs(n)
    # excluded: delta in V_d + R w
    excl=[]
    for d in D:
        rows=class_rows(n,d)
        # V_d + Rw perp: functionals vanishing on V_d and on w
        excl.append(nullspace(F,rows+[list(w)],n))
    fam={():Sub([],n)}
    Ms=nested_matchings(n,cls)
    Ms.sort(key=lambda M:-len(M))
    for t,M in enumerate(Ms):
        opts=attacker_options(n,w,M,D)
        new={}
        for key,U in fam.items():
            if any(contained(U.basis,o) for o in opts): new[key]=U; continue
            for o in opts:
                V=Sub(U.cons+o,n)
                if any(contained(V.basis,e) for e in excl): continue
                new[V.key]=V
        items=list(new.values()); keep={}
        for U in items:
            if not any(U2 is not U and len(U2.basis)>len(U.basis) and contained(U.basis,U2.cons) for U2 in items):
                keep[U.key]=U
        fam=keep
        if not fam: return True,t,fam
    return False,len(Ms),fam

if __name__=='__main__':
    n=int(sys.argv[1]); w=[int(x) for x in sys.argv[2].split(',')]
    ok,t,fam=run(n,w)
    print(n,w,'coverer wins' if ok else 'ATTACKER SURVIVES',t)
    if not ok:
        for U in list(fam.values())[:4]: print(' dim',len(U.basis),[[x if x<P//2 else x-P for x in v] for v in U.basis])
