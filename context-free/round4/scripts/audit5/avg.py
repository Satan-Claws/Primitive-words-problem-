# audit5: compare dens_{T(M)}(n) with the outline's prediction E[dens_M(|Delta_n|)]
import sys
from math import lgamma, log, exp, sqrt
from flt import F
k=int(sys.argv[1])
for n in map(int,sys.argv[2:]):
    pred=0.0
    for D in range(1,min(n,int(12*sqrt(n)))+1,2):
        p=2*exp(lgamma(n+1)-lgamma((n-D)//2+1)-lgamma((n+D)//2+1)-n*log(2))
        pred+=p*sum(F(k-1,D))
    print(k,n,'actual',round(sum(F(k,n)),4),'E[dens_M(|Delta|)]',round(pred,4))
