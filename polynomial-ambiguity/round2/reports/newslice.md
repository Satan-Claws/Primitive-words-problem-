# R2/newslice: is there a slice family where the transport tiling fails?

Status: **NO NEW CANDIDATE.** All four variants (a)–(d) reduce, at the cone/ply level, to the S_N product
geometry. That geometry is already handled by tile2 Thm B plus S2P patching, modulo Lemma C. Nothing new is
blocked beyond what tile2 already claims, and nothing is unblocked.
- §1, §2, §3(b) and §3(c): [written proof, short].
- §3(a), and the checks in §3(c): [computational, exact certificates].
- §4: [assessment].

Notation is as in prompt §4.3–4.4, poly_T1 P4, poly_T2a, poly_LAM §2 and R2/tile2.
- V_p is the space of (n/p)-periodic vectors.
- Fourier *type* of a frequency f ∈ ℤ_n: S(f) := {k : p_k | f}.
- Ŵ_S is the span of the characters of type S. Then V_{p_k} = ⊕_{S∋k} Ŵ_S and W_n = ⊕_{S≠∅} Ŵ_S.

## 1. The local primitive region of ANY DFA sub-slice [written proof]
Let D be a DFA and n fixed.
- The exponent set of L(D) ∩ (ab*)ⁿ is a finite union, over state sequences, of products ∏_i A_i of
  ultimately periodic sets A_i ⊆ ℕ. Its asymptotic directions are therefore coordinate subspaces ℝ^J: block i
  is free (i ∈ J) or bounded.
- **A DFA cannot impose a non-coordinate linear relation among unbounded exponents.** Congruences change only
  lattices, which is the G3** side.
- Fix a base direction ω ∈ ℝ^J_{≥0}, put A(ω) := {p : ω ∈ V_p}, and take |δ| ≪ t. Then
  tω + c + δ ∈ V_p ⇔ p ∈ A(ω) and c + δ ∈ V_p.
  - Here c is the vector of fixed (bounded) coordinates.
  - If ω ∉ V_p, then tω + c + δ ∉ V_p for t large.
- So the local primitive region is always

  **R_loc = ℝ^J ∖ ∪_{p∈A(ω)} (V_p ∩ (−c + ℝ^J))**, the complement of at most ω(n) affine subspaces.

- In type language, with J = [n] and c = 0: δ ∈ W_n is primitive near U iff the *present types*
  𝒫(δ) := {S : δ_S ≠ 0} satisfy ∩𝒫(δ) = ∅, where δ_S is the component in Ŵ_S.

## 2. Convex level and variant (d): always polynomial, and S_N's E_k is the maximal product [written proof]
**Lemma VC-gen.** For any subspace R and any subspaces {V_p}_{p∈A}, the complement R ∖ ∪V_p has a cover by
pieces ∩_p{ψ_p > 0}, with ψ_p ∈ (R/V_p∩R)*, of ply O(|A| log|A| · Σ_p codim_R(V_p ∩ R)).
- Proof: this is T2a §2 verbatim. With ψ_p independent and uniform on spheres, Pr[ψ_p(x) > 0 ∀p] = 2^{−|A|}
  exactly for every x in the region.
- Consequence for (c) and (d): non-product regions, and defects seen by two primes at once, can never give a
  convex obstruction. Only laminarity can, exactly as for S_N.

**Facet economy.** A facet μ ⊥ Σ_{k∈K} V_{p_k} serves every prime in K. At δ it is usable iff some present type
S has S ∩ K = ∅. So a piece through δ can use

  τ(δ) := min #{sub-family of 𝒫(δ) with empty intersection}

facets. τ(δ) = N forces every present type to have |S| ≥ N − 1, that is, δ ∈ ⊕_k E_k (E_k = Ŵ_{[N]∖k}).
- Low-type defects, for example δ = 1_{O_1} + 1_{O_2} with O_j an orbit of shift n/p_j, give τ = 2. They are
  2-prime problems, polynomial by the n = pq-type bounds.
- Types of size N − r give τ ≥ N/r factors, with the same fibre count u = n/rad(n) for narrow-facet localisation
  (LAM §1). The best narrow-facet lower bound is then (u/2s)^{N/r}, which is weaker than S_N.
- So **variant (d) only lowers the number of independent factors.** The E_k region of S_N is already the
  extremal product.
- Covering W_n ∖ W by families indexed by the facet prime-sets {K_i} (set covers of [N]) costs a factor at most
  Bell(N) ≤ N^N = n^{1/2+o(1)} [assessment]. That is polynomial.

## 3. Variants (a), (b), (c)
**(a) Deeper prime powers, n = ∏ p_k^{a_k}.**
- Primitivity involves only the maximal divisors n/p. There is no "every level" condition, so deeper exponents
  only enlarge the fibres u = n/rad(n).
- The structure is identical to S_N:
  - g_k = u·p_k;
  - E_k = Ŵ_{[N]∖k}, of dimension u(p_k − 1);
  - μ_k = (1 − T^{n/p_k}) ∏_{j≠k} (1 − T^{g_j}) ν_k, with ν_k on a window of length g_k.
- Clusters have width ≈ nΣp_j/rad(n), which is much smaller than the nesting gaps n/(p_k p_{k+1}) once
  rad(n) ≫ N p_N³. So LAM §2(c) Russian-doll assembly survives.
- Computational check [exact, random-integer-ν certificate; `newslice_check.py`]:
  - μ_k ⊥ V_{p_k}, U and the period-g_j vectors (j ≠ k) for every case.
  - **0 W-balanced arcs** (the Lemma C analogue, Thm B hypothesis) for every k at (N, a) = (2,2), (2,3), (2,4),
    (3,2), (3,3), up to n = 27000 with |supp| up to 18000.
  - Transport rule at x-level points: spanning, non-crossing, valid trees in every sample (12/12 for N = 2,
    a = 2, 3; 4/4 for N = 3, a = 2), with 0 pairwise ply violations.
- Large a_k is still S_N-type, so tile2 blocks it.

**(b) Lower strata.**
- Inside U every ω has A(ω) = all primes, so R_loc is the same for P_N/p-periodic ω as for generic ω.
- Thm B's coverage hypothesis is about W, not about ω: "μ|_I ⊥ W". So it is ω-independent and applies verbatim
  at every ω ∈ U_{>0}.
- ω-level balanced arcs, which are more numerous on smaller strata, are irrelevant (tile2 §3).
- If ω ∉ U, then A(ω) ⊊ [N] and the problem is a product with fewer factors.
- Boundary ω (zero coordinates) is the fixed-coordinate case (c).

**(c) DFA sub-slices.**
- By §1, only coordinate restrictions ℝ^J are possible. Positivity of ω on J with ω ∈ ∩_{p∈A}V_p forces J to be
  a union of fibres F′ (orbits mod u).
- Taking ν_k supported on J keeps μ_k inside J, because every shift is a multiple of u. The problem is then S_N
  on |F′| fibres.
- Check (half of the fibres, n = 216 and 900): orthogonality holds, 0 W-balanced arcs, and the rule gives a
  valid ply-1 tree in every sample.
- |F′| = 1 is the squarefree-type slice on P_N blocks, which is capped at about linear.
- **Key structural fact:** a balanced arc means μ|_I ⊥ span(region). A coordinate restriction never forces this
  for a generically chosen admissible μ. Each arc condition is a proper linear condition on the large affine
  space of admissible μ with a given support class. So **no DFA slice can break tile2's coverage hypothesis.**

## 4. Exact gap
A new negative candidate within slices would need one of the following.
- (G-C⁻) For a positive-measure set of u_k, *every* admissible μ_k with nestable support has a W-balanced proper
  arc. By §3(c) this is generically false; it would need a forced arc, and none exists in any family tested.
  The live question is still only Lemma C (some choice works) for all N.
- A non-laminar or non-pair source, outside Lemma 3P. Excluded by Structure (c).
- The length side G3**, which is untouched here.

What remains open is not geometric:
- Lemma C for all N (and for deep powers);
- realisability of the Bell(N)-indexed family on W_n ∖ W as one grammar;
- G3**.

## Files
- `polynomial-ambiguity/round2/scripts/newslice_check.py`: deep powers and fibre-restricted sub-slices. It checks
  orthogonality, W-balanced arcs (exact certificate) and the transport rule. Run time about 1 min.
