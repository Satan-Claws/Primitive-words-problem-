import sys
from cover_r6 import *
lo,hi=int(sys.argv[1]),int(sys.argv[2])
def segs(l):
    out=[]
    def rec(s,rem):
        if rem==0 and len(s)>1: out.append(s); return
        for k in range(1,rem):
            rec(s+'a'+'b'*k,rem-1-k)
    rec('a',l-1); return out
allseg=[]
for l in range(3,hi-15+1): allseg+=segs(l)
tab=T(allseg)
A=[s.count('a') for s in allseg]; Bc=[s.count('b') for s in allseg]; L=[len(s) for s in allseg]
bylen={}
for i,s in enumerate(allseg): bylen.setdefault(len(s),[]).append(i)
cnt=0; checked=0; bad=0
idx=[0]*6
def rec(k,used):
    global cnt,checked,bad
    if k==6:
        if used<lo: return
        cnt+=1
        a=[A[i] for i in idx]; b=[Bc[i] for i in idx]
        if not(per(a) and per(b)): return
        if not prim(idx): return
        checked+=1
        if not Ncover(tab,idx):
            bad+=1; print('UNCOVERED',[allseg[i] for i in idx],flush=True)
        return
    rem=6-k-1
    for l in range(3,hi-used-3*rem+1):
        for i in bylen.get(l,[]):
            idx[k]=i; rec(k+1,used+l)
rec(0,0)
print('words',cnt,'count-periodic primitive checked',checked,'uncovered',bad)
