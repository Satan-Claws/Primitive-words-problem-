"""Brute-force checks of the examples in density.md.
(1) E' = {w : #b = #a + 1} contains no non-primitive word (n <= 18), and
    |E'_n|^(1/n) -> 2.
(2) R_k = {w : #a not= 0 mod k} contains no k-th power (n <= 18, k = 2..6).
(3) Identity used in Theorem 2: a u0 (b v a u0)^N b == (a u0 b v)^N a u0 b ... as
    U (v U)^N with U = a u0 b (random words).
"""
import itertools, random, math
def powers(n):
    out=set()
    for d in range(1,n):
        if n%d==0 and n//d>=2:
            for z in itertools.product('ab',repeat=d):
                out.add((''.join(z)*(n//d), n//d))
    return out
for n in range(1,19):
    P=powers(n)
    assert not any(w.count('b')==w.count('a')+1 for w,k in P)
    for k in range(2,7):
        assert not any(w.count('a')%k!=0 for w,kk in P if kk==k)
print("E' and R_k: no forbidden powers up to n=18")
for n in [101,1001,10001]:
    m=(n-1)//2
    print(n, (math.comb(n,m))**(1.0/n) if n<2000 else math.exp((math.lgamma(n+1)-math.lgamma(m+1)-math.lgamma(n-m+1))/n))
rng=random.Random(0)
rw=lambda: ''.join(rng.choice('ab') for _ in range(rng.randint(0,6)))
for _ in range(10000):
    a,u0,b,v=rw(),rw(),rw(),rw(); N=rng.randint(0,5)
    U=a+u0+b
    assert a+u0+(b+v+a+u0)*N+b == U+(v+U)*N
print("identity ok")
