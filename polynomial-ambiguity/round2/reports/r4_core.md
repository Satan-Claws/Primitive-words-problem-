# r4_core.md — R4-A: coverage loop with uniform sound gadgets

Scripts:
- `scripts/r4_core_lib.c`: exact membership and tree counts for every gadget, in C. It also does the exhaustive sweep and canonical forms.
- `scripts/r4_core_cover.py`: driver. It runs the soundness check and the cross-check against `r3_offw_fold.certs`, then the coverage table, and writes U_n to `r4_core_U.txt`.
- `scripts/r4_core_analyze.py`: characterises U (g, Off, zeros of x̂, run sequences, local count gcd h_K).
- `scripts/r4_core_mc.py`: numpy re-implementation, cross-checked against the C code on all words with n ≤ 12. It runs Monte Carlo coverage up to n = 65536.

Run: `python r4_core_cover.py 28 3 2 3` (K = 3, KP = 2, R = 3). This takes about 2 minutes.

## Verdict

**Small lengths: exhaustive coverage is high [computational].** A library of 6 uniform, sound, linearly ambiguous gadget families covers every primitive word for n ≤ 19 and n = 21, 22, 23. The uncovered sets are:

| n | 20 | 24 | 25 | 26 | 27 | 28 |
|---|---|---|---|---|---|---|
| \|U_n\| | 40 | 48 | 400 | 780 | 1242 | 3248 |
| share of \|Q_n\| | 4·10⁻⁵ | 3·10⁻⁶ | 1·10⁻⁵ | 1·10⁻⁵ | 9·10⁻⁶ | 1.2·10⁻⁵ |
| classes | 1 | 1 | 7 | 10 | 17 | 40 |

Classes are counted up to rotation, reversal and letter swap.

**What the small-n U looks like.** It is a structured family: sparse, *near-reflection-symmetric* run sequences. More precisely:
- x̂(1) ≠ 0 always, so U_n ⊆ Off and the words are not W-type.
- The local factor counts share a divisor, or g = 1 with large Bézout coefficients.
- The fold has mixed signs.

**Large lengths: U does NOT shrink to a structured family [computational + written sketch].** On uniform random words, the share covered by the library decays like Θ(n^{−1/2}):

| n | 256 | 1024 | 4096 | 16384 | 65536 |
|---|---|---|---|---|---|
| covered | 0.87 | 0.56 | 0.34 | 0.20 | 0.095 |

So asymptotically the uncovered core is dominated by *generic* words, not by a structured family. This holds for every library of this type (§4).

**Main conclusion.** The uniformity crux is already visible on generic words, and it is not a near-periodic phenomenon. That is the opposite of the per-slice picture, where the hard words are near-periodic (S_N, W_n).

## 1. Gadget library (each one is a single CFG for all lengths, with L ⊆ Q)

Notation:
- w ∈ {a,b}ⁿ, read cyclically.
- For a window function φ: Σ^K → ℤ, put x^φ_k = φ(w[k..k+K−1]), with indices mod n.
- x^f = x^φ for φ = [window = f], the occurrence indicator of the factor f.
- occ_f(w) = Σ_k x^f_k is the number of cyclic occurrences of f.

**Lemma S (one soundness lemma for all gadgets) [written proof].** Suppose w = u^p with p ≥ 2. Then:
- (i) every x^φ is (n/p)-shift-invariant, so Σ_k x^φ_k ≡ 0 (mod p) and x̂^φ(1) = 0;
- (ii) if w is not unary, the cyclic run sequence (α_i, β_i)_{i ∈ ℤ_r} is (r/p)-periodic, so α̂(1) = β̂(1) = 0 over ℤ_r.

*Proof.*
- (i) Rotation by |u| fixes w, so it fixes x^φ. That rotation acts freely with order p on ℤ_n, so every level set of x^φ is a union of orbits of size p. The DFT at a frequency j with (n/p)·j ≢ 0 (mod n), in particular j = 1, vanishes by the geometric sum.
- (ii) Rotation by |u| permutes the maximal cyclic runs freely with order p and preserves their lengths. ∎

So any certificate that Σ c_φ Σ_k x^φ_k = ±1, or that x̂^φ(1) ≠ 0 (or α̂(1) ≠ 0), proves w primitive. The cases n < K are a finite set of words and are handled separately.

**CF realisation of window features [written proof].**
- Annotate each position with its window c_k ∈ Σ^K.
- The annotated words that are consistent form a regular set R_K. The DFA guesses c_0 and checks the wrap at the end.
- The projection c ↦ c[0] is injective on R_K.
- A gadget is (grammar over Σ^K) × DFA(R_K), followed by the projection. DFA products and an injective letter projection keep tree counts exactly (prompt §7).

**The gadgets.** Ambiguity is the number of derivation trees.

| id | gadget | membership certificate | soundness | amb |
|---|---|---|---|---|
| LIN | Parikh lines L_{r,s,±1} (Lemma O, `PA/poly_L.md`), plus #a = 1 and #b = 1; 1 ≤ r, s ≤ R = 3, gcd(r,s) = 1 | r#a − s#b = ±1 | g \| 1 | ≤ #pieces (DCFL each) |
| D1·b | `PA/poly_T3.md` | #b − #a = 1 | subsumed by LIN (r = s = 1) | 1 |
| FOLD | G_fold (`R2/r3_offw.md` §4) | a pure-sign fold certificate (m,±) on x = x^b | x̂(1) ≠ 0 | ≤ n (tree count = #certs, re-checked n ≤ 12) |
| FL_K | **new.** Factor-count lines over factors f, h with \|f\|,\|h\| ≤ K = 3 | occ_f = 1, or c₁·occ_f − c₂·occ_h = ±1 (c_i ≤ 3, coprime) | Lemma S(i) | ≤ #pieces (a constant ≈ 1.3·10³; observed ≤ 200). Each piece is a one-counter DCFL ∩ R_K, so it is unambiguous |
| LF_K | **new.** Fold on the indicators x^f, 2 ≤ \|f\| ≤ 3 | a pure-sign fold certificate on x^f | Lemma S(i) | ≤ 12n |
| PF | **new.** Fold on signed features x^f − x^h, \|f\| = \|h\| = 2 | the same, on integer pair differences in {−2..2} | Lemma S(i) | ≤ 6n |
| RLF | **new.** Run-length fold: a pure-sign fold over ℤ_r on the a-run sequence α and on the b-run sequence β | Σ_i α_i sin(2π(i − m/2)/r) ≠ 0, certified pairwise | Lemma S(ii) | ≤ 2r ≤ n |

**RLF grammar [written proof for words that start an a-run and end with b; the wrap run is a sketch].**
- Mirror pairs of runs are generated outside-in.
- A comparison α_L < α_R uses `C → a C a | B⁺ N A⁺` with the pair `P → C B⁺`. This gives a^i b⁺ N a^{i+e} b⁺ with e ≥ 1.
- The other cases are the same: = uses `a C a | B⁺ N`, and > is symmetric.
- Each comparison has exactly one derivation, so a certificate (m,±) has exactly one tree.
- **Wrap run** a^s … a^t (its length is s + t). Its comparison with α_j is still non-crossing: arcs from a^s land in the left part of α_j, and arcs from a^t land in the right part. This is a proof sketch.

**Computational soundness check.** No gadget accepts any non-primitive word with n ≤ 16. This covers all 2¹⁷ words of lengths up to 16 across all six families. The fold count equals the certificate count of `r3_offw_fold.py` on all words with n ≤ 12. Tree counts were not recomputed from literal CFGs for FL, LF, PF or RLF; they follow from the constructions above.

**Union ambiguity [computational, full evaluation for n ≤ 16].** The maximum over w of the summed tree counts, by stage (cumulative):

| n | 8 | 12 | 16 |
|---|---|---|---|
| S0 (LIN + FOLD) | 9 | 12 | 16 |
| S1 (+FL) | 238 | 188 | 192 |
| S2 (+LF) | 313 | 304 | 349 |
| S3 (+PF) | 335 | 338 | 395 |
| S4 (+RLF) | 337 | 340 | 397 |

The bound is O(n) for every n [written]. The FL constant dominates; it depends only on K and R.

## 2. Coverage loop (exhaustive, K = 3, KP = 2, R = 3)

Columns S0–S4 are the fraction of Q_n covered, cumulative by stage. S0 is LIN + FOLD, then FL, LF, PF and RLF are added in turn.

| n | \|Q_n\| | S0 | S1 | S2 | S3 | S4 | \|U_n\| | classes |
|---|---|---|---|---|---|---|---|---|
| ≤ 11, 13 | | 1 | 1 | 1 | 1 | 1 | 0 | 0 |
| 12 | 4020 | .976 | .994 | 1 | 1 | 1 | 0 | 0 |
| 16 | 65280 | .923 | .990 | 1 | 1 | 1 | 0 | 0 |
| 18 | 261576 | .903 | .985 | 1 | 1 | 1 | 0 | 0 |
| 20 | 1047540 | .839 | .984 | .99993 | | 1−4·10⁻⁵ | 40 | 1 |
| 22 | 4192254 | .825 | .980 | 1 | 1 | 1 | 0 | 0 |
| 24 | 16772880 | .677 | .970 | | | | 48 | 1 |
| 25 | 33554400 | .783 | .9999 | | | | 400 | 7 |
| 26 | 67100670 | .636 | .972 | | | | 780 | 10 |
| 27 | 134217216 | .795 | .995 | | | | 1242 | 17 |
| 28 | 268419060 | .623 | .968 | | | | 3248 | 40 |

Notes on the table:
- At prime n, LIN + FOLD alone cover 100% for n ≤ 17. There g = 1 for every non-unary word.
- At n = 23, S1 = 1.
- Iteration effects:
  - Iteration 1 (FL, LF, PF) took U_22 from 735 k words to 0.
  - Iteration 2 (RLF) took U_20 from 120 words (3 classes) to 40 (1 class) and U_24 from 816 words (13 classes) to 48 (1 class).
- With K = 2 instead of 3, U is larger: U_22 has 1540 words (25 classes) at S4. `r4_core_U.txt` holds the K = 3 output.

## 3. Characterisation of U (n ≤ 28, K = 3) [computational]

Tallies are over the 76 classes; output from `r4_core_analyze.py`.
- **Off.** All 76 classes satisfy x̂(1) ≠ 0. So U ⊆ Off, U ∩ W_n = ∅, and these words are not S_N-type. In most of them x̂(j) has no zeros at all; a few have zeros only at j ∈ (n/g)ℤ or at j = n/2.
- **Density.** U is sparse: #b ∈ {5, 6, 7, 8, 10, 12}, all with #b ≤ 12 ≤ 0.43n. Usually every b is isolated (β ≡ 1).
- **g.** The values are 1 (14 classes; R = 3 is too small for these Bézout coefficients), 2 (27), 3 (10), 4 (9), 5 (8), 6 (1) and 7 (7). The local count gcd h₃ = gcd of all occ_f, |f| ≤ 3, equals g in every class except 7 of the 9 g = 4 classes, where h₃ = 2. So the counting lines (FL) never fire on U.
- **Shape.** The a-run sequence α is a near-palindrome with one long run, for example α = (2,3,3,2,5), (2,3,3,3,2,7) or (2,4,4,2,8). Such an α is *exactly reflection-symmetric* about one axis. Then Im(e^{−iπm/r} α̂(1)) = 0 on that axis, and every other axis sees mixed signs. For odd r there is no axis perpendicular to it.
- **Candidate structured family (small n).** 𝓕 = { b a^{α₀} b a^{α₁} ⋯ b a^{α_{r−1}} : α a palindrome of length r − 1 plus one long run, r prime or 2·prime }.
  - Examples: α = (2,3,3,2,L) and (2,3,3,3,2,L), for all L.
  - Every member is primitive.
  - Every pure-sign fold fails, on x, on the x^f and on α, as soon as α has ≥ 2 distinct inner values.
  - FL/LIN cover a member only when its counts happen to hit a small line.

## 4. The trend: generic words are the asymptotic core [computational + written sketch]

Monte Carlo on uniform random primitive words, cumulative S0..S4 (300 words per n; 400 per n for LIN ∪ FL only):

| n | 32 | 64 | 128 | 256 | 1024 | 4096 | 16384 | 65536 |
|---|---|---|---|---|---|---|---|---|
| S0 (LIN + FOLD) | .56 | .013 | .010 | 0 | | | | |
| S4 (all) | 1 | 1 | .97 | .87 | | | | |
| LIN ∪ FL | | | | .84 | .56 | .34 | .20 | .095 |

**Why the coverage vanishes [written sketch].**
- *Pure-sign folds* (FOLD, LF, PF, RLF) need Θ(n) or Θ(r) mirror differences, all with one sign. Pairs at distance > K are independent, so a random word passes with probability n·e^{−Ω(n)}.
- *Counting lines* (LIN, FL). Each occ_f is a sum with local CLT scale √n. A fixed finite set of pieces c₁o₁ − c₂o₂ = ±1 is hit with probability O(1/√n).
- Together, any finite library of the §1 type covers O(n^{−1/2}) of Q_n. Increasing K or R only changes the constant.

**Consequence.** The uncovered part of Q is asymptotically *almost all of Q*. Random words are primitive for a trivial reason: they have unique factors of length about 2 log₂ n. Every uniform certificate here is either bounded-window or pure-sign, and neither sees that reason.

**Precise open target (DENSE-SOUND).** Is there a polynomially ambiguous CFG L ⊆ Q with |L ∩ Σⁿ| ≥ c·2ⁿ for all n, or even for all n ∈ 6ℕ?
- An affirmative answer to the main problem implies DENSE-SOUND.
- "No such L" implies the main negative.
- Restricted to n ∈ 6ℕ, DENSE-SOUND asks for a dense poly-ambiguous subset of L₆ = NonSq ∩ NonCube ∩ Σ^{6ℕ}.
- Theorem X forbids exposed two-prime certificates. Every gadget known so far has density O(n^{−1/2}).

This is a candidate hard core for a negative proof that is NOT near-periodic. It is stated as a question, not a conjecture of truth.

**Sound combinations with G_p that fail [assessment, not proved].**
- G_p ∩ L_{r,s,±p} would be sound, because it forces g | p.
- But NonSq ∩ {#a − #b = 2} = {D = 2} ∩ {D(h₁) ≠ 1} ∪ … contains an abelian-square-type condition (#a(h₁) = #b(h₂) + 1 across the midpoint). That is a crossing two-counter constraint, and likely not CF.
- No regular constraint forces the prime support of g into {p}, since only finitely many moduli are visible.
- So per-prime grammars combine soundly only through Parikh or Fourier certificates. These are exactly the §1 gadget types.

## 5. Status labels

| claim | label |
|---|---|
| Lemma S and the soundness of LIN, FL, FOLD, LF, PF and RLF; CF realisation via R_K | written proof (RLF wrap run: sketch) |
| Every gadget has amb = O(n) | written proof |
| Coverage tables, U_n lists and characterisation (n ≤ 28) | computational (exhaustive) |
| Coverage → 0 like n^{−1/2} | MC + written sketch |
| U ⊆ Off and U ∩ W_n = ∅ | computational, n ≤ 28 only |
| DENSE-SOUND as the core | open question |
