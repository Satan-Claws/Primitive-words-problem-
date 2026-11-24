# r7_lemmaQ_rect.py: centre rectangles X x Y in G^- (|x|=|y|=N).  X x Y in G^- iff exists barrier g with
# X <= {F_x(k) <= g(k)}, Y <= {R_y(k) > g(k)}  (F = #a prefix of x, R = #a suffix of y).  Max rectangle = max_g P(F<=g)P(R>g).
# Evaluate for g(k) = k/2 + lam*sqrt(k) and fit exponent in N.
import numpy as np, math
def stay(N,g,below=True):
    p=np.zeros(N+2); p[0]=1.0
    for k in range(1,N+1):
        q=np.zeros(N+2); q[:]=0.5*p; q[1:]+=0.5*p[:-1]; p=q
        idx=np.arange(N+2)
        p[(idx>g(k)) if below else (idx<=g(k))]=0
    return p.sum()
for lam in [-1.0,-0.5,-0.25,0.0,0.25,0.5,1.0]:
    vals=[]
    for N in [500,2000]:
        g=lambda k: min(k-1,max(0,math.floor(k/2+lam*math.sqrt(k))))
        vals.append(stay(N,g,True)*stay(N,g,False))
    e=math.log(vals[1]/vals[0])/math.log(4)
    print(f"lam={lam:5.2f} prod(N=2000)={vals[1]:.2e} exponent={e:.3f}")
