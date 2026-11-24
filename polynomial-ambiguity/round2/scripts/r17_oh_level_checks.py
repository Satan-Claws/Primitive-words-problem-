"""r17_oh_level checks: (1) MS^in bookkeeping; (2) exact DP for Lemma D density of S_n(M;C,a)."""
import random, numpy as np
D = {'a': 0.5, 'b': -0.5}
def prof(s):
    P=[0.0]
    for ch in s: P.append(P[-1]+D[ch])
    return P
def AB(W):
    P=prof(W); n=len(W)
    return (lambda k:P[k]), (lambda k:P[n]-P[n-k])
# (1) bookkeeping: W' = p U alpha x beta w v_rho V q with x V-level (suffix-flat) word; check
# B_{W'}(k) <= max_{j<=m}B_W(j) + c1 + K for m<=k<=m+c1+|x|, and A_{W'}=A_W on U range.
rnd=random.Random(17); viol=0; T=0
rw=lambda L:''.join(rnd.choice('ab') for _ in range(L))
for it in range(3000):
    p,U,w,V,q,al,be,vr=(rw(rnd.randint(0,L)) for L in (3,30,3,10,3,3,3,4))
    W=p+U+w+V+q; n=len(W); m=len(V+q)
    x=('ab'*(n+3))  # suffix excess of (ab)^k read from right: steps +1/2,-1/2 -> <= 1/2 =: K
    K=0.5
    W2=p+U+al+x+be+w+vr+V+q; n2=len(W2)
    A1,B1=AB(W); A2,B2=AB(W2)
    c1=len(vr+w+be); Hm=max(B1(j) for j in range(m+1))
    for k in range(1,len(p+U)+1):
        T+=1
        if A2(k)!=A1(k) or k>n2/2: viol+=1
        if m<=k<=m+c1+len(x) and B2(k)>Hm+c1/2+K+1e-9: viol+=1   # D(.)<=|.|/2
        if k<=m and B2(k)!=B1(k): viol+=1
print(f"(1) MS^in bookkeeping: {T} checks, {viol} violations")
# (2) exact density of S_n(M;C,a): integer steps +-1 (heights doubled), C,a in doubled units.
def ballot_max(T,gmax):
    # P(max_{k<=T} A <= g) for g=0..gmax, A simple +-1 walk
    out=[]
    for g in range(gmax+1):
        size=g+T+2; v=np.zeros(2*T+3); off=T+1; v[off]=1
        for _ in range(T):
            v=0.5*(np.roll(v,1)+np.roll(v,-1)); v[off+g+1:]=0
        out.append(v.sum())
    return np.array(out)
def dens(n,M,C=1,a=1):
    T=n//2; Hmax=M+1; off=C
    # state (b, h): b in [-C, M], h=max in [0, M]
    st=np.zeros((M+C+2, M+2)); st[off,0]=1
    for _ in range(M):
        new=np.zeros_like(st)
        # up
        new[1:,:]+=0.5*st[:-1,:]
        new[:-1,:]+=0.5*st[1:,:]
        new[0,:]=0  # b=-C-1 killed (index -1 rolled out) ; index0 is b=-C kept: recompute
        new[0,:]=0.5*st[1,:]
        # update max
        for b in range(1,M+C+2):
            hb=b-off
            if hb>0:
                row=new[b,:hb].sum(); new[b,:hb]=0; new[b,hb]+=row
        st=new
    # survival on remaining T-M steps from b
    R=T-M; L=M+C+R+3; v=np.zeros(L); 
    surv=np.zeros(M+C+2)
    # compute survival for each start via backward DP
    f=np.ones(L)  # f[b] = P(survive remaining) indexed b+C
    for _ in range(R):
        g=np.zeros(L); g[1:-1]=0.5*(f[2:]+f[:-2]); g[0]=0.5*f[1]; g[-1]=g[-2]; f=g
    pa=ballot_max(T, M+a+1)
    tot=0.0
    for b in range(M+C+2):
        for h in range(M+2):
            if st[b,h]>0: tot+=st[b,h]*f[b]*pa[min(h+a,len(pa)-1)]
    return tot
for n in (256,1024,4096):
    row=[]
    for M in (4,16,64):
        if M<=n//4:
            d=dens(n,M); row.append(f"M={M}: n*d/sqrt(M)={n*d/np.sqrt(M):.3f}")
    print(f"(2) n={n}: "+"; ".join(row))
