"""r17_gwordp: tolerance of the fold-centre-escape gain in context size h and level C.
E_n(C,h) = {W : P(j) <= min(C, P(n)+C) for h <= j <= n-h}  (Lemma FR-pos conclusion, Q(C) form).
(1) brute-force check (n<=14): E_n(C,h) subset of F_n(C+2*Delta_h) and |P(n)| <= C + 2h.
(2) Monte Carlo: fraction of uniform words having SOME rotation in E_n(C,h), vs the bound
    (2K+1)*sqrt(2/(pi n)) + 2n exp(-(K-C)^2/(2h)),  K = C + 2 sqrt(h ln n).
"""
import itertools, math, numpy as np
rng = np.random.default_rng(17)

def inE(P, n, C, h):
    mid = P[h:n-h+1]
    return mid.size == 0 or mid.max() <= min(C, P[n] + C)

# (1) brute force
viol = 0; tot = 0
for n in range(4, 15):
    for bits in itertools.product((1, -1), repeat=n):
        P = np.concatenate(([0], np.cumsum(bits)))
        for C in (0, 1, 2):
            for h in range(0, n // 2 + 1):
                if not inE(P, n, C, h):
                    continue
                tot += 1
                D = max(abs(P[j]) + abs(P[n] - P[n - j]) for j in range(h + 1))
                c = C + 2 * D
                if P.max() > min(0, P[n]) + c or abs(P[n]) > C + 2 * h:
                    viol += 1
print(f"(1) brute force n<=14: {tot} (W,C,h) with W in E_n(C,h); violations of E subset F(C+2Delta) or |P(n)|<=C+2h: {viol}")

# (2) Monte Carlo rotation-closure
def rot_hit(w, C, h):
    n = w.size
    S = np.concatenate(([0], np.cumsum(np.concatenate((w, w)))))
    tot = S[n]
    win = np.lib.stride_tricks.sliding_window_view(S[h:], n - 2 * h + 1)[:n]  # rows r: S[r+h .. r+n-h]
    m = win.max(axis=1) - S[:n]
    return bool(np.any(m <= min(C, tot + C)))

for n in (400, 1600):
    trials = 400 if n == 400 else 150
    W = rng.choice([1, -1], size=(trials, n))
    for C in (0, 3):
        row = []
        for h in (0, int(n ** 0.5), int(n / math.log(n)), n // 8, n // 4):
            frac = np.mean([rot_hit(w, C, h) for w in W])
            K = C + 2 * math.sqrt(max(h, 1) * math.log(n))
            bnd = (2 * K + 1) * math.sqrt(2 / (math.pi * n)) + 2 * n * math.exp(-(K - C) ** 2 / (2 * max(h, 1)))
            row.append(f"h={h}:{frac:.3f}(bnd {min(bnd,1):.2f})")
        print(f"(2) n={n} C={C}: " + "  ".join(row))
