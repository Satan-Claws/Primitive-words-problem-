# Independent helpers (redteam). Words of length n are ints; bit i = letter at position i.
def primes_of(n):
    ps=[];m=n;p=2
    while p*p<=m:
        if m%p==0:
            ps.append(p)
            while m%p==0: m//=p
        p+=1
    if m>1: ps.append(m)
    return ps
def is_primitive_str(s):
    # classical test: s primitive iff s not found in (s+s)[1:-1]
    return len(s)>0 and (s+s).find(s,1)==len(s)
def to_str(w,n): return ''.join('b' if (w>>i)&1 else 'a' for i in range(n))
def nonprim_words(n):
    """all non-primitive words of length n as ints, via v^p, p prime | n"""
    S=set()
    for p in primes_of(n):
        d=n//p
        for v in range(1<<d):
            w=0
            for t in range(p): w|=v<<(t*d)
            S.add(w)
    return S
