# Round 1 — Route D: Analytic / ambiguity (negative direction)

Author: researcher D. Status: **no proof of non-context-freeness. The route is blocked, and the blocks below are proved with explicit certificates.** What this report contributes: (i) explicit CF languages that show Petersen's analytic invariants cannot reach finite ambiguity, let alone general CF; (ii) a dichotomy for regular slices that rules out "bounded-like slices with Möbius counting"; (iii) an exact reformulation of what any purely counting-based non-CF proof would have to show.

Code and outputs are in `/tmp/claude-5714/-home-shobhit--claude-spares-spare-fauO4P/6f48459d-5790-4a18-bccc-eabb8efc4544/scratchpad/analytic/` (`slices.py`, `slices.out`, `two_ambiguous.py`, `two_ambiguous.out`). Every closed-form generating function stated below was checked against brute-force enumeration (asserts pass).

---

## 0. Baseline: what Petersen's argument uses

q(n) = Σ_{d|n} μ(n/d) 2^d, and

  Q(z) = Σ_{n≥1} q(n) zⁿ = Σ_{k≥1} μ(k) · 2z^k/(1−2z^k)   (checked numerically, n ≤ 14).

The term for k has simple poles exactly at the k roots of z^k = 1/2, all of modulus 2^{−1/k}. Different k give different moduli, so poles never cancel. Every squarefree k therefore contributes poles. Q(z) is meromorphic in |z|<1 with infinitely many poles. Since the p-th roots of unity (p prime) become dense in the circle, the poles accumulate at every point of |z|=1, so |z|=1 is a natural boundary. Consequences: Q(z) is not algebraic (an algebraic function has finitely many singularities) and not D-finite (a D-finite function has finitely many singularities). By Chomsky–Schützenberger (an unambiguous CFL has an algebraic GF), Q is not unambiguous CF. That is Petersen's theorem.

**The structural fact behind everything below.** For any CFG G, the derivation series D_G = Σ_w amb_G(w)·w is ℕ-algebraic. Its length-commutative image d_n = Σ_{|w|=n} amb_G(w) is an algebraic function's coefficients. The language L(G) is only the **support** of D_G, and c_n = |L(G) ∩ Σⁿ| counts support points. Analytic theorems (algebraicity, Puiseux and singularity structure, Banderier–Drmota exponents) apply to d_n. They transfer to c_n exactly when amb ≡ 1 on L, i.e. when G is unambiguous.

---

## 1. Finitely ambiguous grammars

### 1.1 What is true (proved here or standard)

* A union of k unambiguous CFLs is k-ambiguous (take the union of the k grammars under a new start symbol). I do **not** use the converse. I cannot reconstruct a proof that a k-ambiguous CFL is a finite union of unambiguous CFLs, and I am not aware of such a theorem. It does not matter here: the obstructions below already occur for unions of **two DCFLs**, the most benign finitely ambiguous case.
* Inclusion–exclusion identity. Let G be k-ambiguous for L. For w ∈ Σ*, 1_L(w) = 1 − (1−1)^{amb(w)} = Σ_{j=1}^{k} (−1)^{j+1} C(amb(w), j). Hence

  c_n = Σ_{j=1}^{k} (−1)^{j+1} N_j(n),  N_j(n) = #{(w, S) : |w|=n, S a j-set of distinct G-derivations of w}.

  Only N_1 = d_n is known to be algebraic. N_2 counts unordered pairs of distinct derivation trees with the same yield. This is a "same-yield" (Hadamard / intersection-type) object, and such objects have no algebraicity theorem: intersections of two DCFLs already encode Turing-machine computations. **This is the exact obstruction:** Petersen's argument goes through for a k-ambiguous grammar iff Σ_n N_j(n) zⁿ is algebraic for j = 2..k. Nothing forces that.
* Sandwich. From inclusion–exclusion, the only unconditional information is c_n ≤ d_n ≤ k·c_n with d algebraic.

### 1.2 Proposition 1 (sandwich is vacuous for Q, already at k = 2)

The ℕ-rational series d_n = 2ⁿ (n ≥ 1) satisfies q(n) ≤ d_n ≤ 2 q(n) for all n ≥ 1.

*Proof.* q(n) ≤ 2ⁿ is trivial. For the other inequality: q(1)=2, q(2)=2, q(3)=6 ≥ 4. For n ≥ 4, 2ⁿ − q(n) = #non-primitive ≤ Σ_{d ≤ n/2} 2^d < 2^{n/2+1} ≤ 2^{n−1}. ∎

So no argument that uses only "d algebraic and c ≤ d ≤ kc" can refute even 2-ambiguity of Q. The Möbius signal 2^{n/p} sits at relative size 2^{−n/2}, far below the resolution of a bounded multiplicative distortion.

### 1.3 Theorem 2 (Petersen's singularity pattern is compatible with inherent ambiguity 2) — new certificate

Over Δ = {a,b,#}, split a word into its #-separated segments u_1#u_2#…#u_m.

* L1 = {u_1#…#u_m : u_{2i} = u_{2i−1}^R for all 2i ≤ m} = (P#)*(P ∪ {a,b}*), with P = {u#u^R : u ∈ {a,b}*}.
* L2 = {u_1#…#u_m : u_{2i+1} = u_{2i}^R for all 2i+1 ≤ m} = {a,b}*(#P)*(ε ∪ #{a,b}*).

Both are DCFLs with unambiguous grammars: the #-factorization is unique and each P-check is deterministic. Their intersection is

  L1 ∩ L2 = {u # u^R # u # u^R # … (m segments) : u ∈ {a,b}*, m ≥ 1}.

Generating functions (verified by brute force for n ≤ 12):

* GF(L1) = (1+z−4z²)/((1−2z)(1−3z²)), rational.
* GF(L2) = (1−z)(1−2z²)/((1−2z)²(1−3z²)), rational.
* GF(L1∩L2) = Σ_{m≥1} z^{m−1}/(1−2z^m).
* GF(L1 ∪ L2) = GF(L1) + GF(L2) − Σ_{m≥1} z^{m−1}/(1−2z^m).

The last series has simple poles at all z with z^m = 1/2, for every m ≥ 1. These are the same moduli 2^{−1/m} as Q (Q uses only squarefree m). They accumulate on all of |z| = 1, giving a natural boundary. So L = L1 ∪ L2 is a CFL with a 2-ambiguous grammar whose GF is non-algebraic and non-D-finite, with infinitely many poles in the open disk. By Chomsky–Schützenberger, L is inherently ambiguous; its inherent degree of ambiguity is exactly 2.

**Binary version.** Apply the code h(a)=ab, h(b)=abb, h(#)=abbb. Each codeword is a·b^i, so decoding is unique and h maps derivations bijectively. Then h(L1), h(L2) ⊆ {a,b}* are unambiguous CF and h(L) is 2-ambiguous CF. GF(h(L1∩L2)) = Σ_m z^{4(m−1)}/(1 − z^{2m} − z^{3m}), with poles of modulus x₀^{1/m}, where x₀ ≈ 0.754878 is the real root of x²+x³=1. Again there are infinitely many poles, accumulating on |z|=1.

**Consequence.** Every global analytic feature of Q(z) that Petersen-type arguments use also occurs for an explicit binary CFL of inherent ambiguity 2:
* non-algebraic,
* non-D-finite,
* meromorphic in the disk with infinitely many poles at radii a^{−1/m},
* natural boundary at |z| = 1.

Hence no criterion built from these features can show that Q is not finitely ambiguous. A proof of "Q not finitely ambiguous" must use structure (which words carry multiple derivations), not counting.

**Remark (signs).** Inclusion–exclusion over three or more languages produces positive-sign intersection terms. So even signed divisor-type patterns like μ(k) are not excluded in principle for finite unions of DCFLs. I did not construct one with exactly Q's signs; that is not needed for the negative conclusion.

### 1.4 Where a finite-ambiguity proof would have to come from

The missing lemma is a **structural** constraint on finitely ambiguous grammars that controls N_2: for example an Ogden-type lemma in which the pumped pair cannot create a new derivation, or Wich-style ambiguity-growth dichotomies applied to the set of words with amb ≥ 2. None is known to me that is strong enough. Such a lemma would be of theorem strength. And per PROBLEM.md, "Q not finitely ambiguous" would anyway be a restricted-class result that does not count.

---

## 2. Regular slices and bounded languages

### 2.1 Exact theorems, with hypotheses

* **Ginsburg–Spanier (bounded CFLs).** For L ⊆ w₁*…w_k*: L is CF iff L is the image of a finite union of stratified linear subsets of ℕ^k under e ↦ w₁^{e₁}…w_k^{e_k}. In particular a bounded CFL has a semilinear exponent set.
* **"Every bounded CFL is unambiguous" is FALSE.** {a^i b^j c^k : i=j or j=k} ⊆ a*b*c* is bounded and inherently ambiguous (classical; Ginsburg–Ullian 1966 characterize the unambiguous bounded CFLs via disjoint stratified decompositions). My belief that every bounded CFL is a finite union of unambiguous ones is not reconstructed here and is not used.
* **Counting.** A bounded CFL has a rational length-GF. Source: D'Alessandro–Intrigila–Varricchio, counting functions of sparse CFLs (recalled, not re-proved). Independently, a semilinear exponent set counted with a linear weight has a rational GF (Eilenberg–Schützenberger / Ito: every semilinear set is a finite disjoint union of linear sets with independent periods).
* **No theorem says "L CF ⇒ L ∩ R unambiguous" for any useful structured R.** The example above shows bounded R are not enough either.

### 2.2 Proposition 3 (code-slices: finite vs infinite Möbius sums)

Let C ⊆ Σ⁺ be a regular code such that C* is pure: u^m ∈ C⁺ ⇒ u ∈ C⁺. Let c(z) = GF(C) and S = c/(1−c). Each word of C⁺ is uniquely a power of a primitive C-sequence, and primitivity as a word coincides with primitivity as a C-sequence. Therefore

* GF(Q ∩ C⁺) = Σ_{k≥1} μ(k) S(z^k)  (infinite Möbius sum);
* GF(Q ∩ C^K) = Σ_{e | K} μ(e) c(z^e)^{K/e}  (finite Möbius sum: rational).

Verified cases:
* C = a⁺b: c = z²/(1−z), S = z²/(1−z−z²). The infinite sum matches brute force for n ≤ 18; poles at radii φ^{−1/k}. So Q ∩ (a⁺b)* is not unambiguous CF, which is Petersen again and nothing more.
* C = a*b with K = 2, 3, 4, 6, 12: Σ_{e|K} μ(e)(z^e/(1−z^e))^{K/e} matches brute force for n ≤ 30 (K=12: n ≤ 22).

### 2.3 Proposition 4 (no "bounded-like slice with dominant Möbius term")

Let R be regular with a trim DFA and growth rate ρ.

1. If ρ = 1 (polynomial growth), R is bounded (Szilard–Yu–Zhang–Shallit). Then Q ∩ R has a rational GF. Proof sketch: membership of φ(e) = w₁^{e₁}…w_k^{e_k} in the set of powers, and the equality φ(e) = φ(e'), are Presburger-definable. Compare two concatenations of periodic blocks whose lengths are linear in e: on each overlap segment, long overlaps reduce to a congruence condition by Fine–Wilf, and short overlaps give finitely many cases. So the set of canonical exponent vectors of primitive words is semilinear and the count is rational. The Fine–Wilf step is a sketch, not written line by line.
   Verified numerically: linear recurrences fit for Q∩a*b*a*b* (order 6), Q∩ab*a*ab* (order 5), Q∩a*ba*b*a* (order 5). Q∩a*b*a*b*a*b* had too few terms (28) to certify.
2. If ρ > 1: a non-primitive u^k ∈ R of length n has u in the factor language F(R). F(R) is regular with the same growth rate ρ (trim automaton). So #(non-primitive ∩ R ∩ Σⁿ) ≤ C·n^{r+1}·ρ^{n/2}, while |R ∩ Σⁿ| is of order n^s ρⁿ along its support progressions. The Möbius correction is exponentially subdominant.

So every regular slice is either rational (no information) or "Petersen-shaped": a non-algebraic correction of relative size ρ^{−n/2}, which detects only non-unambiguity (Theorem 2 / Proposition 1 logic). The hoped-for intermediate case, a slice that is bounded-like yet carries Möbius counting, does not exist among regular slices.

---

## 3. Flajolet's criteria, and whether analytics can ever prove non-CF

### 3.1 What Flajolet (1987, "Analytic models and ambiguity of CF languages") proves

All criteria have the form "f_L is transcendental ⇒ L is not unambiguous CF":
* **(a) Singularity criterion:** infinitely many singularities, or a natural boundary.
* **(b) Asymptotic criterion:** coefficients not of the Newton–Puiseux form C·ρ^{−n}·n^α with α ∈ ℚ∖{−1,−2,…} on residue classes. Examples: log factors, irrational exponents, transcendental ρ.
* **(c) Arithmetic criteria:** Eisenstein-type denominator bounds, and gap theorems.

Applied to languages already known to be CF (Goldstine, Crestin's double palindromes, Shamir), they give **inherent ambiguity**. Applied to a language not known to be CF, they give only "not unambiguous CF", as in Petersen. They never prove non-context-freeness, because their only input is Chomsky–Schützenberger, which is a statement about multiplicity series.

### 3.2 Analytic facts valid for ALL CFLs (the only possible openings)

* Growth gap: every CFL has polynomial or exponential growth (Incitti; Bridson–Gilman).
* A polynomial-growth CFL is bounded and has a rational GF.

An analytic non-CF proof must therefore find a CF-preserving image of Q with intermediate growth, or with polynomial growth but non-rational counting. Q ∩ (bounded R) is always rational (Proposition 4.1). A rational transduction τ with τ(Q) bounded: τ(Q) = τ(Σ*) ∖ {y : τ^{−1}(y) ⊆ non-primitive}. A regular set inside the non-primitive words has growth rate 1, so it is bounded. So everything is decided by bounded slices of Q — the bounded-language dead end in PROBLEM.md. This reduction is heuristic; I did not prove that it loses nothing.

Growth rate: Q's is 2, algebraic, so it carries no information.

### 3.3 Precise reformulation of any purely count-based non-CF proof

Over {a,b}: (q(n)) is the counting sequence of a CFL iff some co-CF set T ⊆ {a,b}* has |T ∩ Σⁿ| = D(n) := 2ⁿ − q(n) = −Σ_{k|n, k≥2} μ(k) 2^{n/k}. (Complement both ways; complements of CFLs are exactly co-CF.)

Co-CF sets are closed under finite intersection, not union. The natural T = ∪_p {u^p} is a union. Every canonical-representative variant I tried needs a ∀∃ condition and so is not co-CF:
* smallest prime p,
* largest prime p,
* primitive root.

The marker set T = {u#u^R#u…} is co-CF and has divisor-sum counts with one sign (Theorem 2's complement), but needs markers (one visible period). I could not settle whether (q(n)) is a CF counting sequence. Deciding it appears to be of the same difficulty as the original question.

**Conclusion.** No known analytic invariant separates Q from CFLs:
* the features of Q(z) are realized by explicit (even 2-ambiguous, binary) CFLs;
* the only all-CFL analytic constraints reduce to bounded slices, where Q's counting is rational.

An analytic non-CF proof is not provably impossible, but it would need a new theorem about supports of ℕ-algebraic series. The obstruction is the uncontrolled same-yield count N_2 (and the co-CF union problem in §3.3), and a theorem controlling it is of theorem strength, comparable to the original problem.
