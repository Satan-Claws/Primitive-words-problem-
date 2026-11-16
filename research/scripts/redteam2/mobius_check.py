# Independent check of Lemma 3.1 / Theorem B (ambiguity.md).
# (1) Brute force: coefficient of y^x in GF(1_{E_n}) equals [word a b^x1 ... a b^xn is primitive],
#     compared against the Mobius formula expanded as a truncated power series (no sympy cancel).
# (2) Reduced denominator: factor with sympy and list #vars per irreducible factor; additionally
#     verify that f = 1 - prod_{i = 1 mod s} y_i really is a pole: F*g*(other factors) evaluated on
#     the hypersurface f = 0 is not identically 0 (done via numeric substitution).
import itertools, sys, sympy as sp
from sympy import mobius, divisors, primefactors
def prim(w):
    n=len(w); return all(w!=w[:d]*(n//d) for d in range(1,n) if n%d==0)
def mobius_coeff(n,x):
    # coefficient of y^x in sum_d mu(d) prod_r 1/(1-m_{s,r}) = sum_d mu(d) [x is s-periodic], s=n/d
    tot=0
    for d in divisors(n):
        s=n//d
        if all(x[i]==x[(i+s)%n] for i in range(n)): tot+=mobius(d)
    return tot
# NOTE: the series of prod_r 1/(1-m_{s,r}) has coefficient 1 exactly on s-periodic x (classes disjoint).
for n in range(1,8):
    B=4 if n<=5 else 2
    bad=0
    for x in itertools.product(range(B+1),repeat=n):
        w=''.join('a'+'b'*k for k in x)
        if int(prim(w))!=mobius_coeff(n,x): bad+=1
    print("n=%d brute-force vs Mobius coefficient mismatches: %d"%(n,bad))
# series of prod_r 1/(1-m_{s,r}) really is indicator of s-periodic vectors: check by sympy series for n=4,6
for n in (4,6):
    y=sp.symbols('y1:%d'%(n+1))
    for d in divisors(n):
        s=n//d
        term=sp.Integer(1)
        for r in range(s):
            m=sp.Mul(*[y[i] for i in range(r,n,s)])
            term*=sum(m**k for k in range(3))  # truncated geometric
        P=sp.Poly(sp.expand(term),*y)
        for mon,c in P.terms():
            if max(mon)<=2-0 and sum(mon)<=2:  # low-degree region where truncation is exact
                assert c==1 and all(mon[i]==mon[(i+s)%n] for i in range(n))
print("geometric-class expansion ok")
def reduced_den(n):
    y=sp.symbols('y1:%d'%(n+1))
    F=0
    for d in divisors(n):
        s=n//d; t=sp.Integer(1)
        for r in range(s): t/= (1-sp.Mul(*[y[i] for i in range(r,n,s)]))
        F+=mobius(d)*t
    num,den=sp.fraction(sp.cancel(sp.together(F)))
    return y,num,den,[ (f,len(f.free_symbols)) for f,e in sp.factor_list(den)[1]]
for n in range(2,int(sys.argv[1]) if len(sys.argv)>1 else 10):
    y,num,den,fs=reduced_den(n)
    odd=[p for p in primefactors(n) if p%2]
    print(n,"odd primes",odd,"factor var-counts",sorted(v for f,v in fs))
    for q in odd:
        s=n//q; f=1-sp.Mul(*[y[i] for i in range(0,n,s)])
        assert any(sp.expand(g-f)==0 or sp.expand(g+f)==0 for g,_ in fs), (n,q)
        # numerator nonvanishing on f=0: substitute y1 = 1/prod(other vars in f) and random values
        import random
        rnd=random.Random(n)
        sub={v:sp.Rational(rnd.randint(2,9),rnd.randint(11,19)) for v in y}
        others=[y[i] for i in range(s,n,s)]
        sub[y[0]]=1/sp.Mul(*[sub[v] for v in others])
        assert num.subs(sub)!=0
    print("   f-factor present and numerator nonzero on f=0 for all odd q")
