# Independent randomized test of density Theorem 1 and Lemma M.
# Membership in Ctx_{p,q}(R,{c}) is decided by folding (decoding), R given by a random complete DFA
# over Gamma = Sigma^p x Sigma^q. kappa = idempotent power of a minimal-rank element found by random
# search (not BFS over the whole monoid as in the original script). Also runs a "sanity mutant" with
# D replaced by (p+q) (g=1) to show the test detects failures when the exponent is wrong.
import random, math, sys, itertools
def mk(rng):
    p,q=rng.choice([(1,0),(0,1),(1,1),(2,1),(1,2),(2,0),(0,2),(3,1),(2,2)])
    k=2**(p+q); ns=rng.randint(2,6)
    dfa=[[rng.randrange(ns) for _ in range(k)] for _ in range(ns)]
    F={s for s in range(ns) if rng.random()<0.35} or {rng.randrange(ns)}
    c=''.join(rng.choice('ab') for _ in range(rng.randint(0,3)))
    return p,q,dfa,F,c,ns,k
def letter(l,r): 
    s=(l+r).replace('a','0').replace('b','1'); return int(s,2) if s else 0
def fold(w,p,q,c):
    n=len(w); t,rem=divmod(n-len(c),p+q)
    if n<len(c) or rem or w[p*t:p*t+len(c)]!=c: return None
    return [letter(w[p*(i-1):p*i], w[n-q*i:n-q*(i-1)]) for i in range(1,t+1)]
def run(dfa,s,ys):
    for y in ys: s=dfa[s][y]
    return s
def member(w,L):
    p,q,dfa,F,c,ns,k=L; ys=fold(w,p,q,c)
    return ys is not None and run(dfa,0,ys) in F
def unf(ys,p,q,c):
    pairs=[]
    for y in ys:
        s=format(y,'0%db'%(p+q)).replace('0','a').replace('1','b') if p+q else ''
        pairs.append((s[:p],s[p:]))
    return ''.join(l for l,r in pairs)+c+''.join(r for l,r in reversed(pairs))
def trans(dfa,ns,ys): return tuple(run(dfa,s,ys) for s in range(ns))
def trial(rng,mutant=False):
    L=mk(rng); p,q,dfa,F,c,ns,k=L
    # random search for minimal rank: random long words
    best=None
    for _ in range(400):
        ys=[rng.randrange(k) for _ in range(rng.randint(1,30))]
        t=trans(dfa,ns,ys); r=len(set(t))
        if best is None or r<best[0]: best=(r,ys)
    r,w0=best
    # verify minimality exhaustively over words up to length 6 (cheap) -- else skip
    for l in range(1,6):
        for ys in itertools.product(range(k),repeat=l):
            if len(set(trans(dfa,ns,list(ys))))<r: return 'notmin'
    kap=list(w0)
    while trans(dfa,ns,kap+kap)!=trans(dfa,ns,kap): kap=kap+w0
    g=math.factorial(r)
    # Lemma M directly
    for _ in range(5):
        Y=[rng.randrange(k) for _ in range(rng.randint(0,8))]
        for j in range(3):
            assert trans(dfa,ns,kap+(Y+kap)*(g*j))==trans(dfa,ns,kap)
    # y0 = P kappa S in R
    for _ in range(200):
        P=[rng.randrange(k) for _ in range(rng.randint(0,4))]; S=[rng.randrange(k) for _ in range(rng.randint(0,4))]
        if run(dfa,0,P+kap+S) in F: break
    else: return 'nokappa'
    y0=P+kap+S; u0=unf(y0,p,q,c); assert member(u0,L)
    D=(p+q)*(1 if mutant else g)
    for _ in range(4):
        v=''.join(rng.choice('ab') for _ in range(rng.randint(0,7)))
        for j in range(1,4):
            if not member(u0+(v+u0)*(D*j),L): return 'FAIL'
    return 'ok'
rng=random.Random(int(sys.argv[1])); st={}
for _ in range(int(sys.argv[2])):
    r=trial(rng); st[r]=st.get(r,0)+1
print("Theorem 1:",st)
rng=random.Random(int(sys.argv[1])+99); st={}
for _ in range(int(sys.argv[2])):
    r=trial(rng,True); st[r]=st.get(r,0)+1
print("mutant D=(p+q):",st)
