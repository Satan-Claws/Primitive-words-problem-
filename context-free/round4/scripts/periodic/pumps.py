# For w = a (a^m b)^k, enumerate pump decompositions w = x u y v z with |uyv|<=P, |uv|>=1,
# and classify those for which some x u^j y v^j z (0<=j<=J) is NON-primitive.
import sys
from common import primitive
from collections import Counter
m,k,P,J=map(int,sys.argv[1:5])
w='a'+('a'*m+'b')*k; n=len(w)
bad=Counter(); total=0; examples=[]
for s in range(n):
  for lu in range(0,P+1):
    for ly in range(0,P+1-lu):
      for lv in range(0,P+1-lu-ly):
        if lu+lv==0 or s+lu+ly+lv>n: continue
        x=w[:s];u=w[s:s+lu];y=w[s+lu:s+lu+ly];v=w[s+lu+ly:s+lu+ly+lv];z=w[s+lu+ly+lv:]
        total+=1
        js=[j for j in range(J+1) if not primitive(x+u*j+y+v*j+z)]
        if js:
          key=(u,v,tuple(js),'pos_in_first_block' if s<=m+1 else 'later')
          bad[(u,v,tuple(js))]+=1
          if len(examples)<15: examples.append((s,u,y,v,js,x+u*js[0]+y+v*js[0]+z))
print('w=',w,'n=',n,'decomps',total,'with a nonprimitive pump',sum(bad.values()))
for kk,c in sorted(bad.items(),key=lambda t:-t[1])[:25]: print(kk,c)
for e in examples: print(e)
