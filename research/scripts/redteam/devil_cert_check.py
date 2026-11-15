# Redteam: devil C1 (min certificate = omega+1 attained), C4 (universal mismatch exceptions), C5 (words in W_n)
import sys, itertools, numpy as np
from rt_common import *
for n in [int(a) for a in sys.argv[1:]]:
    P=primes_of(n); k=len(P); D=[n//p for p in P]
    # basis of W_n (real span of d-periodic vectors)
    B=[]
    for d in D:
        for r in range(d): B.append([1.0 if i%d==r else 0.0 for i in range(n)])
    B=np.array(B); rk=np.linalg.matrix_rank(B)
    need_more=0; univ_fail=0; inW=0; below=0; tot=0
    pos=list(range(n))
    for w in range(1<<n):
        s=to_str(w,n)
        if not is_primitive_str(s): continue
        tot+=1
        bits=[(w>>i)&1 for i in range(n)]
        if not any(all(bits[i]!=bits[(i+d)%n] for d in D) for i in range(n)): univ_fail+=1
        if np.linalg.matrix_rank(np.vstack([B,np.array(bits,float)]))==rk: inW+=1
        def cert(S):
            return all(any(i%d==j%d and bits[i]!=bits[j] for i in S for j in S) for d in D)
        if any(cert(S) for S in itertools.combinations(pos,k)): below+=1
        if not any(cert(S) for S in itertools.combinations(pos,k+1)): need_more+=1
    print('n',n,'primitive',tot,'cert<=omega',below,'need>omega+1',need_more,'univ-mismatch fails',univ_fail,'in W_n',inW)
