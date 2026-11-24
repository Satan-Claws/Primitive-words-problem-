# uniform.md — uniform witness grammars: one prime works, two primes are blocked

Scripts:
- `scripts/uniform_nonpow.py`: exhaustive parse-tree counts for G_p.
- `scripts/uniform_marked.py`: two-chord cone rays, and the markings of the single-defect words.

**Verdict.**
- **One prime: works.** For each fixed prime p, NonPow_p = {w : w ≠ u^p} has a uniform CFG G_p. Its ambiguity is
  exactly the number of mismatches, so it is linear [written proof; exhaustive check].
- **Two or more primes: blocked.** The trick does not extend to two primes. No CFG that *exposes* one mismatch pair
  per prime (as marked leaves) can cover even the primitive words a^{n−2}bb with n ∈ 6ℕ, whatever its ambiguity
  [written proof]. This is the word-level form of the §6 route "One witness per prime". I stopped there, as instructed.
- **NONUNIF is not decided.** Grammars that do not expose witnesses remain open (§4).

## 1. The single-prime grammar G_p [written proof]

Let p be prime and C → a | b. G_p has the following rules.
- S → R_r (1 ≤ r ≤ p−1), with R_r → C^r | C^p R_r. These generate lengths ≢ 0 mod p, each unambiguously.
- S → P[c,σ] M[p−2−c,τ] for σ ≠ τ ∈ {a,b} and 0 ≤ c ≤ p−2.
- P[c,σ] → C^{p−1} P[c,σ] C | C^c σ. This generates {xσy : |x| = (p−1)|y| + c}.
- M[d,τ] → C M[d,τ] C^{p−1} | τ C^d. This generates {zτt : |t| = (p−1)|z| + d}.

**Correctness.** Write w = xσ·yz·τt.
- From the rules, n = |w| = p(|y|+|z|+1). So the marked letters σ and τ are exactly n/p apart.
- Conversely, take a mismatch w[i] ≠ w[i+m], with m = n/p and i < (p−1)m. Then c = i mod (p−1) and |y| = ⌊i/(p−1)⌋
  are forced, and |z| = m−1−|y| ≥ 0.
- A word of length pm is a p-th power iff it is m-periodic. Hence L(G_p) = NonPow_p.

**Exact ambiguity.**
- If p ∤ n, then amb_{G_p}(w) = 1.
- If p | n, then amb_{G_p}(w) = A_p(w) := #{ i < (p−1)n/p : w[i] ≠ w[i+n/p] } ≤ (p−1)n/p.
- The bound is attained (for example by a^m b^m when p = 2), so the ambiguity is exactly linear.

Every derivation is one *chord* of span n/p. The span is not counted directly. It is enforced by the ratio
"outside : inside = (p−1) : 1", using the linear counters P and M on either side of the cut between y and z. This is
the classic non-square trick (the case p = 2) generalised.

**Check [computational].** `uniform_nonpow.py` compares parse-tree counts with the formula for every binary word, for
p = 2, 3 (|w| ≤ 12), p = 5 (|w| ≤ 10), and p = 7 (|w| ∈ {1, 6, 7, 13, 14}): 43 196 words, 0 disagreements. The maximum ambiguity at length n is (p−1)n/p (e.g. 6 at n = 12 for p = 2, and 12 at n = 14 for p = 7).

**Relation to Lemma A (`PA/poly_A2.md`).**
- Lemma A forbids *canonical* (equality-based, "first non-zero fibre") per-prime choices.
- G_p never canonicalises: it is the union over all mismatches. Choosing the first mismatch would need
  w[j] = w[j+m] for all j < i, which is a copy constraint.
- So G_p evades Lemma A for one prime, at the price of linear ambiguity. For finitely many primes the product of
  witness counts would still be polynomial (n^{|P|}). The obstruction is therefore not ambiguity but coexistence,
  which §2 covers.

## 2. Two primes: witness-exposing grammars do not exist [written proof]

**Definition.** A grammar is *(p,q)-witness-exposing* for a language L if it is a CFG G′ over Σ × {0,1,2} such that:
- every word of L(G′) has exactly one pair of 1-marks, at positions (i, i+n/p) with different letters, and exactly
  one pair of 2-marks, at (j, j+n/q) with different letters;
- L ⊆ π(L(G′)), where π erases the marks.

The grammars of §1, multiplied across primes, would be of this kind. So would any "ring gadget of span n/p_k" family
in the sense of `realise.md` §3 that makes its chords visible.

**Theorem W.** Let p < q be primes. Let L be any language that contains w_m := a^{n−2}bb with n = pqm for infinitely
many m. Then L has no (p,q)-witness-exposing grammar. Note that w_m is primitive, so w_m ∈ Q ∩ T, where
T = NonPow_p ∩ NonPow_q ∩ Σ^{pqℕ}.

*Proof.*
1. **The admissible marks.** In w_m:
   - the p-mismatches are exactly i ∈ {n−n/p−2, n−n/p−1}, since the shift must hit a b;
   - the q-mismatches are exactly j ∈ {n−n/q−2, n−n/q−1}.
   - Every admissible marking therefore marks both b's (one with 1, one with 2) and two a's.
   - The a-runs before, between and after the two marked a's have lengths
     (x, y, z) = (n − n/p, n/p − n/q, n/q) − O(1), with each error at most 3.
   - All three slopes in m are positive because q > p. (Checked in `uniform_marked.py`.)
2. **Restrict to one shape.** Let R = a*·a⁽ᵏ⁾·a*·a⁽ˡ⁾·a*·{b⁽¹⁾b⁽²⁾, b⁽²⁾b⁽¹⁾} with {k, l} = {1, 2}, which is regular.
   Then K := L(G′) ∩ R is CF. By step 1 it contains, for infinitely many m, at least one marking of w_m. Every word
   of K is such a marking, because R plus the marking rules force the shape a^{n−2}bb.
3. **Pump.** Take a long word in K and apply the CF pumping lemma.
   - Neither v nor y can contain a marked letter or a b, since R fixes their number.
   - So vxy lies in at most two of the three a-runs.
   - Pumping t → ∞ leaves at least one run fixed while another grows without bound.
   - Every word of K has all three runs within O(1) of fixed positive multiples of m. The pumped words leave K,
     which is a contradiction. ∎

**Corollaries.**
- **Q.** No CFG for Q (or for any L with {w_m} ⊆ L ⊆ Q) exposes one mismatch witness per prime for primes 2 and 3
  simultaneously. This holds even for exponentially ambiguous grammars.
- **The single-defect family.** The words w_m are, in a-coordinates, the single-defect words of §6 ("fails on
  single-defect words when n has ≥ 2 primes"). Theorem W is that block made rigorous at grammar level, and it applies
  to unions, not only to canonical choices.
- **Cone check [computational].** `uniform_marked.py` covers every relative order of the four marked positions
  (including coincidences) for (p,q) = (2,3), (2,5) and (3,5). Every feasible order has a homogeneous cone whose
  extreme rays all have support exactly 3, and none has support 2. So no order of two exposed chords is stratifiable
  (Ginsburg), not just the nested order used above.

## 3. What a CFG can generate uniformly

**What works.**
- One chord of span n/p per derivation spine, enforced by ratio counting against the *whole* outside.

**What fails.**
- A second chord of span n/q (q ≠ p) also needs ratio counting against the whole outside.
- The two counting relations then share the outside letters with different ratios. Theorem W shows this is not CF,
  for every arrangement: nested, crossing or disjoint.
- In the vocabulary of `realise.md`, the transport family's ring spans s_k = n/p_k cannot be realised as *visible*
  chords for two or more primes in one skeleton. Its open question about uniform refinement is answered negatively
  for visible-chord refinements.

## 4. Status

| claim | status |
|---|---|
| NonPow_p has a CFG with amb = A_p(w), exactly linear, for all lengths | [written proof] + [computational] check |
| Witness-exposing grammars for ≥ 2 primes do not exist, even on {a^{n−2}bb} ⊆ Q | [written proof] (Theorem W) |
| Every order of two exposed chords is non-stratified | [computational], p,q ≤ 5 |
| Is T = NonPow_2 ∩ NonPow_3 ∩ Σ^{6ℕ} CF? (implicit certification) | OPEN |
| NONUNIF | NOT decided |

On the open row:
- Proving T non-CF by Ogden or pumping on bounded letter-count shapes is the §6-blocked route. [assessment, hand argument only] On bounded run-shapes, landing in
  V_{n/2} ∪ V_{n/3} needs the defect vector to be proportional to the pump direction, and that direction's ratio
  α:β is chosen adversarially. So no single word defeats every two-run pump.
- Grammars that certify non-periodicity without exposing a witness pair (for example by hiding the witness inside
  counter nonterminals that do not fix positions) are untouched by Theorem W.
- **One-line stop:** the remaining affirmative route for ≥ 2 primes is "one witness per prime" (§6, Lemma A), now
  rigorous at word level. Stopped.
