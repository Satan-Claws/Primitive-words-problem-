"""S4U driver: verify the piece for v=2e0+e10+e15+e20 independently, then run search on S4T's 120 uncovered sparse x."""
import itertools, random, importlib.util, os, numpy as np
d=os.path.dirname(os.path.abspath(__file__))
def load(nm):
    s=importlib.util.spec_from_file_location(nm,os.path.join(d,nm+'.py')); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
U=load('s4u_local'); C=load('s4t_chords'); n=30
def prim(x): return all(any(x[t]!=x[(t+n//p)%n] for t in range(n)) for p in (2,3,5))
def verify(x,res,trials=20000):
    GS,(ext,L)=res; G=list(GS)+ext
    assert not any(U.cross(tuple(a),tuple(b)) for a,b in itertools.combinations(G,2))
    M=np.array([[g.get(t,0) for t in range(n)] for g in G]); assert np.linalg.matrix_rank(M)==n
    for p,Lp in zip((2,3,5),L):
        assert abs(Lp@np.array(x)-1)<1e-5 and all(Lp@r>=-1e-6 for r in M)
    rng=random.Random(1)
    for _ in range(trials):
        y=np.array(x)+sum(rng.choice([0,0,1,2,5])*r for r in M)
        assert prim(list(y))
    return len(G)
if __name__=='__main__':
    v=[0]*n; v[0]=2; v[10]=v[15]=v[20]=1
    r=U.search(v); print('v piece #gens',verify(v,r),'G_S',r[0])
    def sub(L,k): return [s for j in range(k+1) for s in itertools.combinations(range(L),j)]
    def vec(L,s): return [1 if t in s else 0 for t in range(L)]
    unc=[]
    for ks in ((2,1,1),(1,2,1),(1,1,2)):
        for sa in sub(15,ks[0]):
            for sb in sub(10,ks[1]):
                for sc in sub(6,ks[2]):
                    x=C.W30(vec(15,sa),vec(10,sb),vec(6,sc))
                    if not C.inE(x): continue
                    if (C.count(x,'disjoint',stop=True) or len(C.rect_certs(x)))==0: unc.append(tuple(x))
    unc=sorted(set(unc)); print('S4T uncovered (distinct)',len(unc))
    left=[]
    for x in unc:
        r=U.search(list(x))
        if r is None: left.append(x)
        else: verify(list(x),r,trials=500)
    print('still uncovered after local laminar pieces:',len(left),left[:3])
