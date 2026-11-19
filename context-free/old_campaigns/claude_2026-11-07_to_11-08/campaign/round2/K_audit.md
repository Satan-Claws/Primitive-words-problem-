# Round 2 / K: adversarial audit of the round-1 theorems

Auditor K. I re-derived every claimed proof below in my own words, step by step, using the checklist in PROBLEM.md:
- quantifier order;
- ε and exponent conventions;
- closure misuse;
- ambiguity-class confusion;
- off-by-one errors;
- the cases n = 1 and single-letter powers;
- numerics presented as proof;
- misquoted hypotheses.

Spot checks are in `/tmp/claude-5714/-home-shobhit--claude-spares-spare-fauO4P/6f48459d-5790-4a18-bccc-eabb8efc4544/scratchpad/r2_audit/`. Each `*.py` file has a matching `*.out` file.

## Verdict table

| # | Claim | Verdict |
|---|---|---|
| 1a | G Thm 2: Q_n is an exact union of O(n) balanced Q-rectangles, ≤ 8 for odd n | **CERTIFIED WITH FIXES.** There is an off-by-one in the "balanced" shape when 3 \| n; it is repaired by non-wrapping windows. |
| 1b | G Lemma 1 (slice grammar): ≤ \|N\|·n nonterminals | **CERTIFIED** |
| 1c | (side claim) G Prop 5 / REGISTRY: "c·n ≤ min grammar size of Q_n" | **FALSE.** For prime n, Q_n has a CNF grammar with O(log n) nonterminals. |
| 2a | B Thm 1: interchange barrier with fraction 1/(e(ω(n)+1)) | **CERTIFIED** (one trivial edge case: m = n = 2) |
| 2b | B Thm 2: box barrier (8m)^{ω(n)}, and Cor. 3 | **CERTIFIED** |
| 3 | C Lemma A, Lemma B, Thm 1 | **CERTIFIED.** I reproduced the finite Z₆/Z₁₂ sub-case of Lemma B. |
| 4 | D Thm 2: 2-ambiguous CFL with a non-algebraic, non-D-finite GF | **CERTIFIED.** "Inherent ambiguity exactly 2" is true but not needed. |
| 5 | A Thm A: OG preserved by rational transductions, reversal and cyclic shift | **CERTIFIED WITH FIXES.** Parts (a)–(c) are correct, with a small constant fix in (b). The proof of part (d), cyclic shift, has a real gap in the mark count. The registry's conclusion still holds through a different, Q-specific argument (§5.4). The remark "the same proofs work for Bar-Hillel" is unjustified. |
| 6a | E Lemma 2 (semilinearity) | **CERTIFIED** |
| 6b | E Lemma 3 (L₁ = {k≥i, k≥j}, L₂ = {k≠i, k≠j} are not CF) | **CERTIFIED.** The remark that they are "the regular slices" of the transversals is imprecise (≥ vs >). |
| 6c | E Lemma 5 (cyclotomic barrier) | **CERTIFIED** (needs n ≥ 2 for the affine-to-linear step) |

None of these items moves the main problem. They are all barrier or no-go results, and every one of them is a restricted-model statement.

---

## 1. Route G

### 1a. Theorem 2 (explicit balanced cover)

**My re-derivation.** E = D∖{n/2} is closed under gcd. For distinct d₁ < d₂ in E we have gcd ≤ d₁ < d₂ ≤ n/3, and gcd is a proper divisor, so it lies in E. The bounds M₁ ≤ n/3 hold for every n. M₂ ≤ n/4 holds for even n and M₂ ≤ n/5 for odd n, because the elements of E are n/k with k ≥ 3, and odd n forces k odd.

**Lemma 3 (period extension).** Let u be the last d letters of X. Then X is a suffix of u^r. The word u has period g with g | d, so u = v^{d/g}, and X inherits period g. ✓

**Lemma 4 (chain).** Consecutive windows X_k and X_{k+1} overlap in O, which is a suffix of X_k and a prefix of X_{k+1}.
- |O| ≥ λ−s ≥ max(M₁+M₂−1, M₁).
- If the least E-periods d_k ≠ d_{k+1}, then d_k + d_{k+1} − gcd ≤ M₁+M₂−1. Fine–Wilf gives O the period g = gcd ∈ E.
- Lemma 3 applies with |O| ≥ M₁ ≥ d_k. It gives X_k the period g, and minimality of d_k forces g = d_k. Symmetrically g = d_{k+1}, a contradiction.
- So all windows share one period d. For each i there is t ∈ T with offset (i−t) mod n ≤ s−1, and then (i−t)+d ≤ s−1+M₁ ≤ λ−1. Hence w_i = w_{i+d} cyclically, and d | n, so w is a power. ✓

**Theorem 2.**
- Soundness of A_t and B_{t,i,a}: ✓.
- Coverage. Both ends of a pair {i, i+n/2} cannot lie in the window: they would sit at linear distance exactly n/2 inside a window with period n/2. Both cannot lie in the complementary arc either, since ⌈n/3⌉ < n/2+1. ✓
- Count of admissible i: offsets o with λ−n/2 ≤ o < n/2, which is exactly n−λ = ⌈n/3⌉. ✓
- Window counts: s ≥ (n+4)/12 for even n, giving ≤ 12 windows. s ≥ (2n+5)/15 for odd n, giving ≤ 8 windows. ✓

**Faulty step (off-by-one, checklist item "lengths").** The proof says that one of the arcs J_t, J̄_t is a linear interval "of length λ or ⌈n/3⌉, both in [n/3, 2n/3]", and therefore that each piece "has the shape required in Lemma 2".
- Lemma 2 needs the yield length in the half-open range (n/3, 2n/3]. This is forced by its proof, which uses ℓ > parent/2 > n/3.
- When 3 | n, a window with t > n−λ wraps around 0. Its only linear side is then J̄_t, of length n/3, which is not in (n/3, 2n/3].
- `g_cover.py` counts the pieces with no admissible linear side: n=6: 5 of 15, n=12: 27 of 54, n=18: 39 of 65, and n=3, 9, 15: 1–3 pieces each. For every n with 3 ∤ n the count is 0.
- Exactness of the union itself holds for every n tested (binary n ≤ 20, ternary n ≤ 11).

**Fix (certified).** Use only non-wrapping windows [t, t+λ) with T ⊆ [0, n−λ], 0 ∈ T, n−λ ∈ T and gaps ≤ s. This is already G's Theorem 3 form. The yield is then the window, of length ⌊2n/3⌋ ∈ (n/3, 2n/3] for every n ≥ 2.
- The chain argument gives a *linear* period d on all of w. Since d | n, w is a power.
- For B-pieces, the linear partner i ± n/2 cannot also lie in the context: that would need n/2 ≥ λ+1, or t > n/2.
- The number of windows only drops, to ≤ ⌈(n−λ)/s⌉+1. That is ≤ 4 for odd n and ≤ 6 for even n.
- Verified exact, and of the correct shape, for binary n ≤ 20 and ternary n ≤ 11 (`g_cover.out`, "linear" columns).
- All conclusions (≤ 8 pieces for odd n, O(|Σ|n) pieces in general, fooling sets of size O(n)) survive.

**Edge cases.** n = 2: E = ∅, λ = 1, A_t = ∅, and the B-pieces give {ab, ba}. ✓ n = 1 is excluded by the hypothesis n ≥ 2, and Q₁ = Σ is trivial.

### 1b. Lemma 1 (slice grammar)

Induction on ℓ: (A,ℓ) ⇒* y iff A ⇒* y and |y| = ℓ. In CNF a length-1 yield must come from a rule A → a. A possible S → ε does not matter because n ≥ 1. The grammar has |N|·n nonterminals and ≤ |P|·n² rules. **Certified.**

The threshold statement in the registry is also correct: "ω(n) CNF nonterminals along a subsequence refutes CF-ness". The grammar G is fixed, so CNF conversion costs only a constant.

### 1c. Side finding: the lower bound "c·n ≤ μ(Q_n)" (G Prop 5 and the REGISTRY) is false

For prime n, Q_n is the set of non-constant words. Take a binary addition chain C for n, with |C| ≤ 2log₂n + O(1), and for each ℓ ∈ C nonterminals U_ℓ (any word), A_ℓ (contains a), B_ℓ (contains b) and M_ℓ (contains both). For ℓ = ℓ₁+ℓ₂ the rules are:
- U → UU
- A → AU | UA
- B → BU | UB
- M → MU | UM | AB | BA

`g_loggrammar.py` checks L(M_n) = Q_n exhaustively for n = 5, 7, 11, 13, 17. The grammar has 27 nonterminals at n = 13 and 155 at n = 1 000 003.

The same doubling trick, N_{2r} = U_r N_r | N_r U_r, gives polylogarithmic grammars for the non-p-th powers. So the only valid unconditional lower bound is Ω(log n). This does not hurt the route, since ω(n) is still the refutation target. But the registry line "Known: c·n ≤ min size" should be deleted.

---

## 2. Route B

### 2a. Theorem 1 (single-window barrier)

**Re-derivation.**
- A word of length n is non-primitive iff it is (n/p)-periodic for some prime p | n.
- If ℓ ≤ n/2, the context arc has length n−ℓ ≥ n/2 ≥ n/p. That arc meets every residue class mod n/p, so it determines the unique (n/p)-periodic completion, if one exists. Hence each row has ≤ ω(n) zeros. The case ℓ ≥ n/2 is symmetric, for columns.
- `b_barrier.py` checks this exhaustively for binary n ≤ 14, all windows: the maximum is exactly ω(n).
- Random S with each middle included at rate π = 1/(ω+1), and A(S) = {contexts with no zero in S}. For (c,x) ∈ R we have x ∉ zeros(c), so the event "x ∈ S and zeros(c) ∩ S = ∅" has probability π(1−π)^{|zeros(c)|} ≥ (1/(ω+1))(ω/(ω+1))^ω ≥ 1/(e(ω+1)). Linearity of expectation finishes the proof. ✓

**Quantifiers.** The interchange lemma (ORW 1985) reads: ∃c_L ∀n ∀R ⊆ L_n ∀m ∃ window ∃Z, with |Z| ≥ |R|/(c_L n²). B quotes this correctly. Theorem 1 gives the conclusion for *every* window, with c = e, using ω(n)+1 ≤ n². That is strictly stronger than needed.

**Edge case.** For m = n = 2 we need ℓ = 2 = n, which is outside Theorem 1's range ℓ ≤ n−1. But then the context is empty and Z = R works trivially. Harmless.

**Corollary 2.** K > e(ω+1)·n·ln|Σ| copies, then a union bound over ≤ |Σ|ⁿ entries. ✓

**Empirical check.** The worst window fraction is 0.229–0.278 for n = 6, 10, 12, against the bound 0.123. Every cross-swap was verified.

### 2b. Theorem 2 (box barrier)

**Re-derivation.**
- For d = n/p, the map k ↦ (piece(k), piece(k+d mod n)) has ≤ (m−1) + (m−1) + 1 internal breakpoints, so there are ≤ 2m classes. On each class β, φ(β) = β+d does not wrap and lies in one piece.
- Primitivity gives a class β_p with z|β_p ≠ z|φ(β_p). Pigeonholing over the tuples (β_p)_p costs (2m)^ω.
- Take independent uniform random sets T_p. The box conditions "y|β_p ∈ T_p" and "y|φ(β_p) ∉ T_p" each involve a single coordinate, because each class lies in one piece. Every reassembly then has w|β_p ≠ w|φ(β_p) for every p, so it is primitive.
- For a fixed z ∈ R′ the two strings z|β_p ≠ z|φ(β_p) are distinct, so the probability for each p is exactly 1/4, independently across p. The total loss is (8m)^ω. ✓

**Corollary 3.** 16t+8 ≤ 24t; sup 24^{ω(n)}/n² < ∞; t^{ω(n)} ≤ n^{log₂t} ≤ n^{2(t−1)}. ✓ (Take C₁ ≥ 1.)

**Certified.**

---

## 3. Route C

### Lemma A
- Suppose x is α-invariant and y is β-invariant, with α, β ≢ 0, and they differ only at p.
- If α+β ≢ 0, then p+α, p+β and p+α+β all differ from p. The chain y(p) = y(p+β) = x(p+β) = x(p+α+β) = y(p+α+β) = y(p+α) = x(p+α) = x(p) is valid and gives a contradiction.
- If α+β ≡ 0, both words are α-invariant, so {p} would be α-invariant, which is impossible. ✓
- This holds over any alphabet. Non-primitive words exist only for n ≥ 2, so length 1 is vacuous.

### Lemma B
- Step 1 (δ ∈ {α, β, α+β}) is the chain argument of Lemma A. ✓
- Step 2: if A = ∅, then H₁ = {0, δ} and δ = n/2. Otherwise α+β ∈ {0, δ} forces |A|, |B| ≤ 2, so a, b ≤ 4.
- If g = gcd(a,b) ≥ 2, both words are n/g-invariant, so the 2-element difference set is a union of orbits of size g. That forces g = 2 and the two positions to be antipodal. ✓
- The coprime pairs (a,b) ∈ {(2,3),(3,2),(3,4),(4,3)} reduce to residue classes mod n/(ab).
  - If p and q lie in different classes, Lemma A applies inside one class.
  - If they lie in the same class, the problem is finite, on Z₆ or Z₁₂. I re-ran it with a+b letters, which is enough for every equality pattern. Z₆ has 60 exactly-2 pairs, all antipodal. Z₁₂ has none. So the finite step is a legitimate exhaustive proof, not numerical evidence.
- Global exhaustive check (`c_lemmas.py`): binary n ≤ 24, ternary n ≤ 14 and 4-ary n ≤ 12. There are no distance-1 pairs, and all 45 057 / 21 324 / 46 422 distance-2 pairs are antipodal.

**Certified.**

### Theorem 1

**Path lemma.** A single toggle of a D-position changes each crossover in exactly one letter. Lemma A forces the non-primitive crossover to alternate between c₁ and c₂. c₁(I₁) and c₁(I₃) differ exactly at {p, q}, so Lemma B gives |p−q| = n/2. ✓

**Walk.** The walk [0,m) → [0,m+1) → [1,m+1) → … → [n−m, n) touches every position, because m ≤ n/2. So D ⊆ {p₀, p₀+n/2}. The three end cases each produce an interval whose crossovers are {w, w′}:
- |D| = 1: some length-m window misses D, because n ≥ 2m.
- |D| = 2 and m < n/2: the window [p₀+1, p₀+m+1) misses D.
- |D| = 2 and m = n/2: the interval [p₀, p₀+n/2+1) contains all of D.

I checked the index ranges in each case. ✓

**Checks.** Exhaustive for all pairs at n ≤ 10 (489 555 pairs at n = 10, 0 failures). Also 3000 near-power pairs at each of n = 12, 16, 18, 24, 30, with 0 failures. This agrees with G's finding of no 2-element fooling sets for 5 ≤ n ≤ 10. At n = 4 the balanced range (4/3, 8/3] contains only length 2, so lengths m and m+1 are not both available. That explains G's n = 4 exception and is not a contradiction.

**Certified.** Lemma S and Theorem 2/3 were not in scope. Lemma S is open, as C states.

---

## 4. Route D, Theorem 2

**Set identities.**
- L₁ = (P#)*(P ∪ {a,b}*) and L₂ = {a,b}*(#P)*(ε ∪ #{a,b}*), with P = {u#u^R}. Both factorizations are unique.
- Both languages are DCFLs: push the odd (respectively even) segment, then pop and compare.
- L₁ ∩ L₂ = {u#u^R#u#…}. ✓

**GFs.** I derived them by hand:
- GF(P) = z/(1−2z²);
- GF((P#)*) = (1−2z²)/(1−3z²);
- this gives the stated rational GF(L₁) and GF(L₂).

GF(L₁∩L₂) = Σ_m z^{m−1}/(1−2z^m), because the word determines (u, m). `d_gf.py` checks all three GFs against brute force over {a,b,#}, n ≤ 12.

For the binary code h, GF(h(L₁∩L₂)) = Σ z^{4(m−1)}/(1−z^{2m}−z^{3m}). It was brute-forced for n ≤ 22 (`d_binary_bf.py`) and matches for n ≥ 1. The constant term 1 is ε = h(ε), which is in L₁∩L₂ (m = 1, u = ε). The real root of x²+x³ = 1 is x₀ = 0.75488. The other two roots have modulus 1.151 > 1, so inside the disk the poles are exactly z^m = x₀.

**Analytic claims.**
- The poles of the m-th term lie on the circle of radius 2^{−1/m}. These radii are distinct for distinct m, and the tail of the sum is uniformly convergent on |z| ≤ r < 1, so no poles cancel.
- The poles e^{2πij/m}2^{−1/m} are dense near every point of |z| = 1, so the unit circle is a natural boundary.
- Hence the GF is neither algebraic nor D-finite, since both classes have finitely many singularities.
- Adding the rational GF(L₁) + GF(L₂) cannot cancel infinitely many poles. ✓

**Ambiguity.**
- L = L₁ ∪ L₂ has a 2-ambiguous grammar: the union of two unambiguous grammars.
- Its GF is not algebraic, so Chomsky–Schützenberger shows L is not unambiguous.
- Hence the inherent degree of ambiguity is ≥ 2, and the grammar gives ≤ 2. "Exactly 2" is correct.
- **It is not needed.** The barrier only requires that *some* finitely ambiguous CFL has a Q-like GF. Inherent ambiguity is a free corollary of the GF, not an input.
- No ambiguity classes are confused: D explicitly restricts the conclusion to "analytic features cannot exclude finite ambiguity".

**Certified.**

---

## 5. Route A, Theorem A (OG closure)

Recall: OG(L) means that π⁻¹(L)∩R satisfies Ogden for every letter-to-letter π and every regular R.

### 5.1 The Nivat reduction and part (a), alphabetic image, possibly erasing: correct
- Alignment alphabet Ξ = {(θ,δ) : π′(θ) = g(δ)} ∪ {(□,δ) : g(δ) = ε}. Then π′⁻¹(g(L))∩R′ = g₁(π₂⁻¹(L) ∩ g₁⁻¹(R′)), with π₂ letter-to-letter. ✓
- Ogden transfers through g₁ because marks are placed only on non-erased letters.
  - A marked letter in VX′ maps to a marked letter in g₁(VX′).
  - The marks in vwx cannot increase.
  - The pumps are images of pumps.

  ✓ The erasing case is handled correctly *for Ogden*.

### 5.2 Part (b), inverse alphabetic morphism with erased letters: correct after a constant fix
- **Case 1** (some erased block e_i holds ≥ s+1 marks): a DFA loop between two cut points. ✓ The s+1 marks must be taken *consecutively* so that v holds ≤ s marks. This is implicit in the proof.
- **Case 2** (annotate c_i with the monoid element of e_i, and c₁ also with e₀):
  - Lifting is done position by position, so every pumped copy carries its own factor.
  - Membership of the pumped annotated word in R″ certifies that the lift lies in R′.
  - The f-image of the lift equals the π-image, which is in L′. ✓
  - **Constant slip:** the first factor e₀c₁e₁ can hold up to 2s+1 marks, not s+1. So the lifted window bound is (2s+1)·p_ξ, and one should take P = (2s+1)(p_ξ+1).
  - Uniformity holds: p_ξ depends only on (f, R′).

### 5.3 Part (c), reversal: correct
π⁻¹(L^R)∩R = (π⁻¹(L)∩R^R)^R, and Ogden is symmetric under reversal.

### 5.4 Part (d), cyclic shift: the proof has a gap

**The step that fails.** The proof restricts the marking to a window that holds exactly P′ marks, and applies Ogden to the rotated word s = xy. Ogden then bounds only the *window* marks inside VWX′. The conclusion of Ogden for t needs a bound on the *original* marks inside vwx. Two cases break:

- **Same-part case.** VWX′ is contiguous, contains a window mark, and contains ≤ p window marks. It can still run out of one end of the window into a region with arbitrarily many original marks. Nothing bounds those.
- **Mixed case** (V in the x-part, X′ in the y-part). The new vwx in t is X′·y₂x₁·V. The proof says "x₁ lies inside the chosen window". That is false in general: x₁ is the whole prefix of x before V. Also y₂ is unmarked only in the *restricted* marking, not in the original one.

Marking everything does not fix this either. In the mixed case the vwx in t is the complement of W, which can hold ≥ P − p original marks. The same mixed case also defeats the "Bar-Hillel works too" remark: there |vwx| is unbounded. So OG closure under cyclic shift for *arbitrary* L is **unproved**. I found no counterexample.

**Repair, sufficient for the registry's conclusion.** I prove the following lemma.

*Lemma K1.* If L = cyc(L), then for every rational transduction τ, cyc(τ(L)) = ⋃_q τ′_q(L) is again a rational transduction of L.

*Proof.* Normalize the transducer T so that each transition outputs ≤ 1 letter. Then a split of an output xy happens between transitions, at some state q, and corresponds to a split w = w₁w₂ of the input.

τ′_q works in two phases:
1. Simulate T from q on a prefix (this will be w₂) until some final state.
2. Switch by an ε-move to q₀, simulate T on the rest (this will be w₁), and require that it ends in q.

The output is yx.
- (⊆) If xy ∈ τ(w) with w ∈ L, then w₂w₁ ∈ L because L is cyclically closed, and τ′_q(w₂w₁) ∋ yx.
- (⊇) If τ′_q produces yx from v = w₂w₁ ∈ L under a guessed split, then xy ∈ τ(w₁w₂), and w₁w₂ ∈ L because L is cyclically closed. ∎

Similarly, τ(L)^R = τ^R(L^R) = τ^R(L) when L = L^R.

Q is closed under both rotation and reversal. By induction along any chain of permitted operations, every language reachable from Q is τ(Q) for a single rational transduction τ. Parts (a) and (b), which are certified, then give OG(τ(Q)) from OG(Q).

So the registry statement holds *for chains that start at Q*: "closure chains + Ogden refute CF-ness iff Ogden fails on some π⁻¹(Q)∩R". The general claim "OG is closed under cyclic shift" should be withdrawn, or labelled as unproved.

**Bar-Hillel remark.** "The same proofs work with the Bar-Hillel lemma" is unjustified for (a) as well as (d).
- (a) needs marks on the non-erased letters only. Under Bar-Hillel, VX′ may consist entirely of erased letters, and then g₁(v)g₁(x) = ε.
- (d) fails in the mixed case, as explained above.

Only (b) and (c) transfer to Bar-Hillel. In practice this is harmless, since Ogden subsumes Bar-Hillel, but the sentence should be deleted.

**Verdict:** CERTIFIED WITH FIXES (for chains from Q, via Lemma K1). The cyclic-shift clause as a general theorem is FLAWED (proof gap).

---

## 6. Route E

### 6a. Lemma 2 (semilinearity)
- S = {(d,n)} is the Parikh image of a CFL, after a gsm that maps letters between the marks to one symbol and all letters to another. So S is semilinear.
- Every nonzero period has v_n > 0, since otherwise d ≥ n somewhere.
- Along a ray from the base in direction v, K = v_n d − v_d n is constant, and gcd(d,n) | K.
- If K ≠ 0: pick a prime q ∤ v_n K. Since v_n is invertible mod q², some t ≥ 0 gives q² | n. But n = g·p with g | K forces q² | p, which is impossible.
- So every period is collinear with the base. Then the component lies on a single line d/n = c, and n/gcd(d,n) = denom(c) is a single prime.
- Finitely many components give finitely many primes. ✓
- For prime n, n/gcd(d,n) = n, so only finitely many prime lengths occur. This matches the "misses long prime lengths" remark.

The quantifiers are correct, and the restricted model is stated honestly. **Certified.**

### 6b. Lemma 3
- **L₁ = {aᵏbaⁱbaʲ : i ≤ k, j ≤ k}** with z = aᴺbaᴺbaᴺ and Bar-Hillel pumping.
  - Pumps containing b fail at i = 2.
  - Pumps touching block 1 fail at i = 0, since then k < j.
  - Pumps confined to blocks 2–3 fail at i = 2.
  - Every decomposition fails. ✓
- **L₂ = {k ≠ i, k ≠ j}** with Ogden, block 1 marked, and z = aᴺba^{N+N!}ba^{N+N!}.
  - vx must meet block 1, and contains no b.
  - With t = |v| ≤ N (or |vx| when both pieces lie in block 1), choose i = 1 + N!/t. Then block 1 equals block 2 or block 3 when the other is untouched.
  - This includes the case "v in block 1, x in block 3", which Ogden allows because block 2 is unmarked. Block 2 is then fixed at N+N!, and k reaches N+N!. ✓

**Imprecision.** E says these are "the regular slices" of the transversals "unique longest run" and "unique run length". For L₂ that is accurate. For "unique longest" the slice condition is strict (k > i, k > j), not L₁'s ≥. The same proof works with z = aᴺbaᴺ⁻¹baᴺ⁻¹.

If "unique longest run" is meant over all runs, its slice is a *union* over which block is the maximum, and neither proof covers that union. So the parenthetical "so those transversals are not CF" is proved only for the front-anchored versions.

**Lemma 3 itself is certified.**

### 6c. Lemma 5 (cyclotomic barrier)
- A sound P_n means L_n vanishes on all non-primitive 0/1 vectors. These span ΣA_p: the indicators of residue classes mod n/p are 0/1 vectors.
- In Q[x]/(xⁿ−1), A_p is the ideal generated by (xⁿ−1)/(x^{n/p}−1) = ∏_{d|n, v_p(d) = v_p(n)} Φ_d.
- A sum of ideals is generated by the gcd of the generators, which is Φ_n. So ΣA_p = (Φ_n), and the missed primitive words are exactly those with Φ_n | w(x). ✓
- `e_cyclo.py`: rank(ΣA_p) = n − φ(n) for n = 6, 10, 12, 15, 18, 20.
- The primitive words with Φ_n | w form 2, 24 and 6 classes at n = 12, 18, 20, which matches E's numbers. aabaabbaaabb is one of them. There are 0 classes at n = 6, 10, 15.
- **Hypothesis to state:** for "weighted count ≠ 0" with *affine* weights (r per a, −s per b), the reduction to linear uses the fact that aⁿ is non-primitive, i.e. n ≥ 2.
- The de Bruijn citation (n = pᵃqᵇ, vanishing sums with nonnegative coefficients are sums of p-gons and q-gons; 0/1 coefficients force disjointness) is quoted correctly.

The cyclotomic identity with single-witness failures is empirical, as E says. **Certified.**

---

## 7. Checklist summary
- **Quantifier order:** correct in B (the ORW lemma), C (U-property) and E2. No issues found.
- **ε and exponents:** D counts ε in GF(L₁∩L₂), which is correct. E5 needs n ≥ 2. Q excludes ε throughout. No issues found.
- **Closure misuse:** A(d) is the only real proof gap; it is repaired for chains from Q (Lemma K1). The Bar-Hillel remark in A is wrong. No step uses complement, ∩CF or infinite intersection.
- **Ambiguity classes:** D is careful. "Exactly 2" is correct but unnecessary.
- **Off-by-one:** G Thm 2's balanced shape when 3 | n, and the first-factor constant in A(b). Both are fixed above.
- **n = 1 and single-letter powers:** all the theorems state n ≥ 2 (or n ≥ 3), or are vacuous at n = 1. aⁿ is handled correctly everywhere.
- **Numerics as proof:** C's Lemma B finite step is a genuine exhaustive proof, and I reproduced it. G's even-n shared-yield claim (§7.2) and C's Lemma S are computational only, and both are labelled as such.
- **New error found:** the "c·n ≤ μ(Q_n)" lower bound in G Prop 5 and the REGISTRY is false (§1c).
