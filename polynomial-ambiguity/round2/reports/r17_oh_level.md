# r17_oh_level.md — R17b-C: one-sided heavy models via levelness of the heavy block

Status: **one-sided heavy models are CLOSED** for every tail exponent β₀ ∈ (0, 1) [written proof; inputs are r14 Lemma
Bot / Prop HL / Lemma PC, r15 Theorem SM (in the audited C3 form), r16 Lemma MS⁺(b), r13 Lemma R, and the Banderier–Drmota
exponent classification (cited, as in PR2⁺)]. **No Denisov–Wachtel input is needed.**

Route taken: route (a) ("absorb the light V tape"), made rigorous through one new deterministic lemma (MS^in). The
key observation is a strengthening of the "levelness" input: by SM + HL, **every heavy block is both U-(log-)level and
V-(log-)level**. So the heavy block on the U tape can also be used as a *V-level* word, inserted as the **innermost**
token. This freezes the suffix walk B while it crosses the inserted word, and thereby puts an upper barrier on the
U-prefix walk A at height max_{j≤|Vq|} B(j). The light V tape only costs a barrier of height ≍ √|V|, and |V| ≲ n^γ
with γ slightly above β₀ except on a set of pair mass O(1).

Script: `scripts/r17_oh_level_checks.py` → `scripts/r17_oh_level_checks_out.txt`.

## 0. Setting
As in r15_onesided §0 / r16 §1: critical linear SCC C, X ∈ C, S ⇒* pXq, exit X ⇒* w; first-return loops give i.i.d.
tokens (u, v) with law π, Σπ = 1; W = p U w V q with U = u₁⋯u_r, V = v_r⋯v₁; n = |W|; A(k) = P(k),
B(k) = P(n) − P(n−k); W ∈ G⁻ ⟺ A(k) < B(k) for 1 ≤ k ≤ n/2. Put m(W) := |Vq|.

**One-sided heavy case.** Some C-rule carries a heavy block (Cor H sense: μ < ∞, infinite mean) on the U side; no
C-rule carries a heavy block on the V side; π(v ≠ ε) = q_V ≥ 0 arbitrary (q_V > 0 is the open case; q_V = 0 is also
covered). β₀ := 2^{−k_max} is the tail exponent of the loop length: by B–D Thm 3 every lower block has coefficients
≍ n^{−1−2^{−k}} on residue classes or is exponentially small, so F̄(y) = O(y^{−β₀}) (r16 PR2⁺ step 1), and the
heaviest block, which sits on the U side, gives the matching lower bound P(|u| > y) ≥ c_u y^{−β₀}.
(If a V-side block were heavy, Lemma L below makes it V-(log-)level and the model is two-sided: PR2⁺, modulo the
log-level caveat C7 of audit_r16 — not this file.)

## 1. Lemma L (heavy ⇒ level on BOTH sides) [written proof from SM + HL]
Let H be a heavy block. Then H is U-level or U-log-level, **and** V-level or V-log-level.

*Proof.* Lemma Bot gives Y ∈ C* (critical nonlinear) with H ⇒* sYt and a terminal binary form Y ⇒* αYβYγ.
Prop HL's proof uses only: T₀ = w₀ ∈ L(Y), T_{k+1} = αT_kβT_kγ ∈ L(Y), and Lemma PC applied to the cycles
(αT_kβ, γ), (α, βT_kγ) inside H's grammar. So it applies verbatim to **any** terminal binary form of Y (audit C3).
- Some choice (form, w₀) has e ≥ 0: if the original form has D(w₀) + d < 0 for all w₀, SM(U) (as proved: Step 3)
  produces a binary form with e = 0. Otherwise some w₀ has e ≥ 0.
- Some choice has e ≤ 0: mirror, SM(V).
HL: e > 0 ⇒ U-level; e < 0 ⇒ V-level; e = 0 ⇒ U- and V-level, or U- and V-log-level. Combine. ∎

"log-level" means: words of H of lengths ℓ_i with ℓ_{i+1} ≤ 2ℓ_i + c, profile bound K(ℓ) = c log ℓ (r14 §3).

## 2. Lemma MS^in (innermost insertion: an upper barrier for A) [written proof]
Suppose some C-rule carries on its U side a block H that is V-(log-)level. Then there is c < ∞ with, for every W ∈ L
and every k ≤ |pU|:
  A_W(k) ≤ max_{j ≤ m(W)} B_W(j) + c + c·log(n+2).     (with c log replaced by 0 if H is V-level)

*Proof.* Fix a first-return loop ρ at X through that rule, all lower-block words fixed except one H-word x; its token
is (α x β, v_ρ). Choose x V-(log-)level with n ≤ |x| ≤ 3n + c, suffix profile D(x) − P_x(|x|−j) ≤ K := K(3n+c).
Append ρ as the **last** (innermost) token: W' = p U α x β w v_ρ V q ∈ L, n' = n + |αxβ| + |v_ρ| ≥ 2n.
- For k ≤ |pU|: A_{W'}(k) = A_W(k).
- For k ≤ m := |Vq|: B_{W'}(k) = B_W(k).
- For k = m + c₁ + j, c₁ := |v_ρ w β|, 0 ≤ j ≤ |x|: B_{W'}(k) = D(Vq) + D(v_ρ w β) + (D(x) − P_x(|x|−j)) ≤ D(Vq) + c₁ + K.
- For m ≤ k ≤ m + c₁: B_{W'}(k) ≤ D(Vq) + c₁.
Every k ≤ |pU| ≤ n satisfies k ≤ n'/2 and k ≤ m + c₁ + |x|. G⁻ for W' gives A_W(k) < B_{W'}(k) ≤ max_{j≤m}B_W(j) + c₁ + K. ∎

(Check: in the one-tape case v ≡ ε, m = |q| and this is PR1's barrier max P ≤ C.)

## 3. Lemma D (density of the barrier set) [written proof, elementary]
For n ≥ 4, M ≤ n/4, C ≥ 0, a ≥ 0 put T = ⌊n/2⌋ and
  S_n(M; C, a) := {W ∈ {a,b}ⁿ : B(k) ≥ −C and A(k) ≤ max_{j≤M}B(j) + a for all 1 ≤ k ≤ T}.
Then 2^{−n}|S_n| ≤ c (C+1)^{3/2} (M + (a+C+1)²) M^{−1/4} / n.

*Proof.* Under the uniform measure the first T and the last T letters are disjoint (n ≥ 2T), so A and B are independent
simple ±½ walks. Write H_M = max_{j≤M} B(j) ≥ B(M), τ = first k with B(k) < −C.
1. Ballot: P(max_{k≤T} A ≤ g) ≤ c(g+1)/√T. Given B, the A-event has g = H_M + a.
2. Markov at M: P(B stays ≥ −C on (M, T] | B(M) = h) ≤ c(h + C + 1)/√(T−M), T−M ≥ T/2.
3. So 2^{−n}|S_n| ≤ (c/T) E[(H_M + a + C + 1)² 1{τ > M}] ≤ (c/T) ‖(H_M + a + C + 1)²‖₂ P(τ > M)^{1/2}.
4. Doob L⁴: E H_M⁴ ≤ (4/3)⁴ E B(M)⁴ ≤ cM²; ballot: P(τ > M) ≤ c(C+1)M^{−1/2}. ∎
(Hölder with p → ∞ in step 3 gives M^{1/2+ε}/n; the true order is √M/n, see the DP check. M^{3/4} suffices.)

## 4. Theorem OH (one-sided heavy padding rigidity) [written proof]
Let (C, p, w, q) be critical with a heavy block on the U side, no heavy block on the V side, and L ⊆ G⁻. Then the pair
map is not injective (L is ambiguous). Mirror: heavy on V only.

*Proof.* Suppose injective. Fix γ with β₀ < γ < 4β₀/3.
1. **Lower bound** (Lemma R + tail, r16 PR2⁺ step 2): Σ_{n≤N} |L_n| 2^{−n} ≥ c N^{β₀}.
2. **Two-sided height constraints.** Lemma L makes the U-side heavy block both U- and V-(log-)level. MS⁺(b) (log form:
   pick the flat word with length in [n, 3n+c]) gives B_W(k) ≥ −C_n for all k ≤ n/2, C_n = C + c log n.
   MS^in gives A_W(k) ≤ max_{j≤m(W)}B_W(j) + a_n for k ≤ |pU|, a_n = c + c log n.
3. **Class 1: m(W) ≤ M_n := ⌊n^γ⌋** (n large so that M_n ≤ n/4 − |w|). Then |pU| = n − |w| − m ≥ n/2, and
   max_{j≤m}B ≤ max_{j≤M_n}B, so W ∈ S_n(M_n; C_n, a_n). Lemma D: 2^{−n}|class-1 words| ≤ c n^{−1+3γ/4} log³n.
   Summed: O(N^{3γ/4} log³N) = o(N^{β₀}).
4. **Class 2: m(W) > |W|^γ.** By injectivity its uniform mass is 2^{−|pwq|} Σ_r P_π(|V_r| + |q| > |W_r|^γ)
   ≤ c Σ_r [P(|V_r| > 2μ_V r) + P(|U_r| < (2μ_V r + |q| + 1)^{1/γ})].
   - |v| has an exponential moment: a first-return loop has a geometrically tailed number of steps (ρ(M|_{C∖X}) < 1,
     r13 §3); each step emits ≤ K fixed letters and V-side blocks, all non-heavy, hence (B–D, Σπ = 1) exponentially
     small coefficients, i.e. radius > ½; conditionally on the path the block words are independent. So Chernoff:
     P(|V_r| > 2μ_V r) ≤ e^{−c r}. (μ_V = 0 is trivial.)
   - P(|U_r| < x) ≤ P(max_i |u_i| < x) ≤ exp(−r c_u x^{−β₀}); with x = (c'r)^{1/γ} this is exp(−c r^{1−β₀/γ}),
     summable since γ > β₀.
   So class 2 has total mass O(1) over all N.
5. Steps 3–4 give Σ_{n≤N}|L_n|2^{−n} = o(N^{β₀}), contradicting step 1. ∎

**Remarks.**
- No tail regularity beyond the B–D two-sided ≍ is used: the upper tail bound feeds Lemma R, the lower bound of the
  heaviest block feeds step 4.
- It covers the whole one-sided family, all β₀, including (T½) (independent of PR1s, and without DW).
- The structural input is **only** Lemma L. In particular it does not matter whether the V tape has long level blocks.

### 4.1 One-tape sub-case (q_V = 0, block U-level only) — root scope update [written proof]
Covered twice over. (i) Thm OH with v ≡ ε: m(W) = |q| is constant, class 2 is empty, and Lemma D with M = |q| gives
density O(log³n / n), mass O(log⁴N) = o(N^{β₀}). (ii) More directly: in a one-tape model the heavy block (it exists,
else the tail is exponential and this is not the heavy case) is, by Lemma L, both U- and V-(log-)level, so PR1
(PR1ˡᵒᵍ: barrier c log n, bridges density O(n^{−3/2}polylog n), finite mass) applies for every β₀. The phrase "block
U-level only" can therefore not occur for a *heavy* block; a light U-level-only block is irrelevant, because only the
heavy block is used. (Caveat: the U-level-only block of r15_onesided §4 caveat (suffix-flat on the U tape) is likewise
subsumed — Lemma L gives the other shape too.)

## 5. Checks (`scripts/r17_oh_level_checks_out.txt`)
1. MS^in bookkeeping: 3000 random (p, U, w, V, q, α, β, v_ρ) with x = (ab)^{n+3} (suffix-flat, K = ½), all k ≤ |pU|:
   A_{W'} = A_W, k ≤ n'/2, B_{W'} = B_W on k ≤ m, B_{W'}(k) ≤ max_{j≤m}B_W(j) + c₁/2 + K on the x-range —
   **49,663 checks, 0 violations.**
2. Exact DP of 2^{−n}|S_n(M; 1, 1)| (integer-step units): n·density/√M =
   n = 256: 5.11, 4.40, 3.45 (M = 4, 16, 64); n = 1024: 5.27, 4.80, 4.42; n = 4096: 5.32, 4.91, 4.78.
   Bounded ⇒ true order √M/n (Lemma D's M^{3/4} is lossy but sufficient).

## 6. Points for the auditor
- Lemma L relies on HL accepting the *new* binary form produced by SM Step 3 (audit_r16 C3). I checked HL's proof:
  it uses only Y ⇒* αYβYγ with terminal α, β, γ, plus H ⇒* sYt. No restriction.
- B–D two-sided ≍ for the heaviest block (lower tail bound c_u y^{−β₀}); if only an upper bound were available one can
  instead use any heavy U-side block with exponent β₁ and pick γ ∈ (β₁, 4β₀/3) — needs β₁ < 4β₀/3, which holds when
  β₁ = β₀ (the heaviest block is on U since V has no heavy blocks).
- Light V blocks ⇒ radius > ½ uses "N-algebraic at radius ½ ⇒ infinite mean" (B–D exponents 2^{−k} ≤ 1), as in PR2⁺.
- The log-level variants only add log factors (C_n, a_n), absorbed by the polynomial gap N^{3γ/4} vs N^{β₀}.

## Status
| claim | label |
|---|---|
| Lemma L: heavy ⇒ U-(log-)level AND V-(log-)level | written proof (SM in C3 form + HL) |
| Lemma MS^in: innermost V-level insertion ⇒ A ≤ max_{j≤|Vq|}B + c + c log n on the U range | written proof + bookkeeping check |
| Lemma D: barrier-set density ≤ c(log)·M^{3/4}/n | written proof (ballot, Doob) + exact DP |
| **Thm OH**: one-sided heavy (any β₀, any q_V) ⇒ ambiguous | **written proof** modulo B–D (cited), Lemma R, MS⁺(b), SM/HL |
