# audit_t8: independent checks for r17_oh_level (Lemma L, MS^in, Lemma D). Integer steps a=+1, b=-1.
import itertools, random, math
import numpy as np
INF=10**9
# ---------- Test 1: Lemma L on all critical Polish grammars Y -> f Y^{k_f}, complete prefix codes depth<=3 ----------
def codes(depth):
    if depth==0: return [['']]
    out=[['']]
    for L in codes(depth-1):
        for R in codes(depth-1):
            out.append(['a'+x for x in L]+['b'+x for x in R])
    return out
def wd(w): return sum(1 if c=='a' else -1 for c in w)
def stats_word(w):
    P=0;mn=0
    for c in w: P+=1 if c=='a' else -1; mn=min(mn,P)
    S=0;mx=0
    for c in reversed(w): S+=1 if c=='a' else -1; mx=max(mx,S)
    return wd(w),-mn,mx   # D, depth, max suffix sum
def concat(t1,t2):  # dicts (D)->(mindepth) ; combine
    pass
def run_grammar(rules,LMAX):
    # dep[l][D]=min depth ; suf[l][D]=min max-suffix-sum, over words of L(Y) of length l
    dep=[dict() for _ in range(LMAX+1)]; suf=[dict() for _ in range(LMAX+1)]
    def comb(A,B,mode):  # A,B lists of dicts by length ; result dict by length
        R=[dict() for _ in range(LMAX+1)]
        for l1 in range(LMAX+1):
            for D1,v1 in A[l1].items():
                for l2 in range(LMAX+1-l1):
                    for D2,v2 in B[l2].items():
                        v=max(v1,v2-D1) if mode=='dep' else max(v2,D2+v1)
                        d=R[l1+l2]; k=D1+D2
                        if d.get(k,INF)>v: d[k]=v
        return R
    for it in range(LMAX+2):
        changed=False
        newdep=[dict() for _ in range(LMAX+1)]; newsuf=[dict() for _ in range(LMAX+1)]
        for f,k in rules:
            D,dp,sx=stats_word(f)
            Ad=[dict() for _ in range(LMAX+1)]; As=[dict() for _ in range(LMAX+1)]
            if len(f)<=LMAX: Ad[len(f)][D]=dp; As[len(f)][D]=sx
            for _ in range(k): Ad=comb(Ad,dep,'dep'); As=comb(As,suf,'suf')
            for l in range(LMAX+1):
                for D2,v in Ad[l].items():
                    if newdep[l].get(D2,INF)>v: newdep[l][D2]=v
                for D2,v in As[l].items():
                    if newsuf[l].get(D2,INF)>v: newsuf[l][D2]=v
        if newdep==dep and newsuf==suf: break
        dep,suf=newdep,newsuf
    return dep,suf
def test1(LMAX=26):
    allc=codes(3); seen=set(); n=0; bad=[]
    for C in allc:
        if len(C)>4: continue
        for ar in itertools.product(range(4),repeat=len(C)):
            if sum(2.0**-len(f)*(1-k) for f,k in zip(C,ar))!=0: continue
            if max(ar)<2: continue
            if 0 not in ar: continue
            key=tuple(sorted(zip(C,ar)))
            if key in seen: continue
            seen.add(key); n+=1
            dep,suf=run_grammar(list(zip(C,ar)),LMAX)
            lens=[l for l in range(LMAX//2,LMAX+1) if dep[l]]
            if not lens: continue
            md=max(min(dep[l].values()) for l in lens)   # worst over lengths of best U-level word
            ms=max(min(suf[l].values()) for l in lens)
            bad.append((md,ms,key))
    bad.sort(key=lambda t:-max(t[0],t[1]))
    print("Test1 critical nonlinear Polish grammars (|code|<=4, arity<=3):",n)
    print("  worst min-depth over lengths in [L/2,L]:",max(b[0] for b in bad),"; worst min-suffix-excess:",max(b[1] for b in bad))
    print("  top3:",[(b[0],b[1],b[2]) for b in bad[:3]])
# ---------- Test 2: MS^in bookkeeping, independent ----------
def rw(l): return ''.join(random.choice('ab') for _ in range(l))
def prefP(w):
    P=[0]
    for c in w: P.append(P[-1]+(1 if c=='a' else -1))
    return P
def vlevel(l,K):  # random word with all suffix sums <= K
    while True:
        out=[];S=0
        for _ in range(l):
            c=random.choice('ab'); s=S+(1 if c=='a' else -1)
            if s>K: c='b'; s=S-1
            out.append(c); S=s
        return ''.join(reversed(out))
def test2(T=4000):
    random.seed(1); checks=0; viol=0
    for _ in range(T):
        p,U,w,V,q,al,be,vr=[rw(random.randint(0,l)) for l in (2,14,2,10,2,2,2,3)]
        W=p+U+w+V+q; n=len(W)
        if n<2: continue
        K=random.randint(0,3); x=vlevel(random.randint(n,3*n+2),K)
        W2=p+U+al+x+be+w+vr+V+q; n2=len(W2)
        P=prefP(W); P2=prefP(W2); m=len(V+q)
        A=lambda k:P[k]; B=lambda k:P[n]-P[n-k]; A2=lambda k:P2[k]; B2=lambda k:P2[n2]-P2[n2-k]
        c1=len(vr+w+be); bar=max(B(j) for j in range(m+1))+c1+K
        for k in range(1,len(p+U)+1):
            checks+=1
            ok = (2*k<=n2) and A2(k)==A(k) and B2(k)<=bar
            if not ok: viol+=1
        # also the logical consequence: if W2 in G-, then A(k)<bar for k<=|pU|
        if all(A2(k)<B2(k) for k in range(1,n2//2+1)):
            for k in range(1,len(p+U)+1):
                checks+=1
                if not A(k)<bar: viol+=1
    print("Test2 MS^in: checks",checks,"violations",viol)
# ---------- Test 3: Lemma D exact density, S_n(M;C,a) ----------
def survT(T,dmax):  # S[d]=P(walk from height d never goes below 0 in T steps), d=0..dmax
    size=dmax+T+2; s=np.ones(size)
    for _ in range(T):
        ns=np.zeros(size); ns[1:-1]=0.5*(s[2:]+s[:-2]); ns[0]=0.5*s[1]; ns[-1]=s[-1]; s=ns
    return s[:dmax+1]
def densD(n,M,C,a):
    T=n//2; W=M+C
    st=np.zeros((W+1,M+1)); st[C,0]=1.0   # index bi = b+C
    for _ in range(M):
        nst=np.zeros_like(st)
        for d in (1,-1):
            for bi in range(W+1):
                nb=bi+d
                if nb<0 or nb>W: continue
                row=st[bi]
                if not row.any(): continue
                b=nb-C
                for h in range(M+1):
                    if row[h]==0: continue
                    nh=max(h,b)
                    if nh<=M: nst[nb,nh]+=0.5*row[h]
        st=nst
    SB=survT(T-M,W); SA=survT(T,M+a+1)
    return sum(st[bi,h]*SB[bi]*SA[h+a] for bi in range(W+1) for h in range(M+1) if st[bi,h])
def test3():
    print("Test3 Lemma D exact density (C=a=1): n*dens/sqrt(M), n*dens/M^0.75")
    for n in (256,1024,2048):
        row=[]
        for M in (4,16,64):
            d=densD(n,M,1,1); row.append((M,round(n*d/M**0.5,3),round(n*d/M**0.75,3)))
        print("  n=",n,row)
    print("Test3b growth with C=a (log-level constants): n=1024,M=16")
    for C in (1,4,8,16):
        d=densD(1024,16,C,C); print("   C=a=",C," n*dens=",round(1024*d,2))
if __name__=="__main__":
    test2(); test3(); test1()
