"""Checks for the non-CF proof of Phi_R = {w : |w| - 4 m(w) = R}, m = # mismatched central mirror pairs.
(1) on a^i b^j a^k: m = min(j, |i-k|)   (2) stratified candidate periods and their pairwise cones.
(3) the even-linear barrier walk: P(SRW stays in [-K,K] for h steps)."""
import itertools, numpy as np
def m_central(w):
    n=len(w); return sum(1 for t in range(n//2) if w[t]!=w[n-1-t])
bad=0
for i in range(0,14):
    for j in range(0,14):
        for k in range(0,14):
            w='a'*i+'b'*j+'a'*k
            if m_central(w)!=min(j,abs(i-k)): bad+=1
print("slice formula mismatches:",bad)
f=lambda d: d[0]+d[1]+d[2]-4*min(d[1],abs(d[0]-d[2]))
# all nonneg integer vectors with support<=2, entries<=12, f=0
cands=set()
for d in itertools.product(range(13),repeat=3):
    if sum(1 for x in d if x)<=2 and any(d) and f(d)==0:
        g=np.gcd.reduce(d); cands.add(tuple(x//g for x in d))
print("primitive support<=2 directions with f=0:",sorted(cands))
for u,v in itertools.combinations(sorted(cands),2):
    zero=all(f(tuple(x*a+y*b for a,b in zip(u,v)))==0 for x in range(0,6) for y in range(0,6))
    wit=[(x,y) for x in range(1,6) for y in range(1,6) if f(tuple(x*a+y*b for a,b in zip(u,v)))!=0][:1]
    print(u,v,"f==0 on cone:",zero,"witness",wit)
# level counts of E_R at N
for R in (1,-1,2,0):
    print("R",R,[sum(1 for i in range(N+1) for j in range(N+1-i) if f((i,j,N-i-j))==R) for N in range(40,49)])
