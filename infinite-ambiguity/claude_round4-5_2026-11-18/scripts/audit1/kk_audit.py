# Independent audit of kk.md (audit1). Exact integer arithmetic.
import itertools, random
from fractions import Fraction
random.seed(7)
def primes(n): return [p for p in range(2,n+1) if n%p==0 and all(p%q for q in range(2,p))]
def vp(n,p):
    a=0
    while n%p==0: n//=p;a+=1
    return a
def inV(x,D): n=len(x); return all(x[i]==x[(i+D)%n] for i in range(n))
def refl(x,c): n=len(x); return [x[(c-i)%n] for i in range(n)]
def anti(x,c): r=refl(x,c); return [x[i]-r[i] for i in range(len(x))]
def chords(n,c):
    P=[];seen=set()
    for i in range(n):
        j=(c-i)%n
        if (j,i) in seen: continue
        seen.add((i,j)); P.append(tuple(sorted({i,j})))
    return P
def stratified(supps):
    for s in supps:
        for t in supps:
            if len(s)==2 and len(t)==2:
                i,k=s; j,l=t
                if i<j<k<l: return False
    return True
# 1. P_c stratified for all n<=40, all c
print("P_c stratified all n<=40:", all(stratified(chords(n,c)) for n in range(2,41) for c in range(n)))
# 2. A2 + Theorem A: B_p single class mod p^a; good c exists, random and exhaustive
def check(x):
    n=len(x); ps=[p for p in primes(n) if not inV(x,n//p)]
    good=[c for c in range(n) if all(not inV(anti(x,c),n//p) for p in ps)]
    for p in ps:
        B=[c for c in range(n) if inV(anti(x,c),n//p)]
        m=p**vp(n,p)
        if len({c%m for c in B})>1: return 'A2fail'
    return 'ok' if good else 'noGood'
res={}
for n in [4,6,8,9,10,12]:
    for x in itertools.product(range(3) if n<=8 else range(2),repeat=n):
        r=check(list(x)); res[r]=res.get(r,0)+1
print("exhaustive n in {4,6,8,9,10,12}:",res)
res={}
for n in [18,24,30,36,60,72,90,210]:
    ps=primes(n)
    for _ in range(150 if n<100 else 30):
        # hard: sum of periodic vectors (in W_n) plus small noise sometimes
        x=[0]*n
        for p in ps:
            D=n//p; base=[random.randint(0,5) for _ in range(D)]
            x=[x[i]+base[i%D] for i in range(n)]
        if random.random()<0.3: x[random.randrange(n)]+=1
        r=check(x); res[r]=res.get(r,0)+1
print("random n up to 210:",res)
# 3. Corollary A3: points of delta+ + N P_c are primitive (sample)
bad=0
for n in [6,12,30]:
    for _ in range(200):
        d=[random.randint(-3,3) for _ in range(n)]
        if any(inV(d,n//p) for p in primes(n)): continue
        c=[c for c in range(n) if all(not inV(anti(d,c),n//p) for p in primes(n))][0]
        m=min(d); b=[v-m for v in d]
        for _ in range(20):
            y=b[:]
            for (i,*r) in chords(n,c):
                t=random.randint(0,4); y[i]+=t
                if r: y[r[0]]+=t
            if any(inV(y,n//p) for p in primes(n)): bad+=1
print("A3 sampled piece points non-primitive:",bad)
# 4. GAP test for Theorem B with non-constant h: naive piece b + N P_{c,h} vs V_d, d not in D_h.
n=6; h=[1,2,1,2,1,2]   # h in V_2 (=n/3), not in V_3 (=n/2): D_h={2}
found=[]
for d0 in itertools.product(range(3),repeat=n):
    d=list(d0)
    if inV(d,2): continue
    goodc=[c for c in range(n) if not inV(anti([Fraction(d[i],h[i]) for i in range(n)],c),2)]
    for c in goodc:
        # search small elements y = d + K h + sum t_ch (h_i e_i + h_j e_j) in V_3, i.e. non-primitive
        ch=chords(n,c)
        for K in range(0,2):
            for ts in itertools.product(range(4),repeat=len(ch)):
                y=[d[i]+K*h[i] for i in range(n)]
                for (s,t) in zip(ch,ts):
                    for i in s: y[i]+=t*h[i]
                if inV(y,3) or inV(y,2) or inV(y,1):
                    found.append((d,c,K,ts,y)); break
            else: continue
            break
    if len(found)>=1: break
print("naive weighted-reflection piece hits non-primitive vector:",found[:1])
