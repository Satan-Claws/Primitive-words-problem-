"""r9_selfsim_cover.py -- coverage of the truncation certificates L_k inside P∩Q (class-weighted),
and the instance length m = |trunc_1(w)| = H + R (blocks + top-level primes).
Exhaustive for n<=NE (P words enumerated directly), Monte Carlo for listed n.
Membership in L_k is invariant under the H block rotations, so 'miss' is a property of the conjugacy class."""
import random, sys, itertools
from r9_selfsim_exact import prim, blocks, tr, inP

def to_P(w):
    # cycle lemma: start right after the first argmax of the prefix walk (a=+1)
    h=0;best=0;arg=0
    for i,c in enumerate(w):
        h+= 1 if c=='a' else -1
        if h>best: best=h;arg=i+1
    return w[arg:]+w[:arg]

def stats(w,K=(1,2,3)):
    B=blocks(w)
    return [prim([tr(D,k) for D in B]) for k in K], len(B), len(B)+sum(len(tr(D,1)) for D in B)

def exhaustive(n):
    miss=[0,0,0]; tot=0
    for t in itertools.product('ab',repeat=n):
        w=''.join(t)
        if not inP(w) or not prim(w): continue
        s,H,m=stats(w); wt=1.0/H; tot+=wt
        for k in range(3):
            if not s[k]: miss[k]+=wt
    return [x/tot for x in miss]

def mc(n,T,seed=1):
    rnd=random.Random(seed); miss=[0,0,0]; tot=0; Hs=0; ms=0
    while tot<T:
        w=''.join(rnd.choice('ab') for _ in range(n))
        H=w.count('a')-w.count('b')
        if H==0: continue
        if H<0: w=w.translate(str.maketrans('ab','ba'))
        w=to_P(w)
        if not prim(w): continue
        s,H,m=stats(w); tot+=1; Hs+=H; ms+=m
        for k in range(3):
            if not s[k]: miss[k]+=1
    return [x/T for x in miss], Hs/T, ms/T

if __name__=='__main__':
    NE=int(sys.argv[1]) if len(sys.argv)>1 else 18
    for n in range(8,NE+1,2 if NE>16 else 1):
        print('exh n=%d miss L1,L2,L3 = %s'%(n,['%.4f'%x for x in exhaustive(n)]),flush=True)
    for n in (64,256,1024,4096):
        mi,H,m=mc(n,2000)
        print('mc n=%d miss=%s  E[H]=%.1f E[m]=%.1f  m/sqrt(n)=%.2f'%(n,['%.4f'%x for x in mi],H,m,m/n**0.5),flush=True)
