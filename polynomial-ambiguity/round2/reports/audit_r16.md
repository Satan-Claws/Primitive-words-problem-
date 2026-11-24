# audit_r16.md — R16-B gated audit: Thm PR1s, Theorem SM, Thm PR2^β

Script: `scripts/audit_r16_dp.py` → `scripts/audit_r16_dp_out.txt` (independent exact DP, own code, C = 0).

## Verdicts
| candidate | verdict |
|---|---|
| Thm PR1s + Lemma CM + Lemma J (`r15_onesided.md`) | **SURVIVES** (minor caveats C1–C2) |
| Theorem SM (`r15_side.md`) | **SURVIVES** (caveats C3–C4) |
| Thm PR2^β + Lemma QW + Lemma Bal + Lemma ST (`r15_tails.md`) | **SURVIVES** (caveats C5–C7) |
All three remain "modulo cited Denisov–Wachtel" exactly as PR2 (survival m^{−2/3} in the 3π/4 wedge; uniform bound
P_x(τ>t) ≤ C(1+|x|)^{4/3}t^{−2/3}). No fatal flaw found.

## 1. PR1s
- **Lemma CM recomputed.** λ = √(4m log m): (λ+1)·c m^{−2/3} = O(m^{−1/6}√log m). Hoeffding for s_m (increments in
  [−1,1], range 2): P(s_m > λ) ≤ exp(−2λ²/(4m)) = m^{−2}; (m+1)m^{−2} = O(1/m). Correct. The exponent −1/6 is just
  √m (typical |s_m|) × m^{−2/3} (survival); no conditioning subtlety is needed because the truncation is crude.
- **Own DP** (m = 16…256): P·m^{2/3} = 0.3279 → 0.3316; M1·m^{1/6} = 0.393 → 0.341; E[s_m;τ>m]·m^{1/6} = 0.311 → 0.320
  (flat ⇒ true order m^{−1/6}); J(m,4m)·m^{1/6}(4m)^{1/2} = 0.347 → 0.355. Matches r15 numbers to 4 digits.
- **Lemma J**: Markov at m + skip-free reflection φ(x) ≤ (2x+1)·sup_y P(S=y) ≤ c(x+1)/√K. Correct.
- **Three-class split**: class masses (R+1), Chernoff O(1), and class 3 bound O(N^{1/6}) + O(N^{5/12}√log N) check out;
  MS-mirror ⇒ B(k) ≥ −C_V exactly for k ≤ |Vq| (n−k ≥ |pUw|). Sum Σ_{n≤N} n^{−1/2}·m^{−1/6} with m ≍ √N gives N^{5/12}. ✓
- **C1 (minor, fixable).** For m ≤ n < 4m the text bounds 2^{−n}|S_n(m)| by P(τ_{W₁} > ⌊n/2⌋), but the wedge is only
  guaranteed for k ≤ min(m, n/2). Correct bound: P(τ > min(m,⌊n/2⌋)) ≤ c(n/4)^{−2/3}; still sums to O(m^{1/3}).
- **C2.** §4 b*-shape variant is one line only (author flags it); not part of PR1s.

## 2. Theorem SM
- Step 1 identity h(Z) − D(w) = Σσ: correct (telescoping; σ ≥ 0 by substituting maximisers; σ ∈ ½ℤ).
- **Step 2 rare/frequent split — both bounds uniform.** Rare: #{trees, n_r < εn} ≤ v^{−εn}[zⁿ]y_v ≤ C(v^{−ε}/ρ′)ⁿ with
  v fixed first, ρ′ ∈ (½, ρ_v), then ε small; frequent: n_r ≥ εn ⇒ D(w) ≤ h(Y) − εn/2 ⇒ ≤ 2ⁿe^{−ε²n/2+O(1)}. Both are
  bounds on all of L(Y)_n with constants independent of n; words ≤ trees, so even unambiguity is not needed there.
- **Non-strongly-connected system.** Handled correctly: trees from Y use C* and SCCs strictly below it; Lemma Bot gives
  the lower SCCs radius > ½, so they are analytic parameters at z = ½. On C*, y_v(½) ≤ y₁(½) < ∞, strict at lhs(r) and
  then everywhere (irreducible), J₁(y₁) irreducible with ρ = 1 (forced, else IFT would make ½ regular), strict PF ⇒
  ρ(J_v(y_v)) < 1 ⇒ IFT continuation; the continuation agrees with the least fixed point (monotone limit from below),
  so Pringsheim gives ρ_v > ½. SCCs not below C* are irrelevant to L(Y). ✓
- Step 3 rebuild: path from Y to the two Y-occurrences stays in C* (both ends in C*), off-path nonterminals get zero-slack
  maximiser subtrees ⇒ h = d′ + 2h, e′ = 0. ✓
- **C3 (wording).** Step 3 produces a *new* binary form (α′,β′,γ′) with e′ = 0; it is not a contradiction with the
  hypothesis for the *original* form (for that form one only gets h + d ≤ 0). The theorem's conclusion "some binary
  form and some w₀ give e = 0" is what is proved, and is what Prop HL needs — provided Prop HL accepts any binary form
  built from C*-rules plus arbitrary expansions (check r14 Prop HL wording; I did not find a restriction).
- **C4.** Relies on r14 Lemma Bot (lower SCCs radius > ½) and Prop HL e = 0 subcase as given.

## 3. PR2^β
- **Lemma QW recomputed.** m > n/4: quadrant survival m^{−1} ≤ c m^{−1/3}n^{−2/3}. ✓ Else: in Q, A and B are independent
  (disjoint letters), Hölder E[|A_m|^{4/3};τ^A>m] ≤ (c√m)^{2/3}(m^{−1/2})^{1/3} = c m^{1/6}; × P(τ^B>m) ≤ m^{−1/2}
  ⇒ m^{−1/3}; optional stopping uses bounded overshoot (steps ±½). Phase 2 has ≥ n/4 steps ⇒ factor n^{−2/3}. ✓
- **Own DP** (both Valley wedges, inclusion–exclusion, H throughout): m^{1/3}T^{2/3}P ∈ [0.82, 0.97] for T = 256, 512,
  m = 4…64 — bounded; ≈ 2× r15's single-wedge constants (0.48–0.615), as expected.
- **Exponent bookkeeping.** Lemma Bal: ℓ_s ≥ (r/K)^{1/β_s} with r ≥ εN^β ⇒ M ≳ N^{β/β_max} = N^γ ✓. Upper bound
  Σ_{2m≤n≤N} m^{−1/3}n^{−2/3} = O(N^{(1−γ)/3}) ✓. β > (1−γ)/3 with β = 2^{−k}, γ = 2^{j−k} ⇔ 2^j > 2^k − 3 ✓:
  balanced all k ✓; (2,1): ¼ > 1/6 ✓; (2,0): ¼ = ¼ borderline ✓; k ≥ 3, j < k fails ✓.
- **Lemma ST(i) Perron argument.** Correct conclusion, imprecise write-up (C5): if ρ(M(½)) = 1 and A(½) ≠ 0 then
  wY = wA + wY forces Y(½) = ∞ outright (no finite solution), so B(½) = ∞ — stronger than μ = ∞; the "w(I−M)μ = 0, wA > 0"
  line should read w(A′ + M′Y) > 0 after differentiating. Either way finite-μ blocks have no ρ = 1 linear SCC below.
- **C6.** Lemma Bal needs two-sided tail regularity of the token side-length (mixture ⇒ min exponent) — cited "standard,
  not written out". Also β_s := 1 for exponential sides is a convention that works only via the Chernoff branch.
- **C7.** PR2^β needs a U-level *and* a V-level block (constant C); the log-level variant (Valley_{C+c log n}) is not treated.

## Bottom line
No fatal flaw. PR1s, SM, PR2^β stand as [written proof modulo cited DW], with fixes C1 (bound for m ≤ n < 4m), C3
(state SM's conclusion as "a binary form with e = 0 exists"), C5 (ST(i) write-up). T8_unamb gap = unbalanced two-tape
(R16-A) unchanged.
