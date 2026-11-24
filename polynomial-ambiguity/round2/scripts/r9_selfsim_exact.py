"""r9_selfsim_exact.py -- exhaustive checks of the exact transfers used in r9_selfsim.md.
(a) c(a)=ba, c(b)=bba:  c(u) in Q <=> u in Q, and Q ∩ (ba+bba)^* = c(Q)            (|u|<=L)
(b) mu(a)=ab, mu(b)=abb, mu(x)=abbb: mu(u) in Q <=> u in Q_3                           (|u|<=L3)
(c) slice: Q ∩ (b*a)^+  <=> run-length sequence primitive                               (n<=N)
(d) P ∩ {a,ba}^* = {a,ba}^* a ; and t in (b* a)^+ : t in Q <=> sigma_min(t) in L_k for all k (x=b)
(e) L_k ⊆ L_{k+1} ⊆ P∩Q, union = P∩Q at height<=k ; sigma-decoding unique (count parses)   (n<=N)
"""
import itertools, sys
from collections import Counter

def prim(s):
    n=len(s)
    if n==0: return False
    # smallest period via failure function
    f=[0]*n; k=0
    for i in range(1,n):
        while k and s[i]!=s[k]: k=f[k-1]
        if s[i]==s[k]: k+=1
        f[i]=k
    p=n-f[-1]
    return not (n%p==0 and p<n)

def inP(w):
    h=0
    for c in reversed(w):
        h+= 1 if c=='a' else -1
        if h<=0: return False
    return len(w)>0

def blocks(w):
    """P word -> list of D_i (b-first Dyck, b=open a=close)."""
    out=[];d=0;st=0
    for i,c in enumerate(w):
        d+= 1 if c=='b' else -1
        if d==-1:
            out.append(w[st:i]); st=i+1; d=0
    assert st==len(w)
    return out

def primes(D):
    out=[];d=0;st=0
    for i,c in enumerate(D):
        d+= 1 if c=='b' else -1
        if d==0: out.append(D[st:i+1]); st=i+1
    return out

def tr(D,k):
    """depth-k truncation of a Dyck word D: G_0=x^*, G_j=(b G_{j-1} a)^*"""
    if k==1: return 'x'*len(primes(D))
    return ''.join('b'+tr(p[1:-1],k-1)+'a' for p in primes(D))

def trunc(w,k):
    return ''.join(tr(D,k)+'a' for D in blocks(w))

def inLk(w,k):
    """w in P assumed; truncated block sequence primitive"""
    return prim([tr(D,k) for D in blocks(w)])

def words(n,al='ab'):
    for t in itertools.product(al,repeat=n): yield ''.join(t)

def main(L=14,L3=9,N=16):
    bad=Counter()
    c={'a':'ba','b':'bba'}
    for n in range(1,L+1):
        img=set()
        for u in words(n):
            cu=''.join(c[x] for x in u); img.add(cu)
            if prim(cu)!=prim(u): bad['a_pres']+=1
    # Q ∩ (ba+bba)^* = c(Q) : decode
    import re
    for m in range(1,2*L+1):
        for w in words(m):
            if re.fullmatch('(ba|bba)*',w) and prim(w):
                u=w.replace('bba','B').replace('ba','a').replace('B','b')
                if not prim(u): bad['a_img']+=1
    mu={'a':'ab','b':'abb','x':'abbb'}
    for n in range(1,L3+1):
        for u in words(n,'abx'):
            if prim(''.join(mu[x] for x in u))!=prim(u): bad['b']+=1
    for n in range(1,N+1):
        for w in words(n):
            if re.fullmatch('(b*a)+',w):
                runs=[len(r) for r in w.split('a')[:-1]]
                if prim(w)!=prim(runs): bad['c']+=1
            if re.fullmatch('(a|ba)*',w) and inP(w)!=(w.endswith('a') and not w.endswith('ba')):
                bad['d1']+=1
    # (d) sigma_min: t over {b,a} in (b*a)^+, b plays x ; sigma_min(b)=ba
    for n in range(1,N//2+1):
        for t in words(n):
            if not re.fullmatch('(b*a)+',t): continue
            w=''.join('ba' if x=='b' else 'a' for x in t)
            for k in (1,2,3):
                if not inP(w) or inLk(w,k)!=prim(t): bad['d2']+=1
    # (e) chain / soundness, exhaustive
    cnt=Counter()
    for n in range(1,N+1):
        for w in words(n):
            if not inP(w): continue
            q=prim(w); m=[inLk(w,k) for k in (1,2,3,4)]
            for k in range(3):
                if m[k] and not m[k+1]: bad['e_chain']+=1
            if any(m) and not q: bad['e_sound']+=1
            hgt=max(map(len,blocks(w)))//2+1
            if q and not inLk(w,max(1,hgt)): bad['e_union']+=1
            if q: cnt[(n,tuple(m))]+=1
    print('violations:',dict(bad) or 0)
    return cnt

if __name__=='__main__':
    main(*map(int,sys.argv[1:]))

def decode_check(N=12,K=(1,2,3)):
    """E1: count pairs (t in R_k, prime assignment for x's) with sigma-image = w; must be exactly 1 for every w in P."""
    import re
    from functools import lru_cache
    dyck=lambda s: inP(s+'a') and len(blocks(s+'a'))==1
    PR=[p for m in range(2,N+1,2) for p in map(''.join,itertools.product('ab',repeat=m)) if p[0]=='b' and dyck(p) and len(primes(p))==1]
    bad=0
    for k in K:
        cnt=Counter()
        def expand(t,i,acc):
            if len(acc)>N: return
            if i==len(t): cnt[acc]+=1; return
            if t[i]=='x':
                for p in PR: expand(t,i+1,acc+p)
            else: expand(t,i+1,acc+t[i])
        def inRk(t):  # R_k = (G_{k-1} a)^+ with depth tracking
            d=0;closed=False
            for c in t:
                closed=False
                if c=='b': d+=1
                elif c=='a': d-=1
                elif d!=k-1: return False
                if d<-1 or d>k-1: return False
                if d==-1: d=0;closed=True
            return closed
        for m in range(1,N+1):
            for t in map(''.join,itertools.product('abx',repeat=m)):
                if inRk(t): expand(t,0,'')
        for m in range(1,N+1):
            for w in words(m):
                if inP(w) and cnt[w]!=1: bad+=1
                if not inP(w) and cnt[w]: bad+=1
    print('E1 decode violations (N=%d):'%N,bad)
