# Check classification: w=a(a^m b)^k, all decompositions with |uyv|<=m, exponents j=0..J.
# Predicted non-primitive cases: (A) uv = 'a' (total one letter a, no b), j=0, inside block 0;
# (A') uv='a', j=2, inside block k/2 (k even); (B) uv has one b and m-1 a's, j=0, merge yields
# block sequence periodic. Prints any case outside A/A'/B and the B cases found.
import sys
from common import primitive
def blocks(t):  # t ends with b
    return [len(s) for s in t.split('b')[:-1]]
for m in range(3,8):
  for k in range(4,9):
    w='a'+('a'*m+'b')*k; n=len(w); other=[]; Bc=0
    for s in range(n):
     for lu in range(m+1):
      for ly in range(m+1-lu):
       for lv in range(m+1-lu-ly):
        if lu+lv==0 or s+lu+ly+lv>n: continue
        x=w[:s];u=w[s:s+lu];y=w[s+lu:s+lu+ly];v=w[s+lu+ly:s+lu+ly+lv];z=w[s+lu+ly+lv:]
        for j in range(0,7):
          t=x+u*j+y+v*j+z
          if primitive(t): continue
          uv=u+v
          if uv=='a' and j in (0,2): continue
          if uv.count('b')==1 and uv.count('a')==m-1 and j==0: Bc+=1; continue
          other.append((s,u,y,v,j))
    print(m,k,'B-type',Bc,'unexplained',other[:3],len(other))
