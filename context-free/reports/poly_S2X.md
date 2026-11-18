# poly_S2X: TILE_k probed at n = 36 (agent S2X) — [computational], INCONCLUSIVE (undersampled)

Setting: poly_S2P.md §3 (TILE_k), poly_GLAM.md §1, poly_GLAM2.md, poly_LAM.md §2. Script
`scripts/poly/s2x_tile.py` (raw output reproduced below; `python3 s2x_tile.py 2 1500`, ~5 min).

## Set-up (PROVED-routine reductions used by the script)
n = 36, P_N = 6, p ∈ {2,3}. μ_k = (1−T^{s_k})∏_{j≠k}(1−T^{P p_j})ν_k, ν_k Gaussian on a window of length P p_k
(so u_k is generic, multi-fibre: |supp μ| = 24 (k=1, 4 per fibre), 36 (k=2, 6 per fibre)).
Validity of a bichromatic NC tree is root-independent (μ ⊥ U: rerooting flips side and sign together), so
K_T ∩ (U_{>0} slice) = {ω ∈ ℝ^6_{>0} : g_e(ω) > 0 ∀ edges e}, g_e = sign(μ_a)·fold(μ|_{A_e}). The root/lex
condition is u_k(δ) > 0 (automatic on R_k(u)); for generic ω no g_e(ω) = 0 ties, so lex directions play no
role on the sampled set (non-generic ω untested).
Family: NOT all NC trees (≈ (27/4)^24 ≈ 10^19, infeasible); LAM §2(b) greedy trees at sampled ω (1 canonical + 3
random merge orders each). Cover: min max-ply subfamily covering the sample (ILP, HiGHS), LP lower bound,
greedy set cover; then holdout check on 5000 fresh ω. (Half the ω uniform on the simplex, half Dirichlet(0.3).)

## Data [computational]
| k (p) | seed | trees in family | sampled chambers / forms | full-family ply | greedy cover: #, ply | ILP min ply (#trees) | holdout: ILP cover covers, ply / family covers, ply |
|---|---|---|---|---|---|---|---|
| 1 (2) | 0 | 5018 | 1127 / 245 | 66 | 360, 5 | **1** (370) | 0.78, 3 / 0.94, 66 |
| 1 (2) | 1 | 4791 | 1156 / 242 | 63 | 367, 4 | **1** (385) | 0.76, 2 / 0.93, 63 |
| 2 (3) | 0 | 5779 | 1476 / 1075 | 33 | 1043, 3 | **1** (1047) | 0.24, 3 / 0.47, 33 |
| 2 (3) | 1 | 5730 | 1484 / 997 | 23–25 | 951, 3 | **1** (950) | 0.29, 2 / 0.55, 25 |
Median per-tree validity fraction 0.0007–0.002 of the simplex (each greedy cone is tiny).

## Reading
(a) On every finite sample the ILP reaches ply 1 (LP bound 1): no *forced* overlap was detected. But
sampled chambers ≈ #samples and holdout coverage < 1 (76–78% for p=2, 24–29% for p=3), so the sample does
not resolve the arrangement; ply 1 on samples is not evidence of a ply-1 tiling.
(b) Holdout points of the selected subfamily already see ply 2–3 (p_k = 2,3), while the full greedy family
has ply 23–66: the naive "one tree per chamber" family overlaps heavily, a chosen subfamily far less.
(c) One size (n = 36) only: no growth rate in p_k vs #fibres/#chambers can be read off.
Verdict: neither "ply ≤ p_k^{O(1)}" nor "ply ~ #chambers" is supported; weak hint that small-ply covers are
not excluded at n = 36. TILE_k remains OPEN. Next: exact arrangement (enumerate chambers of the 245 forms for
k=1 via LP), test whether each chamber's validity set is covered by ≤ c greedy cones, and repeat at P_N = 30.
