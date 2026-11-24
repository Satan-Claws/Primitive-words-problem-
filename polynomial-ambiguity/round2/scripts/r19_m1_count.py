"""r19_m1_count.py -- exact check of the left-tilted segment count (Lemma TS, r19_m1.md).

For a grammar G and an SCC T, count exactly
  Tot(n, a) = #{(tree of length n rooted at S, T-segment on a root path) : left-sibling letters of segment = a}
(an upper bound for the number of trees whose pi_h-segment in T has left part a), and compare with 2^n.
Lemma TS predicts  Tot(n, >=a) <= C * n^c * 2^n * exp(-theta a)  with theta from rho(M_theta(1/2)) < 1.
Also prints the prefix-count of the left labels (no gain for the audit example).
"""
import math, sys
import numpy as np

N = int(sys.argv[1]) if len(sys.argv) > 1 else 42

def tree_counts(G):
    F = {X: [0] * (N + 1) for X in G}
    for n in range(1, N + 1):
        for X in G:
            s = 0
            for rhs in G[X]:
                s += word_count(rhs, F, n)
            F[X][n] = s
    return F

def seq_counts(syms, F, upto):
    """counts[l] = number of tree tuples for symbol string syms with total yield l (uses F[.][<=l])."""
    c = [0] * (upto + 1); c[0] = 1
    for s in syms:
        nc = [0] * (upto + 1)
        if s in ('a', 'b'):
            for l in range(upto): nc[l + 1] += c[l]
        else:
            for l in range(upto + 1):
                if c[l]:
                    for k in range(1, upto - l + 1): nc[l + k] += c[l] * F[s][k]
        c = nc
    return c

def word_count(rhs, F, n):
    # F[.][<n] known; rhs has >=2 symbols or terminals (no unit rules, eps-free) so components < n
    return seq_counts(rhs, F, n)[n]

def analyse(name, G, T, S, note):
    F = tree_counts(G)
    # one-step T-contexts M[X][Y][a][b]
    M = {(X, Y): np.zeros((N + 1, N + 1), dtype=object) for X in T for Y in T}
    for X in T:
        for rhs in G[X]:
            for j, s in enumerate(rhs):
                if s in T:
                    L = seq_counts(rhs[:j], F, N); R = seq_counts(rhs[j + 1:], F, N)
                    for a in range(N + 1):
                        if L[a]:
                            for b in range(N + 1 - a): M[(X, s)][a, b] += L[a] * R[b]
    # C = sum_r M^r (contexts X ->* Y inside T), by increasing a+b
    C = {(X, Y): np.zeros((N + 1, N + 1), dtype=object) for X in T for Y in T}
    for X in T: C[(X, X)][0, 0] = 1
    for tot in range(1, N + 1):
        for a in range(tot + 1):
            b = tot - a
            for X in T:
                for Z in T:
                    s = 0
                    for Y in T:
                        m = M[(X, Y)]; c = C[(Y, Z)]
                        for a1 in range(a + 1):
                            for b1 in range(b + 1):
                                if a1 + b1 and m[a1, b1] and c[a - a1, b - b1]:
                                    s += m[a1, b1] * c[a - a1, b - b1]
                    C[(X, Z)][a, b] = s
    # rho(M_theta(1/2)) on truncation
    def rho(th):
        K = np.array([[sum(float(M[(X, Y)][a, b]) * (math.exp(th) / 2) ** a * 0.5 ** b
                            for a in range(N + 1) for b in range(N + 1 - a)) for Y in T] for X in T])
        return max(abs(np.linalg.eigvals(K)))
    # outer: root S = X_top in T (outer context trivial) -- outer factor is poly*2^l by Lemma TS step 1
    Tot = np.zeros((N + 1, N + 1), dtype=object)  # [n][a]
    for X in T:
        if X != S: continue
        for Z in T:
            c = C[(X, Z)]
            for a in range(N + 1):
                for b in range(N + 1 - a):
                    if c[a, b]:
                        for li in range(1, N + 1 - a - b): Tot[a + b + li, a] += c[a, b] * F[Z][li]
    print(f"== {name}: {note}")
    print("   rho(M_theta(1/2)) theta=0,0.05,0.1:", " ".join(f"{rho(t):.3f}" for t in (0, .05, .1)))
    lo, hi = 0.0, 2.0
    for _ in range(40):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if rho(mid) < 1 else (lo, mid)
    print(f"   theta* (rho(M_theta*)=1, truncated at N): {lo:.3f}  -> predicted decay e^-theta* = {math.exp(-lo):.3f}")
    n = N
    tot = sum(Tot[n]); print(f"   n={n}: trees={tot}, trees/2^n={tot / 2 ** n:.3g}")
    line = []
    for a in (0, 3, 6, 9, 12, 15, 18):
        if a > n: break
        r = sum(Tot[n][a:]) / 2 ** n
        line.append(f"a>={a}:{r:.2e}")
    print("   Tot(n,>=a)/2^n:", " ".join(line))
    # tilted sums  S_theta(n) = sum_a Tot(n,a) e^{theta a} / 2^n : bounded in n iff theta < theta*
    for th in (lo / 2, 2 * lo):
        vals = [sum(Tot[m][a] * math.exp(th * a) for a in range(m + 1)) / 2 ** m for m in (16, 32, 48, N)]
        print(f"   S_theta(n) theta={th:.3f}, n=16,32,48,{N}:", " ".join(f"{v:.3g}" for v in vals))
    return Tot

# G1: audit example with a critical exit Z (mass carrier).  T = {X}; left parts a/b free, right part aa forced.
G1 = {'X': [('a', 'X', 'a', 'a'), ('b', 'X', 'a', 'a'), ('Z',)], 'Z': [('a', 'Z'), ('b', 'Z'), ('a',)]}
# unit rule X->Z: handle by inlining Z's rules into X's exit
G1 = {'X': [('a', 'X', 'a', 'a'), ('b', 'X', 'a', 'a'), ('a', 'Z'), ('b', 'Z'), ('a',)],
      'Z': [('a', 'Z'), ('b', 'Z'), ('a',)]}
# G2: light left side nonterminal C (a^k b a^k), right part light D (a^k b) ; positive-drift cycles available
G2 = {'X': [('C', 'X', 'D'), ('b', 'X', 'a'), ('a', 'Z'), ('b', 'Z'), ('a',)],
      'C': [('a', 'C', 'a'), ('b',)], 'D': [('a', 'D'), ('b',)],
      'Z': [('a', 'Z'), ('b', 'Z'), ('a',)]}
# G3: two-NT subcritical linear SCC, left letters free, right companion of length 1 (barely subcritical)
G3 = {'X': [('a', 'Y', 'a'), ('b', 'X', 'a'), ('a', 'Z'), ('b', 'Z')],
      'Y': [('a', 'X', 'b'), ('b', 'Y', 'b'), ('a',)],
      'Z': [('a', 'Z'), ('b', 'Z'), ('a',)]}
# G4: light nonlinear SCC (M1'): X -> aXXa | bX a a | b | baa ; radius > 1/2
G4 = {'X': [('a', 'X', 'X', 'a'), ('b', 'X', 'a', 'a'), ('b',), ('b', 'a', 'a')]}
# G5: nonlinear, non-critical, heavy (critical, finite-mass) exit material: nonempty Dyck P below
G5 = {'X': [('a', 'X', 'X', 'a', 'a'), ('b', 'X', 'a', 'a'), ('P',)],
      'P': [('a', 'P', 'b', 'P'), ('a', 'b', 'P'), ('a', 'P', 'b'), ('a', 'b')]}
G5['X'] = [r for r in G5['X'] if r != ('P',)] + G5['P'][:]  # inline unit exit X->P

if __name__ == '__main__':
    analyse('G1', G1, ['X'], 'X', 'audit M1 example X->aXaa|bXaa + critical exit Z')
    analyse('G2', G2, ['X'], 'X', 'light left nonterminal C, light right D, positive cycle (C,D)')
    analyse('G3', G3, ['X', 'Y'], 'X', 'two-NT linear SCC, right companion length 1')
    analyse('G4', G4, ['X'], 'X', 'M1prime: light nonlinear SCC')
    analyse('G5', G5, ['X'], 'X', 'M1prime: noncritical nonlinear, critical Dyck exit (finite mass)')
