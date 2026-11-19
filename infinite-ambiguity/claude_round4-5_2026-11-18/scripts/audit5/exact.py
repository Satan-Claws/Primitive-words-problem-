# audit5: exact counts of T^k(E') via the (length, #b) recursion; independent of walk's scripts
from math import comb, lgamma, log, exp, gamma, pi
from fractions import Fraction
import sys
def N(k,m):
    if k==0: return 1 if m==0 else 0
    if m<k: return 0
    return k*comb(2*m,m-k)//m
def T_counts(B, Nmax):
    """B[(D,j)] = #words of M of length D with j b's (M rotation-closed). returns same for T(M)."""
    out={}
    byD={}
    for (D,j),c in B.items(): byD.setdefault(D,[]).append((j,c))
    for n in range(1,Nmax+1):
        for D,lst in byD.items():
            if D<1 or D>n or (n-D)%2: continue
            m=(n-D)//2
            s=sum(c*N(j,m) for j,c in lst)
            assert (n*s)%D==0
            c=n*s//D
            if c:
                out[(n,m)]=out.get((n,m),0)+c          # delta=+D: #b=m
                out[(n,n-m)]=out.get((n,n-m),0)+c      # swapped
    return out
if __name__=='__main__':
    Nmax=int(sys.argv[1])
    E={}
    for D in range(1,Nmax+1):
        for j in range(D+1):
            if abs(D-2*j)==1: E[(D,j)]=comb(D,j)
    cur=E; levels=[E]
    for k in range(3):
        cur=T_counts(cur,Nmax); levels.append(cur)
    for n in range(1,Nmax+1,2):
        print(n,[round(sum(c for (L,j),c in lv.items() if L==n)/2**n,4) for lv in levels])
