"""R15-B check 1: exponents of stacked critical SCCs (Lemma ST).
Scaled series in x = 2z (so coefficient = |L_n| 2^{-n}).
 D  = 1 + (x^2/4) D^2                      critical nonlinear, exponent -3/2
 Y2 = 1 + (x^3/8) D Y2^2                   nonlinear on nonlinear: -1-1/4
 Y3 = 1 + (x^3/8) Y2 Y3^2                  third level: -1-1/8
 X  = 1 + (x/2) Y2 X                       LINEAR critical on Y2: coeff n^{-3/4}, mu = inf
 Xl = 1 + (x/2)(1/2... subcritical) check: linear with rho<1 keeps Y2 exponent.
Tree counts (= word counts for an unambiguous realisation)."""
import numpy as np
N=4096
def solve(rhs):
    y=np.zeros(N+1); 
    for n in range(N+1):
        y[n]=rhs(y,n)
    return y
def conv(a,b,n):  # [x^n] a*b using a[0..n], b[0..n]
    return np.dot(a[:n+1],b[n::-1])
def shift(n,k,f): return f(n-k) if n>=k else 0.0
D=np.zeros(N+1); Y2=np.zeros(N+1); Y3=np.zeros(N+1); X=np.zeros(N+1); Xs=np.zeros(N+1)
DY2=np.zeros(N+1)
for n in range(N+1):
    D[n]=(1.0 if n==0 else 0)+(conv(D,D,n-2)/4 if n>=2 else 0)
for n in range(N+1):
    Y2[n]=(1.0 if n==0 else 0)
    if n>=3:
        m=n-3; t=np.convolve(D[:m+1],np.convolve(Y2[:m+1],Y2[:m+1])[:m+1])[m]; Y2[n]+=t/8
for n in range(N+1):
    Y3[n]=(1.0 if n==0 else 0)
    if n>=3:
        m=n-3; t=np.convolve(Y2[:m+1],np.convolve(Y3[:m+1],Y3[:m+1])[:m+1])[m]; Y3[n]+=t/8
for n in range(N+1):
    X[n]=(1.0 if n==0 else 0)+(conv(Y2,X,n-1)/2 if n>=1 else 0)
    Xs[n]=(1.0 if n==0 else 0)+(conv(Y2,Xs,n-1)/4 if n>=1 else 0)   # subcritical linear (rho=1/2)
def locexp(c,name,target):
    out=[]
    for n in [256,512,1024,2048,4000]:
        # use even n and n/2 (D has parity); average neighbours
        a=c[n]+c[n+1] if n+1<=N else c[n]+c[n-1]; b=c[n//2]+c[n//2+1]
        out.append(np.log(a/b)/np.log(2))
    print(f"{name:28s} target {target:+.4f} local exps:", " ".join(f"{e:+.4f}" for e in out))
print("mu(D),mu(Y2),mu(Y3) partial sums at N:",D.sum(),Y2.sum(),Y3.sum(), "(limits 2,2,2 approached slowly)")
locexp(D,"D (bottom nonlinear)",-1.5)
locexp(Y2,"Y2 (nonlin over nonlin)",-1.25)
locexp(Y3,"Y3 (3 stacked nonlin)",-1.125)
locexp(X,"X (linear critical over Y2)",-0.75)
locexp(Xs,"Xs (linear subcritical/Y2)",-1.25)
cs=np.cumsum(X); print("renewal mass U(N)/N^{1/4}:"," ".join(f"{cs[n]/n**0.25:.3f}" for n in [256,1024,4096]))
