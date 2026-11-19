"""Test whether F_2 members lie in builder's Cyc(L(S)) (letter-level reflection dominance, a<b)."""
def LY(v):
    n=len(v); s=False
    for i in range(n//2):
        if v[i]>v[n-1-i]: return False
        if v[i]<v[n-1-i]: s=True
    return s
def LS(v): return LY(v) or (len(v)>=1 and LY(v[1:]))
def cycdom(w):
    return any(LS(w[r:]+w[:r]) for r in range(len(w)))
def cycdom_rev(w):  # also with b<a order (swap letters)
    t=w.translate(str.maketrans('ab','ba')); return cycdom(w) or cycdom(t)
if __name__=='__main__':
    miss=[];tot=0
    for p in range(1,9):
        for q in range(1,9):
            for k in range(2,6):
                w='a'+('a'*p+'b'+'a'*q+'b'+'ab')*k; tot+=1
                if not cycdom(w): miss.append((p,q,k))
    print('F_2 tested',tot,'missed by Cyc(L(S)):',len(miss), miss[:10])
