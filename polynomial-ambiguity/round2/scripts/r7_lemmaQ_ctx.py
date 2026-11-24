# r7_lemmaQ_ctx.py: quotient P^{-1} G^- S^{-1} is NOT determined by (t,h); with h=1 it can be all of Sigma^m.
import itertools
def inG(w):
    n=len(w); d=0
    for k in range(1,n//2+1):
        d+= (w[k-1]=='a')-(w[n-k]=='a')
        if d>=0: return False
    return True
def qdens(P,S,m):
    c=sum(inG(P+''.join(x)+S) for x in itertools.product('ab',repeat=m)); return c/2**m
m=10
# context: P=b, x (left half), S = b^r a^m a   (x paired with a's; d_1=-1 i.e. h=1)
for r in [0,2,4]:
    P='b'; S='b'*r+'a'*m+'a'
    N=len(P)+m+len(S); t=len(S)-len(P)
    h=-( (P[0]=='a')-(S[-1]=='a'))
    print('h=',h,'t=',t,'N=',N,'quotient density',qdens(P,S,m))
# generic centred context t=0, h=1: x's own fold meander
print('t=0,h=1:',qdens('b','a',m))
