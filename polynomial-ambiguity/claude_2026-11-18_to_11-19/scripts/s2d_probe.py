"""S2D probe: direction-1 Ginsburg pumping obstruction on the devil region W_n.
For x in E_n ∩ W_n, test whether some non-crossing perfect matching J (periods e_i+e_j)
has x ∉ (span J + V_p) for every prime p | n.  If yes for every x, the obstruction gives nothing.
Usage: python3 s2d_probe.py n box samples"""
import sys, random, itertools
from fractions import Fraction
def rank(rows):
    M=[list(map(Fraction,r)) for r in rows]; r=0
    if not M: return 0
    m=len(M[0])
    for c in range(m):
        p=next((i for i in range(r,len(M)) if M[i][c]!=0),None)
        if p is None: continue
        M[r],M[p]=M[p],M[r]
        for i in range(len(M)):
            if i!=r and M[i][c]!=0:
                f=M[i][c]/M[r][c]; M[i]=[a-f*b for a,b in zip(M[i],M[r])]
        r+=1
    return r
def primes(n): return [p for p in range(2,n+1) if n%p==0 and all(p%q for q in range(2,p))]
def Vbasis(n,d): return [[1 if i%d==r else 0 for i in range(n)] for r in range(d)]
def nc_matchings(lst):
    if not lst: yield []; return
    a=lst[0]
    for k in range(1,len(lst),2):
        for L in nc_matchings(lst[1:k]):
            for R in nc_matchings(lst[k+1:]): yield [(a,lst[k])]+L+R
def periodic(x,d): return all(x[i]==x[(i+d)%len(x)] for i in range(len(x)))
def main():
    n=int(sys.argv[1]); box=int(sys.argv[2]); S=int(sys.argv[3]); random.seed(1)
    P=primes(n); Vs={p:Vbasis(n,n//p) for p in P}
    W=[v for p in P for v in Vs[p]]
    Ms=list(nc_matchings(list(range(n))))
    pre=[]
    for M in Ms:
        U=[[1 if i in e else 0 for i in range(n)] for e in M]
        pre.append((M,{p:(U+Vs[p],rank(U+Vs[p])) for p in P}))
    tested=0; fail=[]; cnt={}
    for _ in range(S):
        coef=[random.randint(0,box) for _ in W]
        x=[sum(c*v[i] for c,v in zip(coef,W)) for i in range(n)]
        if any(periodic(x,n//p) for p in P): continue
        tested+=1; ok=None
        for M,d in pre:
            if all(rank(B+[x])>r for B,r in d.values()): ok=M; break
        if ok is None: fail.append(x)
        else: cnt[str(ok)]=cnt.get(str(ok),0)+1
    print(f"n={n} matchings={len(Ms)} hard vectors tested={tested} unseparated={len(fail)}")
    for k,v in sorted(cnt.items(),key=lambda t:-t[1])[:3]: print(" first separating matching",k,v)
    for x in fail[:5]: print(" FAIL",x)
main()
