# literal construction: sigma(E') by direct generation, all rotations, swap; compare with decode test
import itertools,sys
from brute import inT, sw
N=int(sys.argv[1])
def dyck_nonempty(maxlen):
    # z in B nonempty: prefix sums <=0, total 0, b=-1
    res=[]
    for L in range(2,maxlen+1,2):
        for t in itertools.product('ab',repeat=L):
            s=0;ok=True
            for c in t:
                s+= 1 if c=='a' else -1
                if s>0: ok=False;break
            if ok and s==0: res.append(''.join(t))
    return res
Z=dyck_nonempty(N)
sig={'a':['a'],'b':[z+'a' for z in Z]}
words=set()
def gen(v,i,acc):
    if len(acc)>N: return
    if i==len(v):
        words.add(acc); return
    for p in sig[v[i]]:
        if len(acc)+len(p)<=N: gen(v,i+1,acc+p)
for D in range(1,N+1):
    for t in itertools.product('ab',repeat=D):
        v=''.join(t)
        if abs(v.count('a')-v.count('b'))==1: gen(v,0,'')
T=set()
for w in words:
    for i in range(len(w)):
        r=w[i:]+w[:i]; T.add(r); T.add(sw(r))
for n in range(1,N+1):
    lit={w for w in T if len(w)==n}
    test={''.join(t) for t in itertools.product('ab',repeat=n) if inT(''.join(t),1)}
    print(n,len(lit),len(test),lit==test)
