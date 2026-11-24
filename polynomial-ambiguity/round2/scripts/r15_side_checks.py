"""R15-A side mismatch checks.
(1) Polish-notation (Lukasiewicz) grammars Y -> f Y^{k_f} over complete prefix codes of depth<=3:
    unambiguous; critical at z=1/2 iff sum 2^-|f|(1-k_f)=0. Check: D bounded above on L(Y)
    (exact DP of max D over words of length n<=NMAX) => D constant (Thm SM), i.e. e=0.
(2) Ambiguous grammar Y -> bYa | bYYb | a | bbbb: derivation GF critical, D<=1/2, slack>0;
    Thm SM predicts its LANGUAGE has radius >1/2: distinct-word counts / 2^n decay exponentially.
"""
import itertools
from fractions import Fraction as Fr
def D(w): return Fr(w.count('a')-w.count('b'),2)
def codes(depth):
    # complete prefix codes = leaf sets of full binary trees of depth<=depth
    def trees(p,d):
        yield [p]
        if d>0:
            for L in trees(p+'a',d-1):
                for R in trees(p+'b',d-1): yield L+R
    return [c for c in trees('',depth) if len(c)>=2]
NMAX=40
tot=crit=bnd=viol=0
for code in codes(3):
    for ar in itertools.product((0,1,2),repeat=len(code)):
        if 0 not in ar or 2 not in ar: continue
        tot+=1
        if sum(Fr(1,2**len(f))*(1-k) for f,k in zip(code,ar))!=0: continue
        crit+=1
        # DP: best[n][p] = (maxD,minD) over sequences of codewords of total length n with p pending slots
        NEG=None
        best=[dict() for _ in range(NMAX+1)]; best[0][1]=(Fr(0),Fr(0))
        for n in range(NMAX+1):
            for p,(mx,mn) in list(best[n].items()):
                if p==0: continue
                for f,k in zip(code,ar):
                    m=n+len(f); q=p-1+k
                    if m>NMAX or q>NMAX: continue
                    v=(mx+D(f),mn+D(f)); o=best[m].get(q)
                    best[m][q]=v if o is None else (max(o[0],v[0]),min(o[1],v[1]))
        fin=[best[n][0] for n in range(NMAX+1) if 0 in best[n]]
        mxs=[x[0] for x in fin]; mns=[x[1] for x in fin]
        bounded_above = max(mxs[len(mxs)//2:])<=max(mxs[:len(mxs)//2])  # no growth in 2nd half
        const = max(mxs)==min(mns)
        if bounded_above:
            bnd+=1
            print('   bounded-above:',dict(zip(code,ar)),'D const =',mxs[0])
            if not const: viol+=1; print('VIOLATION',code,ar,mxs[:6],mns[:6])
print(f'(1) polish grammars tried={tot} critical={crit} D-bounded-above={bnd} of which nonconstant D={viol}')
# example of the potential: code {a:1? ...} print the bounded ones' lambda
# (2)
N=26
W=[set() for _ in range(N+1)]; W[1].add('a'); W[4].add('bbbb')
for n in range(3,N+1):
    W[n]|={'b'+w+'a' for w in W[n-2]}
    for k in range(1,n-2):
        for u in W[k]:
            for v in W[n-2-k]: W[n].add('b'+u+v+'b')
T=[0]*(N+1); T[1]=1; T[4]+=1
for n in range(3,N+1): T[n]+=T[n-2]+sum(T[k]*T[n-2-k] for k in range(1,n-2))
print('(2) words/derivations:',' '.join(f'{n}:{len(W[n])/T[n]:.3f}' for n in range(12,N+1,2)))
print('(2) n, distinct words, ratio |L_n|/|L_{n-2}| (->4 iff radius 1/2):')
print(' '.join(f'{n}:{len(W[n])}:{len(W[n])/max(1,len(W[n-2])):.3f}' for n in range(12,N+1,2)))
