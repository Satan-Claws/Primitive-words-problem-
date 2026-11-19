"""Exact linear-algebra audit for the 12-coordinate, six-run-pair slice.

This checks only perfect-matching affine cones, not all stratified cones.
"""
import json
from functools import lru_cache
from pathlib import Path
import sympy as sp
import z3


@lru_cache(None)
def matchings(vertices):
    if not vertices:
        return ((),)
    i = vertices[0]
    out = []
    for cut in range(1, len(vertices), 2):
        j = vertices[cut]
        for left in matchings(vertices[1:cut]):
            for right in matchings(vertices[cut+1:]):
                out.append(((i, j),) + left + right)
    return tuple(out)


def annihilators(n, d, matching):
    cols = [[int(i % d == j) for i in range(n)] for j in range(d)]
    cols += [[int(i in edge) for i in range(n)] for edge in matching]
    matrix = sp.Matrix(n, len(cols), lambda i,j: cols[j][i])
    result = []
    for v in matrix.T.nullspace():
        multiplier = sp.ilcm(*[t.q for t in v])
        result.append([int(t*multiplier) for t in v])
    return result


def main():
    n = 12
    ms = matchings(tuple(range(n)))
    xs = [z3.Real('x'+str(i)) for i in range(n)]
    solver = z3.Solver()
    solver.set(timeout=60000)
    # A general primitive exponent vector; no integrality bound is imposed.
    for d in [4,6]:
        solver.add(z3.Or([xs[i] != xs[i % d] for i in range(d,n)]))
    # Translation, rotation and scaling allow a zero minimum and unit maximum.
    solver.add(xs[0] == 0, *[z3.And(x>=0,x<=1) for x in xs])
    solver.add(z3.Or([x==1 for x in xs]))
    nullspaces = []
    for matching in ms:
        tests = []
        ns = {}
        for d in [4,6]:
            rows = annihilators(n,d,matching)
            ns[d] = rows
            tests.append(z3.And([z3.Sum([v*x for v,x in zip(row,xs)]) == 0 for row in rows]))
        solver.add(z3.Or(tests))
        nullspaces.append({'matching': matching, 'annihilators': ns})
    print('matchings',len(ms),flush=True)
    answer=solver.check()
    result={'n':n,'periods':[4,6],'matchings':len(ms),'result':str(answer),
            'meaning':'Existence of primitive real tuple with no safe perfect-matching affine span',
            'limitation':'Does not quantify over all stratified period sets'}
    if answer==z3.sat:
        model=solver.model()
        point=[sp.Rational(str(model.eval(x))) for x in xs]
        scale=sp.ilcm(*[v.q for v in point])
        integer_point=[int(v*scale)+1 for v in point]
        result['positive_integer_point']=integer_point
        # Independent arithmetic check of the returned point for every matching.
        assert all(any(integer_point[i]!=integer_point[i%d] for i in range(d,n)) for d in [4,6])
        for data in nullspaces:
            assert any(all(sum(a*b for a,b in zip(row,integer_point))==0 for row in rows)
                       for rows in data['annihilators'].values())
        result['verified']=True
    elif answer==z3.unknown:
        result['reason']=solver.reason_unknown()
    Path('paired_slice_matchings_result.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2),flush=True)


if __name__=='__main__':
    main()
