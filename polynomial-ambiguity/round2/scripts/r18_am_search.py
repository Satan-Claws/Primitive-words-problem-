"""search critical (sum 2^{-|u|-|v|}=1) IF-clean single linear SCCs X -> uXv | w with nontrivial exit slides.
usage: r18_am_search.py seed [heavy]"""
import random, itertools, sys
from fractions import Fraction as F
import r18_am_lib as L
def mass(sp): return F(1,2) if sp=='B' else F(1,2**len(sp))
def tmass(t): return mass(t[0])*mass(t[1])
lits=[''.join(p) for l in range(0,4) for p in itertools.product('ab',repeat=l)]
rng=random.Random(int(sys.argv[1])); heavy=len(sys.argv)>2
found=0; nIF=0
for trial in range(20000):
    tok=[]
    if heavy:
        tok.append(rng.choice([('B',''),('','B'),('B','a'),('a','B'),('B','b'),('b','B')]))
    m=sum(tmass(t) for t in tok)
    while m<1:
        u=rng.choice(lits); v=rng.choice(lits)
        if not(u or v) or (u,v) in tok or len(u)+len(v)<2: continue
        if m+tmass((u,v))<=1: tok.append((u,v)); m+=tmass((u,v))
    w=rng.choice(['a','b','ab','ba','aa'])
    G={'tok':tok,'w':w}
    if L.check_IF(G,11): continue
    nIF+=1
    words=L.enumerate_trees(G,14); u,D0,Em,nw=L.stats_from_enum(words,14)
    if max(Em)>1.05:
        print(tok, repr(w), 'Em14=%.3f'%Em[14], 'u14=%.3f'%u[14], 'D0sum=%.3f'%sum(D0), flush=True); found+=1
    if found>=8: break
print('IF-clean',nIF,'trials',trial+1)
