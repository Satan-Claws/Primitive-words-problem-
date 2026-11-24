"""l6_thmS_check.py -- sanity checks for the explicit families in reports/l6.md.  [computational]
(1) Theorem S family:  w = a^{L+D} b (a^L b)^5  (D = 0 mod 6, D > 0) is in L6;
    pumping D a's into runs 2 and 4  gives (a^{L+D} b a^L b)^3 : a cube, not a square;
    pumping D a's into run 3         gives (a^{L+D} b a^L b a^L b)^2 : a square, not a cube.
(2) Lemma U family:  u_k = a^6 (b^k a^k)^6 is in L6 and every cyclic factor of length <= k occurs = 0 mod 6 times,
    so u_k escapes every count-split grammar C_k (pieces G_2 n R_3k, G_3 n R_2k, R_2k n R_3k).
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from l6_census import in_L6, is_pow, cyc_counts

def runs_word(x):   # cyclic run vector -> word a^{x0} b a^{x1} b ...
    return ''.join('a'*xi + 'b' for xi in x)

ok = True
for D in (6, 12, 24):
    for L in range(0, 15):
        x = [L+D] + [L]*5
        w = runs_word(x)
        c = runs_word([L+D, L, L+D, L, L+D, L])
        s = runs_word([L+D, L, L, L+D, L, L])
        ok &= in_L6(w) and is_pow(c, 3) and not is_pow(c, 2) and is_pow(s, 2) and not is_pow(s, 3)
print("Theorem S family checks:", ok)
for k in range(1, 8):
    u = 'a'*6 + ('b'*k + 'a'*k)*6
    good = in_L6(u) and all(v % 6 == 0 for v in cyc_counts(u, k).values())
    print(f"k={k}: |u_k|={len(u)}, in L6 and all <=k cyclic counts = 0 mod 6: {good}")
