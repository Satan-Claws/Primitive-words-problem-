# audit3: adversarial audit of cl1 (CL2 part), density4, dense, poles, thue, analytic (L1)

**No proof of either resolution is claimed or found.** I re-derived every audited proof line by line and
re-checked each one with independent code: `infinite-ambiguity/claude_round4-5_2026-11-18/scripts/audit3/checks.py` (one core, about 1 min).
I wrote this script myself and did not reuse any of the authors' scripts.

## Verdict table

| Claim | Verdict |
|---|---|
| cl1 Thm 3 (L(c0) CF, ⊇ F(c0), ⊆ Q) | CONFIRMED |
| cl1 F_2 members primitive | CONFIRMED |
| cl1 Thm 4 (F_2 escapes 𝓡) | CONFIRMED (a weak, restricted-class statement, as the author says) |
| cl1 Parikh claim (aaabb)^3 | CONFIRMED |
| density4 Thm P, Lemma AC | CONFIRMED |
| density4 Prop C | CONFIRMED |
| dense W soundness | CONFIRMED (cosmetic nit: ε) |
| dense W positive density | CONFIRMED |
| dense Thm P^R | CONFIRMED |
| poles Lemma 1 (incl. McMillan step) | CONFIRMED |
| poles Lemma 2 | CONFIRMED |
| poles Lemma 3 | CONFIRMED |
| thue L-UC, L-UF, L-PS, exact decision procedure | CONFIRMED |
| thue L-μ | statement TRUE; the written proof has a GAP at e = 2 (repaired below) |
| analytic Thm 3.2 (L1 count 2^{n−1} − d(n), non-algebraic) | CONFIRMED |

## 1. cl1, section CL2

### Theorem 3: CONFIRMED

**Membership.**
- R(c^k)_i = c[(K−i) mod ℓ] = c[(−i) mod ℓ]. This step uses ℓ | K.
- The m·1 part cancels.
- e_1 − Re_1 = e_1 − e_K.
- T_{K+1−i} = −T_i holds identically. For K odd, T at the middle index is 0, because 2i − 1 = K ≡ 0 (mod ℓ).
  So the pair-by-pair linear grammar is consistent.

**Shift argument.**
- (σ_ℓ e_j) = e_{j−ℓ}, so E = e_1 − e_K − e_{K+1−ℓ} + e_{K−ℓ}. This matches the report.
- The four indices are distinct when K ≥ 2ℓ ≥ 4. The tightest case is K = 2ℓ, where the indices are 1, ℓ, ℓ+1, 2ℓ,
  still distinct; for ℓ = 2, K = 4 they are 1, 2, 3, 4. So no cancellation can occur.
- Rσ_d = σ_{−d}R was checked coordinatewise. Hence D, and therefore E, is σ_d-invariant.
- The +1-set {1, K−ℓ} is a single orbit of size 2, so d = K/2.
- From that orbit: −ℓ−1 ≡ K/2. From the −1-set {K, K+1−ℓ}: 1−ℓ ≡ K/2.
- Subtracting gives 2 ≡ 0 (mod K), which is impossible for K ≥ 4.

**Fact B and conjugates.**
- Fact B is valid: the root of a word in (a*b)^+ ends in b.
- Every conjugate that ends in b is cut at a block boundary, so its block vector is a rotation of x.

**COMPUTER-CHECKED (independent):**
- 9 bases c0, including (5,0), (0,7,2) and (3,3,0,1): every word of L(c0) of length ≤ 20 is primitive.
- 27,000 random large members built from x − Rx = T (K up to 30) are all primitive.
- 20,000 random words a·(c)^k, with arbitrary c of length 2–5 and k ≥ 2, are all primitive. This also covers F_2.
- The family F(c0) lies in L(c0).

### Theorem 4: CONFIRMED

- Conjugates that land in (a*b)^+ are block rotations.
- Rotation followed by R acts on Z_K as i ↦ s − i. With 3 | K it fixes one residue class mod 3 and swaps the
  other two.
- The two swapped classes carry two distinct values among p, q, 1, so every entry of x′ − Rx′ in those classes has
  absolute value ≥ (gap) − 1 > B.
- The theorem is only about the explicitly bounded class 𝓡. It says nothing about general CFLs.

### Parikh claim: CONFIRMED

a(aab·ab·ab)^2 = aaabababaababab has ψ = (9,6), and so does (aaabb)^3.

## 2. density4 and dense

### Theorem P step (i): CONFIRMED

- ZΛ + qΛ_E = Λ_E holds, because the index divides gcd(I, q^e) = 1.
- Σp_i has full support, because the p_i are nonnegative and their span contains the all-ones vector.
- Cyclic Euler words have V_k(s^q) = qV_k(s), even when |s| < k.

### Theorem P step (ii): CONFIRMED

- The degenerate case gives p_i = 0, so M is a single point.

### Lemma AC: CONFIRMED

- The Cauchy step is correct: g(L·L_0) = L_0 g(L) = L g(L_0).
- λ_u is independent of u, because f depends only on the edge multiset.
- In the swap step, k-grams cannot straddle both ends of a block once m ≥ k. If the switch pair is shorter, extend
  both words by the same suffix.
- Binomial anti-concentration and Chernoff then finish the proof.

### Prop C: CONFIRMED

It is trivial given closure of CFLs under Cyc.

### W soundness: CONFIRMED

- The window (i, i + ⌊n/2⌋] contains i + d for every proper period d ≤ n/2.
- In each sign case, e = D/p has the sign that contradicts the corresponding window condition.
- Nit: read literally, "∃ i" over an empty window puts ε in W. Restrict W to Σ^+.

COMPUTER-CHECKED: W has no proper power for n ≤ 16. Its density at n = 12..16 is 0.78, 0.84, 0.71, 0.76, 0.77.

### W positive density: CONFIRMED

- If i ≤ n/2, then i + ⌊n/2⌋ ≤ n, so the window stays inside [0, n].
- The limit event has a null boundary, so the Donsker limit applies.

### Theorem P^R: CONFIRMED

- The insertion of (uρu)^m keeps the DFA state, since u's action e is idempotent and the action of h is e.
- The count change lies in mΛ_E ⊆ ZΛ_M once I | m.
- Write qV(s) − c = q(V(s) − c) + (q−1)c. Since c need not lie in the cone, V(s) − c must be chosen at depth > |c|
  inside it. λ large gives this.
- The congruence holds because (q−1)V(s) ∈ IΛ_E.
- The finale is the standard affine-semigroup "deep points" lemma.

## 3. poles

### Lemma 1: CONFIRMED

- The code factorisation is unique, so the words x^k are pairwise distinct.
- The tail of the Lambert sum converges uniformly.
- McMillan gives Σ2^{−|x|} ≤ 1. So X is absolutely convergent and bounded on |z| ≤ 1/2, and every pole has modulus
  in (1/2, 1).
- Poles of X are not poles of X⁺ (X/(1−X) tends to −1 there), but they are covered by the k = 1 term, i.e. by Π(X)
  with j = 1.

### Lemma 2: CONFIRMED

- k is determined by the first b.
- w₀^r = u^k forces k | r.
- The divisibility set is Presburger-definable only if the primes are ultimately periodic, which they are not.

### Lemma 3: CONFIRMED

- The characterisation was checked for n ≤ 16.
- The series S(z) = Σ_t E₁(z^t) was checked coefficientwise for n ≤ 16.

## 4. thue

### L-UC and L-UF: CONFIRMED

The rotation by |t| has all orbits of size e.

### L-PS and the decision procedure: CONFIRMED

- Both directions hold, including the converse: a parse to a position pos with pos ≡ −n (mod P) and pos ≥ 2P−n
  gives σr = t^e with e ≥ 2.
- The prose speaks of a flag, but `full_escape` actually stores the exact position below 2P−n and the residue
  above it, so the procedure is exact.
- COMPUTER-CHECKED: random brute force against the case split.

### L-μ: GAP in the proof (the statement is true)

**Failing inference.** "|t| odd ⇒ e even ⇒ μ(x) = (t²)^{e/2}". When e = 2 this is exponent 1, which is not a
proper power. The rest of the argument then yields only x = y¹, so there is no contradiction.

**Repair.** Suppose μ(x) = tt with N = |t| odd. Write μ(x) = y_0 y_1 ⋯ y_{2N−1}.
- The μ-pairs force y_{2i} ≠ y_{2i+1}.
- The period N, together with 2·(1..N) covering Z_N because N is odd, gives y_r ≠ y_{r+1} for every r ∈ Z_N.
- That would be a proper 2-colouring of an odd cycle, which is impossible (for N = 1 it reads y_0 ≠ y_0).

**COMPUTER-CHECKED.** No μ(x) = tt with |t| odd exists for |x| ≤ 14, and μ(x) is primitive exactly when x is,
for |x| ≤ 14.

## 5. analytic, Theorem 3.2: CONFIRMED

- Words ending in b number 2^{n−1}, and their factorisation into blocks is unique.
- The complement in (a*b)^+ is exactly the constant-block words (a^{e−1}b)^{n/e}, one for each e | n.
- Linearity: L1 = R·{a^i b a^j b : i ≠ j}·R with R regular. The middle language comes from S → Tb, T → aTa | a⁺b | ba⁺.
- Non-algebraicity has two routes:
  - the radial blow-up (1/k)(1−r)^{−1} log(1/(1−r)) at every root of unity;
  - Pólya–Carlson: an integer series with radius 1 is rational or has a natural boundary, and d(n) is not a
    quasi-polynomial.
- COMPUTER-CHECKED for n ≤ 20.

## Registry entry
1. **Aim:** break the listed claims.
2. **Proved:** all audited claims are correct as statements. One proof gap was found and repaired (L-μ, e = 2).
3. **Missing step:** none for the audited lemmas. None of them is a proof of either resolution.
4. **Counterexamples:** none to any claim. The ε-in-W nit is cosmetic.
5. **Strength:** not applicable.
6. **Reopen:** not applicable.
