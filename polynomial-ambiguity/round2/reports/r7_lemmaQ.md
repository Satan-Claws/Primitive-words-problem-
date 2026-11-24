# r7_lemmaQ.md — R7-B: Lemma Q via polynomial ambiguity (negative side)

Status: final (see Verdict).

Scripts: `round2/scripts/r7_lemmaQ_ctx.py` (Q0 counterexample, <1 s).

## Q0. Lemma Q as stated is false (context dependence) [written proof + exhaustive check m = 10]
The quotient P⁻¹G⁻S⁻¹ is not a function of (t, h). Take P = b, S = bʳ a^{m+1}, |x| = m.
Then h = 1 (d_1 = −1), t = r + m, and x lies left of centre, paired letter-by-letter with the block a^m.
Every increment [x_i = a] − 1 is ≤ 0 and the bʳ block only lowers d, so P x S ∈ G⁻ for all x:
the quotient has density 1 although h/√m → 0. (Script: density 1.0 for r = 0, 2, 4; the t = 0, h = 1 quotient has density 0.45 at m = 10.)
So any Lemma Q must depend on the paired window of the context, not only on (t, h).

Scripts (cont.): `round2/scripts/r7_lemmaQ_rect.py` (centre rectangles, DP to N = 2000, ~10 s).

## Verdict (final)
**NOT resolved.** Three results and a sharpened gap:
- **Q0**: Lemma Q as stated in r6 §4 is false (above). The right object is not the quotient but the *centre-spine rectangle*.
- **Lemma R** (centre rectangles of G⁻ sit exactly at the rotation threshold) [written proof modulo KMT + Prékopa; DP check].
- **Prop S** (unambiguous, fixed centre spine ⇒ n^{−3/2}) [written proof modulo standard algebraic-coefficient asymptotics]. Uses set-level
  closure (uncoupled lengths stay in L ⊆ G⁻) + exact counts (unambiguity ⇒ disjointness + regular variation). Not a §6 count-only route.
- **Gap**: uniformity of Prop S in the spine; and the ambiguity loss in the disjointness step (exactly n^k for amb ≤ n^k).

## 1. Spine rectangles (any grammar) [written, standard]
Fix a tree of w ∈ L_n (n = 2N+1 odd for simplicity; even n is the same with ε centre). Let s be the *centre spine*: the sequence of productions
from the root to the leaf at position N. The hanging nonterminals give X_s = L(A_1)⋯L(A_t) (left, in order) and Y_s = L(B_t)⋯L(B_1), and a
centre letter c_s. Every x ∈ X_s, y ∈ Y_s gives a valid tree, so **X_s · c_s · Y_s ⊆ L for all lengths** (uncoupled). Its centred slice
(X_s)_N × (Y_s)_N is a left/right rectangle inside G⁻, and L_n = ⋃_s (X_s)_N c_s (Y_s)_N (disjoint if G is unambiguous).

## 2. Lemma R: centre rectangles are ≤ polylog · 2ⁿ/n
**Lemma R.** If X, Y ⊆ Σ^N and X·c·Y ⊆ G⁻, then |X|·|Y| ≤ C (log N)² 4^N / N.

*Proof.* For k ≤ N, d_k(xcy) = F_x(k) − R_y(k), with F_x(k) = #a(x[0,k)), R_y(k) = #a(suf_k y). Put g(k) = max_{x∈X} F_x(k).
Then X ⊆ {F ≤ g}, Y ⊆ {R > g}, so |X||Y|/4^N ≤ P(S ≤ γ)·P(S ≥ γ), where S is the centred simple walk (F − k/2) and γ = g − k/2.
(KMT) Couple S with a Gaussian walk W so that max_{k≤N} |S_k − W_k| ≤ C log N off an event of probability N^{−10}. Then
P(S ≤ γ)P(S ≥ γ) ≤ P(W ≤ γ + c)P(W ≥ γ − c) + 2N^{−10}, with c = C log N.
(Prékopa) γ ↦ P(W ≤ γ + c) is log-concave on ℝ^N ({(x, γ) : x ≤ γ + c} is convex, W is Gaussian), and so is γ ↦ P(W ≥ γ − c).
The sum φ(γ) of their logs is concave, and φ(−γ) = φ(γ) because W =ᵈ −W. So φ is maximised at γ = 0, which gives
P(W ≤ c)P(W ≥ −c) ≤ (C′ log N/√N)² by the ballot estimate. ∎

DP check (`r7_lemmaQ_rect.py`, g = k/2 + λ√k, N = 500 → 2000): the fitted exponent is −0.999 at λ = 0, −1.05 at λ = ±0.25,
−1.19 at ±0.5 and −1.76 at ±1. It is symmetric, with its maximum at λ = 0, exactly as the evenness argument predicts.
[conjecture: the log² can be removed (discrete Prékopa).]
*Meaning.* A single centre rectangle can reach density ≍ 1/n (X = b-dominant prefixes, Y = a-dominant suffixes), which is exactly the
rotation-dense threshold. So rectangles alone give nothing (cf. N3). Some *uncoupled* closure is needed, and §3 uses it.

## 3. Prop S: unambiguous + fixed spine ⇒ O_s(2ⁿ n^{−3/2})
**Prop S.** Let G be unambiguous with L(G) ⊆ G⁻, and fix a centre spine s. Then
|{w ∈ L_n : centre spine s}| ≤ C_s 2ⁿ n^{−3/2} for all n ≥ n_0(s).

*Proof.*
1. (set level, uncoupled closure) For each a, the words x c_s y with |x| = a, |y| = n−1−a are in L_n. By unambiguity they are pairwise
   distinct, across different a as well, since a word with two such splits would have two trees. So Σ_a |X_{s,a}||Y_{s,n−1−a}| ≤ |G⁻_n| ≤ C 2ⁿ n^{−1/2}.
2. (exact counts) X_s(z) = ∏ L_{A_j}(z) is an N-algebraic series that counts *words*, again by unambiguity; the same holds for Y_s. If either
   has radius > 1/2, the centred term is exponentially small. Otherwise, along residue classes mod a period p = p(s), the coefficients have
   asymptotic expansions C·2^m m^{α}(1 + o(1)) [cited: Flajolet–Sedgewick VII.7–8; Banderier–Drmota 2015 for the periodic structure of positive systems].
   Hence for |j| ≤ εN with j ≡ 0 (mod p), |X_{s,N+j}||Y_{s,N−j}| ≥ ½|X_{s,N}||Y_{s,N}| once N ≥ N_0(s, ε).
3. Summing over these ≍ εN/p shifts in 1. gives |X_{s,N}||Y_{s,N}| ≤ (2p/εN)·C 2ⁿ n^{−1/2} = O_s(2ⁿ n^{−3/2}). ∎

**Corollary S′.** If G is unambiguous, L ⊆ G⁻ and L is rotation-dense, then for every *finite* set 𝒮 of spines, the centre spines of
uniformly random w ∈ L_n avoid 𝒮 with probability 1 − O_𝒮(n^{−1/2}). In other words, the spine escapes to infinity.

## 4. Exact gap
- **(G1) Uniformity.** Prop S has to hold with Σ_s C_s·[s used at length n] = o(n^{1/2}). In typical trees the centre spine has unbounded
  length, through cycles s = s₁ cᵉ s₂. The constants N_0(s), C_s and p(s) come from ∏ of t = |s| algebraic factors, and in step 2 the
  regular-variation window εN must not shrink with t. This is the Lemma-Q uniformity, now in a correct form: **smoothness at relative scale
  ε of |X_s ∩ Σ^m| in m, uniformly over centre spines.** A spine cycle A ⇒ uAv with |u| ≠ |v| gives the needed shift for free on the cycle
  part (X_{s₁cᵉ⁺¹s₂} vs X_{s₁cᵉs₂}). So a route for (G1) is to group spines by cycle-reduced skeleton and use the e-shifts. I could not
  control the multiplicity of skeletons.
- **(G2) Ambiguity.** For amb ≤ C nᵏ, step 1 becomes Σ_a ≤ C nᵏ|G⁻_n|, and step 2 needs word counts, not tree counts. Prop S then gives
  n^{k−3/2}: still useful for finitely ambiguous grammars (k = 0, provided step 2 holds with tree counts, which it does after the bound
  |L ∩ X_s c Y_s| ≥ trees/amb), but **vacuous for k ≥ 1/2**. To lift to polynomial ambiguity, one needs that the shifted copies
  (different a) are *mostly distinct words* (multiplicity O(1) on average, not nᵏ). This is where Lemma M (`newmech.md`: ≤ k log|w| + log C
  disjoint locally ambiguous nodes) would have to enter. The bad case is one word reachable from many splits of the same spine.
- No §6 collapse: step 1 uses the set-level fact that *uncoupled* lengths stay inside G⁻. Q has no analogue of this (x c y ∈ Q at all
  splits is free). Count-only data cannot replace it.

## Status
| claim | label |
|---|---|
| Q0: Lemma Q as stated is false | written proof + exhaustive m = 10 |
| Spine rectangles / uncoupled closure | written (standard) |
| Lemma R: centre rectangle ≤ C log²N · 4^N/N | written proof (KMT + Prékopa, cited); DP exponents −0.999 at the optimum |
| Prop S: unambiguous, fixed spine ⇒ O_s(2ⁿn^{−3/2}) | written proof modulo cited algebraic asymptotics (periodic case hedged) |
| Unambiguous rotation-dense L ⊆ G⁻ impossible | OPEN: gap G1 (uniformity in spine) |
| Poly-ambiguous lift | OPEN: gap G2 (Prop S vacuous for k ≥ 1/2) |
