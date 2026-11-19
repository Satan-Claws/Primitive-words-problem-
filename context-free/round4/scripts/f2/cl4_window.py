# Lemma W check: w = a u u'' where u'' = u except in an interval window. If w = z^k (k>=2) then
# k odd >= 3 and the cyclic word z has at most 2|D| letter changes, D = {1<=j<=L : w_j != w_{j+L}}.
import itertools, sys
L = int(sys.argv[1]) if len(sys.argv) > 1 else 12
mmax = int(sys.argv[2]) if len(sys.argv) > 2 else 3
def root(w):
    n = len(w); i = (w + w).find(w, 1); return i if i < n else n
def cyc_changes(z):
    return sum(z[i] != z[(i+1) % len(z)] for i in range(len(z)))
powers = 0; viol = 0; maxratio = 0
for tup in itertools.product('ab', repeat=L-1):
    u = ''.join(tup) + 'b'
    for start in range(L):           # window in second copy (positions of u'')
        for ln in range(1, mmax+1):
            if start + ln > L: break
            for x in itertools.product('ab', repeat=ln):
                x = ''.join(x)
                u2 = u[:start] + x + u[start+ln:]
                if u2 == u: continue
                w = 'a' + u + u2
                M = root(w)
                if M < len(w):
                    powers += 1
                    k = len(w) // M
                    D = sum(w[j] != w[j+L] for j in range(1, L+1))
                    z = w[:M]
                    if k % 2 == 0 or k < 3 or cyc_changes(z) > 2*D: viol += 1; print('VIOL', w, M, D)
print('L', L, 'mmax', mmax, 'powers found', powers, 'violations', viol)
