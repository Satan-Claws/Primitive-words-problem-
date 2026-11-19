# poly_S3V — base points near a vertex, ω_M = M·e_r + 𝟙: does validity force few-fibre facets? (agent S3V)

Setting: poly_S2Y §1 (K_T ∩ U_{>0} = {ω : sgn(top u)⟨f_u, ω⟩ > 0}), poly_GLAM2 §1, poly_LAM §1–2, poly_S3A (DP).
Targets: μ_k = make_mu-type with ν restricted to a fibre set F, |F| = s (shift operators commute with fibre
restriction, so supp μ_k and the E_k-facet u_k touch exactly F). n = 36, P_N = 6, p ∈ {2,3}.
Status: **lever FAILS pointwise [written proof]; two-vertex validity is impossible for wide facets
[written proof for all of F; computational for pairs]; no ply bound follows (gap below).**

## 1. Results
(a) [written proof] For every u_k and every generic ω (in particular ω_M, any M) a valid NC tree exists:
LAM §2(b) greedy with masses μ_i ω_{res i}. So validity at ONE near-vertex point forces nothing on the facet;
LAM §1 cannot be applied at tω_M+δ. Data: test A feasible 100% for all s, M.
(b) [written proof] Let M₀(μ) := max_{I, r: f_I[r]≠0} |Σ_{q≠r} f_I[q]| / |f_I[r]| (I over intervals of supp μ;
≤ ‖μ‖₁ for integer μ, so poly(n)). For M > M₀, validity at ω_M^{(r)} ⇔ for every subtree:
s_u f_u[r] > 0, or f_u[r] = 0 and s_u Σ f_u > 0. If T is valid at ω_M^{(r)} for ALL r ∈ F, then s_u f_u ≥ 0
coordinatewise and f_u ≠ 0 for every u: T is fold-dominant, so by GLAM2 Lemma |F| = 1.
Hence for multi-fibre u_k no tree's cone K_T contains all |F| near-vertex points ω_M^{(r)}, r ∈ F.
(c) [computational] Pairs: for M ≥ 10 NO tree is valid at ω_M^{(r)} and ω_M^{(r')} (r ≠ r' ∈ F) in every
tested case (k=1,2; s=2..6; 10 seeds; 10–150 pairs each; 0 feasible). At M = 1 some pairs are feasible
(e.g. k=1,s=6: 26/150). So each K_T meets ≤ 1 vertex neighbourhood (conjecture; proved only for s = 2).
(d) [computational] Segment [𝟙, ω_M^{(r)}] (test B) and the M = ∞ two-ray version (weak at e_r, strict at 𝟙):
feasible at low but nonzero rate even for s = 6 (k=1: 4/60, k=2: 1/60; s=2: 6/20, 3/20). Certificates
re-verified by `edge_forms` (strict positivity at 𝟙 and at M = 10‖μ‖₁/min|μ|). E.g. k=1 seed 5 r=0: 175 trees.
**This refutes S3A's OPEN conjecture** ("no NC tree valid on [𝟙, e_r] for any multi-fibre μ_k, any r") —
S3A's seeds were among the (majority) infeasible cases.

| test (M = 1000) | s=1 | s=2 | s=3 | s=4 | s=5 | s=6 |
|---|---|---|---|---|---|---|
| A one point, k=1 / k=2 | all | all | all | all | all | all |
| B [𝟙, ω_M^{(r)}], k=1 | 10/10 | 6/20 | 6/30 | 2/40 | 1/50 | 4/60 |
| B, k=2 | 10/10 | 3/20 | 2/30 | 0/40 | 0/50 | 1/60 |
| C all r ∈ F (both k) | 10/10 | 0/10 | 0/10 | 0/10 | 0/10 | 0/10 |
M = 10, 100, 1000 give identical B/C/E rows (M₀ is small here); M = 1 is more permissive.

## 2. Exact gap
The lever only constrains ω-UNIFORMITY: a wide-facet tree serves ≤ 1 (proved: < |F|) vertex neighbourhoods,
so D_k ≥ 2 (conjecturally ≥ |F| = P_N) distinct trees per wide target. This is a tree-COUNT bound, not an
overlap bound: cones each holding one vertex neighbourhood can still form a fan (ply 1, cf. S2Y §3), and the
greedy pieces at each single ω_M are wide, so the LAM §1 test-point argument (which needs ALL pieces at one
base point to be narrow) never starts. To get ply ≥ (P_N/2s)^N one would need a point where every
covering piece is valid on a neighbourhood of ≥ 2 vertices simultaneously — no such point is forced.
Script: `scripts/poly/s3v_vertex.py` (`python3 s3v_vertex.py 10` ≈10 s; pairs + certificate check:
`python3 -c "import s3v_vertex as v; v.pairwise_and_verify(10)"` ≈10 s).
