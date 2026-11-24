# r14_steep.md — R14-B: steep models and heavier tails (the remaining PR gap)

Status: **partial.**
- Steep case (a) is **reduced, not closed**: every heavy block is level on *some* side, or log-level on both
  (Prop HL, written proof). PR2 extends to log-slack padding (Thm PR2ˡᵒᵍ, written proof modulo a uniform cone bound).
  What is left is a *side mismatch*.
- (b) heavier tails: **OPEN**. The exact obstruction is stated in §5.
- (c) one-sided conditional-moment step: **not attempted** (no time).
- **T8_unamb stays OPEN.** No counterexample.

Scripts: `scripts/r14_steep_checks.py` → `scripts/r14_steep_checks_out.txt`.
Notation as in r12/r13: D(x) = drift of x (a = +½, b = −½), depth(x) = −min_j P_x(j).
- U-level: long words with depth ≤ K.
- V-level: long words with every suffix drift ≤ K.
- *log-level*: K is replaced by c·log|x|, along a family whose lengths grow geometrically.

## 0. Correction to the premise of (a)
"No long level words ⇒ slope bounded away from 0" is **false**. b^m a^m (or b^m E a^m) is steep with D = 0. Steepness
is a statement about nesting, not about drift.

My first steep candidate, T → bTTa | ε, looks heavy because it has Catalan-many trees. As a *language*, though, it has
Motzkin-many words (growth √3 < 2), because the grammar is ambiguous. So it is **not** a heavy block (check (1)).
I found no steep full-entropy block.

## 1. Lemma PC (pump criterion for level) [written proof]
Let B be a CF language with a reduced grammar. Suppose some useful nonterminal Y and some x = u v w y z ∈ B satisfy
Y ⇒⁺ vYy and Y ⇒* w, with |vy| ≥ 1.
- (U) If D(v) ≥ 0 and D(v) + D(y) ≥ 0, then B is U-level.
- (V) If D(y) ≤ 0 and D(v) + D(y) ≤ 0, then B is V-level.

*Proof of (U).* Let x_i = u vⁱ w yⁱ z ∈ B. Bound the prefix walk region by region:
- In u, it is unchanged.
- In the j-th copy of v, it is P(u) + (j−1)D(v) + P_v(r) ≥ P(u) + min P_v.
- In w, it is ≥ P(u) + min P_w, since iD(v) ≥ 0.
- In the j-th copy of y (1 ≤ j ≤ i), the shift is iD(v) + (j−1)D(y). This is ≥ 0 if D(y) ≥ 0. Otherwise it is
  ≥ (i−1)(D(v)+D(y)) + D(v) ≥ 0.
- In z, the shift is i(D(v)+D(y)) ≥ 0.

So depth(x_i) ≤ depth bound of x for all i, and the lengths |x| + (i−1)|vy| → ∞.

*Proof of (V).* Apply (U) to φ(x^R), where φ swaps a and b. This maps the cycle (v, y) to (φ(y^R), φ(v^R)) and negates drifts. ∎

Corollary: "steep on both sides" means every cycle has D(v) < 0 < D(y), because the complement of K ∪ K′ is exactly
{D(v) < 0 < D(y)}.

## 2. Lemma Bot (heavy blocks contain a critical *nonlinear* SCC) [written proof, standard facts]
Let B be heavy (Cor H: μ(B) < ∞ and infinite mean). Then:
- B's radius is ½. Unambiguity gives radius ≥ ½, and radius > ½ would give a finite mean.
- Some SCC C* reachable from B has radius ½ while every SCC strictly below it has radius > ½.
- If C* were linear, then ρ(M(½)) = 1 with analytic lower data would give a pole, so μ(Y) = ∞ for Y ∈ C*.
  B ⇒* sYt then gives μ(B) ≥ 2^{−|st|}μ(Y) = ∞, a contradiction.

So C* is nonlinear. By strong connectivity and productivity, there is a derivation **Y ⇒* αYβYγ** with α, β, γ terminal words.

## 3. Prop HL (heavy ⇒ level, or log-level on both sides) [written proof]
Fix Y, α, β, γ from Lemma Bot. Let d = D(αβγ), pick any w₀ ∈ L(Y), and put e = D(w₀) + d.
Define T₀ = w₀ and T_{k+1} = α T_k β T_k γ ∈ L(Y). Then D(T_k) = 2^k e − d and |T_k| ≍ 2^k.
- **e > 0.** D(T_k) → +∞. The cycle (αT_kβ, γ), obtained by expanding the first Y, has D(v) ≥ 0 and total D(T_k) + d ≥ 0.
  By PC(U), B is **U-level** (B ⇒* sYt supplies the context).
- **e < 0.** The cycle (α, βT_kγ) has D(y) → −∞ and total → −∞. By PC(V), B is **V-level**.
- **e = 0.** D(T_k) = −d is constant.
  - If D(α) ≥ 0, the cycle (α, βT_kγ) has total 0 and D(v) ≥ 0, so B is U-level and V-level.
  - If D(γ) ≤ 0, the same holds with (αT_kβ, γ).
  - Otherwise depth(T_{k+1}) ≤ depth(T_k) + c and the suffix excess also grows by ≤ c per step, with c = |αβγ| + 2|d|.
    So B is **U- and V-log-level** via s·T_k·t, with depth O(log|T_k|) and lengths ratio → 2.

So **no heavy block is steep on both sides in the log sense.**

## 4. Thm PR2ˡᵒᵍ (log-slack padding) [written proof modulo a uniform cone bound]
PR2 and PR1 hold with "level" replaced by "log-level" (indeed by "L^γ-level" for any γ < 1/8).

Changes to r13:
1. **MS.** In step 5, choose the block word with L ∈ [k′, 2k′ + c], which the geometric lengths allow.
   Then B(k′) ≤ β + c log k′, so heights at U-position k are ≤ C + c log k. The mirror is the same.
2. **V.** This gives Valley_{C+c log n}.
3. **K.** The apex slack is c log n. Use the uniform Denisov–Wachtel bound P_x(τ > m) ≤ C(1+|x|)^{p} m^{−p/2} with
   p = π/θ = 4/3 (DW 2015, uniform upper bound accompanying Thm 1) [cited].
   This gives density O((log n)^{4/3} n^{−2/3}), or n^{−2/3+4γ/3} for γ-slack.
4. **Squeeze.** O(N^{1/3} polylog N) is o(c√N) under (T½), so the map is not injective.

Check (2), m = 512: the survival ratio p_W1(m, C)/p_W1(m, 0) is 1.64, 1.95, 2.25 for C = 2, 4, 8. That is well below
(1+C)^{4/3}, so it is consistent with the bound (pre-asymptotic).

## 5. Exact remaining gap
1. **Side mismatch (from (a)).** Prop HL can return the wrong side. Two examples: a U-side heavy block that is only
   V-level (the case e < 0 for every choice of w₀ and of binary form), or a V-side block that is only U-level.
   MS needs a V-(log-)level block on the V tape and a U-(log-)level block on the U tape.
   - A U-side block with all e < 0 dips with *linear* drift along T_k. This is consistent with G⁻, and SF does not exclude it.
   - Open: does criticality force e = 0 for some (w₀, binary form)? The zero-mean-drift identity ρ′(0) = 0 from the
     cosh-tilt comparison suggests so, but it is not proved.
   - Also open: the case where the other tape carries no infinite block at all. That is the one-sided case (r13 §5).
2. **Heavier tails (b).**
   - Lemma Bot shows the tail exponent is −3/2 at the bottom.
   - Heavier tails, block exponent −1−β with β = 2^{−k}, k ≥ 2, arise only by composing critical *linear* SCCs above it.
     This matches the Banderier–Drmota exponents [cited; completeness of their classification for all ℕ-algebraic
     series not re-checked].
   - Lemma R gives mass N^{β} ≤ N^{1/4}, while the cone gives N^{1/3}, so the squeeze fails by counting.
   - Any fix must use the inner linear SCC of the heavy block. I have no argument for that.
3. **(c)** The one-sided conditional-moment step (r13 §5 step 3) is not written.

F1 check: everything uses the drift and walk geometry of G⁻ and the cone bound. Q has density 1, so nothing here
applies to it.

## Status
| claim | label |
|---|---|
| Premise "steep ⇒ slope ≠ 0" | false (b^m a^m) |
| Lemma PC (cycle criterion for U/V-level) | written proof |
| Lemma Bot (heavy block ⊇ critical nonlinear SCC) | written proof (standard facts) |
| Prop HL: heavy ⇒ U-level, V-level, or log-level on both sides | written proof |
| Thm PR2ˡᵒᵍ / PR1ˡᵒᵍ | written proof modulo uniform DW bound [cited] + check (2) |
| Side mismatch; heavier tails; one-sided step; T8_unamb | **OPEN** |
