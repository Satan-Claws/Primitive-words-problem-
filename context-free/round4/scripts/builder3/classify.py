# classify missed necklaces: Parikh, runs, block vectors, Hamming distance to nearest power, best periods
import sys
from math import gcd
def dist_power(w):
    n=len(w); best=(n,None)
    for d in range(1,n):
        if n%d: continue
        dd=0
        for r in range(d):
            col=[w[i] for i in range(r,n,d)]; o=sum(col); dd+=min(o,len(col)-o)
        if dd<best[0]: best=(dd,n//d)
    return best
def runs(w):
    n=len(w); st=next(i for i in range(n) if w[i]!=w[i-1]); v=w[st:]+w[:st]; R=[];i=0
    while i<n:
        j=i
        while j<n and v[j]==v[i]: j+=1
        R.append(j-i); i=j
    return R
def blocks(w,one):
    n=len(w); st=w.index(one); x=[];c=0
    for j in range(1,n+1):
        if w[(st+j)%n]==one: x.append(c); c=0
        else: c+=1
    return x
for fn in sys.argv[1:]:
    for line in open(fn):
        s=line.strip(); w=[0 if ch=='a' else 1 for ch in s]; n=len(w); b=sum(w)
        ms=[sum(1 for i in range(n) if w[i]==1 and w[(c-i)%n]==0) for c in range(n)]
        dp=dist_power(w)
        print(n, s, 'A,B=%d,%d'%(n-b,b), 'K=%d'%len(runs(w)), 'runs=',runs(w), 'bv_b=',blocks(w,1),'distPow=%d(p=%s)'%dp, 'min m_c=%d'%min(ms))
