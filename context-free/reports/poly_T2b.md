# poly_T2b: effective witness length in the slice argument (gap G3)

Setting as in poly_P.md: G'' CNF of G, V'' its nonterminals; G_m = ((G''×D_{R_m})×D_n) reduced, n = 2m,
M = m−1; amb_G(w) ≤ C|w|^k. Notation: S_i = product-DFA states reachable inside block i; for R_m,
|S_i| ≤ 2 ("just read a", "read ≥1 b"; sink states are useless). Put
  h := 4|V''|,   K₁ := 2^{h−1},   K₂ := h·K₁,   K := 2K₂ = |V''|·2^{4|V''|+2}   (constants of G only).

## 1. Skeleton data of G_m (all PROVED)

**Fact A (annotation classes).** A G_m-nonterminal (p,A,q) whose yield contains exactly the a's
a_i..a_j has p ∈ S_{i−1}, q ∈ S_j; one with yield in b⁺ has p,q ∈ S_s for its block s. So each such
class has ≤ h nonterminals. In a skeleton no root–leaf path repeats a nonterminal (PROOF.md §3(d)).

(a) **Side / b-subtrees.** A maximal subtree of a skeleton (or a side child's unique tree, F3) with yield in
b⁺ lies in one block, so its paths have ≤ h nodes: yield length ≤ K₁ = 2^{4|V''|−1}. Independent of n.

(c) **Ring vectors.** Members of a ring share (s,t), so ring length r ≤ h; one turn hangs r side subtrees:
  ‖v_π‖₁ ≤ hK₁ = K₂ ≤ K.  Also r_σ = ρ_σ + d_σ ≤ n + k (poly_P §2: d_σ ≤ k).

(b) **Offsets.** Let T_a = nodes whose yield contains an a. Its leaves are the n a-leaves; it has ≤ n−1
binary nodes, so its unary nodes form ≤ 2n−1 chains. Along a chain the set of a's is fixed, so by Fact A
a chain has ≤ h nodes; each unary node hangs one b-subtree (≤ K₁ b's); binary nodes and a-leaves hang none:
  ‖c_σ‖₁ ≤ (2n−1)·h·K₁ ≤ nK.

(d) **Number of skeletons.** Distinct skeletons σ with c_σ = c are distinct trees (q = 0) of the word with
exponent c, of length ≤ n(K+1). So
  #Σ_m ≤ C(n(K+1))^k · #{c ∈ ℕ^n : ‖c‖₁ ≤ nK} ≤ C(n(K+1))^k · (e(K+1))^n.
Exponential growth is possible in general (it does not use L = Q): (a(b|bb))^n has 2^n skeletons.

**Lattice data.** For a basis B ⊆ V_σ, I_σ ≤ [sat : ℤB] = gcd of maximal minors ≤ ∏‖v‖₂ ≤ K^n. For laminar
pair vectors a_e e_p + b_e e_q on a forest component, rooting at the deleted column j makes the minor
triangular: minor_j = ∏_e coef(e, child_j(e)); so I = gcd_j ∏_e coef(e, child_j(e)) (cycle components of
the outerplanar support graph: unicyclic dets a∏ ± b∏). **This is still exponential, even cyclic:**
  V = {e_1} ∪ {e_i + 2e_{i+1} : 1 ≤ i ≤ ρ}  ⇒  ℤ^{ρ+1}/ℤV ≅ ℤ/2^ρ  (det 2^ρ; the minor deleting e_1 and column
  ρ+1 is 1), quotient map u ↦ Σ_j (−2)^{ρ+1−j} u_j mod 2^ρ. Laminar (adjacent pairs), entries ≤ 2.
Facet normals likewise: ν ⊥ {e_i + 2e_{i+1}} forces ν ∝ ((−2)^{ρ−i})_i, heights 2^{Θ(n)} (D_σ, γ_σ = ν(c_σ)).
So "laminar ⇒ index/exponent ≤ K^{o(n)}" is FALSE; the answer to (2)'s first question is: index ≤ K^{n}
(product of entries along a rooted spanning forest), and exponential is attained by the quotient exponent.

**Cost of the N! route as written.** N must exceed I_σ, D_σ, γ_σ ≤ K^{O(n)}, and t ≥ N!: |w| = exp(K^{Θ(n)}).
Replacing N! by lcm over all skeletons does not help (#Σ_m exponential, lcm of numbers ≤ K^{O(n)} ~ e^{K^{O(n)}}).

## 2. Effective witnesses (PROVED: singly exponential)

**Lemma S (single coset, PROVED).** Every coset of ℤV_σ in span V_σ ∩ ℤ^n has a representative with
ℓ¹ ≤ ρ_σK ≤ nK (round the coordinates in a basis B: x − Σ⌊λ_v⌋v = Σ{λ_v}v). So the index alone is never
the obstruction for one σ; the problem is simultaneity.

**Theorem E (PROVED).** If L(G) = Q and amb_G is polynomial, then for every m some w ∈ Q∩R_m has
amb(w) ≥ ⌈m/2⌉ and  |w| ≤ n(K+1) + (n+k)K·n(n+k)(n³K)^{n²/2+1} = exp(O(n² log(nK))).
*Proof.* poly_P §3 (qualitative, PROVED) gives a point P ∈ ∩_{σ∈S} L_σ for a set S of s = ⌈m/2⌉ skeletons
(one of P(t,±δ)). Fix σ₀ ∈ S. The integer program in q^σ ∈ ℕ^{r_σ} (σ ∈ S):
  V_σ q^σ − V_{σ₀} q^{σ₀} = c_{σ₀} − c_σ   (σ ∈ S∖σ₀)
is feasible, has ≤ (s−1)·2M ≤ n²/4 rows, ≤ s(n+k) unknowns, entries ≤ nK (by 1(b),(c)). Papadimitriou
(J. ACM 1981): a feasible {Ax=b, x∈ℕ^N} with m rows, |entries| ≤ a has a solution with ‖x‖_∞ ≤ N(ma)^{2m+1}.
Any solution gives P' = c_{σ₀} + V_{σ₀}q^{σ₀} ∈ ∩_S L_σ ⊆ exp(Q∩R_m) (L_σ ∩ Δ = ∅), with s distinct trees
(distinct skeletons). Bound ‖P'‖₁ by 1(b),(c). ∎
General form (for multi-period slices): a point of ply p found qualitatively can be taken with
|w| ≤ (pn²K)^{O(pn)}. So superpoly ply p makes this worse, not better.

## 3. Can poly(n)·K be reached? (OPEN — exact gap)
**Gap G3\*.** Given S ⊆ 𝓗 (full-dim cones A_σ with (ω,ω) ∈ int A_σ, laminar V_σ, ‖v‖₁ ≤ K, ‖c_σ‖₁ ≤ nK)
with ∩_S L_σ ≠ ∅: is there a common point of norm poly(n)·K? Needed: a short point in the intersection of
|S| ≈ m/2 cosets c_σ + ℤV_σ (a coset of Λ_S = ∩ℤV_σ, det ≤ K^{n|S|} = K^{O(n²)}, Minkowski allows covering
radius K^{O(n)}) lying in the fat part of ∩_S A_σ ∩ {ψ_σ(δ) ≥ γ_σ} (facet heights 2^{Θ(n)} possible).
**Abstract obstruction (PROVED, but lower-dimensional, so not in 𝓗-form).** With ρ even,
  L₁ = ℕ{e_1, e_{2i}+2e_{2i+1}},  L₂ = ℕ{e_{2i−1}+2e_{2i}, e_{ρ+1}}  (both laminar, entries ≤ 2):
  L₁ ∩ L₂ = ℕ·(1,2,4,…,2^ρ), so every nonzero common point has norm ≥ 2^ρ. Hence "pairwise-laminar small data
  ⇒ small common point" is false; a poly proof must use the covering property (f ≥ 1 on NE_M, f = 0 on Δ) or
  full-dimensionality, not only the skeleton bounds. For full-rank lattices I found no exponential example.
**Test grammar.** Not found. Note: for grammars of Q∩R_m alone (size free in m) the obstruction is trivially
real (finite unambiguous part for |w| ≤ X, natural ply-(m−1) grammar ∩ {|w| > X}), but that needs X ~ |G''|,
i.e. it is absorbed in K. A real obstruction needs fixed G'' with ply < m/2 on all |w| ≤ poly(m)K: OPEN.

Verdict for the registry: G3 is NOT closed. Witness length ≤ exp(O(n² log nK)) is proved; this is still
fatal for the S_N candidate (needs n^{o(log n / log log n)}).
