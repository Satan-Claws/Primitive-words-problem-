"""S4T part 3 driver: sparse exhaustive + random ply for the mixed family of s4t_chords.py.
x = a+b+c (periods 15,10,6), each generator 0/1 with support <= (2,1,1),(1,2,1),(1,1,2)."""
import itertools, random, importlib.util, os
spec=importlib.util.spec_from_file_location('m',os.path.join(os.path.dirname(os.path.abspath(__file__)),'s4t_chords.py'))
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
def sub(L,k): return [s for j in range(k+1) for s in itertools.combinations(range(L),j)]
def vec(L,s): return [1 if t in s else 0 for t in range(L)]
tot=unc=0; ex=None; mx=0; mn=10**9
for ks in ((2,1,1),(1,2,1),(1,1,2)):
    for sa in sub(15,ks[0]):
        for sb in sub(10,ks[1]):
            for sc in sub(6,ks[2]):
                x=m.W30(vec(15,sa),vec(10,sb),vec(6,sc))
                if not m.inE(x): continue
                tot+=1; k=m.count(x,'disjoint',stop=True) or len(m.rect_certs(x))
                if k==0: unc+=1; ex=ex or x
print('sparse W30 primitive',tot,'uncovered',unc,ex)
rng=random.Random(3)
for _ in range(150):
    x=m.rnd(rng)
    if m.inE(x): k=m.mixed(x); mx=max(mx,k); mn=min(mn,k)
print('random W30 ply (#certificates containing x): min',mn,'max',mx)
