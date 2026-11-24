"""Example S + Dyck-block tokens + literal fill to exact criticality; IF check; report slides."""
import itertools, sys
from fractions import Fraction as F
import r18_am_lib as L
base=[('ab','ab'),('bb','a'),('','ba')]
def mass(sp): return F(1,2) if sp=='B' else F(1,2**len(sp))
def tmass(t): return mass(t[0])*mass(t[1])
lits=[''.join(p) for l in range(0,5) for p in itertools.product('ab',repeat=l)]
heavies=[(x,'B') for x in lits if len(x)<=2]+[('B',x) for x in lits if len(x)<=2]
cands=[(u,v) for u in lits for v in lits if 2<=len(u)+len(v)<=5]
K=int(sys.argv[1]); out=0
for h1,h2 in itertools.combinations(heavies,2):
    tok=base+[h1,h2]; m=sum(tmass(t) for t in tok)
    if m>1: continue
    rest=1-m
    fills=[[]] if rest==0 else [[c] for c in cands if tmass(c)==rest]+[[c,d] for c,d in itertools.combinations(cands,2) if tmass(c)+tmass(d)==rest and rest>=F(1,16)]
    for f in fills:
        G={'tok':tok+f,'w':'ab'}
        if L.check_IF(G,K): continue
        words=L.enumerate_trees(G,14); u,D0,Em,nw=L.stats_from_enum(words,14)
        print(G['tok'][3:], 'Em14=%.3f'%Em[14], 'D0sum=%.3f'%sum(D0), flush=True); out+=1
        if out>=10: sys.exit()
