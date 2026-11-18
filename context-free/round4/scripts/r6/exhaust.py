# Exhaustive: all z in ({0,1}^+)^6, |z_i|<=L, primitive, with BOTH count tuples (#0,#1 per segment)
# 2- or 3-periodic (others are covered by the commutative certificate). Check nested pattern with slack.
import itertools, sys
from cover3lib import startmis, endmis, per, prim
def covered(z, slack):
    for S in range(6):
        sq=z[(S+3)%6]
        A=startmis(z[S],sq); B=endmis(z[S],z[(S+2)%6])
        if A and B and min(A)<=max(B)+slack: return True
        C=startmis(z[S],z[(S-2)%6]); D=endmis(z[S],sq)
        if C and D and min(C)<=max(D)+slack: return True
    return False
L=int(sys.argv[1]); slack=int(sys.argv[2])
bycnt={}
for n in range(1,L+1):
    for p in itertools.product('01',repeat=n):
        s=''.join(p); bycnt.setdefault((s.count('0'),s.count('1')),[]).append(s)
keys=list(bycnt)
tot=bad=0; ex=[]
seen=set()
# periodic count-tuples: square (k0,k1,k2,k0,k1,k2) or cube (k0,k1,k0,k1,k0,k1), separately for 0s and 1s
def tuples():
    for a in itertools.product(range(0,L+1),repeat=3):
        yield (a[0],a[1],a[2],a[0],a[1],a[2])
    for a in itertools.product(range(0,L+1),repeat=2):
        yield (a[0],a[1],a[0],a[1],a[0],a[1])
T=set(tuples())
for t0 in T:
    for t1 in T:
        ks=[(t0[i],t1[i]) for i in range(6)]
        if any(k not in bycnt for k in ks): continue
        for z in itertools.product(*[bycnt[k] for k in ks]):
            if not prim(z): continue
            tot+=1
            if not covered(z,slack):
                bad+=1
                if len(ex)<10: ex.append(z)
print("L",L,"slack",slack,"checked",tot,"uncovered",bad); [print(e) for e in ex]
