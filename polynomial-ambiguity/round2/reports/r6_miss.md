# r6_miss.md — R6: what the fold certificates miss

Scripts (all in `scripts/`):
- `r6_miss_lib.c`: tier membership (C, via ctypes).
- `r6_miss_exh.py`: exhaustive run for n ≤ 30, about 40 s on 14 threads. Its output is saved as `r6_miss_exh_out.txt`.
- `r6_miss_mc.py`: Monte Carlo up to n = 10⁴. Its output is saved as `r6_miss_mc_out.txt`.
- `r6_miss_windows.py`: sound-window search.
- `r6_miss_lemmaA.py`: exhaustive check of Lemma A for n ≤ 18.

Notation:
- d_k(v) = #a(pre_k v) − #a(suf_k v) for 1 ≤ k ≤ n/2.
- T_w(i) = n·#a(w[0,i)) − i·#a(w), read cyclically. This is the drift-corrected walk, and T(i) = T(j) iff the window w[i,j) has a-density exactly A/n.
- g = gcd(#a, #b).

## Verdict

1. **E is empty for n ≤ 30 once rotations are allowed** [computational, exhaustive]. Rotating the fold costs nothing in soundness. Rot(F_K) alone misses only 1200, 2392, 432, 5040 and 31080 words at n = 24, 26, 27, 28 and 30. Every one of these is certified by the feature version or by the r4 gadget library. Without rotation, F_K misses about 40% of Q at every n.
2. **New sound certificate G⁻ (no window at all)** [written proof + exh]. Let G⁻ = {v : d_k(v) < 0 for all 1 ≤ k ≤ n/2} ⊆ Q. By **Lemma A**, Rot(G⁻) contains every word whose T has a unique argmax. Hence Rot(G⁻) ⊇ {g = 1}, and its miss rate is ≤ P(argmax not unique) ≈ 0.43·n^{−1/2} → 0 [MC to n = 7680].
3. **Single-prime rotation rigidity (Lemma R)** [written proof]. Rot(F_max) = Q_n whenever n is a prime power. Its miss set needs ω(n) ≥ 2, with different rotations "palindromic" for different primes.
4. **Windows (Prop W)** [written proof + exact search]. The interval windows sound for all n are exactly those containing [1/3, 1/2]. Since 2 | n and 3 | n are regular properties, residue-dependent windows are allowed and raise the density from 0.608 to between 0.69 and 0.76.
5. **Density conclusion.** The union of sound fold-type certificates has density → 1, and one fixed language already gets there: Rot(G⁻). Suppose FOLD-COUNTER were solved for G⁻, i.e. a poly-ambiguous CF L ⊆ G⁻ containing the argmax rotation of most words. Then what remains is the **tie family** 𝒯 = {w : T_w attains its max at ≥ 2 points}. 𝒯 ⊆ {g ≥ 2}, its density is Θ(n^{−1/2}), and its ties lie at distances in (n/g)ℤ. The miss set of Rot(F_K) is far smaller still: it sits inside the double-tie family (argmax and argmin both non-unique) and is observed to decay faster than any power for n ≤ 48. CF-ness of G⁻ is **OPEN**; this is the sharpened FOLD-COUNTER.

## 1. Soundness lemmas [written proofs]

**Lemma M (exact soundness criterion for folds on w).** Let K ⊆ [1, n/2]. Then F_K = {w : d_k ≠ 0 ∀k ∈ K} ⊆ Q_n **iff**, for every prime p | n, K contains a multiple of n/p.

*Proof (⇐).* Lemma F of r5. If w = u^p, then pre_{jm} = u^j = suf_{jm}, where m = n/p.

*Proof (⇒).* Suppose K misses (n/p)ℤ, and let m = n/p ≥ 2. Put u = a b^{m−1} and w = u^p. For k = jm + t with 0 < t < m, we get d_k = #a(u[0,t)) − #a(u[m−t,m)) = 1 − 0 ≠ 0. So w ∈ F_K but w is not primitive.

If m = 1, then (n/p)ℤ covers everything and K ≠ ∅ suffices. ∎

The same criterion and proof hold for every window feature x^φ, by Lemma S(i) of r4_core: x^φ is (n/p)-periodic on u^p.

**Corollaries (all sound).**
- F_max = ∪_{sound K} F_K = {w : for every prime p | n, the p-block a-count vector (c_0..c_{p−1}), with blocks of length n/p, is not a palindrome}. This holds because d_{jm} = Σ_{i<j}(c_i − c_{p−1−i}).
- Rot(X) for any sound X, since primitivity is rotation-invariant. Reversal and a↔b swap only flip the sign of d, so they add nothing.
- The feature versions use x^a, x^{aa} and x^{ab}, read cyclically.

**Lemma R (rotation rigidity, one prime).** Fix a prime p | n and a feature x ∈ {0,1}^n. If every rotation of x has a palindromic p-block vector, then x is (n/p)-periodic.

*Proof.* Let m = n/p and γ(r) = Σ x[r, r+m). Palindromicity at rotation r gives c_0 = c_{p−1}, that is γ(r) = γ(r−m) for all r, so γ is m-periodic. Then the difference γ(r+1) − γ(r) = x_{r+m} − x_r is m-periodic too. So along each coset r + mℤ, x is an arithmetic progression of length p on a cycle, with common difference δ and pδ = 0. Hence δ = 0. ∎

*Consequence.* If n = q^e, then Rot(F_max) = Q_n. Moreover, Rot(F_max)-miss ⟹ ℤ_n = ∪_{p|n} R_p with each R_p ≠ ℤ_n, where R_p is the set of rotations that are p-palindromic. So it needs ω(n) ≥ 2.

**Lemma A (argmax rotation).** Let the rotation v = w[r..]w[..r) start at an argmax r of T. Then d_k(v) = T(r+k) + T(r−k) − 2T(r) ≤ 0 for all k. If the argmax is unique (mod n), every inequality is strict for 1 ≤ k ≤ n/2, so v ∈ G⁻.

*Proof.* The two windows have equal length k, so the drift terms cancel. ∎

G⁻ ⊆ F_K for every K, so G⁻ ⊆ Q.

If g = 1, then T(i) = T(j) with i ≢ j would need n | (j−i)·A, which is impossible. So the argmax is unique and w ∈ Rot(G⁻).

`r6_miss_lemmaA.py` checks exhaustively for n ≤ 18 that Lemma A has 0 failures and that G⁻ accepts no non-primitive word.

**Lemma A' (structure of the Rot(F_K)-miss set).** If w ∉ Rot(F_K), then g ≥ 2 and both argmax T and argmin T have ≥ 2 elements. Each argmax r has k ∈ K with r ± k also an argmax, and all such ties lie in r + (n/g)ℤ.

*Proof.* Lemma A, together with its mirror for argmin (where d_k ≥ 0). ∎

The MC asserts this on about 1.5·10⁶ samples, and the exhaustive n ≤ 30 data agree (§2).

**Prop W (sound interval windows)** [written proof + exact Farey search, `r6_miss_windows.py`]. By Lemma M, a window [αn, βn] is sound for all n iff [α, β] contains some j/p (1 ≤ j ≤ p/2) for every prime p.
- p = 2 forces β = 1/2.
- p = 3 forces α ≤ 1/3, because j = 1 is the only choice.
- So **[1/3, 1/2] is the unique minimal all-n window.**
- Any interval of length L > 0 is sound for every p > 1/L; only finitely many primes are exceptions, which is the F_δ construction.

Windows may also depend on whether 2 | n and 3 | n, which is regular. The windows maximising α/β among Farey endpoints with denominator < 60 are shown below. The BM no-zero probability is (2/π)·asin√(α/β).

| class of n | window | BM density | MC (n) |
|---|---|---|---|
| 6 \| n | [1/3, 1/2] | 0.608 | 0.60 |
| 2 \| n, 3 ∤ n | [2/5, 1/2] | 0.705 | 0.708 (1024), 0.694 (10⁴) |
| 3 \| n, 2 ∤ n | [1/3, 3/7] | 0.688 | — |
| gcd(n, 6) = 1 | [2/5, 6/13] | 0.762 | exh. n = 25: 0.744, n = 29: 0.764 |

This is F_W, tier bit 8. It is the best *pure-sign single-interval* certificate. It still has a constant miss rate.

## 2. Exhaustive results (n ≤ 30)

The tiers below are densities inside Q_n.
- **Soundness check:** 0 non-primitive words with a nonzero tier mask, for n ≤ 20, all 10 tiers.
- The non-rotated tiers F_K, F_max and F_W have constant or slowly decaying miss rates. F_max takes values like 0.70 at n = 24 and 0.9999 at n = 29 (prime n: only the palindrome test with p = n).

| n | \|Q_n\| | F_K | F_max | F_W | Rot F_K miss (words/classes) | Rot F_max miss | Rot F_K∪feat, Rot F_max feat miss |
|---|---|---|---|---|---|---|---|
| ≤ 23, 25, 29 | | .56–.65 | .59–1 | .57–.82 | 0 | 0 | 0 |
| 24 | 16772880 | .577 | .696 | .577 | 1200 / 17 | 48 / 1 | 0 |
| 26 | 67100670 | .596 | .844 | .701 | 2392 / 26 | 0 | 0 |
| 27 | 134217216 | .596 | .815 | .674 | 432 / 5 | 0 | 0 |
| 28 | 268419060 | .612 | .838 | .713 | 5040 / 54 | 0 | 0 |
| 30 | 1073708010 | .583 | .704 | .583 | 31080 / 286 | 600 / 6 | 0 |

Classes are counted up to rotation, reversal and swap.

**E_n.** Let E_n = Q_n ∖ (fold tiers ∪ r4 gadget library). Then |E_n| = 0 for all n ≤ 30.
- For n ≤ 28: every one of the 76 U-classes of `r4_core_U.txt` is certified by Rot(F_K) (all 10 tiers fire on most of them).
- For n = 29, 30: the feature-rotation tiers alone cover all of Q_n.
- So |E_n| = 0 even if the gadgets are dropped and only {Rot F_K with features} is kept.

**Structure of the Rot(F_K)-miss classes** (n = 24 … 30; output from `r6_miss_exh.py`).
- g ∈ {2, 3, 4, 6, 8, 10, 12, 14, 15}. **Always g ≥ 2**, as Lemma A' requires.
- (#argmax T, #argmin T) ≥ (2, 2) always. The most common case is exactly (2, 2), an antipodal pair of ties.
- The Hamming distance to the nearest u^p is 2 to 8, so these are near-powers. The typical form is u₁u₂ with equal-Parikh halves differing by a few transpositions. Example: aaaaaabababb·aaaaaabbaabb.
- x̂(1) = 0 in only 7 of the 388 classes.
- Primes with a p-palindromic rotation: the class always uses ≥ 1 prime, mostly {2}, {2,3} or {2,3,5}. At n = 27 = 3³ (g = 3), the misses use p = 3 only. This does not contradict Lemma R: Rot(F_K) is weaker than Rot(F_max).

**Structure of the Rot(F_max)-miss classes:**
- n = 24: one class, aabababbabaababbaababbab, with g = 12. Its rotations are split between p = 2 and p = 3.
- n = 30: 6 classes, with g = 6 and primes {2, 3, 5}.
- All of them have **x̂(1) = 0** and Hamming distance 4 to 6 to the nearest power.
- Only n with ω(n) ≥ 2 occur (Lemma R).
- None survives the feature tiers.

## 3. Monte Carlo (`r6_miss_mc.py`)

The table gives miss rates, i.e. 1 − density. "g6|" means words with #a = 6⌊n/12⌉, so that g has the two prime factors 2 and 3.

| n | F_K | F_W | F_max | F_max (g6\|) | all Rot tiers (unif and g6\|) |
|---|---|---|---|---|---|
| 60 | .39 | .39 | .20 | .29 | 0 / 2000 |
| 256 | .38 | .29 | .046 | — | 0 / 2000 |
| 1024 | .39 | .29 | .030 | — | 0 / 2000 |
| 2310 | .39 | .39 | .036 | .058 | 0 / 2000 |
| 9240 | .42 | .42 | .012 | .034 | 0 / 500 |
| 10000 | .39 | .31 | .010 | — | 0 / 500 |

**Decay of the Rot(F_K) miss rate** (2·10⁵ samples per n):

| n | 24 | 30 | 36 | 48 | 60 | 90 | 120 | 210 | 420 |
|---|---|---|---|---|---|---|---|---|---|
| miss, uniform | 3.3e−4 | 7.5e−5 | 5e−6 | 0 | 0 | 0 | 0 | 0 | 0 |
| miss, g6\| | 5.8e−4 | 8e−5 | 4e−5 | 0 | 0 | 0 | 0 | 0 | 0 |
| P(double tie) | .047 | .043 | .036 | .030 | .027 | .022 | .019 | .013 | .010 |

For n ≥ 210 the uniform miss rate is out of 5·10⁴ samples and the g6| rate out of 1.25·10⁴.

**P(#argmax T ≥ 2)** (2·10⁴ samples per n) is ≈ 0.43·n^{−1/2}. It bounds the miss rate of Rot(G⁻):
- n = 30: .117
- n = 240: .032
- n = 1920: .0098
- n = 7680: .0048

**Restricted to g with ≥ 2 prime factors.** The rotation tiers still show 0 misses. F_max misses about 3× more often, because g6| makes block-count ties likelier, but the rate still → 0.

## 4. Conclusion for FOLD-COUNTER

- **Density → 1 for fold-type certificates: yes.**
  - [written proof of soundness; density → 1 by MC + the tie heuristic below]
  - F_δ gives 1 − O(√δ) for each fixed δ (r5).
  - F_max (non-rotated) has miss rate ~ Σ_{p|n} P(p-block palindrome) = O(ω(n)·n^{−1/2}). It needs n-dependent single depths, which makes it less grammar-friendly.
  - **Rot(G⁻), a single fixed language with no window and no n-arithmetic, has miss rate ≤ P(tie) ≍ n^{−1/2}.**
  - Rot(F_K) does even better: it misses only double ties with the midpoint property, at < 10⁻⁵ for n ≥ 36.
- **The remaining family** after Rot(G⁻) is the tie family 𝒯 = {w : two cyclic windows of complementary lengths both have a-density exactly #a/n, at the maximum of T}. It is structured: 𝒯 ⊆ {g ≥ 2}, and the ties sit at distances in (n/g)ℤ.
  - Its density is Θ(n^{−1/2}), so it is not exponentially small.
  - After Rot(F_K), the remaining set at n ≤ 30 consists of near-powers at Hamming distance ≤ 8 with (≥ 2, ≥ 2) ties.
- **Realisation**:
  - Rot(L) is CF for CF L (classical; Oshiba / Maslov).
  - The standard cut-along-a-path construction gives amb_{Rot L}(z) = Σ_i amb_L(rot_i z) ≤ n·amb_L [sketch, not re-verified].
  - So the sharpened question is **ROT-FOLD-BALLOT**: is there a poly-ambiguous CF L ⊆ G⁻ (fold of the ballot language "all prefix sums of e < 0" over pairs) that contains the argmax rotation of a 1 − o(1) (or positive) fraction of words?
  - Theorem P_K / Prop P do not obstruct this. Those bounds are on the density of L itself, and here even all of G⁻ is sparse: each word puts only about one rotation into it. The density comes from rotating L. That sparsity is new compared with F_K.
  - **OPEN.**
- Caveat: Lemma A uses the *full* window [1, n/2]. Requiring negativity from k = 1 is a ballot condition at the fold centre's outer end, the same crossing-arcs issue as r5 §1. Nothing here makes it easier to realise as a CFG.

## Status

| claim | label |
|---|---|
| Lemma M (exact soundness criterion), Lemma R, Lemma A / A', Prop W | written proof; Lemma A and the tiers checked exhaustively (n ≤ 18 and n ≤ 20) |
| \|E_n\| = 0 for n ≤ 30; miss tables and structure | computational (exhaustive) |
| Rot(F_K) and Rot(G⁻) density → 1; P(tie) ≈ 0.43/√n | MC + heuristic (not proved) |
| Ambiguity of the rotation closure ≤ n·amb | sketch |
| G⁻, or a rotation-dense subset of it, is CF / poly-ambiguous | OPEN (ROT-FOLD-BALLOT) |
