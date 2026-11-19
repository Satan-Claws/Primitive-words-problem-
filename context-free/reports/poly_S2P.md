# poly_S2P: patching ω-local laminar covers into one slice cover (agent S2P; geometry only)

Setting: poly_GLAM.md §1–3, poly_GLAM2.md, poly_S2W.md, poly_T2a.md §2. Piece σ = (u-tuple, T_1..T_N),
W := U ⊕ ⊕_k E_k, K_T := {x ∈ W : n_v(x) := μ_k(x|_{S_v}) has sign of top(v) ∀v} (cone, apex 0).
Status: **patch REDUCED (PROVED) to a per-component tiling property TILE_k (OPEN); chamber-tiling
argument as posed is INVALID; candidate S_N NOT blocked at the geometric level.**

## 1. What works (PROVED)
(a) Product bound. For a sample S of u-tuples (T2a §2) and families 𝒯_k(u),
  ply(x) = Σ_{u∈S, x_E ∈ ∏{ψ_{u,k}>0}} ∏_k #{T ∈ 𝒯_k(u) : x ∈ K_T^{c}}  ≤  plyVC · ∏_k q_k,
  q_k := sup_{u,x} #{T ∈ 𝒯_k(u) : x ∈ K_T^{c}},  plyVC = O(N log N Σ d_k) = √n·polylog.
  K_T^c := half-open version fixed by the offset c_σ (coordinate of c_σ in the edge basis 0 ⇒ facet closed,
  1 ⇒ open; Lat/Deep as in T2a §1). So ply(ω,δ) ≤ (ply in tree-space) × (VC ply) is TRUE, and by GLAM §3(a)
  q_k ≤ p_k^{O(1)} suffices.
(b) Lex rule does not double count. The lex rule (GLAM §1) is just membership of x = tω+N!δ in K_T^c; a
  wall point ω contributes exactly the trees whose half-open cones contain x. Choosing a generic η and
  closing facet f iff f(η) > 0 makes any family of cones that tile an open region tile it half-openly
  (each x goes to the unique cone containing x+εη): ply exactly 1 on walls, including non-generic ω and
  f(δ)=0 strata. Realizable, since the facets of K_T are edge coordinates, independently set by c_σ.
(c) Finiteness. S is finite, μ_k is fixed per u, trees on supp μ_k are finite ⇒ the forms n_v form a finite
  rational arrangement in W ⇒ finitely many chambers. Every chamber meeting R_k(u) := {x near U_{>0},
  u_k(x_k) > 0} carries a valid tree (LAM §2(b) with masses m_i = μ_i x_i, Σ m_i = u_k(x_k) > 0).
  So coverage of all ω ∈ U_{≥0}∖0, all lex directions, holds (with the full tree family: huge ply).

## 2. The gap (PROVED that it is a gap)
A chamber tiling with "ply 1 in ω" is NOT available: a piece's region is K_T (the simplicial cone on V_σ,
facets = T's own forms only), not the chamber C ⊆ K_T it was picked for. L_σ = c_σ + ℕV_σ admits no extra
facets, so pieces cannot be shrunk to chambers (GLAM §2). Picking T_C per chamber gives
  q_k(x) = #{C : x ∈ K_{T_C}},  up to #chambers incident/contained — not 1, not obviously poly.
ω-uniform choices are excluded (GLAM2: ≥ (P_N/2)^N), so the trees must vary and overlap is the issue.

## 3. Exact remaining obstruction
(TILE_k) For each k and each u_k in (a T2a-sufficient random family of) E_k*, is there an admissible μ_k and a
family 𝒯 of non-crossing bichromatic trees on supp μ_k whose cones K_T cover R_k(u) with ply ≤ p_k^{O(1)}?
(Equivalently GLAM §3(b) with ρ_k ≤ poly.) YES ⇒ by §1 a poly-ply slice cover exists ⇒ S_N BLOCKED
geometrically (modulo realizability by a grammar). NO for every μ_k ⇒ superpolynomial ply, S_N survives here.
Not decided: a canonical tree map x ↦ T(x) tiles only if T(x)=T ⇔ x ∈ K_T, i.e. validity cones disjoint;
no such rule known (greedy LAM §2(b) cones overlap).
