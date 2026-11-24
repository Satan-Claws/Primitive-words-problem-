# Search single-nonterminal linear SCCs X -> u_i X v_i | w (fixed exit w) for centre slides
# without C_exp (no two token sequences with the same interface (U,V), checked to depth R).
# Reports growth of max multiplicity m_r = max_W #{token seqs of length<=R giving word U w V}.
import itertools, random, collections, sys
random.seed(int(sys.argv[1]) if len(sys.argv)>1 else 1)
def words(maxlen):
    out=['']
    for L in range(1,maxlen+1): out+= [''.join(p) for p in itertools.product('ab',repeat=L)]
    return out
W2=words(2)
def analyse(toks,w,R):
    seen={}  # interface -> seq
    mult=collections.Counter(); byR=[]
    frontier=[((),'','')]
    for r in range(1,R+1):
        nf=[]
        for seq,U,V in frontier:
            for i,(u,v) in enumerate(toks):
                U2,V2=U+u,v+V; s=seq+(i,)
                if (U2,V2) in seen: return None   # IF violation => C_exp
                seen[(U2,V2)]=s; nf.append((s,U2,V2)); mult[U2+w+V2]+=1
        frontier=nf
        byR.append(max(mult.values()))
    return byR
best=[]
for trial in range(4000):
    k=random.choice([2,3])
    toks=[(random.choice(W2),random.choice(W2)) for _ in range(k)]
    if any(u+v=='' for u,v in toks) or len(set(toks))<k: continue
    w=random.choice(W2)
    res=analyse(toks,w,9)
    if res and res[-1]>=3: best.append((res[-1],res,toks,w))
best.sort(key=lambda x:-x[0])
seen=set()
for b in best[:12]:
    key=(tuple(b[2]),b[3])
    if key in seen: continue
    seen.add(key); print(b[1],b[2],repr(b[3]))
print('candidates with mult>=3:',len(best))
