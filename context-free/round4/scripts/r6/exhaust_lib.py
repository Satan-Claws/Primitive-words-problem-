# Exhaustive: all z in ({0,1}^+)^6, |z_i|<=L, primitive, with BOTH count tuples (#0,#1 per segment)
# 2- or 3-periodic (others are covered by the commutative certificate). Check nested pattern with slack.
import itertools, sys
from cover3lib import startmis, endmis, per, prim
def covered(z, slack):
    for S in range(6):
        sq=z[(S+3)%6]
        A=startmis(z[S],sq); B=endmis(z[S],z[(S+2)%6])
        if A and B and min(A)<=max(B)+slack: return True
        C=startmis(z[S],z[(S-2)%6]); D=endmis(z[S],sq)
        if C and D and min(C)<=max(D)+slack: return True
    return False
