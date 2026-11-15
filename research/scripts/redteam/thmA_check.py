# Redteam check of rectangles Thm A (and devil R1): for a prefix (cyclic arc) of length L,
# number of completions making the word non-primitive. Uses only the set of non-primitive words.
import sys
from rt_common import *
N=int(sys.argv[1]) if len(sys.argv)>1 else 34
for n in range(2,N+1):
    NP=nonprim_words(n)
    # sanity vs brute-force string test for small n
    if n<=14:
        for w in range(1<<n):
            assert (w in NP)==(not is_primitive_str(to_str(w,n))),(n,w)
    L=(2*n)//3
    maxc={}
    for l in range(1,n):
        mask=(1<<l)-1; cnt={}
        for w in NP:
            y=w&mask; cnt[y]=cnt.get(y,0)+1
        maxc[l]=max(cnt.values())
    om=len(primes_of(n))
    # Thm A: unique completion for every l >= floor(2n/3)
    okA=all(maxc[l]<=1 for l in range(L,n))
    # smallest l0 such that all l>=l0 unique
    l0=n-1
    while l0-1>=1 and maxc[l0-1]<=1: l0-=1
    # devil R1(a): inner length m=n-l, if l >= n/p for all p (i.e. l>=n//min p) then <= omega
    pmin=min(primes_of(n))
    okR1a=all(maxc[l]<=om for l in range(1,n) if l>=n//pmin)
    okR1b=True
    if n%2==0 and n>=4:
        okR1b = maxc[n//2-1]<=om+1
    print(n,'omega',om,'L',L,'uniqueFrom',l0,'ThmA',okA,'R1a',okR1a,'R1b',okR1b,
          'maxc@L-1',maxc.get(L-1))
    assert okA and okR1a and okR1b
print("ALL PASS")
