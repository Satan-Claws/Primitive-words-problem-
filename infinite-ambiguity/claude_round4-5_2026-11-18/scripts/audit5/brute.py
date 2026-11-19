# audit5: independent brute force for T(E'), T^2, T^3, G; and literal construction crosscheck
import sys, itertools
def prim(w):
    n=len(w)
    for d in range(1,n):
        if n%d==0 and w[:d]*(n//d)==w: return False
    return n>0
def delta(w): return w.count('a')-w.count('b')
def sw(w): return w.translate(str.maketrans('ab','ba'))
def canon_rots(w):
    # all rotations ending at strict max (w with delta>0)
    n=len(w); D=delta(w); out=[]
    for i in range(n):
        r=w[i:]+w[:i]; s=0; ok=True
        for t in range(n-1):
            s+= 1 if r[t]=='a' else -1
            if s>=D: ok=False;break
        if ok: out.append(r)
    return out
def pieces(r):
    s=0; mx=0; cur=''; out=[]
    for c in r:
        cur+=c; s+= 1 if c=='a' else -1
        if s>mx: mx=s; out.append(cur); cur=''
    assert cur=='' ; return out
def phi(r): return ''.join('a' if p=='a' else 'b' for p in pieces(r))
def gtype(p):
    if p=='a': return 'A'
    return 'B' if p[1]=='a' else 'C'
def isrot(u,v): return len(u)==len(v) and u in v+v
def decode(w,checkall=False):
    """return Phi of a canonical rotation (after swap if delta<0), or None if delta==0"""
    D=delta(w)
    if D==0: return None
    if D<0: w=sw(w)
    cr=canon_rots(w) if checkall else None
    if checkall:
        assert len(cr)==abs(D), (w,cr)
        ph=[phi(r) for r in cr]
        assert all(isrot(ph[0],x) for x in ph), (w,ph)
        return ph[0]
    # fast: rotate to start after first global max position
    n=len(w); s=0; best=-10**9; pos=0
    for t,c in enumerate(w):
        s+= 1 if c=='a' else -1
        if s>best: best=s; pos=t+1
    r=w[pos:]+w[:pos]
    return phi(r)
def inE(w): return abs(delta(w))==1
def inT(w,k):
    if k==0: return inE(w)
    v=decode(w)
    return v is not None and inT(v,k-1)
def inG(w):
    D=delta(w)
    if D==0: return False
    if D<0: w=sw(w)
    s=0; best=-10**9; pos=0
    for t,c in enumerate(w):
        s+= 1 if c=='a' else -1
        if s>best: best=s; pos=t+1
    r=w[pos:]+w[:pos]
    g={'A':1,'B':-2,'C':0}
    return abs(sum(g[gtype(p)] for p in pieces(r)))==1
if __name__=='__main__':
    N=int(sys.argv[1])
    import random
    # rotation-invariance check on random words
    random.seed(1)
    for _ in range(3000):
        n=random.randint(1,30); w=''.join(random.choice('ab') for _ in range(n))
        if delta(w)!=0: decode(w,checkall=True)
    print("canonical-rotation count = |D| and Phi rotation-invariant: OK on 3000 random words")
    for n in range(1,N+1):
        cnt=[0]*4; bad=[0]*4; cG=0; bG=0
        for t in itertools.product('ab',repeat=n):
            w=''.join(t); p=None
            for k in range(4):
                if inT(w,k):
                    cnt[k]+=1
                    if p is None: p=prim(w)
                    if not p: bad[k]+=1
            if inG(w):
                cG+=1
                if p is None: p=prim(w)
                if not p: bG+=1
        print(n,[c/2**n for c in cnt],'nonprim',bad,'G',cG/2**n,bG,flush=True)
