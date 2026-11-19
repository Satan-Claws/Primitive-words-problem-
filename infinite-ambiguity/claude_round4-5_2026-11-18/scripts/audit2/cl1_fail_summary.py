exec(open('cl1_crossing_audit.py').read().split('# cyclic closure')[0].replace("print('cl1","pass#"))
def incyc(w,f): return any(f(w[r:]+w[:r]) for r in range(len(w)))
from collections import Counter
C=Counter()
for i in range(0,5):
  for j in range(0,5):
    for u in (['a'*i+'b'] if j==0 else []) + ['a'*i+'b'+'a'*j+'b']:
      for k in range(2,5):
        p=u*k
        for pos in range(len(p)+1):
            w=p[:pos]+'a'+p[pos:]
            if not incyc(w,inLgen): C[(u,k)]+=1
print(sorted(C.items())[:40]); print(len(C))
