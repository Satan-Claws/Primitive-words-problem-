"""r18_gend checks.
(1) B-D exponent arithmetic for CT(c): alpha_y + alpha_c + 2 < 0 ?
(2) Light finite critical linear SCC inside G^-: for single-nonterminal T -> u T v | w,
    mass of tokens (u,v) compatible with G^- (pumped alone, and pairwise), |u|+|v| <= L.
(3) Pair-model word/tree ratio for an explicit light critical SCC (split multiplicity).
"""
import itertools, math
from fractions import Fraction as Fr

print("(1) CT(c): alpha_c = -1-2^-k (finite-mass heavy side branch), alpha_y = -1 + m 2^-j (divergent yield)")
bad=good=0
for k in range(1,5):
    for j in range(0,5):
        for m in range(1,2**j+1):
            ay=-1+m/2**j; ac=-1-1/2**k
            s=ay+ac+2
            if s<0: good+=1
            else: bad+=1
print("  combos with condition TRUE:",good," FALSE:",bad,
      " e.g. light yield (ay=0) + Dyck side (ac=-3/2): sum =",0-1.5+2)

def D(c): return 1 if c=='a' else -1
def walk(w):
    P=[0]
    for c in w: P.append(P[-1]+D(c))
    return P
def inGminus(W):
    n=len(W); P=walk(W)
    for k in range(1,n//2+1):
        A=P[k]; B=P[n]-P[n-k]
        if not A<B: return False
    return True

def words(L):
    for l in range(L+1):
        for t in itertools.product('ab',repeat=l): yield ''.join(t)

print("(2) tokens (u,v), |u|+|v|<=L, exit w; G^- tested on u^i w v^i, i<=6 (alone) and on all")
print("    sequences of length<=4 over a pair (pairwise). mass = sum 2^-(|u|+|v|); critical needs >=1")
for L in (3,4,5):
    for w in ['a','ab','aab','aaab']:
        toks=[(u,v) for u in words(L) for v in words(L) if 1<=len(u)+len(v)<=L]
        ok=[]
        for (u,v) in toks:
            if all(inGminus(u*i+w+v*i) for i in range(1,7)): ok.append((u,v))
        mass=sum(Fr(1,2**(len(u)+len(v))) for u,v in ok)
        # pairwise: all sequences length<=4 from {t1,t2}
        def seqok(S):
            for r in range(1,5):
                for seq in itertools.product(S,repeat=r):
                    U=''.join(t[0] for t in seq); V=''.join(t[1] for t in reversed(seq))
                    if not inGminus(U+w+V): return False
            return True
        # greedy max-mass pairwise-compatible set
        ok.sort(key=lambda t:len(t[0])+len(t[1]))
        chosen=[]
        for t in ok:
            if all(seqok([t,s]) for s in chosen): chosen.append(t)
        gm=sum(Fr(1,2**(len(u)+len(v))) for u,v in chosen)
        fin = 'u-finite' 
        print(f"  L={L} w={w}: single-ok mass={float(mass):.3f} ({len(ok)} toks); greedy pairwise set mass={float(gm):.3f}; e.g. {chosen[:4]}")

print("(2b) same, restricted to drift-balanced tokens D(u)=D(v)=0 (forced by Hoeffding under poly ambiguity, §3)")
for L in (4,6,8):
    for w in ['a','ab','aab']:
        toks=[(u,v) for u in words(L) for v in words(L) if 1<=len(u)+len(v)<=L
              and sum(map(D,u))==0 and sum(map(D,v))==0]
        ok=[(u,v) for (u,v) in toks if all(inGminus(u*i+w+v*i) for i in range(1,6))]
        mass=sum(Fr(1,2**(len(u)+len(v))) for u,v in ok)
        print(f"  L={L} w={w}: balanced single-ok mass={float(mass):.4f} ({len(ok)} toks) e.g. {ok[:3]}")
