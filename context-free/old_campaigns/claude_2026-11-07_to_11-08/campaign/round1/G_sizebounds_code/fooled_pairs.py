# Exhaustive: number of pairs {f,g} of primitive words fooled at EVERY balanced interval.
import itertools
def primes_of(n): return [p for p in range(2,n+1) if n%p==0 and all(p%q for q in range(2,p))]
for n in [4,5,6,7,8,9,10]:
    ps=primes_of(n)
    P=[format(x,f'0{n}b') for x in range(1<<n)]
    prim=set(w for w in P if all(w[n//p:]+w[:n//p]!=w for p in ps))
    Ql=sorted(prim)
    ivs=[(i,l) for l in range((n+2)//3,(2*n)//3+1) for i in range(n-l+1)]
    cnt=0; ex=None
    for a in range(len(Ql)):
        f=Ql[a]
        for b in range(a+1,len(Ql)):
            g=Ql[b]
            if all(not((g[:i]+f[i:i+l]+g[i+l:]) in prim and (f[:i]+g[i:i+l]+f[i+l:]) in prim) for (i,l) in ivs):
                cnt+=1; ex=(f,g)
    print(f"n={n} |Q_n|={len(Ql)} intervals={len(ivs)} pairs fooled at all balanced intervals={cnt} example={ex}",flush=True)
