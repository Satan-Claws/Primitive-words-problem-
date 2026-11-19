# poly_S3L: abstract lower bound D ≥ P−1 for chain-valid covers; with S3E, D ∈ {P−1, P} (agent S3L)

Setting: poly_S3Q.md (Π(T), D, R_T, Π(T) ⊆ Lin(R_T)), poly_S2Q.md §1 (Lemma 1), poly_S3E.md (star trees, D ≤ P).
μ abstract: fibre sums 0, genericity μ(S_u) ≠ 0 (chain-validity then gives s_u μ(S_u) > 0, S3Q §1), and
subset-genericity (no proper nonempty subset of a fibre has μ-sum 0). ρ = root fibre, P = P_N.
Status: **PROVED (abstract, any μ with the two genericity conditions): every chain-valid T has
|Π(T)| ≤ P!/(P−1), hence D ≥ P−1. With S3E: D ∈ {P−1, P}. So D_k ≥ P_N − 1 ≫ p_k^{O(1)}: the chain-valid
order-cone selection can NOT block S_N; ∏_k D_k ≥ (P_N−1)^N, no better than the natural cover.**
The hint's form "π_1 ∈ F_T, |F_T| ≤ c" is FALSE in general (fibres can nest; many fibres can be π_1-admissible), but
the weaker "every fibre ≠ ρ is constrained" suffices.

## 1. Lemma A (every non-root fibre is in R_T) — PROVED
R_T = {(res v, r) : v splits r, r ≠ res v}; π ∈ Π(T) ⇒ res v <_π r for each pair (S3Q §4, via Lemma 1 +
subset-genericity). Claim: if Π(T) ≠ ∅, every fibre q ≠ ρ occurs in some pair of R_T.
Proof. Suppose q ≠ ρ occurs in no pair. Then (i) no foreign vertex splits q; (ii) a fibre-q vertex d splits no
other fibre, so f_d = μ(S_d ∩ q)·e_q. Let x be a deepest vertex with S_x ⊇ fibre q (root qualifies, so x exists).
- x of fibre q: x ≠ root (q ≠ ρ), f_x[q] = μ(q) = 0 and by (ii) f_x = 0, so μ(S_x) = 0 — contradicts genericity.
- x foreign: by maximal depth no child contains all of q; a child d meeting q splits q, so by (i) d has fibre q and
  by (ii) f_d = μ(S_d∩q)e_q, whose last prefix sum gives s_d μ(S_d∩q) > 0. All such d have the same sign −s_x and
  Σ_d μ(S_d∩q) = μ(q) = 0 (x ∉ q). Contradiction. ∎

## 2. Lemma B (connected posets) — PROVED
If a relation R on an s-set has connected comparability graph, e(R) ≤ s!/s = (s−1)!.
Proof: among the s cyclic rotations of any order, at most one extends R: if σ = (A,B) and (B,A) both extend R
(A, B ≠ ∅), every relation between A and B would point both ways, so none exists — disconnected. ∎
For components C_1..C_m of R (|C_i| ≥ 2), restrictions of a uniform π to disjoint sets are independent, so
Pr_π[π ∈ Lin(R)] ≤ ∏ 1/|C_i|.

## 3. Theorem: |Π(T)| ≤ P!/(P−1), D ≥ P−1 — PROVED
By Lemma A the nontrivial components of R_T cover ≥ P−1 fibres; for a, b ≥ 2, ab ≥ a+b, so ∏|C_i| ≥ Σ|C_i| ≥ P−1.
Hence |Π(T)| ≤ |Lin(R_T)| ≤ P!/(P−1), and any cover of S_P by sets Π(T) needs ≥ P−1 trees.
Tightness: S3E star trees have |Π(T_ρ)| = (P−1)! = P!/P (R_T = star out of ρ), and P of them cover; D ∈ {P−1, P}.

## 4. Consequences / caveats
- Applies to the real μ_k as soon as μ_k is generic + subset-generic (NC/supp only make D larger). If μ_k has a
  zero-sum proper subset of a fibre, Lemma 1's "splits ⇒ f_v(r) ≠ 0" step fails and §1 needs re-checking (OPEN, minor).
- Patching ply via this selection: ply_VC·∏D_k ≥ (P_N−1)^N ≈ n^{N/2}: no gain over the natural cover. The chain-valid
  (order-cone) route to TILE_k with small ply is DEAD; TILE_k itself (non-chain-valid cones, which avoid ω = 1 per
  S3Q §2) is untouched and OPEN.
