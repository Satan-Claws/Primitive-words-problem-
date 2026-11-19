"""S4U: local laminar piece search at sparse x in W_30 (n=30).
Find laminar G = G_S (pair-vectors on S=supp x, entries<=2, x in int cone(G_S) within R^S)
  + one extension h_j per j notin S (e_j, e_j+a e_s, 2e_j+e_s), all supports pairwise non-crossing
  in linear order 0..29, and L_p in V_p^perp (p=2,3,5) with L_p(x)=1, L_p(g)>=0 on all chosen g.
Then cone(G) contains an orthant-neighbourhood of x and finitely many translates c+NG (L_p(c)>0) cover it
inside E (separating functional => avoids V_p). MILP via scipy."""
import itertools, sys, numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds, linprog
n=30; PER={2:15,3:10,5:6}
def cross(a,b):
    if len(a)<2 or len(b)<2: return False
    i,j=sorted(a); k,l=sorted(b); return i<k<j<l or k<i<l<j
def interior(x,G,S):
    A=np.array([[g.get(s,0) for g in G] for s in S],float)
    if np.linalg.matrix_rank(A)<len(S): return False
    m=len(G); c=np.zeros(m+1); c[-1]=-1
    Aeq=np.hstack([A,np.zeros((len(S),1))]); beq=np.array([x[s] for s in S],float)
    Aub=np.hstack([-np.eye(m),np.ones((m,1))]); r=linprog(c,A_ub=Aub,b_ub=np.zeros(m),A_eq=Aeq,b_eq=beq,bounds=[(0,None)]*m+[(0,1)])
    return r.status==0 and -r.fun>1e-7
def solve(x,GS,S,M=50):
    # variables: L_p (3*30, bounded), binaries y_{j,h}
    ext=[]
    for j in range(n):
        if j in S: continue
        opts=[{j:1}]+[{j:a,s:b} for s in S for (a,b) in ((1,1),(1,2),(2,1))]
        opts=[h for h in opts if not any(cross(tuple(h),tuple(g)) for g in GS)]
        ext.append((j,opts))
    nL=3*n; Y=[(j,h) for j,o in ext for h in o]; nv=nL+len(Y)
    rows=[];lo=[];hi=[]
    def row(): return np.zeros(nv)
    for pi,p in enumerate((2,3,5)):
        d=PER[p]
        for r0 in range(d):  # L in V_p^perp: orbit sums zero
            R=row(); [R.__setitem__(pi*n+t,1) for t in range(r0,n,d)]; rows.append(R);lo.append(0);hi.append(0)
        R=row(); [R.__setitem__(pi*n+t,x[t]) for t in range(n)]; rows.append(R);lo.append(1);hi.append(1)
        for g in GS:
            R=row(); [R.__setitem__(pi*n+t,a) for t,a in g.items()]; rows.append(R);lo.append(0);hi.append(np.inf)
        for k,(j,h) in enumerate(Y):
            R=row(); [R.__setitem__(pi*n+t,a) for t,a in h.items()]; R[nL+k]=-3*M  # L(h) >= -3M(1-y)
            rows.append(R);lo.append(-3*M);hi.append(np.inf)
    for j,o in ext:
        R=row()
        for k,(jj,h) in enumerate(Y):
            if jj==j: R[nL+k]=1
        rows.append(R);lo.append(1);hi.append(1)
    for a in range(len(Y)):
        for b in range(a+1,len(Y)):
            if cross(tuple(Y[a][1]),tuple(Y[b][1])):
                R=row();R[nL+a]=1;R[nL+b]=1;rows.append(R);lo.append(-np.inf);hi.append(1)
    integ=np.r_[np.zeros(nL),np.ones(len(Y))]
    b=Bounds(np.r_[-M*np.ones(nL),np.zeros(len(Y))],np.r_[M*np.ones(nL),np.ones(len(Y))])
    r=milp(np.zeros(nv),constraints=LinearConstraint(np.array(rows),lo,hi),integrality=integ,bounds=b)
    if r.status!=0: return None
    z=r.x; ch=[Y[k][1] for k in range(len(Y)) if z[nL+k]>.5]
    return ch,[z[pi*n:(pi+1)*n] for pi in range(3)]
def candidates(S):
    pool=[{s:a} for s in S for a in (1,2)]+[{s:a,t:b} for s,t in itertools.combinations(S,2) for a in (1,2) for b in (1,2)]
    return pool
def search(x,maxg=6):
    S=[t for t in range(n) if x[t]]; pool=candidates(S)
    for k in range(len(S),maxg+1):
        for GS in itertools.combinations(pool,k):
            if any(cross(tuple(a),tuple(b)) for a,b in itertools.combinations(GS,2)): continue
            if not interior(x,GS,S): continue
            res=solve(x,GS,S)
            if res: return GS,res
    return None
if __name__=='__main__':
    x=[0]*n; x[0]=2; x[10]=x[15]=x[20]=1
    out=search(x); print(out)
