# r6_build.md — R6-A: FOLD-COUNTER, affirmative side

Scripts:
- `scripts/r6_build_kernel.py`: checks Prop K on 3000 random fold automata and runs the mod-3 toy (about 2.5 min).
- `scripts/r6_build_splitA.py`: exhaustive soundness check of L_A for n ≤ 18, plus Monte Carlo of Rot(L_A) (about 1 s).

## Verdict

**No construction found.** FOLD-COUNTER is still OPEN, both for F_K/F_δ and for the root's sharpened target G⁻ (`r6_miss.md`). This round gives three results.

1. **Prop K (finite-state folds are dead)** [written proof + computational check]. Let R be any regular condition on the fold pair sequence. This covers mod-m counters, any DFA, either reading direction, and finite information at the centre. If fold(R) ⊆ Q, then the density of fold(R) is e^{−Ω(n)}. The fooling word is explicit: u^{2j+1}, where j is an idempotent exponent of the DFA's monoid. So the prompt's idea (1) cannot work in any regular form. A fold certificate needs **unbounded memory along the fold spine**, and F_K's single counter is the minimum.
2. **Lemma SA (G⁻ reduces to one length inequality)** [written proof + exhaustive n ≤ 18]. This is a split certificate L_A ⊆ G⁻ ⊆ Q built from two independent one-counter pieces and a single length inequality. Its rotation closure has positive density, ≈ 0.62–0.67 by Monte Carlo for n = 64 to 1024.
3. **Prop N (L_A itself is not CF)** [written proof, pumping on a slice]. The length inequality is exactly where the difficulty sits. I could not find a CF positive-density sub-certificate of L_A or G⁻, and §3 explains why the natural attempts fail.

## 1. Prop K: the kernel obstruction for regular fold conditions

Setting:
- Π = {a,b}² is the pair alphabet.
- For w of length n, z(w) = π_0 … π_{⌊n/2⌋−1}, with π_i = (w_i, w_{n−1−i}).
- c(w) is the centre letter (ε if n is even).
- A fold automaton is a DFA D over Π with an accepting set F ⊆ states × {ε, a, b}.
- fold(D) = {w : (δ(q₀, z(w)), c(w)) ∈ F}. This is exactly what S_q → σ S_{q′} τ grammars generate, and it is unambiguous.

**Prop K.** If fold(D) ⊆ Q, then |fold(D) ∩ Σⁿ| ≤ 2ⁿ·(1 − 4^{−ℓ})^{⌊n/2ℓ⌋} for a constant ℓ = ℓ(D). The density is exponentially small.

*Proof.*
1. Let φ : Π* → M be the transition monoid, and let K be its minimal ideal (the kernel). Fix z₀ with φ(z₀) ∈ K. Every z containing z₀ as a factor has φ(z) ∈ K, because K is an ideal.
2. **Claim.** No y with φ(y) ∈ K is accepted, with any compatible centre. Suppose y were accepted with centre c, and let δ = (c, c) when c ≠ ε (empty otherwise). Put ȳ = swap(reverse(y)), where swap exchanges the two coordinates of every pair.
3. Put g = φ(y δ ȳ) ∈ K. Then g ≤_R φ(y). Both lie in the completely simple kernel, so g R φ(y).
4. Take j ≥ 1 with e = g^j idempotent. Then e R φ(y), so e is a left identity on that R-class and e·φ(y) = φ(y).
5. Let u be the word whose own pair sequence is y δ ȳ, i.e. u = (left letters of y)·c·reverse(right letters of y). Then w = u^{2j+1} has z(w) = (yδȳ)^j y and c(w) = c.
6. So φ(z(w)) = e·φ(y) = φ(y), and w is accepted. But w is not primitive, a contradiction.
7. Hence every accepted word avoids z₀ in its pair sequence, which gives the bound. ∎

**Remarks.**
- The fooling exponent 2j+1 only has to be ≡ 1 modulo the monoid's idempotent exponent. So any finite-state check along the fold confuses p = 1 with p = 2j+1.
- Detecting the zero of d at depth n/p for every p therefore needs unbounded spine memory.
- The even primes alone *can* be handled finite-state. R₃ = {Σ c_i ≢ 0 mod 3} rejects every u^{2r}, because (yȳ)^r has c-sum 0. The check found 0 squares accepted for n ≤ 20. It accepts (ab)⁷.
- The same argument covers block folds S → xSy with |x| = |y| = B: replace Π by Π_B.

**Check.** `r6_build_kernel.py` ran 3000 random DFAs with 2–8 states. Every DFA for which an accepted kernel word exists (2977 of them) was fooled by an explicit non-primitive u^{2j+1} of length at most 115, verified by direct simulation. Not fooled: 0.

## 2. Lemma SA: a split certificate inside G⁻

Notation: h(k) = #a(w[0,k)) − #b(w[0,k)) and H = h(n). Then G⁻ ⟺ d_k < 0 for 1 ≤ k ≤ n/2 ⟺ **h(k) + h(n−k) < H for all 0 < k < n**, which is symmetric in k ↔ n−k.

**L_A** = { x·y : x is a b-first Dyck word (h ≤ 0 on x, h(|x|) = 0); every nonempty suffix of y has more a's than b's; **|x| ≥ |y|** }.

**Lemma SA.** L_A ⊆ G⁻ ⊆ Q.

*Proof.* Let s = |x| ≥ n/2. Then H ≥ 1, and h < H on (s, n).
- If k ≤ n/2 ≤ s, then h(k) ≤ 0.
- If n−k ≥ s, then h(n−k) < H.
- If n−k < s, then h(n−k) ≤ 0 < H.
- In every case h(k) + h(n−k) < H. ∎

**Checks.**
- Exhaustive for n ≤ 18: L_A ⊆ G⁻, with 0 non-primitive words.
- Monte Carlo: P(some rotation of w or of swap(w) lies in L_A) ≈ 0.62 at n = 64, 0.67 at n = 256 (400 samples each), and 0.62 at n = 1024 (150 samples). So **Rot(L_A ∪ swap L_A) has positive density** [MC only].
- If L_A (or any positive-density-after-rotation part of it) had a poly-ambiguous CFG, the exact cyclic closure of `cyclic.md` would answer DENSE-SOUND affirmatively. Swap is a letter morphism, so it preserves tree counts. Without the length inequality, the pieces are trivially CF: D_b·P has ambiguity ≤ n, from the choice of split.

**Why |x| ≥ |y| cannot be dropped.** Without it, baa·baa ∈ D_b·P, which is a square. Threshold or step-function substitutes do not help: if h ≤ θ(k) with θ a step function, then G⁻ needs θ(k) + θ(n−k) < H. When both k and n−k lie past the step, this forces the step to sit at ≥ n/2. So some split at the centre is unavoidable.

## 3. Prop N: L_A is not CF, and where every attempt breaks

**Prop N.** L_A is not context-free.

*Proof.*
1. Exhaustively, for i, i′ ≤ 14 and l < 40, L_A ∩ b⁺a⁺ba⁺ consists of the words bⁱ a^{i′} b a^l with:
   - l ∈ [i−i′+2, 3i−i′+3] if i′ ≤ i;
   - l ∈ [2, 3i−i′−1] if i′ > i.

   The general description follows from the s-rule: take s to be the last zero before the walk first reaches +1.
2. Take bᴺ aᴺ b a^{2N+3} with N greater than the pumping constant.
3. Pumps containing the middle b, or straddling a block boundary, leave the slice.
4. Pumping the b-block alone fails at t = 0. Pumping the first a-block alone, a^l alone, or (a^{i′}, a^l) fails at t = 2.
5. Pump (bⁱ, a^{i′}) by (α, β):
   - t = 2 needs β ≤ α or β + 4 ≤ 3α;
   - t = 0 needs β ≥ 3α;
   - these are incompatible unless α = β = 0.
6. Pumping bⁱ together with a^l is impossible, since |vwx| < N. ∎

G⁻ itself contains all of b⁺a⁺ba⁺, so Prop N says nothing about G⁻ or about dense subsets of L_A.

**The common failure (assessment).** Every sound certificate I tried has the same two parts:
- a long left structure with a counter (Dyck x, or the d-walk);
- a long right structure with a counter (P for y);
- a length coupling between them of order Θ(n).

A CFG can couple lengths only along one spine, where it has finite state. Each counter then needs its own non-crossing arcs, and these cross the coupling arcs.

I tried several routes:
- **Couple primes, not letters.** Hang the Dyck primes of x and the blocks E·a of y off a common spine. This is CF, but it compares *numbers* of blocks, not lengths. A random Dyck path has O(1) returns and the spine has O(√n) steps, so the coupling fails on typical words.
- **Bounded y-blocks.** This needs y's suffix-majority as finite state on the spine, which by Prop K-type reasoning (or simply rarity) gives density 0.
- **Recursion into y.** The pairs (k, n−k) with k > s are centred at n/2, not at the centre of y, so G⁻ does not recurse into y.

This is consistent with r5's Theorem P_K and with Prop K above. The remaining affirmative hope is a branching mechanism that couples two Θ(n) one-counter structures by length on a positive-density set. I have no candidate.

## Status

| claim | label |
|---|---|
| Prop K: regular fold conditions, if sound, have density e^{−Ω(n)}; explicit fooling word u^{2j+1} | written proof; 2977/2977 random DFAs fooled |
| Even-p-only fold certificate R₃ (d_{n/2} ≢ 0 mod 3) | written; exhaustive check, no squares accepted for n ≤ 20 |
| Lemma SA: L_A ⊆ G⁻ ⊆ Q | written proof; exhaustive n ≤ 18 |
| Rot(L_A ∪ swap L_A) has density ≈ 0.62–0.67 | MC n ≤ 1024 |
| Prop N: L_A not CF | written proof (pumping on b⁺a⁺ba⁺); slice description checked i, i′ ≤ 14, l < 40 (written derivation sketched) |
| CF positive-density subset of F_K / F_δ / G⁻ / L_A | **OPEN** (FOLD-COUNTER unresolved) |
