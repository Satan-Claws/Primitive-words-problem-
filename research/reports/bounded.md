# Agent "bounded": report (INTERIM CHECKPOINT, written before further work)

Status so far: **(iii) partial results / evidence only.** No proof of the conjecture, no barrier theorem yet.
Scripts: `scripts/bounded/`. Literature could not be opened (publi.math.unideb.hu and arxiv.org are outside the
session's allowed network domains); literature facts below are from search snippets only and are marked as such.

Notation. n >= 2. For a divisor d of n, V_d = { x in Q^n : x_i = x_{i+d} for all i (indices mod n) }.
D(n) = { n/p : p prime, p | n }. E_n = { x in N^n : x not in V_d for all d in D(n) } (primitive sequences).
A finite set P of vectors of N^n is *stratified* if every p in P has at most two nonzero coordinates and there
are no p, p' in P and i<j<k<l with p_i p_k p'_j p'_l != 0. A *stratified linear set* is c + N P with P stratified.

## 1. Set-up lemmas

**L1 (Ginsburg for arbitrary words). PROVED from the distinct-letter version (FROM LITERATURE: Ginsburg 1966, Thm 5.4.2).**
Let w_1..w_k be words, f(i_1..i_k) = w_1^{i_1}...w_k^{i_k}, L a subset of w_1*...w_k*. Then L is CF iff the FULL
preimage f^{-1}(L) is a finite union of stratified linear sets.
Proof. Let h(c_j) = w_j for new distinct letters c_j. L' = h^{-1}(L) ∩ c_1*...c_k* has exponent set f^{-1}(L). If L is
CF so is L' (inverse homomorphism, intersection with regular); apply the distinct-letter theorem. Conversely L = h(L').

**L2. PROVED.** w = a b^{x_1} ... a b^{x_n} is primitive iff (x_1..x_n) is primitive as a word over N, i.e. x in E_n.
(Any root of w starts with a, so w = u^k forces k | n and x to have period n/k.) Viewing (ab*)^n inside
a* b* a* b* ... (2n blocks) the a-exponents are fixed to 1, so periods vanish there; hence
Q_n := Q ∩ (ab*)^n is CF iff E_n is a finite union of stratified linear sets in N^n.

**L3 (prime powers). PROVED.** If n = p^h then E_n = union over i<j, j ≡ i mod n/p of {x_i < x_j} ∪ {x_i > x_j},
and {x_i > x_j} = e_i + N e_i + N(e_i+e_j) + sum_{k != i,j} N e_k is stratified linear. So Q_n is CF.

**L4 (disjoint non-crossing witnesses). PROVED.** If W is a set of pairwise DISJOINT, pairwise non-crossing pairs
{i,j}, then T_W = {x : x_i != x_j for all {i,j} in W} is a finite union of stratified linear sets (product of the
sets in L3 over disjoint coordinate sets; the supports are the pairs of W, which do not cross).

**L5 (shared endpoints are NOT harmless). PROVED.** The following sets are not finite unions of stratified linear sets:
 (a) {(a,b,c) : a > b, a > c};  (b) {(a,b,c) : b < a < c};  (c) {(a,b,c,d) : a > c, b > d};
 (d) {(a,b,c) : a != b, a != c}.
Proofs. (a) In a linear set S inside the set every period p has p_a >= p_b and p_a >= p_c (else iterate p). A 2-sparse
period with p_b > 0 has support {a,b}, with p_c > 0 support {a,c}; so on S, a >= b + c - const; the points (N,N-1,N-1)
are not covered. (b) p_b <= p_a <= p_c for all periods, so p_b > 0 forces 3 nonzero entries: b is bounded on S; the
points (N, N-1, N+1) are not covered. (c) p_c > 0 forces support {a,c}, p_d > 0 forces support {b,d}; these cross, so on
each S one of c, d is bounded; (N,N,N-1,N-1) not covered. (d) by Lemma L6 below applied with the three coordinates
(family (N, N+L, N+L)): span(P_1) has dimension >= 2 and would have to equal both planes {a=b} and {a=c}.
Consequence: the scout's "non-crossing mismatch pairs, shared endpoints allowed" statement does NOT by itself give
context-freeness of Q_n: {x : x_i != x_j, x_i != x_k} is not stratified. Only pairwise disjoint non-crossing pairs (L4)
give a stratified piece directly. (Example: x = (1,0,0,0,0,0), n = 6: every mismatch pair contains coordinate 1.)

## 2. The near-constant pumping criterion

**L6 (near-constant criterion). PROVED (argument below).** Suppose there is delta in Z^n, delta not in V_d for every
d in D(n), such that for EVERY stratified finite P_1 ⊂ N^n with 1 = (1,..,1) a strictly positive rational combination
of all elements of P_1, there is d in D(n) with delta in span_Q(P_1) + V_d. Then E_n is not a finite union of stratified
linear sets (so Q_n, hence Q, is not CF).
Proof. Assume E_n = S_1 ∪ ... ∪ S_m, S_k = c_k + N P^(k) stratified. There are finitely many subsets P_1 of the P^(k);
for each P_1 and d with delta in span(P_1)+V_d fix a rational decomposition delta = sum r_j p_j + v; let L be a common
multiple of all denominators. Consider y_N = N·1 + L·delta (N large so y_N >= 0). y_N is primitive (D_d y_N = L D_d delta != 0).
Some S_k contains y_N for infinitely many N; by Dickson's lemma there are N < N' with representations lambda <= lambda'
(componentwise), so sum (lambda'-lambda)_j p_j = (N'-N)·1. Let P_1 = {p_j : lambda'_j > lambda_j}; it is stratified and 1 is
a strictly positive combination of P_1. Take d with delta in span(P_1) + V_d: L delta = sum (L r_j) p_j + L v with L r_j in Z
and L v in V_d ∩ Z^n. For t large, mu_j := -L r_j + t (lambda'-lambda)_j >= 0, and
y_N + sum mu_j p_j = N·1 + L v + t (N'-N)·1 is in V_d, i.e. is a non-primitive point of S_k. Contradiction.

**L7 (structure of span(P_1)). PROVED.** For P_1 as in L6 the connected components C of the support graph form a
non-crossing partition of [n], and span(P_1) = ∩_C ker g_C over the components C whose span has codimension 1 in Q^C,
where g_C is supported exactly on C, sum of g_C over C is 0 and g_C changes sign along every edge. The smallest spans are
the non-crossing perfect matchings M (g = e_i^* - e_j^*, span(M) = {x : x_i = x_j for {i,j} in M}).
So delta is "escaped" by (pi,g) via d iff some f in span{g_C} sums to zero on every residue class mod d and f(delta) != 0.

**C1 (the criterion L6 can NOT fire for small n). COMPUTER-CHECKED, exact rational arithmetic.**
For n = 6, 10, 12, 14, 18, 20 there is no delta as in L6: already a handful of non-crossing perfect matchings M_1..M_r
satisfy: every delta outside the union of the V_d lies outside span(M_i)+V_d for all d in D(n), for some i. (So every
near-constant family N·1 + delta is covered by a stratified linear set delta' + N{e_i+e_j : {i,j} in M_i} ⊆ E_n.)
Scripts: `arr2.py` (subspace-arrangement engine), `near_constant.py`; certificates `cert_nearconst_<n>.json`.
For n = 30 the same was observed modulo the prime 2^31-1 only (`arrangement_rand.py 30 400`: family dies after 18
random matchings) -- NOT yet re-verified over Q at the time of this checkpoint.

**C2. COMPUTER-CHECKED.** `oriented.py 6`: for the two-scale family 1·N + eps·v (v a generic total order), the
restricted strategy "non-crossing perfect matching with pairs oriented by v and a directed cycle in every quotient graph
mod d" fails for 72 of the 720 orders v when n = 6. Since Q_6 is CF (literature), this only shows that this restricted
strategy class is insufficient; it is NOT an obstruction.

## 3. Literature status (snippets only, NOT verified against the papers)
- Kászonyi–Katsura conjecture: Q_n CF for all n. Proved for n = p^r, p^r q^s, and three prime powers (possibly with
  side conditions). A snippet of Kászonyi (Publ. Math. Debrecen 2010) states "if n = p_1^{f_1}...p_k^{f_k} and
  sum 1/p_i < 4/5 then Q_n is CF" -- note 1/2+1/3+1/5 > 4/5, so that statement does not cover n = 30.

(Sections on further work follow below once done.)
