import sys
from fracpos import *
n=int(sys.argv[1])
tot,unc=coverage(n)
def maxperstretch(c):
    # longest cyclic factor (length<=n) with period <= len/2 ... report (len, period) maximizing len with period<=len/3
    n=len(c); cc=c*2; best=(0,0)
    for i in range(n):
        for L in range(n,0,-1):
            x=cc[i:i+L]; d=minper(x)
            if 3*d<=L:
                if L>best[0]: best=(L,d)
                break
    return best
for c in unc: print(c, maxperstretch(c))
