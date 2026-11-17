# Check: for w in R_m = a(ab+)^{m-1} a (ab+)^{m-1}, w primitive  <=>  x != y.
import itertools
def primitive(w):
    n=len(w)
    return all(w != w[d:]+w[:d] for d in range(1,n) if n%d==0)
bad=0; tot=0
for m in range(2,6):
    M=m-1
    B = 4 if M<=2 else (3 if M==3 else 2)
    for x in itertools.product(range(1,B+1),repeat=M):
        for y in itertools.product(range(1,B+1),repeat=M):
            w='a'+''.join('a'+'b'*v for v in x)+'a'+''.join('a'+'b'*v for v in y)
            tot+=1
            if primitive(w)!=(x!=y): bad+=1; print('FAIL',m,x,y)
print('slice identity checked',tot,'words, failures',bad)
