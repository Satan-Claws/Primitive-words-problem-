# Adversarial audit of PROOF.md: §1, §4, §5 (geometry part)

Scope: §1 (slice), §4 (Lemmas 4.1, 4.2), §5 (geometric argument), and how the result is carried over to Q.
Lemma 3 (Structure) and the §2 reductions are taken as given; another auditor checks them.

**Verdict: CORRECT WITH (MINOR) FIXES.** I found no gap that breaks the argument. Every step I checked
either holds as written or needs only a one-line clarification (F1–F7 below). The computational checks
found no counterexample, and they confirm that the two hypotheses that do the real work are needed:
laminarity, and the N! scaling.

---

## §1 Lemma 1 (slice identity): holds

* Write w = u^k with k ≥ 2. Since w starts with a, so does u. So every copy of u starts at a block
  boundary, each copy has n/k blocks, and exp(w) is invariant under the cyclic shift by s = n/k ∈ (0,n).
  The zero coordinates are exactly {1, m+1}, because x_i, y_i ≥ 1. So 1+s ≡ m+1 and s = m, which is
  x = y. The converse direction is immediate.
* Degenerate m: the lemma needs m ≥ 2 (M ≥ 1), and §5 only uses m = 2k+1 ≥ 3. For m = 1, R_1 = {aa},
  and the statement is vacuous but still true.
* Re-ran `check_slice.py`: 1257 words, 0 failures.
* Side claim "the diagonal pairs cross pairwise": i < j ≤ M < M+i < M+j. True.

## §4 Lemma 4.1 (non-interleaving): holds

* The path p → r in C₁ must jump over q ∉ C₁, so some edge {a,b} of C₁ has a < q < b. An edge of C₂ that
  leaves (a,b) must end strictly outside [a,b], because a, b ∈ C₁. So it would cross {a,b}, which means
  C₂ ⊆ (a,b). By symmetry, C₁ ⊆ (c,d) for an edge {c,d} of C₂ around r. Then a < c, so a ∉ (c,d).
  Contradiction.
* Loops and multi-edges are irrelevant to the argument.
* Exhaustive check over every non-crossing graph on N ≤ 8 points (231,168 graphs for N = 8): 0
  violations (`audit_geom/lemma41_exhaustive.py`).

## §4 Lemma 4.2 (Lemma X): holds

Checked each step and each case:

* **Direct sum.** span V = ⊕_C span V_C. Correct, since the supports split along the components.
* **Spanning tree bound.** dim span V_C ≥ |C| − 1, by the leaf argument; any positive weights work.
  Multi-edges: pick one vector per tree edge.
* **Non-full components.** A non-full component is λ^⊥ ∩ ℝ^C.
  * A loop forces λ_p = 0.
  * An edge with positive weights propagates "λ_p = 0", so λ vanishes nowhere on C.
  * Hence non-full components have no loops, and e_p ∉ span V for p ∈ C. A projection onto ℝ^C
    preserves span V, because span V is a direct sum of coordinate blocks.
* **Single-point supports.** A vector whose support is one point of a pair is just a loop. Handled.
* **Isolated vertices.** An isolated unlooped vertex gives a non-full singleton, which cannot contain
  its partner, so it is impossible. Handled.
* **At most one non-full component.** Two non-full components each contain a pair {i, M+i} and
  {j, M+j}, i < j. They interleave (i < j < M+i < M+j), which Lemma 4.1 forbids. So at most one
  component is non-full, and dim ≥ 2M − 1.
* **Gap (F1).** The "Moreover" sentence says *at most one component contains a pair*. The proof only
  shows this for **non-full** components. The same Lemma 4.1 argument applies to any components, so the
  claim is true, but the proof should say so. Nothing later depends on it. §5 case 2 cites it, but does
  not need it (see F3).
* **Computation** (`audit_geom/lemmaX_exhaustive.py`): exhaustive over all support patterns for M = 2
  (48 non-crossing edge sets × 16 loop sets) and M = 3 (2880 × 64), with unit, random and multi-edge
  weights. 1552 and 245,091 families have W ⊆ span V. Results:
  * dim ≥ 2M − 1: 0 violations.
  * "at most one component contains a pair": 0 violations.
  * The §5 corollary (#{v : n_v ≡ 0 on W} ≤ dim − (2M − 1), i.e. |V_{σ,0}| ≥ 2M − 1): 0 violations.
* **Laminarity is necessary.** The crossing family {e₁+e₃, e₂+e₄, e₄}, which is the period set of the
  piece "x₁ = y₁, x₂ < y₂", has dim 3 and W ⊆ span. But one of its coordinate functionals vanishes on
  W, so the corollary fails for it.

## §5: holds

**Setup.**
* L_σ ⊆ NE_M because f ≥ 1_{L_σ} and f = 0 off exp(Q ∩ R_m).
* A period cannot touch the two constant-0 blocks, otherwise c + v would leave R_m.
* Supports are subsets of the laminar pairs, so they are non-crossing in the induced order, also after
  the two 0-blocks are deleted.

**Genericity of ω.** Each ∂C_σ of a full-dimensional polyhedral cone, and each lower-dimensional C_σ,
lies in finitely many proper subspaces, so a suitable ω ∈ ℤ_{≥1}^M exists. ω depends only on G_m. This
is fine.

**Lattice fact.**
* Write Λ = span V_σ ∩ ℤ^{2M}. Then P − P₁ ∈ N!ℤ^{2M} ∩ span V_σ = N!Λ: if N!z lies in a subspace, so
  does z.
* ℤV_σ is a full-rank sublattice of Λ, because V_σ is a rational basis of span V_σ (Lemma 3 gives
  independence). So Λ/ℤV_σ is finite of order I_σ, and I_σΛ ⊆ ℤV_σ.
* I_σ | N! gives N!Λ ⊆ I_σΛ.
* P₁ − c ∈ ℕV_σ.

Correct.

**Positivity fact.**
* ω ∈ int C_σ means (u,u) ∈ cone(V_σ) for u in an open set, so W ⊆ span V_σ.
* n_v is defined on span V_σ, and n_v ≥ 0 on the cone. So u ↦ n_v(u,u) is a linear form that is ≥ 0
  near ω. If it is 0 at ω, it vanishes identically.
* span V_{σ,0} ⊇ W, because w = Σ_{v∈V_{σ,0}} n_v(w)v.
* V_{σ,0} is laminar, non-negative and independent, so Lemma X gives |V_{σ,0}| ≥ 2M − 1, and hence
  |V_{σ,1}| ≤ dim − (2M − 1) ≤ 1.

**The implication |V_{σ,0}| ≥ 2M − 1 is valid.**

**Cases are exhaustive.** Genericity gives ω ∉ C_σ or ω ∈ int C_σ. In the second case Lemma X gives
dim ∈ {2M − 1, 2M}. If dim = 2M − 1, then V_{σ,1} = ∅. If dim = 2M, V_σ is a basis and
|V_{σ,1}| ∈ {0, 1}.

**Case 1.**
* If P(t,δ) ∈ L_σ for unboundedly many t with δ fixed (pigeonhole over the finite δ-set), then
  (P − c)/t → (ω,ω) inside the closed cone. Contradiction.
* t₀(R) depends on R. This is allowed.

**Case 2.**
* λ_i = −λ_{M+i} is justified, but directly: W ⊆ span V_σ = λ^⊥. Lemma 4.2's non-full component is not
  needed (F3).
* ⟨λ, P(t₁,δ₁)⟩ = N!⟨λ_y, δ₁⟩ ∈ N!ℤ, and N! > |⟨λ,c⟩|, so ⟨λ,c⟩ = 0.
* So c_σ ∈ span V_σ. This is what makes n_v(c_σ) well defined (F2).
* P₀ = (tω,tω) with t ∈ N!ℤ lies in c + span V_σ. The lattice fact gives integer coordinates, and they
  are ≥ 0 for large t because every n_v(ω,ω) > 0. So P₀ ∈ L_σ ∩ Δ. Contradiction.
* The conclusion holds for all t, δ, which is exactly what §5 needs.

**Case 3.** Same as case 2, with no λ needed. Correct.

**Case 4.**
* ψ_σ ≠ 0, because n_{v*} ≠ 0 vanishes on W and ℝ^{2M} = W ⊕ (0 × ℝ^M).
* ψ_σ(ℤ^M) ⊆ (1/D_σ)ℤ, by the adjugate formula.
* n_{v*}(P(t,δ)) = N!ψ_σ(δ).
* For v ≠ v*: t·n_v(ω,ω) + N!·n_v(0,δ) − n_v(c) ≥ 0 once t ≥ t₀(R). N is already fixed at that point.
* γ ≤ 0 would put (tω,tω) in L_σ.
* N!/D_σ > γ_σ turns "N!ψ ≥ γ" into "ψ > 0".

All correct.

**Order of choices.** The choices are made in this order: ω, then N, then R, then t ≥ t₀(R). N depends
only on the following, all of which are fixed by G_m alone (λ is chosen once per σ):
* I_σ, D_σ, |⟨λ_σ, c_σ⟩| and γ_σ;
* none of these depends on R, t or δ.

𝓗 is defined by an existence statement over all t and δ, so it does not depend on R. **Consistent.**

**P(t,δ) ∈ NE_M.** This needs δ ≠ 0 and t > N!|δ|_∞, which "t large" covers. The word is primitive by
Lemma 1, so it is in L(G_m) and f ≥ 1.

**Convex geometry.**
* K is a rational polyhedral cone. If K ≠ {0}, it has a non-zero rational ray, and scaling gives an
  integer point. So K = {0}. This also forces 𝓗 ≠ ∅.
* If the ψ_σ did not span the dual, their common kernel would meet K.
* M independent forms define a simplicial cone ≠ {0}, so |𝓗| ≥ M + 1.
* Choose δ off finitely many hyperplanes. Then exactly one of ψ(δ) > 0 and ψ(−δ) > 0 holds, for every
  σ. Both points use the same R and t. So max(f(P(t,δ)), f(P(t,−δ))) ≥ ⌈(M+1)/2⌉ = ⌈m/2⌉, which is
  k + 1 for m = 2k + 1.
* Repeated ψ's are counted with multiplicity on both sides. Fine.

**Quantifiers and the definition.**
* k is the uniform bound sup_w amb_G(w). This is the only meaningful reading, since a cycle-free
  grammar has finitely many trees for every word anyway.
* The same k is used for every slice: G_m depends on m, k does not.
* Trees are counted as derivation trees throughout.
* Lemma 1.1 only decreases tree counts. Lemma 1.2 preserves them on R_m.
* So a word with ≥ k + 1 trees in G_m has ≥ k + 1 trees in G.
* k is arbitrary, so the conclusion holds.

**Transfer to Q.** The only step is G ↦ G × DFA(R_m), i.e. intersection with the regular set R_m.
No other closure property is used.

---

## Fixes (all minor and presentational)

* **F1 (Lemma 4.2, "Moreover").** Replace the sentence by: "If two components each contained a pair,
  they would interleave, contradicting 4.1." This applies to every component, full or not.
* **F2 (§5 notation).** n_v is a functional on span V_σ. V_{σ,0} and V_{σ,1} are only defined when
  W ⊆ span V_σ, which holds whenever ω ∈ int C_σ. In case 2, say explicitly that ⟨λ,c_σ⟩ = 0 gives
  c_σ ∈ span V_σ, so n_v(c_σ) makes sense.
* **F3 (case 2).** "λ_i = −λ_{M+i}" follows at once from W ⊆ span V_σ = λ^⊥. Drop the reference to
  Lemma 4.2.
* **F4 (choice of N).** "N! divisible by D_σ" is never used. What is used: I_σ | N!,
  N! > |⟨λ_σ, c_σ⟩|, and N! > D_σ·γ_σ. Say this.
* **F5 (thresholds).** Take t₀(R) as the maximum over the finitely many σ, and also t₀(R) > N!·R, so that
  P(t,±δ) ∈ NE_M.
* **F6 (interface with Lemma 3).** Lemma 3 is stated for the product with D_n. G_m is the product with
  a DFA for R_m. Use D_n × D_{R_m}, which still recognizes R_m ⊆ (ab*)^n, so the block annotation
  (s,·,t) is available. This is for the Lemma 3 auditor to confirm.
* **F7 (Remark).** In §6, "2(m−1) half-space pieces, ply m−1" is consistent with the computation below
  (pieces ψ = ±δ_i). It is not part of the proof.

## Computational checks (`research/finite_ambiguity/audit_geom/`)

| script | what | result |
|---|---|---|
| `lemma41_exhaustive.py` | Lemma 4.1 on all non-crossing graphs, N ≤ 8 | 0 violations (`lemma41.out`) |
| `lemmaX_exhaustive.py` | Lemma 4.2 + "≤ 1 component with a pair" + "\|V₀\| ≥ 2M−1", all patterns M = 2, 3 | 0 violations; crossing example violates the corollary (`lemmaX.out`) |
| `section5_classify.py 1` | random laminar simple linear sets in M = 2 (r = 1..4, entries ≤ 3, c ∈ [0,4]⁴), ω = (7,11), scaling L = lcm(1..40) in place of N!, window \|δ\|_∞ ≤ 3, t = L·10⁶. Each set is classified as in the proof, and the predicted membership is compared with direct exact membership. | 0 unexplained mismatches. 3518 case 1, 5 case 2, 363 case 3, 56 + 6 case 4 (empty / exact half-plane ψ > 0). Every remaining mismatch is a set that **meets Δ**; an explicit diagonal point was found for each, so the hypothesis does not hold for them (`section5_scaled.out`). |
| `section5_classify.py 2 1` | same, **without** scaling (L = 1) | 48 unexplained mismatches, e.g. V = {2e₁, e₂+e₄, 2e₃, 3e₁+2e₄}, c = (0,4,4,3), whose window pattern is a coset, not a half-plane. This shows that the N! / lattice-fact step is essential and is used correctly (`section5_unscaled.out`). |
| `cover_search.py` | natural pieces and a ply-1 cover search (below) | `cover_search.out` |

Results of `cover_search.py`:

* **Natural pieces.** For x₁<y₁, x₁>y₁, x₂<y₂, x₂>y₂, each is case 4, and its window pattern is
  exactly the half-plane ψ = ±δ₁ or ±δ₂. Together they have ply M = 2 on generic δ, which matches the
  lower bound ⌈3/2⌉ = 2.
* **Other pieces.**
  * The cross-index piece x₁ < y₂ is case 3 and meets Δ, so it is not admissible.
  * The nested "sum-type" piece {y₂ ≥ x₁+1, y₁ ≥ x₂} has C_σ equal to the diagonal line, so it is
    case 1 and empty near the diagonal.
* **Non-laminar piece.** "x₁ = y₁, x₂ < y₂" has crossing periods. Its pattern is the lower-dimensional
  ray {δ₁ = 0, δ₂ > 0}, which no laminar set can produce. With x₁<y₁, x₁>y₁ and "x₁=y₁, x₂>y₂" it
  gives the familiar unambiguous (ply-1) partition. So laminarity is exactly the hypothesis that
  blocks it.
* **Ply-1 cover search.** I built a pool of diagonal-free laminar simple linear sets: 6000 random sets
  plus the natural pieces, keeping those with no diagonal point among coefficients up to 18–25. I then
  ran an exact-cover search (Algorithm X) over the 48 window points.
  * Scaled window: only 6 distinct non-empty patterns, all open half-planes through 0, and **no exact
    cover**.
  * Unscaled window: 93 patterns, and still **no exact cover**.
  * So no M = 2 refutation was found.
  * Limits of this check: the pool is finite and random, and "meets Δ" is tested by bounded search.
    The search is a sanity check, not a proof. The proof's own argument (δ vs −δ with |𝓗| ≥ 3) already
    rules out ply 1 for M = 2.

Note on finite-box searches: covering NE₂ ∩ [1,B]⁴ with ply 1 is trivial (use singletons). So a
meaningful search has to look at near-diagonal asymptotics, as done here, and not at a truncated box.
