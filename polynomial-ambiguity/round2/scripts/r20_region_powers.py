"""r20_region: how many m make a two-sided pumping x_m = al s^m be t^m ga a proper power?
Random short al,s,be,t,ga (|s|+|t|>=1), m=0..60. Reports the max number of power-values of m per family."""
import random
def prim(w):
    n=len(w); return n>0 and all(w!=w[p:]+w[:p] for p in range(1,n) if n%p==0)
random.seed(2); rw=lambda L:''.join(random.choice('ab') for _ in range(L))
hist={}
for _ in range(20000):
    al,be,ga=rw(random.randint(0,4)),rw(random.randint(0,4)),rw(random.randint(0,4))
    s,t=rw(random.randint(0,3)),rw(random.randint(0,3))
    if not s+t: continue
    c=sum(not prim(al+s*m+be+t*m+ga) for m in range(1,61) if al+s*m+be+t*m+ga)
    hist[c]=hist.get(c,0)+1
print("families by #m in [1,60] giving a power:",dict(sorted(hist.items())))
