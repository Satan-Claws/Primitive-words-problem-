# Markerless l=3 family a(a^p b a^q b a^r b)^k. Candidate certificate:
# class0: y_i=x[3i], y_0-y_{k-1}=1, y_i=y_{k-1-i} (chord sum 3k-3)
# plus optional second class c in {1,2} palindromic w.r.t. chord sum s (adjacent axis, non-crossing with class 0)
import itertools
def periodic(x):
    K=len(x); return any(all(x[j]==x[(j+d)%K] for j in range(K)) for d in range(1,K))
def ok(x,k,extra):
    K=3*k; y=[x[3*i] for i in range(k)]
    if y[0]-y[k-1]!=1 or any(y[i]!=y[k-1-i] for i in range(1,k-1)): return False
    if extra:
        c,s=extra
        for j in range(K):
            if j%3==c:
                j2=s-j
                if 0<=j2<K and x[j]!=x[j2]: return False
    return True
for extra in [None,(1,None),(2,None)]:
    for k in range(2,6):
        K=3*k
        ex=None if extra is None else (extra[0], 3*k-4 if extra[0]==1 else 3*k-2)
        V=3 if K<=9 else 2
        bad=0;tot=0;first=None
        for x in itertools.product(range(V),repeat=K):
            if ok(x,k,ex):
                tot+=1
                if periodic(x):
                    bad+=1; first=first or x
        print('extra',ex,'k',k,'V',V,'tested',tot,'periodic',bad,first)
