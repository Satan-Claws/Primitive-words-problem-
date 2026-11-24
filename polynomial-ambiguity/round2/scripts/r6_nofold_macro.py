# r6_nofold Prop S (MC): macroscopic pump-down of words in G^-. Sample w in G^- (rejection from a meander-biased start),
# delete v=w[m,m+r) (left half) and y=w[m2,m2+r2) (right half), r,r2 = Theta(n); report P(ux z in G^-), and P for
# pump-up i=2 (u v v x y y z).  Fast d via prefix sums.
import random, sys
def inG(w):
    n=len(w); A=[0]
    for c in w: A.append(A[-1]+(c=='a'))
    return all(A[k]-(A[n]-A[n-k])<0 for k in range(1,n//2+1))
random.seed(1); n=int(sys.argv[1]) if len(sys.argv)>1 else 400
S=[]; 
while len(S)<400:
    w=''.join(random.choice('ab') for _ in range(n))
    w='b'+w[1:-1]+'a'
    if inG(w): S.append(w)
for (fr,fr2) in [(0.2,0.0),(0.2,0.2),(0.2,0.1),(0.05,0.15)]:
    dn=up=0
    for w in S:
        r=int(fr*n); r2=int(fr2*n)
        m=random.randint(n//10,n//2-r); m2=random.randint(n//2,n-n//10-r2)
        v,y=w[m:m+r],w[m2:m2+r2]
        dn+=inG(w[:m]+w[m+r:m2]+w[m2+r2:]); up+=inG(w[:m]+v+w[m:m2]+y+w[m2:])
    print(f'|v|={fr}n |y|={fr2}n  P(pump down in G-)={dn/len(S):.2f}  P(pump up i=2 in G-)={up/len(S):.2f}')
