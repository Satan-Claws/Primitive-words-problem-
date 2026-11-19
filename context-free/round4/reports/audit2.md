# Audit2: adversarial audit of builder.md, cl1.md, crossing.md, transduce.md

**Claim status: I claim no proof of either resolution.** This is an audit only. All checks use scripts I wrote
myself; I did not reuse the agents' code. Scripts are in `context-free/round4/scripts/audit2/`:
- `builder_audit.py`
- `cl1_crossing_audit.py`
- `cl1_fail_summary.py`
- `crossing_audit.py`

Each runs in under 3 minutes on one core.

Verdicts: CONFIRMED / GAP / FALSE.

## Summary of verdicts

| Report | Claim | Verdict |
|---|---|---|
| builder | Lemma D / Theorem D (all d, d = n/2, n odd/even, both axis types) | CONFIRMED |
| builder | grammar = predicate; Cyc(L(S)) characterisation | CONFIRMED (n ≤ 14) |
| builder | density bound 2n·2^n·(3/4)^⌊(n−1)/2⌋ | CONFIRMED |
| builder | missed family F1 (m ≥ 2) | CONFIRMED |
| builder | half-imbalance n/6 | CONFIRMED |
| builder | "covers every primitive word of length ≤ 8" | GAP (trivial): fails at n = 1 |
| cl1 | Theorem 1 (L = a·P ⊆ Q), grammar, CL1 refuted | CONFIRMED |
| cl1 | cyclic-shift citation | CONFIRMED in substance; exact reference is HU79 Ex. 6.4(c) |
| cl1 | Theorem 2 (L_gen ⊆ Q, linear CF) | CONFIRMED |
| cl1 | "Cyc(L_gen) contains every one-a insertion into u^k for every u with ≤ 2 blocks / whenever β(u)^k is reflection-symmetric up to rotation" | **FALSE** |
| crossing | Lemma 1 (a)–(c) | CONFIRMED |
| crossing | Theorem 1 | GAP (literal): (ii) is unsatisfiable because of length-1 words; fixed by restricting to \|w\| ≥ 2 |
| crossing | Lemma 4 | **FALSE as stated** (length-1 counterexample); true after restricting F to length ≥ 2 |
| crossing | Lemma 2; no fooling pairs | CONFIRMED (no fooling pairs checked for lengths ≤ 10) |
| transduce | T1 (via closure.md Prop P) | CONFIRMED (Prop P re-audited) |
| transduce | T2 | CONFIRMED (minor presentational gaps) |
| transduce | Prop D | CONFIRMED (one imprecise line, bound unaffected) |
| transduce | DIST3, CROSS≠ not CF | CONFIRMED |

---------------------------------------------------------------------------------------------------
## 1. builder.md

**Lemma D (CONFIRMED).** Suppose w has period d, with d | n. Then w_i depends only on i mod d, and on ℤ_n this
is well defined because d | n.

Take j ∈ H with j ≡ c − i0 (mod d). Then:
- w_j = w_{τ i0} = b;
- c − j ≡ i0 (mod d), so w_{τ j} = a.

This is a strict reversed pair inside H, which contradicts dominance. If j = i0, the same congruences force
a = b, which is also a contradiction.

The special case (n even, c = 0, H = {1..n/2−1}, d = n/2) works: j = n/2 − i0 lies in H and j ≡ −i0 (mod n/2).

The hypothesis H ∩ τH = ∅ is never used in the proof. This is harmless.

**Parameter cases (CONFIRMED).**
- Y, n even: c = n−1, H = {0..n/2−1}, |H| = n/2.
- Y, n odd: |H| = (n−1)/2 ≥ n/3, and n/3 bounds every proper divisor.
- XY: c = 0. For n even, the pair i = (n−2)/2 of v is self-paired at position n/2. The grammar leaves this
  position free (Z → X), so H = {1..n/2−1}. For n ≥ 6, n/2 − 1 ≥ n/3. For n = 4, d = 2 is the special case.
  For n = 2, the language is empty.

**Theorem D and the characterisation of Cyc(L(S)).** I wrote an independent recursive recogniser for the
literal grammar and an independent predicate. The predicate is: some reflection c ∈ ℤ_n, all mixed pairs
have their b on one side of the axis (sides computed by (2i − c) mod 2n), and at least one mixed pair exists.

COMPUTER-CHECKED (`builder_audit.py`) for n ≤ 14:
- L(S) ⊆ Q;
- the set of rotations of L(S) ∩ Σ^n equals the predicate exactly;
- the density bound holds.

The missed-necklace counts agree with the builder's table: n = 9: 2, n = 11: 6, n = 12: 12, n = 13: 34,
n = 14: 58. The proof of the bound is correct: L(S) ∩ Σ^n has at most 2·2^n(3/4)^⌊(n−1)/2⌋ words, and there
are n rotations.

GAP (trivial): the registry says L(S) "contains every primitive word of length ≤ 8". The words a and b
(n = 1) are missed, since L(Y) has no words of length < 2. The table itself starts at n = 2, so it is correct.

**F1 (CONFIRMED).** The case analysis is correct. COMPUTER-CHECKED for 2 ≤ m ≤ 60. Note that m = 0 and m = 1
ARE covered (bbbab and bbababa), so the hypothesis m ≥ 2 is necessary and correctly stated.

Side remark: the sentence "no square, no 4th power" in the argument that Q ∩ bba\*baba\* is regular is
imprecise. A correct argument: a non-primitive word in this slice must be a square u² with u starting with
bb, which forces a bounded length. So only finitely many words are non-primitive, and the conclusion holds.

**Half-imbalance n/6 (CONFIRMED).**
- For p even, the imbalance is 0.
- For p odd, write u = u′u″ with |u′| = |u|/2. The imbalance is ||u″|_b − |u′|_b| ≤ |u|/2 = n/(2p) ≤ n/6.

COMPUTER-CHECKED for all even n ≤ 24: the maximum over all powers is ≤ n/6, with equality at n = 6, 12, 18, 24.

## 2. cl1.md

**Grammar and Theorem 1 (CONFIRMED).**
- COMPUTER-CHECKED: the grammar equals a·{block palindromes} for n ≤ 16, and L ⊆ Q for n ≤ 16.
- Fact B is correct: σ_d-invariance implies σ_gcd(d,k)-invariance, which gives w = u^{k/g}.
- The argument with D = e_1 − e_k is correct, because the σ_d-orbit of position 1 has size ≥ 2.

So CL1 is refuted.

**Citation (CONFIRMED in substance).** The construction is Hopcroft–Ullman 1979, Exercise **6.4(c)** (part (c),
not the whole of 6.4). The original proofs are Oshiba 1972 and Maslov 1973. Cyc(L) = {vu : uv ∈ L} is
exactly the operation used. Cyc(L) ⊆ Q because Q is conjugation-closed. Correct.

**Theorem 2 (CONFIRMED).** x − Rx = e_j − e_{k+1−j} ≠ 0 cannot be σ_d-invariant. The condition j ≠ k+1−j
forces k ≥ 2. COMPUTER-CHECKED: L_gen ⊆ Q for n ≤ 16.

**FALSE: the coverage claim after Theorem 2.** The claim reads: Cyc(L_gen) contains every one-a insertion into
u^k "whenever β(u)^k is reflection-symmetric up to rotation. In particular this holds for every u with at
most 2 blocks."

Counterexample: u = bab, so β(u) = (0,1). Take k = 2 and insert a to get w = baabbab. This word is primitive,
since its length 7 is prime. Its cyclic block vectors are the rotations of (0,2,0,1). No rotation x has a
j with x − e_j a palindrome and j ≠ k+1−j; I checked all 8 cases by hand and by script. Another example:
u = aabb, k = 2, inserted at the front, giving aaabbaabb.

COMPUTER-CHECKED (`cl1_fail_summary.py`): every 2-block u = a^i b a^j b with 0 ≤ i, j ≤ 4, for every
k ∈ {2,3,4}, has some one-a insertion outside Cyc(L_gen). That is 60 of 60 (u, k) combinations.

The cause is parity. L_gen uses only the reflection i ↦ k+1−i. Rotations change the reflection centre by 2
per block. If the block count K of u^k is even and every symmetry of β(u)^k is a reflection whose axis passes
through blocks, rotation cannot reach the standard reflection. Example: β = (2,0) repeated is symmetric only
about block axes.

The "lesson" therefore holds only when the reflection parity matches. The fix is to add the second reflection
type, i ↦ k − i (a block-centred palindrome with a free central pair), which is equally linear. I did not
re-verify a fixed version.

## 3. crossing.md

**Lemma 1 (CONFIRMED).**
- (a) and (b) are correct. The descent works for n ≥ 2.
- (c): COMPUTER-CHECKED (`crossing_audit.py`). For 200 random CNF grammars (4 nonterminals, bounded length 7),
  ⟨A⟩ = {zx : S ⇒* xAz} exactly.

**Theorem 1 (GAP, literal).** A b.c.f. requires n/3 < |y| ≤ 2n/3. For n = 1 that means 1/3 < |y| ≤ 2/3, which
is impossible. So the primitive words a and b have no b.c.f., and (ii) "every primitive word has a b.c.f. in
some L_i × M_i" can never hold. As literally stated, (i)⇒(ii) is false.

Fix: say "every primitive word of length ≥ 2". In (iii)⇒(i), add {a,b} to K. With this fix, both directions
are correct:
- (i)⇒(ii) is Lemma 1.
- (iii)⇒(i): K = ∪ L_i M_i is CF and K ⊆ Q. Cyc(K) is CF (HU Ex. 6.4(c)), Cyc(K) ⊆ Q, and Cyc(K) ⊇ Q.

**Lemma 4 (FALSE as stated; CONFIRMED after the fix).** Counterexample: L = Σ⁺ is rotation-closed and has
the CNF grammar S → SS | a | b, so g = 1. Take F = {a, b}. Neither word has a b.c.f., so the fooling
condition holds vacuously, but |F| = 2 > g.

The proof's step "by Lemma 1, each w ∈ F has a b.c.f." needs |w| ≥ 2. With F ⊆ Σ^{≥2}, the proof is correct.
The computations in the report use lengths ≥ 2, so they are unaffected.

**Lemma 2 (CONFIRMED).** COMPUTER-CHECKED for all ℓ, k < 40, p ∈ {2,3,5,7}, and all j.

**Fooling pairs.** I independently re-checked lengths 2..10 (224 primitive necklaces): there are 0 fooling
pairs. This agrees with the report.

I did not audit Theorem 3.

## 4. transduce.md (and its dependence on closure.md)

**Prop P (closure.md), re-audited (CONFIRMED).**
- Pigeonhole: take 2(n_V+1) output-carrying edges, and split them into two halves of n_V+1 edges each. Each
  half contains two edges with the same source vertex, so it contains a closed walk with nonempty output.
- The silent case pumps without changing the label.
- Otherwise, Lemma RC′ applies with Z ≠ ε. In its periodic alternative, j = 1 gives λ(π) ∈ ρ⁺ ∩ Q = {ρ}, so
  |XYZ| ≤ |Y|, which is a contradiction.
- The RC′ deletion step is correct: deleting a factor of length t|ρ| from ρ^M leaves ρ^{M−t}.

**T1 (CONFIRMED).**
- M(Q) is closed under composition, so M(T) ⊆ M(Q).
- Each reduction lands on a language with no u v^{≥k₀} w subset. Renaming the second block is a gsm map,
  not a morphism, but M(Q) is closed under rational transductions, so this is fine.
- Shorter route: {aⁿbaⁿb} itself already has no u v^{≥k₀} w subset.

**T2 (CONFIRMED).** The argument uses the following from closure.md:
- **Step A:** γ₁γ₂ has ≤ 4n_V − 2 < K₁ edges, so the support is preserved, and L₀ ≥ 6|g₁g₂|.
- **B2–B3:** these are as stated.

The key point is that a bounded output is determined by its Parikh vector, which is linear in the edge
counts. Then:
- the non-commuting pieces have image g(R_𝔱), which is regular;
- the commuting pieces lie in finitely many slices.

Minor presentational gaps:
- R has several final states, while CL uses a single target t. Split by final state.
- "ℓ ≥ L₀" must be included in R_𝔱. It is a regular condition.

**Prop D (CONFIRMED, one imprecise line).**
- In the rigid range, Lemma OB gives, for each pair (i, i+s), either e_i − e_{i+s} = δ or a finite set of
  pairs. So A_s is not exactly the stated set {e_i − e_{i+s} = δ}. Each condition still ties e_{i+s} to e_i up
  to finitely many choices, so the dimension stays ≤ gcd(r,s) ≤ ⌊r/2⌋.
- I re-derived the merge count m ≤ (number of fixed runs) ≤ k. A merge between originally adjacent free blocks
  reduces to the original merge condition at that index, which is false by hypothesis. This gives the generic
  bound (r − k + m)/2 ≤ r/2 and the self-merge bound r − k ≤ k.
- The r′ = 1 non-self-merge case is fine.
- (ab\*)⁴ is merge-free and attains the bound.

**DIST3 and CROSS≠ (CONFIRMED).** Ginsburg's Theorem 5.4.2 is cited correctly, in the stratified-linear-sets
form.
- **DIST3.** α < N, so 2N!/α and N!/α are integers. In the γ > 0 case, stratification forces β = 0.
- **CROSS≠.** The periods (α,0,γ,0) and (0,β,0,δ) are both periods of the same linear set containing P_N.
  They cross (1 < 2 < 3 < 4), so that set is not stratified. The intermediate step "α ≤ γ" is unnecessary but
  harmless.

## Registry entry
1. **Aimed at:** breaking the claims of builder, cl1, crossing and transduce.
2. **Proved:**
   - one FALSE claim: cl1's coverage claim for 2-block and reflection-symmetric bases, with explicit
     counterexamples baabbab and aaabbaabb;
   - crossing Lemma 4 is false as stated (counterexample L = Σ⁺, F = {a,b});
   - crossing Theorem 1(ii) is literally unsatisfiable (length-1 words).

   Each of these has a stated fix. All main theorems survive: Theorem D, cl1 Theorems 1 and 2, crossing
   Theorem 1 (after the fix), T1, T2, Prop D, DIST3, CROSS≠.
3. **Missing step:** none introduced. The open steps are unchanged.
4. **Counterexamples:** baabbab (u = bab, k = 2); aaabbaabb; L = Σ⁺ with F = {a,b}; a, b for crossing (ii) and
   for builder's "length ≤ 8" claim.
5. **Strength:** not applicable.
6. **Reopen:** the cl1 "lesson" (that every reflection-symmetric base is harmless) needs a corrected L_gen
   with both reflection parities before it is used.
