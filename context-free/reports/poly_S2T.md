# poly_S2T: toward ply p at length poly(p) — additive vs multiplicative growth; a c-local ply lemma

Setting: poly_G4 (valid cover of NE_M, data ≤ K, ‖c_σ‖₁ ≤ C₁), poly_G3 §1 (Lemmas C, G, K), poly_P §3
(ω generic off ∂C_σ, C_σ = {u : (u,u) ∈ A_σ}; 𝓗(ω) type-4 set; ψ_σ; |𝓗| ≥ M+1 ⇒ for generic δ₀ one of
S_± := {σ ∈ 𝓗 : ±ψ_σ(δ₀) > 0} has size ≥ ⌈(M+1)/2⌉). Norm ℓ¹ ≈ word length.

## 1. The inductive scheme r → r+2 (Lemma F faces) — BLOCKED (fiber non-propagation)
Let P ∈ F_I have ply q via pieces S. On F_{I'} (I' = I ∪ {a,b}) the point (P, u) with u ≠ 1 on the new
coordinates lies in L_σ (σ ∈ S) only if V_{σ,J'} has generators reaching u while fixing z_J = P. Lemma F
uses the value 1 essentially (z_k = 1 ⇒ q_v = 0 for v ∋ k); for fixed values ≠ 1 the fiber
L_σ ∩ {z_J = P} is a finite union of translates of ℕ(generators touching J'∖J), possibly empty off u = 1.
So old ply does not propagate: the forced set at r+2 (Theorem E at a fresh generic ω on the bigger face)
is unrelated to S, and nothing is "added". If one instead adds pieces to a fixed S, the joint lattice is
Λ_{S∪τ} = Λ_S ∩ ℤV_τ and the covering radius can multiply by exp(ℤ^{2r}/ℤV_τ) ≤ K^{O(r)} per step:
**multiplicative**, total K^{O(r²)} = K^{O(p²)} — Cor F again.
Diagnosis: the only multiplicative sources in Lemma G are (1) facet heights and (2) quotient exponents,
and BOTH are controlled by component size (Lemma T: heights ≤ K^{|C₀|}; exponents ≤ det ≤ K^{|C|}),
not by |S|. Once components are bounded, the |S|-dependence is additive (in fact absent): §2.

## 2. Lemma S2T (c-local covers) — PROVED
Call a valid cover of NE_r **c-local** if for every piece σ the classes of [r] under
  i ~ j  ⇔ some component of the support graph of V_σ meets {x_i,y_i} and {x_j,y_j}
have size ≤ c (so support-graph components have ≤ 2c vertices). Then there is P with
  ply(P) ≥ ⌈(r+1)/2⌉,    ‖P‖₁ ≤ Φ(K,c) · r^{2c+3} · (C₁ + 1),
Φ(K,c) depending only on K, c (Φ ≤ exp(g^{O(1)}), g = (2c)^{c}K^{2c}).
*Proof.* (a) Product structure. Generators lie in single components, so A_σ = ∏_C A_{σ,C},
ℤV_σ = ⊕_C ℤV_{σ,C}, and A_σ ∩ W, hence C_σ = ∏_{classes} C_{σ,class}. Up to relabelling, (V_{σ,C}) ranges
over a finite set depending only on (K,c). Hence: every facet normal of A_σ (types 3/4 are full-dim) is a
primitive integer vector on ≤ 2c coords with entries ≤ g (Cramer/Hadamard); every facet hyperplane of C_σ
(or hyperplane containing a lower-dim C_σ) is supported on one class with height ≤ g; ψ_σ (Lemma T) is
supported on I₀(σ) ⊆ one class, height ≤ g; quotient exponents of ℤ^{2r}/ℤV_σ divide E := lcm(1,…,g);
the (Deep) constant of poly_P §3 per component is ≤ g' = g'(K,c), shift ‖K₀u₀‖₁ ≤ g'·4r²(K+1)³ =: C₂.
(b) Small generic ω, δ₀. All genericity hyperplanes (∂C_σ, ψ_σ = 0) are among
N ≤ r^c(2g+1)^c distinct ones. A hyperplane contains ≤ T^{r−1} points of {1..T}^r, so T := N+1 gives
ω, δ₀ ∈ {1..T}^r generic. Take S := S_+ or S_− (sign absorbed into δ₀), |S| ≥ ⌈(r+1)/2⌉.
(c) Integer depth direction. D := λ(ω,ω) + (0,δ₀), λ := 2cgT + 1. For σ ∈ S, facet ν (W-facet):
ν(D) = ψ_σ(δ₀) ≥ 1; other facets ν': (ω,ω) ∉ ν'^⊥ and integrality give ν'(ω,ω) ≥ 1, so
ν'(D) ≥ λ − 2cgT ≥ 1. ‖D‖₁ ≤ 3λTr.
(d) Lattice for free. Λ_S ⊇ Eℤ^{2r} (all exponents | E, independent of |S|), and c_σ ∈ ℤV_σ (Lemma C;
σ ∈ S contains P(t,δ₀) by poly_P §3 case 4). Put P := tD, t := E·⌈g(C₁+C₂)⌉. Then P − c_σ ∈ ℤV_σ and
ν'(P − c_σ − K₀u₀) ≥ t − g(C₁ + C₂) ≥ 0 for every facet ν' of A_σ, so P − c_σ ∈ ℕV_σ (Deep, per
component), P ∈ L_σ for all σ ∈ S (Lemma G). ‖P‖₁ ≤ t·3λTr ≤ Φ(K,c) r^{2c+3}(C₁+1). ∎
Note: E = lcm(1..g) is where |S|-independence comes from — the lcm of exponents bounded by g is
≤ e^{1.04g} no matter how many pieces; this is the additive mechanism. It is NOT K^{O(1)} in general
(2-dim lattices of index ≤ K² at distinct primes ≤ K² intersect with index e^{Θ(K²)}); K^{O(1)} if the
pieces of S have unimodular or common lattices.

**Corollary S2T (with Lemma F).** If some face F_I, |I| = 2p−1, carries a c-local restricted cover
(restriction only deletes generators, so locality is inherited, and can be *created* by choosing I),
then ply ≥ p at norm ≤ Φ(K,c)·p^{2c+3}(C₁+1) + 2(M−2p+1). In particular, if the interaction graph
(i ~ j iff some generator of some piece touches both pair i and pair j) has max degree Δ, an independent
I of size ⌈M/(Δ+1)⌉ gives c = 1: **ply min(p, ⌈M/(2Δ+2)⌉) at norm Φ(K,1)·p^5·(C₁+1) + 2M** — polynomial.
For R_m (C₁ ≤ 2mK) this is poly(m) length for ply up to ~M/Δ.

## 3. What this buys / exact gap
- Additive iff component (W-class) size on the chosen face is O(1); multiplicative K^{|C|} otherwise
  (Lemma T heights, chain e_i + 2e_{i+1}: exponent 2^{|C|}). Steps with growing components are the only
  exponential source; |S| itself costs nothing.
- **Gap (OPEN):** R_m covers need not be c-local on any face of 2p−1 pairs: a cover may use, on every
  sparse I, long laminar components (nested pairs {x_i, y_j}, chains) — no bound on Δ is known from
  G_m × DFA data. Removing c-locality = controlling, for components of size ~r, facet heights
  K^{|C₀|} and exponents K^{|C|} jointly — exactly G3** (poly_G3 §4) restricted to large components.
- Even unconditionally, ply p at poly(p) on R_{O(p)} gives amb ≥ Ω(|w|) at best (poly_P §3 length remark):
  linear ambiguity only. So S2T is stated for general laminar covers (usable for other slices / poly_GLAM
  covers where per-component locality is natural), not as a resolution.
Status: §1 BLOCKED (multiplicative), §2 Lemma + Corollary PROVED (hypothesis c-local), §3 gap OPEN.
