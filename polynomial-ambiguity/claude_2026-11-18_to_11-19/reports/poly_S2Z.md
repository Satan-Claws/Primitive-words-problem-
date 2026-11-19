# poly_S2Z — computer probe of S2Y Q1/Q2 at n = 36 (P_N = 6, p ∈ {2,3})

Status: **[computational] INCONCLUSIVE — no chain-valid tree found for any sampled order π; search not exhaustive. Q2 not reached.**

## Setup
Targets μ_k from `s2x_tile.make_mu` (k=1: p=2, |supp|=24; k=2: p=3, |supp|=36), seeds 0,1 (4 targets).
For 100 random orders π (of 720) per target: DFS over LAM §2(b) contraction sequences (merge cyclically
adjacent opposite-sign clusters x→y; gives NC bichromatic trees), pruning: absorbed cluster's fold vector F_x
must be chain-valid, s_x·Σ_{t≤j} F_x[π_t] ≥ 0 ∀j; final edge checked likewise (F_x = −F_y, s_x = −s_y — NOT
automatic; an early run that skipped it produced spurious "valid" trees). Dead-state memo, node limit 4000/π.
Found trees are re-verified with `edge_forms` (every edge side, every prefix).

## Data
| target | found / 100 π | DFS outcome |
|---|---|---|
| p=2 seed 0, 1 | 0, 0 | all 100 hit node limit |
| p=3 seed 0, 1 | 0, 0 | all 100 hit node limit |
(An earlier run with limit 20000 on 20 π of p=2 seed 0 also found none once the final-edge check is in place.)

## Reading
Chain-validity on all of O_π is hard to satisfy: the heuristic ordering (lex point of O_π) never completes.
This is weak evidence AGAINST Q1 for generic multi-fibre μ_k, but proves nothing (no exhaustive refutation; a
contraction sequence may also miss some NC trees). Q2 (cones met by K_{T(π)}; script computes it by 20k
sampled ω + exact LP over 720 order cones) is untested since no T(π) was found.
Next: exact ILP/CP-SAT over NC trees with chain constraints, or an LP-duality certificate of infeasibility for
a fixed π (e.g. show some prefix A_j forces a sign-mixed edge).

Script: `scripts/poly/s2z_chain.py` (`python3 s2z_chain.py [seeds=2] [nodelimit=5000] [npi=100]`, ≈2 min).
