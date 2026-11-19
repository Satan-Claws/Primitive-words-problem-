"""Test candidate 'periodic-piece' class families G for soundness (L*M subset of Q,
pieces up to length NS) and measure extra coverage of words left uncovered by fracpos.FAMS."""
import sys, itertools
from fracpos import minper, primitive, words, coverage, in_some_class

def aper(x,t): return minper(x) > t*len(x)
def per(x,t):  return minper(x) <= t*len(x)
def nxt(m): q=minper(m); return m[len(m)-q]          # letter predicted after m
def prv(m): q=minper(m); return m[q-1]               # letter predicted before m
def mid(x): return x[len(x)//2]

# variant: which constraints
def compat(y,m,variant):
    if not (aper(y,2/3) and per(m,1/3)): return False
    if y[0]==nxt(m): return False
    if 'prev' in variant and y[-1]==prv(m): return False
    if 'mid' in variant and mid(y)==mid(m): return False
    return True

def soundness(NS,variant):
    pcs=[w for k in range(1,NS+1) for w in words(k)]
    Ls=[y for y in pcs if aper(y,2/3)]; Ms=[m for m in pcs if per(m,1/3)]
    bad=[]
    for y in Ls:
        for m in Ms:
            if compat(y,m,variant) and not primitive(y+m): bad.append((y,m))
    return bad

def covered_G(w,variant):
    n=len(w)
    for r in range(n):
        v=w[r:]+w[:r]
        for l in range(n//3+1,2*n//3+1):
            if 3*l<=n: continue
            y,m=v[:l],v[l:]
            if compat(y,m,variant) or compat(m,y,variant): return True
    return False

if __name__=="__main__":
    NS=int(sys.argv[1]); NC=int(sys.argv[2])
    for variant in [(),('prev',),('mid',),('prev','mid')]:
        b=soundness(NS,variant)
        print("variant",variant,"unsound pairs:",len(b),b[:5])
    for variant in [('mid',),('prev','mid'),('prev',)]:
        for n in range(4,NC+1):
            tot,unc=coverage(n)
            rest=[w for w in unc if not covered_G(w,variant)]
            print(variant,n,len(unc),"->",len(rest),rest[:8])
