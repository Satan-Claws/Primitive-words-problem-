# poly_G3: gap G3* on R_m — reduction, the two proposed mechanisms, exact residue

Setting and notation as in poly_P.md §3 and poly_T2b.md (G_m, n = 2m, M = m−1, K, L_σ = c_σ + ℕV_σ,
A_σ = cone V_σ, type-4 set 𝓗 = 𝓗(ω), ψ_σ, γ_σ, W = diagonal, π(x,y) := y − x). Target: some w ∈ Q∩R_m with
amb(w) ≥ ⌈m/2⌉ and |w| ≤ poly(m)·K.

## 1. Reduction lemmas (PROVED)

**Lemma C (the coset is a lattice).** If σ is of type 2, 3 or 4 and L_σ contains some P(t,δ), then
span V_σ = ℝ^{2M} or λ_σ^⊥, and c_σ ∈ ℤV_σ. *Proof.* P(t,δ) ∈ N!ℤ^{2M}; in types 3/4 span V_σ = ℝ^{2M},
so N!ℤ^{2M} ⊆ I_σℤ^{2M} ⊆ ℤV_σ, hence c_σ = P(t,δ) − (P(t,δ) − c_σ) ∈ ℤV_σ. (Type 2: same inside λ^⊥,
using ⟨λ,c_σ⟩ = 0 from PROOF.md §5 case 2.) ∎
So in G3* the joint coset ∩_S(c_σ + ℤV_σ) is the **lattice** Λ_S := ∩_{σ∈S} ℤV_σ (it contains 0).

**Lemma K (where Deep's K₀ enters).** If V_σ is linearly independent (d_σ = 0), ℤV_σ ∩ cone V_σ = ℕV_σ,
i.e. K₀ = 0. For d_σ > 0, K₀ is needed only to pass from ℤV_σ ∩ cone to ℕV_σ; replacing V_σ by a basis
B ⊆ V_σ trades it for the index [ℤV_σ : ℤB] (≤ K^{2M}, Hadamard). Either way K₀ is a *lattice* effect, not a
depth effect along ω. (Proof: coordinates in a basis are integral on ℤB and ≥ 0 on cone B.) ∎

**Lemma G (effective ply criterion).** Let S ⊆ 𝓗 (all d_σ = 0 for simplicity; else add K₀u₀ to c_σ) and
  Π_S := ∩_{σ∈S} (c_σ + A_σ)   (a polyhedron; v*-facet condition = ψ_σ-side condition is included).
Every P ∈ Λ_S ∩ Π_S has amb(P) ≥ |S|, and P ∈ NE_M automatically (L_σ ∩ Δ = ∅).
*Proof.* P − c_σ ∈ ℤV_σ (Lemma C) with all basis coordinates ≥ 0, so P ∈ L_σ for each σ ∈ S. ∎
Qualitatively (poly_P §3) some S with |S| ≥ ⌈m/2⌉ and Λ_S ∩ Π_S ≠ ∅ exists: S = {σ ∈ 𝓗(ω₀) : ψ_σ(δ₀) > 0}.
**Consequences.** (i) ω, its genericity and its size do not enter the effective problem: they only certify
that S exists. Only the cones of S (those with (ω₀,ω₀) on their W-facet) matter. (ii) Since the recession
cone C_S := ∩_S A_σ contains (ω₀,ω₀) + ε(0,δ₀) in its interior, a lattice point exists at
  ‖P‖₁ ≤ poly(n)·( ‖apex Π_S‖ + μ(Λ_S)/θ_S ),
μ = covering radius, θ_S = inradius of C_S ∩ {‖·‖₂ = 1}. Bounds from skeleton data: apex ≤ K^{O(n)}
(Cramer on facets of A_σ), μ(Λ_S) ≤ 2M·lcm_S(exp ℤ^{2M}/ℤV_σ) ≤ 2M·K^{n|S|}, θ_S ≥ K^{−O(n)}: this
re-proves Theorem E (exp(O(n² log nK))) geometrically and **separates G3* into three numbers**.

## 2. Mechanism (a), density/averaging — BLOCKED (reduces to Lemma G)
Fix Λ' := ∩ ℤV_σ over the pieces that meet a deep neighbourhood of the ray ℝ₊(ω₀,ω₀). The §5 argument run on
a residue class r + Λ' needs a diagonal point in that class (it is the Δ-contradiction that kills types 2/3 and
fixes γ_σ > 0). Hence **forced ply ≥ ⌈m/2⌉ exists only on classes r ∈ W_ℤ + Λ'**, of density
1/[ℤ^M : π(Λ')]; on the other classes nothing beyond f ≥ 1 is derived. So a box average gives
avg_B f ≥ 1 + (⌈m/2⌉−1)/[ℤ^M : π(Λ')] − o(1), never better than exhibiting one point of the forced class,
which is exactly Lemma G with the numbers μ, θ_S. Per-coset averaging adds nothing new: within the class,
f is the exact count #{σ ∈ S : n_{v*}(P) ≥ γ_σ} only in the deep region, so depth (apex/θ_S) is still needed.
Depth enters via apex Π_S (facet heights γ_σ and n_v(c_σ), up to K^{O(n)}), not via ω.

## 3. Mechanism (b), slice congruences — BLOCKED
**Lemma B (PROVED).** Let D_L be a DFA counting b's mod L in each block, slice R_m^L ⊆ R_m (x_i, y_i ≡ fixed
residues). If every ring of G'' is a simple cycle (one cycle through each ring nonterminal), the rings of
G''×D_L are the iterates q_π v_π, q_π = L/gcd(L, gcd v_π); in normalised coordinates on Lℤ^{2M} the lists,
indices I_σ, quotient exponents, facet normals and γ_σ are **unchanged** (index is scale-invariant:
[Lℤ^n ∩ span : LℤV] = [ℤ^n ∩ span : ℤV]). E.g. the chain V = {e_1, e_i + 2e_{i+1}} keeps ℤ/2^ρ.
(Proof: a product cycle projects to a G''-cycle at the same nonterminal, which is the unique simple one,
iterated until the mod-L state closes.) For grammars with composite rings the index can drop, but only to
I_σ / |(ℤ^n/ℤV_σ) ⊗ ℤ/L|, so killing a 2-part 2^ρ needs 2^ρ | L, i.e. L = 2^{Θ(n)} — and the product
constant becomes K' = |V''|·2^{O(|V''|L²)} (class size h' = |V''|(L+1)²), doubly exponential.
Block-dependent moduli L_i (e.g. L_i = 2^i normalises e_i + 2e_{i+1} to e_i + e_{i+1}) cannot normalise
both orientations e_i + 2e_{i+1}, 2e_i + e_{i+1} at the same pair, and again need L_i = 2^{Θ(n)}.
Since the skeleton data must be handled for arbitrary G, slice freedom gives no poly(n)·K bound.

## 4. Exact residual gap (OPEN) and obstruction status
**G3\*\*.** For some ply-set S (|S| ≥ ⌈m/2⌉) bound simultaneously (1) apex of Π_S = ∩(c_σ + A_σ),
(2) covering radius μ(Λ_S) of the homogeneous joint lattice, (3) inradius θ_S of ∩_S A_σ, by poly(n)·K.
Each of (1)–(3) is individually K^{Θ(n)} for single laminar pieces (chain examples, poly_T2b §1), but in
every such example the bad piece is not of type 4 in a Δ-avoiding NE_M-cover; I found no valid
(Δ-avoiding, NE_M-covering, data ≤ K) family where (1), (2) or (3) is forced super-poly for all ply-sets.
The full-rank analogue of T2b's L₁ ∩ L₂ = ℕ(1,2,…,2^ρ) is not known: each ℤV_σ has a basis of norm ≤ K,
but det Λ_S ≤ K^{n|S|} only gives λ₁(Λ_S) ≤ √(2M)·K^{O(|S|)}, still exponential for |S| ≈ m/2.
No explicit obstruction configuration (the requested "ply ≥ 2 only at norm 2^{Ω(m)}") was found: OPEN.
Verdict: G3* NOT closed; sharpened to G3** (three explicit geometric numbers; ω, genericity and K₀ removed).
