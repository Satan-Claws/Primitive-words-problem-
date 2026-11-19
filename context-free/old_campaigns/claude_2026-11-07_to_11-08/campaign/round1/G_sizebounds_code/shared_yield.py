# Cross-length "shared yield" measure test.  A fixed grammar provides only |N| yield sets per length l,
# shared by all positions i and all total lengths n (contexts are free).  Test whether Q_n is covered
# using ONLY the yield sets  Sigma^l,  {first letter = a},  {last letter = a}  (1+2|Sigma| per length):
#  type A: some balanced cut [j,j+l) whose context arc (length n-l) has no period in D  (yield free)
#  type B (n even): cut [j,j+l), l<=n/2, context arc has no period in E=D\{n/2}, and yield's first
#          (or last) letter differs from its antipode, which lies in the context.
import numpy as np
from verify_general import all_words, prim, has_period, divisors
def run(n,k=2):
    D=divisors(n); E=[d for d in D if 2*d!=n]; h=n//2
    W=all_words(n,k); P=prim(W); cov=np.zeros(len(W),bool)
    for l in range(-(-n//3),(2*n)//3+1):
        L=n-l
        for j in range(n):
            idx=[(j+l+o)%n for o in range(L)]; X=W[:,idx]
            aE=np.ones(len(W),bool)
            for d in E: aE&=~has_period(X,d)
            cov|=aE&~has_period(X,h) if (n%2==0) else aE
            if n%2==0 and l<=h:
                for e in (j,(j+l-1)%n):
                    cov|=aE&(W[:,e]!=W[:,(e+h)%n])
    return (not np.any(cov&~P)),(not np.any(P&~cov)),int((P&~cov).sum())
for n in range(6,21):
    print(n,run(n),flush=True)
