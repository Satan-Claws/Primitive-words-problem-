import random, sys
from certs import *
random.seed(1)
for n in [int(x) for x in sys.argv[1].split(',')]:
    T = int(sys.argv[2]); cnt = {k:0 for k in ('D','RD','GB','RGB','CFU','G','RG','ALL')}
    for _ in range(T):
        w = tuple(random.randint(0,1) for _ in range(n))
        r = {k: CERTS[k](w) for k in CERTS}
        r['CFU'] = r['D'] or r['GB'] or r['RD'] or r['RGB']; r['ALL'] = r['CFU'] or r['G'] or r['RG']
        for k in cnt: cnt[k] += r[k]
    print(n, ' '.join('%s:%.3f' % (k, cnt[k]/T) for k in cnt), flush=True)
