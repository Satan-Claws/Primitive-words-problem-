#!/usr/bin/env python3
"""density4 checks (single core, < 2 min).
(a) brute force n<=16: E', Cyc(bDa)-language U, L0, L1, L5 facts.
(b) Lemma AC: exact distribution of a k-gram statistic via DP, sup_t P*sqrt(n).
(c) Theorem P(i): random full-rank linear sets for k=1,2 -> explicit s^q in M.
(d) L5 hits every x T z (Parikh-prescribed t) for small x,z.
"""
import itertools, random, math, sys
from math import gcd
from collections import defaultdict

def is_prim(w):
    n=len(w)
    for d in range(1,n):
        if n%d==0 and w[:d]*(n//d)==w: return False
    return n>0

def Delta(w): return w.count('a')-w.count('b')

def walk(w):
    h=[0]
    for c in w: h.append(h[-1]+(1 if c=='a' else -1))
    return h

def inL0(w): return Delta(w) not in (0,1)
def inL1(w):
    h=walk(w); n=len(w)
    return Delta(w) not in (0,1) and max(h)>h[n] and min(h)<h[n]
def F5(w): # |w|_a - 4|w|_aa (linear counts)
    return w.count('a')-4*sum(1 for i in range(len(w)-1) if w[i:i+2]=='aa')
def inL5(w): return F5(w) not in (0,1,2,3)
def inEp(w): return w.count('b')==w.count('a')+1
def inU(w):
    # some rotation r = b x a with every nonempty proper prefix of r having Delta<0 and Delta(r)=0
    n=len(w)
    if Delta(w)!=0 or n==0: return False
    for i in range(n):
        r=w[i:]+w[:i]; h=walk(r)
        if all(h[j]<0 for j in range(1,n)): return True
    return False

def part_a(N=16):
    print("(a) n | E'/2^n*sqrt(n) | U/2^n*sqrt(n) | L0 dens | L1 dens | L5 dens | violations")
    for n in range(1,N+1):
        cE=cU=c0=c1=c5=0; bad=0
        for t in itertools.product('ab',repeat=n):
            w=''.join(t); p=is_prim(w)
            if inEp(w):
                cE+=1; bad+= (not p)
            if inU(w):
                cU+=1; bad+= (not p)
            c0+=inL0(w); c1+=inL1(w); c5+=inL5(w)
        T=2**n
        print(n, round(cE/T*n**.5,3), round(cU/T*n**.5,3), round(c0/T,3), round(c1/T,3), round(c5/T,3), bad)

def dist_stat(n, k, ell):
    """exact distribution of sum_g ell[g]*V_k(w)_g over w in Sigma^n (cyclic counts), n>=k.
    DP over first k-1 letters, last k-1 letters."""
    res=defaultdict(int)
    for pre in itertools.product('ab',repeat=k-1):
        pre=''.join(pre)
        # state: last k-1 letters -> {value:count}
        st={pre:{0:1}}
        for i in range(n-(k-1)):
            nst=defaultdict(lambda: defaultdict(int))
            for last,d in st.items():
                for c in 'ab':
                    g=last+c; nl=g[1:]
                    for v,m in d.items(): nst[nl][v+ell.get(g,0)]+=m
            st=nst
        for last,d in st.items():
            # wrap k-grams: from last+pre
            s=last+pre; extra=sum(ell.get(s[j:j+k],0) for j in range(k-1))
            for v,m in d.items(): res[v+extra]+=m
    return res

def part_b():
    print("(b) Lemma AC: sup_t #{ell(V)=t}/2^n * sqrt(n)")
    tests=[(1,{'a':1,'b':-1}),(2,{'a'+'a':1,'ab':-1}),(2,{'aa':1,'bb':-1}),(3,{'aba':1,'bab':-1,'aaa':2})]
    for k,ell in tests:
        row=[]
        for n in (20,40,80,160):
            d=dist_stat(n,k,ell); row.append(round(max(d.values())/2**n*n**.5,4))
        print(" k=%d ell=%s:"%(k,ell),row)
    # degenerate example: ell = #ab - #ba (cyclic) is identically 0 -> no bound expected
    d=dist_stat(30,2,{'ab':1,'ba':-1}); print(" degenerate #ab-#ba cyclic: support",sorted(d))

# ---------- (c) Theorem P(i) ----------
def kgrams(k): return [''.join(t) for t in itertools.product('ab',repeat=k)]
def Vcyc(w,k):
    n=len(w); ww=w*(k//n+2); G=kgrams(k); v=dict.fromkeys(G,0)
    for i in range(n): v[ww[i:i+k]]+=1
    return tuple(v[g] for g in G)

def euler_word(v,k):
    """cyclic word with cyclic k-gram vector v (v>0, balanced)."""
    G=kgrams(k); mult={g:v[i] for i,g in enumerate(G)}
    if k==1:
        return 'a'*mult['a']+'b'*mult['b']
    adj=defaultdict(list)
    for g,m in mult.items(): adj[g[:-1]]+= [g]*m
    for u in adj: random.shuffle(adj[u])
    start='a'*(k-1); stack=[start]; path=[]; ptr={u:list(adj[u]) for u in adj}
    edges=[]; estack=[]
    # Hierholzer on edges
    cur=start; circ=[]
    st=[(start,None)]
    while st:
        u,e=st[-1]
        if ptr[u]:
            g=ptr[u].pop(); st.append((g[1:],g))
        else:
            st.pop()
            if e is not None: circ.append(e)
    circ.reverse()
    w=''.join(g[-1] for g in circ)
    return w

def smith_index_check(P, c, q, k):
    """find integer z with c + sum z_i p_i == 0 mod q (componentwise), brute force small."""
    r=len(P); K=len(c)
    for z in itertools.product(range(q),repeat=r):
        ok=all((c[j]+sum(z[i]*P[i][j] for i in range(r)))%q==0 for j in range(K))
        if ok: return z
    return None

def part_c(trials=200, seed=1):
    random.seed(seed); print("(c) Theorem P(i) random full-rank linear sets")
    okc=0; skipped=0
    for tr in range(trials):
        k=random.choice([1,2])
        # generators of E cap N^K: cyclic count vectors of random short words
        def rv():
            w=''.join(random.choice('ab') for _ in range(random.randint(1,4))); return Vcyc(w,k)
        dimE = 2 if k==1 else 3
        P=[rv() for _ in range(dimE+random.randint(0,1))]
        import numpy as np
        if np.linalg.matrix_rank(np.array(P,dtype=float))<dimE: skipped+=1; continue
        c=rv()
        found=False
        for q in (2,3,5,7):
            z=smith_index_check(P,c,q,k)
            if z is None: continue
            T=3
            n_i=[z[i]+q*T for i in range(len(P))]
            Pt=[c[j]+sum(n_i[i]*P[i][j] for i in range(len(P))) for j in range(len(c))]
            v=[x//q for x in Pt]
            assert all(x%q==0 for x in Pt) and all(x>0 for x in v)
            s=euler_word(v,k)
            assert Vcyc(s,k)==tuple(v), (s,v)
            assert Vcyc(s*q,k)==tuple(Pt)
            assert not is_prim(s*q)
            found=True; break
        okc+=found
        if not found: print("  no q in (2,3,5,7) works for",P,c)
    print("  constructed s^q in M:",okc,"skipped (rank-deficient):",skipped)

def part_d():
    print("(d) L5: for all |x|,|z|<=2, A in [3|xz|+3, 3|xz|+6], B in [A+1,A+4]: exists t, Parikh(t)=(A,B), xtz notin L5")
    fails=0; tot=0
    W=[''.join(t) for L in range(3) for t in itertools.product('ab',repeat=L)]
    for x in W:
        for z in W:
            m=3*len(x+z)+3
            for A in range(m,m+4):
                for B in range(A+1,A+5):
                    tot+=1
                    hit=False
                    for j in range(A):   # the explicit witness of the proof: b a^{j+1} (b a)^{A-j-1} b^{rest}
                        t='b'+'a'*(j+1)+'ba'*(A-j-1)+'b'*(B-(A-j))
                        assert t.count('a')==A and t.count('b')==B
                        if not inL5(x+t+z): hit=True; break
                    if not hit: fails+=1; print("  FAIL",x,z,A,B)
    print("  cases",tot,"fails",fails)

if __name__=="__main__":
    part_a(int(sys.argv[1]) if len(sys.argv)>1 else 16)
    part_b(); part_c(); part_d()
