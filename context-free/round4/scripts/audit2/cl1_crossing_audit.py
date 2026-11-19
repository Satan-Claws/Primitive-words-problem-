import itertools, sys
from functools import lru_cache
def prim(w):
    n=len(w)
    return n>0 and all(w!=w[d:]+w[:d] for d in range(1,n) if n%d==0)
def words(n): return (''.join(t) for t in itertools.product('ab',repeat=n))
def beta(w):
    if not w: return ()
    if w[-1]!='b': return None
    return tuple(len(p) for p in w[:-1].split('b'))
# grammar T->aS; S->Nb|Ab|eps; N->aNa|bS; A->aA|eps
@lru_cache(None)
def gS(s):
    if s=='': return True
    if s[-1]!='b': return False
    t=s[:-1]
    if set(t)<= {'a'}: return True  # A b
    return gN(t)
@lru_cache(None)
def gN(s):
    if len(s)>=2 and s[0]=='a' and s[-1]=='a' and gN(s[1:-1]): return True
    return len(s)>=1 and s[0]=='b' and gS(s[1:])
def inL(w): return len(w)>=1 and w[0]=='a' and gS(w[1:])
def predL(w):
    if not w or w[0]!='a': return False
    x=beta(w[1:]); return x is not None and x==x[::-1]
def inLgen(w):
    x=beta(w)
    if not x: return False
    k=len(x)
    for j in range(k):
        if x[j]>=1 and j!=k-1-j:
            z=list(x); z[j]-=1
            if z==z[::-1]: return True
    return False
for n in range(1,17):
    for w in words(n):
        assert inL(w)==predL(w),w
        if inL(w): assert prim(w),w
        if inLgen(w): assert prim(w),w
print('cl1 grammar==pred, L,Lgen in Q up to 16')
# cyclic closure of Lgen: test claim "every u with <=2 blocks, every one-a insertion into u^k in Cyc(Lgen)"
def incyc(w,f): return any(f(w[r:]+w[:r]) for r in range(len(w)))
bad=[]
for i in range(0,5):
  for j in range(0,5):
    for u in (['a'*i+'b'] if j==0 else []) + ['a'*i+'b'+'a'*j+'b']:
      for k in range(2,5):
        p=u*k
        for pos in range(len(p)+1):
            w=p[:pos]+'a'+p[pos:]
            if not incyc(w,inLgen): bad.append((u,k,pos,w))
print('2-block insertion failures',len(bad),bad[:5])
# chiral example from CL2
u='ab'+'aab'+'aaaab'
for k in (2,3):
    w='a'+u*k
    print('chiral',w,incyc(w,inLgen),incyc(w,lambda v: inL(v)))
# crossing Lemma 2
from math import ceil
for l in range(1,40):
  for kk in range(1,40):
    n=l+kk
    for p in (2,3,5,7):
      if n%p: continue
      for j in range(1,p):
        iy=l-(-(-j*l//p)); im=j*kk//p
        assert 0<=iy<l and 0<=im<kk and (l+im)-iy==j*n//p
print('Lemma2 ok')
