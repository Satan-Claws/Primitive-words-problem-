# poly_S2Y: TILE_k by hand — validity cones, order-cone selection, why "width" lower bounds fail (agent S2Y)

Setting: poly_S2P.md §3 (TILE_k), poly_S2X.md, poly_GLAM2.md, poly_LAM.md §1–2. ω ∈ U_{>0} ≅ ℝ^{P_N}_{>0},
f_u := fold(μ_k|_{S_u}) ∈ ℝ^{P_N}, fold(μ_k) = 0 (so every fibre-restriction μ|_r has total 0).
Status: **(a) PROVED (routine); order-cone selection REDUCED to a chain-validity question (OPEN);
(b) "narrow cone ⇒ forced overlap" route INVALID as posed (PROVED); TILE_k remains OPEN.**

## 1. Validity cone (PROVED)
m_i = μ_i ω_{res i} ⇒ n_u(ω) = Σ_{i∈S_u} μ_i ω_{res i} = ⟨f_u, ω⟩. Hence
  K_T ∩ U_{>0} = {ω > 0 : sgn(top u)·⟨f_u, ω⟩ > 0 ∀ non-root u},
an open polyhedral cone in ℝ^{P_N} cut by ≤ |supp μ_k| − 1 forms, each a union of chambers of the finite
arrangement 𝒜 = {f_S : S ⊆ supp μ_k a possible NC subtree vertex set}. Weak/ray form: for a cone
C = cone(r_1..r_m) ⊆ ℝ^{P_N}_{≥0}, C° ⊆ K_T ⇔ sgn(top u)⟨f_u, r_j⟩ ≥ 0 ∀u,j and > 0 for some j (per u).
GLAM2 = the case C = whole orthant (r_j = e_r): impossible for multi-fibre u_k.

## 2. Order-cone selection (REDUCED)
Order cone O_π = {ω_{π1} > … > ω_{πP}} = cone°(1_{A_1},…,1_{A_P}), A_j = {π1..πj}. By §1,
  O_π ⊆ K_T ⇔ T is *chain-valid* for π: every subtree has sgn(top)·μ(S_u ∩ fibres A_j) ≥ 0 ∀j
  (≠0 at j = P is automatic for generic μ, since μ(S_u) ≠ 0).
The masses μ·1_{A_j} are balanced (fibre sums 0), so this is GLAM2's condition weakened from "every single
fibre" to "every initial segment of one chain". The lex-extreme point ω = (1, ε, ε², …) in π-coordinates
always has a valid (greedy, LAM §2(b)) tree; chain-validity on all of O_π is strictly stronger and NOT decided.
If chain-valid T(π) exist ∀π: the family {T(π)} covers U_{>0}, with ply(ω) = #{π' : ω ∈ K_{T(π')}}, and
  q_k ≤ max_π #{π' : K_{T(π')} ∩ O_π ≠ ∅}.
Heuristic support [computational, S2X]: at P_N = 6 the median greedy-cone volume 0.0007–0.002 of the simplex
brackets 1/6! ≈ 0.0014 — greedy cones are order-cone sized. But order cones ⊆ K_T is unverified, and the
overlap count could be up to P_N! (superpoly) unless K_{T(π)} stays within p_k^{O(1)} order cones.

## 3. Lower bound via width: INVALID as posed (PROVED)
Narrowness alone forces no overlap: the order cones themselves have the S2X-observed width and tile U_{>0}
with ply 1 (half-openly, S2P §1(b)). Any lower bound must use *which* cones are available: ply-q TILE_k ⇔
the family {K_T} has a subfamily that q-fold covers ℝ^{P_N}_{>0}; ply 1 ⇔ a subfamily is (half-openly) a
complete fan. An obstruction must show the tree cones admit no such sub-fan, e.g. a point ω* (ω* = 1?) where
every valid K_T has a facet f_u with ⟨f_u, ω*⟩ small but the cones' facets cannot be matched up.

## 4. Sharpened sub-questions
(Q1) For generic multi-fibre μ_k (LAM §2(a)) and every π, is there a chain-valid NC bichromatic tree?
(Q2) If yes, can T(π) be chosen so K_{T(π)} meets ≤ p_k^{O(1)} order cones (e.g. only π' differing by
moves inside the ≤ 2N p_N entries per fibre-cluster)? Q1+Q2 ⇒ TILE_k ⇒ S_N geometrically BLOCKED (S2P §3).
(Q1 is finite-checkable at n = 36: 720 LPs-free sign checks per candidate tree, extend s2x_tile.py.)
