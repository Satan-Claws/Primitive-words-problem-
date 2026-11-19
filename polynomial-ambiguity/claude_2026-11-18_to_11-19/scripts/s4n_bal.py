from itertools import product
def prim(w):
    n=len(w); return all(not(n%d==0 and w==w[:d]*(n//d)) for d in range(1,n))
def pieces(w):
    h=[0];
    for c in w: h.append(h[-1]+(1 if c=='a' else -1))
    m=min(h[:-1]); i=h.index(m); r=w[i:]+w[:i]
    cuts=[j for j in range(len(r)) if sum(1 if c=='a' else -1 for c in r[:j])==0]+[len(r)]
    return tuple(r[cuts[k]:cuts[k+1]] for k in range(len(cuts)-1))
def neckprim(s): return prim(list(s)) if True else 0
bad=0;cnt=0
for n in range(2,17,2):
  for t in product('ab',repeat=n):
    w=''.join(t)
    if w.count('a')!=n//2: continue
    p=pieces(w); cnt+=1
    assert all(x[0]=='a' and x[-1]=='b' for x in p)
    if prim(w)!=prim(list(p)): bad+=1
print('balanced words',cnt,'mismatch',bad)
s={'x':'ab','y':'aabb'};bad=0
for n in range(1,15):
  for t in product('xy',repeat=n):
    if prim(t)!=prim(''.join(s[c] for c in t)): bad+=1
print('sigma mismatch',bad)
