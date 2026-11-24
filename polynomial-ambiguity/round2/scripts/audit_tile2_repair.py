import sys, random
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from tile2_muk import structure
from tile2_core import make_cost, optimal_plan, is_spanning_tree, is_nc, valid_exact

def subtree_sums(edges, mass, root):
    m=len(mass); adj={v:[] for v in range(m)}
    for i,j in edges: adj[i].append(j); adj[j].append(i)
    order=[root]; par={root:None}
    for v in order:
        for w in adj[v]:
            if w not in par: par[w]=v; order.append(w)
    sub={v:mass[v] for v in range(m)}
    for v in reversed(order):
        if par[v] is not None: sub[par[v]]+=sub[v]
    return sub
def s2p_valid(edges, m_raw, mu, root):
    # S2P: n_v(x)=mu(x|S_v) has sign of top(v) for ALL v incl. root (S_root = everything, n = tau)
    sub=subtree_sums(edges,m_raw,root)
    return all((sub[v]>0)==(mu[v]>0) and sub[v]!=0 for v in range(len(mu)))

N=2; k=0
ps,P,n,w,supp,rows=structure(N,k)
rng=random.Random(5)
found=0

for N,k in ((2,0),(2,1)):
  ps,P,n,w,supp0,rows=structure(N,k)
  rng=random.Random(3)
  for rep in range(3):
    while True:
      nu=[rng.choice([-1,1])*rng.randint(1,50) for _ in range(w)]
      mu0=[sum(v*nu[q] for q,v in rows[i].items()) for i in supp0]
      if all(mu0): break
    s=next(a for a in range(len(mu0)) if mu0[a]>0)  # cut before first positive vertex
    supp=supp0[s:]+supp0[:s]; mu=mu0[s:]+mu0[:s]; m=len(supp); c=make_cost(m,rep)
    pts=[]
    while len(pts)<30:
      om=[rng.randint(100,1000) for _ in range(P)]; B=10
      x={i:B*om[i%P] for i in supp}
      for p in ps:
        d=[rng.randint(-60,60) for _ in range(P*p)]
        for i in supp: x[i]+=d[i%(P*p)]
      mraw=[mu[a]*x[supp[a]] for a in range(m)]; tau=sum(mraw)
      if tau<=0: continue
      mp=list(mraw); mp[0]-=tau
      if mp[0]<=0: continue
      E=sorted(optimal_plan(mp,c)); ok=is_spanning_tree(E,m) and is_nc(E) and s2p_valid(E,mraw,mu,0)
      pts.append((mraw,E,ok))
    viol=sum(1 for a in pts for b in pts if a[1]!=b[1] and s2p_valid(b[1],a[0],mu,0))
    print(N,k+1,'mu_v0_orig',mu0[0],'S2P-valid T* (root=positive cut):',sum(p[2] for p in pts),'/30','pairwise violations',viol)
