# Audit of r7_lemmaQ: (1) Q0: b x b^r a^{m+1} in G- for all x in {a,b}^m (m=10, r=0,2,4);
# (2) |G-_n| * sqrt(n) / 2^n roughly constant (used in Prop S step 1), exhaustive n<=20.
from itertools import product
def inGm(w):
    n=len(w)
    return all(w[:k].count('a')-w[n-k:].count('a')<0 for k in range(1,n//2+1))
m=10
for r in (0,2,4):
    ok=all(inGm('b'+''.join(x)+'b'*r+'a'*(m+1)) for x in product('ab',repeat=m))
    print('Q0 r=%d all in G-:'%r,ok)
for n in range(8,21,2):
    c=sum(inGm(''.join(t)) for t in product('ab',repeat=n)); print(n,c,round(c*n**0.5/2**n,3))
