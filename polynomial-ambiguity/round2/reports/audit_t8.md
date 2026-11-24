# audit_t8.md — R17b gated audit: r17_oh_level (Thm OH) and the T8_unamb assembly

Script: `scripts/audit_t8_checks.py` → `scripts/audit_t8_checks_out.txt` (own code: MS^in brute force, exact DP for
Lemma D, exhaustive Lemma L check on critical Polish grammars).

## Verdict
| candidate | verdict |
|---|---|
| Lemma L (heavy ⇒ U-(log-)level AND V-(log-)level) | **SURVIVES** |
| Lemma MS^in (innermost V-level insertion ⇒ A ≤ max_{j≤\|Vq\|}B + c + c log n on k ≤ \|pU\|) | **SURVIVES** |
| Lemma D (barrier-set density ≲ polylog·M^{3/4}/n) | **SURVIVES** (constant is (C+1)^{1/2}, not (C+1)^{3/2}; harmless) |
| Thm OH (one-sided heavy, any β₀, any q_V ≥ 0, incl. one-tape) | **SURVIVES** with caveats C1–C4 |
| T8_unamb assembly | **COMPLETE as a case split.** Every case is covered. It is **conditional** on links that have never had a gated audit (§4) |

No fatal flaw.

## 1. Lemma L
- **SM gives both signs.**
  - Fix the Lemma Bot form (α, β, γ), d = D(αβγ).
  - If some w₀ has D(w₀) + d ≥ 0, this is a choice with e ≥ 0. Otherwise SM(U) applies, and its proof (Step 3, read
    as audit_r16 C3) builds a *new* C*-form with e = 0.
  - In the same way, either some w₀ has e ≤ 0 or SM(V) builds an e = 0 form.
  - Both are statements about L(Y) for the same Y with H ⇒* sYt. Which tape H sits on plays no role.
- **HL is side-agnostic and form-agnostic.**
  - I re-derived Lemma PC (the region-by-region shift argument) and Prop HL.
  - e > 0: the cycle (αT_kβ, γ) has D(v) = 2^k e − d + D(αβ) → +∞ and total 2^k e ≥ 0, so PC(U) applies.
  - e < 0: the cycle (α, βT_kγ) with PC(V).
  - e = 0: depth and suffix excess grow by ≤ c per doubling.
  - These steps use only Y ⇒* αYβYγ with terminal α, β, γ and the context s, t. "U-level" and "V-level" are properties
    of the word set L(H), not of the tape H sits on.
- So every heavy H is both U-(log-)level and V-(log-)level. The log family has length ratio → 2, so a word with length in
  [n, 2n + c] exists, as MS^in and MS⁺ need.
- **Independent check (Test 1).** I took all 100 critical nonlinear Polish grammars Y → fY^{k_f} (complete prefix code
  with ≤ 4 words, depth ≤ 3, arity ≤ 3) and ran an exact DP for min depth and min max-suffix-sum per length, up to ℓ = 26.
  - Every grammar has, at every large length, words with depth ≤ 1 **and** words with suffix excess ≤ 1.
  - The values up to 7 occur only at short or sparse lengths, and they fall to 1 (or 0) by ℓ ≈ 30 (checked to 44).
  - Both shapes are present everywhere.
- **Consequence.** audit_r17 C3's "U-level but not V-level heavy block (HL e > 0 branch)" is **empty**, and so is
  r16 §5's "U-level only" scope flag. Both are superseded.

**Root questions.**
- **(i) Late-rise U blocks such as {(ba)^m a^m}.** This block has radius 1 > ½, so it is light and is never used. Lemma L
  only needs the *heavy* block, which exists by Cor H and is V-(log-)level. Even if a heavy H also contains late-rise
  words, PC exhibits its flat words s·x_i·t directly, so condition (F) of r17_oh_region always holds for the heavy block.
- **(ii) A V-tape block with infinite mean that is not V-level.** This cannot happen. Σπ = 1 gives μ < ∞, so an
  infinite-mean block is heavy, and Lemma L makes it V-(log-)level. The model is then two-sided and PR2⁺ applies
  (log form, audit_r17 C2).
- **(iii) Does Thm OH implicitly use A ≤ C from MS⁺?** No.
  - Step 2 uses only MS⁺(b), B ≥ −C_n, which is valid one-sided: its U-level word comes from Lemma L.
  - The A-barrier is the random height max_{j≤m}B + a_n from MS^in.
  - In §4.1, the constant A-barrier of PR1 comes from MS^in with m = |q|, not from MS⁺.

## 2. Lemma MS^in
- **Geometry.** Appending ρ as token r+1 gives W' = p U (αxβ) w v_ρ V q ∈ L. This is a legal token sequence.
  - A_{W'} = A_W on k ≤ |pU|.
  - The last m = |Vq| letters are unchanged, so B_{W'} = B_W on k ≤ m.
  - Then B crosses v_ρ w β (fixed) and then x from its end. Suffix drift ≤ K gives B_{W'} ≤ D(Vq) + c₁ + K
    ≤ max_{j≤m}B_W(j) + c₁ + K.
  - n' ≥ 2n gives k ≤ |pU| ≤ n ≤ n'/2.
  - |x| ≥ n gives k ≤ m + c₁ + |x|.
  - The fold centre of W' lies right of every k that is used.
- **Test 2.** Random p, U, w, V, q, α, β, v_ρ and random V-level x with K ∈ [0, 3] and |x| ∈ [n, 3n + 2]. I checked
  A_{W'} = A_W, 2k ≤ n', the bound B_{W'}(k) ≤ barrier, and the implication G⁻(W') ⇒ A_W(k) < barrier.
  **34,190 checks, 0 violations.**

## 3. Lemma D and the exponents
- **Lemma D re-derived.**
  - Ballot for A gives c(H+a+1)/√T.
  - B survives on (M, T] with probability c(B(M)+C+1)/√T.
  - Cauchy–Schwarz then gives ‖(H+a+C+1)²‖₂·P(τ>M)^{1/2} ≲ (M+(a+C+1)²)(C+1)^{1/2}M^{−1/4}.
- **Test 3, my own exact DP** (C = a = 1, ±1 steps): n·dens/√M = 5.11, 4.40, 3.45 at n = 256 (M = 4, 16, 64).
  - This reproduces r17's numbers to 3 digits.
  - n = 2048 gives 5.30, 4.87, 4.65, so the value stays bounded.
  - The growth in C = a is polynomial (n·dens = 19, 57, 133, 349 for C = 1, 4, 8, 16), so log-level constants cost only
    polylog factors.
- **Exponents.**
  - Class 1 has mass Σ_{n≤N} n^{−1+3γ/4} polylog n = O(N^{3γ/4} polylog). This is o(N^{β₀}) ⟺ γ < 4β₀/3.
  - Class 2 needs γ > β₀, because exp(−c r^{1−β₀/γ}) is summable.
  - The interval (β₀, 4β₀/3) is non-empty for every β₀ > 0, and γ < 2/3 < 1 keeps M_n ≤ n/4.
  - Class 1 has m ≤ n^γ, so |pU| ≥ n/2 and MS^in covers all k ≤ T.
  - In class 2, |W|^γ < m ≤ 2μ_V r + |q| forces |U_r| < (c′r)^{1/γ}.
  - Correct.

## Caveats
- **C1.** "For every W ∈ L" should read "for every pair-model word" (as in audit_r17 C1).
- **C2.** The Lemma D constant is (C+1)^{1/2}, not (C+1)^{3/2}. This is harmless.
- **C3.** Lemma L should be recorded as a corollary of SM + HL. It makes audit_r17 C3's uncovered case, and r16 §5's
  flag, vacuous.
- **C4.** B–D Thm 3 is cited (not re-checked) in three places:
  - (a) F̄ = O(y^{−β₀}), for Lemma R;
  - (b) the lower tail P(|u| > y) ≥ c y^{−β₀} for the heaviest U block (the residue-class ≍ suffices after summing);
  - (c) "finite mean ⇒ radius > ½" for V blocks, i.e. no exponent in (1, ∞) for a finite-valued N-algebraic series.
  - The exponential moment of |v| also uses the geometric step count (ρ(M|_{C∖X}) < 1, audit_r14 C4).

## 4. T8_unamb assembly
Suppose L ⊆ G⁻ is unambiguous and rotation-dense, meaning |Rot(L)_n| ≥ δ2ⁿ for all large n.
- **0.** Thm M(i): μ(L) = ∞ (trivial).
- **1.** Lemma F: the lowest SCC C with μ = ∞ is linear, with ρ(M(½)) = 1. This uses the DLW finite value at the
  singularity for nonlinear SCCs.
- **2.** Pair model (r10 §2 / r13 §0): first-return tokens, Σπ = 1, and the pair map is injective by unambiguity.
- **Case split** (lower blocks in loop rules of C, by side):

| case | covered by |
|---|---|
| (a) all loop blocks have finite mean (heavy blocks in the exit word or context only, or none) | Lemma Rn, renewal theorem (exit word fixed) |
| (b) heavy blocks on both tapes | Lemma L ⇒ U-level on U, V-level on V ⇒ PR2⁺ in log form (audit_r17 C2), any tail |
| (c) heavy on the U tape only, any q_V ≥ 0, including one-tape q_V = 0 | **Thm OH** (this candidate) |
| (d) heavy on the V tape only | mirror of Thm OH |
| side mismatch / steep | impossible (Lemma L ⊇ SM) |

PR1, PR1s, PR2, PR2^β and r15_onesided are no longer needed. They are subsumed by OH and PR2⁺.

**Verdict: COMPLETE (every case is covered), conditional on these links.**
- Never gated-audited:
  - r9 Lemma F, Lemma Rn and Cor H;
  - r10 §2 pair-model reduction;
  - r14 Lemma Bot.
- r14 Lemma PC and Prop HL were re-derived in this audit (§1) and are correct.
- Lemma R was audited in audit_r14, and its β₀ form in audit_r17.
- Cited theorems, not re-checked:
  - Banderier–Drmota Thm 3: its hypotheses (general, non-strongly-connected N-algebraic systems, residue classes)
    must cover the block GFs;
  - Drmota–Lalley–Woods;
  - the Markov/Erdős–Feller–Pollard renewal theorem.
- Recommendation: a gated audit of r9 §2–3 and r14 Lemma Bot, then promote T8_unamb to [written proof, audited, modulo
  citations].
