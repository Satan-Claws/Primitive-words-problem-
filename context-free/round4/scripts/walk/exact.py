# Exact count of |T(E')_n| (odd n), T(E') = Cyc(sigma(E')) u mirror.
# canonical words with D pieces, k of them with nonempty z: C(D,k) * N(k,m),
# m=(n-D)/2, N(k,m) = [y^m](C(y)-1)^k = (k/m) C(2m, m-k) (k>=1), N(0,m)=[m==0].
from math import comb, gamma
from fractions import Fraction
import sys
def N(k, m):
    if k == 0: return 1 if m == 0 else 0
    if m < k: return 0
    return k * comb(2*m, m-k) // m
def count(n):
    tot = Fraction(0)
    for D in range(1, n+1, 2):
        if (n - D) % 2: continue
        m = (n - D)//2
        for k in ((D-1)//2, (D+1)//2):
            if 0 <= k <= D:
                tot += Fraction(n, D) * comb(D, k) * N(k, m)
    return 2 * tot   # mirror
const = 2*(2/3.141592653589793)*2**-0.75*gamma(0.25)*2  # see report
for n in [int(x) for x in sys.argv[1:]]:
    c = count(n); assert c.denominator == 1
    d = float(c / 2**n)
    print(n, f"density={d:.5f}  density*n^(1/4)={d*n**0.25:.4f}  E'*n^(1/2)={(2*comb(n,(n-1)//2)/2**n)*n**0.5:.4f}")
