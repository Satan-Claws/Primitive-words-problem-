"""Bookkeeping check of Lemma MS^back (r17_oh_region §2): appending the token (alpha x beta, v_rho) innermost.
W = p U w V q ; W' = p U alpha x beta w v_rho V q.  Checks, for all admissible k:
  A_W'(k) = A_W(k)  (k <= |pU|),   B_W'(m0+|v_rho beta|+j) = B_W(m0) + wt(v_rho beta) + S_x(j)  (m0=|wVq|),
and that |x| >= n gives n'/2 >= |pU|."""
import random
wt=lambda s: sum(.5 if c=='a' else -.5 for c in s)
A=lambda W,k: wt(W[:k]); B=lambda W,k: wt(W[len(W)-k:])
rnd=lambda l: ''.join(random.choice('ab') for _ in range(l))
random.seed(17); bad=0
for _ in range(2000):
    p,U,w,V,q,al,be,vr=(rnd(random.randint(0,12)) for _ in range(8))
    W=p+U+w+V+q; n=len(W); x='ba'*(n+3); Wp=p+U+al+x+be+w+vr+V+q; m0=len(w+V+q)
    bad+= any(A(Wp,k)!=A(W,k) for k in range(len(p+U)+1))
    bad+= any(B(Wp,m0+len(vr+be)+j)!=B(W,m0)+wt(vr+be)+wt(x[len(x)-j:]) for j in range(len(x)+1))
    bad+= not (len(Wp)/2>=len(p+U))
print("violations:",bad,"of 2000 instances")
