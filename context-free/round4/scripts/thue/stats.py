"""How do escapes look?  For each family, count instances where the FIRST certified window is
(a) inside R away from defect, (b) has UF certificate with |delta|<=?, and whether escape exists using only
windows that avoid the defect position entirely."""
from common import *
from survey import defects
for (U, k, rho) in [('abbabaa', 3, 6), ('aababb', 3, 6), (tm(10), 3, 8)]:
    tot = avoid = uf = par = 0
    for (typ, d, W) in defects(U, k):
        if not primitive(W): continue
        for a0 in range(0, len(W) - rho + 1):
            marks = set(range(a0, a0 + rho)); tot += 1
            got = False
            for cuts in windows(W, marks, 3, rho + 4):
                if cuts[0] <= d < cuts[-1]: continue
                loops = [W[cuts[j]:cuts[j+1]] for j in range(3)]
                r = W[cuts[-1]:] + W[:cuts[0]]
                if full_escape(r, loops) is True:
                    got = True
                    if par_cert(r, loops): par += 1
                    elif uf_cert(r, loops, maxlam=len(r)//2): uf += 1
                    break
            avoid += got
    print(U, k, 'instances', tot, 'escape with window avoiding defect', avoid, 'of which PAR', par, 'UF', uf)
