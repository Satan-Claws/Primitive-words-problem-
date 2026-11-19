# poly_S3T — TILE_k redone at n = 36 with exact cones K_T (agent S3T) — [computational], INCONCLUSIVE, leaning "ply grows slowly"

Script `scripts/poly/s3t_tile.py` (`python3 s3t_tile.py Ntrain seeds [k]`). Supersedes the sampling side of poly_S2X.md.

## Method
Targets μ_k = `s2x_tile.make_mu` (p=2: |supp|=24; p=3: |supp|=36; seeds 0,1). Training ω: barycentre 𝟙, Dirichlet(1),
Dirichlet(0.3), near-vertex (e_r + ε𝟙, ε∈[1e-3,1e-1]), near-3-face; fresh validation set (4000 ω, same mix, new seed).
Trees: (a) one **exactly uniform** random valid NC tree per training ω (sampler on the S3A interval DP); (b) "max-cone"
trees: grow W from an uncovered ω by nearest neighbours while the DP (σ_W, strict validity at all w∈W) stays feasible.
Each tree's exact cone K_T = {ω>0 : G_T ω > 0} (G_T = edge_forms). ILP (scipy milp/HiGHS): min z with every training ω
covered and ply ≤ z, then min #trees; validated on fresh ω. 0.4–1.3% of ω admit NO strictly valid tree (ties/near-face).

## Data [computational]
| k (p) | seed | N_train | max-cone trees: fresh cover, max ply | ILP: train ply z, #trees | ILP: fresh cover, fresh max ply |
|---|---|---|---|---|---|
| 1 (2) | 0 | 300 | 104: 0.63, 3 | 1, 102 | 0.58, 2 |
| 1 (2) | 1 | 300 | 99: 0.62, 4 | 2, 95 | 0.61, 3 |
| 2 (3) | 0 | 300 | 142: 0.38, 4 | 1, 146 | 0.37, 2 |
| 2 (3) | 1 | 300 | 159: 0.35, 3 | 1, 158 | 0.34, 2 |
| 1 (2) | 0 | 1200 | 215: 0.82, 4 | **2**, 199 | 0.80, 3 |
| 2 (3) | 0 | 1200 | 416: 0.52, 4 | **2**, 402 | 0.51, 3 |
| 1 (2) | 0 | 4000 | 388: 0.93, 6 | **2**, 328 | 0.92, 3 |
Full pools have ply 15–179 (random valid trees overlap heavily). Median single-cone volume ≈ 2·10⁻³ (p=2), 3·10⁻⁴ (p=3).

## Reading
- Ply 1 on training is lost once N ≥ 1200 (forced overlap z = 2 in all three large runs): consistent with "no ply-1
  tiling generically". Achieved fresh max ply is 3 throughout (p = 2 and 3), with #trees ~ N^{0.5} still growing.
- **≥ 99% fresh coverage was NOT reached** (best 92%, p=2, 328 trees; p=3 only 51%), so the requested "minimal max ply
  at ≥99% coverage" is not determined; coverage is limited by tiny cones near faces/vertices, not by ply.
- Weak evidence for TILE_k with small q_k at n=36 (ply 2–3 on what is covered, no growth p=2→3), but the uncovered
  near-boundary region is exactly where forcing could occur (cf. S3V: no tree valid at two vertices for M ≥ 10, so
  near-vertex regions need ≥ |F| distinct cones meeting near 𝟙-segments). TILE_k OPEN. Next: targeted near-vertex/face
  training points, LP-chamber enumeration of uncovered fresh ω, k=2 at N=4000.
