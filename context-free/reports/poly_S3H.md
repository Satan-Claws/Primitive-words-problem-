# poly_S3H: is the genericity-hyperplane count (N) of poly_S2L a real exponential source? — NO (absorbed into θ_S)

Setting: poly_S2L §3 (Lemma S2T′, open term (N)), poly_S2T §2(b)–(d), poly_G3 §1 (Lemmas C, G, K; G3** terms
(1) apex Π_S, (2) μ(Λ_S), (3) θ_S = inradius of C_S := ∩_{σ∈S} A_σ). d := 2r, facet heights ≤ h.

## 1. Full genericity really is exponential (PROVED; S2L's Siegel remark is correct but beside the point)
(a) Line/box count: N hyperplanes are avoided by some ω ∈ {1..N+1}^r (S2T(b)), or on a line ω₀ + t v, t ≤ N.
So cost is LINEAR in N: the "N+1 along a line" observation does not kill the term when N = exp(Ω(r)).
(b) Lower bound (pigeonhole): if ω ∈ {0..T}^r avoids all hyperplanes with normals in {−h..h}^r, then the
(h+1)^r values ν·ω, ν ∈ {0..h}^r, are distinct in [0, rhT], so T ≥ ((h+1)^r − 1)/(rh). Already h = 1
(subset sums) forces T ≥ 2^r/r. Hence any proof that needs ω generic for ALL skeleton boundaries pays
exp(r) whenever exp(r) distinct boundaries occur. (Matching upper bound: ω = (1, B, …, B^{r−1}), B = 2h+1.)
(c) Lex/symbolic perturbation does not escape this by itself: ω_ε = ω + εe_1 + … + ε^d e_d is lex-generic
for free, but realising it integrally (D = Λ^d ω + Λ^{d−1}e_1 + …, Λ > dh) costs (dh)^d — (b) again.

## 2. Genericity is not needed beyond the cones of S (PROVED)
**Lemma H (count-free integral inradius).** Let Q = {x ∈ ℝ^d : ν_j(x) > 0, j = 1..N} ≠ ∅, ν_j ∈ ℤ^d,
‖ν_j‖_∞ ≤ h. Then some x ∈ ℤ^d has ν_j(x) ≥ 1 ∀j and ‖x‖_∞ ≤ d·(√d·h)^d — INDEPENDENT of N.
*Proof.* Q' = {ν_j(x) ≥ 1 ∀j} ≠ ∅ (rescale a point of Q). A minimal face of Q' is an affine space
{ν_j(x) = 1, j ∈ J} (Schrijver Thm 8.4); solve k ≤ d independent rows of it by Cramer with the other
coordinates 0: x = y/Δ, 1 ≤ Δ ≤ (√d h)^d, ‖y‖_∞ ≤ d(√d h)^{d−1} (Hadamard), x ∈ Q'. Then Δx ∈ ℤ^d, ν_j(Δx) ≥ Δ ≥ 1. ∎
Chain {x_1 > 0, x_{i+1} > 2x_i} (h = 2, N = d) needs x_d ≥ 2^{d−1}: the exponential is a HEIGHT/vertex
effect, present with N = d, absent with N = exp but bounded-support normals of a product structure.
**Consequence (reduction).** Fix any ply-set S given qualitatively by poly_P §3 at a real generic ω₀
(existence only; ω₀ never enters a bound). Lemma G needs P ∈ Λ_S ∩ Π_S, i.e. only the facets of A_σ,
σ ∈ S (including the ψ_σ-side): genericity w.r.t. ∂C_τ for τ ∉ S, and the global count N, are irrelevant.
Moreover one may shrink S to |S'| = ⌈(r+1)/2⌉, so at most |S'|·F facets occur (F ≤ d if d_σ = 0, simplicial
A_σ; else pass to a basis, Lemma K) — N_eff = O(r²) — and by Lemma H even this count does not matter.
Applying Lemma H to int C_{S'} ∋ (ω₀,ω₀) + ε(0,δ₀) gives the depth direction D of S2T(c) with
‖D‖ ≤ (√d h)^{O(d)}, and in general exactly the θ_S term: ‖P‖₁ ≤ poly(n)(apex Π_S + μ(Λ_S)/θ_S) of
poly_G3 §1(ii), which contains no ω, no N. **So (N) is not a fourth source; G3** = the three height terms.**
In S2T′, (N) may be deleted from the hypotheses provided (H) is read as "θ_{S} ≥ 1/poly" (which (H)+product
structure gives: C_S splits over classes into cones of dim ≤ 2c, height ≤ g, Lemma H per class ⇒ g^{O(c)}).

## 3. What remains (OPEN) and why pigeonhole over small ω does not help
Choosing ω₀ in a poly box with lex perturbation ω₀ + εω*: S(ω_ε) works, and the needed D is
λ(ω₀,ω₀) + (integral point of the tangent cone of C_S at (ω₀,ω₀)) — the tangent cone is cut only by the
S-facets THROUGH (ω₀,ω₀), and its integral inradius is again a Lemma-H/height quantity. Averaging over the
box bounds the expected number of boundaries through ω₀ by N/T, useless for N = exp; but by Lemma H the
number is irrelevant anyway — only whether those facets form a high-height chain. Hence the residue is
term (3) (and (1),(2)) of G3**, unchanged; no new obstruction from (N).
Status: §1 PROVED, §2 PROVED (N-term eliminated; G3** reduces to apex / μ / θ_S), §3 OPEN = G3**.
