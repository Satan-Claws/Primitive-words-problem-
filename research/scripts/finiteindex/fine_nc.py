"""
Near-constant criterion in FINE coordinates (blocks split into parts = full preimage, legitimate by
inverse homomorphism + intersection with a regular set).
Coarse slice: (a b^*)^n  [coordinates = b-blocks], optional seam: b^* (a b^*)^n  (block 0 split across the ends).
Fine coordinates: each coarse block j is split into parts[j] consecutive coordinates.
Non-primitive subspaces: H_d = coarse^{-1}(V_d), d in D(n).
Family: N*1 + L*delta (fine all-ones direction; coarse image is (parts_j), must lie in V_1 => all parts equal).
Coverer structures: disjoint ratio-1 pairs + singletons, class LIN or METk (pairs non-crossing, laminar forest of paths, <=k roots).
Attacker set = {delta : for all structures exists d: delta in span(P)+H_d} minus union H_d.
"""
import sys, itertools
from arr2 import Field, rref, nullspace, max_divs
P=2**61-1; F=Field(P)
def dot(f,v): return sum(a*b for a,b in zip(f,v))%P

def setup(n, parts):
    coords=[]  # fine index -> coarse block
    for j in range(n):
        coords += [j]*parts[j]
    return coords

def Hd_basis(coords, n, d):
    N=len(coords); B=[]
    first={}
    for i,j in enumerate(coords):
        if j not in first: first[j]=i
        else:
            v=[0]*N; v[i]=1; v[first[j]]=P-1; B.append(v)
    for c in range(d):
        v=[0]*N
        for j in range(c,n,d): v[first[j]]=1
        B.append(v)
    return B

def structures(N, cls, k):
    allp=[(i,j) for i in range(N) for j in range(i+1,N)]
    out=[]
    def valid(ps):
        # non-crossing, each pair at most one child, roots<=k (LIN: k=1)
        for a,b in itertools.combinations(ps,2):
            (i,j),(u,v)=sorted([a,b])
            if i<u<j<v: return False
        # children
        roots=0
        for p in ps:
            par=[q for q in ps if q!=p and q[0]<p[0] and p[1]<q[1]]
            if not par: roots+=1
        for q in ps:
            ch=[p for p in ps if p!=q and q[0]<p[0] and p[1]<q[1] and not any(r!=p and r!=q and q[0]<r[0] and r[1]<q[1] and r[0]<p[0] and p[1]<r[1] for r in ps)]
            if len(ch)>1: return False
        return roots<=k
    def rec(start,cur,used):
        out.append(list(cur))
        for idx in range(start,len(allp)):
            p=allp[idx]
            if p[0] in used or p[1] in used: continue
            c2=cur+[p]
            if not valid(c2): continue
            used|={p[0],p[1]}; rec(idx+1,c2,used); used-={p[0],p[1]}
    rec(0,[],set())
    res=[]
    for ps in out:
        u=set(x for p in ps for x in p)
        res.append(ps+[(x,) for x in range(N) if x not in u])
    res.sort(key=lambda s:-sum(len(b)==2 for b in s))
    return res

class Sub:
    def __init__(s,cons,N):
        s.cons,_=rref(F,cons,N) if cons else ([],[]); s.key=tuple(tuple(r) for r in s.cons); s.basis=nullspace(F,s.cons,N)
def contained(basis,cons): return all(dot(f,v)==0 for f in cons for v in basis)

def run(n, parts, cls='LIN', k=1, verbose=False):
    coords=setup(n,parts); N=len(coords); D=max_divs(n)
    Hb={d:Hd_basis(coords,n,d) for d in D}
    Hperp={d:nullspace(F,Hb[d],N) for d in D}
    S=structures(N,cls,k)
    fam={():Sub([],N)}
    for t,st in enumerate(S):
        rows=[]
        for b in st:
            v=[0]*N
            for i in b: v[i]=1
            rows.append(v)
        opts=[nullspace(F,rows+Hb[d],N) for d in D]
        new={}
        for key,U in fam.items():
            if any(contained(U.basis,o) for o in opts): new[key]=U; continue
            for o in opts:
                V=Sub(U.cons+o,N)
                if any(contained(V.basis,Hperp[d]) for d in D): continue
                new[V.key]=V
        items=list(new.values()); keep={}
        for U in items:
            if not any(U2 is not U and len(U2.basis)>len(U.basis) and contained(U.basis,U2.cons) for U2 in items): keep[U.key]=U
        fam=keep
        if not fam: return True,t+1,len(S),None
    return False,len(S),len(S),fam

if __name__=='__main__':
    n=int(sys.argv[1]); parts=[int(x) for x in sys.argv[2].split(',')]; k=int(sys.argv[3]) if len(sys.argv)>3 else 1
    ok,t,tot,fam=run(n,parts,'MET',k)
    print('n',n,'parts',parts,'k',k,'structures',tot,'coverer wins after %d'%t if ok else 'ATTACKER SURVIVES')
    if not ok:
        for U in list(fam.values())[:3]: print(' dim',len(U.basis),[[x if x<P//2 else x-P for x in v] for v in U.basis][:4])
