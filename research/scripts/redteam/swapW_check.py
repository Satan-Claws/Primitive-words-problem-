# Redteam: Lemma W (closure) as a consequence-check: two distinct non-primitive words of length n
# sharing a prefix of length n-k. Report max n/k over violations (closure claims 18/7 up to n=20).
from rt_common import *
from fractions import Fraction
best=Fraction(0); arg=None
for n in range(2,37):
    NP=nonprim_words(n)
    for k in range(1,n):
        l=n-k; mask=(1<<l)-1; seen={}
        viol=False
        for w in NP:
            y=w&mask
            if y in seen and seen[y]!=w: viol=True;break
            seen[y]=w
        if viol:
            assert 6*k>n, ("Lemma W violated",n,k)
            if Fraction(n,k)>best: best=Fraction(n,k);arg=(n,k)
print("Lemma W holds for n<=36; max ratio n/|x| among violations:",best,float(best),arg)
