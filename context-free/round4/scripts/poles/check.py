# Brute-force checks for poles.md. One core, runs in < 1 min.
from itertools import product
def is_power(v,k):
    n=len(v)
    return n%k==0 and v==v[:n//k]*k
def proot(v):
    n=len(v)
    for d in range(1,n+1):
        if n%d==0 and v==v[:d]*(n//d): return v[:d]
def exc(v): return v.count('b')-v.count('a')

# (1) Marker language M_Y = {a^k b v : v nonempty, v not u^k with u in Y}, Y = a{a,b}*.
# Check count of excluded words E_n = sum_{k>=1, k | n-k-1} 2^{(n-k-1)/k - 1} (n<=16)
def inY(u): return len(u)>0 and u[0]=='a'
for n in range(2,17):
    cnt=0
    for k in range(1,n-1):
        m=n-k-1
        for t in product('ab',repeat=m):
            v=''.join(t)
            if is_power(v,k) and inY(v[:m//k]): cnt+=1
    pred=sum(2**((n-k-1)//k-1) for k in range(1,n-1) if (n-k-1)%k==0)
    assert cnt==pred,(n,cnt,pred)
print("marker excluded-count formula OK n<=16")
# slice a^k b (ab)^r : excluded iff k | r
for k in range(1,12):
    for r in range(1,30):
        v='ab'*r
        assert (is_power(v,k) and inY(v[:len(v)//k]))==(r%k==0)
print("slice a^k b (ab)^r: excluded iff k|r  OK")

# (2) S = {v : exc(v)>=1, v is an exc(v)-th power}. Check S = {u^t: exc(u)=1}
#     and v in S iff exc(proot(v))==1, and |S_n| = sum_{t|n} |E1_{n/t}|, E1 = {exc=1}
from math import comb
def E1(m): return comb(m,(m-1)//2) if m%2==1 else 0
for n in range(1,17):
    cnt=0
    for t in product('ab',repeat=n):
        v=''.join(t); e=exc(v)
        inS = e>=1 and is_power(v,e)
        assert inS == (e>=1 and exc(proot(v))==1)
        cnt+=inS
    pred=sum(E1(n//t) for t in range(1,n+1) if n%t==0)
    assert cnt==pred,(n,cnt,pred)
print("excess-normalised power set S: characterisation and count OK n<=16")
