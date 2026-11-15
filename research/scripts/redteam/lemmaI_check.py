# Redteam: independent test of closure Lemma I, rigid case (f), r>=2:
#   for merge-free cyclic data and e in [T,inf)^r:  W(e) non-primitive <=> exists s in 1..r-1, U'_i = U'_{i+s} for all i,
# with a_i, b_i computed DIRECTLY from the word w (maximal periodic extension on the circle), not from formulas.
# Also checks F1 (a_i,b_i independent of e and < A*) and |R_i| <= n-2.
import random, sys
from rt_common import is_primitive_str
seed=int(sys.argv[1]) if len(sys.argv)>1 else 1
random.seed(seed)
AL='ab' if seed%2 else 'abc'
def rw(lo,hi): return ''.join(random.choice(AL) for _ in range(random.randint(lo,hi)))
def rprim(lo,hi):
    while True:
        y=rw(lo,hi)
        if is_primitive_str(y): return y
def merges(x,y,ynext,c):
    u=x+ynext*c; return (y*(len(u)//len(y)+2)).startswith(u)
inst=0; tests=0; nonprim=0; mism=0
while inst<int(sys.argv[2]) if len(sys.argv)>2 else 3000:
    if random.random()<0.5:
        r=random.randint(2,4); ys=[rprim(1,3) for _ in range(r)]; xs=[rw(0,3) for _ in range(r)]
    else:  # shift-invariant data so that non-primitive cases occur
        r0=random.randint(1,2); rep=random.randint(2,3); r=r0*rep
        ys0=[rprim(1,3) for _ in range(r0)]; xs0=[rw(0,3) for _ in range(r0)]
        ys=ys0*rep; xs=xs0*rep
    Y=max(map(len,ys)); X=max(map(len,xs)); c=Y+1
    if any(merges(xs[i],ys[i],ys[(i+1)%r],c) for i in range(r)): continue
    inst+=1
    Astar=X+c*Y; T=4*Y+X+2*Astar+c+2
    ab_seen=None
    for trial in range(40):
        if random.random()<0.5 and r>=2:
            e=[T+random.randint(0,10) for _ in range(r)]
        else: # make e shift invariant under some s
            s=random.randint(1,r-1); e=[None]*r
            base=[T+random.randint(0,10) for _ in range(r)]
            # orbit-constant up to offsets
            for i in range(r): e[i]=base[i%__import__('math').gcd(s,r)]
            if random.random()<0.5: e[random.randrange(r)]+=random.choice([-1,1])
        w=''.join(ys[i]*e[i]+xs[i] for i in range(r)); n=len(w)
        s_=[0]*r
        for i in range(1,r): s_[i]=s_[i-1]+e[i-1]*len(ys[i-1])+len(xs[i-1])
        a=[0]*r;b=[0]*r
        for i in range(r):
            p=len(ys[i]); start=s_[i]; L=e[i]*p
            bb=0
            while L+bb+1<=n-1 and w[(start+L+bb)%n]==w[(start+L+bb-p)%n]: bb+=1
            aa=0
            while L+bb+aa+1<=n-1 and w[(start-aa-1)%n]==w[(start-aa-1+p)%n]: aa+=1
            a[i]=aa;b[i]=bb
            assert aa<Astar and bb<Astar and L+aa+bb<=n-2,("F1 bound",ys,xs,e)
        if ab_seen is None: ab_seen=(a,b)
        else: assert ab_seen==(a,b),"F1: a,b depend on e"
        t=[(s_[i]-a[i])%n for i in range(r)]
        U=[]
        for i in range(r):
            ln=(t[(i+1)%r]-t[i])%n
            U.append(''.join(w[(t[i]+j)%n] for j in range(ln)))
        crit=any(all(U[i]==U[(i+s)%r] for i in range(r)) for s in range(1,r))
        truth=not is_primitive_str(w)
        tests+=1; nonprim+=truth
        if crit!=truth: mism+=1; print("MISMATCH",ys,xs,e)
print('seed',seed,'instances',inst,'tests',tests,'nonprimitive',nonprim,'mismatches',mism)
