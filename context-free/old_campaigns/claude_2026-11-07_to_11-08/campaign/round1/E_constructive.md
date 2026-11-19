# Round 1, Route E: affirmative constructions (CFG/PDA for Q), plus the obstructions found

**Verdict.** I found no CFG/PDA with L = Q_{a,b}. Every construction I tried is either sound but incomplete, or complete but not CF. This report records the exact reformulation I used, each candidate with exhaustive test data (n ≤ 20; n ≤ 16 for the slow ones), and the specific obstruction that stops each one. Several obstructions are proved lemmas. They are lemmas about restricted *certificate models*, not about all PDAs, so none of them settles the problem.

Code and raw output are in
`/tmp/claude-5714/-home-shobhit--claude-spares-spare-fauO4P/6f48459d-5790-4a18-bccc-eabb8efc4544/scratchpad/constructive/`
(`lib.py`, `candidates.py`, `witness.py`, `bounded6.py`, `union.py`, `cyc_vs_sw.py`, `out/*.txt`).
The tests enumerate primitive classes with the FKM algorithm (Lyndon counts checked against A001037). Soundness is tested on every non-primitive word of each length.

---

## 0. Exact reformulation (the "transversal" form)

**Lemma 0.** Q is CF ⇔ there is a CF language P with P ⊆ Q such that P meets every primitive conjugacy class.
*Proof.* (⇐) Q is closed under rotation, so cyc(P) ⊆ Q. P meets every class, so cyc(P) = Q. Cyclic shift preserves CF. (⇒) Take P = Q. ∎

**Corollary.** For any regular R that meets every primitive class (for example "starts with a, ends with b", plus the two letters), Q is CF ⇔ Q ∩ R is CF.

So the reformulation loses nothing and gains nothing in principle. It only frees us to pick convenient representatives. Every attempt below is a choice of P.

---

## 1. Candidate transversals P: exhaustive data

"missed" counts primitive classes with no rotation in P. All candidates are **sound**: 0 non-primitive words were accepted in every case.

| P | CF? | missed at n=16 / 18 / 20 | first misses |
|---|---|---|---|
| Lyndon words | **no** (Berstel–Boasson, from memory) | 0 / – / – (n ≤ 16) | – |
| Unbordered words | open to me; the complement {xyx} is a copy language | 0 (n ≤ 16) | – |
| unique longest run (a or b) | **no** (Lemma 3) | 267 / 979 / 3602 (≈7%, stable) | aaabaaababab |
| unique run length | **no** (Lemma 3) | 164 / 521 / 1845 | aabaabababab |
| gcd(\|w\|_a,\|w\|_b)=1 | no (not semilinear) | 2032 / 10042 / 27713 | a^{n-2}bb |
| gcd of cyclic m-gram counts = 1, m=1..4 (upper bound for *every* Bezout certificate on m-grams) | – | m=4: 80 / 270 / 728 | a^K b a^{K'} b with K+K' even |
| unique cyclic factor of length ≤ c (regular), c=2,3,4,6 | yes | c=6: 16 / 40 / 86 | a^K b a^{K'} b |
| walk / cycle-lemma, weights (r,−s), r,s ≤ 5 (one counter) | yes | 197 / 1147 / 6359 | a^{n-1}b (Parikh ratio out of range) |
| same, weights (B,−A) taken from the word | no | 455 / 2070 / 6565 | – |
| single witness position (one i that sees a mismatch for every prime) | (would be the "one centre" scheme) | 0 / 24 / 6; n=12: 2 | aaabbaabaabb |
| **union of explicit CF families** (Bezout \|rA−sB\|=1 with r,s ≤ 4; walks; ≤3 b's or ≤3 a's; unique factor ≤ 5; alternating b-gap sum ±1) | **yes, and sound** | 8 / 60 / 102; n=14: 4, n=17: 2, n=19: 2 | aaabaaabaabaab, aabaabaabaababaabab |

In the union, the uncovered fraction is small (≤ 0.5%) but never reaches zero. It is nonzero even at prime lengths 17 and 19, where Q ∩ Σ^n is just the non-constant words. This is the semilinearity obstruction of Lemma 2 seen in the data: the CF families cannot use "n is prime".

---

## 2. Proved obstructions to the natural certificate schemes

### Lemma 1 (each mismatch pair refutes at most one prime; witness positions can be forced to be numerous)
Let H_p = ⟨n/p⟩ ≤ Z_n. A mismatch w[i] ≠ w[i+d] refutes invariance under the shift n/p iff n/gcd(d,n) = p. So **every mismatch pair refutes at most one prime**, and any pair-based certificate needs ≥ ω(n) pairs, which is unbounded.

Stronger: let C_p be the set of positions lying in a non-constant H_p-coset, and let h(w) be the minimum size of a set of positions meeting every C_p. Then **h(w) = ω(n) is attainable for every set of primes.**
*Construction.* Take n = g·∏p with g ≥ k = #primes. Give residue class r_p (mod g) the 0/1 sequence (0^{p-1}1)^{R/p}, where R = ∏p, and make every other class constant. Shifts n/q are multiples of g, so they stay inside residue classes. Class r_p has minimal period p, so it is invariant under all n/q with q ≠ p and not under n/p. Hence the C_p are pairwise disjoint and nonempty.
Verified: n=12 (word aabaabbaaabb, h=2), n=90 (h=3), n=840 (h=4). Exhaustive distribution: h=2 occurs for 2 classes at n=12, 24 at n=18, 6 at n=20 (`out/witness.txt`).
⇒ "One guessed position compared against all primes" (a star certificate) fails already at n=12.

### Lemma 2 (semilinearity kills explicitly marked prime-refuting chords), rigorous
Let M be CF, consisting of words with two marked positions at distance d, such that in every word of M the marked pair is a mismatch with n/gcd(d,n) prime. Then the set S = {(d,n)} is semilinear (Parikh), and **only finitely many primes occur as n/gcd(d,n).**
*Proof.* Take a linear component b + Σt_i v_i of S. Since d < n, every nonzero period has v_n > 0. Look along a ray (d0+tv_d, n0+tv_n) and put K = v_n d0 − v_d n0.
- If K ≠ 0: gcd(d,n) | K, so n = g·p with g | K. Pick a prime q ∤ v_n·K and t with q² | n. This contradicts n = g·p.
- So K = 0, and the whole component lies on one line d/n = c. Then n/gcd(d,n) = denominator(c), a single fixed prime.
- Bounded components contribute finitely many points. ∎

**Consequence.** Any construction that, for each prime p | n, exhibits (in a way a finite-state relabelling of derivations can mark) a mismatch at a distance tied to n/p certifies only finitely many primes. It therefore misses all long words of prime length. Any grammar for Q must accept long prime-length words "for reasons" other than an exposed refuting chord. Restricted model: this is *not* a theorem about all PDAs.

### Lemma 3 (one-versus-many comparisons are not CF)
L_1 = {a^k b a^i b a^j : i ≤ k, j ≤ k} is not CF: pump a^N b a^N b a^N, where every decomposition fails. L_2 = {a^k b a^i b a^j : k ≠ i, k ≠ j} is not CF: Ogden with block 1 marked, on a^N b a^{N+N!} b a^{N+N!}, using the factorial trick.
These are the regular slices of "unique longest a-run at the front" and "unique run length". So those transversals are not CF (their cyclic closures are proper subsets of Q anyway). Lyndon and unbordered words have the same flavour: a universal comparison of one prefix quantity against unboundedly many others.

### Lemma 4 (binary nested chains degenerate)
"All distances" form: w is primitive ⇔ for every d ∈ [1, n−1] there is a cyclic mismatch at distance d. There is no divisibility here, so this evades Lemma 2.
The CF-natural way to cover all d is a nested chain of mismatch chords (l,r) → (l+1,r) or (l,r−1), which a linear grammar X_{d,c} → d′X_{d′,c} | X_{d,c′}c′ can generate.
**Over {a,b} this forces the left endpoint to stay inside one run and the right endpoint inside another.** If w[l] ≠ w[r], then w[l+1] ≠ w[r] ⇔ w[l+1] = w[l]. So only a^i b^j-type words admit a full chain.
Any CF all-distance scheme therefore needs non-chain (crossing or counted) chord families, and crossing families are exactly what CF cannot verify.

### Lemma 5 (cyclotomic barrier for every "linear functional ≠ 0" certificate), rigorous
Let P_n = {w ∈ Σ^n : L_n(w) ≠ 0} with L_n linear on Q^n. This covers every one-counter "weighted count ≠ 0" certificate with fixed weights, and every single comparison of interval sums.
If P_n is sound, L_n vanishes on all non-primitive 0/1 words. These span A_{p1}+…+A_{pk} (A_p = (n/p)-periodic vectors). So **P_n misses every primitive w in A_{p1}+…+A_{pk}**, i.e. every w with w(ζ_n) = 0 for a primitive n-th root of unity (Φ_n | w(x)).
- For n = p^a q^b these are, by de Bruijn's theorem on vanishing sums of roots of unity, the superpositions "union of H_p-cosets ⊔ union of H_q-cosets". Example: aabaabbaaabb, with b-positions {5,11} ⊔ {2,6,10}.
- **Empirical identity:** for n = 12, 18, 20, 24 the cyclotomic-hard classes coincide *exactly* with the single-witness failures of Lemma 1 (2, 24, 6, 236 classes; `out/cyc_vs_sw.txt`). I have not proved the identity in general.
- These words are often caught by *arithmetic* certificates such as Bezout on Parikh counts (5 b's out of 12 gives gcd 1). Arithmetic certificates are not of the "≠ 0" type, but only finitely many Bezout relations are CF.

### Lemma 6 (finite families of counting certificates miss a 2-parameter family)
For a^K b a^{K'} b with K ≠ K', K+K' even and K, K' ≥ m, all cyclic m-gram counts are even. So every Bezout certificate with factors of length ≤ m fails, and any fixed finite-state weight takes value ±1 only on finitely many lines in (K,K'). These classes need a genuine comparison (K ≠ K'). Combined with Lemma 3, comparison certificates can only be nested and pairwise compatible.

---

## 3. Bounded b-count: the first case where two primes must be combined

Q ∩ (a*b)^c is a bounded language. Its CF-ness is decidable via Ginsburg–Spanier: is the gap-tuple set E_c (cyclic non-periodic tuples in N^c) a finite union of stratified linear sets? For c a prime power there is a single prime, so it is CF. **c = 6 is the first two-prime case.** I analysed it as a test of combining primes.

- **Single interval comparisons refuting both primes exist**, for example g0+g1 ≠ g3+g4: window length 2 kills the period-2 (cube) case, and offset 3 kills the period-3 (square) case. Each is one nested length comparison, hence CF.
- **Exact computation** (`bounded6.py`, union of subspaces over all rotations): every non-crossing comparison template fails exactly on the 4-dimensional subspace A+B, with A = 3-periodic and B = 2-periodic. No compatible pair of comparisons exists for c=6: every diameter chord crosses or shares an endpoint with every distance-2 chord. 420 primitive tuples in [0,5]^6 are left uncovered, all in A+B. This is Lemma 5 in the bounded setting.
- **Hard family:** g = (x+s, y, z+s, x, y+s, z) with s ≠ 0 and not x=y=z, with s and x−y, y−z ≡ 0 modulo every modulus the grammar uses, so parity and mod tricks fail. Exact invariants are forced: B-avoidance cannot come from an exact or modular invariant on this family (proved above in my notes: such an invariant would have to vanish on A+B). It must come from a cone inequality.
- **But a cone-inequality cover exists locally.** L = b + N{e03, (0,1,2,0,0,0), (0,1,3,0,0,0), (0,0,0,0,1,2), (0,0,0,0,1,3)} is stratified (non-crossing) and avoids A (g0−g3 = s is exact). It avoids B because Θ = g0−2g1+g2+g3−2g4+g5 ∈ B^⊥ is ≥ 0 on all generators and > 0 at b. It contains the 3-parameter subfamily 2y < z < 3y. Near-diagonal regions (y ≈ z) are handled by window forms such as g0+g1−g2−g3.
- **Status:** I found no obstruction, and expect E_6 to be stratifiable, consistent with PROBLEM.md ("bounded intersections look CF"). I did **not** complete a full cover or a proof. For a negative proof this is the place to look: the E_6 stratification question is finite and decidable, and A+B is its only hard locus.

---

## 4. Where an affirmative construction would have to live (synthesis)

A CFG for Q would need, for every primitive class, a representative certified by a mechanism that:
1. does not expose a prime-refuting chord (Lemma 2), including at prime lengths;
2. is not a single linear "≠ 0" functional (Lemma 5: fails on superposition words);
3. is not a bounded set of counting / Bezout relations (Lemma 6);
4. is not a one-against-many comparison (Lemma 3) or a binary nested chain (Lemma 4);
5. must still handle superposition words of length p^a q^b r^c… with ≥ ω(n) disjoint witness sets (Lemma 1), with the number of primes unbounded.

The only mechanisms CF offers beyond these are stratified nested comparisons with cone inequalities (§3). They work for a *fixed* number of blocks, but the cover depends on the block count c. The missing ingredient is a **uniform** (c-independent) way to combine refutations of unboundedly many primes using non-crossing comparisons. I found no candidate for it. I believe it is of theorem strength in either direction.

**Most useful leads for other routes:**
- **(negative)** The superposition / cyclotomic words (Φ_n | w(x), w primitive). They are exactly where every "single counter" and "single witness" scheme fails, and they are explicit and plentiful. A pumping argument should aim pumped words at A_p + A_q structure.
- **(bounded test)** Decide stratifiability of E_6, then of E_30 (three primes). Whether there is a uniform family of stratified covers as c grows is the precise affirmative question.
