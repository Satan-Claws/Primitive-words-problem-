"""r19_fixes checks (fast, <10 s).
(1) Lemma SP toy: X -> H X | a, H -> aH | bH | a (H critical linear, simple pole).
    trees_X(N)/2^N is a lower bound on max per-word ambiguity at length N: must grow exponentially.
(2) Lemma W toy: blocks U = {b} u {a^k b^k : k>=1} u {(ab)^k b : k>=1}  (light: <=2 words/length,
    every block has D<=0, so every block path has D<=0 = NC).  Exact #U*_l (distinct words, brute force)
    vs 2^l, and the ell^{1/3}-type bound's ingredients: max internal rise vs l.
(3) rho_R = 2cos(pi/(2R+3)) for the rise-bounded transfer matrix (re-check of gend2 input), R<=6.
"""
import itertools, math
import numpy as np

def chk1():
    N = 60
    h = [0] + [2 ** (j - 1) for j in range(1, N + 1)]     # |L(H) cap Sigma^j| = 2^{j-1}, H unambiguous
    T = [0] * (N + 1); T[1] = 1                          # X -> a  (length 1)
    for n in range(2, N + 1):
        T[n] = sum(h[j] * T[n - j] for j in range(1, n))
    out = [(n, T[n] / 2 ** n) for n in (10, 20, 40, 60)]
    print("(1) trees_X(N)/2^N:", ", ".join(f"N={n}: {r:.3g}" for n, r in out))
    r = (T[60] / T[40]) ** (1 / 20) / 2
    print(f"    per-letter growth of trees/2^N ~ {r:.4f} (>1 => exponential ambiguity)")

def chk2(L=18):
    U = {"b"}
    for k in range(1, L + 1):
        U.add("a" * k + "b" * k); U.add("ab" * k + "b")
    U = {u for u in U if len(u) <= L}
    def inUstar(w):
        ok = [False] * (len(w) + 1); ok[0] = True
        for j in range(1, len(w) + 1):
            for i in range(j):
                if ok[i] and w[i:j] in U:
                    ok[j] = True; break
        return ok[-1]
    res = []
    for l in range(4, L + 1, 2):
        c = sum(1 for t in itertools.product("ab", repeat=l) if inUstar("".join(t)))
        res.append((l, c / 2 ** l))
    print("(2) #U*_l / 2^l:", ", ".join(f"{l}:{r:.3g}" for l, r in res))
    rat = [math.log(res[i][1] / res[i + 1][1]) / 2 for i in range(len(res) - 1)]
    print("    per-letter decay rates:", ", ".join(f"{x:.3f}" for x in rat))

def chk3():
    bad = 0
    for R in range(0, 7):
        M = np.zeros((R + 1, R + 1))
        for r in range(R + 1):
            if r + 1 <= R: M[r, r + 1] += 1
            if r == 0: M[0, 0] += 1
            else: M[r, r - 1] += 1
        rho = max(abs(np.linalg.eigvals(M)))
        if abs(rho - 2 * math.cos(math.pi / (2 * R + 3))) > 1e-9: bad += 1
    print(f"(3) rho_R = 2cos(pi/(2R+3)) for R<=6: {'OK' if bad == 0 else f'{bad} mismatches'}")

if __name__ == "__main__":
    chk1(); chk2(); chk3()
