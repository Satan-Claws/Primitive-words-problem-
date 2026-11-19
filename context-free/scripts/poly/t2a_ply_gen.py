"""T2a: upper bound for min max-ply of covers of prod_k (Z^{d_k}\\0) by products of open half-spaces,
normals restricted to a fixed finite set per factor (so result = UPPER bound on the true minimum).
Points: one representative per face (sign vector) of each factor arrangement, from integer pts in [-B,B]^d.
Usage: python3 t2a_ply_gen.py d1,d2,...   (normal sets hard-coded below)"""
import sys, itertools, numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import csr_matrix
dims=[int(a) for a in sys.argv[1].split(',')]
def normals(d):
    base=[tuple(int(i==j) for j in range(d)) for i in range(d)]
    base+= [tuple([1]*d)]
    base+= [tuple(1 if j==i else (-1 if j==(i+1)%d else 0) for j in range(d)) for i in range(d)] if d>2 else []
    out=[];[out.extend([v,tuple(-x for x in v)]) for v in base]; return np.array(out)
def faces(d,V,B=4):
    seen={}
    for p in itertools.product(range(-B,B+1),repeat=d):
        if any(p): seen.setdefault(tuple(np.sign(V@np.array(p))),p)
    return np.array(list(seen.keys()))   # sign vectors
Vs=[normals(d) for d in dims]; Fs=[faces(d,V) for d,V in zip(dims,Vs)]
print("normals",[len(V) for V in Vs],"faces",[len(F) for F in Fs])
pieces=list(itertools.product(*[range(len(V)) for V in Vs])); pts=list(itertools.product(*[range(len(F)) for F in Fs]))
rows=[];cols=[]
for i,pt in enumerate(pts):
    for j,pc in enumerate(pieces):
        if all(Fs[k][pt[k]][pc[k]]>0 for k in range(len(dims))): rows.append(i);cols.append(j)
nv=len(pieces)+1;P=len(pts)
A1=csr_matrix((np.ones(len(rows)),(rows,cols)),shape=(P,nv))
A2=csr_matrix((np.r_[np.ones(len(rows)),-np.ones(P)],(np.r_[rows,range(P)],np.r_[cols,[nv-1]*P])),shape=(P,nv))
from scipy.sparse import vstack
A=vstack([A1,A2]);lb=np.r_[np.ones(P),-np.inf*np.ones(P)];ub=np.r_[np.inf*np.ones(P),np.zeros(P)]
c=np.zeros(nv);c[-1]=1;c[:-1]=1e-3
res=milp(c,constraints=LinearConstraint(A,lb,ub),integrality=np.ones(nv),bounds=Bounds(0,np.r_[np.ones(nv-1),1000]),options={"time_limit":1500})
x=np.round(res.x).astype(int)
print("dims",dims,"status",res.status,"maxply<=",x[-1],"pieces",int(x[:-1].sum()),"prod d",np.prod(dims))
