# check certificate structures are non-crossing (near-)perfect matchings: valid stratified period sets
import json,sys,glob
for f in sorted(glob.glob('../bounded/cert_nearconst_*.json')):
    c=json.load(open(f)); n=c['n']; ok=True
    for st in c['structures']:
        pts=sorted(i for comp in st for i in comp)
        if pts!=list(range(n)) or any(len(comp)>2 for comp in st) or sum(len(comp)==1 for comp in st)>(n%2): ok=False
        prs=[tuple(sorted(comp)) for comp in st if len(comp)==2]
        for (a,b) in prs:
            for (c2,d) in prs:
                if a<c2<b<d: ok=False
    print(f.split('/')[-1],'n',n,'valid non-crossing matchings' if ok else 'INVALID')
