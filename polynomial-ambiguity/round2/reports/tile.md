# R2/tile: TILE_k, the ply side (agent W1-A)

Status: **TILE_k OPEN.** Proved: (T1) topological covering lemmas (KKM / Sperner / Lebesgue) cannot give any ply
lower bound for TILE_k [written proof]; (T2) TILE_k is exactly a chamber exact-cover problem [written proof].
Computed: in every small abstract instance tested (P = 3 exact, m ≤ 11; P = 4 LP-based, m ≤ 11), the full family of NC-tree
validity cones contains a **ply-1 fan** [computational]. So no "forced overlap" lemma built only from the fold lemma,
the near-vertex result and non-crossing can hold at these sizes; a lower bound must be asymptotic in P_N (or use the
specific support of μ_k). Neither (i) nor (ii) of the task is achieved.

## 0. Definitions (as in PA/poly_S2Y.md §1, PA/s3a_ncdp.py)
- P = P_N; ω ∈ U_{>0} ≅ ℝ^P_{>0}. μ = μ_k has fold(μ) = 0, where fold(x)_r = Σ_{i ≡ r (P)} x_i ("fibre" r).
- T: a non-crossing (NC) spanning tree on supp μ in ℤ_n circle order, bichromatic (adjacent vertices have opposite
  sgn μ). Root T at the first support point v₀. Then every subtree vertex set S_u is a linear interval of the other
  support points (S3A). Put f_u = fold(μ|_{S_u}) ∈ ℤ^P and s_u = sgn μ_u.
- K_T = {ω ∈ ℝ^P_{>0} : s_u⟨f_u, ω⟩ > 0 for every non-root u}. This is an open polyhedral cone and does not depend
  on the root, because fold(μ) = 0.
- 𝒜 = {f_I^⊥ : I a linear interval of supp μ ∖ v₀}. A *chamber* is a connected component of ℝ^P_{>0} ∖ ∪𝒜.
  Each K_T is a union of chambers.
- Half-open rule (PA/poly_S2P.md §1(b)): fix a generic η. A point x is counted in T iff x + εη ∈ K_T for all small
  ε > 0. ply_𝔉(x) = #{T ∈ 𝔉 : x counted in T}.
- TILE_k(q): some finite family 𝔉 of trees covers U_{>0} with ply ≤ q everywhere. The target is q = p_k^{O(1)}.

## 1. T2: reduction to chambers [written proof]
For x ∈ U_{>0} and generic η, the point x + εη lies, for all small ε > 0, in one chamber C(x), since 𝒜 is a finite
central arrangement. So ply_𝔉(x) = #{T ∈ 𝔉 : C(x) ⊆ K_T}. Therefore

  TILE_k(q) ⇔ some 𝔉 has every chamber in at least 1 and at most q of the sets K_T (T ∈ 𝔉).

In particular, ply 1 ⇔ the chambers can be exactly partitioned into tree cones. ∎
This makes TILE_k an exact finite set-cover problem for each fixed μ. The scripts below solve it exactly.

## 2. T1: topological covering lemmas are blocked [written proof]
Claim. No argument that uses only closure or incidence data of the cones, such as KKM, Sperner, Lebesgue covering
dimension or nerve dimension, can prove ply ≥ 2 for TILE_k.

Proof.
- Such lemmas bound the multiplicity of an **open** cover of a **compact** set, or of a closed cover.
  - KKM form: assign each set to a facet {ω_i = 0} that its closure misses. Then some point lies in P sets.
- The sets actually counted, the half-open cones of §1, are neither open nor closed.
- By §1, any subfamily that is a complete fan (closures cover, interiors disjoint) has half-open ply exactly 1, even
  though all its closures meet at interior rays. Example: the order-cone fan (PA/poly_S2Y.md §3).
- So the closure multiplicity that KKM bounds (≥ P at some point) is compatible with ply 1.
- If one insists on genuinely open cones K_T, they cannot cover the walls without overlapping. That forced
  multiplicity is an artefact the lex rule removes.
- Hence the topological hypotheses hold for fans, and the conclusion says nothing about ply. ∎

Consequence. A lower bound for TILE_k must prove that the specific family {K_T} contains **no sub-fan and no
low-ply subfamily**. That is a statement about which chamber unions occur as tree cones, as in §1.

The fold lemma (PA/poly_GLAM2.md) and the near-vertex result (PA/poly_S3V.md) only say that certain cones do not
exist: no cone contains U_{>0}, and none is valid near two vertices. These are tree-count statements. §3 shows they
are compatible with ply-1 fans.

## 3. Computation [computational]
The instances are abstract. supp μ is a cyclic sequence of m points with residues r_i ∈ ℤ_P (each fibre has ≥ 2
points) and random integer μ_i ∈ [−9, 9] ∖ 0 with every fibre sum 0. They are generic: every interval sum is ≠ 0.

For each instance the scripts:
- enumerate **all** bichromatic NC trees by the S3A interval recursion;
- compute all chambers of 𝒜;
- compute each K_T as a set of chambers;
- run CP-SAT to find the minimum q with TILE(q).

`tile_p3exact.py` (P = 3) is exact in rational arithmetic, and its chamber count is checked against the Euler formula.
`tile_pgen.py` (general P) finds chambers incrementally with an LP using maximum slack. It is floating point, so its
results are [computational].

| P | m | instances | trees per instance | chambers | min ply q |
|---|---|---|---|---|---|
| 3 (exact) | 7 | 3 | 10–28 | 7–11 | 1 in 3/3 |
| 3 (exact) | 9 | 20 (12 with residues 012012012, i.e. n = 9) | 21–767 | 4–124 | **1 in 20/20** |
| 3 (exact) | 11 | 20 | 84–4514 | 21–660 | **1 in 20/20** |
| 4 (LP) | 8 | 3 | 20–70 | 8–42 | 1 in 3/3 |
| 3 (LP) | 9 | 3 | 61–369 | 24–67 | 1 in 3/3 (cross-check of the LP code) |
| 4 (LP) | 11 | 8 | 84–1248 | 46–542 (single-chamber cones: 9–46) | **1 in 8/8**; the fans use 24–85 cones |
| 4 (m = 12), 5, 6 | | not finished | | | stopped for budget (enumerating trees by LP is slow) |

Reading.
- At these sizes the full tree family always contains an exact tiling, i.e. a fan of tree cones.
- PA/poly_S3T.md found forced overlap z = 2 on training samples. That pool was a **sample** of trees. With all trees,
  small abstract instances need no overlap. The S3T observation is therefore no evidence of forced ply.
- Caveat: the true μ_k at n = 36 (|supp| = 24 or 36, P = 6) is out of exact reach. Its arrangement has about 300
  hyperplanes in ℝ⁶, and its tree count is astronomically large. These toys have 2–4 points per fibre.

## 4. Exact gap
TILE_k is OPEN.
- **(i) Lower bound.** One must exhibit, for the actual μ_k (fixed periodic support, P_N → ∞), a chamber set that
  every sub-cover hits with multiplicity P_N^{Ω(1)}. By §2 this must use the tree-cone structure beyond closures, and
  by §3 it does not already hold for generic μ with P ≤ 4, m ≤ 11 (2–4 points per fibre).
- **(ii) Construction.** One needs a rule selecting trees whose cones are pairwise disjoint (a fan) or overlap
  p_k^{O(1)}-fold, for all P_N.
  - No such rule is known.
  - The greedy rules (LAM §2(b), leftmost interval-DP) give cones that overlap. Their validity regions depend on the
    signs of intervals that are not in T.
- The data mildly favour (ii): fans exist at all small sizes tested, and they are mostly built from multi-chamber cones (P = 4: only 9–46 of the 46–713 cones are single chambers). This is not proof.

## Files
- `polynomial-ambiguity/round2/scripts/tile_p3exact.py`: exact P = 3. Run
  `.venv/bin/python …/tile_p3exact.py 20 9` (about 1 s) or `… 20 11` (about 11 s).
- `polynomial-ambiguity/round2/scripts/tile_pgen.py`: general P, LP-based. Run `… tile_pgen.py trials m P`.
- Cited: PA/poly_S2P.md §1(b), PA/poly_S2Y.md §§1, 3, PA/poly_GLAM2.md §1, PA/poly_S3V.md, PA/poly_S3T.md,
  PA/s3a_ncdp.py.
