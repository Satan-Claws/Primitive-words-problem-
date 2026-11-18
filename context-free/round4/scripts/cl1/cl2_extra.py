import itertools
from cl2 import make_gen, in_cond, T
from refute import primitive, blocks
c0 = (0, 1, 3)
gen = make_gen(c0)
print('condition words by length <=14:', [len(gen(n)) for n in range(15)])
tot = 0
for n in range(1, 31):
    for w in gen(n):
        tot += 1; assert primitive(w), w
print('c0=(0,1,3): all', tot, 'words up to length 30 primitive')
# control: drop the e_1 - e_K term -> must contain powers
def bad(w):
    x = blocks(w); K = len(x) if x else 0
    if not x or K % 3 or K < 6: return False
    return all(x[i-1] - x[K-i] == c0[(i-1) % 3] - c0[(-i) % 3] for i in range(1, K+1))
ex = next(''.join(t) for n in range(1, 30) for t in itertools.product('ab', repeat=n) if bad(''.join(t)) and not primitive(''.join(t)))
print('control (no e1-eK term) contains power:', ex)
