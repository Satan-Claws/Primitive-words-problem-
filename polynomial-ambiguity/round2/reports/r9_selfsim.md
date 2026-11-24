# r9_selfsim.md — R9-C: exploiting the self-similar block reduction (both directions)

Scripts (`scripts/`):
- `r9_selfsim_exact.py`: exhaustive checks of every exact transfer used below. Output is in §5.
- `r9_selfsim_cover.py`: coverage of the truncation certificates L_k, exhaustive for n ≤ 18 and Monte Carlo for n ≤ 4096. Output: `r9_selfsim_cover_out.txt`.

## Verdict (short)

**No amplification either way.** Both directions reduce to the original problem, *exactly*, with tree counts preserved.

- **(A) Negative.** Three results:
  - P(P∩Q) ⇒ P(Q) [written proof]. The converse is OPEN, and the gap is identified exactly (§2.3).
  - Every transfer available here has the form amb_target(w) = amb_source(ℓ(w)), or the same up to a poly(n) factor (cyclic closure). So the renormalisation map is F(x) = x. A "renormalisation" inequality amb(n) ≥ C·amb(n^α)^s rules out polynomial ambiguity **iff sα > 1** [written proof, Lemma RG]. The block self-similarity gives s = 1 and α = ½, which is sub-marginal. Even a two-instance product at scale √n (s = 2) is exactly marginal.
  - Worst-case hardness sits on words whose instance length is Θ(n), not √n. So the √n contraction is a typical-word phenomenon, and typical-word bounds do not count (§7).
- **(B) Affirmative.** The invariant certificate "top-level prime-count sequence (r₁,…,r_H) primitive" (and its depth-k refinements L_k) is sound. It is CF-composable by an *unambiguous CF substitution*, with tree counts preserved exactly. The instance it lands in is the slice Q ∩ (b*a)⁺, i.e. primitive ℕ-sequences in unary, with **unbounded** H ≈ √n blocks.
  - That slice is the *whole* problem: P(Q ∩ (b*a)⁺) ⇔ P(Q) by the code {ba, bba}.
  - It is not a fixed-(ab*)ⁿ slice, so the fixed-n bounded-ambiguity results do not apply.
  - Hence **P(L_k) ⇔ P(Q) for every finite k** [written proof]. The certificates are equivalent reformulations of Q, not easier instances.
  - Coverage: L₁ misses ≍ n^{-1/2} of the classes, L₂ about 10× less, L₃ ≈ 0 at n = 4096 (MC). The misses come from small H.

## 1. Setup

- **Notation.**
  - P = (D_b a)⁺ = {every nonempty suffix strictly a-heavy}.
  - D_b is the Dyck language with b = open and a = close.
  - Every w ∈ P factors uniquely as w = D₁a⋯D_Ha (U3). P∩Q = {w ∈ P : (D₁,…,D_H) primitive over the alphabet D_b}.
  - Each D ∈ D_b factors uniquely into primes D = p₁⋯p_r with p_j = b D'_j a. So D_b ≅ plane forests, and w ∈ P ≅ a sequence of H plane forests.
- **Q-type problem over a code.** For a code C ⊆ Σ⁺ (here C = D_b a, an unambiguous CF prefix code), let
  Prim_C = {c₁⋯c_H : c_i ∈ C, (c_i) primitive as a sequence over C}. Then Prim_{D_b a} = P∩Q (U3).
- **Depth-k truncation.**
  - Put G₀ = x*, G_j = (b G_{j−1} a)*, and R_k = (G_{k−1} a)⁺. These are regular languages over {a, b, x}.
  - tr₁(D) = x^{r(D)}, and tr_k(D) = ∏_j b·tr_{k−1}(D'_j)·a.
  - trunc_k(w) = tr_k(D₁)a⋯tr_k(D_H)a ∈ R_k. Primes at depth < k are kept literally; each prime at depth exactly k becomes x.
  - Let σ be the substitution σ(x) = b D_b a (the Dyck primes; unambiguous CF), with σ(a) = a and σ(b) = b. Then σ(G_j) = D_b and σ(R_k) = P.
- **Certificate.** L_k := {w ∈ P : trunc_k(w) ∈ Q₃}, where Q₃ is the primitive words over {a, b, x}.
  - Because trunc_k(w) ends every block with the only a at walk level 0, primitivity of trunc_k(w) as a word equals primitivity of the truncated block sequence (tr_k(D_i))_i.
  - So L_k = σ(Q₃ ∩ R_k).

## 2. Direction (A): exact relations, and why there is no renormalisation gain

### 2.1 Lemmas used (all exact; tree counts preserved)

- **E1 (unique σ-decoding).** For t ∈ R_k and w ∈ σ(t), t = trunc_k(w), and the x-to-prime assignment is unique.
  - *Proof.* In σ(t), every literal b/a of t sits at Dyck depth < k inside its block. Every letter produced by an x sits at depth ≥ k.
  - So the depth-k primes of w are exactly the x-images, and they are determined by w.
  - The prime grammar b D_b a is unambiguous. ∎
  - Consequence: if G is a CFG for M ⊆ R_k, then substituting an unambiguous grammar for b D_b a into x gives a CFG G^σ for σ(M) with amb_{G^σ}(w) = amb_G(trunc_k w).
- **E2.** For μ(a) = ab, μ(b) = abb, μ(x) = abbb: μ(u) ∈ Q ⇔ u ∈ Q₃, and Q ∩ μ({a,b,x}*) = μ(Q₃).
  - This is the run-length correspondence: (ab⁺)⁺ ↔ sequences over ℕ_{≥1}, with primitivity preserved both ways. Same argument as §5.4.
  - Pullback along the prefix code μ is a DFA product followed by block decoding, so tree counts are preserved.
- **E3.** For c(a) = ba, c(b) = bba: Q ∩ (ba + bba)* = c(Q), and c(u) ∈ Q ⇔ u ∈ Q. This is the mirror of §5.4.
  - Also Q ∩ (b*a)⁺ ↔ primitive ℕ-sequences of b-run lengths.
- **E4.** P ∩ {a, ba}* = {a, ba}*·a, where the last code word is a.
  - For t ∈ (b*a)⁺, put σ_min(t) = t with b ↦ ba. Then σ_min(t) ∈ L_k ⇔ t ∈ Q, for every k ∈ {1, 2, …, ∞}, with L_∞ := P∩Q.
  - *Proof.* All blocks of σ_min(t) are (ba)^{r_i} with height 1. So the block sequence, trunc_k, and the r-sequence all carry the same information. ∎

### 2.2 Theorem A1 (P∩Q and all L_k are at least as hard as Q) [written proof]

For every k ∈ {1, …, ∞}: if L_k has a CFG with ambiguity f, then Q has one with ambiguity f(O(n)) + 1.

*Proof.*
1. L_k ∩ {a, ba}*a is a DFA product.
2. Pull back along the prefix code {x ↦ ba, a ↦ a} (E4). This gives Q ∩ (x*a)⁺ with the same tree counts.
3. Pull back along c (E3, x playing b). This gives Q ∖ {a}. Add a.

Lengths grow by a factor ≤ 6. ∎

This also gives P(P∩Q) ⇒ P(Q) without the cyclic closure. The cyclic closure route is also valid: Rot(P∩Q) = Q ∩ {H ≥ 1}, with amb_{Rot}(w) = Σ_j amb(rot_j w).

### 2.3 Theorem A2 (each finite-depth certificate is equivalent to Q) [written proof]

For every finite k: P(Q) ⇒ P(L_k), with amb_{L_k}(w) = amb_G(μ(trunc_k w)). Together with A1, **P(L_k) ⇔ P(Q)**.

*Proof.*
1. A grammar G for Q pulls back along μ (E2) to a grammar for Q₃ with the same counts.
2. DFA product with R_k (regular).
3. Substitute σ (E1). ∎

**The converse of A1 at k = ∞ (P(Q) ⇒ P(P∩Q)) is OPEN.** The exact gap:
- L₁ ⊆ L₂ ⊆ ⋯ and ∪_k L_k = P∩Q.
  - Monotonicity holds because trunc_k is a function of trunc_{k+1}.
  - The union is exact: a word of block height < k has trunc_k equal to its block sequence.
- Each L_k is equivalent to Q *with a grammar that depends on k*. P(P∩Q) needs a single grammar that certifies "the first depth at which the truncated block cycle stops being periodic". That is a one-vs-rest comparison again (U3).
- Pulling back to P∩Q needs an intersection with the one-counter language P, which is not an allowed operation.

### 2.4 Lemma RG (renormalisation threshold) [written proof, elementary]

Let f be nondecreasing and unbounded, with f(n) ≥ C(n)·f(n^α)^s for all large n, where α ∈ (0,1) and s ≥ 1.

- (i) If sα > 1, then f is superpolynomial. Taking logs, φ(n) = log f(n)/log n satisfies φ(n) ≥ sα·φ(n^α) + log C/log n. Iterating log log n times gives log f(n) ≥ (log n)^{1+Ω(1)}.
- (ii) If sα = 1 and C is constant, f(n) = n^k/D with D^{s−1} ≥ C satisfies the inequality. So polynomials are not excluded.
  - Polynomials are excluded when C(n) ≥ n^δ. Then φ grows by δ per level, giving f ≥ n^{Ω(δ log log n)}.
- (iii) If sα < 1, every polynomial satisfies it for large n.

**Applying it to the block self-similarity.**
- The P-form gives ONE instance (the block sequence, or trunc_k) of length m = H + R ≈ 1.6√n on typical words (MC, §4). The blocks themselves are atoms compared only for equality. They are *not* Q-instances, so there is no product over blocks.
- So the best available inequality is amb(n) ≥ amb(m) with s = 1 and α = ½: case (iii), vacuous.
- Worse, the inequality only holds per word. The words of length n that carry an instance of length Θ(n) (e.g. σ_min-images, E4) already give the trivial monotonicity amb_{P∩Q}(n) ≥ amb_Q(n/6). The √n contraction exists only on typical words, and typical-word bounds do not count (§7).
- **What would be needed.** One of:
  - a *product* lemma at linear scale. For example, an exact CF "AND-gadget" e(u, v) ∈ Q ⇔ u, v ∈ Q with |e| = O(|u| + |v|), together with an inherent-ambiguity direct-product theorem. This gives f(N) ≥ f(N/c)², i.e. sα = 2·1 in linear scale, hence superpolynomial.
  - √n-many independent sub-instances (s ≈ √n).
  - Neither is known. No exact AND-gadget is known for Q: Q is a ∀p condition, and a power in one coordinate must force a global period [assessment]. Direct-product theorems for inherent ambiguity are not available in the literature I know [assessment, not checked].
- This extends §6 "morphic self-similarity" from finite codes to unambiguous CF substitutions with unique decoding (E1): **exactness kills amplification**.

## 3. Direction (B): the invariant certificate lands in the full problem

- **Which invariant.** A coarse block invariant φ gives a CF certificate by substitution only if φ is computed *letterwise by an unambiguous substitution*.
  - The top-level prime count r(D) qualifies (σ: x ↦ b D_b a). So do its depth-k refinements tr_k.
  - The semilength |D|/2 does not. Expanding x^ℓ into an arbitrary Dyck word of semilength ℓ needs a second stack interleaved with the grammar for the instance; it is not a substitution [sketch].
  - Neither does the height. "Unique deepest block" is the non-CF one-vs-each comparison (U3).
- **The instance.** With φ = r, the certificate is L₁ = σ(Q ∩ (x*a)⁺). This is exactly the slice "primitive sequences over ℕ in unary", i.e. Q ∩ (b*a)⁺ (the swap/mirror of Q ∩ (ab*)⁺), **with the number of blocks H free**.
  - By E3 this slice contains c(Q). So it is the full problem (A1/A2), not a fixed-n slice (ab*)ⁿ.
  - The fixed-n slices with bounded ambiguity (KK, unverified, ≤ 3 prime powers) need H fixed. Here H ≈ √n is unbounded, and H runs through all integers, including those with many prime factors.
- **Is the instance easier?** No.
  - Typical instance length is m ≈ 1.6√n, so a grammar for Q with amb n^k gives an L₁ grammar with typical amb O(n^{k/2}).
  - The worst case is still n^k, on words with r_i = O(1) blocks of height 1 (E4).
  - Depth refinements L_k are equally hard (A2).
- **Density.** See §4. L_k is sound, but the union over k is needed for exactness (§2.3), and that is the open uniformity.

## 4. Coverage numbers (diagnostic only; these languages are not claimed CF without a grammar for Q)

Miss = fraction of primitive classes with H ≥ 1 whose truncated block cycle is periodic (class-weighted; swap covers H ≤ −1).

| n | miss L₁ | miss L₂ | miss L₃ | E[H] | E[m = H+R] | m/√n |
|---|---|---|---|---|---|---|
| 12 (exh) | 0.0923 | 0.0077 | 0 | | | |
| 18 (exh) | 0.0791 | 0.0076 | 0.0005 | | | |
| 64 (MC 2000) | 0.044 | 0.004 | 0.001 | 7.1 | 13.8 | 1.73 |
| 256 | 0.017 | 0.0015 | 0 | 13.5 | 26.7 | 1.67 |
| 1024 | 0.010 | 0.0015 | 0 | 26.0 | 52.0 | 1.62 |
| 4096 | 0.0065 | 0.0005 | 0 | 52.3 | 104.8 | 1.64 |

- The L₁ miss is ≍ n^{−1/2}. It is dominated by H = 2 with r₁ = r₂, since P(H small) ≍ n^{−1/2}.
- L₂ and L₃ shrink further.
- Exactness, however, needs every class, including H = 2 classes with deep equal truncations. That is the k-uniformity gap again.

## 5. Computational checks (`r9_selfsim_exact.py 14 9 18`)

All exhaustive:
- (a) E3 for |u| ≤ 14.
- (b) E2 for |u| ≤ 9 over 3 letters.
- (c) Q ∩ (b*a)⁺ ↔ primitive run sequences, n ≤ 18.
- (d) E4 for k = 1, 2, 3.
- (e) L_k ⊆ L_{k+1} ⊆ P∩Q, and P∩Q = L_{height+1}, for all P words with n ≤ 18.

RESULT: **0 violations** in (a)–(e).

(f) E1 unique σ-decoding (`decode_check(12)`): every w ∈ P with |w| ≤ 12 has exactly one (t ∈ R_k, prime assignment) for k = 1, 2, 3, and no w ∉ P is produced. **0 violations.**

## Status

| claim | label |
|---|---|
| A1: P(L_k) ⇒ P(Q) for all k ≤ ∞; in particular P(P∩Q) ⇒ P(Q) | written proof + exhaustive checks |
| A2: P(Q) ⇒ P(L_k) for each finite k; so P(L_k) ⇔ P(Q) | written proof |
| P(Q) ⇒ P(P∩Q) | **OPEN**: exactly the uniformity over truncation depth k |
| Lemma RG: renormalisation excludes polynomials iff sα > 1 (or sα = 1 with C ≥ n^δ) | written proof |
| Block self-similarity gives s = 1, α = ½ (vacuous); the √n contraction is typical-only | written proof (per-word identity) + MC |
| (B) invariant certificate = unbounded-H slice Q ∩ (b*a)⁺ = full problem | written proof |
| semilength/height invariants not substitution-composable | sketch |
| coverage L₁ miss ≍ n^{−1/2}, L₃ ≈ 0 at n = 4096 | exhaustive n ≤ 18 + MC |
| amplification via self-similarity | **NO-GO for exact transfers**; would need an AND-gadget plus a direct-product theorem (open) |
