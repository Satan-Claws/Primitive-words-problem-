"""r10_heavy_survivors.py -- explicit G- violations at n=28 for the two leading N=16 survivors of r10_heavy_search.py
(margin p=bb,q=aa only delays failure)."""
def inG(x):
    n = len(x); d = 0
    for k in range(n // 2):
        d += (x[k] == 'a') - (x[n - 1 - k] == 'a')
        if d >= 0: return False
    return True
E6 = 'b' * 6 + 'a' * 6                          # an E-block (b D a)
w1 = 'bb' + 'bb' + 'a' * 10 + E6 + 'aa'          # S->bb X aa, X->X a | X E | bb : V = a^10 E6
w2 = 'bb' + E6[::-1].translate(str.maketrans('ab', 'ba')) + 'b' * 10 + 'aa' + 'aa'  # mirror: X->bX|EX|aa
for w in (w1, w2): print(len(w), w, 'in G-:', inG(w))
