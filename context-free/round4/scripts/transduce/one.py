import sys, itertools, math
def primitive(w):
    n=len(w); return n>0 and (w+w).find(w,1)==n
ys=sys.argv[1].split(','); xs=sys.argv[2].split(',')
r=len(ys)
for R in [8,16,32,64]:
    cnt=0; ex=[]
    for e in itertools.product(range(R),repeat=r):
        w=''.join(ys[i]*e[i]+xs[i] for i in range(r))
        if not primitive(w):
            cnt+=1
            if R==16 and len(ex)<0: ex.append(e)
    print(R,cnt)
