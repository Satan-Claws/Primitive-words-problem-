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
for trial in range(200):
    nu=[rng.choice([-1,1])*rng.randint(1,50) for _ in range(w)]
    mu=[sum(v*nu[q] for q,v in rows[i].items()) for i in supp]
    if not all(mu) or mu[0]>0: continue
    m=len(supp); c=make_cost(m,0)
    om=[rng.randint(100,1000) for _ in range(P)]
    B=10
    x={i:B*om[i%P] for i in supp}
    for p in ps:
        d=[rng.randint(-60,60) for _ in range(P*p)]
        for i in supp: x[i]+=d[i%(P*p)]
    mraw=[mu[a]*x[supp[a]] for a in range(m)]
    tau=sum(mraw)
    if tau<=0: continue
    mp=list(mraw); mp[0]-=tau
    plan=optimal_plan(mp,c); E=sorted(plan)
    if not is_spanning_tree(E,m): continue
    rep_valid=valid_exact(E,mp)
    roots_ok=[r for r in range(m) if s2p_valid(E,mraw,mu,r)]
    print(dict(supp=m, mu_v0=mu[0], tau=tau, report_valid=rep_valid, nc=is_nc(E), S2P_valid_roots=roots_ok))
    if found==0:
        print('nu=',nu); print('mu=',mu); print('x(on supp)=',[x[i] for i in supp]); print('T*=',E)
    found+=1
    if found>=6: break
