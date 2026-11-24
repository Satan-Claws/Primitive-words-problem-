# Inspect slide example: X -> ab X ab | bb X a | X ba | ab (exit).  Check IF to depth R, show max-mult words.
import collections,sys
toks=[('ab','ab'),('bb','a'),('','ba')]; w='ab'; R=int(sys.argv[1]) if len(sys.argv)>1 else 14
seen={}; mult=collections.defaultdict(list); fr=[((),'','')]; viol=0
for r in range(1,R+1):
    nf=[]
    for s,U,V in fr:
        for i,(u,v) in enumerate(toks):
            U2,V2,s2=U+u,v+V,s+(i,)
            if (U2,V2) in seen: viol+=1
            seen[(U2,V2)]=s2; nf.append((s2,U2,V2)); mult[U2+w+V2].append((len(U2),s2))
    fr=nf
    print(r,'max mult',max(len(x) for x in mult.values()),'IF violations',viol)
W=max(mult,key=lambda x:(len(mult[x]),-len(x)))
print(W,len(W)); [print(' centre',c,'seq',s) for c,s in sorted(mult[W])[:8]]

