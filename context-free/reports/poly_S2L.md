# poly_S2L: can c-locality be forced on R_m covers by the Lemma-F face? — NO; and Lemma X does not force r−1 pairs either

Setting: poly_S2T §2 (Lemma S2T, c-local: classes i~j ⇔ a support-graph component of V_σ meets pairs i and j),
poly_G4 §2 (Lemma F), §3 (Lemma T), PROOF.md §4 (Lemma X 4.2 + audit G1: at most ONE component of any
W-spanning laminar family contains a pair {x_i,y_i}, full or not).

## 1. What Lemma X actually forces (PROVED)
For a type-4 piece σ on a face of r pairs, facet F, V_F: pair i is *internal* if x_i, y_i lie in one
component of V_F. Lemma X: all internal pairs lie in one component, and it is C₀ (a non-full component is a
union of pairs, so it contains an internal pair; only one component can). Every non-internal pair has x_i, y_i
in two different FULL components (e_{x_i} ∈ span V_F). Nothing forces |I₀| large:
**Example.** σ = {x_1 > y_1, others free}: V = {e_{x1}, e_{x1}+e_{y1}, e_{x_k}, e_{y_k} (k≥2)}, c = 1+e_{x1}.
Facet ν = e_{x1} − e_{y1}, V_F = {e_{x1}+e_{y1}, loops}, C₀ = {x_1,y_1}: **|I₀| = 1**. So alternative (ii)
("C₀ ⊇ r−1 pairs") is FALSE; type-4 pieces of the §6 grammar "∃i x_i≠y_i" are 1-local.

## 2. Locality is NOT forceable by choosing the face (PROVED, abstract covers; realizability sketched)
**Star cover.** σ_i^>: c = 1+e_{x_i}, V = {e_{x_i}, e_{x_i}+e_{y_j} (all j), e_{x_k} (k≠i), e_{y_k} (k≠i)}.
Edges x_i–y_j share the endpoint x_i, so the family is laminar; L(σ_i^>) = {x_i > y_i} exactly
(x_i − y_i = 1 + a + Σ_{j≠i} s_j covers all positive values; others free). Mirror σ_i^< with star at y_i to all
x_j (also non-crossing). {σ_i^>, σ_i^<}_i is a valid cover of NE_M, K = 2. On any face F_I, σ_i^{≷} survives iff
i ∈ I (c_{x_i} = 2), and its restricted star component meets every pair of I: class size r. Every piece of
every restricted cover is r-local only, and no c-local subcover exists (all pieces are of this form).
Hence (i) fails: no face choice, random or clever, yields c-locality. (The union-bound route fails for the
same reason: hubs survive with probability r/M per piece, and the M hub positions are all occupied.)
Realizability in G_m × DFA: nested rings pumping (x_i-block, y_j-block) for j = M, M−1, …, 1 inside one
skeleton — laminar, ‖v‖ ≤ 2; SKETCH, not needed for the conclusion below.

## 3. Moral: c-locality is the wrong hypothesis; what S2T really uses
The star cover has ply-⌈(r+1)/2⌉ points at norm O(r) (all heights 1, unimodular). S2T's proof uses locality
only to bound: (H) facet heights of A_σ / C_σ and ψ_σ by g; (E) quotient exponents by g; (D) per-component
(Deep) constants by g'; (N) the number of DISTINCT genericity hyperplanes (∂C_σ, ψ_σ = 0) by poly(r).
**Adapted Lemma S2T′ (PROVED, same proof as poly_S2T §2(b)–(d)):** if a valid cover of NE_r satisfies
(H),(E),(D) with constants g, g' and (N) with N distinct hyperplanes, then ply ≥ ⌈(r+1)/2⌉ at norm
≤ poly(g, g', N, r)·(C₁+1). One big component per piece is fine if (H),(E),(D),(N) hold.
**Exact gap (OPEN).** For large components (H),(E),(D) can be K^{|C|} (chain e_i+2e_{i+1}, Lemma T), and (N):
without one-class support, hyperplanes range over ≤ (2g+1)^{2r} normals; if exp(Ω(r)) of them occur (possible
with exp(O(n)) pieces), Siegel's lemma forces ‖ω‖ ≥ g^{Ω(r)}, i.e. exponential — a fourth exponential source
not visible in poly_S2T §3. So the gap is G3** for large components plus the genericity count (N).
Status: §1 PROVED (ii refuted), §2 PROVED (i refuted; realizability SKETCH), §3 S2T′ PROVED, gap OPEN.
