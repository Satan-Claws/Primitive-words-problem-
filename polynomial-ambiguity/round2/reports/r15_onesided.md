# r15_onesided.md — R15-C: the one-sided padding case, written out

Status: **Thm PR1s (one-sided padding rigidity) — written proof, modulo the SAME cited Denisov–Wachtel survival bound
that PR2 uses.** The conditional-moment step that r13 §5 left as a sketch is proved here (Lemma CM), with a harmless
√log loss. It does **not** need the Denisov–Wachtel conditional limit theorem or any moment convergence: one
truncation plus Hoeffding replaces it. Together with PR2, this removes r13 §6 gap 3 and audit_r14 caveat C1.
No counterexample (as the theorem predicts). **T8_unamb stays OPEN** (steep models, heavier tails, side mismatch).

Scripts:
- `scripts/r15_onesided_moment.py` → `scripts/r15_onesided_moment_out.txt` (exact DP for Lemma CM and Lemma J).
- `scripts/r15_onesided_models.py` → `scripts/r15_onesided_models_out.txt` (exact n ≤ 22 test of candidate models).

## 0. Setting (as r13 §0)
- Critical linear SCC C, X ∈ C, context S ⇒* pXq, exit X ⇒* w. First-return loops at X give i.i.d. tokens (u, v),
  law π(u, v) = 2^{−|u|−|v|}, Σπ = 1. W = p u₁⋯u_r w v_r⋯v₁ q. Write U = u₁⋯u_r and V = v_r⋯v₁.
- The sequence ↦ word map is injective (unambiguity).
- A(k) = P(k), B(k) = P(n) − P(n−k). W ∈ G⁻ ⟺ A(k) < B(k) for 1 ≤ k ≤ n/2.
- (T½): every lower block in a C-rule has tail Σ_{ℓ>y}|B_ℓ|2^{−ℓ} = O(y^{−1/2}).
- U-level / V-level as in r13 §0.

**One-sided case.** Some C-rule carries a U-level block. The V tape is arbitrary: its blocks need not be level, and
it may have no infinite block at all. The only extra hypothesis is that the V tape is not identically empty:
q_V := π(v ≠ ε) > 0. (The mirror case, a V-level block with π(u ≠ ε) > 0, is symmetric. The case v ≡ ε is the
one-tape case, see §4.)

## 1. Statement
**Thm PR1s.** Let (C, p, w, q) be critical, satisfy (T½), carry a U-level block in some C-rule, and have q_V > 0.
If {pUwVq} ⊆ G⁻, the pair map is not injective. Hence L is ambiguous.
The same holds for the mirror (V-level block, π(u ≠ ε) > 0).

It needs no hypothesis on the V-side blocks. In particular it also re-proves PR2 (a two-sided model is a fortiori
one-sided), with a weaker bound N^{1/2−1/12+o(1)} in place of N^{1/3}.

## 2. Ingredients already proved (cited from r13, audited in audit_r14)
- **MS-mirror** (r13 §1): with a U-level block, C_V := sup{P_W(j) − P_W(n) : W ∈ L, j ≥ |pUw|} < ∞.
  Equivalently, **B(k) ≥ −C_V for every k ≤ |Vq|.** This holds per word and needs nothing on the V blocks.
- **Lemma R** (r13 §3): under (T½) and injectivity, Σ_{n≤N}|L_n|2^{−n} ≥ c₀√N for N ≥ N₀.
- **DW survival** (r13 Lemma K, cited): for the wedge W₁ = {A < B, B ≥ −C} (opening 3π/4), the walk (A, B) from
  the origin has P(τ_{W₁} > m) ≤ c_C m^{−2/3}. This is the only cited input, the same one PR2 uses.

Walk facts (elementary). For k ≤ n/2, the steps of (A, B) under the uniform measure on {a,b}ⁿ are i.i.d. uniform
(±½, ±½). The prefix and suffix letters are disjoint. s_k := B(k) − A(k) is a lazy walk with steps −1, 0, +1 and
probabilities ¼, ½, ¼.

## 3. Proof
### Lemma CM (the conditional-moment step) [written proof, given DW survival]
For m ≥ 2, E[(s_m + 1)·1{τ_{W₁} > m}] ≤ C₁ m^{−1/6}√(log m).

*Proof.* Put λ = √(4m log m).
- On {s_m ≤ λ} the integrand is ≤ (λ + 1)·1{τ > m}, with expectation ≤ (λ + 1)c_C m^{−2/3} = O(m^{−1/6}√log m).
- On {s_m > λ} the integrand is ≤ m + 1. By Hoeffding, P(s_m > λ) ≤ exp(−λ²/(2m)) = m^{−2}.
  So this part is ≤ (m + 1)m^{−2} = O(m^{−1}). ∎

This is the step r13 §5 stated as "E[dist·1{τ > m}] ≲ m^{−1/6} from the DW conditional limit". The truncation shows
that the survival bound alone suffices, up to a √log factor. The DP (§6) shows the true order is m^{−1/6}, with no
log: M1·m^{1/6} = 0.419, 0.393, 0.373, 0.359, 0.348 for m = 8, …, 128, decreasing to a constant.

### Lemma J (wedge then half-plane) [written proof, given DW survival]
For 1 ≤ m and K ≥ 2m: P(τ_{W₁} > m, τ_H > K) ≤ C₂ m^{−1/6}√(log m)·K^{−1/2}, where H = {A < B}.

*Proof.*
1. Apply the Markov property at time m. P(τ_{W₁} > m, τ_H > K) = E[1{τ_{W₁} > m}·φ(s_m)], where φ(x) is the
   probability that the lazy walk from x stays > 0 for K − m ≥ K/2 steps.
2. Skip-free reflection for the symmetric lazy walk S from 0 gives
   φ(x) = P(min_{j ≤ K−m} S_j > −x) = P(|S_{K−m}| < x) + P(S_{K−m} = −x) ≤ (2x + 1)·sup_y P(S_{K−m} = y).
   The local bound sup_y P(S_j = y) ≤ c/√j then gives φ(x) ≤ c'(x + 1)/√K.
3. Lemma CM finishes the proof. ∎

DP check: J(m, K)·m^{1/6}K^{1/2} = 0.335 → 0.348 (K = 2m), 0.340 → 0.355 (K = 4m), 0.342 → 0.357 (K = 8m) for
m = 8 → 128. These are stable, and the local exponent of J(m, 4m) is −0.639, −0.650, −0.657, −0.661, approaching the
predicted −2/3.

### Proof of Thm PR1s
Assume injectivity and L ⊆ G⁻. Fix η > 0, to be chosen, and for large N put R = ⌈η√N⌉ and m = ⌈q_V R/2⌉. Split the
sequences (tokens₁, …, tokens_r) whose word has length ≤ N into three classes.
1. **Short sequences, r ≤ R.** For each r the r-token sequences carry total mass 2^{−|pwq|}·π^{⊗r}(all) = 2^{−|pwq|}.
   So this class has mass ≤ (R + 1)2^{−|pwq|} ≤ 2η√N.
2. **Atypical V tape, r > R and |V| < m.** Then #{i : v_i ≠ ε} < q_V r/2, where this count is Bin(r, q_V) under π^{⊗r}.
   By Chernoff the class has mass ≤ Σ_{r>R} e^{−q_V r/8} = O(1).
3. **The rest, r > R and |V| ≥ m.** By injectivity these sequences give distinct words W ∈ L_n with n ≤ N, n ≥ m and
   |Vq| ≥ m. For each such word:
   - MS-mirror gives B(k) ≥ −C_V for k ≤ |Vq|, in particular for k ≤ min(m, n/2);
   - G⁻ gives A(k) < B(k) for k ≤ n/2.
   So W lies in S_n(m) := {W ∈ {a,b}ⁿ : (A, B) stays in W₁ for k ≤ min(m, ⌊n/2⌋) and in H for k ≤ ⌊n/2⌋}.
   The mass of this class is ≤ Σ_{m≤n≤N} 2^{−n}|S_n(m)|, and 2^{−n}|S_n(m)| is a probability for the uniform walk:
   - for n < 4m it is ≤ P(τ_{W₁} > ⌊n/2⌋) ≤ c n^{−2/3}, which sums to O(m^{1/3}) = O(N^{1/6});
   - for n ≥ 4m, Lemma J with K = ⌊n/2⌋ gives ≤ C₂ m^{−1/6}√(log m)·n^{−1/2}, which sums to
     O(√N·m^{−1/6}√log m) = O(N^{1/2−1/12}√log N).
4. **Contradiction.** Lemma R gives c₀√N ≤ (sum of the three masses), so
   c₀√N ≤ 2η√N + O(1) + O(N^{1/6}) + O(N^{5/12}√log N).
   With η = c₀/4 this fails for large N. So the map is not injective. ∎

**Multiplicity corollary.** The same computation shows that the multiplicity cannot be O(n^{1/12−ε}) on average.
This is weaker than PR2's 1/6 because one wedge phase only lasts m ≍ √N steps.

**Remarks on the hypotheses.**
- q_V > 0 is used only in class 2. Any linear lower bound |V| ≥ c·r off an exponentially small set would do.
- The constant m ≍ √N is forced: the renewal count r is ≍ √N under (T½), so the guaranteed V-region has length ≍ √N,
  whereas n can be as large as N. This is why the gain is only m^{−1/6} = N^{−1/12} and not n^{−1/6}. It suffices,
  because the comparison is against the √N renewal mass with a free constant η.
- The DW conditional limit theorem, the local limit theorem in cones and moment convergence are **not** used.

## 4. One-tape models with a U-level block only (small extension of PR1) [written proof, given DW survival]
PR1 assumed a block that is both U- and V-level. If v ≡ ε and some C-rule has a U-level block (for example a*), the
MS-mirror argument applies to the **whole** word:
1. Prepend a loop ρ carrying a U-level word x with |x| ≥ |W| to the sequence of W. This puts x immediately after p.
2. For k ≤ n' /2 with n' − k still inside the tail of W, the suffix excess B(k) is unchanged, while A(k) ≥ −K − |p|,
   because k ≤ |p| + |x|.
3. G⁻ then forces P_W(j) − P_W(n) ≤ K + |p| + O(1) for **all** j, so B(k) ≥ −C for every k ≤ n.
4. Hence L ⊆ G⁻ ∩ {wedge W₁ for all k ≤ n/2}, whose density is O(n^{−2/3}) (Lemma K). That gives mass O(N^{1/3}) < c√N.

The mirror (u ≡ ε, V-level block) is symmetric. So **every** pair model under (T½) that has a level block on at least one
tape is ambiguous, provided the tapes are not trivially degenerate. If v ≡ ε, §4 applies. If v ≢ ε, PR1s applies.
- *Caveat:* if v ≡ ε and the only level-shaped long words on the U side are "suffix-flat" (b*-type, V-level shape on the
  U tape), use the PR1 step 1 placement instead: put x last, which gives max P ≤ C, and then the wedge W₂. This is the
  same argument. I have not written it beyond this line.

## 5. Exact model tests (n ≤ 22)
`r15_onesided_models.py` enumerates three one-sided candidate token families:
- a*b | {a, b}: critical, with a* U-level and the V side made of single letters;
- a⁺ | {b, ab, ba}: critical;
- (ab)⁺ | {a, b, ε}.
For each, it runs over all (p, w, q) with |p|, |w|, |q| ≤ 2 and reports the longest length up to which some choice
stays both injective and inside G⁻. RESULT (exact, n ≤ 22): no choice survives.
| family | best (p, w, q) | survives to | first failure |
|---|---|---|---|
| a*b \| {a, b} | (bb, aa, aa) | 11 | bbaaaabaabaa ∉ G⁻ (n = 12) |
| a⁺ \| {b, ab, ba} | (bb, ba, aa) | 9 | bbaaababaa ∉ G⁻ (n = 10) |
| (ab)⁺ \| {a, b, ε} | (bb, aa, aa) | 9 | collision at n = 10 (not injective) |

This is consistent with PR1s. These small tests are sanity checks, not evidence for the asymptotic theorem.

## 6. Numerics (`r15_onesided_moment_out.txt`, exact DP, C = 0, m ≤ 128, K ≤ 8m)
| m | P(τ_{W₁} > m)·m^{2/3} | M1·m^{1/6} | J(m, 4m)·m^{1/6}(4m)^{1/2} |
|---|---|---|---|
| 8 | 0.3237 | 0.4194 | 0.3400 |
| 16 | 0.3279 | 0.3931 | 0.3466 |
| 32 | 0.3299 | 0.3733 | 0.3506 |
| 64 | 0.3309 | 0.3587 | 0.3530 |
| 128 | 0.3314 | 0.3482 | 0.3545 |

The local exponents of M1 are −0.260, −0.241, −0.224, −0.210. They drift slowly towards −1/6, because the "+1" term is of
order m^{−2/3} and dominates at small m. Either way M1 = O(m^{−1/6}), which is all the proof uses (with √log).

## 7. What this does and does not close
- Closed: r13 §6 item 3 and audit_r14 caveat C1. "All level-padded classes excluded" is now justified, under (T½) and
  the cited DW survival bound, for two-sided, one-sided and one-tape models.
- Still OPEN: steep models with no level block on either tape (r14 side mismatch), heavier tails −1−2^{−k}, k ≥ 2
  (Lemma R gives only N^{β}), and T8_unamb.
- F1 check: the proof uses the fold geometry (A < B, the 3π/4 wedge) and the density n^{−1/2} of G⁻. Q has density 1,
  so nothing here bears on Q.

## Status
| claim | label |
|---|---|
| Lemma CM: E[(s_m + 1); τ_{W₁} > m] = O(m^{−1/6}√log m) | written proof (given DW survival); DP: true order m^{−1/6} |
| Lemma J: wedge for m steps, then half-plane for K steps, ≲ m^{−1/6}√log m·K^{−1/2} | written proof (given DW survival) + DP |
| **Thm PR1s** (one-sided, q_V > 0, (T½), G⁻ ⇒ ambiguous) | written proof modulo the cited DW survival bound (as PR2) |
| §4 one-tape, U-level only | written proof (sketch-level for the b*-shape variant) |
| Counterexample | none (theorem excludes) |
| T8_unamb | **OPEN** |
