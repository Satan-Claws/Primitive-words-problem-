# poly_LAM: does laminarity kill the T2a low-ply cover? (agent LAM; geometry only)

Setting as poly_T2a: n = P_N², s_j := n/p_j, U = P_N-periodic, E_k ⊆ period-(P_N p_k) vectors with zero
fibre sums (fibre = residue class mod P_N), ω ∈ U ∩ ℤ^n_{≥1} generic, T = cyclic shift. Laminar pieces:
L_σ = c_σ + ℕV_σ, V_σ independent, pair supports non-crossing (PROOF.md §3(f)); near ω the piece is
{n_v(δ) > 0 : v ∈ V'}, V' = V_σ ∖ V_F, ω ∈ relint cone V_F, U ⊆ span V_F (Lemma-X-type face condition).

## 1. Narrow facets force superpolynomial ply (PROVED)
Product pieces O_σ = ∏_k{ψ_{σ,k} > 0}, ψ_{σ,k} ∈ E_k* nonzero on at most s fibres mod P_N.
Test points: x_k supported on one fibre r_k (such x_k ∈ E_k, any nonzero sign pattern with zero sum).
A piece can contain one only if ψ_{σ,k} touches fibre r_k for all k, so covering all (r_1..r_N) needs
|𝓗| ≥ (P_N/s)^N. With x_k independent symmetric continuous on E_k, Pr[x ∈ O_σ] = 2^{−N} for every σ, so
  max ply ≥ E[ply] = |𝓗|/2^N ≥ (P_N/(2s))^N = n^{N/2}/(2s)^N.
Pair facets x_a > x_{a+s_k} (the "natural conjunctive grammar", s = 1) give ply ≥ (P_N/2)^N = n^{ω(1)}.
So a low-ply cover needs facets touching P_N^{1−o(1)} fibres: wide tree potentials (Lemma T, poly_G4 §3).

## 2. Wide facets with arbitrary E_k-part are laminarly realizable, with the face condition (PROVED)
(a) Target. Given u_k ∈ E_k* (e.g. T2a's random normals), put
  μ_k := (1 − T^{s_k}) ∏_{j≠k}(1 − T^{P_N p_j}) ν_k.
Then μ_k ⊥ U, μ_k ⊥ E_j (j≠k), μ_k ⊥ V_{p_k} (the factors kill period-P_N p_j and period-s_k vectors), and
each factor acts invertibly on E_k (eigenvalues 1 − e^{2πi p_j f/p_k}, 1 − e^{2πi f(P_N/p_k)/p_k}, f ≢ 0 mod p_k),
so ν_k (support in a window of length P_N p_k) can be chosen with ⟨μ_k,·⟩|_{E_k} = u_k. Generic ⇒ no zero
entries on supp μ_k: two clusters A_k, A_k+s_k, each of width ≤ P_N·Σ_j p_j ≤ 2N p_N P_N ≪ P_N.
(b) Tree. For masses m_i = μ_i ω_i (Σ m_i = 0, both signs, generic) there is a non-crossing tree on supp μ_k,
bichromatic w.r.t. sign μ, in which every proper subtree has total mass of the sign of its top vertex.
Proof: repeatedly take two consecutive current vertices x,y of opposite sign with |m_x| < |m_y|, hang x
under y, give y mass m_x+m_y (same sign, ≠ 0); total stays 0, so both signs persist; last two vertices =
root + child. Invariant "no arc of a subtree passes strictly over its top" makes each new arc {x,y}
crossing-free and is preserved. Edge vectors a e_p + b e_q with a/b = |μ_q|/|μ_p| make the coordinate
functional of the root edge v_k = {t_k, o_k} (o_k a looped outside vertex) a positive multiple of ±μ_k;
every internal edge coordinate at ω is the subtree mass / |μ_top| > 0; loops > 0 at ω. Hence
ω ∈ relint cone V_F, span V_F = ∩_k μ_k^⊥ ⊇ U.
(c) Assembly. Components for k = 1..N nested Russian-doll style: component k+1 inside an empty gap of
component k (between A_k and A_k+s_k; s_{k+1} < s_k), all other vertices loops. Non-interleaving holds,
V_σ is a laminar basis, V' = {v_1..v_N}, and near ω the piece is exactly ∏_k{⟨u_k, e_k⟩ > 0}.
Globally L_σ ⊆ {μ_k ≥ γ_k > 0 ∀k} (choose c_σ), and μ_k ≡ 0 on V_{p_k}, so L_σ ∩ ∪_p V_p = ∅: every piece is
a valid laminar linear set inside the primitive set.
⇒ At any FIXED generic ω, the T2a cover (ply O(N log N Σ d_k) = √n·polylog n) is realized by laminar
pieces satisfying the Lemma-X face condition. Laminarity + face condition do NOT force n^{ω(1)} locally.

## 3. Status and exact residue
Local laminar obstruction route: BLOCKED (§2, a construction of type (i), local version).
Not done: one grammar good at ALL points. The internal-edge conditions n_u ≥ 0 depend on ω (merge order
in 2(b) changes across an arrangement in U), and non-generic ω / lower strata / off-⊕E points are untreated.
Exact sub-question (G-LAM): cover U_{>0} by open cones Ω_1..Ω_r of overlap poly(n) such that a single tree
per (σ, Ω_i) satisfies 2(b) on all of Ω_i, and extend to non-generic base points with poly ply.
If G-LAM holds, S_N has a poly(n)-ply laminar cover (candidate dead independently of G3**); if it fails,
the failure must come from ω-uniformity, not from laminarity at a generic point.
