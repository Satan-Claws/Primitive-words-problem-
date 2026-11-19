# Independent check of r6's Cover Lemma: every primitive w in R6 lies in C or satisfies some N(S,+-2).
import sys, random
INF=10**9
def startmis(S,X):
    m=[t for t in range(min(len(S),len(X))) if S[t]!=X[t]]
    if len(X)<len(S): m.append(len(X))
    return m
def endmis(S,X):
    off=len(X)-len(S)
    m=[t for t in range(len(S)) if 0<=t+off<len(X) and S[t]!=X[t+off]]
    if len(X)<len(S): m.append(len(S)-len(X)-1)
    return m
class T:
    def __init__(s,segs):
        s.segs=segs; n=len(segs); s.mS={}; s.MS={}
    def minS(s,i,j):
        k=(i,j)
        if k not in s.mS:
            m=startmis(s.segs[i],s.segs[j]); s.mS[k]=min(m) if m else INF
        return s.mS[k]
    def maxE(s,i,j):
        k=(i,j)
        if k not in s.MS:
            m=endmis(s.segs[i],s.segs[j]); s.MS[k]=max(m) if m else -INF
        return s.MS[k]
def per(v):
    p2=all(v[i]==v[(i+2)%6] for i in range(6)); p3=all(v[i]==v[(i+3)%6] for i in range(6))
    return p2 or p3
def Ncover(tab,idx):
    for S in range(6):
        z=idx[S]; p3=idx[(S+3)%6]; p2=idx[(S+2)%6]; m2=idx[(S-2)%6]
        if tab.minS(z,p3)<=tab.maxE(z,p2): return True
        if tab.minS(z,m2)<=tab.maxE(z,p3): return True
    return False
def prim(idx):
    sq=all(idx[i]==idx[(i+3)%6] for i in range(6))
    cu=all(idx[i]==idx[(i+2)%6] for i in range(6))
    return not(sq or cu)
