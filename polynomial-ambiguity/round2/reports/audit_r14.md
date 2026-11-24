# audit_r14.md — R14-A: gated audit of r13_padding.md (Thm PR1, Thm PR2, Lemmas MS/V/K/R)

**Verdict: SURVIVES (with caveats).** No fatal flaw found. PR1 and PR2 hold as stated, under their hypotheses
(level blocks + (T½), and for PR2 the cited Denisov–Wachtel bound). T8_unamb is still OPEN, as r13 itself says.

Script: `scripts/audit_r14_wedge.py` → `scripts/audit_r14_wedge_out.txt` (independent exact DP, m ≤ 1024).

## Checks
1. **Lemma MS (lag freedom).** The lower blocks are independent nonterminals in C-rules. So, by substitution closure, any
   block word can be put into a fixed closed path ρ at X. Loops at X concatenate in any order, and a rule of the SCC lies
   on some X-cycle. Prepending ρ gives W' = p U_ρ U_W w V_W V_ρ q, since V reads from the outside in.
   - A(k') = P_W(k) + P(U_ρ).
   - The suffix of length k' ≤ L lies in (tail of x)·(fixed letters of ρ right of x)·q, so B(k') ≤ K + β.
   - n' ≥ |W| + L ≥ 2k' once L is large.
   The bound is per word: it holds for every W ∈ L, with a constant that depends only on ρ. The finite-state coupling
   only limits which rules follow which. It does not tie block lengths across the two tapes, so the lag really is free.
   The mirror case and the one-tape version (put ρ last and then first, giving max P ≤ min(0, P(n)) + C) check out.
   Lemma V follows: max P ≤ max(C_U, P(n) + C_V) + O(|w|).
2. **Lemma K.**
   - For k ≤ n/2, the prefix letters and the suffix letters are disjoint. So (A, B) is a free walk with no endpoint
     conditioning, and the density |G⁻_n ∩ Valley|/2ⁿ is a survival probability, not a local one. Using the exponent
     for survival is therefore correct.
   - The steps (±½, ±½) are i.i.d. uniform with covariance ¼·I, so the walk is isotropic and uncorrelated. In the
     rotated coordinates s = (B−A)/2, t = (A+B)/2 it is exactly simple random walk on ℤ².
   - W₁ = {s > 0, B ≥ −C} has its vertex at (−C, −C). Its boundary rays run along the directions π/4 and π, so the
     opening is 3π/4.
   - The Denisov–Wachtel survival exponent is p/2 with p = π/θ, so π/(2θ) = 2/3.
   - The DP (C = 0) gives local exponents −0.658, −0.663, −0.665, −0.666, −0.6662, −0.6664. Also m^{2/3}·P(W₁) =
     0.3299 → 0.3318, which is stable. At C = 3 the exponents −0.51 → −0.651 approach −2/3 slowly, as a finite-offset
     effect should. W₂ is identical to W₁ by symmetry. The half-plane exponent is −0.4998.
3. **Lemma R and the squeeze.**
   - Wald with truncation is correct: S'_τ ≥ x, because either X_τ > x or all terms are ≤ x.
   - Under (T½), m(x) = O(√x), so U(x) ≥ c√x.
   - Injectivity gives mass ≥ 2^{−|pwq|}·U(N − |pwq|). Each word has weight 2^{−|W|} and the token weights multiply.
   - The comparison is c√N against Σ n^{−2/3} = O(N^{1/3}). This is consistent with (2), because both sides use
     survival-type densities.
   - Sanity check: G⁻ alone has density n^{−1/2}, which gives mass √N, so there is no contradiction without the valley.
     That matches No-go 3.
4. **Multiplicity corollary.** If multiplicity ≤ c·n^{1/6−ε}, the word mass is ≥ c√N/N^{1/6−ε} = N^{1/3+ε}, which
   contradicts O(N^{1/3}). This is valid. It needs no injectivity anywhere else, because MS, V and K use only L ⊆ G⁻.
   "On average" in the status table should be read as the ratio (sequence mass)/(word mass) ≳ N^{1/6}.
5. **Scope and No-go 3.** No-go 3 has no lower blocks at all (its tokens are single letter pairs), so it has no level block
   and PR2 correctly does not apply. PR2 does **not** cover T8_unamb.

## Caveats (non-fatal)
- C1. The line "all level-padded classes excluded" in the Status table overstates the result. The one-sided case
  (a level block on one tape only) is a sketch (§5). Its step 3, the conditional first-moment bound m^{−1/6}, is unverified.
- C2. The (T½) remark "excludes only exponents −1−1/2^k, k ≥ 2" relies on the dyadic-exponent theorem for ℕ-algebraic
  series (Banderier–Drmota). It should be cited. Heavier tails and steep models stay open (§6), as r13 says.
- C3. PR2 depends on the DW upper bound for a lattice walk started at the vertex region. This is standard (DW 2015,
  Thm 1, isotropic, bounded steps), and the DP confirms it to m = 1024 with a stable constant. A self-contained proof would
  be better, for example a Lyapunov or harmonic-function supermartingale built from r^{2/3}·sin(2φ/3).
- C4. Lemma R's tail bound sketches "ρ(M restricted to C∖X) < 1 ⇒ geometric number of steps". Make it explicit that this
  is evaluated at weight ½ per letter, with the lower blocks summed at their finite μ.
