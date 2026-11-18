"""Generalised certificate L_gen = { w in (a*b)+ : exists j with x - e_j a palindrome, x_j>=1, j != k+1-j }
(x = block vector of w, indices 1..k).  CF: linear grammar for block palindromes with a one-bit flag
'extra a emitted in a non-central block'.  Check: all words of L_gen up to length 20 primitive;
covers insertion of one a into any block of u^k whenever beta(u)^k is a cyclically reflection-symmetric
vector (up to rotation, i.e. after Cyc)."""
import itertools
from refute import primitive, blocks
def in_gen(w):
    x = blocks(w)
    if not x: return False
    k = len(x)
    for j in range(k):
        if x[j] >= 1 and j != k - 1 - j:
            z = x[:]; z[j] -= 1
            if z == z[::-1]: return True
    return False
cnt = 0
for n in range(1, 21):
    for t in itertools.product('ab', repeat=n):
        w = ''.join(t)
        if in_gen(w):
            cnt += 1; assert primitive(w), w
print('L_gen words up to length 20:', cnt, 'all primitive')
