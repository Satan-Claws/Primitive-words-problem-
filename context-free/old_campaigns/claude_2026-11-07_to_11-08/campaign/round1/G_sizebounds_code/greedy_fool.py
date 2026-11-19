# Greedy (randomized) fooling sets for balanced rectangles: F ⊆ Q_n such that NO balanced
# Q-rectangle contains two elements of F. Theorem 2 forces |F| <= #rectangles of the explicit cover.
import random, sys
def primes_of(n): return [p for p in range(2,n+1) if n%p==0 and all(p%q for q in range(2,p))]
def is_prim(w,ps,n): return all(w[n//p:]+w[:n//p]!=w for p in ps)
def run(n, tries, seed):
    ps=primes_of(n); rng=random.Random(seed)
    ivs=[(i,l) for l in range((n+2)//3,(2*n)//3+1) for i in range(n-l+1)]
    best=0
    for _ in range(tries):
        F=[]
        cand=list(range(1<<n)); rng.shuffle(cand)
        for x in cand:
            w=format(x,f'0{n}b')
            if not is_prim(w,ps,n): continue
            ok=True
            for f in F:
                for (i,l) in ivs:
                    c1=f[:i]+w[i:i+l]+f[i+l:]; c2=w[:i]+f[i:i+l]+w[i+l:]
                    if is_prim(c1,ps,n) and is_prim(c2,ps,n): ok=False;break
                if not ok: break
            if ok: F.append(w)
        best=max(best,len(F))
    return best, F
for n,tries in [(6,50),(8,30),(10,20),(12,8),(14,3),(16,2)]:
    b,F=run(n,tries,1)
    print(f"n={n} best greedy fooling set size={b} example={F[:6]}",flush=True)
