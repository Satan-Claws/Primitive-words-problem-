"""T2a heuristic illustration (NOT exact): random product-half-space covers. s random pieces,
coverage and ply estimated on random test points (Gaussian per factor). Usage: python3 t2a_random.py N d s T"""
import sys, numpy as np
N,d,s,T=map(int,sys.argv[1:]); rng=np.random.default_rng(1)
U=rng.standard_normal((N,s,d))
X=rng.standard_normal((N,T,d))
inside=np.ones((T,s),bool)
for k in range(N): inside&=(X[k]@U[k].T)>0
ply=inside.sum(1)
print(f"N={N} d={d} pieces={s} uncovered={int((ply==0).sum())}/{T} maxply={ply.max()} prod d={d**N} sum d={N*d}")
