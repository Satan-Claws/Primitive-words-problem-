import numpy as np, time
from affine_cover import run
rng = np.random.default_rng(777)
for n in range(19, 25):
    t = time.time()
    r = run(n, rng, ntest_subset=20, best_of=4)
    print(f"{r['n']:2d} {r['k']}  {r['Qn']:9d}  {r['emp_prob']:.4f} vs {r['exact_prob']:.4f}"
          f"            {r['random_cover']:4d} ({r['random_draws']:5d})         {r['greedy_cover']:4d}        {r['bound']:5d}"
          f"   [{time.time()-t:.1f}s]", flush=True)
