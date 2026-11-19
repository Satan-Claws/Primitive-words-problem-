# poly_S3E: size of a single chain-validity set Π(T) — abstract star trees give |Π| = (P−1)!, D ≤ P (agent S3E)

Setting: poly_S3Q.md (Q2′, Π(T), D), poly_S2Q.md §1 (Lemma 1, π-monotone folds), poly_S2Y.md §2. P = P_N,
n = P². "Abstract" = μ any real vector on a vertex set with fibre sums 0, subset-generic (no proper nonempty subset
of a fibre sums to 0, μ(S_u) ≠ 0), trees bichromatic spanning, positions/NC ignored.
Status: **No superpoly bound from staircase/sign structure (PROVED, construction). Abstractly
(P−1)! ≤ max_T |Π(T)| ≤ P!/2, and for ONE fixed abstract μ, D ≤ P (P trees suffice). So abstract D ∈ [2, P].
For the actual μ_k (fixed supp, values forced by u_k, NC on Z_n) max|Π| and D remain OPEN.
CAVEAT: all of this bounds only the chain-valid (order-cone) selection route, not general covers / TILE_k.**

## 1. Upper bound (PROVED, from S3Q §4): |Π(T)| ≤ P!/2 for every T (T not GLAM2-valid ⇒ some comparability).
Refinement that does NOT improve it: if N(T) := {r : ∃u, s_u f_u[r] < 0} then π_1 ∉ N(T) for π ∈ Π(T)
(prefix sum at j = 1 is f_u[π_1]); and if r ≠ ρ (root fibre) is never negative then, propagating f_u[r] = 0 down
from the root (children of a vertex outside fibre r have same-sign r-coordinates summing to 0), the topmost fibre-r
vertex w has S_w ⊇ fibre r ("self-enclosed"). Self-enclosure costs only one disjunctive constraint inside S_w.
The staircase does NOT force a poset with P^{Ω(1)} comparabilities: constraints are disjunctive
("negative coordinate q must be preceded by enough positive mass") and can all be absorbed by one fibre.

## 2. Star trees: |Π(T_ρ)| = (P−1)! (PROVED; checked numerically P = 5, all 120 orders)
Fixed μ, per fibre q: R_q (+, A_q), buffers c_{q,r} (−, −a_{q,r}) for r ≠ q, g_q (+, b_q), d_q (−, −b′_q), with
generic a_{q,r} > b_r, b′_q > b_q, A_q = Σ_r a_{q,r} + b′_q − b_q (fibre sums 0).
T_ρ: root R_ρ; root children c_{ρ,r} (r ≠ ρ) each with child g_r; d_r (all r) as root children;
g_ρ under d_ρ; for q ≠ ρ: R_q under d_q, buffers c_{q,·} as leaf children of R_q.
Folds: f_{c_{ρ,r}} = −a_{ρ,r} e_ρ + b_r e_r (sign −, valid ⇔ ρ <_π r); every other subtree is single-fibre
(f_{d_q} = −b_q e_q, f_{d_ρ} = (b_ρ − b′_ρ)e_ρ, f_{R_q} = (b′_q − b_q)e_q, leaves). Hence Π(T_ρ) = {π : π_1 = ρ},
|Π| = (P−1)!, and ⋃_ρ Π(T_ρ) = S_P with the SAME μ: D ≤ P. Every subtree of T_ρ obeys Lemma 1 (only the root
fibre is "first").

## 3. Consequences
- A superpoly lower bound D ≥ P!/max|Π| needs max|Π| ≤ P!/superpoly; §2 shows this is false for abstract μ,
  so any such bound must use supp μ_k / u_k-values / non-crossing — e.g. that the P star trees (which reuse the
  same vertex positions in P differently-nested ways) are not simultaneously NC-embeddable, or that μ_k lacks
  the "one large positive vertex per fibre" (R_q) needed for a single-fibre-dominated root.
- Concrete test for S2Z/S3-style search at P = 6: for the real μ_k, look for star-type trees (all multi-fibre
  subtrees = (root-fibre buffer + one foreign leaf)); |Π| = 120 each would give D ≤ 6 and revive the route.
- Lower bound side unchanged: D ≥ 2 (S3Q). Gap for real μ_k: 2 ≤ D ≤ (unknown; ≤ P!).
