# audit_et.md — gated audit of Theorem ET / Cor ET / Prop E (`r20_dense.md`)

Script: `scripts/audit_et_check.py` (Part 1: Poisson model of ε(g); Part 2: the ET proof run step by step on explicit CNF grammars, ~2 s).

## Verdict: SURVIVES (Theorem ET, Cor ET, Prop E), with minor caveats. No fatal flaw found.

## (a) Theorem ET: the proof, line by line

- **Claim 1 (pieces are short).** Correct. The subtree replacement touches only [0, m). The competitor runs lie in (m, n) and are
  unchanged, so they still force a leading run ≥ m − g in w′ ∈ L ⊆ LeadMax_c. Both cases (y ∈ c\*, y ∉ c\*) are right. The
  case t = 0 with y starting with the other letter gives w′ ∉ LeadMax_c directly. The last letter is unchanged, so the
  convention "does not end with c" (which makes cyclic runs equal linear runs) is kept.
- **Claim 2 (spine).** Correct. Every leaf in [0, m) has a unique maximal ancestor whose yield lies inside [0, m). The
  parent of that ancestor contains position m (R₁ starts at 0), so the ancestor is the left child of an ancestor of leaf m.
  These pieces partition [0, m), so h ≥ m/(C+g).
- **Pumping pairs and blocks.** Correct. U = w[ℓ_j, ℓ_i) ⊆ R₁ and |U| ≥ j − i ≥ g+1 (step g+1, |N|+1 members, span
  |N|(g+1) < B). V = (r_i, r_j] lies right of m. V may be empty, which only helps. Because r_k is monotone, V-intervals from
  different blocks are disjoint.
- **No Ogden case split is needed.** The proof does not use Ogden's lemma. U always lies on the left side of the spine of
  leaf m, so it is inside R₁. V always lies on the right side, at positions ≥ m. The cases "U and V both inside R₁" and
  "V inside R₁" cannot occur for these pairs. This is why the argument is clean.
- **Pump down.** Correct. Position m is in [ℓ_i, r_i], so it is kept, and the leading run becomes exactly m − |U| ≤ m − g − 1.
  A single interval V that meets both R₂ and R₃ must contain the separator after the earlier one. Two disjoint intervals
  V and V′ cannot both contain it, so for one of the two pairs some competitor is untouched. Merges at the seam only
  lengthen it. Then w₀ ∈ L \ LeadMax_c, a contradiction.
- **Adversarial grammars (Part 2).**
  - G1 is a CF grammar for a^{k+1}a⁺ b a^k b a^q b, where the first competitor is nested with the leading run. Take
    w = a⁴¹ b a³⁹ b a³⁹ b with g = 2. The extracted pair puts V *inside the first competitor*, so pump-down shortens the
    leader and that competitor together (lead 38). The second competitor survives at 39. The output is
    w₀ ∈ L, w₀ ∉ LeadMax: exactly the one-partner mechanism.
  - G2 nests both competitors (a^{q+k+r} b a^k b a^q b). It stays inside LeadMax_a, but nesting forces k + q ≤ m, so
    near-ties are impossible. This is consistent with ET.
  - I found no CF construction that couples two competitors to the leading run through a single V.

## (b) Consistency (F1, the literature)

- **Q is not in LeadMax.** abaab ∈ Q is in neither LeadMax_a nor LeadMax_b (confirmed). ET is ambiguity-free and says
  nothing about Q. This matches F1.
- **ET is stronger than Berstel–Boasson, and consistent with it.** Berstel–Boasson (Bull. EATCS 63, 1997, pp. 139–140,
  citation verified) show that the Lyndon set is not CF. The Lyndon set is rotation-dense, so Cor ET implies their result.
- **No known dense CF subset of the Lyndon words contradicts it.** The natural candidates have their competitors coupled
  by nesting (like G2), which forces competitors ≤ m/2. Their rotation density → 0, consistent with ET.
- **Regular sets are consistent too.** Cor ET implies that no *regular* L ⊆ LeadMax is rotation-dense. This is true
  directly: a regular set has a bounded or pumpable leading run.

## (c) The run-statistics step

- **The method is standard.** It is the Poisson approximation for the number of long runs (Erdős–Rényi / Arratia–Gordon–
  Waterman). The report gives it as "[cited/standard]" without a specific reference. **Caveat:** add a citation.
- **Part 1 checks it.** I used the Poisson model with independent counts at each level, X_k ~ Poi(μ2^{−k}).
  - ε(g) = P(#c-runs ≥ M−g ≤ 2) comes out as .586, .327, .172, .088, .022 for g = 1, 2, 3, 4, 6.
  - This is the same within ±1e-4 for every fractional part of log₂ μ, so the lattice oscillation of the maximum does not
    affect this statistic.
  - 2^g ε(g) → 1.44, so ε(g) ≈ 1.44·2^{−g} → 0.
  - These values match the report's MC and my rerun of `r20_dense_ties.py`: .59, .33, .17, .09, .02.
- **Minor caveat.** A_n(g) should be the *union* of the a-version and the b-version, because L splits by first letter.
  This gives a density bound of 2ε(g) instead of ε(g), which is harmless.

## (d) Prop E

- **The logic is correct, and nearly tautological.** If DENSE-SOUND holds, FOLD would give L′ ⊆ σ(G⁻). Applying T8_poly
  to σ⁻¹L′ gives a contradiction. If ¬DENSE-SOUND holds, FOLD is vacuous.
- **What it relies on.** T8_poly must be invariant under the 4 symmetries (σ preserves context-freeness, ambiguity, Q and
  density). FOLD must require L′ to be poly-amb CF.
- **The "¬DENSE-SOUND ⇒ negative answer" step** holds because Q itself is rotation-dense.
- **Not audited.** I did not audit the appeal to r5_generic §1(a).

## Caveats (not fatal)

1. **Lemma PP and the classification table are heuristic.** "Partner principle ⇒ dead" is proved only for the ET
   instance (and for Thm X/V elsewhere). Conjecture PP-class is correctly labelled open.
2. **The g+1 remark for strict sets is unnecessary.** L_U and Lyndon are already ⊆ LeadMax_c, so ET applies to them as
   stated.
3. **Non-fold claim not audited.** The claim "Lyndon/UMR are non-fold, ≈ c·log n/√n" is MC only. The fit is plausible
   (ratio of the data to log n/√n ≈ 1.06–1.15).
4. **Write ET's constants explicitly:** M₀ = 2B(C+g) with B = (g+1)|N|+1.
