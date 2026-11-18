# poly_S2Q: GLAM2 induction under chain-validity — no fibre-count restriction; a π-monotonicity lemma (agent S2Q)

Setting: poly_GLAM2.md §1, poly_S2Y.md §2 (Q1), poly_S2Z.md. f_u := fold(μ|_{S_u}) ∈ ℝ^{P}, fold(μ) = 0,
L = prefix-sum map in π-order, (Lf)(j) = Σ_{t≤j} f[π_t]. T chain-valid for π ⇔ s_u·L f_u ≥ 0 (coordinatewise)
for every non-root u, s_u = sign of u = top sign of u. pos(r) := index of fibre r in π.
Status: **"chain-valid ⇒ ≤ 2 fibres / single fibre" FALSE (PROVED, explicit 3-fibre example, abstract trees);
π-monotonicity lemma PROVED; Q1 stays OPEN — any obstruction must use the fixed support / NC geometry of μ_k.**

## 1. Lemma (π-monotone folds, PROVED)
If T is chain-valid for π, then for every vertex u: f_u[π_t] = 0 for all t < pos(res u)
(the subtree's fold lives on fibres weakly π-after u's own fibre).
Proof (GLAM2 induction with ≥0 replaced by the cone L^{-1}(ℝ_{≥0}^P)). Root: f_root = fold(μ) = 0. Let u have
sign s, children d (sign −s): Σ_d L f_d = L f_u − μ_u·1_{j ≥ pos(res u)}. For j < pos(res u) the right side is
L f_u(j), of sign s (weakly; = 0 at the root), the left side of sign −s: both vanish. Each s_d L f_d(j) ≥ 0 and
they sum to 0, so L f_d(j) = 0 for j < pos(res u). In particular L f_u(j) = 0 for j < pos(res u), i.e.
f_u vanishes on π_1..π_{pos(res u)−1}. ∎
(GLAM2's single-fibre conclusion needed the cone ℝ_{≥0}^P, whose sums vanish only termwise *coordinatewise for
every coordinate*; for L-cone only the coordinates j < pos(res u) are forced, the rest are free.)

## 2. Chain-valid 3-fibre example (PROVED, by hand)
P ≥ 3, π = (1,2,3,…). Vertices (sign, fibre, μ): root R (+,1,2.1); children of R: c (−,1,−2.1),
c′ (−,2,−1), c″ (−,3,−1); children of c: g₂ (+,2,1), g₃ (+,3,1).
Fibre sums: 2.1−2.1 = 0, −1+1 = 0, −1+1 = 0 ⇒ fold(μ) = 0. Bichromatic. f_c = (−2.1,1,1), L f_c = (−2.1,−1.1,−0.1) < 0;
leaves trivially valid; all μ(S_u) ≠ 0. On O_π: n_c(ω) = −2.1ω₁+ω₂+ω₃ < 0 ✓. Any abstract tree is NC-embeddable
when positions are free (place vertices in DFS order, choose gaps to fix residues), so the GLAM2-style
"abstract, any n" refutation of Q1 is impossible. Consistent with Lemma 1 (every vertex is π-minimal in its fold
support). Perturbing values keeps validity (strict inequalities), so this is not a degenerate case.

## 3. Consequence for the order-cone selection route
- Q1 is NOT refuted by sign/linear-algebra alone: chain-validity permits arbitrarily many fibres. A NO answer must
  use what GLAM2 did not need — the fixed supp μ_k, its values (forced by u_k), and non-crossing on Z_n.
- Lemma 1 is a necessary condition that S2Z's DFS can use as exact pruning: a cluster with representative residue r
  may only absorb fold mass on fibres π-after r (prefix sums before pos(r) must stay 0), and the root's fibre
  ρ must satisfy f_c = 0 on π-before ρ for every root child — strongly favouring ρ = π_1.
- Heuristic tension: for generic μ_k every fibre π_1-mass must be cancelled inside subtrees rooted at fibre-π_1
  vertices; S2Z's empty search suggests the NC/value constraints bite, but this is unproved.
Route status: order-cone selection ALIVE (OPEN), not killed; next step = exact search with Lemma-1 pruning, or
a NC-specific obstruction.
