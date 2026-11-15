# Redteam: closure Lemma OB tail structure. For m >= M*, S is either empty or {(m, m-kappa)}.
import random
from rt_common import is_primitive_str
random.seed(3)
def rw(lo,hi,al='ab'): return ''.join(random.choice(al) for _ in range(random.randint(lo,hi)))
def rp(lo,hi):
    while True:
        y=rw(lo,hi)
        if is_primitive_str(y): return y
bad=0; nonempty=0
for t in range(20000):
    y=rp(1,3)
    if random.random()<0.5: yp=rp(1,3)
    else: k=random.randrange(len(y)); yp=y[k:]+y[:k]
    x,z,xp,zp=[rw(0,4) for _ in range(4)]
    if random.random()<0.3:  # force a solution sometimes
        m0=random.randint(3,6); W=x+y*m0+z; 
        # choose xp,zp as prefix/suffix of W around a yp-block if possible
    C=len(x)+len(xp)+len(z)+len(zp); Ms=-(-(C+2*len(y)+2*len(yp))//len(y))
    S=set()
    for m in range(0,Ms+30):
        W=x+y*m+z; rest=len(W)-len(xp)-len(zp)
        if rest>=0 and rest%len(yp)==0 and W==xp+yp*(rest//len(yp))+zp: S.add(m)
    tail=[m in S for m in range(Ms,Ms+30)]
    if any(tail): nonempty+=1
    if any(tail) and not all(tail): bad+=1; print('OB FAIL',x,y,z,xp,yp,zp,sorted(S))
print('instances',20000,'with nonempty tail',nonempty,'violations',bad)
