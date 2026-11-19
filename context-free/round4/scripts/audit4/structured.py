# Exhaustive/sampled search over count-periodic 6-tuples: real segments a(ab+)+ (mode real) or arbitrary binary (mode abs).
import sys, itertools, random, time
from cover_r6 import *
mode=sys.argv[1]; amax=int(sys.argv[2]); bmax=int(sys.argv[3]); cap=int(sys.argv[4]); tlim=float(sys.argv[5])
random.seed(1)
cls={}
if mode=='real':
    def comps(n,k):
        if k==1:
            if n>=1: yield (n,)
            return
        for f in range(1,n-k+2):
            for r in comps(n-f,k-1): yield (f,)+r
    for A in range(2,amax+1):
        for B in range(A-1,bmax+1):
            cls[(A,B)]=['a'+''.join('a'+'b'*x for x in c) for c in comps(B,A-1)]
else:
    for A in range(0,amax+1):
        for B in range(0,bmax+1):
            if A+B==0: continue
            cls[(A,B)]=[''.join(p) for p in set(itertools.permutations('a'*A+'b'*B))]
segs=sorted({s for v in cls.values() for s in v}); sid={s:i for i,s in enumerate(segs)}
tab=T(segs)
Avals=sorted({k[0] for k in cls}); Bvals=sorted({k[1] for k in cls})
def pervecs(vals):
    out=set()
    for x,y in itertools.product(vals,repeat=2): out.add((x,y,x,y,x,y))
    for x,y,z in itertools.product(vals,repeat=3): out.add((x,y,z,x,y,z))
    return sorted(out)
AV=pervecs(Avals); BV=pervecs(Bvals)
t0=time.time(); checked=0; bad=0; exh=0; samp=0
for av in AV:
    for bv in BV:
        if time.time()-t0>tlim: break
        lists=[cls.get((av[i],bv[i])) for i in range(6)]
        if any(not l for l in lists): continue
        size=1
        for l in lists: size*=len(l)
        if size<=cap:
            it=itertools.product(*lists); exh+=1
        else:
            it=(tuple(random.choice(l) for l in lists) for _ in range(cap)); samp+=1
        for tup in it:
            idx=[sid[s] for s in tup]
            if not prim(idx): continue
            checked+=1
            if not Ncover(tab,idx):
                bad+=1
                if bad<=10: print('UNCOVERED',tup,flush=True)
print(mode,amax,bmax,'patterns exhaustive',exh,'sampled',samp,'checked',checked,'uncovered',bad,'time',round(time.time()-t0))
