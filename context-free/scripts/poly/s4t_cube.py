"""S4T: 3-prime 'cube' certificate for n=30 (A=15,B=10,C=6).
Cube at shift i: positions P(v)=i+15a+10b+6c mod 30, v=(a,b,c) in {0,1}^3.
g_p = f_{chi_p} (chi_p has p-th bit 1) vanishes on V_p; certificate: all three g_p != 0.
Checks: (1) coverage of E∩W_30 by sign-certificates (random a+b+c, entries in {0,1,2});
(2) for each sign orthant K_s={y>=0: s_p g_p(y)>=0} in R^8: extreme rays (support sizes);
(3) laminarity: can K_s be covered by cones of <=2-support vectors in K_s whose supports are
non-crossing in the linear order of positions? (sampling + LP over maximal laminar families).
Usage: python3 s4t_cube.py [samples]"""
import sys, itertools, random
from fractions import Fraction
import numpy as np
from scipy.optimize import linprog
n=30; A,B,C=15,10,6; PR={2:A,3:B,5:C}
V=list(itertools.product((0,1),repeat=3))
def per(x,d): return all(x[t]==x[(t+d)%n] for t in range(n))
def inE(x): return not any(per(x,d) for d in (A,B,C))
def pos(i,v): return (i+A*v[0]+B*v[1]+C*v[2])%n
CHI=[c for c in V if any(c)]
def f(x,i,chi): return sum((-1)**(sum(a*b for a,b in zip(v,chi)))*x[pos(i,v)] for v in V)
def sample(rng):
    a=[rng.randint(0,2) for _ in range(A)]; b=[rng.randint(0,2) for _ in range(B)]; c=[rng.randint(0,2) for _ in range(C)]
    return [a[t%A]+b[t%B]+c[t%C] for t in range(n)]
def coverage(N,chis):
    rng=random.Random(1); unc=0; tot=0; ex=None; plies=[]
    for _ in range(N):
        x=sample(rng)
        if not inE(x): continue
        tot+=1; k=0
        for i in range(n):
            for ch in chis:
                if all(f(x,i,c)!=0 for c in ch): k+=1
        plies.append(k)
        if k==0: unc+=1; ex=ex or x
    return tot,unc,ex,(min(plies) if plies else None),(max(plies) if plies else None)
def rays(G):  # extreme rays of {y>=0, G y>=0} in R^8
    M=np.vstack([np.eye(8),G]); out=set()
    for S in itertools.combinations(range(len(M)),7):
        sub=M[list(S)]
        if np.linalg.matrix_rank(sub)<7: continue
        _,_,vt=np.linalg.svd(sub); r=vt[-1]
        for s in (r,-r):
            if (M@s>=-1e-9).all():
                s=s/np.abs(s).max(); out.add(tuple(np.round(s,6)))
    return [np.array(r) for r in out]
def cross(e1,e2,order):
    if len(e1)<2 or len(e2)<2 or set(e1)&set(e2): return False
    a,b=sorted(order[t] for t in e1); c,d=sorted(order[t] for t in e2)
    return a<c<b<d or c<a<d<b
def analyse(i,chi3,signs,Nsamp=400,rng=None):
    G=np.array([[s*(-1)**sum(a*b for a,b in zip(v,c)) for v in V] for c,s in zip(chi3,signs)],float)
    R=rays(G); sup=sorted(int((np.abs(r)>1e-9).sum()) for r in R)
    order={k:pos(i,v) for k,v in enumerate(V)}
    good=[r for r in R if (np.abs(r)>1e-9).sum()<=2]
    # all <=2-support rays of K (extreme rays of each 2-face) already among cone's 2-support members:
    cand=list(good)
    for p,q in itertools.combinations(range(8),2):
        for (a,b) in ((1,0),(0,1)):
            pass
        sub=np.zeros((0,8))
        Gp=G[:,[p,q]]
        # rays of {(s,t)>=0, Gp (s,t)>=0}
        M=np.vstack([np.eye(2),Gp])
        for row in M:
            r=np.array([-row[1],row[0]])
            for s in (r,-r):
                if (M@s>=-1e-9).all() and np.abs(s).max()>0:
                    y=np.zeros(8); y[p],y[q]=s; y/=np.abs(y).max(); cand.append(y)
    U={tuple(np.round(c,6)) for c in cand}; cand=[np.array(c) for c in U]
    sup_of=[tuple(k for k in range(8) if abs(c[k])>1e-9) for c in cand]
    m=len(cand); X=[[cross(sup_of[a],sup_of[b],order) for b in range(m)] for a in range(m)]
    # maximal laminar families via Bron-Kerbosch on compatibility graph
    comp={a:{b for b in range(m) if b!=a and not X[a][b]} for a in range(m)}
    fams=[]
    def bk(Rs,P,Xs):
        if not P and not Xs: fams.append(Rs); return
        for v in list(P):
            bk(Rs|{v},P&comp[v],Xs&comp[v]); P=P-{v}; Xs=Xs|{v}
    bk(set(),set(range(m)),set())
    # sample interior points of K: random y>=0 with G y>0 (rejection)
    rng=rng or np.random.default_rng(0); fail=0; tried=0; bad=None
    while tried<Nsamp:
        y=rng.exponential(size=8)
        if not (G@y>1e-6).all(): continue
        tried+=1; ok=False
        for F in fams:
            Mx=np.array([cand[k] for k in F]).T
            res=linprog(np.zeros(len(F)),A_eq=Mx,b_eq=y,bounds=(0,None),method='highs')
            if res.status==0: ok=True; break
        if not ok: fail+=1; bad=bad if bad is not None else y
    return sup,len(cand),len(fams),tried,fail,bad
if __name__=='__main__':
    N=int(sys.argv[1]) if len(sys.argv)>1 else 3000
    axes=[[(1,0,0),(0,1,0),(0,0,1)]]
    allch=[ch for ch in itertools.product(*[[c for c in CHI if c[k]] for k in range(3)])]
    print('coverage axes-only:',coverage(N,axes))
    print('coverage all chi-triples:',coverage(N//3,allch))
    for i in (0,):
        for chi3 in [((1,0,0),(0,1,0),(0,0,1)),((1,1,1),(1,1,1),(1,1,1)),((1,1,0),(0,1,1),(1,0,1))]:
            for s in itertools.product((1,-1),repeat=3):
                print('i',i,'chi',chi3,'signs',s,analyse(i,chi3,s,Nsamp=150)[:5])
