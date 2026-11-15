# Redteam: rectangles Prop 5.1: psi(n) <= 2^n <= 2 psi(n); C(i+j,i) <= 2 psi(i,j); formulas vs brute force.
from math import comb
from rt_common import *
def mob(d):
    r=1;m=d;p=2
    while p*p<=m:
        if m%p==0:
            m//=p
            if m%p==0: return 0
            r=-r
        p+=1
    return -r if m>1 else r
def divs(n): return [d for d in range(1,n+1) if n%d==0]
psi=lambda n: sum(mob(d)*2**(n//d) for d in divs(n))
from math import gcd
psi2=lambda i,j: sum(mob(d)*comb((i+j)//d,i//d) for d in divs(gcd(i,j))) if (i or j) else 0
for n in range(1,15):
    bf=sum(is_primitive_str(to_str(w,n)) for w in range(1<<n)); assert bf==psi(n)
    for i in range(n+1):
        bf2=sum(1 for w in range(1<<n) if bin(w).count('1')==n-i and is_primitive_str(to_str(w,n)))
        assert bf2==psi2(i,n-i),(i,n-i)
assert all(psi(n)<=2**n<=2*psi(n) for n in range(1,1500))
assert all(comb(i+j,i)<=2*psi2(i,j) for i in range(1,300) for j in range(1,300))
print('Prop 5.1 checks pass')
