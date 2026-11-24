"""audit_r17: independent brute-force test of Lemma MS+ (r16_unbal) and the quadrant density.
Weights a=+1, b=-1 (scale irrelevant). A(k)=P(k), B(k)=P(n)-P(n-k), G- <=> A(k)<B(k) for 1<=k<=n//2.
Test 1 (b): for ALL middles M in {a,b}^m, W=pMq, W'=p alpha x beta M v q with x U-level (P_x>=-K), |x|>=n.
  Claim: W' in G-  ==>  B_W(k) >= -C_V for every 1<=k<=n//2, C_V = K+|p|+|alpha|+|v|+|q| (crude).
  We record the actual min over k<=n/2 of B_W(k) among W with W' in G-, and count violations.
Test 2 (a): mirror, W''= p u M beta' y alpha' q with y V-level; claim A_W(k) <= C_U.
Test 3: exact quadrant density n*2^-n|Q_n(C)| via product of 1-D ballot DPs, cross-checked by brute force n<=16.
"""
import itertools, random
def P(w):
    s=[0]
    for c in w: s.append(s[-1]+(1 if c=='a' else -1))
    return s
def AB(w):
    s=P(w); n=len(w)
    return [s[k] for k in range(n//2+1)], [s[n]-s[n-k] for k in range(n//2+1)]
def inG(w):
    A,B=AB(w); return all(A[k]<B[k] for k in range(1,len(w)//2+1))
def rw(L,rng): return ''.join(rng.choice('ab') for _ in range(L))
def ulevel(L,K,rng):
    s=0;out=[]
    for _ in range(L):
        c=rng.choice('ab')
        if c=='b' and s-1< -K: c='a'
        s+= 1 if c=='a' else -1; out.append(c)
    return ''.join(out)
def vlevel(L,K,rng):  # suffix excess <= K: reverse of a U-level word with letters swapped? suffix sums <=K
    x=ulevel(L,K,rng); return ''.join('a' if c=='b' else 'b' for c in reversed(x))
rng=random.Random(17)
viol=0; tested=0; worst=[]
for trial in range(300):
    p,q,al,be,v=(rw(rng.randint(0,3),rng) for _ in range(5))
    m=rng.randint(4,12); K=rng.randint(0,2)
    n=len(p)+m+len(q)
    x=ulevel(n+rng.randint(0,6),K,rng)
    CV=K+len(p)+len(al)+len(v)+len(q)
    mn=None
    for M in itertools.product('ab',repeat=m):
        M=''.join(M); W=p+M+q; W2=p+al+x+be+M+v+q
        if inG(W2):
            tested+=1
            b=min(AB(W)[1][1:n//2+1])
            mn=b if mn is None else min(mn,b)
            if b< -CV: viol+=1
    worst.append((mn,CV))
print("Test1 (b): words W with W' in G-:",tested,"violations of B_W>=-C_V:",viol)
print("  sample (min B over admissible W, C_V):",worst[:8])
viol=0; tested=0
for trial in range(300):
    p,q,al,be,u=(rw(rng.randint(0,3),rng) for _ in range(5))
    m=rng.randint(4,12); K=rng.randint(0,2)
    n=len(p)+m+len(q)
    y=vlevel(n+rng.randint(0,6),K,rng)
    CU=K+len(q)+len(al)+len(u)+len(p)
    for M in itertools.product('ab',repeat=m):
        M=''.join(M); W=p+M+q; W2=p+u+M+be+y+al+q
        if inG(W2):
            tested+=1
            a=max(AB(W)[0][1:n//2+1])
            if a> CU: viol+=1
print("Test2 (a): tested",tested,"violations of A_W<=C_U:",viol)
# Test 3 quadrant density
def surv(mm,C):  # P(max_{k<=mm} S_k <= C), +-1 walk
    d={0:1.0}
    for _ in range(mm):
        e={}
        for h,pr in d.items():
            for s in (1,-1):
                if h+s<=C: e[h+s]=e.get(h+s,0)+pr/2
        d=e
    return sum(d.values())
for n in (8,12,16):
    for C in (0,1):
        bf=sum(1 for w in itertools.product('ab',repeat=n) if (lambda A,B:max(A[1:])<=C and min(B[1:])>=-C)(*AB(''.join(w))))
        print(f"n={n} C={C} brute n*dens={n*bf/2**n:.4f} DP={n*surv(n//2,C)**2:.4f}")
for n in (256,1024,4096):
    print(f"n={n}: n*dens C=0 {n*surv(n//2,0)**2:.4f}  C=1 {n*surv(n//2,1)**2:.4f}  C=10 {n*surv(n//2,10)**2:.3f}  (C+1)^2-scaled C=10: {n*surv(n//2,10)**2/121:.4f}")
