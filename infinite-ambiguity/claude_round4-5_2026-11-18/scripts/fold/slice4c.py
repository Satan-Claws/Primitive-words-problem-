"""U ∩ (a*b*)^K slices, sampled: compare U, interval rule, and H = {min(|w|_a,|w|_b) >= min T(n)}.
Records where H\\U points sit (directions)."""
import numpy as np, sys
from lines import targets
def mvals(w):
    n=len(w); W=np.array(w,float); F=np.fft.rfft(W)
    conv=np.rint(np.fft.irfft(F*F,n=n)).astype(int); return int(W.sum())-conv
rng=np.random.default_rng(5); K=int(sys.argv[1]); 
for n in (60,121,240,481,960):
    T=targets(n); c=dict(H=0,U=0,IV=0,HnotU=0,tot=0); ex=[]
    for _ in range(3000):
        cuts=np.sort(rng.choice(np.arange(1,n),2*K-1,replace=False)); parts=np.diff(np.concatenate([[0],cuts,[n]]))
        w=[];  [w.extend([s%2]*p) for s,p in enumerate(parts)]
        M=mvals(w); s=set(M.tolist()); na=w.count(0); nb=n-na
        u=any(t in s for t in T); iv=any(M.min()<=t<=M.max() for t in T); h=min(na,nb)>=min(T)
        c['tot']+=1;c['U']+=u;c['IV']+=iv;c['H']+=h;c['HnotU']+=(h and not u)
        if h and not u and len(ex)<3: ex.append((list(parts),min(na,nb)/n,sorted(s)[:3],sorted(s)[-3:]))
    print(n,c,ex,flush=True)
