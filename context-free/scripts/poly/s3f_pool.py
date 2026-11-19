"""S3F: pool of full-rank laminar pair-supported pieces c+NV on NE_M (M=2), generator entries <= E."""
import itertools, numpy as np
def gens(d,E):
    G=[]
    for k in range(d):
        v=[0]*d; v[k]=1; G.append((tuple(v),(k,)))
    for a,b in itertools.combinations(range(d),2):
        for p in range(1,E+1):
            for q in range(1,E+1):
                if np.gcd(p,q)==1:
                    v=[0]*d; v[a]=p; v[b]=q; G.append((tuple(v),(a,b)))
    return G
def cross(s,t):
    if len(s)<2 or len(t)<2: return False
    a,b=s; c,d=t
    return a<c<b<d or c<a<d<b
def families(d,E):
    G=gens(d,E); out=[]
    for S in itertools.combinations(G,d):
        if any(cross(s[1],t[1]) for s,t in itertools.combinations(S,2)): continue
        V=np.array([s[0] for s in S]).T
        if round(abs(np.linalg.det(V)))==0: continue
        out.append(V)
    return out
if __name__=="__main__":
    F=families(4,2); print(len(F))
