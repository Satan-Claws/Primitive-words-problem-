"""T = {1 y 0 y} (binary, letters a=0,b=1 mapped to 'a','b'): Hamming-1 neighbours of squares.
(1) check primitivity of all members up to |y| = 9; (2) fraction covered by builder's letter-level dominance
Cyc(L(S)) (either letter order); (3) check the code reduction phi: 0->ab, 1->aab maps 1y0y to a.u.u (u = phi(0y))."""
import itertools, random
from dom import cycdom_rev
from refute import primitive
phi = {'0': 'ab', '1': 'aab'}
tot = cov = 0
for n in range(0, 10):
    for y in itertools.product('01', repeat=n):
        y = ''.join(y); x = '1' + y + '0' + y
        assert primitive(x)
        u = ''.join(phi[c] for c in '0' + y)
        assert ''.join(phi[c] for c in x) == 'a' + u + u
        if n <= 9:
            tot += 1; cov += cycdom_rev(x.replace('0', 'a').replace('1', 'b'))
print(f'T members |y|<=9: {tot}, all primitive, phi(1y0y)=a.u.u verified; dominance covers {cov}/{tot}')
rnd = random.Random(3)
for n in (20, 40):
    c = sum(cycdom_rev(('1' + y + '0' + y).replace('0','a').replace('1','b'))
            for y in (''.join(rnd.choice('01') for _ in range(n)) for _ in range(300)))
    print(f'|y|={n}: dominance covers {c}/300')
