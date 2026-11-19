# Abstract model: w = (z1..z6), z_i nonempty words over {0,1}. Primitive iff not square-tuple and not cube-tuple.
# Test simple nested certificate patterns (see r6.md).
import itertools, sys
def startmis(S,X):
    r=[t for t in range(min(len(S),len(X))) if S[t]!=X[t]]
    if len(X)<len(S): r.append(len(X))
    return r
def endmis(S,X):
    d=len(X)-len(S); r=[t for t in range(len(S)) if 0<=t+d<len(X) and S[t]!=X[t+d]]
    if len(X)<len(S): r.append(len(S)-len(X)-1)
    return r
def per(v):
    return (v[0]==v[3] and v[1]==v[4] and v[2]==v[5]) or (v[0]==v[2]==v[4] and v[1]==v[3]==v[5])
def lencert(z):
    return not per([x.count('1') for x in z]) or not per([x.count('0') for x in z])
def covered(z, slack=0):
    if lencert(z): return 'len'
    for S in range(6):
        sq=z[(S+3)%6]
        A=startmis(z[S],sq); B=endmis(z[S],z[(S+2)%6])
        if A and B and min(A)<=max(B)+slack: return 'p+2'
        C=startmis(z[S],z[(S-2)%6]); D=endmis(z[S],sq)
        if C and D and min(C)<=max(D)+slack: return 'p-2'
    return None
def prim(z):
    sq= z[0]==z[3] and z[1]==z[4] and z[2]==z[5]
    cu= z[0]==z[2]==z[4] and z[1]==z[3]==z[5]
    return not(sq or cu)
