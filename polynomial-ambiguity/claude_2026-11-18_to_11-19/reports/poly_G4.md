# poly_G4: can high-ply R_m points be forced far away? (cover-level question behind G3**)

Setting: poly_P §2–3, poly_T2b, poly_G3. A *valid cover* of NE_M (M = m−1) is a finite family
L_σ = c_σ + ℕV_σ ⊆ ℕ_{≥1}^{2M}, pair/singleton supports non-crossing in x_1<…<x_M<y_1<…<y_M,
‖v‖₁ ≤ K, ‖c_σ‖₁ ≤ nK, r_σ ≤ n+k, L_σ ∩ Δ = ∅, ∪L_σ = NE_M; f = Σ_σ P_σ(·−c_σ); ply(P) := f(P).
K is a constant of G (poly_T2b: K = |V''|2^{4|V''|+2}); only m → ∞ is asymptotic.

## 1. Small cases
- m = 2 (M = 1): ⌈m/2⌉ = 1, trivial. A ply-1 *partition* exists: (1,2)+ℕ{e_y, e_x+e_y} ∪ (2,1)+ℕ{e_x, e_x+e_y}.
- m = 3 (M = 2): ⌈m/2⌉ = 2. Every valid cover has a ply-2 point of norm ≤ B(2,K) := Theorem E bound at
  n = 6, i.e. K^{O(1)} (poly_T2b §2; its proof uses only cover data + qualitative §5).
  For fixed m every bound is K^{O_m(1)}, so exhaustive small-m search cannot separate (A)/(B):
  the question is purely the m-dependence of the exponent.

## 2. Lemma F (face restriction) — PROVED
Let I ⊆ [M], |I| = r, J = {x_i, y_i : i ∈ I}, and F_I := {z ∈ ℕ_{≥1}^{2M} : z_k = 1 for k ∉ J}. Then
  L_σ ∩ F_I = (c_σ + ℕV_{σ,J})  if c_{σ,k} = 1 for all k ∉ J,  and ∅ otherwise,
where V_{σ,J} = {v ∈ V_σ : supp v ⊆ J}; multiplicities agree (P_σ restricted = P_{V_{σ,J}}).
*Proof.* c_σ ∈ L_σ ⊆ ℕ_{≥1}^{2M} so c_{σ,k} ≥ 1; z_k = 1 forces c_{σ,k} = 1 and q_v = 0 whenever v_k > 0. ∎
Hence {L_σ ∩ F_I} (coordinates J deleted) is a valid cover of NE_r with the same K: laminar for the
induced order x_{i_1}<…<x_{i_r}<y_{i_1}<…<y_{i_r}, Δ_r-avoiding (diag on J + ones = diag), covering
(x_J ≠ y_J extended by ones lies in NE_M). Realizability: F_I is the spaced slice with fixed blocks b¹
(poly_R3a Lemma I), i.e. the sub-cover is the data of G_m × DFA — no new constraint.

**Corollary F (B for bounded ply) — PROVED.** Every valid cover of NE_M has, for each p with 2p−1 ≤ M,
a point of ply ≥ p and ℓ¹-norm ≤ B(2p−1, K) + 2(M−2p+1), B(r,K) = exp(O(r² log rK)) (Thm E at M = r).
In particular **ply ≥ 2 at norm ≤ 2m + K^{O(1)}**, and ply ≥ c·√(log m / log log m) at norm poly(m)
(K fixed). So alternative (A) is FALSE for ply ≥ 2 (any constant ply); it can only hold at thresholds
p ≫ √(log m).

## 3. Lemma T (shape of type-4 facets) — PROVED
For σ of type 4 at ω (poly_P §3), F the facet with (ω,ω) ∈ relint F, normal ν: by Lemma X (PROOF.md 4.2)
on V_F, span V_F = ν^⊥ has exactly one non-full component C₀ of the support graph, C₀ = ∪_{i∈I₀}{x_i,y_i},
and ν is supported on C₀ (full components force ν = 0 there). Each edge a e_p + b e_q of C₀ gives
ν_q = −(a/b)ν_p, so ν is a multiplicative alternating potential on a non-crossing spanning tree of C₀
with |ν_{x_i}| = |ν_{y_i}|, and
  ψ_σ(δ) = Σ_{i ∈ I₀} ν_{y_i} δ_i,   supp ψ_σ = I₀(σ).
Facet heights γ_σ and ‖ν‖ are ≤ K^{|C₀|} (ratios a/b ≤ K along tree paths); the poly_T2b chain is the
case of a path C₀ with ratios 2.

## 4. What remains (OPEN) at the threshold ⌈m/2⌉
(B) at ply ⌈m/2⌉: Lemma F gives nothing (restriction to r pairs only forces ⌈(r+1)/2⌉). Lattice side:
Λ_S ⊇ lcm_S(exp ℤ^{2M}/ℤV_σ)·ℤ^{2M}, and Minkowski gives λ₁(Λ_S) ≤ √(2M)·(∏_S I_σ)^{1/2M} ≤ √(2M)·K^{|S|}
= K^{O(m)} — so the lattice *can* in principle force 2^{Ω(m)}; poly needs structure of S-joint lattices.
(A) at ply ⌈m/2⌉: not constructed. A construction must (i) keep ply ≤ O(√log m) up to norm 2^{o(m)}
on every face F_I (Cor. F is tight only if this is possible), (ii) use type-4 pieces whose C₀-potentials
(Lemma T) have ratio products 2^{Θ(m)} on ≥ ⌈m/2⌉ pieces sharing a ψ-sign pattern, (iii) still cover the
complementary lattice classes near the diagonal (poly_G3 §2) with Δ-avoiding laminar pieces. I found no
family satisfying (iii): the natural "parity / φ mod 2^ρ" certificates need generators ≥ 2^ρ e_M
(the ray t·e_M + r in a fixed class is only reachable by v ∈ ℕe_M, and φ(c e_M) = c ≡ 0 needs c ≥ 2^ρ),
violating K = O(1).
Verdict: (B) PROVED for constant ply (ply 2: 2m + K^{O(1)}); threshold ⌈m/2⌉ OPEN in both directions;
no evidence that the R_m witness-length route needs Q-external input, but none that it doesn't.
