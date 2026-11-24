"""audit_m1_words.py -- independent WORD-level check of Lemma TS / Thm M1 (audit of r19_m1).
G1 : S -> b X aa,  X -> a X aa | b X aa | Z,  Z -> aZ | bZ | a      (audit M1 example + critical exit)
     theta* = ln 4 (M_theta = e^theta/4).  left yield of the X-run = i (number of X->.X.. steps).
G1': X -> C X a | Z, C -> aC | b (C = a*b, radius 1), Z as above.
     M_theta = F_C(e^theta/2)/2, F_C(x)=x/(1-x); theta* = ln(4/3).
For every word of length n (brute force over {a,b}^n) compute the max over derivations of the left yield of the
T-run, and the ambiguity; report frac(n, >=a) = #{W : max left yield >= a}/2^n and max ambiguity.
"""
import itertools, math, sys

def g1(w):
    n = len(w); best = -1; amb = 0
    if n < 4 or w[0] != 'b' or not w.endswith('aa'): return best, amb
    for i in range(0, n):
        # w = b u z (aa)^{i+1}, |u| = i, |z| >= 1, z ends in a
        tail = 2 * (i + 1); m = n - 1 - i - tail
        if m < 1: break
        if w[n - tail:] != 'a' * tail: break
        if w[1 + i + m - 1] == 'a':
            amb += 1; best = max(best, i)
    return best, amb

def g1p(w):
    n = len(w); best = -1; amb = 0
    bpos = [k for k, ch in enumerate(w) if ch == 'b']
    for i in range(0, n):
        if i > 0 and w[n - i] != 'a': break
        if i > len(bpos): break
        L = 0 if i == 0 else bpos[i - 1] + 1
        z = w[L:n - i]
        if len(z) >= 1 and z[-1] == 'a':
            amb += 1; best = max(best, L)
    return best, amb

def run(name, f, theta, ns, As):
    print(f"== {name}: theta* = {theta:.4f}, e^-theta* = {math.exp(-theta):.4f}")
    for n in ns:
        cnt = {a: 0 for a in As}; tot = 0; mamb = 0
        for t in itertools.product('ab', repeat=n):
            b, am = f(''.join(t))
            if am:
                tot += 1; mamb = max(mamb, am)
                for a in As:
                    if b >= a: cnt[a] += 1
        fr = ' '.join(f"a>={a}:{cnt[a]/2**n:.2e}" for a in As)
        rat = ' '.join(f"{(cnt[As[j+1]]/cnt[As[j]]) if cnt[As[j]] else 0:.3f}" for j in range(len(As)-1))
        print(f"  n={n} |L_n|/2^n={tot/2**n:.3f} maxamb={mamb} | {fr} | step ratios {rat}")

N = int(sys.argv[1]) if len(sys.argv) > 1 else 20
run("G1 (audit M1 example)", g1, math.log(4), [N - 2, N], [0, 1, 2, 3, 4, 5])
run("G1' (left C=a*b light infinite)", g1p, math.log(4 / 3), [N - 2, N], [0, 2, 4, 6, 8, 10])
