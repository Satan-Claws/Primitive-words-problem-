# Abstract model: w = (z1..z6), z_i nonempty words over {0,1}. Primitive iff not square-tuple and not cube-tuple.
# Test simple nested certificate patterns (see r6.md).
import itertools, sys
def startmis(S,X):
    r=[t for t in range(min(len(S),len(X))) if S[t]!=X[t]]
    if len(X)<len(S): r.append(len(X))
    return r
def endmis(S,X):
    d=len(X)-len(S); r=[t for t in range(len(S)) if 0<=t+d<len(X) and S[t]!=X[t+d]]
    if len(X)<len(S): r.append(len(S)-len(X)-1)
    return r
def lencert(z):
    l=[len(x) for x in z]
    return any(l[i]+l[(i+1)%6]!=l[(i+3)%6]+l[(i+4)%6] for i in range(6))
def covered(z, slack=0):
    if lencert(z): return 'len'
    for S in range(6):
        sq=z[(S+3)%6]
        A=startmis(z[S],sq); B=endmis(z[S],z[(S+2)%6])
        if A and B and min(A)<=max(B)+slack: return 'p+2'
        C=startmis(z[S],z[(S-2)%6]); D=endmis(z[S],sq)
        if C and D and min(C)<=max(D)+slack: return 'p-2'
    return None
def prim(z):
    sq= z[0]==z[3] and z[1]==z[4] and z[2]==z[5]
    cu= z[0]==z[2]==z[4] and z[1]==z[3]==z[5]
    return not(sq or cu)
L=int(sys.argv[1]); slack=int(sys.argv[2]) if len(sys.argv)>2 else 0
segs=[''.join(p) for n in range(1,L+1) for p in itertools.product('01',repeat=n)]
# restrict to length vectors in V2+V3 (others covered by len)
bad=0;tot=0;ex=[]
import random
for lv in itertools.product(range(1,L+1),repeat=6):
    if any(lv[i]+lv[(i+1)%6]!=lv[(i+3)%6]+lv[(i+4)%6] for i in range(6)): continue
    pools=[[s for s in segs if len(s)==n] for n in lv]
    size=1
    for p in pools: size*=len(p)
    it = itertools.product(*pools) if size<=20000 else (tuple(random.choice(p) for p in pools) for _ in range(20000))
    for z in it:
        if not prim(z): continue
        tot+=1
        if covered(z,slack) is None:
            bad+=1
            if len(set(''.join(z)))>1 and len(ex)<15: ex.append(z)
print("checked",tot,"uncovered",bad)
for e in ex: print(e)
