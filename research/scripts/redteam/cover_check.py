# Redteam: build the 2*ceil(n/3) rectangles R_{j,c} of rectangles Thm A(2) explicitly and verify
# (i) each rectangle is inside Q_n (direct string primitivity test), (ii) union = Q_n.
# Also Prop 2.8: pi onto Sigma^s for even n; and R4 (devil) first-letter cover.
import sys
from rt_common import *
N=int(sys.argv[1]) if len(sys.argv)>1 else 16
for n in range(2,N+1):
    L=(2*n)//3; s=n-L
    prim=[is_primitive_str(to_str(w,n)) for w in range(1<<n)]
    pi={}
    for w in range(1<<n):
        if not prim[w]:
            y=w&((1<<L)-1); z=w>>L
            assert y not in pi or pi[y]==z
            pi[y]=z
    covered=[False]*(1<<n)
    for j in range(s):
        for c in (0,1):
            rows=[y for y in range(1<<L) if (y not in pi) or (((pi[y]>>j)&1)!=c)]
            cols=[z for z in range(1<<s) if ((z>>j)&1)==c]
            for y in rows:
                for z in cols:
                    w=y|(z<<L)
                    assert prim[w],(n,j,c)
                    covered[w]=True
    assert all(covered[w]==prim[w] for w in range(1<<n))
    onto = (len(set(pi.values()))==(1<<s))
    # devil R4: m=ceil(n/3); for every primitive w exists k<m s.t. all u c z v (|u|=k, c=w_k, z free len m-1) primitive
    m=-(-n//3); okR4=True
    for w in range(1<<n):
        if not prim[w]: continue
        good=False
        for k in range(m):
            base=w & ~(((1<<(m-1))-1)<<(k+1))
            if all(prim[base | (z<<(k+1))] for z in range(1<<(m-1))): good=True;break
        if not good: okR4=False;break
    print(n,'rects',2*s,'cover ok','pi onto' if onto else 'pi NOT onto','R4',okR4)
    assert okR4
