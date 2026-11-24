# Checks (exhaustive n<=16): (1) L_A (split definition of r6 Lemma SA) == P ∩ {h<=0 on [0,ceil(n/2)]};
# (2) every class with an L_B rotation has an L_A rotation (Rot L_A == Rot L_B), and L_B ⊆ Q.
from itertools import product
def walk(w):
    h=[0]
    for c in w: h.append(h[-1]+(1 if c=='a' else -1))
    return h
def inLA_split(w):
    n=len(w); h=walk(w); H=h[n]
    for s in range(0,n+1):
        if any(h[j]>0 for j in range(s+1)): break
        if h[s]!=0 or s<n-s: continue
        y=w[s:]
        if y and all(walk(y[k:])[-1]>0 for k in range(len(y))): return True
    return False
def inP(w):
    return all(walk(w[k:])[-1]>0 for k in range(len(w)))
def inLB(w):
    n=len(w); h=walk(w); return h[n]>=1 and all(h[j]<=0 for j in range((n+1)//2+1))
def prim(w):
    n=len(w); return all(w!=w[d:]+w[:d] for d in range(1,n) if n%d==0)
bad=0
for n in range(1,17):
    for t in product('ab',repeat=n):
        w=''.join(t); a=inLA_split(w); b=inP(w) and inLB(w)
        if a!=b: bad+=1
        if inLB(w) and not prim(w): bad+=1000
        if inLB(w):
            if not any(inLA_split(w[i:]+w[:i]) for i in range(n)): bad+=10**6
print("mismatches/violations:",bad)
