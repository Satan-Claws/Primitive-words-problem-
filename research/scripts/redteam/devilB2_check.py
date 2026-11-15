# Redteam: devil B2 example x=(0,3,1,3,0,4): no set of pairwise vertex-disjoint non-crossing chords of the
# 6-cycle, labelled by the true relations of x, is inconsistent with every period d in {3,2}.
import itertools
x=(0,3,1,3,0,4); n=6; D=[3,2]
pairs=[(i,j) for i in range(n) for j in range(i+1,n)]
def cross(a,b): return a[0]<b[0]<a[1]<b[1] or b[0]<a[0]<b[1]<a[1]
def feasible(cons,d):
    # variables = residues mod d; cons list of (i,j,rel) rel in '<','=','>'
    # infeasible iff a cycle in <= graph containing a strict edge: use Floyd on max-plus
    INF=float('-inf'); g=[[INF]*d for _ in range(d)]
    for i in range(d): g[i][i]=0
    for i,j,r in cons:
        a,b=i%d,j%d
        if r=='<': g[a][b]=max(g[a][b],1)        # x_a +1 <= x_b
        elif r=='>': g[b][a]=max(g[b][a],1)
        else: g[a][b]=max(g[a][b],0); g[b][a]=max(g[b][a],0)
    for k in range(d):
        for i in range(d):
            for j in range(d):
                if g[i][k]+g[k][j]>g[i][j]: g[i][j]=g[i][k]+g[k][j]
    return all(g[i][i]<=0 for i in range(d))
found=None
for r in range(1,4):
    for M in itertools.combinations(pairs,r):
        pts=[p for e in M for p in e]
        if len(set(pts))<len(pts) or any(cross(a,b) for a,b in itertools.combinations(M,2)): continue
        cons=[(i,j,'<' if x[i]<x[j] else '=' if x[i]==x[j] else '>') for i,j in M]
        if all(not feasible(cons,d) for d in D): found=M
print('sound labelled non-crossing matching for',x,':',found)
