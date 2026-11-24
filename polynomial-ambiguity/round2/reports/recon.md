# recon: independent reconstruction of structure (c), Lemma 3P, Lemma F, S3D refinement

W1-C, 2026-11-24. Audit-style reconstruction, not a gated audit. PA/ = `claude_2026-11-18_to_11-19/reports/`.
Script: `round2/scripts/recon_checks.py`.

**Verdict.**
- Structure (c): CONFIRMED.
- Lemma 3P: CONFIRMED. One hypothesis made explicit: K's independence of n needs a slice DFA with O(1) useful
  states per block.
- S3D refinement: CONFIRMED for union, laminarity and ply. It does NOT preserve ‖c‖₁ ≤ nK.
- Lemma F: REPAIRED. The offset bound is inherited from the big slice. Corollary F changes constants.
  Theorem P is unaffected.
- No fatal flaw found.

## 0. Setting rebuilt from definitions
- G'' is CNF of G. G_m = ((G''×D_R)×D_n), reduced, with n = 2m. Tree counts only drop (Lean-checked).
- In D_n, the a-count fixes the state: the a's covered by a nonterminal decide its D_n annotation.
- Every nonterminal is useful. So every (sub)tree occurs in a tree of a word of R_m ⊆ (ab*)^n, which has exactly n a's.

## 1. Structure part (c) under amb ≤ C|w|^k — CONFIRMED [written proof, reconstructed]

**(a) Linearity, ambiguity.md Thm A Step 1.** Suppose X → YZ with Y, Z ∈ C.
- If L(X) has a word with an a, nesting gives words with more than n a's. This is impossible.
- Otherwise the Catalan argument gives C_r ≈ 4^r/r^{3/2} trees on one word of length O(r).
- That is superpolynomial, so the step needs only polynomial ambiguity.

**(a) Step 2 (no ambiguity used).** A side child Z of a cycle X ⇒⁺ uXv lies in u or v.
- Pumping the cycle repeats Z, so an a in L(Z) would give more than n a's.
- So **a-containing pumps are impossible: every pump inserts only b's.** The reason is the fixed a-count of
  (ab*)^n, not ambiguity.
- Z is annotated (s,Z,s) or (t,Z,t). So all of C carries one annotation (s,t). Left side material is in block s
  (b-loop at state s), right side material in block t.
- If s = 0, D_n has no b-loop, so there are no left side children (F2).

**(c) Two first-return contexts κ₁ ≠ κ₂ at X.** Each κ_j inserts b^{p_j} directly left of X's yield (block s)
and b^{q_j} directly right (block t).
- For ε ∈ {12,21}^N, outer∘κ_{ε₁}∘…∘T_X adds N(p₁+p₂) b's to block s and N(q₁+q₂) to block t.
- The yield is the same for every ε. Each block's insertion is a contiguous b-run, so order is irrelevant even
  when s ≠ t (two different blocks).
- Distinctness: by linearity and (b), the C-nodes below the top inserted X form one path. The first-return
  decomposition of that path is unique, so ε is read off the tree.
- So there are 2^N trees on one word of length |w₀| + N·O(1). This exceeds C|w|^k for large N. ∎

**Consequences** (the argument is reused verbatim):
- One ring rule per X, so C is a simple cycle.
- Side children have a unique tree. Two trees of Z give two first-return contexts, via a shortest return path
  (F4); their yields may differ, and the {12,21} trick handles that.
- F3: no nontrivial-SCC node inside a side subtree.
- Pumps into two *different rings* are not part of (c). They are what (d) parametrises: independent q_π, possibly
  with d_σ > 0.

## 2. Lemma 3P — CONFIRMED (one hypothesis made explicit)

**Bijection.** A maximal C-path of a tree enters the ring at X_i and exits at X_j, with length (j−i mod r) + q·r.
- Side trees are unique, so the q full turns are identical and deleting them loses nothing.
- After the exit, the tree cannot re-enter C (SCC). So one C cannot contribute two nested paths.
- Hence tree ↔ (σ, q ∈ ℕ^{r_σ}) is a bijection, and exp(yield) = c_σ + Σ q_π v_π.
- Summing fibres gives amb(w) = Σ_σ P_σ(exp w − c_σ), with V_σ taken as a *list*.
- **No double counting:** σ and q are recovered from the tree.
- Two C-paths of the same ring can occur in one skeleton only when s = t, i.e. b-only rings at incomparable nodes.
  They give repeated vectors (d ≥ 1). The list-P_σ handles this correctly.

**Pair support (why not three blocks).** One turn hangs only side children.
- Those are b-only and annotated (s,·,s) on the left or (t,·,t) on the right of a node annotated (s,t).
- Hence supp v ⊆ {s,t}. A third block would need a b-subtree not adjacent to the ring's span ends. That is
  impossible, because every ring node has yield from state s to state t.

**Laminarity** (from tree nesting). Let π, π' be two C-paths.
- If their tops are comparable, π' lies in an exit subtree of π. It cannot lie in a side subtree (F3) or on π
  itself (maximality). So s ≤ s' ≤ t' ≤ t.
- If the tops are incomparable, the yields are disjoint factors, so t ≤ s' or t' ≤ s.
- In neither case do the pairs cross. Correct.

**Constants** (poly_T2b §1, re-derived).
- *Fact A.* A nonterminal of G_m covering a-range [i..j] has its D_n part forced to (i−1, j).
  - **The n+1 states of D_n never multiply class sizes**, because the D_n annotation is a function of position.
  - The only freedom is the D_R states: p ∈ S_{i−1}, q ∈ S_j.
  - For the minimal DFA of R_m, |S_i| ≤ 2 ("after a", "after ≥1 b"; the sink is useless).
  - So each class has ≤ h = 4|V''| members. The same holds for b-only nonterminals of block s.
- The skeleton has no repeated nonterminal on any root–leaf path. Hence:
  - b-subtree yield ≤ K₁ = 2^{h−1};
  - ring length ≤ h, so ‖v‖₁ ≤ hK₁;
  - the unary chains of T_a number ≤ 2n−1, each ≤ h nodes, so ‖c_σ‖₁ ≤ (2n−1)hK₁ ≤ nK with K = 2hK₁ =
    |V''|·2^{4|V''|+2}.
- Arithmetic checks.
- **Hypothesis to state explicitly:** K is independent of n *because* the slice DFA D_R has O(1) useful states per
  block. For the general slices in prompt §4.3 ("or any sub-slice"), replace 4 by |S|² with
  |S| = max_i |S_i| (|S| = 1 for (ab*)^n itself). A slice family whose DFA needs growing per-block memory gets a
  K that grows with n.
- Skeleton count ≤ C(n(K+1))^k (e(K+1))^n = exp(O(n)). Correct.
- d_σ ≤ k: (L) with q = t·1 + z, z ∈ ker, is correct.

## 3. S3D (Ito / Eilenberg–Schützenberger refinement to d_σ = 0) — CONFIRMED for ply; caveat on offsets

**Proof of the refinement** (self-contained; the literature citation is not needed). Call q ∈ ℕ^r *non-lex-min*
if another q' in its fibre is lex-smaller.
- The non-lex-min vectors form an upward-closed set: q' <_lex q implies q'+e <_lex q+e.
- Its complement N is a finite disjoint union of sets f + ℕ^S (Stanley decomposition).
- V is injective on N. So V_S is independent on each piece: an integer relation α⁺ − α⁻ would give two points of
  f + ℕ^S with the same image.
- Hence c + ℕV = ⊔ (c + Vf + ℕV_S), with V_S ⊆ V independent.

**What it preserves.**
- Union, avoidance and laminarity are preserved (V_S is a sublist).
- The new ply at u is exactly #{σ : u ∈ L_σ} ≤ Σ P_σ = amb(u). **Ply is preserved.**
- r ≤ n holds trivially.

**What it does not preserve.** The offsets c + Vf and the piece count are **not** controlled.
- Laminar example: V = {e₁, 2e_i+e_{i+1} (i ≤ ρ), e_{ρ+1}} ⊂ ℕ^{ρ+1}, with d = 1.
- Its kernel vector has entries up to 2^ρ (checked for ρ ≤ 8). The lex-min ideal generator has a coordinate
  2^{ρ−1}, so some refined piece has ‖offset‖₁ ≥ 2^{ρ−1}.
- So "one may take d_σ = 0" (prompt §4.3) must not be combined with ‖c_σ‖₁ ≤ nK or #σ ≤ exp(O(n)).
- It is unknown whether some other refinement keeps the offsets small. S3D's own conclusion (route BLOCKED at
  cover level) is unaffected.

## 4. Lemma F (face restriction) — REPAIRED

**The restriction identity is correct.**
- c_σ ∈ L_σ ⊆ ℕ_{≥1}^{2M}, because every (σ, 0) is a tree of a word of R_m.
- z_k = 1 for k ∉ J forces c_k = 1 and q_v = 0 whenever v_k > 0.
- So L_σ ∩ F_I = c + ℕV_{σ,J} and P restricts to P_{V_{σ,J}}.
- The other properties also hold: laminarity in the induced order, Δ_r-avoidance, covering of NE_r, ‖v‖₁ ≤ K,
  and r_{σ,J} ≤ 2r + k (a sublist has d ≤ d_σ).

**First unsupported step:** "valid cover of NE_r *with the same K*". The valid-cover definition (poly_G4 header)
includes ‖c_σ‖₁ ≤ n_r K with n_r = 2(r+1). The restriction only gives ‖c_J‖₁ ≤ ‖c_σ‖₁ − 2(M−r) ≤ 2mK.
- The T2b chain argument cannot localise this. A single block can receive b's from Θ(n) nested unary chains:
  all a-ranges [s+1..j], j = s+1..n.
- Toy grammar S → aU, U → BUA | a, B → b, A → aC, C → bC | b. In (ab*)^n its unique skeleton puts n−2 b's in
  block 1. Fixing every other free block to 1 leaves a one-coordinate face whose piece has offset n−2 = Θ(n),
  with r = 1. (Not a Q-grammar; it shows that the skeleton bounds alone do not give the claim.)

**Repaired Lemma F.** The family {L_σ ∩ F_I} is a valid cover of NE_r with ‖v‖₁ ≤ K, r_σ ≤ 2r+k, and
**‖c_σ‖₁ ≤ 2mK (the original n = 2m)**.

**Effect on Corollary F.**
- Theorem E at M = r uses Papadimitriou with a = max(|A|, |b|). As stated, it would give
  (r²mK)^{O(r²)} = m^{O(r²)}. That is still poly(m) for constant ply, but superpolynomial at
  p ≈ √(log m/log log m).
- Repair: use proximity in place of Papadimitriou.
  - Take min 1·x over {Ax = b, x ≥ 0}. The LP vertex has ‖x*‖∞ ≤ ‖b‖₁Δ (Cramer).
  - Cook–Gerards–Schrijver–Tardos (1986) gives an integer optimum within NΔ.
  - Here Δ ≤ (√R·K)^R, R ≤ r² rows, entries of A ≤ K. So ‖q‖∞ ≤ (4smK + N)Δ.
- **Corollary F′:** ply ≥ p at ℓ¹-norm ≤ 2m + m·exp(O(p² log(pK))). Ply 2 is at O(m)·K^{O(1)}, not
  2m + K^{O(1)}.

**Theorem P (POLY_FINAL §1, step 7) is unaffected.**
- Taking m = 2p−1 directly (no face) gives Theorem E with ‖c‖₁ ≤ 2mK = O(pK).
- So L = exp(O(p² log pK)), i.e. p = Ω(√(log L/log log L)). With Cor F′ the large-m version also still holds.

## 5. Status labels
- Structure (c) under polynomial ambiguity: PROVED (reconstructed).
- Lemma 3P (formula, pair support, laminarity, d_σ ≤ k, K = |V''|2^{4|V''|+2} for R_m-type slices with
  ≤ 2 states per block): PROVED (reconstructed).
- S3D refinement: PROVED for union, laminarity and ply. FALSE-AS-COMBINED with the offset/count bounds (example above).
- Lemma F: REPAIRED (offsets ≤ 2mK). Corollary F′ as above. Theorem P intact.
