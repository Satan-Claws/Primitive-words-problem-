# r18_dwfix.md — R18-D: repairing the Denisov–Wachtel citation (audit_foundations_bot_cites §2(c), W1)

Status: **every affected result is repaired.** Two of them needed no new input: their only use of D–W is from a
**fixed** start, where the pointwise D–W Theorem 1 is enough. The others are repaired by a **new elementary lemma
(Lemma U, written proof)**. It is uniform in the start and loses a factor (log m)^{1+p/2}. That loss is harmless in every
application. Each result is also marked superseded where T8_unamb no longer uses it (audit_t8 §4). The original
reports are not edited.

Script: `round2/scripts/r18_dwfix_dp.py` (output `r18_dwfix_dp_out.txt`). It runs an exact DP over all starting points.

## 0. Summary

| result | where D–W enters | verdict |
|---|---|---|
| r13 Lemma K | start at the origin, fixed slack C | **repaired (citation only).** The pointwise Thm 1 suffices. Lemma U also gives it with a (log n)^{5/3} loss. Superseded by PR2⁺ in T8. |
| r14 Thm PR2ˡᵒᵍ | slack c·log n, so the start drifts away from the apex | **repaired by Lemma U.** Density O((log n)³n^{−2/3}). Superseded by PR2⁺ in log form (audit_t8 (b)). |
| r15_tails Lemma QW | phase 2 starts at an arbitrary X_m | **repaired by Lemma U.** Density ≤ c m^{−1/3}n^{−2/3}(log n)^{5/3}. |
| r15_tails Thm PR2^β | through QW | **repaired** (strict inequality β > (1−γ)/3, so polylog is harmless). Superseded by PR2⁺ (r16). |
| r15_onesided Lemma CM, Lemma J, Thm PR1s (and §4) | wedge survival **from the origin**, fixed C_V | **repaired (citation only).** Pointwise Thm 1 suffices. Audit W1's listing of these as "uniform in x" overstates their use. Lemma U also gives them elementarily with polylog loss. Superseded by Thm OH. |
| r15_tails Prop S (lower bound) | asymptotic from a fixed start | pointwise Thm 1, OK as cited. |

## 1. What the pointwise Theorem 1 gives

D–W 2015 Thm 1 states P(τ_x > n) ∼ κV(x)n^{−p/2} for each fixed x ∈ K. So for each fixed x₀ there is a constant
c(x₀) with P_{x₀}(τ > m) ≤ c(x₀)m^{−p/2} for all m ≥ 1, because the ratio converges and every term is finite.

The origin lies on the ray A = B of W₁ = {A < B, B ≥ −C}. To handle this, condition on the first step: only finitely
many first positions x₁ lie in the interior, and the pointwise bound applies to each. The closed side B ≥ −C equals
the open side B > −C − ½ on the half-integer lattice. The hypotheses (isotropy, moments, 2-D cone) are checked in the
audit.

Hence: **every use with a start that does not depend on n or m is fully supported by Thm 1.** This covers Lemma K,
Lemma CM, Lemma J, PR1s class 3 and r15_onesided §4. For each of them the start is the origin and C is a model
constant.

## 2. Lemma U (uniform wedge survival, elementary) [written proof]

**Setting.** Z_k is the walk Z = (2A, 2B) ∈ ℤ². Its steps X are uniform on {(±1, ±1)}: under the uniform measure,
A and B are independent ±½ walks (audit_r14). Hence E X_iX_j = δ_ij, all odd moments vanish, and |X| = √2.

Let W = a + C_Θ be a closed or open wedge with apex a, opening Θ ∈ [3π/4, π) and unit bisector e (so p ∈ (1, 4/3]). Put p = π/Θ, and let
τ be the first exit time from W.

**Lemma U.** There is C = C(Θ) such that for all x ∈ W and m ≥ 2,
  P_x(τ > m) ≤ C·(1 + |x − a|)^p·(log m)^{1+p/2}·m^{−p/2}.
For Θ = 3π/4 this reads P_x(τ > m) ≤ C(1 + |x − a|)^{4/3}(log m)^{5/3}m^{−2/3}.

*Proof.* Take m ≥ m₀ (for smaller m, enlarge C). Fix η = 1/log m ≤ (π − Θ)/4. Then:
- let W′ = a′ + C_{Θ′} with a′ = a − b·e, the same bisector, and Θ′ = Θ + 2η < π;
- let p′ = π/Θ′ ∈ [1, p];
- let (ρ′, φ′) be polar coordinates about a′, with φ′ measured from one side of W′;
- let h′ = ρ′^{p′}sin(p′φ′) = Im F(z), where F(z) = ((z − a′)e^{−iψ₀})^{p′}, the branch cut is on the ray a′ − ℝ₊e,
  and ψ₀ is the direction of one side of W′.

The constant b ≥ 4 is fixed below and does not depend on m or η.

*Geometry.*
- **(G1)** For z ∈ W, the vector v = z − a lies within angle Θ/2 < π/2 of e. So:
  - ρ′(z) = |v + be| ≥ (v + be)·e ≥ b;
  - the angle of v + be to e is at most Θ/2, so φ′ ∈ [η, Θ′ − η] and h′(z) ≥ sin(p′η)ρ′^{p′} ≥ (2/π)η·ρ′^{p′}.
- **(G2)** Let d₀ := dist(a, ∂W′) = b sin(Θ′/2) ≥ b sin(π/4). Then B(a, d₀) ⊂ W′. Since W′ is a convex cone,
  B(z, d₀) ⊂ B(a, d₀) + C_Θ ⊂ W′ for every z ∈ W. With b ≥ 4, every segment [z, z + X] with z ∈ W lies in W′, away
  from the cut, and has ρ′ ≥ ρ′(z) − √2 ≥ ρ′(z)/2.

*Generator bounds.* Let Lf(z) := E f(z + X) − f(z).
- **Bound for h′.** h′ is harmonic. By (G2), Taylor's formula to order 4 applies along [z, z + X]. The 2nd-order term is
  ½Δh′ = 0 and the 3rd-order term has mean zero by symmetry. The remainder is (1/24)·Im(X_ℂ⁴F⁗(ξ)), with
  |F⁗| = p′|p′−1||p′−2||p′−3|ρ′^{p′−4} ≤ (8/9)ρ′^{p′−4}. Hence
  |Lh′(z)| ≤ (1/24)·4·(8/9)·(ρ′(z)/2)^{p′−4} ≤ 2ρ′(z)^{p′−4}.
- **Bound for g.** Let g := ρ′^α with α = p′ − 2 ∈ [−1, −2/3]. Then Δg = α²ρ′^{α−2} = α²ρ′^{p′−4}. The 3rd-order term
  vanishes, and |D⁴g| ≤ c_g ρ′^{α−4} with c_g absolute. So Lg ≥ ½α²ρ′^{p′−4} − c′ρ′^{p′−6} ≥ (1/9)ρ′^{p′−4} once
  ρ′ ≥ ρ₀, where ρ₀ is absolute. Take b ≥ max(4, ρ₀). By (G1), this holds on all of W.
- **Supermartingale.** V := h′ − 18g satisfies LV ≤ 0 at every z ∈ W. These constants are uniform in η.

*Optional stopping.* Let R ≥ 1, let σ_R := inf{k : ρ′(Z_k) ≥ R} and let T := τ ∧ σ_R ∧ m. Before T the walk is in W,
so V(Z_{k∧T}) is a supermartingale, and E V(Z_T) ≤ V(x). By (G2), Z_T ∈ W′ and ρ′(Z_T) ≥ 1, so h′(Z_T) ≥ 0 and
0 < g(Z_T) ≤ 1. Hence E h′(Z_T) ≤ h′(x) + 18.

On E := {σ_R < τ, σ_R ≤ m} we have Z_T ∈ W with ρ′ ≥ R, so h′(Z_T) ≥ (2/π)ηR^{p′} by (G1). Therefore
  P_x(E) ≤ (π/2)·(h′(x) + 18)/(ηR^{p′}),  with  h′(x) ≤ (b + |x − a|)^{p′}.

*Escape from the ball.*
- {τ > m} ⊂ E ∪ {σ_R > m}.
- On {σ_R > m} the first coordinate (a simple ±1 walk) stays in an interval of length 2R for m steps.
- For n ≥ 64R², sup_y P(S_n = y) ≤ √(2/(πn)), so a block of n steps ends inside a given interval of ≤ 3R integers with
  probability ≤ 3R√(2/π)/(8R) < 0.3.
- By the Markov property, P(σ_R > m) ≤ 0.3^{⌊m/⌈64R²⌉⌋}.
- With R² = m/(200 log m), this is ≤ 4m^{−2}.

*Assembly.* Use p − p′ ≤ 2πη/Θ², so that R^{−p′} ≤ e^{π/Θ²}R^{−p}, together with η = 1/log m and p′ ≤ p. Then
  P_x(τ > m) ≤ C(1 + |x − a|)^p·log m·(log m/m)^{p/2} + 4m^{−2}.
Since p ≤ 4/3, the last term is absorbed. ∎

*Remarks.*
- The proof needs only Taylor's formula, optional stopping and the binomial point bound.
- The restriction Θ ≥ 3π/4 keeps α = p′ − 2 ≤ −2/3, so K = 18 is uniform. For the quadrant, and anything used in QW
  steps 3–5, the product structure and reflection are used instead, as in r15.
- The sharp form P_x(τ > m) ≤ C·h(x)m^{−p/2} without logs, with h harmonic for a slightly shifted wedge, is **not
  proved here**. It is numerically supported, as §3 shows.

## 3. Numerical check (exact DP over all starts) [`r18_dwfix_dp.py`]

Setup:
- W = {x < y, y ≥ 0} in Z-coordinates, angle 3π/4.
- u_m(z) = P_z(τ > m), computed by exact backward recursion on a box of half-width 700. Only z with box distance > m
  are used, and the gap between the 0-padded and 1-padded runs there is 0.
- The scan covers all z ∈ W with |z| ≤ 180, which is ≥ 8√m.

| m | sup_z m^{2/3}u_m/(1+|z|)^{4/3} | sup_z m^{2/3}u_m/h′(z) (apex shifted by 2) | m^{2/3}u_m(0,1) |
|---|---|---|---|
| 8 | 0.480 | 0.336 | 1.168 |
| 32 | 0.557 | 0.414 | 1.282 |
| 128 | 0.580 | 0.476 | 1.315 |
| 512 | 0.590 | 0.521 | 1.324 |

- The uniform (1+|z|)^{4/3} ratio saturates near 0.6, with no log growth visible. So Lemma U's statement without the
  log factor appears true.
- The sharp h′-ratio increments shrink (0.034, 0.029, 0.025, 0.020 per doubling), which is consistent with a finite
  limit.
- This is a numerical check, not a proof of the log-free form.

## 4. Repairs, result by result

1. **r13 Lemma K.** Replace "[cited D–W]" with "D–W 2015 Thm 1 (pointwise; start = origin, via a first-step
   decomposition, §1)". The statement c_C·2ⁿn^{−2/3} stands. An elementary alternative is Lemma U with x = origin,
   giving c_C·2ⁿn^{−2/3}(log n)^{5/3}; PR2's squeeze O(N^{1/3}polylog) = o(√N) still closes.
   **Repaired.** Off the T8 path: PR2 is subsumed by PR2⁺.
2. **r14 Thm PR2ˡᵒᵍ, step 3.** Replace the cited "uniform D–W bound" with Lemma U.
   - The start is at distance ≤ c log n + O(1) from the apex, and m = ⌊n/2⌋, so the density is
     O((log n)^{4/3+5/3}n^{−2/3}) = O((log n)³n^{−2/3}).
   - In the γ-slack version the density is O(n^{−2/3+4γ/3}(log n)^{5/3}), which sums to o(√N) for γ < 1/8 (strict), as
     before.
   **Repaired.** Superseded in T8 by PR2⁺ in log-level form (audit_t8 case (b), audit_r17 C2).
3. **r15_tails Lemma QW, step 2.** Apply Lemma U at time m from X_m ∈ W_i with t = ⌊n/2⌋ − m ≥ n/4 and
   |X_m − a_i| ≤ |X_m| + O(C). Steps 3–5 are unchanged (quadrant, Hölder, reflection), so the density is
   ≤ c m^{−1/3}n^{−2/3}(log n)^{5/3}.
   **Repaired**, with the log factor added to the statement.
4. **r15_tails Thm PR2^β.** The upper bound becomes O(N^{(1−γ)/3}(log N)^{5/3}), against the lower bound cN^β with
   β > (1−γ)/3 strict. Coverage is unchanged (the borderline k = 2, j = 0 was already excluded).
   **Repaired.** Superseded by PR2⁺ (r16), which also closes the borderline.
5. **r15_onesided Lemma CM, Lemma J, Thm PR1s, §4.** The only D–W input ("DW survival", §2 there) is from the origin
   with the fixed model constant C_V. Pointwise Thm 1 (§1) gives exactly the c_C m^{−2/3} used. Change the attribution
   from "r13 Lemma K, cited" to "D–W Thm 1, pointwise". Audit W1's classification of these as using the uniform-in-x
   form is inaccurate.
   - Elementary alternative (Lemma U): CM and J gain (log m)^{5/3}, giving m^{−1/6}(log m)^{13/6}. PR1s class 3
     becomes O(N^{5/12}polylog N) = o(√N), so the proof still closes.
   **Repaired.** Superseded in T8 by Thm OH.
6. **r13 §5 one-sided sketch, step 3** (D–W *conditional limit*). This was already replaced by r15 Lemma CM, so item 5
   covers it.

**Net.** No result in round 2 now depends on an uncited uniform-in-start D–W bound. Apart from Lemma U, the only D–W
input left is the pointwise Thm 1 at fixed starts, which the paper does state. T8_unamb is unaffected (PR2⁺ and Thm OH
use ballot bounds only).
