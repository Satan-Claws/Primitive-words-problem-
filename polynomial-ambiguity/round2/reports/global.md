# R2/global: the S_N primitive region away from U (far points, zero U-part, boundary, other strata)

W3, 2026-11-24. Scripts: `round2/scripts/global_forest.py` (≈ 2 s), `round2/scripts/global_sparse.py` (≈ 1 s).
Notation is as in `R2/realise.md`, `R2/newslice.md`, prompt §4.3–4.4. n = P², s_k = n/p_k, and V_k := V_{p_k}.
Positions are on the cycle ℤ_n. A **k-cycle** is an orbit of the shift by s_k (p_k points forming a regular p_k-gon).

**Verdict.**
- **G1.** realise's "near U only" restriction is an artifact of using single-root trees. Slack-transport forests
  tile {μ ≥ 1} globally with ply 1. So the pair-facet family covers **all** primitive points of (U ⊕ ⊕E_k) ∩ ℕⁿ: δ
  may be large relative to ω, ω may be 0, and coordinates may be 0. The ply is unchanged
  [written proof + exhaustive check].
- **G2.** A real hole, which is **near U**: the realise family misses x = t·1 + 1_D + 1_T for every t once N ≥ 6.
  Here δ is sparse and has several types, so δ ∉ ⊕E_k [written proof].
- **G3/G4.** This hole is **not** a negative candidate. Matching pieces with overlapping dual functionals cover it
  with ply 1. A piece's local form at U is constrained only through its lineality L = span(active rings)
  [written proof; certificate checked for N ≤ 8].
- **Net.** Every flag has as local form the complement of ≤ N subspaces (a smaller instance of the same problem).
  No new negative mechanism appears. One *construction* gap remains (§5).

## 1. The primitive set, exactly [written proof, elementary]
- On (ab*)ⁿ the word with exponent vector x is a proper power u^d iff x is (n/d)-periodic. So the primitive set is

  **𝒫_n = ℕⁿ ∖ ⋃_{k≤N} V_k**, on all of ℕⁿ.

  Off W_n every point is primitive; zero exponents play no special role.
- **ANOVA form.** Write a position as (a, y), with fibre a ∈ ℤ_P and CRT coordinates y ∈ ∏ℤ_{p_j}.
  - Decompose x = Σ_{T⊆[N]} x_T, where x_T depends on (a, y_T) and has zero mean in each y_j for j ∈ T.
  - Then x ∈ V_k ⇔ x_T = 0 for all T ∋ k.
  - So **x is primitive ⇔ ⋃{T : x_T ≠ 0} = [N]**. The sets T are complements of newslice's Fourier types.
  - U is T = ∅, and E_k is T = {k}.
- **Strata and flags.**
  - Take a flag of scales x = t₁ω₁ + t₂ω₂ + … + η, with t₁ ≫ t₂ ≫ … and η bounded. Take also a coordinate face J
    with bounded entries c off J.
  - The local primitive region is ℝ^J ∖ ⋃_{k∈A} (V_k ∩ (−c + ℝ^J)). Here A = {k : ω₁, ω₂, … ∈ V_k, J contains a
    k-cycle compatible with c}.
  - So every stratum is a smaller instance of the same "one witness per active prime" problem, with |A| ≤ N. On a
    sparse face J containing no k-cycle, prime k is inactive.
  - This answers (2)(ii) affirmatively at the level of local forms. The condition is a product of independent
    half-space conditions only in ⊕E_k coordinates. In general it is the set-cover condition above (see §3–4).

## 2. Theorem G1: global per-facet tiling [written proof + exhaustive computation]
Let S = supp μ, with μ ∈ {±1}^S. Positions lie on a line or cycle, and crossing is cut-invariant.

**LP.** The variables are
- f_pq ≥ 0 for μ_p = +1, μ_q = −1, with ring vector e_p + e_q;
- r_p ≥ 0 at + vertices (root slack, the one-block loop e_p).

The constraints are Σ_p f_pq = x_q at − vertices and Σ_q f_pq + r_p = x_p at + vertices. The cost is
h(|y_p − y_q|), with h strictly concave and increasing, made generic.

- **Feasibility.** The LP is feasible iff x ≥ 0 and μ(x) ≥ 0.
- **Bases.** A basis is a spanning forest of ring vectors in which each component has exactly one root, at a +
  vertex. It is unimodular: each component is a bipartite incidence matrix plus a unit column.
- **Tiling.** The cones of the c-dual-feasible bases form the regular triangulation of {x ≥ 0, μ(x) ≥ 0}.
- **Non-crossing.** Every such basis is non-crossing. At an interior x the optimum is unique with full support, and
  a crossing pair could be uncrossed at strictly lower cost: a nested swap when the edges interleave, a shorter
  disjoint swap otherwise.
- **Half-open rule.** Use η > 0 coordinatewise with μ(η) < 0. Then every x ∈ ℕ^S with μ(x) ≥ 1 lies in exactly one
  cell, and no x with μ(x) ≤ 0 lies in any cell. Cells are c + ℕV with c ∈ {0,1}-combinations (K = 2).
- **No coverage hypothesis.** Lemma C / Thm B (no balanced arc) is not needed here. Balanced arcs only split the
  forest, and multiple roots are allowed.

**Consequences.**
- *Products.* For a facet tuple σ = (μ₁, …, μ_r) with pairwise nested (gap-compatible) supports, the product pieces
  (forest per facet, loops e_i elsewhere) tile R_σ := {x ∈ ℕⁿ : μ_i(x) ≥ 1 ∀i} with ply exactly 1.
- *Ply of a family.* For any family Σ, ply(x) = #{σ ∈ Σ : x ∈ R_σ}. There is **no patching loss and no near-U
  condition**. The local-to-global patching of task (2)(i) is unnecessary for facet-defined pieces: they are exactly
  conic.
- *realise family.* For realise's pair facets, μ_k(x) = μ_k(δ_k) for every x = u + Σδ_k with u ∈ U. So Lemma 4's
  coverage probabilities ≥ 1/(2p_k) hold for **all** primitive x ∈ (U ⊕ ⊕E_k) ∩ ℕⁿ:
  - ‖δ‖ ≫ ‖u‖ is allowed;
  - u = 0 is allowed;
  - x may have zeros.
  Hence ply_VC ≤ n^{1+o(1)} on that whole subspace. audit_realise caveat 2 ("R⁰ only") is removed for ⊕E_k ⊕ U.

**Check.** `global_forest.py` enumerates all bases, keeps the dual-feasible ones, and tests non-crossing,
|det| = 1 and the ply of every lattice point of a box. It ran on m = 6, 7, 8 points, random signs, boxes [0,3]⁶,
[0,3]⁷ and [0,2]⁸, 10 instances, up to 35 cells and 16 384 points each.
- 0 ply violations: ply = 1 exactly iff μ(x) ≥ 1.
- All cells NC and unimodular.
- The tested points include up to 4499 per instance with μ(x) > max_{p∈+} x_p. These are the far-from-U points that
  no single-root tree covers.

## 3. Proposition G2: the realise family has a near-U hole off ⊕E_k [written proof]
**Setup.**
- Let D = {z, z + n/2} (a 1-cycle, 1_D ∈ V_2) and T = {w, w ± n/3} (a 2-cycle, 1_T ∈ V_3), in generic position.
- Put x_t = t·1 + 1_D + 1_T ∈ W_n. It is primitive for all t ≥ 0 and N ≥ 2.
- Its δ = 1_D + 1_T has present sets T ⊆ [N]∖{1} and T ⊆ [N]∖{2}, all of them present. So δ ∉ ⊕E_k once N ≥ 3.

**Proof.**
- Every facet μ ⊥ V_k satisfies μ(1) = 0, so μ(x_t) = μ(1_{D∪T}). A facet positive at x_t must therefore meet the
  5-point set D ∪ T.
- realise's tuples have N single-prime facets with pairwise disjoint supports. So **for N ≥ 6 no tuple contains x_t,
  for any t**, including t → ∞, which is the near-U regime.
- The same holds for every disjoint-support single-prime facet family. newslice's facet-economy fix, which merges
  primes into one facet, then needs multi-prime facets. Those are constrained as follows.

**Spread lemma [written proof; degree formula checked n = 36, 900].** Suppose μ ⊥ Σ_{k∈K} V_k is supported in an
arc of L consecutive positions. Then L − 1 ≥ deg lcm_k(X^{s_k} − 1) = n(1 − Π_K), with Π_K := ∏_{k∈K}(1 − 1/p_k).
- Reason: μ(X) is divisible by every X^{s_k} − 1.
- Consequence: two facets whose supports lie in disjoint arcs ("gap-compatible", forced for connected NC forests by
  a Jordan argument) satisfy Π_A + Π_B > 1.
- In particular at most one facet of a tuple has Π ≤ 1/2, and only one facet can contain prime 2, since its support
  is antipodally symmetric.
- For x_t with ≤ 5 facets this forces Π_{[N]} > 1/48. That is true for all realistic N, so G2 is a hole in the
  *pair-facet* family, not an impossibility for multi-prime cube facets.

## 4. G3/G4: the hole is not an obstruction [written proof; certificate checked]
**Prop G3 (matching pieces).**
- Let M = {e_{2b} + e_{2b+1}} be the adjacent non-crossing matching (laminar, K = 2), and P* = 1_{D∪T} + ℕM.
- For each k, μ_k = (1 − T^{m·s_k})(δ_{b₀} − δ_{b₀+1}) does the job, with b₀ even and adjacent to a point of D ∪ T:
  - μ_k ⊥ V_k;
  - μ_k(M) = 0, since s_k is even;
  - μ_k(1_{D∪T}) ≠ 0.
- So μ_k is a nonzero constant on P*, and P* misses every V_k. P* contains the whole ray x_t. The μ_k for different
  k **overlap in support**, which is allowed because they are dual certificates and not ring supports.
- Checks: `global_sparse.py` finds certificates for every k at N = 2…8 (n up to 9.4·10¹³, symbolically). It also
  passes the rank test 1_{D∪T} ∉ span M + V_p for all p and the sampled periodicity test (0 hits) at n = 36 and 900.

**Lemma G4 (local form of any laminar piece at U) [written proof, modulo convex separation as in LAM/S2P].**
- Suppose a piece c + ℕV covers t·1 + δ for unboundedly many t. Let L = span of the active rings, so 1 ∈ L.
- The piece's local cone avoids V_k ⇔ for each k there is μ_k ∈ (L + V_k)^⊥ positive on it.
- So δ is coverable near U by that piece only if **δ ∉ L + V_k for every k**.
- Laminarity constrains L (non-crossing connected components; each component carries one ratio pattern). It does
  not force the μ_k to have disjoint supports. That disjointness is an artifact of product constructions.

**Answer to (3).** The non-product local forms (set-cover conditions ⋃T = [N] with shared ANOVA components) do not
yield a laminarity obstruction. The only one found, G2, dies to G3. By Lemma VC-gen a negative argument must still
come from laminarity, i.e. from the lineality structure of G4. No such argument is known.

## 5. Exact gap (construction side)
**G-glob.** Find a bounded-offset (‖c‖₁ ≤ nK), poly-ply cover of the primitive points
x = t·1 + s·δ + η with 1 ≪ s ≪ t, δ ∉ ⊕E_k and sparse (fewer than N disjoint witness sets).
- P* handles bounded s only, because its offsets grow with the pair differences.
- For large s, the full-dimensional orientation cones c + ℕ(M ∪ {e_{2b} or e_{2b+1}}) are laminar, ply 1 and K = 2.
  They are valid iff for each k some pair-antisymmetric, sign-compatible μ_k ⊥ V_k has μ_k(c) ≥ 1. The x_t
  certificates above are sign-compatible.
- In pair coordinates (σ = pair sums, d = pair differences), x ∈ V_k ⇔ σ, d ∈ V′_k on ℤ_{n/2}. So 𝒫_n becomes
  "for every k: a σ-witness OR a d-witness", a disjunctive self-similar recursion n → n/2.
- Bounding its ply (naively 2^N·f(n/2)², not polynomial) is **OPEN**.
- This is an affirmative-side gap. It is not a lower-bound mechanism (§6 morphic self-similarity: exact transfers do
  not amplify).

## Status table
| claim | status |
|---|---|
| 𝒫_n = ℕⁿ ∖ ∪V_k; ANOVA cover criterion; flag/face local forms = complement of ≤ N subspaces | [written proof] |
| G1: slack forests tile {μ ≥ 1} with ply 1, NC, unimodular, K = 2, globally | [written proof] + exhaustive m ≤ 8 |
| realise family covers all primitive (U ⊕ ⊕E_k) ∩ ℕⁿ with ply_VC ≤ n^{1+o(1)} | [written proof] (G1 + realise Lemma 4 sketch) |
| G2: disjoint-support single-prime facets miss t·1 + 1_D + 1_T for N ≥ 6 (near U) | [written proof] |
| Spread lemma L > n(1 − Π_K); gap-compatible ⇒ Π_A + Π_B > 1 | [written proof]; degree formula checked |
| G3: matching piece covers that ray, ply 1, valid | [written proof]; certificates N ≤ 8, rank checks n ≤ 900 |
| G4: local-form criterion δ ∉ L + V_k | [written proof, modulo convex separation] |
| G-glob (large-scale sparse multi-type defects, bounded offsets, poly ply) | OPEN (construction gap) |

## Files
- `polynomial-ambiguity/round2/scripts/global_forest.py`: G1 exhaustive tiling check.
- `polynomial-ambiguity/round2/scripts/global_sparse.py`: G2 setup, G3 certificates, rank/periodicity checks,
  spread-degree formula.
