# poly_S3A — EXACT decision of S2Y Q1 at n = 36 (P_N = 6, p ∈ {2,3}) by interval DP over all NC trees (agent S3A)

Status: **[computational] Q1 = NO at n = 36 for every tested μ_k and EVERY order π (exhaustive, not sampled).
No chain-valid NC bichromatic tree exists: 0/720 orders for each of 20 targets (p=2, p=3; seeds 0–9). Q2 moot.**
Supersedes poly_S2Z.md (which was node-limited and restricted to LAM §2(b) merge sequences).

## Method (exact)
Targets μ_k = `s2x_tile.make_mu(k, seed)` (fixed supp, |supp| = 24 for p=2, 36 for p=3; all 6 fibres used),
vertices = supp μ_k in Z_n cyclic order, edges between opposite signs, non-crossing as chords of the circle.
- Structural fact (PROVED, standard): deleting an edge of a NC spanning tree on points of a circle leaves two cyclic
  arcs. Rooted at v0 = first support point, every subtree is a linear interval [l..r] of supp∖{v0}, and the child
  subtrees of c are consecutive intervals on each side of c; conversely every such recursive decomposition is a NC tree.
- Chain-validity of edge (parent, c) depends only on the interval I = subtree(c): σ(I) = s iff
  s·Σ_{t≤j} f_I[π_t] ≥ 0 ∀j and s·μ(I) > 0 (root-independent since fold μ = 0); need sign(c) = σ(I).
- DP: Sub(l,r) = ∃c∈[l..r], sign c = σ([l..r]), Part(l,c−1,−sign c)·Part(c+1,r,−sign c);
  Part(l,r,t) = concatenation of intervals J with Sub(J), σ(J)=t. Tree exists ⇔ Part(1,m−1,−sign v0). O(m³) per π.
  S2Q π-monotonicity is implied by validity, so it is enforced exactly (no heuristic pruning needed).
- Checks: unconstrained counts 1,3,12,55,273,1428 (= NC spanning trees on m convex points ✓); DP = brute-force
  enumeration on 30 random constrained 7-point instances (0 mismatches); any found tree is re-verified by
  `edge_forms` + `chain_valid`. Positive control: with σ from a single random ω (pointwise validity) the same DP finds
  4 – 1.4·10⁷ trees per target, so the empty result is not an artefact.

## Data
| targets | orders π tested | π with a chain-valid tree | certificate |
|---|---|---|---|
| p=2, seeds 0–9 | all 720 each | 0 | exhaustive DP infeasibility |
| p=3, seeds 0–9 | all 720 each | 0 | exhaustive DP infeasibility |
Sharper (seeds 0,1): imposing only the prefixes j = 1 and j = P (i.e. weak validity at the two rays e_{π1} and 𝟙 of
cl O_π) is already infeasible for all 720 π; the pair j ∈ {P−1, P} is infeasible for 23/24 sampled π; j = P alone
(ω = 𝟙) is feasible. So the obstruction is: **no NC tree valid at ω = 𝟙 has every subtree's fibre-r mass of the
subtree's sign, for any single fibre r** — a two-ray (𝟙, e_r) incompatibility, i.e. O_π ⊄ K_T already fails on the
edge [𝟙, e_{π1}] of the order cone.

## Reading
Order-cone selection (S2Y §2: one tree per order cone) is DEAD at n = 36 for actual admissible μ_k [computational].
TILE_k is not refuted: covering U_{>0} may need trees whose cones cut across order cones. Conjecture (OPEN): for all
multi-fibre μ_k and every fibre r, no NC tree is valid on the segment [𝟙, e_r] — a GLAM2-type statement on two rays.
Script: `scripts/poly/s3a_ncdp.py` (`python3 s3a_ncdp.py [seeds=2]`, ≈10 s; 10 seeds ≈1 min).
