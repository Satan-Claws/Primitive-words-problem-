import sys, time
from freeloops import minW, prim
def tm(n):
    return ''.join('ab'[bin(i).count('1') % 2] for i in range(n))
m, R, Lmax = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
for n in range(12, 33, 4):
    w = tm(n)
    if not prim(w): print(n, 'nonprim'); continue
    for s in [n // 2 - 4, 2]:
        D = set(range(s, s + 8))
        t = time.time()
        print(n, w, 'D', s, minW(w, D, m, R, 8, Lmax), round(time.time() - t, 1), flush=True)
