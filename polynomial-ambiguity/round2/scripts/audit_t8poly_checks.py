"""audit_t8poly checks: (1) independent RP bookkeeping, (2) rise-bounded count bound,
(3) subcritical light/light spanning example outside gend2/LL (prefix count has no gain)."""
import random, itertools, numpy as np
random.seed(7)
D=lambda w: sum(1 if c=='a' else -1 for c in w)
def P(w):
    p=[0]
    for c in w: p.append(p[-1]+(1 if c=='a' else -1))
    return p
def inGm(w):
    p=P(w); n=len(w)
    return all(p[k] < p[n]-p[n-k] for k in range(1,n//2+1))
def rw(l,bias=0.5): return ''.join('a' if random.random()<bias else 'b' for _ in range(l))
# (1) RP: W'=W[0,s) u W[s,e) al x be q ; x V-level (all suffix drifts <= K)
viol=tests=ks=0
for _ in range(60000):
    n=random.randint(4,14); W=rw(n,0.4)
    s=random.randint(0,n-1); e=random.randint(s+1,n); q=W[e:]
    u=rw(random.randint(0,3)); al=rw(random.randint(0,3)); be=rw(random.randint(0,3))
    K=random.randint(0,2); L=random.randint(n+2*len(u), 3*n+3)
    # x: b-biased so suffix drifts stay <= K
    x=''
    while len(x)<L:
        c='a' if random.random()<0.35 else 'b'
        x2=c+x
        if max(P(x2[::-1])) <= K or True:
            pass
        x=x2
    # enforce suffix profile <= K: compute
    pr=[D(x[len(x)-j:]) for j in range(len(x)+1)]
    if max(pr)>K: continue
    Wp=W[:s]+u+W[s:e]+al+x+be+q
    if not inGm(Wp): continue
    tests+=1; pW=P(W)
    Bm=max(pW[n]-pW[n-j] for j in range(len(q)+1))
    for k in range(0,e+1):
        ks+=1
        if pW[k] > Bm + len(be)+len(u)+K: viol+=1
print("(1) RP independent: W' in G- instances",tests,"k-values",ks,"violations",viol)
# (2) rise-bounded walks: count from r=0 vs (R+1)rho^l and 2cos formula
worst=0
for R in range(0,9):
    M=np.zeros((R+1,R+1))
    for r in range(R+1):
        if r+1<=R: M[r,r+1]+=1
        M[r,max(r-1,0)]+=1
    rho=max(abs(np.linalg.eigvals(M)))
    assert abs(rho-2*np.cos(np.pi/(2*R+3)))<1e-9
    v=np.zeros(R+1); v[0]=1
    for l in range(1,61):
        v=v@M; worst=max(worst, v.sum()/((R+1)*rho**l))
print("(2) rho_R=2cos(pi/(2R+3)) R<=8 ok; max count/((R+1)rho^l) =",round(worst,4))
# (3) subcritical light/light spanning T: X0->bXaa, X->aXaa|bXaa|c
def gen(r):
    for l in itertools.product('ab',repeat=r-1):
        yield 'b'+''.join(l)+'c'.replace('c','a')+'aa'*r  # exit c := 'a'
ok=True; cnt={}
for r in range(1,9):
    for w in gen(r):
        ok &= inGm(w)
print("(3) L subset of G- (r<=8):",ok)
# prefix count at h for long words, and NC violation (cycle s='a' has D=1)
r=14; h=10; pref=set(w[:h] for w in gen(r)); print("    distinct length-%d prefixes: %d of 2^%d=%d (no prefix gain); cycle (a,aa): D(s)=+1"%(h,len(pref),h,2**h))
print("    words of length n=3r+1: 2^(r-1) = 2^((n-1)/3 -1): tree mass exponentially small, so a FULL-word (tilted) count is needed")
