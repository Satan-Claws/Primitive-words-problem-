# r3_l6grammar.md — R3-A: a grammar for L₆, or a precise obstruction?

L₆ = {w ∈ {a,b}^{6ℕ} : w ≠ u², w ≠ u³}. Notation follows `l6.md`: n = 6m, V₂ / V₃ are the square / cube spaces.

Script: `scripts/r3_l6_mirror.py` (the check behind Theorem M).

## 0. Verdict

- **No grammar was found. No obstruction covering all CFGs was found either.** Whether L₆ is CF, or polynomially
  ambiguous, is still **OPEN**.
- **No candidate grammar to verify.** Every candidate I wrote down failed soundness on paper (§4) before reaching the
  exhaustive n ∈ {6, 12, 18} test.
- **Proved results** (§§1–3):
  1. **Lemma G.** L₆ has a *rational* generating function. No analytic argument can show that L₆ is inherently
     ambiguous, not even inherently ambiguous at all. Contrast Q, whose generating function is non-algebraic.
  2. **Theorem R°.** Theorem R holds modulo rotation. A grammar for a rotation-section of L₆ still cannot expose two
     chords, a rectangle, a triangle, or the pattern "chord plus mirror at depth m".
  3. **Theorem M** (the main result). The pumping mechanism of Theorem S does **not** lift to "one nested structure
     plus finite control" (G₂ ⊗ tree automaton). Every run-word of L₆ has a 2-chord axis on which no a-run pump
     reaches a cube. So the natural obstruction route is vacuous here, which counts slightly in favour of the
     affirmative.

## 1. Lemma G: the generating function is rational [written proof]

For n = 6m, the squares and cubes are counted by inclusion–exclusion (u² = v³ ⇔ the word is a 6th power):

  |L₆ ∩ Σⁿ| = 2^{6m} − 2^{3m} − 2^{2m} + 2^{m}.

This gives 54, 4020 and 261576 for n = 6, 12, 18, which matches `l6.md`. The generating function is therefore

  Σ_n |L₆ ∩ Σⁿ| zⁿ = 1/(1−64z⁶) − 1/(1−8z⁶) − 1/(1−4z⁶) + 1/(1−2z⁶),

a rational function.

**Consequence.**
- The Chomsky–Schützenberger and Flajolet criteria cannot rule out even an *unambiguous* CFG for L₆.
- For Q, the Möbius sum over all divisors is what makes the series non-algebraic. That source is absent for L₆.
- So any lower bound for L₆ must be structural (§6 "counting sandwiches" also applies).

## 2. Rotation sections and Theorem R° [written proof; Lemma C is a sketch]

**Lemma C [proof sketch; tree-count preservation not audited].** L₆ is closed under rotation. Take a CNF grammar G′
with Cyc(L(G′)) = L₆, so that every conjugacy class of L₆ meets L(G′) ⊆ L₆. The standard cyclic-closure grammar
reverses the root-to-split-leaf path. Its derivations of w correspond to pairs (split w = yx, a G′-tree of xy). Hence
amb(w) ≤ n · max amb_{G′}.

So it would be enough to find a polynomially ambiguous L′ containing one "well-rotated" representative per class.
(By §7 this transfer is a sketch, not a permitted operation, until the tree counts are audited.)

**Theorem R° [written proof].** Let G′ be a CFG over Σ × {0,1}. Suppose every word of L(G′) has exactly k marks, and
its *cyclic* gaps satisfy:
- the k − 1 interior gaps g₁, …, g_{k−1} each satisfy |g_t − γ_t·n| ≤ C;
- the wrap gap g₀ + g_k (the one containing the word boundary) satisfies |g₀ + g_k − γ₀·n| ≤ C.

If at least 3 of the cyclic fractions γ₀, …, γ_{k−1} are positive, then L(G′) is finite.

*Proof.*
1. As in Theorem R, the exponent set E ⊆ ℕ^{k+1} of the bounded CFL is a finite union of stratified linear sets, so
   every period P has support ≤ 2.
2. Along c₀ + jP the cyclic gaps must stay within O(1) of γ·n. This forces P_t = γ_t|P| for 1 ≤ t ≤ k−1, and
   P₀ + P_k = γ₀|P|.
3. So each positive γ_t forces a distinct coordinate of P into its support. Three positive γ's give support ≥ 3,
   which forces P = 0. ∎

The origin, and hence the split of g₀ + g_k, is free. So choosing a good rotation cannot rescue exposure.

**Instances killed (all cyclic gaps positive).**

| configuration | cyclic gaps |
|---|---|
| rectangle | (m, 2m, m, 2m) |
| two chords, any order | 4 positive gaps |
| triangle | (2m, m, 3m) |
| chord (σ, σ+3m) plus the mirror pair (σ−m, σ+m) inside its fold | (m, m, 2m, 2m) |

The last row is the "cube witness nested inside the G₂ fold at depth m" idea from the task.

## 3. What one nested structure certifies (Theorem M) [written proof + exhaustive check]

### 3.1 Fold picture of G₂

G₂ writes w = (xσy)(zτt) with |x| = |y| and |z| = |t|. That is, w is two odd blocks ("folds"):
- fold A is centred at σ and covers [0, 2σ];
- fold B is centred at τ = σ + n/2 and covers the rest.

The P-spine pairs w[σ−d] with w[σ+d], and the M-spine pairs w[τ−d] with w[τ+d].

**The class 𝒟₂.** "One nested structure plus finite control" means G₂ ⊗ A, where A is a finite bottom-up tree
automaton on G₂ skeletons. Equivalently, G₂ with finitely many annotated copies of each nonterminal. Its languages
are 𝒟₂, and 𝒟₃ is defined the same way from G₃. Every such grammar has ambiguity ≤ amb_{G₂}, so linear.

Theorem S is exactly the statement that L₆ is not a finite union of pieces of the special kind G_p × DFA plus
regular. The natural strengthening would be: L₆ ∉ finite unions of 𝒟₂, 𝒟₃ and Reg.

### 3.2 Run-word model and Lemma P1

**Run-word model.** Let w = a^{L+r₀} b a^{L+r₁} b ⋯ a^{L+r_{M−1}} b, with M = 6N, L ≫ N·‖r‖∞, and L ≡ −1 and r
chosen so that 6 | n. Then:
- w is a square ⇔ r is 3N-periodic (V₂), and w is a cube ⇔ r is 2N-periodic (V₃);
- a 2-chord has axis k, meaning the reflection R_k : i ↦ 2k+1−i on run indices mod M, iff
  h_k := Σ_{i=k+1}^{k+3N} r_i − (Σr)/2 ≠ 0.

There are two kinds of chord:
- (b_k, b_k + n/2);
- (b_{k+3N} − n/2, b_{k+3N}), whose centre lies |h_k| letters from b_k. It has the same run reflection, with drift
  O(|h_k|).

**Lemma P1 [written proof].** Take a 𝒟₂-tree with chord axis k. Pump spine loops of length ≤ |A| lying inside a-runs,
each by a multiple of D = lcm(1..|A|)·6. The words reachable this way are exactly r + D·p, where p ≥ 0 is
R_k-palindromic, i.e. a sum of mirror pairs e_i + e_{2k+1−i}.
- Fold A takes the pairs inside [0, 2σ], and fold B the rest. R_k has no fixed run, so the pairs partition the runs.
- Mirror depth windows overlap in ≥ L − O(‖r‖₁) letters, so every pair is pumpable.

Every pumped word keeps the chord, because the G₂ tree stays valid. So soundness can only fail by reaching a cube.
A palindromic p ≥ 0 with r + p ∈ V₃ exists ⇔ anti_k(r) := (r − R_k r)/2 ∈ V₃. (⇐: take p = c·𝟙 − sym_k(r).)

### 3.3 Theorem M

**Theorem M [written proof].** Let r ∉ V₂ ∪ V₃, i.e. the run-word is in L₆. Then some chord axis k (h_k ≠ 0) has
anti_k(r) ∉ V₃. Hence no run-word of L₆ is pushed out of a 𝒟₂ piece by a-run pumping, whatever the piece's chord
choice. The Theorem S mechanism does not separate L₆ from finite unions of 𝒟₂, 𝒟₃ and Reg.

*Proof.*
1. **Setup.** Write r = v + s with v ∈ V₃ and s ∈ V₃^⊥. Each R_k is orthogonal and preserves V₃. So
   anti_k(r) ∈ V₃ ⇔ s is R_k-palindromic.
2. **Contradiction hypothesis.** Suppose this holds for every chord axis. Fix one, k₀. Then:
   - (a) For s palindromic about k₀, h_{2k₀−k}(s) = −h_k(s). (Reflect the summation window: it becomes the
     complementary half.) In particular h_{k₀}(s) = 0, so h_{k₀}(v) ≠ 0.
   - (b) h(v) is 2N-periodic (v is), and h_{k+3N} = −h_k always. So h_{k₀+N}(v) = −h_{k₀}(v) and
     h_{k₀+2N}(v) = h_{k₀}(v).
3. **Case 1: k₀+N or k₀+2N is also a chord axis.** Then s is palindromic about two axes differing by N or 2N, so it
   is invariant under the rotation R_{k₀+N}R_{k₀} (by 2N) or R_{k₀+2N}R_{k₀} (by 4N). Either rotation generates the
   2N-rotations, so s ∈ V₃ ∩ V₃^⊥ = 0. Then r = v ∈ V₃, a contradiction.
4. **Case 2: neither is a chord axis.** Then h_{k₀+N}(r) = h_{k₀+2N}(r) = 0. With (b) this gives
   h_{k₀+N}(s) = h_{k₀}(v) and h_{k₀+2N}(s) = −h_{k₀}(v).
5. By (a), h_{k₀+2N}(s) = −h_{k₀−N}(s) = h_{k₀+N}(s), using h_{k₀−N} = −h_{k₀+2N}. Combining with step 4,
   h_{k₀}(v) = −h_{k₀}(v) = 0, which contradicts (a). ∎

**Check [computational, `r3_l6_mirror.py`].** Zero run-vectors on which the attack works:
- exhaustive: N = 1 with r ∈ {0..3}⁶ (4 020 L₆ vectors); N = 2 with r ∈ {0,1,2}¹² (530 640 vectors);
- random: 50k samples each at N = 2, 3;
- structured mixed words r = v + y (v ∈ V₃, y ∈ V₂): 50k samples each at N = 2, 3, 4.

### 3.4 Scope and reading

**Scope (honest).**
- Theorem M concerns a-run pumps on run-words only.
- Pumps through b's, i.e. inserting short runs at ≥ 6 mirror-paired places to build a 2N-periodic pattern of short
  runs, are not excluded. That is the only remaining pumping attack on 𝒟₂, and I did not settle it.
- The G₃ analogue was not analysed. It is not needed for the conclusion, since a safe 2-chord already exists.

**Reading.**
- A certificate in 𝒟₂ would have to witness "anti_k(r) ∉ V₃": the mirror-antisymmetric part about the chord axis is
  not 2N-periodic.
- Theorem M says such an axis always exists. That is the exact residual task for a 𝒟₂-based affirmative.
- But verifying non-2N-periodicity of anti_k(r) is itself a fractional comparison. In fold coordinates it compares
  depth d with depth d + 2N runs. Tree automata on a fold cannot do it. (The fold sees only mirror comparisons, and
  regular, mod-q, mirror-weighted sums. Those are invariants of V₃ only for residues of N, giving C_k-type coverage
  again.)
- So 𝒟₂ ∪ 𝒟₃ ∪ Reg is neither refuted nor shown sufficient.

## 4. Ideas tried that fail (one line each)

| idea | why it fails |
|---|---|
| compare #b in thirds / halves | Needs the cuts n/3 and 2n/3 plus a count comparison: ≥ 3 positive cyclic gaps, so Theorem R° applies. Even #b(first half) ≠ #b(second half) certifies only non-square. |
| cube witness nested in the G₂ fold at depth m | Cyclic gaps (m, m, 2m, 2m), so Theorem R° applies. |
| chains of ratio-folds (concatenated blocks with arm ratios α_j) | Chord spans n/2 and n/3 force α₂ = 1 and α₃ = −1, which is impossible (Theorem W in fold language). |
| Parikh or factor-count certificates | Parikh(Sq) = 2ℕ^Σ, so these collapse to R_{p,k}. Missed by U_k (Lemma U). |
| characterisation L₆ = {ρ^e : ρ primitive, 6 \| \|ρ\|, gcd(e,6) = 1} | True, but it needs Q-type primitivity of ρ. No gain. |

## 5. Status

| claim | label |
|---|---|
| GF of L₆ is rational, so no analytic obstruction even to unambiguity | [written proof] |
| Theorem R° (exposure modulo rotation is finite) | [written proof] |
| Rotation-section transfer, amb ≤ n·amb′ | [proof sketch; tree counts not audited] |
| Theorem M: a-run symmetric pumping never refutes 𝒟₂ on L₆ run-words | [written proof] + [exhaustive/random check] |
| Polynomially ambiguous CFG for L₆ | **OPEN** (none found) |
| Obstruction for all CFGs | **none**; the Theorem S route is shown vacuous one level up |
