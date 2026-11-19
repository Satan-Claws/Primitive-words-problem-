# For n=6,h=(1,2,1,2,1,2): for each admissible delta, is there a good c and shift K (0..6)
# whose naive piece delta+K h+N P_{c,h} avoids non-primitive vectors (searched up to coeff 5)?
import itertools
from fractions import Fraction
n=6;h=[1,2,1,2,1,2]
def inV(x,D): return all(x[i]==x[(i+D)%n] for i in range(n))
def anti(x,c): return [x[i]-x[(c-i)%n] for i in range(n)]
def chords(c):
    P=[];seen=set()
    for i in range(n):
        j=(c-i)%n
        if (j,i) in seen: continue
        seen.add((i,j)); P.append(sorted({i,j}))
    return P
def piece_clean(d,c,K):
    ch=chords(c)
    for ts in itertools.product(range(6),repeat=len(ch)):
        y=[d[i]+K*h[i] for i in range(n)]
        for s,t in zip(ch,ts):
            for i in s: y[i]+=t*h[i]
        if inV(y,3) or inV(y,2): return False
    return True
stats={'some naive piece clean':0,'all naive pieces dirty':0}; ex=None
for d0 in itertools.product(range(3),repeat=n):
    d=list(d0)
    if inV(d,2): continue
    goodc=[c for c in range(n) if not inV(anti([Fraction(d[i],h[i]) for i in range(n)],c),2)]
    if any(piece_clean(d,c,K) for c in goodc for K in range(7)): stats['some naive piece clean']+=1
    else:
        stats['all naive pieces dirty']+=1
        if ex is None: ex=d
print(stats,"example:",ex)
