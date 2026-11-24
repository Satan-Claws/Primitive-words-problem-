"""construct36_cover.py -- coverage of all primitive x in W_36 ∩ N^36 with |x|_1 <= N (up to D_36) by
(i) chord-dominance systems k<=2, (ii) + transfer atoms.  usage: python construct36_cover.py N"""
import sys, time, numpy as np, construct36_core as C
N = int(sys.argv[1]); t = time.time()
tot, cl = C.enumerate_W36(N)
print(f'N={N}: primitive points {tot}, D_36 classes {len(cl)}  ({time.time()-t:.0f}s)', flush=True)
res = {}; unc = []; cnt = []
for x in cl:
    r = 'dom' if C.systems(x) else ('transfer' if C.systems(x, use_T=True) else None)
    res[r] = res.get(r, 0) + 1
    if r is None: unc.append(x)
print('coverage', res, flush=True)
for u in unc: print(' uncovered', [i for i in range(36) for _ in range(u[i])], C.fibre_structure(u))
np.save(f'/private/tmp/claude-501/-Users-shoru-Desktop-Test4/0ed9f581-4f02-4fb6-a7db-5e10049bb620/scratchpad/W36_N{N}.npy', np.array(cl))
