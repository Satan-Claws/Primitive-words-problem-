# thmR_unif: does Theorem R give a non-uniformity mechanism against every grammar for Q?

2026-11-24. Inputs: `l6.md` §4 (Theorem R), `realise.md` §§1–2 (pair facets, U1–U3, NONUNIF), `recon.md` §§1–2
(Lemma 3P, Fact A), prompt §§4.3, 6, 7. Scratch check: an inline numpy script, described in §2.

## 0. Verdict

**NO. Theorem R gives no new negative mechanism.** It collapses to pumping (§6 "pumping on letter-count families" /
Ogden-type arguments).

- **What does follow** is Theorem R′ (§1). Any infinite set of marked trees with ≥ 3 gaps at fixed fractions lies on
  a 2-gap pump orbit, and that orbit contains marked trees of L(G) whose marks are *off* the fractions. This
  contradicts something only when the fraction constraint is *universal* over the whole orbit. That is Theorem R's
  "every word of L(G′)" hypothesis, i.e. an *exposed* certificate. A cover needs only *some* tree per word, and that
  tree only on the hard family.
- **The fixed-fraction hypothesis is not even forced (§2).**
  - Certifying δ_k ≠ 0 forces only an *inequality*: the ring tree of the facet μ_k has cyclic extent ≥ s_k = n/p_k
    (Lemma E). Inequalities are semilinear, so Ginsburg–Spanier cannot see them.
  - No single ring span is forced: not ≈ γn, and not ≡ 0 mod s_k. There are admissible facets whose ring trees
    have all spans ≤ 2 (Lemma N).
- **Sanity check.** The naive chain "certifying all N primes ⇒ ≥ 3 fixed-fraction marks ⇒ Theorem R" never used the
  polynomial bound. If it worked it would prove Q non-CF, which is open (prompt §3). The gaps are exactly those
  above: an existential cover, a sparse family not closed under pumping, and inequality-type constraints.

## 1. Part (1): the exact tree-level statement

**Marking scheme.** Fix G (CNF) and k. Let M_G^{(k)} be the set of pairs (w, π), where τ is a tree of w and π is a
set of k selected nodes of τ (for example the tops of two ring C-paths). The marks are put on the a's at the left
and right ends of the selected nodes' yields, so a ring pair {s, t} becomes marked blocks s and t.
- M_G^{(k)} is a CFL over Σ × {0,1}: annotate nonterminals with how many selected nodes lie below them.
- Apply the homomorphism a ↦ c, b ↦ ε, marked a ↦ μ, and intersect with c*μc*⋯μc*. The result is a bounded CFL.
  Its exponent set E ⊆ ℕ^{k+1} is the set of block-gap vectors of marked trees.
- By Ginsburg–Spanier, E is a finite union of stratified linear sets, so every period has support ≤ 2.

**Theorem R′ [written proof].** Let γ ∈ ℝ^{k+1}_{≥0} with Σγ_t = 1 and ≥ 3 positive entries. Let Z ⊆ E be
infinite, with ‖z − γ|z|‖_∞ ≤ C for every z ∈ Z. Then there are z ∈ Z and P ∈ ℕ^{k+1}∖0 with |supp P| ≤ 2 such
that z + mP ∈ E for all m ≥ 0 and ‖(z + mP) − γ|z + mP|‖_∞ ≥ m·c_P − C → ∞.

*Proof.*
1. Some linear set L = c + ℕP_1 + ⋯ + ℕP_r ⊆ E contains infinitely many z ∈ Z. So r ≥ 1; take P = P_1.
2. Then z + mP ∈ L ⊆ E. The deviation D(x) = x − γ|x| is linear, so D(z + mP) = D(z) + m·D(P).
3. D(P) = 0 would mean P = γ|P|, so supp P = supp γ, which has ≥ 3 elements. That contradicts |supp P| ≤ 2. So
   D(P) ≠ 0; put c_P = ‖D(P)‖_∞. ∎

The proof also works with an o(n) tolerance in place of C.

**What this does and does not give.**
- Theorem R in `l6.md` is the special case where every marked word of L(G′) obeys the fractions. Then
  z + mP ∈ E is an immediate contradiction.
- In the cover setting we only know a hypothesis of the form H(F, γ): "every tree (or some tree) of every w ∈ F
  carries selected nodes at γ-fractions." Theorem R′ then produces marked trees (w′, π′) ∈ M_G with
  |w′|_a = n + m|P|, and π′ is off the fractions. **This contradicts H only if w′ ∈ F** (and, for the "every tree"
  form, it then does contradict H).
- So the exact negative statement that follows is:

> **Corollary R′′.** For every CFG G, every marking scheme, and every γ with ≥ 3 positive gaps: no family F ⊆ L(G)
> that is **closed under the block-level periods of E** (i.e. w ∈ F, (w, π) ∈ M_G and z(w, π) + mP ∈ E imply that
> every word carrying the marked tree z + mP lies in F) can have all its marked trees at γ-fractions, unless F is
> finite.

- This is Theorem R relativised to a pump-closed family, nothing more. It is a pumping statement. Theorem W
  (`uniform.md`) is exactly an instance where the family {a^{n−2}bb : pq | n} is pump-closed on a subprogression.
  That is why Theorem W works and is "word-level §6 one witness per prime".

**Toy check that the hypothesis alone is harmless.** G: S → AB, A → aAb | ε, B → cBd | ε.
- On F = {a^m b^m c^m d^m}, the *unique* tree marks the block boundaries m, 2m, 3m, giving 4 gaps all ≈ n/4.
- F is infinite and L(G) is CF.
- The pumps (P = one aAb-turn) give a^{m+j} b^{m+j} c^m d^m ∉ F, with marks off the fractions.
- So "every tree of every word of an infinite family has ≥ 3 fixed-fraction gaps" is consistent with being CF, even
  unambiguous.

**Why the S_N family is not pump-closed.**
- In G_n (fixed n), every pump inserts only b's (`recon.md` §1(a) Step 2). Block-level marks are invariant under
  b-pumps, so at fixed n Theorem R′ has no periods to use.
- All periods P of E have |P| ≥ 1 a's, so they change n. The pumped word w^{(m)} has two runs of copied material
  u^m, v^m inserted. Even when n + m|P| = P_{N′}² (which happens for infinitely many m, because |P| divides
  P_{N′}² for large N′), w^{(m)} is not in the near-U region of its slice. Its block vector is dominated by
  |u|_a-periodic runs, not by a P_{N′}-periodic tω plus small δ.
- Its certifying trees are unconstrained. Showing that they must still carry fixed-fraction chords is a claim about
  arbitrary pumped primitive words, i.e. the pumping route of prompt §6. Second-hand from the literature
  (Dömösi–Ito, *Context-free languages and primitive words*): Q satisfies the Bar-Hillel, Ogden and Bader–Moura
  pumping lemmas, so a pure pump-orbit contradiction cannot exist. [unverified citation; not relied on]

## 2. Part (2): which ring spans certify δ_k ≠ 0

**Setting.** As in `realise.md`, a piece certifies the k-th prime near tω through a facet μ_k with:
- μ_k ⊥ V_{p_k}, equivalently μ_k ∈ im(1 − T^{s_k}) as a functional;
- μ_k|_{E_k} ≠ 0. Then ⊥ U and ⊥ E_j (j ≠ k) are automatic, since U, E_j ⊆ V_{p_k}.

The ring vectors of the piece lie in ker μ_k, except the root ring.

**Fact K (support closure) [written proof].** Let αe_p + βe_q (α, β > 0) be a ring vector in ker μ_k with
μ_k(q) = 0. Then μ_k(p) = 0. So the connected component of the ring-support graph that meets supp μ_k lies inside
supp μ_k. The facet tree T_k is a non-crossing tree on supp μ_k whose edges join opposite signs.

**Lemma E (extent) [written proof].** If μ ≠ 0 and μ ⊥ V_p (s = n/p), then supp μ is not contained in any cyclic
arc of s consecutive blocks. Hence T_k, and the union of its chords, has cyclic extent ≥ s_k. The bound is tight:
μ = δ_r − δ_{r+s}.

*Proof.* μ ⊥ V_p means that for each residue r mod s, the sum of μ over the coset r + sℤ/nℤ is 0. A cyclic arc of
≤ s blocks meets each coset at most once. If supp μ lies in such an arc, every coset sum is a single value of μ,
so μ = 0. ∎

**Lemma N (no span is forced) [written proof + numerical check].** Let ν be the alternating ±1 vector on
[0, s_k) and 0 elsewhere, and put μ = (1 − T^{s_k})ν.
- Then μ ⊥ V_{p_k} by construction.
- Its support is all of [0, 2s_k), with consecutive opposite signs except at the seam s_k − 1, s_k.
- The path made of adjacent edges, plus one skip-2 edge across the seam, is a non-crossing bipartite spanning tree
  with **all spans ≤ 2**. In particular no span is ≈ γn and none is ≡ 0 mod s_k.
- μ|_{E_k} ≠ 0 means that the fold of μ mod P·p_k is nonzero.
- Checked with an inline numpy script for (p_1..p_N) = (2,3), n = 36, all k, and (2,3,5), n = 900, all k: ⊥ V_{p_k}
  True, ⊥ U True, nonzero on E_k True, one component, max span 2.

**Caveat (not claimed).** Lemma N is algebraic admissibility only. On a path tree the transport flows are the
alternating prefix sums of x ≈ tω. Over a full residue cycle these have zero ω-fold. Validity at ω then hinges on
δ-dependent walls, i.e. on extra facets that shrink the piece. Whether short-chord trees give *valid low-ply*
covers is part of TILE_k (open, prompt §4.4(i)). So it is open whether low-ply covers can avoid chords of span
≈ s_k entirely. The `realise.md` pair-facet family does use spans s_k(1 ± p_k/P), which is a choice.

**Consequence for the proposed chain.**
- What is forced per prime is "a connected chord system of extent ≥ n/p_k". In gap coordinates that is a rational
  half-space, and half-spaces are semilinear. It is realisable by a CFG.
- Even if every low-ply cover did use chords of span n/p_k (1 + o(1)) for ≥ 2 primes in one tree, giving ≥ 3
  fractional gaps, Theorem R′ still needs pump-closure (§1), which S_N lacks.
- One tree per mixed word does not contradict L(G) = Q. This is consistent with Q's CF-status being open.

## 3. Status

| claim | status |
|---|---|
| Theorem R′ (fractional marked trees lie on 2-gap pump orbits leaving the fractions) | [written proof] |
| Corollary R′′ (R relativised to pump-closed families) | [written proof] |
| Toy a^m b^m c^m d^m: universal fixed-fraction trees on an infinite family, CF | [written proof] |
| Lemma E: certifying facet's chord system has cyclic extent ≥ n/p_k (tight) | [written proof] |
| Lemma N: admissible facets with all ring spans ≤ 2 exist | [written proof + numerical, n = 36, 900] |
| Validity / low ply of short-chord facets | OPEN (= TILE_k) |
| Theorem R as a non-uniformity mechanism against all G for Q | **FAILS**; collapses to §6 pumping |
