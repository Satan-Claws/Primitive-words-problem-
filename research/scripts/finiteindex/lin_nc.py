# Near-constant criterion (bounded L6) restricted to the LINEAR class:
# structures = chains of pairwise disjoint NESTED pairs (i1<i2<..<ik<jk<..<j1) + singletons elsewhere.
# Output: whether the coverer (linear sets) beats every near-constant delta.
import sys, itertools
from arr2 import Field, run, max_divs
def chains(n):
    out=[]
    def rec(lo,hi,cur):
        out.append(list(cur))
        for i in range(lo,hi+1):
            for j in range(i+1,hi+1):
                cur.append((i,j)); rec(i+1,j-1,cur); cur.pop()
    rec(0,n-1,[])
    res=[]
    for ch in out:
        used=set(x for p in ch for x in p)
        res.append(ch+[(k,) for k in range(n) if k not in used])
    return res
n=int(sys.argv[1]); p=2**61-1
F=Field(p); D=max_divs(n)
S=chains(n)
# order: big chains first
S.sort(key=lambda P:-sum(len(b)==2 for b in P))
ok,used,fam=run(F,n,D,S)
print(n,'structures',len(S),'coverer wins' if ok else 'ATTACKER SURVIVES', 'used',len(used))
if not ok:
    for U in list(fam.values())[:5]: print(' dim',len(U.basis),U.basis[:3])
