"""U ∩ a^i b^j a^k b^l (i,j,k,l>=1): exponent set vs interval rule min_c m_c <= t <= max_c m_c."""
import numpy as np, sys
from lines import targets
NMAX=int(sys.argv[1]) if __name__=="__main__" else 0
def mvals(w):
    n=len(w); W=np.array(w,float); F=np.fft.rfft(W)
    conv=np.rint(np.fft.irfft(F*F,n=n)).astype(int); return int(W.sum())-conv
tot=inU=interval=disagree=0; gaps=[]
for n in range(8,NMAX+1):
    T=targets(n)
    for i in range(1,n):
        for j in range(1,n-i):
            for k in range(1,n-i-j):
                l=n-i-j-k
                w=[0]*i+[1]*j+[0]*k+[1]*l
                M=mvals(w); s=set(M.tolist())
                u=any(t in s for t in T)
                iv=any(M.min()<=t<=M.max() for t in T)
                tot+=1; inU+=u; interval+=iv
                if u!=iv:
                    disagree+=1
                    if len(gaps)<15: gaps.append((n,i,j,k,l,sorted(s),T))
print("words",tot,"inU",inU,"intervalrule",interval,"disagree",disagree)
for g in gaps: print(g)
