# r16_unbal.md — R16-A: the unbalanced two-tape case

Status: **the unbalanced two-tape case is CLOSED** (written proof, elementary, no Denisov–Wachtel), for every k and
every lighter exponent j (including the k = 2 borderline). The proof does **not** refine PR2^β. It strengthens
Lemma MS: the existing MS proof already bounds A(k) (resp. B(k)) for **all** k ≤ n/2, not only for U- (resp. V-)
positions. With both halves, L lies in the quadrant set Q_n(C) of density ≍ 1/n. That set has mass O(log N), which
no polynomial renewal mass N^{β₀} can fit into.
- **Flag for audit (scope):** one-sided **heavy** models (U-level block only, q_V > 0, tail β ≤ 1/4) are *not* covered
  by this argument (§5). They appear neither in r15's open list nor in PR1s, which needs (T½). The auditor should
  confirm whether the T8_unamb reduction already excludes them.

Scripts:
- `scripts/r16_unbal_fullms.py` → `r16_unbal_fullms_out.txt`: bookkeeping check of Lemma MS⁺ (2000 random
  instances, 0 violations) and the exact density of Q_n(C).
- `scripts/r16_unbal_barrier.py` → `r16_unbal_barrier_out.txt`: the barrier product bound of §4 (superseded route).

## 1. Lemma MS⁺ (full-range heights) [written proof; the r13 §1 proof, read correctly]
Setting as in r13 §0: W = p u₁⋯u_r w v_r⋯v₁ q, A(k) = P(k), B(k) = P(n) − P(n−k), and G⁻ ⟺ A(k) < B(k) for 1 ≤ k ≤ n/2.

(a) If some C-rule carries a V-level block, there is C_U < ∞ with A_W(k) ≤ C_U for **every** W ∈ L and 1 ≤ k ≤ n/2.
(b) If some C-rule carries a U-level block, there is C_V < ∞ with B_W(k) ≥ −C_V for **every** W ∈ L and 1 ≤ k ≤ n/2.

*Proof of (b).* (a) is the mirror image.
1. Fix a first-return loop ρ at X through the rule that carries the U-level block. Every lower-block word in ρ is fixed
   except one U-level word x, with prefix profile P_x(j) ≥ −K and |x| = L. Write ρ's token as (α x β, v_ρ), where α, β
   and v_ρ are fixed words.
2. For W ∈ L with sequence s, the sequence ρ·s is legal, because tokens are i.i.d. first-return loops. Its word is
   W' = p α x β M v_ρ q, where W = p M q, so M = U w V is contiguous in both words. Then n' = n + L + |αβ v_ρ|.
3. *B transports.* For |q| ≤ k ≤ n − |p|, the suffix of W' of length k + |v_ρ| is (suffix of M of length k − |q|)·v_ρq.
   So B_{W'}(k + |v_ρ|) = B_W(k) + wt(v_ρ).
4. *A is frozen.* For k' ≤ |pαx|, A_{W'}(k') ≥ −K − |p| − |α| =: −K₁.
5. Take L ≥ n. Then for k ≤ n/2 we have k' := k + |v_ρ| ≤ n'/2 and k' ≤ |pαx|. G⁻ for W' gives
   −K₁ ≤ A_{W'}(k') < B_{W'}(k') = B_W(k) + wt(v_ρ).
   So B_W(k) > −K₁ − |v_ρ| for |q| ≤ k ≤ n/2, and trivially B_W(k) ≥ −|q| for k < |q|. ∎

r13 §1 runs exactly this construction, steps 3–5, but states the conclusion only for U-positions (resp. V-positions).
Nothing in the proof uses the restriction. All it needs is that M is contiguous in W' and that the flat word is longer
than n. r15_onesided §4 already uses the full-range form in the one-tape case. The only extra point in the two-tape
case is the fixed word v_ρ, which shifts the index and the height by O(1).

**Check** (`r16_unbal_fullms_out.txt`): on 2000 random (p, M, q, α, β, v_ρ) with x = (ba)^{n+5} and y = (ab)^{n+5},
- the transport identities B_{W'}(k + |v_ρ|) = B_W(k) + wt(v_ρ) and A_{W''}(k + |α|) = A_W(k) + wt(α) hold for every
  admissible k;
- the frozen bound of step 4 holds.
There are 0 violations.

## 2. The quadrant bound [elementary]
Put Q_n(C) := {W ∈ {a,b}ⁿ : A(k) ≤ C and B(k) ≥ −C for 1 ≤ k ≤ ⌊n/2⌋}.
- A only reads the first ⌊n/2⌋ letters and B only the last ⌊n/2⌋. Under the uniform measure these are independent
  simple ±½ walks.
- The ballot/reflection bound gives P(max_{k≤m} S_k ≤ C) ≤ c(C+1)m^{−1/2}.
- Hence 2^{−n}|Q_n(C)| ≤ c_C/n.

Exact DP (`r16_unbal_fullms_out.txt`, n ≤ 4096):
- C = 0: n·density = 1.2535, 1.2683, 1.2720, 1.2729 (→ 4/π ≈ 1.2732);
- C = 1: n·density = 10.41, 11.18, 11.39, 11.44 (still rising slowly; bounded).

## 3. Theorem PR2⁺ (two-sided level padding, all tails) [written proof; cites B–D Thm 3 for the tail form]
**Hypotheses.**
- C is a critical linear SCC of an unambiguous grammar for L.
- Its pair model (p, w, q) has i.i.d. tokens with law π.
- Some C-rule carries a U-level block and some C-rule carries a V-level block.
- L ⊆ G⁻.

**Conclusion.** The pair map is not injective. In fact the average multiplicity is ≥ cN^{β₀}/log N.

*Proof.*
1. **Tail.** Σπ = 1 rules out divergent-mean blocks. By B–D Thm 3, every lower block has coefficients
   ≍ n^{−1−2^{−k}} (per residue class) or exponentially small. The union bound of r13 §3 then gives
   F̄(y) = O(y^{−β₀}) for the loop length, with β₀ = 2^{−k_max} > 0. (This uses only an upper bound, so no
   exact-exponent regularity is needed, unlike Lemma Bal.)
2. **Lemma R** gives U(x) ≥ x/m(x), with m(x) = Σ_{y<x}F̄(y) = O(x^{1−β₀}). So under injectivity,
   Σ_{n≤N}|L_n|2^{−n} ≥ c N^{β₀}.
3. **Upper bound.** Lemma MS⁺ (a) and (b) give L_n ⊆ Q_n(C), with C = max(C_U, C_V). By §2,
   Σ_{n≤N}|L_n|2^{−n} ≤ Σ_{n≤N} c_C/n = O(log N).
4. **Contradiction.** c N^{β₀} ≤ O(log N) fails for large N. ∎

**What it covers.** This covers every case of r15 §5–6:
- balanced and unbalanced;
- heavier exponent 2^{−k} for any k ≥ 1;
- lighter tape 2^{−j} for any j, or exponential;
- the borderline k = 2, j = 0.

The balance of the tapes plays no role. The quadrant constraint holds for **all** k ≤ n/2, whatever the actual lengths
of U and V. It also re-proves PR2 under (T½), with mass O(log N) against c√N, and without Lemma K or DW.
- Lemma V (Valley), Lemma QW, Lemma Bal and the DW citation are no longer needed for two-sided models.
- The multiplicity corollary improves from n^{1/6} to N^{β₀}/log N (under (T½), √N/log N).

Why it was missed: r13 stated MS for U-positions only and then combined the two halves into Lemma V's valley (a 3π/4
wedge). All later rounds inherited the wedge.

## 4. Superseded route (recorded for completeness) [heuristic + numerics]
Before noticing MS⁺, I developed a *separation* argument. Closure of L under concatenation of token sequences
(s, s′ ↦ s·s′) forces a deterministic barrier g with sup_s Ã_s ≤ g < inf_{s′} B_{s′}. A Gaussian log-concavity
product bound, F(g)F̄(g − c) ≤ F(c/2)², then gives density polylog/n.

The obstruction was the index shift a = |V(s)|: B must cross V before reaching U.
- With the barrier regularity g(k − a) ≤ g(k) + O(1) this would close.
- Without it, every accounting I tried landed at exactly the borderline (N^β log N vs N^β).

Numerics (`r16_unbal_barrier_out.txt`): over 16 barrier shapes (±a√k, ±εk, frozen random-walk paths, sawtooth;
T = 100, 400, 1600), max F(g)F̄(g) / F(0)F̄(0) = 1.0000, attained at g = 0, and T·F(0)² → 0.636.

MS⁺ makes this route unnecessary, because the flat loop plays the role of the barrier with g ≈ const.

## 5. Scope flag: one-sided heavy models [observation]
With a U-level block only and q_V > 0:
- MS⁺(b) gives B ≥ −C for all k ≤ n/2;
- G⁻ gives A < B;
- so L lies in the 3π/4 wedge for n/2 steps, with density ≍ n^{−2/3} (DW) and mass O(N^{1/3}).

This beats the renewal mass N^{β₀} only if β₀ > 1/3, i.e. under (T½) (an alternative proof of PR1s, without Lemma J).
For heavy one-sided tails (β₀ ≤ 1/4) it does **not** close. In that case A has no upper constraint, so a superset
argument must use L's structure on the U tape. r15's open list does not mention this case, and PR1s assumes (T½). The
T8_unamb synthesis should state where it is handled, or list it as open.

## 6. T8_unamb — statement for the gated audit
**Theorem T8_unamb (conditional on the reduction chain).** Let L ⊆ G⁻ = {w ∈ {a,b}ⁿ : d_k(w) < 0 for 1 ≤ k ≤ n/2}
be an unambiguous context-free language. Then L is not rotation-dense.

**Proof structure.** Rotation-density forces a critical linear SCC with a pair model, via the earlier reduction rounds
(r10–r12). That model is excluded by:
- the **one-tape** case: PR1 (r13 §5) and r15_onesided §4;
- the **one-sided** case under (T½): Thm PR1s (r15_onesided), or alternatively §5 above;
- **side mismatch / steep** models: Theorem SM (r15_side) and r14_steep;
- the **two-sided level** case, all tails, balanced or not: **Thm PR2⁺ (this file)**.

**Cited results.**
- Banderier–Drmota (CPC 2015, Thm 3): dyadic critical exponents of N-algebraic functions.
- Drmota–Lalley–Woods: square-root singularity and aperiodic coefficient asymptotics for strongly connected critical
  nonlinear systems. Used in Lemma ST and the reduction rounds.
- Denisov–Wachtel: cone survival exponents. Used only by PR1s, Lemma K and SM; **not** needed for PR2⁺.

**Audit conditions.**
1. Confirm that the reduction chain lands every case in the list above.
2. Resolve the §5 scope flag (one-sided, heavy tails). If that case is genuinely uncovered, T8_unamb is closed
   **except** for it.

## Status
| claim | label |
|---|---|
| Lemma MS⁺ (full-range A ≤ C_U, B ≥ −C_V) | written proof (r13 §1 construction) + 0-violation bookkeeping check |
| Quadrant density c_C/n | elementary + exact DP |
| **Thm PR2⁺**: two-sided level, all k, balanced or not ⇒ ambiguous | **written proof** (B–D Thm 3 for the tail form) |
| Unbalanced gap of r15 (k ≥ 3 with j < k; k = 2 with j = 0) | **CLOSED** by PR2⁺ |
| Separation/barrier route (§4) | heuristic; superseded |
| One-sided heavy tails (β₀ ≤ 1/4, U-level only, q_V > 0) | **not covered**; scope flag for the audit |
| T8_unamb | closed modulo the reduction chain and the §5 flag; awaiting gated audit |
