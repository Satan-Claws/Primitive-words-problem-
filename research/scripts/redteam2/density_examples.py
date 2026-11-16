# Independent checks of density.md Sec. 5 examples.
import itertools, math
def prim(w):
    n=len(w); return all(w!=w[:d]*(n//d) for d in range(1,n) if n%d==0)
for n in range(1,17):
    cntE=0
    for t in itertools.product('ab',repeat=n):
        w=''.join(t)
        if w.count('b')==w.count('a')+1:
            cntE+=1; assert prim(w)
    assert cntE==(math.comb(n,(n-1)//2) if n%2 else 0)
print("E': all members primitive, |E'_n| = C(n,(n-1)/2) for n<=16")
# O2: R'_N = {|w|_a = 1 mod N}: z^k in R'_N => gcd(k,N)=1
for N in (2,3,4,6):
    for n in range(1,13):
        for t in itertools.product('ab',repeat=n):
            w=''.join(t)
            if w.count('a')%N==1%N:
                for d in range(1,n):
                    if n%d==0 and w==w[:d]*(n//d): assert math.gcd(n//d,N)==1
print("O2 ok")
# O3 mismatch parity claim
bad={0:0,1:0}
for n in range(1,15):
    for t in itertools.product('ab',repeat=n):
        w=''.join(t); mm=sum(w[i]!=w[n-1-i] for i in range(n//2))
        if mm%2!=w.count('a')%2: bad[n%2]+=1
print("O3 parity identity failures (even n, odd n):",bad[0],bad[1])
