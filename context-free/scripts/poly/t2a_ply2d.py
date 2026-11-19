"""T2a: min over covers of prod_k (Z^2\\0) by products of open half-planes of the max ply.
Factor normals at angles a*pi/m (a<2m); points at angles p*pi/(2m) (all faces of the arrangement).
Exact for configurations with <= m distinct lines per factor (any cyclic type is realizable there).
Usage: python3 t2a_ply2d.py N m"""
import sys, itertools, numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import lil_matrix
N=int(sys.argv[1]); m=int(sys.argv[2])
normals=range(2*m); pts=range(4*m)
inside=lambda a,p: min((p-2*a)%(4*m),(2*a-p)%(4*m))<m
pieces=list(itertools.product(normals,repeat=N)); P=list(itertools.product(pts,repeat=N))
nv=len(pieces)+1
A=lil_matrix((2*len(P),nv))
for i,pt in enumerate(P):
    for j,pc in enumerate(pieces):
        if all(inside(a,p) for a,p in zip(pc,pt)):
            A[i,j]=1; A[len(P)+i,j]=1
    A[len(P)+i,nv-1]=-1
lb=np.r_[np.ones(len(P)),-np.inf*np.ones(len(P))]; ub=np.r_[np.inf*np.ones(len(P)),np.zeros(len(P))]
c=np.zeros(nv); c[-1]=1; c[:-1]=1e-3   # min ply, tie-break few pieces
res=milp(c,constraints=LinearConstraint(A.tocsr(),lb,ub),integrality=np.ones(nv),bounds=Bounds(0,np.r_[np.ones(nv-1),100]),options={"time_limit":600})
x=np.round(res.x).astype(int); sel=[pieces[j] for j in range(nv-1) if x[j]]
print("N",N,"m",m,"status",res.status,"minmaxply",x[-1],"pieces",len(sel)); print(sel)
