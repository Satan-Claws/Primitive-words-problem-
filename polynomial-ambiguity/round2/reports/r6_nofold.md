# r6_nofold.md — R6-B: FOLD-COUNTER, negative side

Scripts: `scripts/r6_nofold_slices.py` (slice membership), `scripts/r6_nofold_mono.py` (Lemma M and Lemma L, exhaustive n ≤ 14),
`scripts/r6_nofold_macro.py` (Prop S, Monte Carlo). Each runs in under a minute.

Notation (as in `r6_build.md` / `r6_miss.md`):
- d_k(w) = #a(pre_k) − #a(suf_k).
- G⁻ = {w : d_k < 0 for 1 ≤ k ≤ ⌊n/2⌋} ⊆ Q.
- F_K⁻ = {w : d_k < 0 on K_n = [⌈n/3⌉, ⌊n/2⌋]}.
- "Rotation-dense" means |L ∩ Σⁿ| ≥ c·2ⁿ/n (equivalently, rot(L) has positive density).
- G⁻ itself has density Θ(n^{−1/2}), since it is a strict meander of the folded walk.

## Verdict

**NOT resolved.** I have no proof that a CF (or poly-ambiguous) L ⊆ G⁻ or L ⊆ F_K must be rotation-sparse.

What I do have is a precise account of why every classical non-CF tool fails on G⁻, F_K and F_δ:
- bounded-slice Ogden,
- bounded pumping,
- macroscopic single pumps,
- the interchange lemma / one-split rectangles.

I also identify the one property of G⁻ that Q lacks and that a successful argument would have to use. It is *fluctuation-level membership*: whether a word is in G⁻ is decided by Θ(√n) fluctuations of the fold walk. Q is different: a non-primitive word has measure 2^{−Ω(n)} near any word.

**Is the length coupling a genuine barrier?** It is genuine for every *local* or *one-split* argument (N1–N3 below). It is not shown to be a barrier for CF-ness. The remaining route is multi-scale, through the spine reduction of §4, and its exact gap is stated there.

**The stop-early check does not trigger.** Every tool below fails on Q too, but none of them *succeeds* on Q, so nothing here proves Q non-CF. The proposed route (§4) uses quotient-sparsity, which Q does not have.

## 1. Rigorous structure of G⁻

**Lemma L (insertion formula / Lipschitz)** [written proof; exhaustive n ≤ 14, 0 violations]. Let w′ = w[0,m)·w[m+r,n), deleting a factor of length r with m ≤ (n−r)/2. Then for every k ≤ ⌊(n−r)/2⌋, suf_k(w′) = suf_k(w), and

  d_k(w′) = d_k(w) for k ≤ m,  d_k(w′) = d_k(w) + #a(w[k,k+r)) − #a(w[m,m+r)) for k > m.

So |d_k(w′) − d_k(w)| ≤ r, and d is unchanged at depths below the edit. Insertion is the inverse operation. Right-half edits follow by the symmetry below.

**Symmetry.** Reverse-complement satisfies d_k(w̄ᴿ) = d_k(w), because #b(suf_k) − #b(pre_k) = #a(pre_k) − #a(suf_k). So G⁻ and F_K are rc-invariant.

**Lemma M (G⁻ is an up-set of the fold order)** [written proof for (i); (ii) is (i) under rc; (iii) is immediate; exhaustive n ≤ 14, 0 violations for G⁻ and also for F_K⁻]. G⁻ is closed under each of these operations:
- (i) inserting b at any index m ≤ ⌊n/2⌋;
- (ii) inserting a at any index m ≥ ⌈n/2⌉;
- (iii) a→b at a position left of the centre, and b→a at a position right of the centre.

*Proof of (i).*
- For k ≤ m nothing changes.
- For m < k ≤ ⌊(n+1)/2⌋ the suffix is unchanged (k ≤ n−m), and pre_k(w′) = w[0,m)·b·w[m,k−1). So d_k(w′) = d_{k−1}(w) − [w_{n−k} = a] ≤ d_{k−1}(w) < 0.
- When k = 1 this reads d_1(w′) = −[w_{n−1} = a] = −1. This holds because w ∈ G⁻ forces w = b…a. ∎

## 2. No-go results for classical tools (why "pumping changes the fold alignment" does not bite)

**N1 (bounded pumps)** [written proof from Lemma L + Brownian heuristic for the measure].
- Fix r and D. Let T_{r,D} = {w ∈ G⁻ : d_k ≤ −r−1 for D ≤ k ≤ n/2}.
- By Lemma L, T_{r,D} is closed under every deletion or insertion of total size ≤ r located in [D, n−D], since depths < D are untouched.
- For a meander, P(T_{r,D} | G⁻) → 1 − O(r/√D). [assessment: Brownian meander]
- So every Ogden / Bader–Moura / pumping conclusion with |vxy| ≤ p is satisfied, away from the ends, by a sub-language of relative density ≈ 1.
- Lemma M adds that pumps of the form (b^s left, a^t right) never exit G⁻, even when pumped up without bound.

**N2 (macroscopic single pumps)** [computational, Prop S]. Take a random w ∈ G⁻ (n = 400) and delete or duplicate blocks v (left) and y (right) of sizes 0.05n–0.2n, at depth ≥ n/10. Then:

| \|v\|, \|y\| | P(u x z ∈ G⁻) | P(u v² x y² z ∈ G⁻) |
|---|---|---|
| 0.2n, 0 | 0.89 | 0.89 |
| 0.2n, 0.2n | 0.90 | 0.88 |
| 0.2n, 0.1n | 0.90 | 0.86 |
| 0.05n, 0.15n | 0.90 | 0.87 |

- Re-pairing at relative shift Θ(n) is a fresh random walk started at height ≍ −√n, so it exits only with probability bounded away from 1.
- So the fold-alignment shift caused by unequal |v|, |y| is real, but a grammar can keep its language inside the ≈ 0.9 surviving part.
- One macroscopic pump per word gives no contradiction.

**N3 (interchange lemma / one-split rectangles)** [written sketch + Brownian assessment].
- The interchange lemma (Ogden–Ross–Winklmann) yields a rectangle C × X ⊆ L ⊆ G⁻ with |C|·|X| ≥ |L_n|/(cn²), at a fixed window [s, s+l).
- G⁻ already contains rectangles of size Θ(|G⁻_n|) at every window. Take X = fillers whose partial a-count #a(x[0,t)) stays within ε√l of t/2 for all t ≤ l (measure e^{−O(1/ε²)}·2^l), and C = contexts with margin ≥ 2ε√l on depths ≥ s.
- So rectangle bounds cannot separate any L ⊆ G⁻ from G⁻. This is the §6 "one split" trap instantiated for folds.

**Slices** [computational, confirms r5]. G⁻ ∩ b^i a^j (ba)^m = {i > m} ∪ {j < i} (i, j, m ≤ 11). It is a union of stratified sets, hence CF; b⁺a⁺ba⁺ ⊆ G⁻ (r6_build). Bounded slices of a strict-inequality fold are fold-nested, so Ogden on slices gives nothing for G⁻, F_K or F_δ. This differs from r5's equality version, which is non-CF on a slice.

## 3. What G⁻ has that Q does not

| property | G⁻ / F_K | Q |
|---|---|---|
| monotone up-set of the fold order (Lemma M) | yes | no (aba → abab) |
| exit probability under one macroscopic surgery | ≈ 0.1 (Θ(1)) | 2^{−Ω(n)} |
| density of two-sided quotient P⁻¹LS⁻¹ for a context of margin h | ≍ min(1, h/√|u|) | 1 − o(1) |

A negative argument that uses only robustness (N1–N3) fails for both languages. An argument that uses Θ(1) exit probability compounded over many *independent* macroscopic surgeries would not apply to Q, because Q's exit probability is exponentially small. That is the only non-F1-blocked handle I found.

## 4. The multi-scale route and its exact gap

**Spine reduction** [written; standard].
- In any tree of w ∈ L, the root-to-centre spine is a regular (finite-state) sequence of nonterminals. So w = α₁⋯α_t · c · β_t⋯β₁, where α_j ∈ L(A_j) hang on the left and β_j ∈ L(B_j) on the right.
- Substituting any α′_j ∈ L(A_j) keeps the word in L. If |α′_j| ≠ |α_j|, every fold pair inside shifts by |α′_j| − |α_j|. This is exactly the length coupling.
- Hence L(A_j) ⊆ P⁻¹ G⁻ S⁻¹ =: G⁻_{t,h}, a shifted meander with centre offset t = |S| − |P| and start height h = −d_{|P|}(context). So the problem is *self-reducible* within the family {G⁻_{t,h}}.

**Exact gap (Lemma Q, OPEN).** We need a bound of the form: for every CF L(A) ⊆ G⁻_{t,h}, the density is ≤ c·min(1, h/√n)^{1+η}, uniformly in t, h. The induction along the spine would then compound the exponent η across the Θ(log n) scales that a heavy path visits, and give rotation-sparsity.
- The base case fails as stated: for h ≥ ε√n the quotient is itself dense (N1). So the induction must charge each scale only for the *margin* it consumes.
- I do not know how to do that without a per-scale independence statement. Such a statement is a property of the grammar, not of G⁻, which is where polynomial ambiguity would have to enter (F1).

## 5. Part (2): the fold-type certificate class

- "Fold-type" is vacuous unless the pair language is restricted. fold : Σ^{2m}(·Σ) → Π^m(·Σ) is a bijection, so every language is fold(D) for D = fold⁻¹(L).
- The meaningful classes are fold(D) with D ∈ REG, DOCL or CF over Π = Σ².

**Theorem / conjecture ladder.**
- **D regular, fold(D) ⊆ Q ⇒ density e^{−Ω(n)}.** This is Prop K of `r6_build.md` [written proof]. Every CF L ⊆ fold(D) inherits the bound trivially.
- **D one-counter (G⁻ = fold(strict meander), F_K, F_δ).** The statement "every CF L ⊆ fold(D) ⊆ Q is rotation-sparse" is **FOLD-COUNTER itself**, OPEN. N1–N3 show it cannot be proved by local or one-split tools.
- **D ∈ CF.** Not pinned down. If fold⁻¹(Q) were CF, a class-wide sparsity theorem would imply Q ∉ CF (F1 / prompt §3). I cannot rule this out, so the class must stop at counters.
- So the strongest honest statement is: *every CFL L ⊆ Q certified by a regular fold condition is exponentially sparse (Prop K). For one-counter fold conditions, sparsity is equivalent to Lemma Q along the spine. It is open.*

## Status

| claim | label |
|---|---|
| Lemma L (insertion formula, Lipschitz ≤ r) | written proof; exhaustive n ≤ 14 |
| rc-invariance of d_k | written proof |
| Lemma M (G⁻ up-set: b-insert left, a-insert right, flips) | written proof; exhaustive n ≤ 14 (also F_K⁻, computational only) |
| N1 bounded-pump no-go | written proof (closure) + Brownian assessment (measure) |
| N2 macroscopic pump survival ≈ 0.9 | computational (MC, n = 400) |
| N3 rectangle / interchange no-go | written sketch + assessment |
| G⁻ ∩ b^i a^j (ba)^m = {i>m} ∪ {j<i} | computational (≤ 11) |
| spine reduction to G⁻_{t,h} | written (standard) |
| Lemma Q / FOLD-COUNTER negative | OPEN |
