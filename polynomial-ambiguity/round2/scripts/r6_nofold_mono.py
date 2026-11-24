# r6_nofold Lemma M check: G^- (and F_K^-) closed under
#  (i) inserting b at position m <= floor(n/2), (ii) inserting a at position m >= ceil(n/2) (insertion index in w),
#  (iii) a->b at i < n/2, b->a at i >= n/2 (i != centre for odd n handled by i<(n-1)/2 / i>(n-1)/2),
#  (iv) reverse-complement invariance; plus Lipschitz |d_k(w')-d_k(w)|<=r for single-factor deletions.
import itertools
from r6_nofold_slices import Gm, FK, d
def FKm(w):
    n=len(w); lo=-(-n//3); return all(d(w,k)<0 for k in range(lo,n//2+1))
rc=lambda w: ''.join('b' if c=='a' else 'a' for c in reversed(w))
bad={'G':[0]*4,'FK-':[0]*4}; tot=0; lipbad=0
for n in range(2,15):
    for t in itertools.product('ab',repeat=n):
        w=''.join(t)
        for name,f in (('G',Gm),('FK-',FKm)):
            if not f(w): continue
            if name=='G': tot+=1
            for m in range(0,n//2+1):
                if not f(w[:m]+'b'+w[m:]): bad[name][0]+=1
            for m in range(-(-n//2),n+1):
                if not f(w[:m]+'a'+w[m:]): bad[name][1]+=1
            for i in range(n):
                if 2*i<n-1 and w[i]=='a' and not f(w[:i]+'b'+w[i+1:]): bad[name][2]+=1
                if 2*i>n-1 and w[i]=='b' and not f(w[:i]+'a'+w[i+1:]): bad[name][2]+=1
            if f(rc(w))!=True: bad[name][3]+=1
        if n<=12:
            for m in range(n):
                for r in range(1,n-m):
                    w2=w[:m]+w[m+r:]
                    if 2*(m)<=n-r and any(abs(d(w2,k)-d(w,k))>r for k in range(1,len(w2)//2+1)): lipbad+=1
print('|G^-| n<=14:',tot,' violations [insB-left,insA-right,flip,rc]:',bad,' Lipschitz violations:',lipbad)
