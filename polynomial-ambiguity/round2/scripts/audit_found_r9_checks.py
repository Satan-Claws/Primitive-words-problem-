"""audit_found_r9: sanity checks for r9 Thm M / Lemma F / Lemma Rn foundations."""
from fractions import Fraction as Fr
import itertools, math
# 1. |G-_n|/2^n -> 0 (DP on pair walk), and Safe-style count vs 2^n/n
def gminus(n):
    m=n//2; cnt={0:1}
    for k in range(m):
        new={}
        for d,c in cnt.items():
            for inc,mult in ((0,2),(1,1),(-1,1)):
                e=d+inc
                if e<0: new[e]=new.get(e,0)+c*mult
        cnt=new
    return sum(cnt.values())*2**(n-2*m)
for n in (10,100,400): print("G-",n, gminus(n)/2**n, "x sqrt(n)=",gminus(n)/2**n*math.sqrt(n))
# 2. Lemma F(a) elementary bound: nonlinear SCC Y -> a Y Y | b (critical at z=1/2: y=z+z y^2 -> y(1/2)=1) finite
z=0.5; y=0.0
for _ in range(200000): y=z+z*y*y
print("nonlinear SCC value at 1/2:",y,"(finite, <= 1/c with c=z)")
# 3. Lemma Rn: brute-force injectivity + first-return weight for linear SCC X->aX|bY, Y->aX|bbY|abY|b (irreducible)
rules={'X':[('a','X'),('b','Y')],'Y':[('a','X'),('bb','Y'),('ab','Y')]}
def M(z): return [[z,z],[z,z**2+z**2]]
import numpy as np
Mh=np.array(M(0.5)); print("rho(M(1/2)) =",max(abs(np.linalg.eigvals(Mh))))
# first-return weight to X: F = M_XX + M_XY (1-M_YY)^-1 M_YX
F=Mh[0,0]+Mh[0,1]*Mh[1,0]/(1-Mh[1,1]); print("first-return total weight F_XX =",F)
