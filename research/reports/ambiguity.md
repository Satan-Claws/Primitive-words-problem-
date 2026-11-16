# Agent "ambiguity": finite ambiguity of the primitive words Q

**Status: the TARGET (Q not finitely ambiguous) is NOT proved.** What is proved:

* **Theorem A (PROVED).** This is a structure theorem for finitely ambiguous grammars of languages
  inside (ab\*)^n. The block-resolved multiplicity series is rational, and every irreducible factor
  of its reduced denominator involves at most two block variables. A refinement, A′, says the
  variable pairs inside each term are non-crossing.
* **Theorem B (PROVED; COMPUTER-CHECKED).** If n has an odd prime factor, then
  L_n := Q ∩ (ab\*)^n is inherently ambiguous. Consequence: a new, elementary proof of Petersen's
  theorem that Q is inherently ambiguous. It uses no Chomsky–Schützenberger and no analysis of
  infinitely many poles.
* **Theorem C (PROVED; COMPUTER-CHECKED).** For p an odd prime, L_p is 2-ambiguous. So by B its
  inherent ambiguity degree is exactly 2.
* **Barrier D.** The slices with a prime number of a's can never show more than "not
  unambiguous". This holds even with all the multivariate generating-function information
  (Theorem C is sharp). Any slice proof of non-finite ambiguity needs composite n, and it must
  use that the bound k is uniform in n. Parts of D rest on LITERATURE (Ginsburg) and are labelled.

Standing conventions. Σ = {a,b}. Q = primitive words. For a CFG G and a word w, d_G(w) is the
number of parse trees. G is *k-ambiguous* if d_G(w) ≤ k for all w. *Finitely ambiguous* means
k-ambiguous for some k.

---------------------------------------------------------------------------------------------

## 1. Reductions (all PROVED)

**Lemma 1.1 (CNF does not raise ambiguity).** Let G be a CFG with d_G(w) < ∞ for all w. Then
there is a CNF grammar G'' with L(G'') = L(G) \ {ε} and d_{G''}(w) ≤ d_G(w) for every w ≠ ε.

*Proof.* The steps are the standard ones. For each step we give an injection from new trees to
old trees that preserves the yield.

(i) *Remove useless symbols.* The trees of terminal words are unchanged.

(ii) *Remove ε-rules.* Let N be the set of nullable symbols. G' has the rules A → α' for every
A → α in G and every deletion of some occurrences of nullable symbols from α with α' ≠ ε. A rule
that arises in several ways is kept once. Fix, for each rule A → α' of G', one source (α,
deletion). Fix, for each nullable B, one tree of B with yield ε. Map a G'-tree T' to a G-tree
Φ(T') by re-inserting the fixed ε-trees at each node. In Φ(T'), the subtrees with empty yield are
exactly the inserted ones, because G'-trees of non-empty words have no ε-yield node. Deleting them
recovers T', so Φ is injective.

(iii) *Remove unit rules.* If a unit cycle A ⇒⁺ A through unit rules existed among useful
symbols, some word would have infinitely many trees. So the unit graph is acyclic. G'' has
A → β whenever A ⇒\* B by unit rules and B → β is a non-unit rule, with one canonical unit chain
fixed per pair. Expanding the canonical chains gives Φ; contracting maximal unit chains inverts
it. So Φ is injective.

(iv) *Binarize long rules and introduce terminal nonterminals.* This gives a bijection on trees. ∎

So "Q is k-ambiguous" (any CFG) implies "Q has a k-ambiguous CNF grammar". Below, every grammar is
CNF.

**Lemma 1.2 (intersection with a DFA preserves tree counts).** Let G be a CNF grammar and D a
complete DFA with states S. The product grammar G_D has nonterminals (s,A,t) and the rules:
* (s,A,t) → (s,B,r)(r,C,t) for A → BC;
* (s,A,t) → c for A → c with δ(s,c) = t;
* start symbols (s₀,S,f) with f final.

Then d_{G_D}(w) = d_G(w) for w ∈ L(D), and d_{G_D}(w) = 0 otherwise.

*Proof.* Every node of a G-tree spans a factor w[i..j]. Its annotation must be
(δ(s₀,w[..i]), A, δ(s₀,w[..j])), so it is determined. This gives a bijection between G-trees of w
and G_D-trees of w when w ∈ L(D). (Several start symbols are joined by a fresh start symbol; for
CNF, replace S → X by copies of X's rules.) ∎

Corollary. If Q has a k-ambiguous grammar, then for every n, L_n = Q ∩ (ab\*)^n has a k-ambiguous
grammar G_n. Here k is the same for all n.

## 2. Theorem A: block-resolved series of finitely ambiguous slices

Fix n. Let D_n be the DFA for (ab\*)^n with states 0..n, where state i means "i a's read", plus a
sink. For a word w = a b^{x_1} a b^{x_2} ⋯ a b^{x_n}, put exp(w) = (x_1,…,x_n) ∈ ℕ^n. This map is
injective on (ab\*)^n. Let y_1,…,y_n be commuting variables. For a grammar G with
L(G) ⊆ (ab\*)^n, define

  F_G(y) = Σ_{w} d_G(w) · y^{exp(w)} ∈ ℕ[[y]].

Let **R** be the set of rational functions P/Q with P, Q ∈ ℚ[y], Q(0) ≠ 0, and Q a product of
polynomials each involving at most two of the variables. R is a ring. In lowest terms (ℚ[y] is a
UFD), every irreducible factor of the denominator of an element of R involves at most two
variables, because it divides one of the ≤2-variable factors.

**Theorem A (PROVED).** If G is finitely ambiguous and L(G) ⊆ (ab\*)^n, then F_G ∈ R. In
particular, F_G is rational.

*Proof.* By Lemma 1.2 we may assume G = G_{D_n}, reduced, so all nonterminals are annotated
(s,A,t) and useful. For a nonterminal X, let F_X(y) = Σ over trees τ rooted at X of the monomial
of yield(τ). A letter b read in state i contributes y_i, and a letter a contributes 1. Then
F_G = Σ_{start X} F_X. Write X → Y when X has a rule with Y on the right, and order the strongly
connected components (SCCs) of this graph.

*Step 1: inside an SCC, rules are linear.* Suppose X → YZ with both Y and Z in the SCC of X. Then
X ⇒\* u X v X z for some terminal u, v, z, from Y ⇒\* u X v' and Z ⇒\* u'' X z' with the
other parts expanded to terminal words. Fix such a derivation tree δ with two X-leaves, and a word
w ∈ L(X) (X is useful).
* If some w ∈ L(X) contains an a, then nesting δ r times gives words in L(X) with ≥ r+1 a's. Since
  X occurs in a derivation from the start symbol, G generates a word with more than n a's,
  contradicting L(G) ⊆ (ab\*)^n.
* So L(X) ⊆ b⁺. Likewise u, v, z ∈ b\*, since an a in them would also be multiplied by nesting δ. For r ≥ 1, take any of the Catalan-many binary
  arrangements of r copies of δ, filling the r+1 remaining X-leaves with a fixed tree of w. Every
  arrangement yields b^{r|uvz| + (r+1)|w|}, so the yield is independent of the arrangement.
  Different arrangements give different trees: at the first node address where they differ, one
  subtree is a copy of δ and the other is a w-tree, and their yields have different lengths
  because |uvz| + 2|w| > |w|. Put this in a fixed context S ⇒\* αXβ ⇒\* α'·_·β'. Then one word has
  at least C_r trees, which is unbounded. This contradicts finite ambiguity.

*Step 2: inside an SCC, the side material is b-only and the annotation is constant.* Let X → YZ
with Y in the SCC C of X and Z ∉ C. Since Y ⇒\* … X …, every word of L(Z) occurs in the right
context of some cycle X ⇒⁺ u X v. If a word of L(Z) contained an a, pumping the cycle would
produce too many a's. So L(Z) ⊆ b⁺. Then Z's annotation is (t,Z,t), where t is the right state of
X, and F_Z is a power series in y_t alone. The case X → ZY is symmetric. Consequently Y has the
same annotation (s,·,t) as X, and all members of C share one pair of states (s,t).

*Step 3: induction over the SCC DAG.* Claim: F_X ∈ R for every X. Take C to be an SCC whose
successors outside C satisfy the claim.
* For Z ∉ C with Z b-only in state t: F_Z ∈ R and F_Z depends only on y_t. Setting the other
  variables to 0 in a representation P/Q gives P'/Q' with Q' = Q(0,…,y_t,…,0). This is a product
  of polynomials in y_t, and it is non-zero since Q(0) ≠ 0. So F_Z ∈ ℚ(y_t) ∩ R.
* The vector F_C satisfies F_C = M F_C + c. Here M_{X,Y} = Σ F_Z over rules X → YZ or X → ZY with
  Y ∈ C, Z ∉ C. So M has entries in R_{s,t} = R ∩ ℚ(y_s, y_t), all with zero constant term: in CNF,
  Z generates non-empty b-words. Each entry c_X is a sum of products F_Y F_Z with Y, Z ∉ C, plus
  terminal monomials, so it lies in R by induction.
* Since M has no constant term, I − M is invertible over ℚ[[y]], and F_C = (I − M)^{-1} c is the
  unique power-series solution. By Cramer's rule, (I − M)^{-1} = adj(I − M)/det(I − M). Clearing
  the one-variable denominators of M's entries shows det(I − M) = N/H, where N and H are
  polynomials in y_s, y_t only and N(0) = H(0) ≠ 0.
* Hence F_C has entries in R. ∎

**Theorem A′ (refinement, PROVED by the same induction).** F_G is a finite sum of fractions
P_τ/Q_τ, where each Q_τ is a product of polynomials f_{(i,j)}(y_i, y_j) (or in a single variable)
and the pairs {i,j} occurring in a single Q_τ are pairwise non-crossing. Non-crossing means no
i < k < j < l with {i,j} and {k,l} both present; shared endpoints are allowed.

*Proof sketch* (each step is the step above, with the pairs tracked). An SCC with state pair (s,t)
contributes factors in (y_s, y_t). Its constant vector c consists of products F_Y F_Z with Y
spanning states [s,r] and Z spanning [r,t]. By induction, their pairs lie in [s,r] and in [r,t]
respectively, and adding the outer pair (s,t) keeps the family laminar. ∎

## 3. Theorem B: slices with an odd prime factor are inherently ambiguous

For s | n, let D_s ⊆ ℕ^n be the set of vectors invariant under the cyclic shift by s, i.e.
x_i = x_{i+s} with indices mod n. A word a b^{x_1}⋯a b^{x_n} is a proper power iff (x_i) is
invariant under some cyclic shift s with s | n, s < n. Let E_n = exp(L_n) = ℕ^n \ ∪_{s|n, s<n} D_s.

**Lemma 3.1 (PROVED).** GF(1_{E_n}) = Σ_{d | n} μ(d) Π_{r=1}^{n/d} 1/(1 − m_{n/d,r}), where
m_{s,r} = Π_{i ≡ r mod s} y_i.

*Proof.* The shifts fixing x form the subgroup generated by the minimal period s₀ | n, and x is
(n/d)-invariant iff d | n/s₀. So Σ_{d | n, x ∈ D_{n/d}} μ(d) = Σ_{d | n/s₀} μ(d) = [s₀ = n]. Also
D_s ≅ ℕ^s, because the coordinate classes mod s are free, and the class of r contributes the
geometric series 1/(1 − m_{s,r}). ∎

**Lemma 3.2 (PROVED).** For any set I of at least 2 indices, 1 − Π_{i∈I} y_i is irreducible over
ℚ.

*Proof.* Suppose 1 − Π y_i = AB with A, B non-constant. The polynomial has degree 1 in each y_i,
so each variable occurs in exactly one of A, B. Let I_A and I_B be these sets; they are disjoint and
both non-empty. Note A(0)B(0) = 1. Pick a non-constant monomial μ of A, with coefficient α ≠ 0.
In AB, the only product of a monomial of A and a monomial of B that equals μ is μ·1, because the
variable sets are disjoint. So μ has coefficient α·B(0) ≠ 0 in AB. But μ ≠ 1, and μ ≠ Π_I y_i since
μ uses only variables from I_A ⊊ I. This is a contradiction. ∎

**Theorem B (PROVED; COMPUTER-CHECKED for n ≤ 9 by `gf_denominators.py`).** If n has an odd prime
factor q, then 1_{E_n} has GF ∉ R. Hence L_n has no unambiguous grammar, i.e. L_n is inherently ambiguous. As a consequence, Q is inherently ambiguous: by
Lemma 1.2, an unambiguous grammar for Q would give one for L_3.

*Proof.* Let s = n/q and f = 1 − m_{s,1}. The factor f involves q ≥ 3 variables and is
irreducible (Lemma 3.2). Among the factors 1 − m_{s',r} in Lemma 3.1, f occurs only for s' = s,
r ≡ 1, because the index class of 1 mod s' equals that mod s only when s' = s (the class sizes are
n/s' and n/s). So GF(1_{E_n}) = μ(q)/(f·g) + V, where:
* g = Π_{r=2}^{s}(1 − m_{s,r}), which is coprime to f;
* μ(q) = −1;
* V is a sum of fractions whose denominators are coprime to f.

Suppose an unambiguous grammar existed. Then d_G = 1_{L_n}, and Theorem A gives GF(1_{E_n}) = C/E
in R with f ∤ E (E's irreducible factors have at most 2 variables). Then 1/(fg) = −(C/E − V) has a
representation with denominator coprime to f. Writing 1/(fg) = P/H with f ∤ H gives H = P f g,
so f | H, a contradiction. ∎

Remarks.
* The script computes the reduced GF of 1_{E_n} with sympy and factors its denominator. The
  largest number of variables in an irreducible factor is 2 for n = 2, 4, 8, and ≥ 3 for
  n = 3, 5, 6, 7, 9. This matches the theorem, including its failure for n = 2^a, where every
  D_s factor has the form 1 − y_i y_{i+n/2}, …
* Petersen (1994/96) and Koechlin (2022) prove Q inherently ambiguous analytically through the
  univariate series. The present proof is finite and algebraic: Q ∩ (ab\*)^3 =
  {ab^x ab^y ab^z : ¬(x=y=z)} is already inherently ambiguous, and the witness is the irreducible
  factor 1 − y_1 y_2 y_3.
* Novelty: not found in the literature checked. Ginsburg–Ullian (JACM 13, 1966) characterise
  inherent ambiguity of bounded CFLs through semilinear sets and could perhaps give B. I could not
  access the paper (network blocked), so this is LITERATURE-UNCHECKED.

## 4. Theorem C: prime slices are exactly 2-ambiguous

**Theorem C (PROVED; COMPUTER-CHECKED by `two_ambiguous_prime.py`).** Let p be an odd prime. Then
L_p = A_1 ∪ A_2, where each A_i is an unambiguous CFL:
* A_1 = { x : ∃ j, x_{2j−1} ≠ x_{2j} } (pairs (1,2),(3,4),…,(p−2,p−1));
* A_2 = { x : ∃ j, x_{2j} ≠ x_{2j+1} } (pairs (2,3),…,(p−1,p)).

So L_p is 2-ambiguous, and with Theorem B its inherent ambiguity degree is exactly 2.

*Proof.*
* *Union.* For prime p, E_p is the set of non-constant vectors. If x ∉ A_1 ∪ A_2, then
  x_1 = x_2 = x_3 = ⋯ = x_p by alternately using the two pair systems, so x is constant. The
  converse is clear.
* *A_1 is unambiguous.* A_1 is the disjoint union over t of
  A_1^{(t)} = { x_{2j−1} = x_{2j} for j < t, x_{2t−1} ≠ x_{2t}, rest free }, where t is the first
  unequal pair. Each A_1^{(t)} is a concatenation of blocks, and every block begins with a and has a
  fixed number of a's, so the factorisation into blocks is unique. The blocks are:
  * Eq = a·P with P → bPb | a, giving a b^m a b^m;
  * Ne = a·U with U → bUb | B⁺a | aB⁺, giving a b^m a b^{m'} with m ≠ m';
  * F = a b\*.
  
  Each block grammar is unambiguous: P and U peel matched b's outside-in, and B⁺ → bB⁺ | b. So
  A_1^{(t)} is unambiguous, and so is the disjoint union.
* *A_2* is handled the same way. S → A_1 | A_2 gives at most 2 trees.

The script builds this grammar and counts trees by dynamic programming over all splits. It checks
every word of (ab\*)^p with blocks ≤ B (p = 3, B = 9; p = 5, B = 4; p = 7, B = 2): there are 0 trees
iff the word is non-primitive and 1 or 2 trees otherwise. It also checks that no word of length
≤ 12/11/10 outside (ab\*)^p is generated. Result: histograms {0:10, 1:180, 2:810},
{0:5, 1:240, 2:2880}, {0:3, 1:156, 2:2028}, with 0 failures. ∎

## 5. Barriers and analysis for the target

**D1 (PROVED, Theorem C).** For prime slices, the lower bound "≥ 2" from Theorem A/B is the truth.
No argument restricted to Q ∩ (ab\*)^p with p prime can show that Q is not 2-ambiguous.

**D2 (LITERATURE: Ginsburg–Spanier (stratified semilinear sets) plus the standard decomposition of
linear sets into simple ones; NOT re-proved here).** Every bounded CFL is a finite union of
unambiguous CFLs, hence finitely ambiguous. So for a fixed slice, "L_n not finitely ambiguous" is
equivalent to "L_n not CF", which is the Kászonyi–Katsura problem. A slice-based proof of the
target must therefore show that **the inherent ambiguity degree of L_n is unbounded in n**. That
is sufficient, by the Corollary of Lemma 1.2; it is also all that slices can give. By D1, the n
must be composite. Candidates are n = 2^a (open even for "≥ 2", see D3) and n with many distinct
prime factors.

**D3 (OPEN, with a concrete sub-question).** For n = 2^a, Theorem A gives nothing, because
GF(1_{E_n}) ∈ R. Theorem A′ might give more. The D_{n/2} term Π_r 1/(1 − y_r y_{r+n/2}) has
pairwise CROSSING pairs (r, r+n/2). *Sub-question:* is Π_{r=1}^{n/2} 1/(1 − y_r y_{r+n/2}) (n ≥ 4)
congruent, modulo sums of non-crossing fractions, to something that bounded multiplicities could
absorb? A negative answer would give "L_4 inherently ambiguous". A quantitative version (crossing
depth versus multiplicity) is a possible route to unbounded degree. CONJECTURED only.

**D4 (PROVED in rectangles.md Prop 5.1; restated).** Univariate and letter-count series cannot
exclude ambiguity 2. This section adds that even the full block-resolved series cannot do so on
prime slices (D1), because the 2-ambiguous m = 1_{A_1} + 1_{A_2} has GF in R and is non-crossing.
Bounded integer weights in [1,k] are flexible enough to cancel every many-variable pole that a
prime slice has. Only crossing (Theorem A′) and uniformity in n remain as levers.

**D5 (analysis of other suggested routes).**
* *Inclusion–exclusion for Q = L_1 ∪ … ∪ L_k.* This needs the series of L_i ∩ L_j, which are
  Hadamard products of algebraic series and not algebraic in general. The only consequence is the
  one already recorded in rectangles.md: if all intersections have ℤ-algebraic series, a
  contradiction follows. Theorem A gives a sharper slice version. If Q = ∪ L_i with each L_i an
  unambiguous CFL, and all the intersections L_I ∩ (ab\*)^n are finitely ambiguous CFLs, then
  inclusion–exclusion puts GF(1_{E_n}) in the ℤ-span of R = R. That is impossible for n with an
  odd prime factor. This holds for k = 1 always; for k ≥ 2 the hypothesis on the intersections is
  not automatic.
* *Fixed number of b's.* Q ∩ (b\*a)^\* with a fixed number of b's is the same slice structure with
  the letters swapped.

## 6. Exact statements proved (summary)

1. (Thm A, PROVED) If G is finitely ambiguous and L(G) ⊆ (ab\*)^n, then Σ d_G(w) y^{exp(w)} is a
   rational function whose reduced denominator has only irreducible factors in ≤ 2 variables. By
   A′, the pairs within each term are non-crossing.
2. (Thm B, PROVED + COMPUTER-CHECKED n ≤ 9) If n has an odd prime factor, Q ∩ (ab\*)^n is
   inherently ambiguous. This gives a new algebraic proof that Q is inherently ambiguous.
3. (Thm C, PROVED + COMPUTER-CHECKED) For odd prime p, Q ∩ (ab\*)^p has inherent ambiguity degree
   exactly 2.
4. (Lemma 1.1, PROVED) Every finitely ambiguous CFG has a CNF equivalent of no larger ambiguity.
   Together with Lemma 1.2: if Q is k-ambiguous, then all slices are k-ambiguous with the same k.

The target theorem (Q not finitely ambiguous), "not 2-ambiguous" and "not polynomially
ambiguous" remain OPEN.

Scripts: `scratchpad/scripts/ambiguity/gf_denominators.py`, `two_ambiguous_prime.py`.
