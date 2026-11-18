# Real R6 words over {a,b}: z_i in a(ab+)+. Check: primitive  <=> (count cert or nested pattern), length <= N.
import sys, itertools
from cover3lib import startmis, endmis, per
from exhaust_lib import covered
N=int(sys.argv[1])
def segs(maxlen):
    out=[]
    def rec(s):
        if len(s)>maxlen: return
        if len(s)>=3: out.append(s)
        for x in range(1,maxlen):
            t=s+'a'+'b'*x
            if len(t)>maxlen: break
            rec(t)
    rec('a'); return out
S=segs(N-15)
byl={}
for s in S: byl.setdefault(len(s),[]).append(s)
def isprim(w):
    n=len(w); return all(not(n%d==0 and w==w[:d]*(n//d)) for d in range(1,n))
cnt=bad=0
def rec(pref,used):
    global cnt,bad
    if len(pref)==6:
        w=''.join(pref); p=isprim(w); z=tuple(pref)
        c = (not per([x.count('b') for x in z])) or (not per([x.count('a') for x in z])) or covered(z,0)
        cnt+=1
        if p!=c: bad+=1; print("MISMATCH",z,p,c)
        return
    for s in S:
        if used+len(s)+3*(5-len(pref))<=N: rec(pref+[s],used+len(s))
rec([],0)
print("words",cnt,"mismatches",bad)
