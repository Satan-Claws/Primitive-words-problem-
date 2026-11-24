# r20_dense.md — R20-D: DENSE-SOUND ⇒ fold? Classifying dense sound certificates

Scripts:
- `scripts/r20_dense_ties.py`: Monte Carlo of the near-tie survivor probabilities used in Cor ET (about 1 s).
- `scripts/r20_dense_lyndon_fold.py`: Monte Carlo testing whether the Lyndon and canonical-UMR certificates lie in the fold region (about 1 s).

## Verdict

1. **The structural claim cannot be a lemma** [written, logically exact; Prop E]. Assume T8_poly. Then "every rotation-dense
   poly-amb CFL L ⊆ Q has a rotation-dense CF part inside G⁻ (up to the dihedral/letter-swap symmetries)" is *equivalent*
   to ¬DENSE-SOUND. ¬DENSE-SOUND in turn implies the negative answer, and by r5_generic §1(a) it needs ambiguity
   essentially. So the bridge via soundness + density is not easier than the problem. It is a strengthening of it.
2. **Non-fold dense sound certificates exist, but their CF parts are dead at ANY ambiguity** [new; written proof; Theorem ET].
   - The Lyndon words, the canonical UMR language L_U, and more generally every "anchored extremal run" set are sound and
     rotation-dense. They are *not* fold-type: their intersection with the dihedral images of G⁻ has relative density
     ≈ c·log n/√n → 0 [MC].
   - Theorem ET: no context-free L inside any of them is rotation-dense, whatever its ambiguity.
   - This closes the UMR lead of r5 in its anchored form. The proof is a pumping/interchange argument with *near-ties*. A
     CF pumping pair (U, V) gives the pumped quantity exactly **one partner interval V**. An extremal-run certificate needs
     the run to beat ≥ 2 separated near-competitors.
3. **Partner principle (classification picture)** [lemma written; classification is a conjecture]. Every dense sound
   certificate class examined so far falls into one of two groups.
   - (A) It needs ≥ 2 partners per pumped quantity. These classes are dead at any ambiguity: ET here, and Theorem X/V for
     chords.
   - (B) It is one-partner, which means a mirror comparison, i.e. the fold. Finite-memory folds are dead (Prop K). The
     unbounded-memory part inside G⁻ is dead at polynomial ambiguity (T8_poly).
   - **Still open:** (i) the one-partner sets that are *not* inside G⁻: F_K/F_δ (window folds), and the general d-sign
     sets; (ii) the unique-factor certificates, where near-ties vanish at the Hamming scale, so ET does not apply;
     (iii) UMR_cyc (unique longest run, unanchored), where seam merges block the proof.

Status: **DENSE-SOUND ⇒ fold is NOT proved.** The result is a partial classification. Group (A) is eliminated
unconditionally. Group (B) is reduced to the fold-counter family, as before.

## 1. Prop E (logical status of the bridge) [written]

Let FOLD be the statement: every rotation-dense poly-amb CFL L ⊆ Q has a poly-amb CF sublanguage L′ ⊆ σ(G⁻) (σ one of
the 4 symmetries) with Rot(L′) of positive density.
- (⇐) If ¬DENSE-SOUND holds, there is no such L, so FOLD is vacuous.
- (⇒) Suppose L witnesses DENSE-SOUND. Then FOLD would give L′, and T8_poly applied to σ⁻¹L′ contradicts it.
- So under T8_poly, FOLD ⟺ ¬DENSE-SOUND.

By r5_generic §1(a), an ambiguity-blind proof of ¬DENSE-SOUND would show that Q is not CF. So any proof of FOLD must use
the polynomial ambiguity bound in an essential way, beyond the renewal step that already sits inside T8_poly. ∎

**Consequence.** "Classify dense sound certificates" is meaningful only class by class. The useful output is a list of
certificate classes each killed by its own squeeze. That is what §2–§3 give.

## 2. Theorem ET (extremal-tie obstruction, any ambiguity) [written proof]

**Sets.** Let c ∈ {a, b} be a letter.
- LeadMax_c = { w : w starts with c, and the c-run at position 0, of length m(w), is ≥ every other cyclic c-run }.
  In this set the run at position 0 is taken *maximal*, i.e. w does not end with c.
- It contains L_U = canonical UMR = { b^m x : x ∈ aΣ\*a, every b-run of x is < m }, which is ⊆ Q.
- It contains the Lyndon words (order a < b) of length ≥ 2: a Lyndon word starts with a longest a-run, else the rotation
  at a longer run is lexicographically smaller. It also contains their mirror (b < a) through c = b.
- Lyndon ⊆ Q, and Lyndon is rotation-dense, since every primitive word has exactly one Lyndon rotation.

For w ∈ LeadMax_c, let N_g(w) be the number of c-runs other than the leading one with length ≥ m − g.

**Theorem ET.** Let L be context-free with L ⊆ LeadMax_c, and fix g ≥ 1. Then there is M₀ = M₀(G, g) such that no w ∈ L has
m(w) ≥ M₀ and N_{g}(w) ≥ 2.
- For the strict sets (L_U, Lyndon with tie allowance) use g+1 in place of g; only constants change.
- The statement uses no ambiguity hypothesis.

*Proof.*
1. **Setup.** Take G in CNF for L, reduced, with nonterminal set N. Let C = max_X min{|y| : y ∈ L(X)}. Take w ∈ L with a
   derivation tree τ. Its leading run is R₁ = [0, m), and position m holds the other letter. Its competitors R₂, R₃ have
   length ≥ m − g; the competitors are runs of the same letter and are not R₁.
2. **Claim 1 (pieces are short).** Let a node Z have yield inside R₁, say c^s at offset t. Then s < C + g + 1.
   - Replace Z's subtree by a tree for a shortest y ∈ L(X_Z). The new word w′ lies in L ⊆ LeadMax_c. Every competitor
     run is untouched, so the leading run of w′ must have length ≥ m − g.
   - If y ∈ c\*: the leading run is m − s + |y| ≤ m − s + C, so s ≤ C + g.
   - Otherwise the leading run is < t + C. This forces t > m − g − C, and then s ≤ m − t < g + C.
   - (If y starts with the other letter and t = 0, w′ ∉ LeadMax_c. That is impossible, so this case does not occur.)
3. **Claim 2 (a long one-sided spine).** Take a node Z maximal with yield ⊆ R₁. Its parent's yield is an interval that
   leaves [0, m), so it contains position m. Hence Z is the left child of an ancestor of leaf m.
   - The left children of ancestors of leaf m that do not contain m are exactly these maximal Z.
   - So the number h of such ancestors satisfies h ≥ m/(C + g).
   - Order them bottom-up as P₁ ⊂ … ⊂ P_h, with yields [ℓ_k, r_k]. Then ℓ_k ≤ m ≤ r_k.
4. **Pumping pairs.** For i < j with X(P_i) = X(P_j), set U = w[ℓ_j, ℓ_i) ∈ c⁺ and V = w(r_i, r_j]. Then
   w_t = w[0, ℓ_j) U^t w[ℓ_i, r_i] V^t w(r_j, n) ∈ L for every t ≥ 0. Each of P_{i+1}, …, P_j contributes its nonempty
   left child to U, so |U| ≥ j − i.
5. **Blocks.** Cut the ancestor list into disjoint blocks of B = (g+1)|N| + 1 consecutive indices. In each block the
   subsequence with step g+1 has |N| + 1 members, so it contains a pair with j − i ≥ g + 1, hence |U| ≥ g + 1.
   - Pairs from different blocks have **pairwise disjoint** V-intervals, since the r_k are monotone.
   - With h ≥ 2B, there are two pairs with disjoint V, V′.
6. **Pump down (t = 0).** The new word starts with c^{m−|U|}. The letter at position m is kept, because it lies in P_i.
   - V is one interval. If it met both R₂ and R₃, it would contain the separator letter right after the earlier of them.
     V and V′ cannot both contain that letter.
   - So for one of the two pairs, a competitor (say R₂) survives intact. Seam merges can only lengthen it.
   - Hence w₀ has a non-leading c-run of length ≥ m − g > m − |U|, the leading run. So w₀ ∉ LeadMax_c, while w₀ ∈ L.
     Contradiction.
7. Therefore h < 2B, i.e. m < 2B(C + g) =: M₀. ∎

*Remark (where it bites).* Steps 4–6 are the **partner principle**. A pumped segment inside the distinguished feature is
coupled to a *single* interval V. The certificate needs the feature to dominate ≥ 2 separated near-competitors, and
both cannot sit inside one V while disjoint pairs exist.

**Corollary ET.** No context-free L ⊆ LeadMax_a ∪ LeadMax_b is rotation-dense, at any ambiguity. In particular this holds
for every CF set of Lyndon words, and for every CF L ⊆ L_U.

*Proof.*
1. Set A_n(g) = {w ∈ Σⁿ : the maximal cyclic c-run length m satisfies m < M₀(g) or N_g ≤ 1}. This is
   rotation-invariant, and Rot(L)_n ⊆ A_n(g) by Theorem ET.
2. P(m < M₀) = e^{−Ω(n)}.
3. P(N_g ≤ 1) → ε(g) as n → ∞. This is extreme-value statistics of i.i.d. geometric run lengths: given the top run, the
   number of runs within g of it is unbounded in probability as g → ∞, and P(gap ≥ g) ≍ 2^{−g}.
   - This step is a standard Poisson approximation of run counts. It is [cited/standard] here and checked by MC below.
4. So limsup dens Rot(L) ≤ ε(g) for every g, and ε(g) → 0. ∎

| n | P(unique max b-run) | P(N_g ≤ 1), g = 1, 2, 3, 4, 6 |
|---|---|---|
| 1024 | .72 | .59 .32 .17 .09 .02 |
| 4096 | .72 | .60 .35 .17 .08 .02 |
| 65536 | .72 | .61 .34 .19 .10 .03 |

Source: `r20_dense_ties.py`. ε(g) ≈ 2^{−g} and is stable in n. (This also corrects r5's figure: the unique *b*-run
probability is ≈ 0.72; the figure 0.36 there refers to a unique longest run over both letters.)

**These certificates are not fold-type** [MC, `r20_dense_lyndon_fold.py`]. Consider the fraction of canonical Lyndon
(resp. UMR) words for which some dihedral/letter-swap image lies in G⁻:

| n | Lyndon | UMR |
|---|---|---|
| 64 | .60 | .62 |
| 256 | .40 | .40 |
| 1024 | .23 | .25 |

This fits c·log n/√n: the long leading run gives a head start of length m ≈ log n, then a ballot walk follows. So
Lyndon and UMR are genuinely non-fold dense sound certificates. "DENSE-SOUND ⇒ fold" therefore cannot hold at the level
of *certificate sets*. It can only hold through CF-ness, and for these classes Theorem ET supplies the missing
CF-obstruction directly, without any fold.

**Scope and limits of ET.**
- **Not covered: UMR_cyc** (unique longest b-run anywhere, unanchored). Pump-down then makes R₂ the new unique champion.
  The contradiction needs a tie between R₂ and R₃ to survive, and a seam merge at V can create a new longest run. Control
  of the runs adjacent to r_i and r_j is missing, because the grammar can align them adversarially. **OPEN.**
- **Not covered: unique-factor certificates** ("y occurs once cyclically", |y| ≈ 2 log n). At the Hamming scale near-ties
  are absent, since E#(occurrences within distance g) → 0. So the tie mechanism does not apply. **OPEN.** This is the
  most natural remaining non-fold, non-run class.
- Consistency with F1: ET is ambiguity-free, but LeadMax ⊉ Q. For example, abaab ∈ Q is in neither LeadMax_a nor
  LeadMax_b: its leading a-run is shorter than the a-run aa, and it does not start with b. So ET says nothing about Q
  itself, as it must not.

## 3. The partner principle and the classification attempt (direction 2)

**Lemma PP (one partner)** [trivial, written]. In any CF derivation, an iterable pair is (U, V) with U and V each a
*single interval*, and pumping changes the word only there. A certificate predicate Φ that is monotone in a quantity q(U)
must be balanced against quantities inside V alone. Anything Φ compares q(U) with outside V is fixed under pumping.

How each known class fares:

| class | partners needed per pumped quantity | fate |
|---|---|---|
| exposed chords / one mismatch per prime (Prop U, Thm V/X) | one per prime, i.e. ≥ 2 | dead, any ambiguity |
| anchored extremal run (Lyndon, L_U, LeadMax) | ≥ 2 (near-ties) | **dead, any ambiguity (Thm ET)** |
| count / Parikh (Thm P_K) | none (global count) | density O(n^{−1/2}), dead |
| finite-memory fold (Prop K) | 1 (mirror) | dead, any ambiguity |
| unbounded fold inside G⁻ (G⁻, Λ = strict cycle-lemma words, L_A) | 1 (mirror) | dead at polynomial ambiguity (T8_poly) |
| window folds F_K, F_δ (d-sign on [n/3, n/2]) | 1 (mirror) | **OPEN** (not inside G⁻) |
| UMR_cyc, unique-factor | ≥ 2 but unanchored / no near-ties | **OPEN** |

**Conjecture PP-class** [conjecture]. Let a rotation-dense CF L ⊆ Q be given. Then a.e. word of L, along a critical linear SCC,
is certified by a one-partner (mirror) comparison of cumulative counts across the fold.

The ET mechanism is evidence for the "≥ 2 partners ⇒ dead" half. The open half is "one partner ⇒ inside a T8-squeezable
region". The visible gap is the window folds F_K: they are one-partner but are not inside G⁻. Extending T8_poly from G⁻ to
F_K⁻ = {d_k < 0 on [n/3, n/2]} would be the next concrete step. That is region work (owner B, `r20_region.md`).

## Status

| claim | label |
|---|---|
| Prop E (FOLD ⟺ ¬DENSE-SOUND under T8_poly; needs ambiguity) | written, logically exact |
| Theorem ET (LeadMax / Lyndon / L_U: near-tie words excluded) | written proof, any ambiguity; **unaudited** |
| Cor ET (no CF subset of Lyndon words or of L_U is rotation-dense) | written; the run-statistics step is standard, MC-checked |
| Lyndon / UMR are not fold-type (≈ c·log n/√n inside σ(G⁻)) | MC |
| Lemma PP | written (trivial) |
| Conjecture PP-class (DENSE-SOUND ⇒ fold) | OPEN; gaps: F_K-type window folds, UMR_cyc, unique-factor |
| main problem | OPEN |
