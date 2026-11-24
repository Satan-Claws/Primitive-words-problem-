"""lemmaC_ends: conditional all-N proof of Lemma C for k = 1, 2 (R2/lemmaC.md §4), exact.
Assume H_k: the block structure of rho0 = prod_{j!=k}(1 - X^{p_j}) is  [fixed head blocks] + one middle block +
[mirror tail blocks] (observed for 6 <= N <= 45). Every proper union then reduces (R2/lemmaC.md §3-4) to
  f = A + sgn * X^D * A'(1/X)  ==  0  mod L'_k = (X-1) prod_{j!=k} Phi_{p_j},
with A, A' nonzero head prefixes (fixed polynomials), sgn = +-1, D = deg rho0 (unknown, all residues allowed).
We show: for every (A, A', sgn) there is q in Q_k (small primes != p_k, all dividing P for N >= 6) or q = 1 such
that Phi_q does not divide f for ANY residue D mod q  (so no N can be bad).  Pure-head/pure-tail unions are
handled by width in the report. Exact arithmetic (sympy).
"""
from sympy import symbols, Poly, cyclotomic_poly, rem
X = symbols('X')
HEADS = {1: [[(0, 1)], [(0, 1), (3, -1)], [(0, 1), (3, -1), (5, -1)], [(0, 1), (3, -1), (5, -1), (7, -1), (8, 1)]],
         2: [[(0, 1), (2, -1)], [(0, 1), (2, -1), (5, -1)]]}
Q = {1: [3, 5, 7, 11, 13], 2: [2, 5, 7, 11, 13]}
ok = True
for k in (1, 2):
    for A in HEADS[k]:
        for B in HEADS[k]:
            for sg in (1, -1):
                killers = []
                if sum(v for _, v in A) + sg * sum(v for _, v in B) != 0: killers.append(1)
                for q in Q[k]:
                    Phi = Poly(cyclotomic_poly(q, X), X)
                    if all(not rem(Poly(sum(v * X**e for e, v in A) + sg * sum(v * X**((d - e) % q) for e, v in B), X), Phi).is_zero
                           for d in range(q)):
                        killers.append(q)
                if not killers: ok = False
                print(f'k={k} A={A} A\'={B} sgn={sg:+d}: Phi_q never divides for q in {killers}')
print('ALL CASES KILLED' if ok else 'SOME CASE SURVIVES')
