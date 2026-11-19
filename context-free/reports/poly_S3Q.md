# poly_S3Q: Q2 for order-cone selection — every chain-valid K_T meets ALL order cones; ply = #distinct trees (agent S3Q)

Setting: poly_S2Y.md §1–2, §4 (Q1, Q2); poly_S2Q.md §1 (π-monotonicity). ω ∈ ℝ^P_{>0}, P = P_N, f_u = fold(μ_k|S_u),
s_u = top sign, L_π = prefix-sum map in π-order. Genericity as in S2Y: μ(S_u) ≠ 0 for every subtree vertex set.
Status: **Q2 as posed is FALSE (PROVED): each chain-valid K_{T(π)} meets all P! order cones. Reformulation PROVED:
the order-cone-selection family has ply exactly D := #distinct trees in {T(π)}. Lower bound D ≥ 2 (PROVED);
D ≤ p^{O(1)} vs superpoly OPEN.**

## 1. Upper-triangular structure (PROVED, from S2Q Lemma 1)
Order the non-root vertices by pos(res u) and write the row vectors L_π f_u ∈ ℝ^P. Chain-validity + Lemma 1 give
  (L_π f_u)(j) = 0 for j < pos(res u),   s_u (L_π f_u)(j) ≥ 0 for j ≥ pos(res u),   s_u (L_π f_u)(P) = s_u μ(S_u) > 0.
So the matrix (s_u L_π f_u)_u is a nonnegative staircase ("π-upper-triangular") matrix whose LAST column is strictly
positive. In c-coordinates ω = Σ_j c_j 1_{A_j} (c_j = ω_{π_j} − ω_{π_{j+1}}, c_P = ω_{π_P}),
n_u(ω) = Σ_j c_j (L_π f_u)(j).
Dual-basis folds are impossible: L_π f_u ∝ e_j with j < P forces μ(S_u) = (L_π f_u)(P) = 0, contradicting genericity.
Only f_u ∝ e_{π_P} (single-fibre) is a "dual" form; hence K_T = O_π never holds (also by §2).

## 2. Theorem: 1 ∈ int K_T for every chain-valid T (PROVED)
⟨f_u, 1⟩ = μ(S_u) = (L_π f_u)(P), which has sign s_u strictly (last column of §1). Thus 1 = (1,…,1) satisfies all
strict defining inequalities of K_T; K_T is open, so it contains a ball B(1, ε). Every order cone O_{π'} has 1 in its
closure, hence meets B(1, ε). **K_{T(π)} meets all P! order cones, for every π and every chain-valid choice.**
(More generally: any tree valid on a whole order cone is valid at 1, by closure + genericity.)
Consequence: S2Y's bound q_k ≤ max_π #{π' : K_{T(π')} ∩ O_π ≠ ∅} equals P_N! — useless; Q2 as posed is refuted
for every T, no example needed.

## 3. Correct count: ply = D (PROVED)
Let 𝔉 = {T(π) : π ∈ S_P} as a set, D = |𝔉|. ply(ω) ≤ D trivially, and for ω ∈ ⋂_{T∈𝔉} B_T(1, ε) (nonempty open,
finite intersection) ply(ω) = D. So the order-cone family is a q-fold cover with q = D exactly. Equivalently
D = min #trees whose chain-validity sets Π(T) := {π : T chain-valid for π} cover S_P.

## 4. Bounds on D
- D ≥ 2 (PROVED): D = 1 means one T with O_π ⊆ K_T ∀π, i.e. K_T ⊇ ℝ^P_{>0} — GLAM2-valid, impossible for multi-fibre u_k.
- Necessary condition for π ∈ Π(T) (PROVED, under subset-genericity: no proper nonempty subset of a fibre has μ-sum 0):
  Lemma 1's proof gives f_v(r) = 0 for all r π-before res v, i.e. S_v contains all or none of fibre r. Say v *splits* r
  if S_v ∩ fibre r is proper nonempty. Then Π(T) ⊆ Lin(R_T), R_T = {res v <_π r : v splits r, r ≠ res v}.
  R_T = ∅ ("clumped" trees, each fibre a connected clump) makes every f_u single-fibre, i.e. GLAM2-valid — excluded; so
  R_T ≠ ∅ and |Π(T)| ≤ P!/2, consistent with D ≥ 2. Linear algebra gives nothing stronger: a tree with |R_T| = 1 could
  have |Π(T)| = P!/2, so D = O(1) is not excluded abstractly; a superpoly lower bound must again use supp μ_k / NC (as in S2Q §3).

## 5. Implication for TILE_k
Q2 must be replaced by **Q2′: can ≤ p_k^{O(1)} trees have chain-validity sets covering S_{P_N}?**
Q1 + Q2′ ⇔ (order-cone selection gives TILE_k with q = D). Q2′ is a covering problem over Lin(R_T)-type sets;
S2Z-style search should record Π(T) per found tree (720 checks at P = 6) rather than per-π trees. Near ω = 1 any
order-cone-selection tiling has ply = D, so 1 is the critical point; if D is superpoly the route dies (but TILE_k itself
could still hold with non-chain-valid cones, which need not contain 1).
