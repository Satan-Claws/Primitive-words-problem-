"""Probe: which members a.u.u of J (u in (a*b)^+) are covered by builder's letter-level dominance Cyc(L(S))
and by Cyc(L_l) for small l."""
import random
from dom import cycdom
from cl3 import covered
from refute import blocks
rnd = random.Random(7)
stats = {}
for nb in range(2, 11):
    miss_dom = miss_all = 0; N = 200
    for _ in range(N):
        c = [rnd.randint(0, 8) for _ in range(nb)]
        u = ''.join('a'*v + 'b' for v in c); w = 'a' + u + u
        d = cycdom(w); x = blocks(w)
        cl = any(covered(l, x) for l in range(1, 5))
        miss_dom += not d; miss_all += not (d or cl)
    print(f'blocks/period={nb}: missed by dominance {miss_dom}/{N}; missed by dominance and L_1..L_4: {miss_all}/{N}')
