def primitive(w):
    n=len(w)
    if n==0: return False
    return (w+w).find(w,1)==n
