"""r20: substitution-stability profile of uniform G^- words (MC).
Substitution = shuffle the letters of a block (preserves D, so a word of L_R stays in L_R ⊆ Q).
Block at fold depth delta (distance to the left end), length ell; 'two-sided' = blocks [0,ell) and [n-ell,n)
(outer tokens of a spanning linear spine). Prints P(substituted word still in G^-)."""
import numpy as np
rng=np.random.default_rng(1); n=1001; h=n//2
def inGm(W):  # W: (m,n) of +-1
    P=np.concatenate([np.zeros((W.shape[0],1),int),np.cumsum(W,1)],1)
    k=np.arange(1,h+1); d=P[:,k]+P[:,n-k]-P[:,[n]]
    return (d<0).all(1)
S=[]
while sum(len(s) for s in S)<3000:
    W=rng.choice([-1,1],size=(20000,n)); S.append(W[inGm(W)])
S=np.concatenate(S)[:3000]
def shuf(W,a,b):
    W=W.copy(); idx=np.argsort(rng.random((W.shape[0],b-a)),1); W[:,a:b]=np.take_along_axis(W[:,a:b],idx,1); return W
print(f"n={n}, {len(S)} uniform G^- samples")
for ell in (4,16,64,256):
    row=[]
    for delta in (0,8,64,250):
        if delta+ell<=n: row.append(f"d={delta}:{inGm(shuf(S,delta,delta+ell)).mean():.3f}")
    two=inGm(shuf(shuf(S,0,ell),n-ell,n)).mean()
    print(f"ell={ell:4d} one-sided "+" ".join(row)+f" | two-sided outer:{two:.3f}  ell^-1/2={ell**-.5:.3f}")
