import sys
from mu import mu_le, prim
n, extra = int(sys.argv[1]), int(sys.argv[2])
for k in range(2 ** (n - 1)):
    w = 'a' + format(k, '0%db' % (n - 1)).replace('0', 'a').replace('1', 'b')
    if not prim(w): continue
    if mu_le(w, 1, n + extra)[0] or mu_le(w, 2, n + extra)[0]: continue
    ok, wit = mu_le(w, 3, n + extra)
    print(w, 'mu<=3' if ok else 'mu>3', wit, flush=True)
