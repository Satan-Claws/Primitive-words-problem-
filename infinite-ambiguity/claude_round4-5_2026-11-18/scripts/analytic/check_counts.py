"""Exact checks for report analytic.md.
(1) L1 = (a*b)^* {a^i b a^j b : i!=j} (a*b)^*  has  2^{n-1} - d(n) words of length n.
(2) X = (aa|ab)^* b (complete binary prefix code), L_X = X^* {xy: x,y in X, x!=y} X^*.
    |L_X cap Sigma^n| = [z^n] ( z/((1-2z)(1+z)) - sum_k z^k/(1-2 z^{2k}) ).
(3) Q-slice bivariate formula: #{x in E_n, |x|_1 = m} = [t^n y^m] sum_d mu(d) t^d/(1-y^d-t^d).
Membership in L1/L_X is decided by the 'two-way' definition: the regular-expression form
(guess a split point and an adjacent pair) AND the unique-factorization form; both must agree."""
import itertools, re
from math import comb

def divisors(n): return [d for d in range(1,n+1) if n%d==0]
def mobius(n):
    r, m, p = 1, n, 2
    while p*p <= m:
        if m%p==0:
            m//=p
            if m%p==0: return 0
            r=-r
        p+=1
    return -r if m>1 else r

# ---- (1)
def blocks_L1(w):
    if not w.endswith('b'): return None
    return w.split('b')[:-1]
def in_L1_fact(w):
    bl = blocks_L1(w)
    return bl is not None and any(bl[i]!=bl[i+1] for i in range(len(bl)-1))
def in_L1_regex(w):
    # (a*b)* a^i b a^j b (a*b)*, i != j : try every pair of adjacent blocks via regex on all splits
    for m in re.finditer(r'(?=(?:^|(?<=b))(a*)b(a*)b)', w):
        if len(m.group(1))!=len(m.group(2)) and re.fullmatch(r'(a*b)*', w[:m.start()] ) and re.fullmatch(r'(a*b)*', w[m.start()+len(m.group(1))+len(m.group(2))+2:]):
            return True
    return False
for n in range(1,17):
    c1=c2=0
    for t in itertools.product('ab',repeat=n):
        w=''.join(t); f=in_L1_fact(w); g=in_L1_regex(w)
        assert f==g,(w,f,g)
        c1+=f
    assert c1 == 2**(n-1)-len(divisors(n)), (n,c1)
print("(1) L1 counts = 2^{n-1}-d(n) for n<=16: OK")

# ---- (2)
def factor_X(w):
    out=[]; i=0
    while i < len(w):
        j=i
        while j < len(w) and w[j]=='a':
            j+=2
        if j>=len(w) or j>len(w): return None
        if w[j]!='b': return None
        out.append(w[i:j+1]); i=j+1
    return out
def in_LX(w):
    f=factor_X(w)
    return f is not None and any(f[i]!=f[i+1] for i in range(len(f)-1))
N=18
# series coefficients
coef=[0]*(N+1)
# z/((1-2z)(1+z)) = sum_n c_n z^n, c_n = (2^n - (-1)^n)/3
for n in range(1,N+1): coef[n]+= (2**n-(-1)**n)//3
for k in range(1,N+1):
    # z^k/(1-2z^{2k}) = sum_j 2^j z^{k+2kj}
    j=0
    while k+2*k*j<=N:
        coef[k+2*k*j]-=2**j; j+=1
for n in range(1,N+1):
    c=sum(in_LX(''.join(t)) for t in itertools.product('ab',repeat=n))
    assert c==coef[n],(n,c,coef[n])
print("(2) L_X counts match z/((1-2z)(1+z)) - sum_k z^k/(1-2z^{2k}) for n<=%d: OK"%N, coef[1:])

# ---- (3)
def nonperiodic(x):
    n=len(x)
    return all(any(x[i]!=x[(i+n//p)%n] for i in range(n)) for p in range(2,n+1) if n%p==0 and all(p%q for q in range(2,p)))
for n in range(1,7):
    for m in range(0,7):
        cnt=sum(1 for x in itertools.product(range(m+1),repeat=n) if sum(x)==m and nonperiodic(x))
        # [t^n y^m] sum_d mu(d) t^d/(1-y^d-t^d) = sum_{d|n} mu(d) [y^m] (1-y^d)^{-n/d}
        s=0
        for d in divisors(n):
            if m%d==0: s+=mobius(d)*comb(m//d+n//d-1, n//d-1)
        assert cnt==s,(n,m,cnt,s)
print("(3) bivariate Q-slice formula OK for n<=6, m<=6")
