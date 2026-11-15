# Redteam: independent verifier of bounded's C1 certificates cert_nearconst_<n>.json.
# Claim: for every delta not in U_d V_d there is a structure M_i with delta not in span(M_i)+V_d for all d.
# Equivalent: for every choice function i->d_i, the subspace  /\_i (span(M_i)+V_{d_i})  lies in some V_d.
# Subspaces handled by annihilators (row spaces) modulo the prime 2^61-1 (exact over Q with overwhelming
# probability; a mod-p rank can only drop, which here could only make the check FAIL spuriously... see note).
import json, sys
PR=(1<<61)-1
def reduce_into(basis, row):
    # basis: dict pivot->row (fully reduced); returns reduced row
    row=row[:]
    for piv,b in basis.items():
        if row[piv]:
            f=row[piv]; row=[(x-f*y)%PR for x,y in zip(row,b)]
    return row
def add(basis,row):
    row=reduce_into(basis,row)
    for j,x in enumerate(row):
        if x:
            inv=pow(x,PR-2,PR); row=[(y*inv)%PR for y in row]
            nb={}
            for piv,b in basis.items():
                f=b[j]; nb[piv]=[(u-f*v)%PR for u,v in zip(b,row)] if f else b
            nb[j]=row; return nb, True
    return basis, False
def rowspace(rows):
    B={}
    for r in rows: B,_=add(B,r)
    return B
def ann_of_span(gens,n):
    # annihilator = kernel of matrix with rows gens
    B=rowspace(gens)
    free=[j for j in range(n) if j not in B]
    out=[]
    for f in free:
        v=[0]*n; v[f]=1
        for piv,b in B.items(): v[piv]=(-b[f])%PR
        out.append(v)
    return out
cert=json.load(open(sys.argv[1])); n=cert['n']; ds=cert['ds']
def Vd_gens(d): return [[1 if i%d==r else 0 for i in range(n)] for r in range(d)]
def Vd_ann(d):  return [[(1 if i==j else 0)-(1 if i==(j+d)%n else 0) for i in range(n)] for j in range(n)]
Mspan=[]
for st in cert['structures']:
    g=[]
    for comp in st:
        v=[0]*n
        for i in comp: v[i]=1
        g.append(v)
    Mspan.append(g)
# annihilator of span(M_i)+V_d
A={}
for i,g in enumerate(Mspan):
    for d in ds: A[(i,d)]=ann_of_span(g+Vd_gens(d),n)
Vann={d:Vd_ann(d) for d in ds}
def contained(B):
    for d in ds:
        if all(not any(reduce_into(B,r)) for r in Vann[d]): return True
    return False
r=len(Mspan); nodes=0; bad=[]
def dfs(i,B,choice):
    global nodes; nodes+=1
    if contained(B): return
    if i==r: bad.append(choice[:]); return
    for d in ds:
        B2=B
        for row in A[(i,d)]: B2,_=add(B2,row)
        choice.append(d); dfs(i+1,B2,choice); choice.pop()
        if len(bad)>3: return
dfs(0,{},[])
print('n',n,'structures',r,'dfs nodes',nodes,'VERIFIED' if not bad else 'FAILED %s'%bad[:3])
