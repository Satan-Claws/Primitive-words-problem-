import sys, numpy as np, random
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from tile2_muk import structure
for N in (2,3,4):
  for k in range(N):
    ps,P,n,w,supp,rows=structure(N,k); m=len(supp); mm=[P*p for p in ps]; dim=sum(mm)
    if N<=3:
        cur=np.zeros((dim,w),dtype=np.int64); pref=[cur.copy()]
        for i in supp:
            off=0
            for M in mm:
                for q,v in rows[i].items(): cur[off+(i%M),q]+=v
                off+=M
            pref.append(cur.copy())
    else:
        rng=random.Random(0); nu=[rng.randint(-10**6,10**6) for _ in range(w)]
        mu={i:sum(v*nu[q] for q,v in rows[i].items()) for i in supp}
        cur=np.zeros(dim,dtype=np.int64); pref=[cur.copy()]
        for i in supp:
            off=0
            for M in mm: cur[off+(i%M)]+=mu[i]; off+=M
            pref.append(cur.copy())
    F=pref[-1]
    keys={}
    for j,Pj in enumerate(pref): keys.setdefault(Pj.tobytes(),[]).append(j)
    lin=sum(len(v)*(len(v)-1)//2 for v in keys.values())  # includes intervals containing supp[0]
    wrap=[]
    for a,Pa in enumerate(pref):
        for b in keys.get((Pa+F).tobytes(),[]):
            if b>a and not (a==0 and b==m): wrap.append((a,b))
    print(N,k+1,'m',m,'balanced linear intervals (any)',lin,'balanced wrapping arcs',len(wrap),wrap[:3],flush=True)
