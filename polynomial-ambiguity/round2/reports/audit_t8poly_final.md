# audit_t8poly_final.md — gated final audit of T8_poly (r19_fixes §1–4 + interface to r19_m1)

**Verdict: COMPLETE (with caveats).** No fatal flaw found. The new repairs (Lemma NS, PD, W, the bottom-up induction,
Thm GE⁻-NS, Prop OS, Lemma SP) check out. The case table is exhaustive at the level of the stated criteria. Every row
cites a result whose hypotheses hold, and the summation is o(2ⁿ) uniformly for n ≥ n₀(G). The (M1/M1′) hypothesis of
§4 is exactly what r19_m1 Thms M1/M1′ deliver; audit_m1 (REGISTRY R19) says these SURVIVE.

So T8_poly is complete modulo the inherited caveats: A1 (LG(c)/SM+HL citation), the LL audit caveats, and the
audit_m1 caveats. Caveats C1–C4 below are presentational or local fixes; none of them changes a row.

Script: `scripts/audit_t8pf_search.py` → `scripts/audit_t8pf_search_out.txt` (6 seeds × 10⁴ random grammars, ~3 min each).

## 1. New lemmas
- **Lemma NS ✓.**
  - Pumped word W′ = W[0,a)σsᵐσ′W[a,b)τ′tᵐτW[b,n) ∈ L by grafting.
  - k₀ = a + |σsᵐσ′| = O(√n log n) ≤ n/2 ≤ n′/2.
  - The suffix of length k₀ is untouched because k₀ ≤ n − b. Since b ≤ n/4, this holds with room to spare.
  - A_{W′}(k₀) ≥ −h − c + m > C_W − h ≥ B_{W′}(k₀).
  - Remark: only B_W(j) for j = O(√n log n) is used (see C1).
- **Lemma PD ✓.** Close the path with a fixed path; NC on the closed cycle gives D(s) ≤ c_K.
- **Lemma W ✓.**
  - Long-block count: ℓ·Σ_{j≥L} C₁z₁^{−j}2^{ℓ−j}.
  - Short blocks: rise ≤ (tail of block p) + D(middle) + (head of block q) ≤ 2L + c_K.
  - Bounded-rise walk count: the transfer matrix on r = P − runmin ∈ [0, R] is the path with a loop at 0, so
    ρ_R = 2cos(π/(2R+3)).
  - With L = ℓ^{1/3}, both terms are exp(−Θ(ℓ^{1/3})).
- **Induction (Step 1 ↔ Step 2) ✓**, with caveats C1 and C3.
  - Critical nonlinear K is not in G_bad (LG(c)).
  - Critical linear K with light blocks: in the λ > 0 case, NS gives NC and Lemma W gives
    #words ≤ m²2ᵐe^{−c(λm/2)^{1/3}}, against ≥ c2ᵐ trees, minus Cramér's exponentially few. Some word then has
    e^{Ω(m^{1/3})} trees. This is super-polynomial in n once m ≥ log⁴n, and m ≤ n/4 may be chosen.
  - The λ = 0 case (pure-right K): pumping gives D(t) ≤ 0. If E D(t) < 0, concentration gives the contradiction. If
    D(t) ≡ 0, the word count is ≤ c2ᵐ/√m while words = trees ≥ c2ᵐ. Both cases hold; neither uses C_W.
- **Thm GE⁻-NS ✓.**
  - The skeleton has ≤ (h+1)^{4c₁} = polylog choices.
  - One non-spanning factor has length ℓ ≥ h/(8c₁).
  - Gain: exp(−c(log⁴n/8c₁)^{1/3}) = exp(−Θ(log^{4/3}n)), which beats n·polylog.
  - Left siblings of π_h lie in [0, h), so there are no partial blocks.
- **Prop OS ✓.**
  - (a) Pure-left means τ = τ′ = t = ε. With D(s) ≥ 0, depth(σsⁱσ′) ≤ |σ| + |s| + |σ′|, which gives a U-level x with
    v = ε. That is the definition of left-good (r18_gend §1).
  - (b) D is an integer, so "no cycle with D ≥ 0" is NC. Heavy left parts go to Lemma SP + LG(c).
- **Lemma SP ✓.**
  - A lowest radius-½ linear C\* is critical with light tokens. The renewal gives ≥ c2ʲ on a progression.
  - Pumping r = εN copies with independent H-trees gives 2ᴺ·[c2^{−c₁}/(2εd)]^{εN}, which is exponential ambiguity.
  - Corollary (iii): for nonlinear T, SP is applied to H = Z₂ ∈ T. If C\* = T, then T is critical nonlinear. Either
    way LG(c) applies.

## 2. Exhaustiveness of the table
Every bad-left word with C_W ≤ √n log n splits its h/2 letters into the non-spanning part (row 2) and the spanning part
(row 3). Row 3's tree, for a spanning SCC T:

| T | condition | row |
|---|---|---|
| nonlinear | radius ½ | 3a |
| nonlinear | light, NC | 3c |
| nonlinear | light, not NC | 3h |
| linear | heavy left | 3b |
| linear | NC | 3c |
| linear | not NC, pure-left | 3e |
| linear | not NC, pure-right | no letters in [0, h) |
| linear | not NC, heavy right | impossible: RH (gend2 §0 / SP (i)) ⇒ NC (Prop NC is grammar-level, any ρ) |
| linear | not NC, light two-sided, critical | impossible: Thm LL, two-sided = π(u ≠ ε), π(v ≠ ε) > 0 |
| linear | not NC, light two-sided, non-critical | 3g |

The tree is a complete case split. The only content lies in the two "impossible" cells, and both cite audited results.

**Computational search.** Random reduced, ε-free, unit-free CFGs with 2–4 nonterminals were filtered as follows:
- L ⊆ G⁻ for all n ≤ 13;
- amb ≤ n²/2 for every nonterminal;
- tree growth ≤ 2.03.

About 2300 grammars survived. Each recursive SCC was then classified by the table's criteria: radius and ρ(M(½)) from
tree-count GFs truncated at length 70, and NC from max-drift cycle closure.

| result | count |
|---|---|
| SCCs in the two "impossible" cells | **0** |
| 3c | ≈ 1170 |
| 3h | ≈ 870 |
| 3a | ≈ 200 |
| 3e | 26 |
| 3g | 12 |
| 3b | 7 |

Random grammars rarely produce critical linear SCCs. For that cell, the exhaustive token search of audit_ll is the
relevant evidence.

## 3. Hypotheses of the cited results
- **h.**
  - Lemma W needs h^{1/3} ≫ log n, and h = log⁴n gives log^{4/3}n.
  - TS (rows 3g/3h) gains e^{−θh/c}, which is enough for any h ≫ log n.
  - Prop NC/NC′ and gend2 are already stated at h = log⁴n.
  - Row 1 needs FR-pos/T-tol with C′ = O(log⁴n) = o(√n) and h log n = o(n). audit_t8poly checked this.
  - No row still uses K log n.
- **M1 interface ✓.**
  - §4 needs: bad-left words with ≥ h/(4N_SCC) letters of [0, h) that are left letters of spanning nodes of one SCC T,
    where T is (M1) linear, non-critical, two-sided, with light/finite sides, or (M1′) nonlinear and light. These
    words must have rotation image o(2ⁿ).
  - The spanning part of T's π_h-segment is one downward T-path. An SCC occurs in at most one maximal segment of a
    root path. Its left letters are exactly the left-sibling yields of that path.
  - r19_m1 Thm M1 (TS with 𝓑 = all trees, a = h/(4N_SCC)) covers every non-critical linear T with light/finite
    left material. Thm M1′ covers light nonlinear T. Both give poly(n)·2ⁿ·e^{−θh/c}.
  - The hypotheses match, and TS covers more than §4 needs: it does not use D(s) ≥ 1, two-sidedness, or left-badness.
  - Non-critical means ρ(M_T(½)) < 1 in r19_m1, and tree radius > ½ in r19_fixes. These agree for linear T with
    light/finite sides.
- **Row 0.** By the reflection principle, P(max_{j≤n/2} B(j) > √n log n − h) ≤ 2e^{−(1−o(1))log²n}.

## 4. Summation
|Rot(L)_n| ≤ O(log⁴n/√n)·2ⁿ [row 1] + n·2ⁿ·e^{−(1−o(1))log²n} [row 0]
+ n·polylog·2ⁿ·(e^{−cΘ(log^{4/3}n)} + n^{O(1)}e^{−θlog⁴n/c}) [rows 2–4, finitely many].

Every bound holds for every n ≥ n₀(G), so |Rot(L)_n| = o(2ⁿ) uniformly. Each bad set is o(2ⁿ/n) before the rotation
factor n. So L is not rotation-dense for any large n, which covers both the "all large n" and the "infinitely many n"
readings.

## 5. Caveats (non-fatal)
- **C1. The induction applies NS to the replaced word W′, but C_{W′} is not controlled.** C_{W′} involves B_{W′}(j)
  for j ≤ n′/2, which can read past W's last n/2 letters.
  - Fix: NS only uses B(k₀) with k₀ = O(√n log n). Either restate NS with C_W^{loc} := max_{j≤3√n log n}B(j) + h, or
    take m = log⁶n in Step 2, so that n′ = n ± polylog.
- **C2. Row 3's pigeonhole omits (S)-factors at spanning between-SCC steps.**
  - These are all-bad left-sibling trees inside [0, h), so they are light by the induction and killed exactly as in
    GE⁻-NS step 2.
  - Row 3 should read "spanning segments ≥ h/4, or (S)-factors ≥ h/4". This agrees with audit_m1's note "S-factors
    stay with U2/U4".
- **C3. The induction's conclusion should be scoped.** "Every G_bad tree language has radius > ½" is proved only for
  SCCs that occur inside [0, h) of some counted word, because Step 2 needs such an occurrence. That is all Lemma W
  and GE⁻-NS use.
- **C4. Rows 3c/3e partly duplicate TS.** TS already kills every non-critical spanning T. Only critical linear T
  really need Lemma W or Prop OS. This is harmless.
- **Inherited.**
  - A1: the LG(c) citation of SM/HL, and Lemma RP's §0 citation in Prop NC.
  - LL caveats 1–3, for row 3f.
  - audit_m1 caveats: the exponent is n^{2k+4}, and D(i) needs ρ > 1 strictly.
