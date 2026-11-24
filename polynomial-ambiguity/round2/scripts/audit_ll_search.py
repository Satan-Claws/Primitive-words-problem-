# Audit of Theorem LL: brute-force search for critical finite token sets (sum 2^-|u|-|v| = 1,
# token sizes <= 2, distinct pairs, two-sided) and small (p,w,q) such that EVERY truncation
# p u1..ur w vr..v1 q for r <= R lies in G^- (d_k < 0, 1<=k<=n/2).  Theorem LL predicts:
# none survive for large R; also report which survive zero-drift (Step 1 necessary condition).
import itertools
from fractions import Fraction as F
def D(s): return s.count('a')-s.count('b')
def inGm(w):
    n=len(w)
    return all(w[:k].count('a')-w[n-k:].count('a')<0 for k in range(1,n//2+1))
words=lambda L:[''.join(t) for t in itertools.product('ab',repeat=L)]
toks=[]
for su in range(0,3):
    for u in words(su):
        for v in words(2-su if False else 0): pass
toks=[(u,v) for s in (1,2) for su in range(s+1) for u in words(su) for v in words(s-su)]
small=[w for L in range(0,4) for w in words(L)]
R=6
surv=[];zd=0;cnt=0
for mask in range(1,1<<len(toks)):
    T=[toks[i] for i in range(len(toks)) if mask>>i&1]
    if sum(F(1,2**(len(u)+len(v))) for u,v in T)!=1: continue
    if not any(u for u,v in T) or not any(v for u,v in T): continue
    cnt+=1
    pi=[F(1,2**(len(u)+len(v))) for u,v in T]
    if sum(p*D(u) for p,(u,v) in zip(pi,T))!=0 or sum(p*D(v) for p,(u,v) in zip(pi,T))!=0: continue
    zd+=1
    for p in small:
      for q in small:
        for w in small[1:]:
          ok=True
          for r in range(R+1):
            for seq in itertools.product(T,repeat=r):
              W=p+''.join(u for u,v in seq)+w+''.join(v for u,v in reversed(seq))+q
              if not inGm(W): ok=False;break
            if not ok:break
          if ok: surv.append((T,p,w,q))
print("critical two-sided sets",cnt,"zero-drift",zd,"surviving depth",R,":",len(surv))
for s in surv[:5]: print(s)

# Phase 2: deeper test of the depth-6 survivors: periodic blocks (len<=3) repeated 40x, and
# two-phase sequences beta1^m beta2^M (the II.2(iii)-type adversary).
import random
random.seed(1)
def killed(T,p,w,q):
    blocks=[list(b) for L in (1,2) for b in itertools.product(T,repeat=L)]
    for b1 in blocks:
        for m in (0,5,20):
            for b2 in blocks:
                seq=b1*m+b2*40
                for r in range(0,len(seq)+1,max(1,len(seq)//25)):
                    s=seq[:r]
                    W=p+''.join(u for u,v in s)+w+''.join(v for u,v in reversed(s))+q
                    if not inGm(W): return (b1,m,b2,r)
    return None
alive=0;uniqT=set()
for T,p,w,q in surv:
    k=killed(T,p,w,q)
    if k is None: alive+=1; print("ALIVE",T,p,w,q)
    uniqT.add(tuple(T))
print("survivor token sets",len(uniqT),"; still alive after deep adversarial test:",alive)

# Phase 3: classify the token sets of deep survivors by the report's case split.
from collections import Counter
cls=Counter()
for T,p,w,q in surv:
    if killed(T,p,w,q) is not None: continue
    pi=[F(1,2**(len(u)+len(v))) for u,v in T]
    allzero=all(D(u)==0 and D(v)==0 for u,v in T)
    eqlen=all(len(u)==len(v) for u,v in T)
    c=("I(delta=0)" if allzero else "II.1(|u|=|v|)" if eqlen else "OTHER")
    cls[(tuple(T),c)]+=1
for k,v in cls.items(): print(v,k)
