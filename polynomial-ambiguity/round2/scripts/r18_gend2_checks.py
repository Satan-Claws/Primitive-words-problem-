"""r18_gend2 checks.
(1) Lemma RP bookkeeping: W' = W[0,s) u W[s,e) alpha x beta W[e,n) with x V-level (suffix walk <= K).
    If W' in G^- then A_W(k) <= max_{j<=n-e} B_W(j) + |beta| + |u| + K for all k <= e.
(2) Rise-bounded words: #{w in {a,b}^h : P(j)-P(i) <= R for all i<j}: DP vs brute force (small h),
    spectral radius rho_R of the transfer matrix = 2cos(pi/(2R+3)), so 2 - rho_R ~ pi^2/(4R^2).
Steps +-1 (a=+1, b=-1). Run: .venv/bin/python scripts/r18_gend2_checks.py
"""
import random, itertools, math
import numpy as np

def walk(w):
    P = [0]
    for ch in w:
        P.append(P[-1] + (1 if ch == 'a' else -1))
    return P

def in_Gminus(w):
    n = len(w); P = walk(w)
    for k in range(1, n // 2 + 1):
        if not (P[k] < P[n] - P[n - k]):
            return False
    return True

def Vlevel_word(L, K, rng):
    # random word whose suffix walk D(x)-P_x(|x|-j) stays <= K: build reversed walk
    rev = []; h = 0
    for _ in range(L):
        ch = rng.choice('ab')
        if ch == 'a' and h + 1 > K:
            ch = 'b'
        h += 1 if ch == 'a' else -1
        rev.append(ch)
    return ''.join(reversed(rev))

def check1(trials=200000, seed=1):
    rng = random.Random(seed)
    hits = viol = checks = 0
    for _ in range(trials):
        n = rng.randint(4, 16)
        W = ''.join(rng.choice('ab') for _ in range(n))
        if not in_Gminus(W) and rng.random() < 0.9:
            continue
        s = rng.randint(0, n); e = rng.randint(s, n)
        u = ''.join(rng.choice('ab') for _ in range(rng.randint(0, 2)))
        al = ''.join(rng.choice('ab') for _ in range(rng.randint(0, 2)))
        be = ''.join(rng.choice('ab') for _ in range(rng.randint(0, 2)))
        K = rng.randint(0, 2)
        x = Vlevel_word(n + 2 * len(u) + 4 + rng.randint(0, n), K, rng)
        Wp = W[:s] + u + W[s:e] + al + x + be + W[e:]
        if not in_Gminus(Wp):
            continue
        hits += 1
        P = walk(W)
        H = max(P[n] - P[n - j] for j in range(0, n - e + 1))
        for k in range(0, e + 1):
            checks += 1
            if P[k] > H + len(be) + len(u) + K:
                viol += 1
    return hits, checks, viol

def rise_count_dp(h, R):
    # state r = P(j) - min_{i<=j} P(i) in [0,R]
    v = np.zeros(R + 1, dtype=object); v[0] = 1
    for _ in range(h):
        nv = np.zeros(R + 1, dtype=object)
        for r in range(R + 1):
            if v[r] == 0: continue
            if r + 1 <= R: nv[r + 1] += v[r]
            nv[max(r - 1, 0)] += v[r]
        v = nv
    return int(sum(v))

def rise_count_brute(h, R):
    c = 0
    for t in itertools.product('ab', repeat=h):
        P = walk(t); m = 0; ok = True
        for p in P:
            m = min(m, p)
            if p - m > R: ok = False; break
        c += ok
    return c

def rho(R):
    M = np.zeros((R + 1, R + 1))
    for r in range(R + 1):
        if r + 1 <= R: M[r, r + 1] += 1
        M[r, max(r - 1, 0)] += 1
    return max(abs(np.linalg.eigvals(M)))

if __name__ == '__main__':
    hits, checks, viol = check1()
    print(f"(1) RP bookkeeping: {hits} instances with W' in G^-, {checks} k-checks, {viol} violations")
    ok = all(rise_count_dp(h, R) == rise_count_brute(h, R) for h in range(1, 15) for R in range(0, 5))
    print(f"(2a) rise-count DP == brute force (h<=14, R<=4): {ok}")
    for R in [1, 2, 4, 8, 16, 32, 64]:
        r = rho(R)
        print(f"(2b) R={R:3d} rho={r:.6f}  2cos(pi/(2R+3))={2*math.cos(math.pi/(2*R+3)):.6f}  (2-rho)R^2={(2-r)*R*R:.3f}")
