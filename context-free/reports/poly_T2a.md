# poly_T2a: cover-ply geometry on the product region ⊕E_k (agent T2a; geometry only, no length)

Setting (poly_T1 P4): n = P_N², U := ∩_k V_{p_k} (P_N-periodic, dim P_N), E_k ⊆ ∩_{j≠k}V_{p_j}, E_k∩V_{p_k}=0,
d_k = dim E_k = P_N(p_k−1), Z_k := {δ ∈ ⊕E_k : e_k = 0}. f = Σ_σ P_σ(·−c_σ), L_σ = c_σ+ℕV_σ, A_σ = cone V_σ.

## 1. Restriction to the subspace ⊕E_k — WORKS (PROVED), but pieces are coupled cones, not products
Take ω ∈ U∩ℤ^n_{≥1} generic (off the U-relative boundaries of all C_σ := A_σ∩U), P(t,δ) := tω + N!δ,
δ ∈ Λ := ⊕E_k ∩ ℤ^n, |δ|≤R, t ∈ N!ℤ, t ≥ t₀(R). P(t,δ) is primitive ⇔ δ ∉ ∪_k Z_k (ω, e_j∈V_{p_k} for j≠k).
For ω ∉ C_σ: no points (PROOF.md §5 case 1). For ω ∈ C_σ: F_σ := face of A_σ with ω ∈ relint F_σ; then
U ⊆ span F_σ. Let π_σ : ℝ^n → ℝ^n/span F_σ, T_σ := π_σ(A_σ) (pointed, rational), S_σ := span V_σ ∩ ⊕E_k.
M_σ := {δ ∈ Λ : P(t,δ) ∈ L_σ for t large}. Then (same Lat/Deep/λ-arguments as poly_P §3):
 (a) M_σ ⊆ S_σ ∩ π_σ^{-1}(T_σ)  [facet normals ν: ν(N!δ) ≥ ν(c_σ), ν(δ) ∈ (1/D)ℤ, N!/D > |ν(c_σ)|; for λ ⊥ span V_σ:
     λ(c_σ) = N!λ(δ) forces λ(δ) = 0];
 (b) M_σ ⊇ S_σ ∩ π_σ^{-1}(int T_σ) ∩ Λ if M_σ ≠ ∅ (Lat + Deep; near relint F, A_σ = span F_σ + tangent cone);
 (c) on π_σ^{-1}(relint G), G a proper face of T_σ, M_σ is all-or-nothing (layer argument of case 4 with the
     face F_G ⊇ F_σ; N!δ ∈ ℤV_{F_G}); 0 ∉ M_σ (else tω ∈ L_σ ∩ non-primitive).
So M_σ = (finite union of relatively open rational cones) ⊆ S_σ, a cone, M_σ ∩ Z_k = ∅ ∀k. The open part
π_σ^{-1}(int T_σ) = {ν_{σ,j}(δ) > 0 ∀j} is an intersection of half-spaces whose forms ν_{σ,j} = Σ_k ν_{σ,j}|_{E_k}
couple several E_k. Since it avoids Z_k, its projection to E_k is an open convex cone ∌ 0, so
  open part ⊆ ∏_k {ψ_{σ,k} > 0},  and by Farkas ψ_{σ,k} ∈ cone(ν_{σ,j}); ψ_{σ,k} independent ⇒ #facets(T_σ) ≥ N,
  codim F_σ ≥ N.  In particular NO half-space piece (codim-1 face, the only type in PROOF §5) is admissible for N ≥ 2
  ({ψ>0} with ψ|_{E_1} ≠ 0 meets Z_2). Lower-dimensional pieces (S_σ ≠ ⊕E_k) and half-open boundary parts (c)
  are NOT excluded by geometry: a product of lexicographic partitions of each E_k∖0 is a family of convex cones
  avoiding ∪Z_k with ply 1. Only a Lemma-X-type input could exclude them (§3).

## 2. Ply lemma G1 — REFUTED (PROVED): min max-ply is O(N log N · Σ_k d_k), not ≥ c^N ∏ d_k
Problem: 𝓗 family of ∏_k{ψ_{σ,k}>0} (ψ rational) covering ∏_k(ℤ^{d_k}∖0); ply(x) = #{σ : x ∈ piece σ}.
Rational ⇒ uncovered set is a union of rational cells ⇒ covering ℤ-points ⇔ covering ∏(ℝ^{d_k}∖0).
(Irrational forms are genuinely different: {y>αx},{y<αx} cover ℤ²∖0 with ply 1.)
 **Lower bound (PROVED).** N=1: max ply ≥ d (take x₀ ⊥ d−1 independent normals with some ⟨v,x₀⟩>0, perturb
 x = x₀+εy with ⟨v_i,y⟩>0): exact, the simplex cover attains d. Fixing the other factors at generic points:
 min max-ply ≥ max_k d_k. Averaging: ≥ |𝓗|/2^N.
 **Upper bound (PROVED, probabilistic).** Ground set ∏_k S^{d_k−1} (normal tuples, uniform μ); ranges
 R_x = ∏_k{u_k : ⟨u_k,x_k⟩ > 0}, μ(R_x) = 2^{−N} for EVERY x ∈ ∏(ℝ^{d_k}∖0) (also non-generic x).
 VC-dim D = O(Σ_k d_k · log N) (N-fold products of half-space classes). Relative (ε,½)-approximation
 (Li–Long–Srinivasan 2001; Har-Peled–Sharir) with ε = 2^{−N}: a random sample of s = C·2^N·D·N tuples has
 sε/2 ≤ |S ∩ R_x| ≤ 3sε/2 for all x simultaneously. So 𝓗 := S covers everything and
   max ply ≤ C' · N log N · Σ_k d_k,   |𝓗| = O(2^N N log N Σ_k d_k).
 Rationalise: g(x) = max_σ min_k ⟨u_{σ,k},x_k⟩ is continuous and > 0 on the compact ∏S^{d_k−1}, so a rational
 perturbation below min g keeps the cover; ply is controlled by slightly enlarged caps (same VC bound).
 For d_k = P_N(p_k−1): Σ d_k ≤ N p_N P_N = √n · polylog(n), versus ∏ d_k ≥ n^{N/2}.
 ⇒ Convex-cover geometry on ⊕E_k can certify at most ~√n·polylog n ambiguity: the T1 candidate's route via G1
   is BLOCKED; any superpolynomial bound must come from laminarity/realizability, not from the ply lemma.

Table (exact ILP, `scripts/poly/t2a_ply2d.py`; "exact" = optimal over all configurations with ≤ m lines per
factor (any cyclic type of ≤ m lines is realised on the regular 2m-gon of normals); for (2,2), ply 2 would force |𝓗| ≤ 8 ⇒ ≤ 8 lines/factor, covered by m = 8, so 3 is the true minimum):
| d | ∏d_k | min max-ply | min |𝓗| at that ply | method |
|---|---|---|---|---|
| (d) | d | d | d+1 | proof |
| (1,d) | d | d | — | proof (A(+),A(−) disjoint covers) |
| (2,2) | 4 | **3** | 7 | ILP m=8, exact |
| (2,2,2) | 8 | ≤ **5** (≥ 2) | 28 found | ILP m=3,4, time limit hit: feasible, not proved optimal |
| (3,3) | 9 | see registry line | | ILP, 14 normals/factor (upper bd) |
Heuristic (`t2a_random.py`, random test points only, NOT exact): N=4, d=10: random 2400-piece cover, max ply 209
vs ∏d = 10⁴; N=4, d=6: 126 vs 1296 — ply grows like Σd, as the theorem says.

## 3. G2 (Lemma X for classes of size P_N > 2) — FALSE (PROVED), and its strong form would be self-defeating
Lemma 4.2's proof transfers to: span V = ⊕_C span V_C; each non-full component C has λ_C nowhere zero and
Σ_{i∈C∩C_r} λ_i = 0 for every residue class C_r (as 1_{C_r} ∈ span V), so |C ∩ C_r| ≠ 1; codim span V = #non-full C.
Counterexample: V = {e_{1+2jP_N} + e_{1+(2j+1)P_N} : 0 ≤ j < P_N/2} ∪ {e_i : other i}; laminar (disjoint intervals),
U ⊆ span V, cone V simplicial with ω ∈ relint, codim = P_N/2. So faces through ω can have large codimension;
4.1-interleaving gives nothing because classes of size > 2 need not be split across components.
Moreover by §1 every admissible piece has codim F_σ ≥ N, so an analogue "dim F ≥ n−1" would leave no piece
near ω at all; the needed statement is instead a lower bound on ply for laminar-realizable coupled cones (OPEN),
and by §2 it cannot come from convexity alone.

Status: (1) PROVED; (2) REFUTED, with bounds max_k d_k ≤ min max-ply ≤ O(N log N Σ d_k); (3) REFUTED (Lemma X
analogue false). Route "T1 candidate via product ply lemma" BLOCKED at G1.
