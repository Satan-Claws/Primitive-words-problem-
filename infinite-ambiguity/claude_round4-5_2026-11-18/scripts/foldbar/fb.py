# foldbar: checks for pattern / window fold certificates. One core, < few minutes.
import itertools, sys
def prim(w):
    n=len(w)
    for d in range(1,n):
        if n%d==0 and w==w[d:]+w[:d]: return False
    return True
def rots(w): return [w[i:]+w[:i] for i in range(len(w))]
def folds(w):
    """all (type, start-letter, pairs, end-letter) for central axes of linear word w (rotation fixed)."""
    n=len(w); out=[]
    if n%2==0:
        m=n//2
        out.append(('E',None,[(w[j],w[n-1-j]) for j in range(m)],None))
        out.append(('V',w[0],[(w[j],w[n-j]) for j in range(1,m)],w[m]))
    else:
        h=(n-1)//2
        out.append(('O',w[0],[(w[j],w[n-j]) for j in range(1,h+1)],None))
    return out
def pattern(pairs):
    return ''.join('L' if a=='1' and b=='0' else 'R' for a,b in pairs if a!=b)
def piLL(pairs):
    p=pattern(pairs)
    cLL=sum(1 for i in range(len(p)-1) if p[i:i+2]=='LL')
    cRR=sum(1 for i in range(len(p)-1) if p[i:i+2]=='RR')
    return (cLL==1 and cRR==0) or (cRR==1 and cLL==0)
def Cr(f,r):
    typ,x,pairs,y=f
    if typ!='V' or x==y: return False
    m=len(pairs)+1; n=2*m
    if n<6*r+6: return False
    P=pairs[:r]  # pairs j=1..r  (pairs[j-1] = (w_j,w_{n-j}))
    for t in range(r+1,m-r):   # t in [r+1, m-r-1]
        if pairs[t-1]!=(x,x): continue
        ok=True
        for j in range(1,r+1):
            if pairs[t+j-1]!=P[j-1] or pairs[t-j-1]!=(P[j-1][1],P[j-1][0]): ok=False;break
        if ok: return False
    return True
def certified(w,test):
    return any(test(f) for v in rots(w) for f in folds(v))
if __name__=='__main__':
    mode=sys.argv[1]
    if mode=='sound':
        N=int(sys.argv[2])
        for n in range(2,N+1):
            bad={'LL':0,'C1':0,'C2':0}; cnt={'LL':0,'C1':0,'C2':0}
            for t in itertools.product('01',repeat=n):
                w=''.join(t)
                fs=folds(w)
                for name,test in (('LL',lambda f:piLL(f[2])),('C1',lambda f:Cr(f,1)),('C2',lambda f:Cr(f,2))):
                    if any(test(f) for f in fs):
                        cnt[name]+=1
                        if not prim(w): bad[name]+=1
            print(n,cnt,'nonprimitive accepted:',bad,flush=True)
    if mode=='cover':
        K=int(sys.argv[2])
        for k in range(0,K+1):
            tot=0; c={'LL':0,'C1':0,'C2':0,'any':0}
            for t in itertools.product('01',repeat=k):
                y=''.join(t); w='1'+y+'0'+y; tot+=1
                a=certified(w,lambda f:piLL(f[2])); b=certified(w,lambda f:Cr(f,1)); d=certified(w,lambda f:Cr(f,2))
                c['LL']+=a;c['C1']+=b;c['C2']+=d;c['any']+=(a or b or d)
            print(k,tot,c,flush=True)
