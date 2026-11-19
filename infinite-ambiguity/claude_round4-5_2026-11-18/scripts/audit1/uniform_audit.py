# Independent audit of uniform.md claims (audit1). Pure python, one core.
import itertools, random, re
from functools import lru_cache
random.seed(1)
def prim_root_exp(w):
    n=len(w)
    for d in range(1,n+1):
        if n%d==0 and w[:d]*(n//d)==w: return n//d
def is_prim(w): return len(w)>0 and prim_root_exp(w)==1
def is_kpow(w,k):
    n=len(w); return n%k==0 and w[:n//k]*k==w
reR=re.compile(r'a(?:ab+)*a(?:ab+)*$')
def cyc_aa(w): n=len(w); return sum(1 for i in range(n) if w[i]=='a' and w[(i+1)%n]=='a')
# (a) enumerate all words of R up to length L directly via regex over all strings
L=22
def gen_R(L):
    # generate words of R by structure: a u a v
    blocks=[]
    def seqs(maxlen):
        # all words in (ab+)* of length<=maxlen
        out=['']; frontier=['']
        while frontier:
            nf=[]
            for s in frontier:
                for k in range(1,maxlen):
                    t=s+'a'+'b'*k
                    if len(t)<=maxlen: nf.append(t)
                    else: break
            out+=nf; frontier=nf
        return out
    S=seqs(L-2)
    bylen={}
    for s in S: bylen.setdefault(len(s),[]).append(s)
    res=[]
    for lu,us in bylen.items():
        for lv,vs in bylen.items():
            if lu+lv+2<=L:
                for u in us:
                    for v in vs: res.append('a'+u+'a'+v)
    return res
Rw=gen_R(L)
assert all(reR.match(w) for w in Rw)
print("words of R, length<=22:",len(Rw))
bad=[w for w in Rw if (not is_prim(w)) and not is_kpow(w,2)]
print("non-primitive non-square words in R:",len(bad))
print("cyclic aa count always 2:", all(cyc_aa(w)==2 for w in Rw))
# multiplicativity of cyclic count on random z,k
ok=all(cyc_aa(z*k)==k*cyc_aa(z) for z in (''.join(random.choice('ab') for _ in range(random.randint(1,9))) for _ in range(3000)) for k in range(1,5))
print("cyc count multiplicative:",ok)
# cross-check regex membership on all strings length<=14
cnt=0
for n in range(0,15):
    for t in itertools.product('ab',repeat=n):
        w=''.join(t)
        if reR.match(w): cnt+=1
print("R words len<=14 via brute:",cnt," via gen:",sum(1 for w in Rw if len(w)<=14))
# (b) G* : count parse trees by DP; language = coPow2 on all words len<=14
def trees(w):
    n=len(w)
    @lru_cache(None)
    def A(i,j,c):  # X^k c X^k spanning w[i:j]
        if j-i<1 or (j-i)%2==0: return 0
        m=(i+j)//2
        return 1 if w[m]==c else 0
    @lru_cache(None)
    def O(i,j):
        return 1 if (j-i)%2==1 else 0  # O -> X | X X O : unique tree per odd length
    t=O(0,n)
    for k in range(1,n):
        t+=A(0,k,'a')*A(k,n,'b')+A(0,k,'b')*A(k,n,'a')
    return t
mism=0
for n in range(0,15):
    for tt in itertools.product('ab',repeat=n):
        w=''.join(tt)
        inL=trees(w)>0
        if inL==is_kpow(w,2): mism+=1
print("G* vs coPow2 mismatches (len<=14, all words incl. eps):",mism)
mx={}
for w in Rw: mx[len(w)]=max(mx.get(len(w),0),trees(w))
print("max trees per even length on R:",[mx[l] for l in sorted(mx) if l%2==0])
# (c) Prop 2.1 instances: R_p, R_{p^e}; exponent sets
def gen_Rk(k,maxlen,trials=20000):
    E=set()
    for _ in range(trials):
        zs=[]
        for _ in range(k):
            nb=random.randint(1,2); zs.append('a'+''.join('a'+'b'*random.randint(1,2) for _ in range(nb)))
        # bias toward powers
        r=random.random()
        if r<0.3:
            d=random.choice([x for x in range(1,k+1) if k%x==0]); zs=zs[:d]*(k//d)
        w=''.join(zs); e=prim_root_exp(w)
        if e>1: E.add(e)
        assert cyc_aa(w)==k
    return E
for k in [2,3,5,4,8,9,6,12]:
    print("R_k k=%d exponents seen:"%k, sorted(gen_Rk(k,0)))
# (d) R6 identity: Q ∩ R6 = R6 ∩ coPow2 ∩ coPow3 = {z1z2z3!=z4z5z6 and not z1z2=z3z4=z5z6}
facs=['a'+''.join('a'+'b'*e for e in es) for nb in (1,2) for es in itertools.product((1,2),repeat=nb)]
print("factor alphabet size",len(facs))
mis=0;tot=0;E=set()
for zs in itertools.product(facs,repeat=6):
    w=''.join(zs); tot+=1
    p=is_prim(w); q=(not is_kpow(w,2)) and (not is_kpow(w,3))
    r=(zs[:3]!=zs[3:]) and not (zs[0:2]==zs[2:4]==zs[4:6])
    if not(p==q==r): mis+=1
    e=prim_root_exp(w)
    if e>1:E.add(e)
print("R6 exhaustive over 6-letter factor alphabet: words",tot,"mismatches",mis,"exponents",sorted(E))
# edge: E(R)=empty case & epsilon
print("eps is 2nd power:",is_kpow('',2), " a is prim:",is_prim('a'))
