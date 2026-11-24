# construct36: explicit low-ply laminar cover of Q ∩ (ab*)^36 (S_2), constructive side

Scripts are in `R2/../scripts/`:
- `construct36_core.py`: enumeration of primitive W_36 ∩ ℕ^36 up to D_36, plus vectorised k ≤ 2 dominance and transfer coverage. It reuses `construct_atoms.py` and `construct2_transfer.py` with n = 36, primes (2,3), A = {2:18, 3:12}.
- `construct36_cover.py N`: exhaustive coverage up to norm N.
- `construct36_family.py N`: the explicit families F36 and F36*, their validity, random and structured tests, ply, and the ILP subfamily.

Order and atoms are those of `R2/construct.md` §1. A system is either one atom with C ⊇ {2,3}, or two atoms with disjoint supports, mutually non-crossing pair sets, and C₁ ∪ C₂ ⊇ {2,3}. For norm ≤ 8, the vectorised search was checked against the original `construct2_transfer.find_systems` path, with 0 mismatches over all classes. Every returned system was re-validated with `construct_atoms` predicates.

## 0. Verdict
- **Coverage [computational].** k ≤ 2 chord-dominance systems cover every primitive x ∈ W_36 ∩ ℕ^36 with ‖x‖₁ ≤ 16. That is 4 595 724 points in 64 634 D_36 classes. No transfer atoms are needed, and no k = 3 atoms are needed. No uncovered vector exists in that range, so there is no obstruction lemma to extract.
- **Proof [written proof].** Lemma 36 (§2) proves coverage of all of E ∩ W_36 by an explicit family F36* of **72 systems**, each of ply 1:
  - 12 fibre rectangles;
  - 60 cross-fibre chord pairs.
- **Ply of the full cover.** Add T1-P1 off W (φ(36) = 12 forms). The cover of Q ∩ (ab*)^36 then has **ply ≤ 72 + 12 = 84 = 2n + φ(n)**. The bound 72 is attained on W at generic points (computational).
- **Answer to the construct2 §5 assessment.** The disjoint-witness-fibre configurations do *not* need transfer atoms. Two single-chord atoms in different fibres are always compatible for a suitable choice of diameter. The rectangle family's p²q failure is a failure of that family only, as at n = 12.

## 1. Coverage table [computational]
| test set | points (classes) | dom k ≤ 2 | + transfer | uncovered |
|---|---|---|---|---|
| exhaustive primitive W_36 ∩ ℕ^36, ‖x‖₁ ≤ 8 | 3 564 (59) | 59 | — | 0 |
| same, ‖x‖₁ ≤ 10 | 29 484 (458) | 458 | — | 0 |
| same, ‖x‖₁ ≤ 12 | 188 208 (2 727) | 2 727 | — | 0 |
| same, ‖x‖₁ ≤ 14 | 1 001 484 (14 279) | 14 279 | — | 0 |
| same, ‖x‖₁ ≤ 16 | 4 595 724 (64 634) | 64 634 | — | 0 |
| random general W_36 points (fibrewise polygon sums, multiplicities 0..9) | 3 000 | F36* covers all | — | 0 |
| A2 product region x = B + e₂ + e₃, B ≤ 60, \|pert\| ≤ 3, disjoint witness fibres | 3 000 | F36* covers all | — | 0 |
| same, arbitrary witness fibres | 3 000 | F36* covers all | — | 0 |
| product region, B ≤ 1000, \|pert\| ≤ 40, disjoint fibres | 2 000 | F36* covers all | — | 0 |
| fresh seed (B ≤ 200) + structured: one α-fibre r, one β-fibre r′ with a zero-difference class, all 30 (r,r′) | 4 720 | F36* covers all | — | 0 |

Norm ≤ 4 contains no primitive point; the minimum norm is 5 (a 2-gon plus a 3-gon). The enumeration uses Φ_36(z) = Φ_6(z⁶), so x ∈ W_36 ⇔ every fibre restriction y_r = (x_{r+6t})_{t∈ℤ_6} lies in W_6, where fibre r is the class r mod 6.

## 2. Lemma 36 and its cover [written proof]

**Fibres and witnesses.** Index the fibre r = class mod 6 by t ∈ ℤ_6 via position r + 6t. Then:
- the shift n/2 = 18 acts on t as t + 3;
- the shift n/3 = 12 acts on t as t + 2.

So x ∉ V_2 iff some y_r is not (t+3)-invariant; call such r a **2-fibre**. Likewise x ∉ V_3 iff some y_r is not (t+2)-invariant; call such r a **3-fibre**. Every 2-witness chord {i, i+18} and every 3-witness chord {i, i+12} lies inside one fibre (A2).

**Family F36\*.**
- (R) For each fibre r and each c ∈ {0,1}, take the lifted n = 6 rectangle R_c: chords {c, c+5} and {c+3, c+2} in fibre indices, i.e. positions r + 6t. Note R_i = R_{i+3} in ℤ_6, so there are only 3 distinct rectangles per fibre; we keep 2. This gives 12 single atoms.
- (X) For each ordered pair r ≠ r′ and each t ∈ {0,1}:
  - the 3-chord κ = {r′+6t, r′+6(t+2)} in fibre r′;
  - the unique diameter δ = {r+6s, r+6s+18} of fibre r that does not cross κ.

  This gives 60 two-atom systems.

All members are k ≤ 2 dominance systems from `R2/construct.md` §1. Each is therefore a ply-1 union of exact laminar pieces with 0/1 ring vectors of support ≤ 2. Validity was checked by `construct36_family.py`: certified primes, disjoint supports, and non-crossing pair sets.

**Lemma 36.** Every x ∈ E ∩ W_36 (primitive, i.e. x ∉ V_2 ∪ V_3) lies in the region of some member of F36*.

*Proof.* There is at least one 2-fibre and at least one 3-fibre.

**Case (a): some fibre r is both a 2-fibre and a 3-fibre.** Then y_r ∈ W_6 is primitive at n = 6.
1. Write y_r = a + b with a 3-periodic and b 2-periodic, as in `R2/construct.md` §2 with A = 3, B = 2.
2. For the rectangle R_i: w + u = 2(b_{i+3} − b_i) and w − u = 2(a_{i+2} − a_i).
3. b is non-constant and 2-periodic, so b_{i+3} = b_{i+1} ≠ b_i for every i.
4. a is non-constant and 3-periodic, and t ↦ t+2 is a 3-cycle on ℤ_3. So a_{i+2} ≠ a_i for at least two of the three classes i mod 3.
5. Hence for some c ∈ {0,1} we have w ± u ≠ 0, so |u| ≠ |w|, and the k = 2 atom R_c (any dominant is allowed) holds.
6. Its two signed forms are balanced mod 3 and mod 2 in fibre indices, which means mod 18 and mod 12 in positions. So R_c certifies {2,3}.

**Case (b): no fibre is both.** Take a 2-fibre r and a 3-fibre r′ with r ≠ r′.
1. y_r is (t+2)-invariant, so y_r(t) = γ + α(−1)^t with α ≠ 0. Every diameter of fibre r is then a 2-witness: y_r(t) − y_r(t+3) = 2α(−1)^t ≠ 0.
2. y_{r′} is (t+3)-invariant and non-constant, so y_{r′}(t) = β_{t mod 3}. The chord κ_t = {t, t+2} has difference β_{t+2} − β_t, which depends only on t mod 3. This difference is nonzero for at least two of the three classes. So κ_0 or κ_1 is a 3-witness; call it κ.
3. The short arc of κ (12 steps) contains exactly two points of fibre r, and they are consecutive in t: r+6s and r+6s+6. These two diameters cross κ. The third diameter, s+2 mod 3, has both endpoints on the long arc, so it does not cross κ.
4. That non-crossing diameter is a witness by step 1. Its endpoints are disjoint from κ because r ≠ r′.
5. So the X-member for (r, r′, t) holds, with d ≠ 0 on both chords, and certifies {2} ∪ {3}. ∎

**Ply.**
- On W, ply ≤ |F36*| = 72, since each member contributes ≤ 1. The value 72 is attained: the maximum observed on random general W points is 72.
- Off W, T1-P1 adds ≤ φ(36) = 12. P1 regions are {L ≠ 0} for L ∈ W^⊥, so they are disjoint from W.
- Total ply ≤ 84.
- The pieces have K = 2, ‖c‖₁ ≤ 3, and are unimodular. The slice-to-grammar converse (`R2/realise.md` §3, sketch/assessment) would turn this into a grammar fragment for Q ∩ (ab*)^36 of ambiguity ≤ 84. That step is not checked here.

## 3. Ply numbers [computational]
| family | size | ply on exhaustive ‖x‖₁ ≤ 16 (min/mean/max) | ply on random general W | ply on product, disjoint fibres |
|---|---|---|---|---|
| F36 (all 18 distinct fibre rectangles + all 180 cross pairs) | 198 | 2 / 18.9 / 38 | 54 / 164.2 / **198** | max 54 |
| **F36\*** (Lemma 36) | **72** | 1 / 5.9 / 12 | 18 / 59.6 / **72** | max 18 |
| all k ≤ 2 dom systems (no selection), ‖x‖₁ ≤ 8 | — | 2 / 252.6 / 384 | — | — |
| ILP minimum-size subfamily of F36 fitted to the test set | 48 | — | — | — |

The 48-member ILP family is **not** a cover. On the fresh-seed and structured set it misses 88 points; with the norm-12 tuning it missed 118. As at n = 30, test-tuned greedy and ILP families overfit, and only F36* is certified.

Under D_36, F36 splits into 4 orbits: 18 rectangles, 72 + 72 cross pairs, and 36. The D_36-invariant minimum over these orbits is all of F36, with max ply 198. F36* is not D_36-invariant (it uses c, t ∈ {0,1}); its D_36-symmetrisation is F36. No minimality is claimed for 72.

Comparison with A2 (`PA/poly_A2.md` §1), whose model allows one chord per prime and no rectangles:
- A2 left all 72 common-fibre vectors uncovered. Here they are case (a), covered by fibre rectangles.
- A2's covered-point ply was ≈ 5·m₂·m₃ ≤ 180. On the product region with disjoint fibres, F36* has ply ≤ 18; the F36 maximum of 54 is consistent with the m₂·m₃ product structure.

## 4. Consequences and limits
- **S_2 admits an explicit low-ply cover of the whole slice, not only near U [written proof].** The cover consists of chord-dominance pieces with ply ≤ 2n + φ(n). This is consistent with, and stronger on this one slice than, the pair-facet result of `R2/realise.md`, which covers the near-U region abstractly with ply_VC ≤ n^{1+o(1)}. It closes open item (d) of the registry for n = 36.
- **No new atom type is needed at n = 36.** Transfer atoms and two-level transfers are unnecessary. Lemma O and FT-type phenomena do not arise, because in case (b) the witnesses live in *different* fibres, where single chords can always be made non-crossing.
- **Where this stops [assessment].** For n = P_N² with N ≥ 3, case (b) needs one system per tuple of pairwise distinct witness fibres (r_1, …, r_N). The analogue of F36* then has ~P^N = n^{N/2} members, all holding at generic product points. This is exactly the multiplicative ply of A2 and of LAM's (P/2s)^N bound for facets touching ≤ s fibres (prompt §4.4 (a)). At N = 2 that bound is O(1), which is why S_2 is easy. So S_2 carries no evidence either way on the S_N question. The first informative slice is S_3 (n = 900), and there the single-fibre chord mechanism is provably multiplicative. Lemma 36 does not extend.
- **Not checked.** n = p²q² for other (p,q), e.g. n = 100. In case (b) a p-only fibre is then p-periodic in fibre index with witness chords {t, t+q}, and not all chords need be witnesses, so step 3 of case (b) needs a counting argument that was not done.
