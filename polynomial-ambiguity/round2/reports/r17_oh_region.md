# r17_oh_region.md — R17b: the region route for one-sided (and one-tape) HEAVY models

Status: **one-sided/one-tape heavy models CLOSED under hypothesis (F) + (V₁)** (written proof, elementary: 1-D
ballot bounds only, no Denisov–Wachtel, no tail exponent used beyond U(N) ≫ log⁴N). The cases outside (F) are listed
in §5 as the exact remaining gap. The premise "MS⁺ gives A ≤ C at every k" is **false** in the one-sided case
(§1); the extra constraint comes from a *different* insertion (Lemma MS^back, §2).

Scripts:
- `scripts/r17_oh_region_dp.py` → `r17_oh_region_dp_out.txt` (exact DP: wedge exponent; density of the new region).
- `scripts/r17_oh_region_check.py` → `r17_oh_region_check_out.txt` (bookkeeping of Lemma MS^back: 0/2000 violations).

## 0. Setting
As r13 §0 / r16 §1: W = p U w V q, A(k) = P(k), B(k) = P(n) − P(n−k), G⁻ ⟺ A(k) < B(k) (1 ≤ k ≤ n/2). Tokens
(u, v) i.i.d., law π, any token sequence is legal, the sequence→word map is injective (unambiguity). Put
m₀(W) := |wVq| = n − |pU|. S_x(j) := wt(last j letters of x) (suffix excess); P_x = prefix profile.

**Hypotheses.**
- (U-lev) some C-rule carries a U-level block (arbitrarily long x with P_x(j) ≥ −K for all j).
- **(F)** some C-rule carries a U-side block with arbitrarily long **suffix-flat** words: S_x(j) ≤ K for all j
  ("V-level shape on the U tape"). It may be the same block: E, D⁻ and every block with flat words (ba)^m,
  b(ba)^{m−1}a satisfy (U-lev) and (F) at once.
- **(V₁)** μ_V := E_π|v| < ∞. Holds in the one-tape case (v ≡ ε, μ_V = 0) and whenever the V tape has no
  infinite-mean block. q_V > 0 is **not** needed.

## 1. The region from {MS⁺(b)} ∩ {G⁻} alone is exactly the 3π/4 wedge [elementary + DP]
With a U-level block only, MS⁺(b) gives B ≥ −C_V; MS⁺(a) (A ≤ C_U) needs a **V-level** block and is not
available. So the constraint set is W₁ = {A < B, B ≥ −C}: opening 3π/4, survival exponent π/(2·3π/4) = 2/3
(DW; DP with C = 1 in integer units: P(τ>m)·m^{2/3} = 0.382, 0.401, 0.406, 0.408 for m = 16…1024; r15 §6 for C = 0). This is sharp for these two constraints, so mass
N^{1/3} and the route **as posed** cannot beat N^{β₀} for β₀ ≤ 1/3. A narrower region needs a new constraint.

## 2. Lemma MS^back (innermost insertion) [written proof + 0-violation check]
Assume (F). There is C' < ∞ such that every W ∈ L satisfies
  A_W(k) < B_W(m₀) + C'   for all m₀ + c ≤ k ≤ |pU| (c fixed).
*Proof.* Fix a first-return loop ρ at X through the rule with the suffix-flat block; its token is (αxβ, v_ρ), all
fixed except x, |x| = L ≥ n, S_x ≤ K. Append ρ as the LAST token of W's sequence (legal). The word is
W' = p U αxβ w v_ρ V q, n' ≥ n + L ≥ 2n.
1. A_{W'}(k) = A_W(k) for k ≤ |pU| (same prefix).
2. The suffix of W' of length m₀ + |v_ρβ| + j is (last j letters of x)·β w v_ρ V q, so
   B_{W'}(m₀ + |v_ρβ| + j) = B_W(m₀) + wt(v_ρβ) + S_x(j) ≤ B_W(m₀) + |v_ρβ| + K, for 0 ≤ j ≤ L.
3. For m₀ + |v_ρβ| ≤ k ≤ |pU| we have k ≤ n ≤ n'/2, so G⁻ for W' gives A_W(k) < B_{W'}(k) ≤ B_W(m₀) + C'. ∎
(MS⁺ inserts at the FRONT and freezes A of W'; MS^back inserts at the BACK and freezes B of W'. The general
position-i insertion gives B_W(k) > A_W(a_i) − K for k ∈ [a_i + c, n − a_i], a_i the i-th U-boundary; not needed.)

## 3. The region and its density [elementary]
Let M ≥ m₀(W) + c, n ≥ 4M, T = ⌊n/2⌋. For k ≤ M: A(k) < B(k) ≤ max_{j≤M}B_j (G⁻). For M < k ≤ T: A(k) <
B(m₀) + C' (MS^back). With MS⁺(b):
  W ∈ E_n(M) := {B(k) ≥ −C ∀k ≤ T} ∩ {A(k) ≤ H_M ∀k ≤ T},   H_M := max_{j≤M} B_j + C'.
Region geometry: after time M it is a **quadrant** {A ≤ h, B ≥ −C} (opening π/2, exponent 1), with a corner h
set by the first M steps.
**Lemma D.** 2^{−n}|E_n(M)| ≤ c √M log M / n for n ≥ 4M; and ≤ c n^{−1/2} for all n.
*Proof.* A (first T letters) and B (last T letters) are independent ±½ walks. Ballot: P(max_{k≤T}A ≤ h) ≤
c(h+1)/√T. Condition on B; Markov at M: P(B ≥ −C on [M, T] | B_M) ≤ c(B_M + C + 1)/√T ≤ c(H_M+C+1)/√T. So
P(E) ≤ (c/T)·E[(H_M + C₂)²; B ≥ −C on [0, M]]. Truncate at λ = √(3M log M): on {H_M ≤ λ+C'} the integrand is
≤ (λ+C₃)², times P(B ≥ −C on [0,M]) ≤ c/√M, giving O(√M log M); on {H_M > λ+C'} (prob ≤ M^{−3}, Hoeffding +
reflection) the integrand is ≤ (M + C₃)², giving O(1/M). The second bound is ballot for B alone. ∎
DP (`r17_oh_region_dp_out.txt`, C = C' = 1, T = 256/1024/4096): T·P(E) = 5.22/5.30/5.32 (M = 4), 9.31/9.74/9.86 (M = 16),
16.1/18.6/19.4 (M = 64): bounded in T (exponent 1, not 2/3) and ≈ ×2 per ×4 in M, i.e. ∝ √M (the log is not seen).

## 4. Theorem OH (one-sided and one-tape heavy models) [written proof]
Under (U-lev), (F), (V₁), injectivity and L ⊆ G⁻ are incompatible, for every tail (all β₀ > 0, also log-level).
*Proof.* S_r := token-length sum of r tokens; U := U(N) = Σ_r P(S_r ≤ N) = π-mass of sequences with |W| ≤ N
(up to 2^{|pwq|}). By r16 §3 steps 1–2 (Lemma R), U ≥ c N^{β₀}; all we use is U ≫ log⁴N.
1. *Renewal moment.* Let r₀ = min{r : P(S_r ≤ N) ≤ ½}. Sub-multiplicativity gives P(S_r ≤ N) ≤ 2^{−⌊r/r₀⌋}, so
   Σ_r r P(S_r ≤ N) ≤ 4r₀², and U ≥ r₀/2. Hence Σ_r r P(S_{r−1} ≤ N) ≤ 20U².
2. *Class 2: |V| ≥ M'.* E[|V_r|; S_r ≤ N] ≤ Σ_i E[|v_i|; S_r − |u_i v_i| ≤ N] = r μ_V P(S_{r−1} ≤ N). Markov:
   mass ≤ 20 μ_V U²/M' ≤ U/4 for M' = 80μ_V U. (One-tape: empty class.)
3. *Class 3: the rest.* m₀ ≤ M := M' + |wq| + c. By injectivity these give distinct words of L_n ⊆ E_n(M), so by
   Lemma D their mass is ≤ 2^{|pwq|} Σ_{n≤N} 2^{−n}|E_n(M)| ≤ C(√M + √M log M · log N) = O(√U log²N).
4. U ≤ U/4 + O(√U log²N) ⇒ U = O(log⁴N), contradicting U ≥ cN^{β₀}. ∎
**One-tape (q_V = 0, audit C3) with a U-level-only block:** covered when (F) holds; then M = O(1), L ⊆ E_n(O(1)),
density O(1/n), mass O(log N) — no (T½), no DW. If the one-tape block is U-level only and **not** suffix-flat,
see §5.

## 5. Exact remaining gap [observation]
(a) **¬(F)**: every long U-side word has unbounded suffix excess. Sub-cases:
- *ascending* words (P_x(j) ≥ εj − K, e.g. a* with a = up): front insertion (MS⁺ step 4 with the true profile)
  gives B_W(k) ≥ εk − C, density e^{−cn}: **closed** (one line, same proof as MS⁺).
- *late-rise* words, e.g. a block {(ba)^m a^m}: front insertion gives only B ≥ −C, back insertion only
  A(k) < B(m₀) + min(j/2, m/2): **OPEN**. The region stays the 3π/4 wedge; the position-i insertion
  constraint B(k) > A(a_i) − K (§2 remark) is the natural next tool.
(b) **¬(V₁)**: an infinite-mean V block that is not V-level (steep/ascending on the V side). The class-2 bound fails;
  Lemma D still applies with M = m₀, so what is missing is only a mass bound on {|V| large}.

## Status
| claim | label |
|---|---|
| {MS⁺(b)} ∩ {G⁻} region = 3π/4 wedge, exponent 2/3 (sharp) | elementary + DP; the "A ≤ C" premise is false here |
| Lemma MS^back (A < B(m₀) + C' on the U range) | written proof + 0/2000 bookkeeping check |
| Lemma D (density √M log M / n; quadrant after time M) | written proof (1-D ballot) + DP |
| **Thm OH**: (U-lev)+(F)+(V₁) ⇒ ambiguous, all tails | **written proof** |
| one-tape, U-level-only block with (F) (audit C3) | closed (mass O(log N)) |
| ascending U words | closed (exponential density) |
| late-rise U blocks without suffix-flat words; infinite-mean non-level V | **OPEN** |
