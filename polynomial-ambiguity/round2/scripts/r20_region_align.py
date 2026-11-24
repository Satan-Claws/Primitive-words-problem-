"""r20_region: (1) exhaustive check of Lemma U: G- = F_[1,n/2] cap b..a, G+ = F cap a..b;
(2) alignment of canonical-rotation maps (Lyndon b<a, argmin-T) with the G- rotation (argmax-T);
(3) fraction of Lyndon(b<a) words lying in G-, and in end-window E_h."""
import random, itertools, math
def d(w,k):
    n=len(w); return w[:k].count('a')-w[n-k:].count('a')
def inG(w,s=-1):
    return all((d(w,k)<0 if s<0 else d(w,k)>0) for k in range(1,len(w)//2+1))
def inF(w): return all(d(w,k)!=0 for k in range(1,len(w)//2+1))
def prim(w):
    n=len(w); return all(w!=w[p:]+w[:p] for p in range(1,n) if n%p==0)
# (1)
bad=0
for n in range(2,17):
    for t in itertools.product('ab',repeat=n):
        w=''.join(t)
        f=inF(w); g=inG(w); gp=inG(w,1)
        if g!=(f and w[0]=='b' and w[-1]=='a') or gp!=(f and w[0]=='a' and w[-1]=='b'): bad+=1
        if f and not prim(w): bad+=1
print("LemmaU+soundness failures n<=16:",bad)
# (2),(3)
def T(w):
    n=len(w);A=w.count('a');t=[0];c=0
    for i in range(n): c+=w[i]=='a'; t.append(n*c-(i+1)*A)
    return t[:n]
def lynstart(w):  # least rotation w.r.t. b<a  (swap letters, min)
    s=w.translate(str.maketrans('ab','ba')); n=len(w)
    return min(range(n),key=lambda i:(s+s)[i:i+n])
random.seed(1)
for n in [64,256,1024]:
    offs=[];inGm=0;inE=0;N=0;h=int(math.log(n)**2)
    for _ in range(1500 if n<1024 else 400):
        w=''.join(random.choice('ab') for _ in range(n))
        if not prim(w): continue
        t=T(w);M=max(t)
        am=[i for i in range(n) if t[i]==M]
        if len(am)!=1: continue
        r=am[0]; l=lynstart(w); N+=1
        offs.append(((l-r)%n)/n)
        v=w[l:]+w[:l]
        inGm+=inG(v); inE+=all(d(v,k)<0 for k in range(1,h+1))
    offs.sort(); ks=max(abs(offs[i]-(i+0.5)/len(offs)) for i in range(len(offs)))
    print(f"n={n} N={N} KS(offset Lyn-vs-argmaxT, uniform)={ks:.3f} P(Lyn rot in G-)={inGm/N:.3f} "
          f"P(Lyn rot in E_h,h={h})={inE/N:.3f} sqrt(n)*P(G-)={math.sqrt(n)*inGm/N:.2f}")
