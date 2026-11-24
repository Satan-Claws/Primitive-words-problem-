# P_cop: the coprime sandwich

Notation: Q = primitive words over {a,b}; ψ(w) = (#a w, #b w); g(w) = gcd ψ(w); P = {(x,y) ∈ ℕ² : gcd(x,y) = 1};
Cop = ψ^{-1}(P) = {w : g(w) = 1}. L1 (`R2/cyclic.md`) gives Cop ⊆ Q.
**P_cop**: some CFL L with Cop ⊆ L ⊆ Q has a polynomially ambiguous grammar.
Script: `round2/scripts/pcop_checks.py`.

## 0. Summary

| item | status |
|---|---|
| P1 Cop is not CF (P is not semilinear) | [written proof] |
| P2 Shape of a semilinear S with P ⊆ S ⊆ ψ(Q): it misses only finitely many points, finitely many lines through 0, and finitely many sets qℤ² | [written proof] + [computational] (ray and 2-period lemmas, 0 mismatches on about 38k random sets) |
| P3 Parikh constraints force nothing at gcd ≥ 2: the step-1 hypothesis "same hardness as Q ∩ (Parikh class, gcd g)" is **false** | [written proof] (trivial example) |
| P4 Equivalence: full ⇒ P_cop. The route P_cop + (grammar for Q∩{g≥2}) ⇒ full is circular (T1). No §5 transfer gives P_cop ⇒ full. | [written proof] (circularity, no-go for §5 transfers) / open (equivalence itself) |
| **U. No unambiguous CFL L has Cop ⊆ L ⊆ Q.** This strictly strengthens Petersen (1996). | [written proof], not audited |
| Extension of U to polynomial ambiguity (that is, ¬P_cop) | **gap**: exactly the count-sandwich trap (§6). See §5. |

Verdict on the task's question 2: P_cop is **not known to be equivalent** to the full problem. It is a weaker affirmative and a stronger
negative. Its finite-level analogue (unambiguous) is now resolved negatively (U), by a cross-slice argument
that is not slice-blind. The polynomial version remains open.

## 1. P1: Cop is not context-free

By Parikh's theorem [published], ψ(L) is semilinear for every CFL L. So it suffices that P is not semilinear.
Semilinear sets are exactly the Presburger-definable sets (Ginsburg–Spanier 1966) [published], and they are closed under
Boolean operations and projection. If P were semilinear, then so would be
  T = {n ≥ 2 : ∀m (1 ≤ m < n → (n,m) ∈ P)} = the set of primes.
Semilinear subsets of ℕ are ultimately periodic: there are N and d ≥ 1 with n ∈ T ⇔ n+d ∈ T for n ≥ N.
Take a prime n₀ ≥ N. Then n₀ + n₀d = n₀(1+d) ∈ T, but it is composite, which is a contradiction. ∎

## 2. P2: semilinear supersets of P inside ψ(Q)

Note ψ(Q) = ℕ² ∖ ({(0,0)} ∪ {(d,0),(0,d) : d ≥ 2}). Every nonaxial vector has a primitive word, for example a^x b^y.

**Ray lemma.** Let R = {c + s·p : s ∈ ℕ} with p ≠ 0 and D = det(p, c) ≠ 0 (R is non-radial). If every point of R has gcd ≥ 2,
then a single prime q divides c and p.
*Proof.* Put u(s) = c + s p. Then p₂u₁(s) − p₁u₂(s) = ±D, so gcd u(s) divides D. Hence only the finitely many primes q | D occur.
For q | D, the set {s : q | u(s)} is either ℕ (when q | c and q | p) or contained in one residue class mod q. If no q divides both
c and p, then by CRT there is an s that avoids one residue class mod each such q, and gcd u(s) = 1. ∎

**Plane lemma.** Let K = c + ℕp₁ + ℕp₂ with det(p₁,p₂) ≠ 0. If every point of K∖{0} has gcd ≥ 2, then a single prime q divides c, p₁ and p₂.
*Proof.* For t ∈ ℕ, the ray R_t = (c + t p₂) + ℕp₁ is non-radial except for at most one t, since det(p₁, c + t p₂) is affine in t
with nonzero slope. By the ray lemma, every good t has a prime q_t | p₁ with q_t | c + t p₂. So q_t lies in the finite set F
of primes dividing p₁. For q ∈ F with q ∤ p₂, the admissible t lie in at most one class mod q. If no q ∈ F divides both
p₂ and c, then CRT gives a good t that avoids all of them, which is a contradiction. ∎

**P2.** Let S be semilinear with P ⊆ S. Write ℕ²∖S as a finite union of linear sets with linearly independent periods
(Eilenberg–Schützenberger / Ito 1969 [published]). Each piece lies in {gcd ≥ 2} ∪ {0}. By the two lemmas,
  ℕ²∖S ⊆ F ∪ (finitely many lines through 0) ∪ ⋃_{q∈Π} qℤ²
for a finite set F and a finite set Π of primes.
So S contains every vector off finitely many slopes whose gcd has no prime factor in Π. In particular, S contains vectors whose gcd has
arbitrarily many prime factors.
The bound is sharp in kind: ℕ²∖2ℤ² ∪ P is semilinear and ⊇ P. [computational check: `pcop_checks.py` (a)]

## 3. P3: the Parikh constraint forces no content

L₀ = {a,b} ∪ a⁺b⁺ is unambiguous, L₀ ⊆ Q, and ψ(L₀) = ψ(Q).
So "ψ(L) ⊇ P, semilinear" forces only **nonemptiness** of L at the vectors in P2. It does not force any Q ∩ ψ^{-1}(v) structure.
The hypothesis that L must carry "the same hardness as Q ∩ (Parikh class with gcd g)" is false at the Parikh level.
Every constraint on L ∖ Cop comes from L being a single CFL that contains **all** of Cop. Pumping coprime words lands
on gcd ≥ 2 vectors, and those landings must be primitive. That is a non-CF-type (pumping) argument, and it would prove more than
needed: "no CF sandwich" implies Q is not CF, which is excluded as a target by §3.

## 4. P4: equivalence

- full ⇒ P_cop: take L = Q.
- Combination route: Q = L(H) ∪ (Q ∩ {g ≥ 2}). A polynomially ambiguous grammar for Q ∩ {g ≥ 2} (or any L ⊆ Q covering it with
  polynomial class mass) is **already** the full problem by T1 (`R2/cyclic.md`). So "P_cop ∧ X ⇒ full" holds only for X ≡ full.
  The union route is circular.
- No-go for §5 transfers. Each allowed transfer (DFA product, cyclic closure, CNF, pullback along a code h) maps words to words with
  g(source) | g(target) (L2, and ψ is preserved by products and rotations). A grammar whose only guarantee is "contains every
  g = 1 word" therefore yields, after any chain of transfers, only guarantees on g = 1 words (pullback of g(h(u)) = 1 forces g(u) = 1).
  Coprime words are all in Q, so membership information at g ≥ 2 cannot be imported from H. Some new transfer is needed.
- Cheap equivalent form: h(x) = ab, h(y) = abb has det 1. Then h(Cop) = Cop ∩ (ab+abb)*, and pullback along h is exact,
  so P_cop ⇔ P_cop on the slice (ab+abb)*. This is the analogue of §5.4. By Theorem C, P_cop ⇔ some CFL L ⊆ Q meets every coprime class
  with polynomial mass.

**Conclusion: not equivalent by any known reduction.** It is not shown to be strictly easier either, since no polynomially ambiguous
sandwich is known.

## 5. Resolution attempt: Theorem U (unambiguous case) and the exact gap for polynomial ambiguity

**Theorem U.** No unambiguous CFL L satisfies Cop ⊆ L ⊆ Q. More precisely, for every unambiguous CF L ⊆ Q and every
sufficiently large prime p, L misses some word w with #a w = p and gcd(p, #b w) = 1.

*Proof.* Let F(x,y) = Σ_{w∈L} x^{#a w} y^{#b w}. It is algebraic over ℚ(x,y) because L is unambiguous (Chomsky–Schützenberger) [published].
Then G = 1/(1−x−y) − F = Σ e_{ij} x^i y^j, where e_{ij} = #{w ∉ L : ψ(w) = (i,j)} ≥ 0, is algebraic. Suppose Cop ⊆ L ⊆ Q. Then
e_{ij} = 0 whenever gcd(i,j) = 1, and e_{ij} ≥ 1 whenever gcd(i,j) ≥ 2, since v^{g} ∉ Q.
[computational check of these support facts: `pcop_checks.py` (b)]

*Coefficient lemma.* Write G = Σ_i g_i(y) x^i. There are m and a finite set S ⊂ ℂ such that every g_i extends analytically along
every path in ℂ∖S. So the singularities of every g_i lie in S, uniformly in i.
Proof: Let P be the minimal polynomial of G. P_T(x,y,G) ≠ 0 by separability, and it has some finite x-order r.
Let Δ(y) = [x^r] P_T(x,y,G) ≢ 0, and m = r+1. Write G = G_{<m} + x^m H. Taylor expansion shows that
Q(x,y,T) := P(x,y,G_{<m} + x^m T)/x^{m+r} is a power series in x, polynomial in T, with coefficients in ℚ[y][g_0,…,g_{m−1}].
At x = 0 it is linear in T with leading coefficient Δ, since 2m > m+r. Comparing x^k coefficients gives
h_k = −R_k(y, g_<m, h_<k)/Δ. Hence every g_i ∈ ℚ[y][g_0,…,g_{m−1}, 1/Δ]. Each g_i with i < m is algebraic over ℚ(y), and so is Δ.
Take S = critical points of these finitely many algebraic functions, together with all zeros of all branches of Δ. ∎

Now take a prime p > max(|S|, m). The series g_p(y) = Σ_j e_{pj} y^j has e_{pj} = 0 for p ∤ j, so g_p(y) = φ(y^p).
It also has 1 ≤ e_{p,pk} ≤ C(p+pk, p), so its radius of convergence is exactly 1. Its coefficients are ≥ 0, so by Pringsheim
y = 1 is a singularity. By the symmetry g_p(ωy) = g_p(y), every p-th root of unity ω is a singularity. These are p > |S| distinct
singular points on the unit circle, contradicting the lemma. (If ζ ∉ S, continue the identity g_p = poly(gens)/Δ^N along a path
in the open disk that avoids S and ends at ζ. The right side is analytic near ζ.) ∎

Remarks.
- U is a cross-slice argument. Each slice #a = p is regular for Cop (L3(i)), and U uses uniformity in p of the singular set.
  So it is **not** blind in the sense of O1.
- U does not count toward the target (§7: unambiguity). It is a strict strengthening of Petersen (Cop ⊊ Q).

**Gap for polynomial ambiguity (exact).** For polynomially ambiguous H, the series A = Σ amb_H(w) x^.. y^.. is ℕ-algebraic, and the
coefficient lemma still applies. But [x^p y^j]A ∈ [C(p+j,p), C n^k C(p+j,p)] at coprime j: there is no exact vanishing. The
1-word deficit at p | j that U uses is swamped, and A = 1/(1−x−y) satisfies all constraints. This is the count sandwich (§6).
Routing through Wich's projection (unambiguous U′ over Σ∪Γ) needs the number of **distinct** projected words, which is the
blocked marker route (§6, M1/M2). So ¬P_cop needs a mechanism beyond U, one that sees exact multiplicity 0 vs ≥ 1 through
polynomially many trees. Open question (FA): does U extend to finitely ambiguous L? It does not follow from the Lean-checked
FA result for Q, which is not a sandwich statement.
