# r6_nofold: membership of G^- and F_K on 3-parameter bounded slices; print the region.
import itertools, sys
def d(w,k): return w[:k].count('a')-w[len(w)-k:].count('a')
def Gm(w):
    n=len(w); return all(d(w,k)<0 for k in range(1,n//2+1))
def FK(w):
    n=len(w); lo=-(-n//3); return all(d(w,k)!=0 for k in range(lo,n//2+1))
def slice_(f,blocks,N):
    out=[]
    for e in itertools.product(range(1,N),repeat=len(blocks)):
        w=''.join(b*x for b,x in zip(blocks,e))
        out.append((e,f(w)))
    return out
if __name__=='__main__':
    blocks=sys.argv[1].split(','); N=int(sys.argv[2]); f={'G':Gm,'F':FK}[sys.argv[3]]
    res=slice_(f,blocks,N)
    print(sum(m for _,m in res),'of',len(res))
    for e,m in res:
        if len(sys.argv)>4 and m: print(e)
