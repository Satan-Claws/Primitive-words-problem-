"""S4T part 2: naive-witness laminar certificates for n=30.
Witness chord for prime p: {s,t} (linear positions 0..29) with t-s ≡ 0 mod n/p, x_s != x_t.
Certificate piece = triple (c2,c3,c5) of witness chords, pairwise non-crossing, + sign pattern.
mode 'disjoint': chords pairwise vertex-disjoint (product of 2-dim cones e_hi, e_hi+e_lo: laminar,
unimodular). mode 'valley': shared endpoints allowed iff shared vertex is strictly smaller
than all its chord partners (periods e_a, e_a+e_b per chord; valley star is 2-support laminar).
Checks: random W_30 samples (a+b+c, entries {0,1,2}); adversarial local search minimising
#certificates over primitive x in W_30 and in {0..2}^30; exhaustive over 0/1 a,b,c in W_30.
Usage: python3 s4t_chords.py"""
import itertools, random
n=30; D={2:15,3:10,5:6}
def per(x,d): return all(x[t]==x[(t+d)%n] for t in range(n))
def inE(x): return not any(per(x,d) for d in D.values())
CH={p:[(s,t) for s in range(n) for t in range(s+1,n) if (t-s)%d==0] for p,d in D.items()}
def crosses(c,e):
    a,b=c; u,v=e
    return a<u<b<v or u<a<v<b
def count(x,mode,stop=False):
    W={p:[c for c in CH[p] if x[c[0]]!=x[c[1]]] for p in D}
    k=0
    for c2 in W[2]:
        for c3 in W[3]:
            if crosses(c2,c3): continue
            for c5 in W[5]:
                cs=(c2,c3,c5)
                if crosses(c2,c5) or crosses(c3,c5): continue
                vs=[v for c in cs for v in c]
                if mode=='disjoint':
                    if len(set(vs))<6: continue
                else:
                    ok=True
                    for v in set(vs):
                        part=[c[0]+c[1]-v for c in cs if v in c]
                        if len(part)>1 and not all(x[v]<x[w] for w in part): ok=False
                    if not ok: continue
                k+=1
                if stop: return k
    return k
def W30(a,b,c): return [a[t%15]+b[t%10]+c[t%6] for t in range(n)]
def rnd(rng,m=2): return W30([rng.randint(0,m) for _ in range(15)],[rng.randint(0,m) for _ in range(10)],[rng.randint(0,m) for _ in range(6)])
if __name__=='__main__':
    rng=random.Random(7)
    for mode in ('disjoint','valley'):
        tot=unc=0; mn=10**9; ex=None
        for _ in range(1500):
            x=rnd(rng)
            if not inE(x): continue
            tot+=1; k=count(x,mode); mn=min(mn,k)
            if k==0: unc+=1; ex=ex or x
        print(mode,'W30 samples',tot,'uncovered',unc,'min#cert',mn,'ex',ex)
    # adversarial local search on W30 generators and on raw {0,1,2}^30
    for space in ('W30','raw'):
        best=None
        for rs in range(30):
            r=random.Random(rs)
            if space=='W30':
                g=[[r.randint(0,2) for _ in range(L)] for L in (15,10,6)]; f=lambda g:W30(*g)
            else:
                g=[[r.randint(0,2) for _ in range(30)]]; f=lambda g:g[0]
            x=f(g); cur=count(x,'disjoint') if inE(x) else 10**9
            for it in range(400):
                h=[l[:] for l in g]; i=r.randrange(len(h)); j=r.randrange(len(h[i])); h[i][j]=r.randint(0,2)
                y=f(h)
                if not inE(y): continue
                k=count(y,'disjoint')
                if k<=cur: g,cur=h,k
                if cur==0: break
            if best is None or cur<best[0]: best=(cur,f(g))
        print('adversarial',space,'min #disjoint certs',best[0],best[1],'valley:',count(best[1],'valley'))
    # exhaustive 0/1 a,b,c (2^31 too many) -> exhaustive over b,c (2^16) with a random/0
    unc=0; tot=0; mn=10**9
    for bits in range(1<<16):
        b=[(bits>>k)&1 for k in range(10)]; c=[(bits>>(10+k))&1 for k in range(6)]
        x=W30([0]*15,b,c)
        if not inE(x): continue
        tot+=1; k=count(x,'disjoint',stop=True)
        if k==0: unc+=1
    print('exhaustive a=0,b,c in {0,1}: primitive',tot,'uncovered(disjoint)',unc)

# ---- part 3: mixed family = (i) 3 disjoint non-crossing witness chords, or
# (ii) rectangle for a prime pair (diagonals non-crossing in linear order, |u|!=|w|)
#      + a witness chord for the third prime lying in a gap of R, outside hull, or enclosing it.
def rect_certs(x):
    out=[]
    for (p,q,r) in ((2,3,5),(2,5,3),(3,5,2)):
        for ka in range(1,p):
            for kb in range(1,q):
                A=ka*D[p]; B=kb*D[q]
                for i in range(n):
                    R=(i,(i+A)%n,(i+A+B)%n,(i+B)%n)
                    if len(set(R))<4: continue
                    d1=tuple(sorted((R[0],R[2]))); d2=tuple(sorted((R[1],R[3])))
                    if crosses(d1,d2): continue
                    u=x[R[1]]-x[R[3]]; w=x[R[2]]-x[R[0]]
                    if abs(u)==abs(w): continue
                    S=sorted(R)
                    for c in CH[r]:
                        if x[c[0]]==x[c[1]] or set(c)&set(R): continue
                        a,b=c
                        ok=(b<S[0] or a>S[3] or (a<S[0] and b>S[3]) or
                            any(S[j]<a and b<S[j+1] for j in range(3)))
                        if ok: out.append((R,c)); 
    return out
def mixed(x): return count(x,'disjoint')+len(rect_certs(x))
if __name__=='__main__':
    import sys
    best=None
    for rs in range(40):
        r=random.Random(100+rs)
        g=[[r.randint(0,2) for _ in range(L)] for L in (15,10,6)]
        x=W30(*g); cur=mixed(x) if inE(x) else 10**9
        for it in range(300):
            h=[l[:] for l in g]; i=r.randrange(3); j=r.randrange(len(h[i])); h[i][j]=r.randint(0,2)
            y=W30(*h)
            if not inE(y): continue
            k=mixed(y)
            if k<=cur: g,cur=h,k
            if cur==0: break
        if best is None or cur<best[0]: best=(cur,W30(*g),g)
    print('mixed family adversarial W30: min #certs',best[0],best[1],'gens',best[2])
