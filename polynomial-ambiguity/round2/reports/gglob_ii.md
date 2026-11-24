# R2/gglob_ii: G-glob′ (ii), the signed slack-forest tiling on d_M-space

W4, 2026-11-24. Scripts: `round2/scripts/gglobii_signed_forest.py` (each run below takes ≤ 4 s) and
`round2/scripts/gglobii_obstruction.py` (< 1 s). Notation follows `R2/gglob.md` and `R2/global.md`.
- M is a non-crossing (NC) matching. Each chord a = {a⁺, a⁻} gives a coordinate d_M(x)_a = x_{a⁺} − x_{a⁻}.
- z ∈ ℤ^M is a point of d_M-space. μ is a facet on d_M-space.
- An original ring e_p (or e_p + e_q) maps to ±e_a (or ±e_a ± e_b). Rings inside one chord map to 0, which is L(M).

**Verdict.**
- **G1 extends to signed rings (Theorem S1) [written proof + exhaustive check].** It needs two hypotheses:
  - (H1) |μ| is constant on supp μ (WLOG μ ∈ {±1}^S);
  - (H2) the face graph G_M(S) is connected. In G_M(S), two chords of S are adjacent iff they bound a common face of
    the chord diagram M.
- Under (H1) and (H2), the signed problem is an **ordinary directed min-cost flow**. Its matrix is a network
  matrix, hence totally unimodular (TU). So:
  - there are no odd cycles;
  - c + ℕV = (c + cone V) ∩ ℤ^S holds exactly;
  - the bases are rooted forests;
  - the ply is exactly 1;
  - the rings satisfy ‖ring‖₁ ≤ 2, are laminar with each other, and are laminar with M.
- **Both hypotheses are necessary for a per-facet (G1-style) tiling [written proof + exact check].**
  - O1: a chord outside supp μ that separates supp μ makes such a tiling impossible.
  - O2: so do unequal weights.
  - (H2) fails for most supports under random NC matchings (§4). It always holds for "star" matchings such as M₀
    and M₁.
- So (ii) is **proved for facets satisfying (H1) and (H2)**. In general it is **not closed**: O1 kills the per-facet
  route, but it does not refute (ii), because pieces need not lie in a single facet half-space.

## 1. The signed problem, exactly
- Write the region as R_μ = {z ∈ ℤ^S : μ(z) ≥ 1}. There is no positivity in d_M-space.
- Off S, the coordinates are tiled by the half-open orthants 0 + ℕe and −e + ℕ(−e), with ply 1, using one-point rings
  e_{a±}.

**Ports.** h(a) := a^{μ_a} is the head and t(a) := a^{−μ_a} is the tail.

**Sign change.** Put w := D_μ z, so that μ(z) = 1·w. The balanced rings with ‖·‖₁ ≤ 2 (μ(v) = 0) and the positive
one-point rings become:

| original ring | z-image | w-column | μ-value |
|---|---|---|---|
| e_{h(a)} + e_{t(b)}, a ≠ b ("arc a→b") | μ_a e_a − μ_b e_b | e_a − e_b | 0 |
| e_{h(a)} ("loop a") | μ_a e_a | e_a | 1 |

**LP (SLP).** min Σ c_{ab} f_{ab} + Σ ε_a r_a subject to Σ_b (f_{ab} − f_{ba}) + r_a = w_a, with f, r ≥ 0.
- Arcs a→b are allowed iff a and b bound a common face of M. Each pair of chords shares at most one face, because
  the dual graph of M is a tree.
- The arc cost is c_{ab} = h(|y_{h(a)} − y_{t(b)}|), where y gives the positions after a cut, h is strictly
  increasing and strictly concave, and c is generic. The ε_a are tiny and generic.
- This is a transshipment problem on the digraph G_M(S), with both orientations of each edge, plus a root node 0
  that has arcs 0→a.
- It is feasible iff 1·w ≥ 0, provided G_M(S) is connected. The cost has no negative cycles.

**What the "signed graph" really is.** In z-coordinates the ring set is bidirected (±e_a ± e_b). It is *balanced*:
the switching D_μ turns every edge into a directed edge e_a − e_b. Odd (unbalanced) cycles need a ring with
μ(v) = ±2, that is w-column ±(e_a + e_b). The LP **excludes** these rings, and it never needs them.
- If they are included and are cheap, the LP does use them. Then det = 2 occurs and exactness fails.
- Example: w = e₀ = ½(e₀ − e₂) + ½(e₀ + e₂), which lies in a cell of the basis {arcs 0→1, 0→2, 0→3, ring e₀ + e₂}
  but has half-integral coordinates in it. In `… 4 1 2 all 1`, all 46 cells have det 2, and 20 box points per
  instance are half-integral.

## 2. Theorem S1 [written proof]
Assume (H1), (H2), and generic c. Then:
- (a) **Bases.** The bases are the spanning forests of G_M(S), with arbitrary arc orientations and exactly one loop
  per component. A loop may sit at *any* vertex, unlike G1, where loops sat only at + vertices. Every basis has
  |det| = 1, because a network matrix is TU.
- (b) **Tiling.** The cones of the c-dual-feasible bases triangulate {1·w ≥ 0}. This is the regular subdivision of
  an LP in its right-hand side.
  - Take a generic η with 1·η < 0, and use the half-open rule as in G1.
  - Every w ∈ ℤ^S with 1·w ≥ 1 then lies in exactly one cell. Reason: w + εη is generic and lies in the interior.
  - Every w with 1·w ≤ 0 lies in no cell. Reason: the loop coordinates are ≥ 0 and sum to 1·w. If 1·w = 0 they are
    all 0, and then they need q′ > 0 although Σ q′_loops = 1·η < 0.
  - Each cell is exactly c + ℕV, with c = Σ_{q′_v<0} v (offsets are {0,1}-combinations and ‖c‖₁ ≤ 2|S|). This
    follows from (a), since V is a ℤ-basis.
- (c) **Laminarity.** In every dual-feasible basis, the arc chords h(a)t(b) are pairwise NC. They are also NC with
  every chord of M (including chords outside S).
  - *With M:* chord h(a)t(b) is a segment inside the convex face F shared by a and b, so it crosses no M-chord.
  - *Arcs in different faces* have disjoint interiors.
  - *Arcs in the same face F:* suppose arcs a→b (flow f) and c→d (flow g) cross. All four ports lie on ∂F, in
    circle order. The two chords are head–tail pairs. The only other head–tail re-pairing is (h(a), t(d)),
    (h(c), t(b)), and it is nested or disjoint according to the colour pattern. By (Q) of tile2 (strict concavity
    in the nested case, strict monotonicity in the disjoint case) it costs strictly less.
  - Move min(f, g) onto the arcs a→d and c→b. Both lie in F, so they are allowed. The node balances are unchanged:
    a and c each still send min(f, g), and b and d each still receive it.
  - If d = a, the arc "a→a" has column 0 and is dropped, which lowers the cost further. Antiparallel arcs a⇄b cancel
    the same way.
  - At an interior w, the optimum of a dual-feasible basis is unique and has full support (generic c). So a crossing
    pair contradicts optimality. ∎
- (d) **Lift.** Each cell lifts to an original-coordinate piece. Its rings are e_{h(a)} + e_{t(b)} and e_{h(a)},
  with K = 2, and they are laminar with M.

**Corollary.** Take M with all chords on one face, such as the adjacent matchings M₀ and M₁ of gglob G6. Then
(H2) holds for every S. So every ±1 facet on d_M-space has a ply-1, TU, NC tiling.

## 3. Exhaustive checks (`gglobii_signed_forest.py m B trials mode`) [computational]
**Method.**
- Cells are found by exact dual-simplex wall-crossing BFS from one LP optimum. This is complete, because the cells
  triangulate a convex cone.
- For m ≤ 5, the BFS cell list is cross-checked against brute-force enumeration of all m-subsets of columns.
- The ply check covers every box point when (2B+1)^m ≤ 70 000, and otherwise 5000 random box points.

| mode | m | instances | cells per instance | brute = BFS | det | rooted forests | NC among arcs | NC with M | ply violations |
|---|---|---|---|---|---|---|---|---|---|
| region (S = M) | 4, 5, 6, 7, 8, 10 | 3, 2, 4, 2, 3, 2 | 21 – 10 768 | yes (m ≤ 5) | all 1 | all | all | all | 0 |
| sub (S ⊊ M, G_M(S) connected) | 4, 5, 6, 8, 10 | 3 each | 21 – 11 710 | yes (m ≤ 5) | all 1 | all | all | all | 0 |
| all (every pair, no face restriction) | 4 – 9 | 13 in total | 35 – 20 152 | yes (m ≤ 5) | all 1 | all | all | **only 3 – 46 % of cells** (100 % in two m = 4 instances) | 0 |

- "all" mode still tiles with ply 1, unimodular and with pairwise-NC arcs. The arcs cross M-chords, though: routing
  through a chord's face is cheaper than respecting it.
- So the face restriction (H2) is what buys laminarity with M.
- The region test sets are 270 – 6937 points (m = 4 – 6) and about 2200 – 2700 sampled points (m ≥ 7). They cover
  1·w ≥ 1, and points with 1·w ≤ 0 are checked to have ply 0.

## 4. Obstructions (exact; `gglobii_obstruction.py`) [written proof + exact enumeration]
**Lemma.** Let a piece c + ℕV ⊆ {μ ≥ 1} have integral generators. Every point with μ = 1 has the form
c + Σ_{μ(v)=0} n_v v.
- So if the balanced rings span less than μ^⊥, a family of μ = 1 points that is unbounded modulo that span meets
  each piece at most once.
- Then no finite family of per-facet pieces covers R_μ.

**O1 (H2 fails: separating chord).** Take points 0..5 and M = {a = (1,2), e = (0,3), b = (4,5)}, so e separates a
from b. Take μ = z_a − z_b.
- There are 23 rings with ‖·‖₁ ≤ 2 that are NC with M. Their balanced d_M-images are only ±e_e and ±2e_e, of rank 1,
  while dim μ^⊥ = 2.
- So the points (z_a, z_e, z_b) = (k+1, 0, k), all with μ = 1, need infinitely many pieces.
- This is exactly the shape of a shift certificate a = e_α − e_{T^s α} (gglob §1) whenever M nests a chord between
  α and T^s α.

**O2 (H1 fails).** Take μ = (1, 2) on two chords sharing a face.
- None of the 14 laminar rings has a nonzero balanced image. The ±e_a ± e_b have μ ∈ {±1, ±3}.
- So the family (1 − 2k, k) needs infinitely many pieces.
- The repair would use rings 2e_a − e_b, with ‖·‖₁ = 3 > 2.

**Frequency of (H2) failure.** Random NC M with random S:

| \|M\| | \|S\| = 2, 4, 6 | \|M\| | \|S\| = 2, 6, 12 |
|---|---|---|---|
| 8 | 242, 288, 240 of 400 disconnected | 18 | 306, 389, 388 of 400 disconnected |

M₀ and M₁ are always connected. So, combined with gglob (i), which needs varying *random* M, the per-facet route
fails for most (M, μ) pairs.

## 5. What this leaves (exact)
- **(ii) holds** for every M and every ±1 facet μ with G_M(supp μ) connected.
- In particular it holds for M₀ and M₁ and all ±1 facets, with ply 1, TU, NC with M, K = 2 and ‖offset‖₁ ≤ 2|S|.
- **Open (ii′).** For separated supports there are two possible routes:
  - choose the facet μ ∈ d_M(V_k)^⊥ with ±1 entries and face-connected support. For example, b = (1 − T^s)·1_P with
    P a face path, but the magnitudes can then reach 2, which is O2;
  - or use pieces that are not contained in a single facet half-space. In O1 such pieces exist, for example
    generators e_a + e_e (μ = 1) and e_b − e_e, but their validity is then a ∪V_k-avoidance question rather than a
    tiling.
- **Caveat on the model.** The true laminarity constraint is NC with the level-t ring forest F₁, not merely with M.
  The ballot matching M ⊆ blocks of F₁ is a proxy, and NC with F₁'s tree chords is at least as restrictive. That
  extra constraint is not tested here.

## Status
| claim | status |
|---|---|
| S1: under (H1) and (H2), the signed SLP is a directed network flow; TU; rooted-forest bases; ply 1 on {μ(z) ≥ 1}; NC among arcs and with M; K = 2 | [written proof] + exhaustive m ≤ 10 |
| Odd cycles and det 2 arise only from μ-unbalanced rings ±(e_a + e_b) in w; excluded; exactness otherwise fails (explicit) | [written proof + exact] |
| Without the face restriction: still ply 1 and TU, but arcs cross M | [computational] |
| O1, O2: (H2) and (H1) are each necessary for any finite per-facet tiling by ‖ring‖₁ ≤ 2, M-laminar pieces | [written proof + exact enumeration] |
| G-glob′ (ii) for separated supports and general M (most random M); F₁-laminarity | OPEN |

## Files
- `polynomial-ambiguity/round2/scripts/gglobii_signed_forest.py`: Theorem S1 checks (modes region, sub, all, and
  mass2 demo).
- `polynomial-ambiguity/round2/scripts/gglobii_obstruction.py`: O1, O2 and the frequency of (H2) failure.
