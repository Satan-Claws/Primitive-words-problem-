# R2/tile2: TILE_k, the upper bound. A ply-1 rule from min-cost transport

Status:
- **TILE_k(1) PROVED** for every μ that is *arc-generic* (Thm A, ω-level) or *W-arc-generic* (Thm B, x-level) [written proof].
- **The actual μ_k is W-arc-generic** for N = 2, 3, 4 and every k [computational, exact certificate]. For general N
  this is Lemma C, which is OPEN but purely combinatorial.
- **New negative finding** [computational, exact]: the ω-only formulation of tile.md §1 is **ill-posed** for the
  actual μ_k when N ≥ 3. There are proper arcs I with fold(μ_k|I) ≡ 0 (the two clusters of poly_LAM §2), so walls
  must be resolved by directions in W, not in U. Thm B does this.

## 0. Setting (tile.md §0, poly_S2P.md)
- Support points v_0, …, v_{m−1} of μ lie in circle order. A tree T is bichromatic, non-crossing (NC) and spanning.
- At a point x, put m_i := μ_i x_i.
  - **ω-level:** x = ω ∈ U_{>0}. Then Σ m_i = ⟨fold μ, ω⟩ = 0.
  - **x-level:** x ∈ W = U ⊕ ⊕_j E_j with x > 0. Then τ := Σ m_i = u_k(x_k). Put m'_{v_0} := m_{v_0} − τ (the root
    v_0 absorbs τ) and m'_i := m_i otherwise.
- T is *valid* at x (x ∈ K_T) iff every non-root subtree S_u has sgn m'(S_u) = sgn μ_u. This is S2P's K_T with
  root v_0.

**Transport dictionary [written proof].**
- For an edge {u, w} of T with u positive, put flow f_e := m'(side of u). Then T is valid at x iff all f_e > 0.
- This holds iff f is a non-degenerate basic feasible solution, with support exactly T, of the transportation
  problem TP(m'): x_{ij} ≥ 0 for i positive and j negative, Σ_j x_{ij} = m'_i, Σ_i x_{ij} = −m'_j.
- Reason: the side S of u is joined to the rest by e alone. So net outflow of S = m'(S) = f_e, which flows from
  the positive end to the negative end. Conversely, a basic solution of TP supported on a spanning tree has
  exactly these flows.

## 1. The rule
Fix a cost c_{ij} = h(|y_i − y_j|), where y_0 < … < y_{m−1} are generic reals (the circle cut just before v_0)
and h is strictly increasing and strictly concave (for example √).

**F_c** := the set of NC bichromatic trees T that are *c-dual-feasible*. That is, there are potentials α with
α_i + α_j = c_{ij} on the edges of T and α_i + α_j ≤ c_{ij} for every positive–negative pair.

Equivalently, T*(x) is the support of the unique min-cost plan of TP(m'(x)), and F_c = {T*(x)}. This is a
regular-subdivision / height-function rule: the "pulling" rule with height c.

**(Q) Uncrossing inequality.** Let a < b < c < d be four points with crossing pairs (a,c), (b,d). Then
cost(a,c) + cost(b,d) > cost of the bichromatic re-pairing.
- If a and b have the same colour, the re-pairing is the nested one, (a,d), (b,c). Strict concavity of h gives
  the inequality.
- If a and b have opposite colours, the re-pairing is the disjoint one, (a,b), (c,d). h strictly increasing gives
  the inequality.

Genericity: c is chosen off the finitely many hyperplanes {alternating sum of c around a cycle of K_{+,−} = 0}.

## 2. Theorem A/B (ply exactly 1) [written proof]
**Theorem.** Let μ be any vector with fold μ = 0 and fixed sign pattern.
- **(i) Ply ≤ 1 everywhere.** For every x, at most one T ∈ F_c is valid at x.
- **(ii) Coverage.** If no proper arc I of supp μ is identically balanced, then every generic x lies in exactly one
  K_T with T ∈ F_c.
  - At ω-level "identically balanced" means fold(μ|_I) = 0 (Thm A). This is tile.md's genericity.
  - At x-level it means the form x ↦ Σ_{i∈I} μ_i x_i vanishes on W (Thm B).
  - With the lex rule of S2P §1(b) (generic η, η ∈ W for Thm B), every point of the region, walls included, has
    ply exactly 1.
- Hence TILE_k(q = 1).

**Proof.**

(i) Suppose T, T' ∈ F_c are both valid at x.
- Then f_T and f_{T'} are feasible for TP(m'(x)) (by §0) and dual feasible, so by complementary slackness both
  are optimal.
- Because c is generic, every non-tree reduced cost of a dual-feasible tree is > 0. So the optimum is unique:
  for feasible z, c·z − c·f_T = Σ_{e∉T} r_e z_e, which is > 0 unless z = f_T.
- So f_T = f_{T'}. Both flows are strictly positive exactly on their trees, so T = supp f_T = supp f_{T'} = T'.
- Nothing about μ or x was used beyond strict validity. Lex walls reduce to generic points x + εη, so (i) holds
  at every point. ∎

(ii) Let x be generic: off the finitely many hyperplanes {m'(S) = 0} for subsets S whose form is not
identically 0 on the region.
- TP(m') is feasible and bounded, so it has a unique optimum z*, which is a vertex. Its support is therefore a
  forest.
- **z* is non-crossing.** Suppose two support edges cross. Move t = min of their flows onto the bichromatic
  re-pairing of (Q). The plan stays feasible and the cost drops strictly, a contradiction.
- **The support is connected.** Each component C of the support is a balanced set: m'(C) = 0. Components of an NC
  forest are pairwise non-interleaving, because two disjoint paths inside a disc joining alternating boundary
  points must cross. Non-interleaving blocks form a non-crossing partition, and if there are ≥ 2 blocks one of
  them is a proper arc I. Then m'(I) = 0 at the generic point x, so the form of I is identically 0. This is
  excluded by hypothesis.
- So supp z* is a spanning NC bichromatic tree T* with all flows > 0. By §0, T* is valid at x.
- T* is optimal and non-degenerate, so its reduced costs are ≥ 0 (otherwise a positive pivot would improve the
  cost). Hence T* ∈ F_c.
- Uniqueness is (i). ∎

**Remarks.**
- (a) The rule is universal. F_c tiles the whole mass space {Σ m = 0, fixed signs} as a complete fan (the
  chamber fan of the LP in the right-hand side). Every section of it, by an ω-space or W-space, inherits ply ≤ 1.
  The only thing that can fail is coverage, through an identically balanced arc.
- (b) No genericity of the arrangement 𝒜 is needed: parallel or repeated hyperplanes, and the periodic structure
  of μ_k, are irrelevant. This answers "highly non-generic".
- (c) This explains tile.md §3: the CP-SAT fans exist because a regular (cost-induced) fan always exists. The
  greedy rules (LAM §2(b), leftmost DP) are not regular, which is why their cones overlap.
- (d) The trees vary with x, as they must (GLAM2: ω-uniform trees force ply ≥ (P_N/2)^N). No tree is valid near
  two vertices (S3V). Both facts are consistent with this.
- (e) This is **not** chain-valid / order-cone selection (dead, S3A/S3L). The cones K_T of F_c are not unions of
  order cones.
- (f) The x-level region is the near-U cone R⁰ = {x ∈ W : x > 0, sgn(m_{v_0} − τ) = sgn μ_{v_0}}. It contains
  U_{>0} (where τ = 0), and S2P's R_k(u) ("near U_{>0}") lies in it. Outside R⁰ no tree rooted at v_0 is valid at
  all. Root choice is S2P's localisation, not TILE's.

## 3. Lemma C (arc-genericity of the actual μ_k)
μ_k = g·ν_k with g = (1 − T^{n/p_k}) ∏_{j≠k}(1 − T^{P p_j}), and ν_k generic on a window of length P p_k.
- **ω-level fails for N ≥ 3 [computational, exact; also by hand].** The cluster ρ = ∏_{j≠k}(1 − T^{P p_j})ν has
  fold ρ = 0. When the two clusters ρ and T^{n/p_k}ρ are separated (width < n/p_k, the regime of poly_LAM §2(a)),
  each cluster is an identically balanced arc.
  - Exact structural counts of balanced arcs (`tile2_muk.py`):
    - N = 2: 0 and 0.
    - N = 3: 241, 301, 0 for k = 1, 2, 3.
    - N = 4: 3363, 3783, 1683, 1 for k = 1..4 (random-ν count).
  - LP test at ω-level for N = 3: the optimal plan splits into exactly zero-mass arcs (sizes 360 + 120, 300 + 300,
    450 + 150). The failures are genuine, not numerical.
  - So tile.md §1's reduction to ω-chambers is ill-posed for actual μ_k. Such an f_I ≡ 0 is a "wall" equal to all
    of U, and only a direction in W resolves it.
- **x-level holds [computational, exact certificate].** No proper arc I has μ|_I ⊥ W, with W = Σ_j
  {period-(P p_j) vectors} (U ⊕ ⊕E_j for the natural E_j). Equivalently, for every arc some fold mod P p_j of
  μ|_I is ≠ 0.
  - N = 2 (n = 36), N = 3 (n = 900): exact structural check (prefix fold matrices in ℤ^{(ΣPp_j)×w}, all distinct):
    0 balanced arcs for all k.
  - N = 4 (n = 44100, |supp| 6300–7140): one integer ν. Distinct prefix vectors certify non-balance exactly:
    0 balanced arcs for all k.
- **General N: OPEN.** It is a finite combinatorial statement about the fixed polynomial g. A proof would show
  that for every proper arc I some ν-coefficient D_q = Σ_{S⊆F, q+σ(S)∈I} (−1)^{|S|} δ_{q+σ(S)} pairs nonzero with W.
  - If I contains a full orbit {q + σ(S)}, then D_q = T^q g, which pairs nonzero with E_k, since g acts
    invertibly on E_k.
  - Partial orbits are the remaining case.

## 4. Computation (evidence for the proof's hypotheses and sanity; not proof)
| test | result |
|---|---|
| P = 3, exact chambers, ALL trees enumerated with edges (tile_p3exact instances), m = 9: 20 instances × 2 costs | F_c cones partition the chambers EXACTLY: **40/40** (\|F_c\| ≤ 35; trees up to 767) |
| same, m = 11 | **40/40** exact partitions (trees up to 4514, \|F_c\| up to 84) |
| actual μ_k, N = 2 (n = 36, \|supp\| 24 / 36), 60 base points each (30 ω-level + 30 x-level), exact validity | T* spanning, NC and valid at the point: 60/60 for both k; pairwise "T*(x′) valid at x ⇒ T*(x′) = T*(x)": 0 violations; 59 distinct trees per 60 points |
| actual μ_k, N = 3 (n = 900, \|supp\| 480–600), 8 points each | x-level: valid T*, **12/12**. ω-level: 6/12, every failure a split into exactly-zero arcs (Lemma C, ω-part) |

Dual margins are > 0 throughout (min 3.5·10⁻⁵ at N = 3). The LP is floating point; tree, validity and arc masses are
checked in exact integers.

## 5. Consequence for S_N (precise)
Combine Thm B, Lemma C and S2P §1(a)/(b) (q_k := max number of chosen trees containing a point).
- For every k and every u_k (with ν_k generic), the family 𝒯_k(u) := F_c(μ_k(u)) has q_k = 1 on the near-U region,
  walls included by the lex rule.
- So the patched laminar cover of the S_N product region has

    ply ≤ ply_VC · ∏_k q_k = ply_VC = O(N log N Σ_k d_k) = √n · polylog n.

- This answers G-LAM (poly_LAM §3, poly_GLAM §1) affirmatively with overlap 1 per component.
- **The S_N candidate is therefore BLOCKED at the geometric (cone-ply) level** [written proof for N ≤ 4; for all N
  modulo Lemma C]. No argument of type Lemma G* can extract n^{ω(1)} from the ply of the laminar
  validity-cone geometry of S_N near U_{>0}.

What remains before S_N is fully dead as a candidate (that is, before a poly-ambiguous grammar on the S_N slices
exists):
1. **Lemma C for all N** (combinatorial; §3).
2. **Realisability.** The pieces L_σ = c_σ + ℕV_σ (u-sample × F_c-trees, LAM §2(c) edge vectors, offsets c_σ
   implementing the lex rule) must be produced by one CFG for Q ∩ slice with ambiguity equal to the cover ply.
   This is the converse of Lemma 3P. It includes:
   - the off-W_n part (T1 P1);
   - lower strata and the boundary of U_{≥0};
   - points outside the near-U cone R⁰ (§2(f));
   - the number of pieces, which is finite but can be exponential, so grammar size is not controlled.
3. **G3** (length side).** The offsets and lattices of the overlapping pieces must not leave lattice points
   uncovered. This needs polynomial apex, covering radius and inradius (prompt §4.4(ii)). Otherwise extra pieces
   are needed near the apex and ply there is uncontrolled. G3** is no longer needed to *block* G* (ply is now
   polynomial everywhere the cones are used). It is needed to make the cover genuine at every lattice point.

## Files
- `polynomial-ambiguity/round2/scripts/tile2_core.py`: the rule. Cost, LP (HiGHS), exact validity, NC check,
  dual margin.
- `polynomial-ambiguity/round2/scripts/tile2_fan_check.py`: exact P = 3 partition check against all trees. Run
  `… 20 9` (1 s) or `… 20 11` (4 s).
- `polynomial-ambiguity/round2/scripts/tile2_muk.py`: actual μ_k. Arc-genericity (exact) and the rule test. Run
  `… 2 60 1` (< 1 s) or `… 3 8 1` (≈ 2.5 min).
- Cited: R2/tile.md, PA/poly_S2P.md §1, poly_LAM.md §2–3, poly_GLAM.md, poly_GLAM2.md, poly_S3A/S3L/S3V.md.
