# audit3 independent checks (one core, < 2 min)
import itertools, re, random, sys
from math import gcd
def prim(w):
    n=len(w)
    if n==0: return False
    return (w+w).find(w,1)==n
def blocks(w):
    # w in (a*b)^+ -> block vector
    if not w or w[-1]!='b': return None
    return [len(s) for s in w.split('b')[:-1]]
def words(n):
    for t in itertools.product('ab',repeat=n): yield ''.join(t)
# ---- 1. L(c0) by definition, primitivity
def inLc0(w,c0):
    x=blocks(w); l=len(c0)
    if x is None: return False
    K=len(x)
    if K%l or K<2*l: return False
    for i in range(1,K+1):
        T=c0[(i-1)%l]-c0[(-i)%l]+(i==1)-(i==K)
        if x[i-1]-x[K-i]!=T: return False
    return True
c0s=[(0,1,3),(0,1),(0,0,1),(0,2,1,5),(1,0,0,2),(0,1,3,2,0),(5,0),(0,7,2),(3,3,0,1)]
for c0 in c0s:
    cnt=0
    for n in range(1,21):
        for w in words(n):
            if inLc0(w,c0):
                cnt+=1
                assert prim(w),(c0,w)
    # random large members: build x with x-Rx=T
    l=len(c0)
    for _ in range(3000):
        k=random.randint(2,6); K=l*k
        x=[None]*K
        for i in range(1,K+1):
            T=c0[(i-1)%l]-c0[(-i)%l]+(i==1)-(i==K)
            j=K+1-i
            if i<j:
                base=random.randint(0,4)
                lo=max(0,T); hi=base+lo
                xi=random.choice([lo,hi,lo+1]); x[i-1]=xi; x[j-1]=xi-T
            elif i==j:
                assert T==0; x[i-1]=random.randint(0,3)
        w=''.join('a'*v+'b' for v in x)
        assert inLc0(w,c0) and prim(w),(c0,x)
    # family membership
    for m in range(-min(c0),-min(c0)+5):
        for k in range(2,6):
            c=[m+v for v in c0]
            w='a'+''.join('a'*v+'b' for v in c)*k
            assert inLc0(w,c0),(c0,m,k)
    print('L(c0) ok',c0,'members<=20:',cnt)
# random T with general l-periodic unbounded v (Theorem 3 uses only periodicity): x=(c)^k+e1 random c
for _ in range(20000):
    l=random.randint(2,5); k=random.randint(2,6); c=[random.randint(0,6) for _ in range(l)]
    w='a'+''.join('a'*v+'b' for v in c)*k
    assert prim(w),w
print('random a.(c)^k primitive ok (F_2-type, any c)')
# Parikh claim
w='a'+('aab'+'ab'+'ab')*2
print('F2 p=2,q=1,k=2:',w,w.count('a'),w.count('b'), 'aaabb^3', ('aaabb'*3).count('a'),('aaabb'*3).count('b'))
# ---- 2. W soundness
def inW(w):
    n=len(w); S=[0]
    for ch in w*2: S.append(S[-1]+(1 if ch=='a' else -1))
    D=S[n]; h=n//2
    for i in range(n):
        win=S[i+1:i+h+1]
        if D>=1 and all(s<=S[i] for s in win): return True
        if D==0 and all(s<S[i] for s in win): return True
        if D<=-1 and all(s>=S[i] for s in win): return True
    return False
for n in range(1,17):
    c=0
    for w in words(n):
        if inW(w):
            c+=1; assert prim(w),w
    if n>=12: print('W n=%d density %.4f'%(n,c/2**n))
print('W sound n<=16; eps in W by literal definition?', inW(''))
# ---- 3. L-mu
mu={'a':'ab','b':'ba'}
for n in range(1,15):
    for x in words(n):
        y=''.join(mu[ch] for ch in x)
        assert prim(y)==prim(x)
print('L-mu ok n<=14')
# e=2, |t| odd: can mu(x)=tt with |t| odd? (proof gap case)
bad=0
for n in range(1,15):
    for x in words(n):
        y=''.join(mu[ch] for ch in x); h=len(y)//2
        if y[:h]==y[h:] and h%2==1: bad+=1
print('mu(x)=tt with |t| odd occurrences:',bad)
# ---- 4. L-PS brute
for _ in range(3000):
    r=''.join(random.choice('ab') for _ in range(random.randint(1,8)))
    s=''.join(random.choice('ab') for _ in range(random.randint(0,10)))
    w=s+r
    if not prim(w) and len(w)>0:
        n=len(r)
        P=[p for p in range(1,len(w)) if len(w)%p==0 and w==w[:p]*(len(w)//p)][0]
        t=w[:P] # primitive root; any root works
        for p in [d for d in range(1,len(w)) if len(w)%d==0 and w==w[:d]*(len(w)//d)]:
            t=w[:p]
            if p>=n: assert r in s
            else:
                assert all(r[i]==r[i+p] for i in range(n-p)) and r[-p:]==t[-p:] or r.endswith(w[-p:])
                tw=(w[-p:]*(len(w)//p+2))
                assert s==tw[:len(s)] and len(s)>=2*p-n
print('L-PS ok')
# ---- 5. L-UC / Lemma 3 / Lemma 2 step 1
def exc(v): return v.count('b')-v.count('a')
def proot(v):
    n=len(v)
    for p in range(1,n+1):
        if n%p==0 and v==v[:p]*(n//p): return v[:p]
for n in range(1,17):
    for v in words(n):
        e=exc(v)
        if e>=1:
            ispow = n%e==0 and v==v[:n//e]*e
            assert ispow == (exc(proot(v))==1),v
print('Lemma 3 ok n<=16')
from math import comb
# series check S(z)=sum_t E1(z^t)
for n in range(1,17):
    cnt=sum(1 for v in words(n) if exc(v)>=1 and n%exc(v)==0 and v==v[:n//exc(v)]*exc(v))
    ser=sum(comb(n//t,(n//t-1)//2) for t in range(1,n+1) if n%t==0 and (n//t)%2==1)
    assert cnt==ser,(n,cnt,ser)
print('S series ok')
# ---- 6. L1 count
L1=re.compile(r'^(a*b)*(a*)b(a*)b(a*b)*$')
def inL1(w):
    x=blocks(w)
    return x is not None and any(x[i]!=x[i+1] for i in range(len(x)-1))
def d(n): return sum(1 for e in range(1,n+1) if n%e==0)
for n in range(1,21):
    c=sum(1 for w in words(n) if inL1(w))
    assert c==2**(n-1)-d(n),(n,c)
print('L1 count ok n<=20')
