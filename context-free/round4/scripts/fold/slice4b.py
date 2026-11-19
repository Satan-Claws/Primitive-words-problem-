"""classify disagreements between U and the interval rule on a^i b^j a^k b^l"""
import numpy as np, sys, collections
from lines import targets
def mvals(w):
    n=len(w); W=np.array(w,float); F=np.fft.rfft(W)
    conv=np.rint(np.fft.irfft(F*F,n=n)).astype(int); return int(W.sum())-conv
NMAX=int(sys.argv[1]); cnt=collections.Counter(); ex=[]
for n in range(8,NMAX+1):
    T=targets(n)
    for i in range(1,n):
        for j in range(1,n-i):
            for k in range(1,n-i-j):
                l=n-i-j-k
                M=mvals([0]*i+[1]*j+[0]*k+[1]*l); s=set(M.tolist())
                u=any(t in s for t in T); iv=any(M.min()<=t<=M.max() for t in T)
                if u!=iv:
                    key=('i=k' if i==k else '')+('j=l' if j==l else '')
                    cnt[(key,u)]+=1
                    if key=='' and len(ex)<12: ex.append((n,i,j,k,l,sorted(s),T))
print(cnt)
for e in ex: print(e)
