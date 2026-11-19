"""CEGIS over a finite family of near-perfect-matching affine spaces.

Exact rational linear predicates, but no claim about all stratified cones.
"""
import json
import time
from pathlib import Path
from functools import lru_cache
import sympy as sp
import z3
from paired_slice_matchings import matchings


@lru_cache(None)
def nulls(n,d,matching,singleton):
    cols=[[int(i%d==j) for i in range(n)] for j in range(d)]
    cols += [[int(i in edge) for i in range(n)] for edge in matching]
    cols.append([int(i==singleton) for i in range(n)])
    matrix=sp.Matrix(n,len(cols),lambda i,j:cols[j][i])
    rows=[]
    for v in matrix.T.nullspace():
        scale=sp.ilcm(*[entry.q for entry in v])
        rows.append(tuple(int(entry*scale) for entry in v))
    return tuple(rows)


def main():
    n=15; periods=(3,5)
    family=[(matching,s) for s in range(n)
            for matching in matchings(tuple(i for i in range(n) if i!=s))]
    xs=[z3.Real('x'+str(i)) for i in range(n)]
    solver=z3.Solver(); solver.set(timeout=10000)
    for d in periods:
        solver.add(z3.Or([xs[i]!=xs[i%d] for i in range(d,n)]))
    solver.add(xs[0]==0,*[z3.And(x>=0,x<=1) for x in xs])
    solver.add(z3.Or([x==1 for x in xs]))
    started=time.monotonic(); rounds=0; used=[]
    result={'n':n,'periods':periods,'family_size':len(family),
            'limitation':'Only unweighted near-perfect matchings plus singleton; no finite stratified cover is implied'}
    while time.monotonic()-started<100:
        answer=solver.check()
        if answer!=z3.sat:
            result['result']=str(answer)
            if answer==z3.unknown: result['reason']=solver.reason_unknown()
            break
        model=solver.model()
        point=[sp.Rational(str(model.eval(x))) for x in xs]
        scale=sp.ilcm(*[v.q for v in point])
        ip=[int(v*scale) for v in point]
        selected=None
        for matching,s in family:
            rows=[nulls(n,d,matching,s) for d in periods]
            if all(any(sum(a*b for a,b in zip(row,ip))!=0 for row in rs) for rs in rows):
                selected=(matching,s,rows); break
        if selected is None:
            result['result']='counterexample'
            result['positive_integer_point']=[x+1 for x in ip]
            break
        matching,s,rows=selected
        solver.add(z3.Or([z3.And([z3.Sum([a*x for a,x in zip(row,xs)])==0 for row in rs]) for rs in rows]))
        used.append({'matching':matching,'singleton':s,'annihilators':dict(zip(periods,rows))})
        rounds+=1
        if rounds%10==0: print('rounds',rounds,'cached_nullspaces',nulls.cache_info().currsize,flush=True)
    else:
        result['result']='timeout'
    result['rounds']=rounds
    result['seconds']=round(time.monotonic()-started,3)
    result['used_matchings']=used
    Path('odd_slice_matchings_result.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='used_matchings'},indent=2),flush=True)


if __name__=='__main__': main()
