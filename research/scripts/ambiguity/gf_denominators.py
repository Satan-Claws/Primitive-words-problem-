# Checks: reduced denominator of GF(1_{E_n}) = sum_{d|n} mu(d) prod_{r mod n/d} 1/(1 - prod_{i=r mod n/d} y_i)
# Reports the number of variables of each irreducible factor of the reduced denominator.
import sympy as sp, sys
from sympy import mobius, divisors
def check(n):
    y = sp.symbols('y0:%d' % n)
    F = 0
    for d in divisors(n):
        s = n // d
        term = sp.Integer(1)
        for r in range(s):
            term *= 1/(1 - sp.Mul(*[y[i] for i in range(r, n, s)]))
        F += mobius(d) * term
    F = sp.cancel(sp.together(F))
    num, den = sp.fraction(F)
    facs = sp.factor_list(den)[1]
    nv = sorted(len(f.free_symbols) for f, e in facs)
    return max(nv), nv
for n in range(2, int(sys.argv[1]) + 1):
    mx, nv = check(n)
    print(n, "max vars in an irreducible denominator factor:", mx, "| odd prime factor:", any(p % 2 for p in sp.primefactors(n)))
