# Round 3, Route L: MP = {per(w) > |w|/2}, its relatives MP_c, and the local-witness target

Code and outputs are in
`/tmp/claude-5714/-home-shobhit--claude-spares-spare-fauO4P/6f48459d-5790-4a18-bccc-eabb8efc4544/scratchpad/r3_mp/`:

| file | what it does |
|---|---|
| `lib.py` | prefix function, period, run-slice border formulas |
| `verify_formulas.py` | checks the slice formulas and the (n/4, n/2] reduction (output `out_verify.txt`) |
| `ogden_full.py` | exhaustive string-level Ogden check for Thm A (`out_ogden_full.txt`) |
| `runmodel.py` | run-model checker, used for tightness |
| `runogden.c` | exhaustive run-model Ogden witness search (`mp_search.out`) |
| `cover.c`, `covmid.c` | class-coverage tests (`out_cover.txt`, `out_covmid.txt`) |
| `lmid.py`, `lmid2.py`, `lmid3.py` | Thm B checks (`out_lmid*.txt`) |
| `sqprefix.py` | square-prefix characterization (`out_sqprefix.txt`) |

Notation:
- n = |w|, and per(w) is the minimal period.
- For θ ∈ (0, 1/2], let MP^θ = {w : longest border < θn}. Then MP_c = MP^θ with θ = 1 − 1/c, and MP = MP^{1/2}.
- lp(c) is the local period at the cut c (centered repetitions, truncated at the ends of the word).

## Verdict

1. **Theorem A (new): MP_c is not CF for every 1 < c < 5/4** (θ < 1/5).
   - The proof is an Ogden argument on MP_c ∩ (a⁺b)⁴ that handles every decomposition. It extends J's UB witness by a large "padding" X ≫ p!.
   - It was checked exhaustively at string level (p ≤ 4) and in the run model (p ≤ 5).
   - The bound 1/5 is sharp for this witness family.
   - It does **not** transfer to MP or to Q: 3 of the 4 decomposition classes are killed by *primitive, non-periodic* words that have a long but non-periodic border. That kind of word exists in MP^θ's complement only for θ < 1/2.
2. **Theorem B (new): the "one local witness at the critical point" target is not CF.** Let L_mid = {w : no square centered at the middle cut}.
   - L_mid ⊆ MP.
   - L_mid meets **every** primitive conjugacy class. I prove this from the Critical Factorization Theorem (CFT) and checked it exhaustively for n ≤ 22.
   - **L_mid is not CF.** The Ogden proof is short, with every decomposition handled.
   - The same holds (sketch plus simulation) for any bounded window of cuts around the middle.
   - With a free cut, "∃c: lp(c) > n/2" is *exactly* MP (verified), so the CFT gives no simplification.
3. **MP itself: no proof either way.** The precise obstruction:
   - In every run slice, MP's complement has the same geometry as Q's, plus one boundary half-space. The pieces have interior equalities, codim ≥ (r−1)/2 (Prop 5.1).
   - The only extra pump direction MP offers is a single-run pump of the first run (Prop 5.2). An unmarked co-pump of any interior run neutralizes it.
   - The "free middle" that powers Thm A disappears exactly at θ = 1/2.
   - Exhaustive run-model Ogden searches (r ≤ 6, both slice types, p = 2, 3) find no non-degenerate MP witness.
4. **Constructive side: no CF candidate survived.**
   - Abelian-unbordered certificates (sound, ⊆ UB) and their linear-CF truncations miss classes from n = 16 (n = 6 for the truncations).
   - The pinned local witness (L_mid) is complete but not CF (Thm B).
   - Mirror-pair (single-centre) certificates directly test only periods of one parity.

---

## 1. Structure of MP (all verified by brute force)

**Prop 1.1 (reduction to long periods).** per(w) ≤ n/2 ⇔ w has a period in (n/4, n/2].
*Proof.* If P ≤ n/4 is a period, the largest multiple kP ≤ n/2 is also a period, and kP > n/2 − P ≥ n/4. ∎
Checked for n ≤ 16. So MP = ∀P ∈ (n/4, n/2] ∃i: w_i ≠ w_{i+P}. The universal quantifier ranges over an interval of Θ(n) *long* distances.

**Prop 1.2 (CFT form).** MP = {w : ∃ cut c with lp(c) > n/2}.
- lp(c) ≤ per(w) always, so ⊆ holds.
- The CFT gives a cut with lp = per(w), so ⊇ holds.
- Checked for n ≤ 13.

So the critical cut is an existential witness, but "lp(c) > n/2" is again a ∀ℓ ≤ n/2 statement.

**Prop 1.3 (self-located candidates).** w ∉ MP ⇔ w has a square prefix u² with u primitive and w a prefix of u^ω.
- Fine–Wilf reduces a non-primitive root to its primitive root.
- Checked for n ≤ 18.
- By the Crochemore–Rytter three-squares lemma there are O(log n) primitively rooted square prefixes. The maximum count was 3 for n ≤ 18.
- Contrast with Q: MP must refute O(log n) candidates that the word *itself* locates (they are visible as a prefix). Q must refute ω(n) candidates located *arithmetically* (n/p).

**Prop 1.4 (exact slice formula).** For x ∈ ℕ₊^r and w = a^{x₁}b⋯a^{x_r}b, put y = (x₂,…,x_r). Then w ∉ MP iff one of:
- (∃ d ≤ (r−1)/2) y is d-periodic and x₁ ≤ y_d, or
- r is even and w is a square.

Checked for r ≤ 7 with all x_i ≤ 4: 0 mismatches.

Equivalently, w ∈ MP iff, writing d = per(y) when it is ≤ |y|/2, x₁ > y_d (minus squares). So MP of a word reduces to "sesqui-periodicity" of its run-length sequence over the infinite alphabet ℕ (in unary), plus one boundary comparison. Testing that needs both run-index matching and a-mass comparison, which is I's index-mass obstruction (see §4e).

General border formulas, used everywhere below and checked against KMP on 3905 tuples:
- **(a⁺b)^r.** A border with s b's exists iff x₁ ≤ x_{r−s+1} and x_i = x_{r−s+i} for 2 ≤ i ≤ s. Its length is Σ_{i≤s}(x_i+1).
- **a⁺(ba⁺)^{r−1}.** A border with s b's (1 ≤ s ≤ r−2) exists iff x₁ ≤ x_{r−s}, x_r ≤ x_{s+1}, and x_{1+i} = x_{r−s+i} for 1 ≤ i < s. Its length is x₁ + x_r + s + Σ_{i=2}^{s} x_i. In addition there is the pure-a border a^{min(x₁,x_r)}.

---

## 2. Theorem A: MP_c is not CF for 1 < c < 5/4

Put θ = 1 − 1/c ∈ (0, 1/5) and L = MP^θ ∩ (a⁺b)⁴.

**Theorem A.** L is not CF. Hence MP_c is not CF.

*Proof.* Suppose L is CF with Ogden constant p. Let D = p! and X ≥ X₀ := ⌈(θ(2D+5+p) + p)/(1 − 5θ)⌉. Take

  z = a^{X+1} b a^{X+D} b a^{X+1+D} b a^{X} b,  n = 4X + 2D + 6,

and mark run 1.

**z ∈ L.** Every border starts with a^{X+1}b, so its suffix copy must start in a run of length ≥ X+1, that is run 2 or run 3.
- Starting in run 2 would force x₃ = x₂.
- Starting in run 3 would force x₄ = x₂.

Both fail, so z is unbordered.

Let z = uvwxy satisfy Ogden's conditions.
- **v or x contains b.** Then the number of b's changes, so the pumped word leaves R.
- **Otherwise.** v = a^α lies in run 1 (v must carry a mark; if v = ε then x lies in run 1). If x lies outside run 1, the window forces α ≤ p. Write x = a^γ in run j. If γ is the whole run, i = 0 leaves R.

The kills use two border types:
- the one-block border a^{x₁'}b, which exists iff x₁' ≤ x₄', with length x₁'+1;
- the square.

The cases:
- **(a) j = 1, or v = ε.** Run 1 shrinks by δ ≤ p at i = 0, so x₁' ≤ X = x₄. The border length is X+2−δ ≥ θ(n−δ), because X(1−4θ) ≥ θ(2D+6) + p − 2.
- **(b) j ∈ {2,3}.** At i = 0 we get x₁' = X+1−α ≤ x₄. The border length is X+2−α and n' < n, so the bound from (a) applies.
- **(c) j = 4, α > γ.** At i = 0 we get x₁' = X+1−α ≤ X−γ = x₄'. The same bound applies.
- **(c) j = 4, α < γ.** At i = 2 we get x₁' = X+1+α ≤ X+γ = x₄'. The border length is X+2+α. Since n' = n+α+γ ≤ 5X+2D+5+p, the condition X(1−5θ) ≥ θ(2D+5+p) suffices.
- **(c) j = 4, α = γ.** At i = 1 + D/α we get (a^{X+1+D} b a^{X+D} b)², a square, with border n'/2 ≥ θn'.

Every decomposition is killed. ∎

**Verification.**
- `ogden_full.py` enumerated **every** string factorization uvwxy that satisfies (i) and (ii) under this marking, testing i ∈ {0, 2, …, D+1}. The configurations were:
  - (X, p, θ) = (12, 1, 1/10), (10, 2, 3/20), (10, 3, 3/20), (19, 3, 19/100), (30, 4, 3/20).
  - In the largest case, 2,098,675 decompositions.
  - Result: 0 survivors in all cases.
- Run-model check for p ≤ 5 agrees.

**Sharpness for this family.** Take θ > 1/5 and X large. Then v = one letter of run 1 with x = a^{X−1} in run 4 survives:
- At i = 0 the word is unbordered.
- At i ≥ 2 the only border is one-block, with ratio ≤ (X+3)/(5X+2D+6) < 1/5.
- The run model confirms this: at θ = 21/100 there are 179–1594 survivors for p = 2..5, all of type (1, 1, 4, γ ≈ X).

The bound needs X ≫ D. At p = 5 and θ = 0.19, X = 400 is too small and survivors appear, exactly as the inequality predicts.

**Anatomy, which explains why it does not reach θ = 1/2.**
- Cases (a), (b) and (c) with α ≠ β land on *primitive* words, indeed on words in MP (period ≈ 3n/4), that have a one-block border a^{x₁'}b of length ≥ θn.
- The piece {x₁ ≤ x_r, x₁+1 ≥ θn} of MP^θ's complement is **full-dimensional** in the slice. Its constraints involve only run 1, run r and the total length, so arbitrary unmarked pumps of runs 2 and 3 cannot leave it.
- The price is length. The α = β case needs two runs ≥ X + D (a square target), and the α < γ case needs i = 2 with γ up to X. Hence θ < 1/5.
- For θ = 1/2 this piece is **empty**: x₁ ≤ x_r and x₁+1 ≥ n/2 force r ≤ 2 and a square. See §5.

Related: J's Thm 2 kills "no *short* border" (f ↑ ∞). Theorem A kills "no *long* border" (≥ θn) for θ < 1/5. MP is the remaining endpoint θ = 1/2.

---

## 3. Theorem B: the local-witness target L_mid

Put c = ⌊n/2⌋ and define

  **L_mid = {w ∈ Σ⁺ : there is no ℓ ∈ [1, c] with w[c−ℓ+1..c] = w[c+1..c+ℓ]}**

(no square centered at the middle cut). Membership is O(n): with L = w[..c] and R = w[c+1..], it is prefix_fn(R#L)[−1] = 0. Checked against the naive definition for n ≤ 16.

**(i) L_mid ⊆ MP.** If P ≤ n/2 is a period, then P ≤ c and P ≤ n−c, and w[c−P+1..c] = w[c+1..c+P]. Brute force for n ≤ 16 finds 0 exceptions.

**(ii) L_mid meets every primitive class.** Let w be primitive of length n ≥ 2. Then per(w³) = n by Fine–Wilf.
- By the CFT, w³ has a cut c₀ < n with lp(c₀) = n, counting truncated repetitions.
- Consider the cut c₀ + n. A centered repetition there of length ℓ < n fits inside w³. By n-periodicity it restricts to a (truncated) repetition at c₀, which would give lp(c₀) ≤ ℓ < n, a contradiction.
- So c₀ + n has no centered square of half-length ≤ n/2.
- The conjugate w' = w³[c₀+n−c+1 .. c₀+n+n−c] has this cut as its middle, so w' ∈ L_mid. ∎

Exhaustive check (`covmid.c`): every primitive class is hit for n ≤ 22 (190,557 classes at n = 22). So **L_mid CF ⇒ Q CF.** This is exactly the "single local witness at a critical point" target from the task.

**(iii) Theorem B: L_mid is not CF.**

**Lemma M1 (holds for any z, no marks needed).** Let z = uvwxy with vx ≠ ε. Suppose |v| ≠ |x|, or |v| = |x| and v, x lie on the same side of the middle cut (|uvwx| ≤ c or |u| ≥ c). Then z_i = uvⁱwxⁱy has a square centered at its middle for i = n+3.

*Proof.* Let n_i = n + (i−1)(|v|+|x|), c_i = ⌊n_i/2⌋ and A = |u|. The block vⁱ occupies [A, A+i|v|) and is |v|-periodic. The block xⁱ starts at B_i = A+i|v|+|w| and is |x|-periodic. It suffices that [c_i−q, c_i+q) lies inside a q-periodic block, which gives a centered square of half-length q.
- **|v| > |x|.** The conditions A+|v| ≤ c_i ≤ A+(i−1)|v| reduce to (i−1)|v| ≥ 2A+2|v|+1−n (whose right side is ≤ n+1) and n−2A ≤ (i−1)(|v|−|x|).
- **|x| > |v|.** The conditions B_i+|x| ≤ c_i ≤ B_i+(i−1)|x| reduce to (i−1)(|x|−|v|) ≥ 2(A+|v|+|w|+|x|)+1−n (right side ≤ n+1) and n ≤ 2A+2|w|+(i+1)|v|+(i−1)|x|.
- **|v| = |x| = q, both left.** Here c_i = c+(i−1)q, and the conditions are A+|w|+2q ≤ c and c ≤ A+iq+|w|.
- **|v| = |x| = q, both right.** The conditions are c ≤ A and A−c ≤ (i−2)q.

All of these hold for i = n+3. ∎
Random test: 14,412 cases, 0 counterexamples (`lmid2.py`).

**Proof of Thm B.** Let p be the Ogden constant and N = max(p, 2). Take

  z = b^{N−1} a^N | b^N a^{N−1},  n = 4N−2,  c = 2N−1,

and mark the 2N letters a^N b^N.

**z ∈ L_mid.**
- For ℓ ≤ N, a^ℓ ≠ b^ℓ.
- For ℓ > N, the right prefix starts with b^N, but the left half contains no b^N.

**Decompositions.** By M1, only the case |v| = |x| = q where vwx contains both letters next to the cut remains.
- Any interval that contains those two letters and leaves the zone has ≥ N+1 > p marks. So vwx ⊆ a^N b^N and 2q ≤ p, which gives q ≤ N/2 ≤ N−1.
- At i = 0 the word is b^{N−1} a^{N−α'} b^{N−β'} a^{N−1} with α'+β' = 2q, and its middle is c−q.
  - If α' = q, the middle is the a|b boundary, and b^{N−q}a^{N−q} | b^{N−q}a^{N−q} is a centered square.
  - If α' ≠ q, the middle lies |α'−q| ≤ q ≤ N−1 letters inside a run, which gives a centered square of half-length 1.

Every decomposition is killed. ∎

Exhaustive Ogden simulation:
- The bare witness above, with N ∈ {p, p+1} and p ≤ 4: 0 survivors.
- Padded witnesses b^{N−1} S a^N b^N S a^{N−1} with S ∈ {ab, abab, aab} and p ≤ 4: 0 survivors.

**Cor B' (bounded window; proof sketch).** For fixed k, let L_mid^{(k)} = {w : some cut within distance k of c has lp > c}.
- It is sound: lp ≤ per.
- It contains L_mid, so it meets every class.
- It is not CF. M1 is used with margins q+k. At i = 0 every cut near the middle of the pumped word has lp ≤ n'/2.

Simulated for k = 1, 2 and p ≤ 4 with N = p+k+1: 0 survivors.

**Dichotomy (parallel to J's Thm 3).**

| where the local witness may sit | language | status |
|---|---|---|
| fixed position, or a bounded window around it | L_mid, L_mid^{(k)} | not CF |
| any cut | MP, by Prop 1.2 | open |

The CFT gives no leverage beyond MP itself.

**Why Thm B does not transfer.** Every kill lands on a word with a centered square at its middle. That is a set of density ≥ 1/2, whose members are mostly primitive with period > n/2. So the kills are in MP, not in its complement. The proof exploits L_mid's **thick complement**: moving the middle into a pumped periodic block always creates a centered square. Neither MP nor Q has such a complement.

---

## 4. Constructive attempts (Task 1) and their failure points

**a. One local witness.** This is resolved negatively by Thm B and Cor B'. To be useful, a CFG must guess the critical cut freely, and then it must still certify ∀ℓ ∈ (n/4, n/2]: w[c−ℓ..c) ≠ w[c..c+ℓ) (with truncation).
- For different ℓ these are *translation* comparisons. Pairs (c−ℓ+i, c+i) with the same ℓ cross one another, and families with different ℓ cross as well.
- For any single ℓ the existential mismatch is CF, by the non-square trick x c u c' y with |u| tied to |x|+|y|. The universal over ℓ is the whole difficulty, exactly as for Q's divisor universal.

**b. Single-centre mirror certificates (linear/one-turn).** Pair i = (i, n+1−i) compares two letters at distance n+1−2i. Such a certificate can therefore refute a period P *directly* only when P ≡ n+1 (mod 2). Periods of the other parity need indirect, counting-type evidence.

**c. Counting (abelian) certificates.** Let G(m) = |pref_m|_a − |suf_m|_a.
- G(m) ≠ 0 for all m ≤ n/2 ⇔ w has no abelian border. Call this set AB.
- AB ⊆ UB ⊆ MP.
- G is a ±1 walk over the mirror pairs, outside-in.
- Bounding the walk height by K gives a **linear CF** language AB_K.

Coverage of primitive classes (`cover.c`):

| n | classes | missed by AB | AB₁ | AB₂ | AB₃ | AB₄ |
|---|---|---|---|---|---|---|
| 12 | 335 | 0 | 279 | 74 | 20 | 3 |
| 14 | 1161 | 0 | 1045 | 319 | 89 | 13 |
| 16 | 4080 | **6** | 3832 | 1448 | 384 | 72 |

AB itself fails at n = 16. The first misses are the classes of bbababaabbaabbaa, bbababaabbaababa and bbababaabababbaa, all of whose rotations are abelian-bordered. The CF truncations fail much earlier.

Unbounded AB is the fold of a one-counter language: it needs the mirror stack *and* a counter, and I expect it is not CF. It is dead anyway as a transversal.

Remark: a *linear* CF transversal of Q is not excluded by Horváth's theorem (Q not linear), because cyc(L) need not be linear. The AB_K are the natural linear candidates, and they fail.

**d. Unique-feature certificates** (a unique factor lying in one half implies MP). These are of the one-vs-many type (E, Lemma 3).

**e. Run-length recursion (Prop 1.4).** In the slice, MP becomes sesquiperiodicity of y over ℕ. Any certificate must compare run masses at a run-distance d for every d ≤ |y|/2. This is I's index-mass conflict (block counts and masses on one stack), now for *all* d rather than for divisors.

**Testing standard.** No CF candidate reached n = 16, so the n ≥ 22, scaled and near-square tests were never reached. L_mid passes n ≤ 22, but that is because it is complete by theorem; it is not CF.

---

## 5. MP itself: the precise negative-side obstruction

**Prop 5.1 (complement geometry).** On (a⁺b)^r, MP's complement is ⋃_{d≤(r−1)/2} Π_d ∪ S, where
- Π_d = {y d-periodic} ∩ {x₁ ≤ x_{d+1}}, of codim r−1−d ≥ (r−1)/2, whose only inequality is on the *first* run;
- S is the set of squares.

On a⁺(ba⁺)^{r−1} the last run gets a second boundary inequality. There are also near-square cones {max(x₁,x_r) ≤ x_k ≤ x₁+x_r}, whose interior equalities are the same as above. Interior runs are always tied by equality to a d-partner.

**Prop 5.2 (direction lemma for MP).** Take a pump direction δ = αe_m + γe_j. Then each piece meets the line z + ℤδ in at most one point, except for:
- (a) δ = δe₁, a single-run pump of the first run, which can meet a Π_d in a ray (half-space); and
- (b) "partner pumps": α = γ on a size-2 orbit of some Π_d, or of S.

*Proof.* The direction must lie in the hull {y d-periodic} × ℝe₁. The y-part of δ is supported on ≤ 2 runs, while every d-orbit has size ≥ 2 because d ≤ (r−1)/2. ∎

For Q, J's Lemma 5.1 gives the same picture without (a). **So, slice by slice, MP = Q + one boundary ray.**
- The ray is useless against an Ogden adversary. If run 1 is marked, the adversary pairs v ⊆ run 1 with an *unmarked* x in any interior run j with arbitrary γ. Every piece then constrains x_j by an equality, so it kills at most one exponent i per piece. Factorial tricks only help for bounded γ.
- If interior runs are marked instead, we are in J's Thm 5 regime (Q-type barrier).
- Thm A escapes only because MP^θ with θ < 1/2 has a piece with *no* interior equalities (the "free middle"). At θ = 1/2 every position of a complement word is constrained by periodicity.

**Searches** (`runogden.c`). These are exhaustive over run vectors and over all whole-run markings, with marked runs > p, and every run-model Ogden option tested for i ≤ Imax. Results for MP (θ = 1/2):

| slice type | r | runs ≤ | p | witnesses |
|---|---|---|---|---|
| (a⁺b)^r | 2..4 | 14 | 2 | 0 |
| (a⁺b)^r | 4 | 30 | 3 | 0 |
| (a⁺b)^r | 5 | 12 | 3 | 0 |
| (a⁺b)^r | 5 | 14 | 2 | 0 |
| (a⁺b)^r | 6 | 7 | 2 | 0 |
| a⁺(ba⁺)^{r−1} | 4 | 30 | 3 | 0 |
| a⁺(ba⁺)^{r−1} | 5 | 12 | 3 | 0 |
| a⁺(ba⁺)^{r−1} | 6 | 7 | 2 | 0 |
| a⁺(ba⁺)^{r−1} | 3 | 14 | 2 | 1, degenerate: (1,3,1) |
| a⁺(ba⁺)^{r−1} | 5 | 14 | 2 | 1, degenerate: (1,1,3,1,1) |

The two degenerate p = 2 hits disappear at p = 3, 4. Together with J's 26,000-candidate search, this suggests (not proved) that MP's slices satisfy Ogden's conclusion, as Q's do.

**Intermediate θ.** For 1/5 ≤ θ < 1/2, small-p searches do find witnesses: p = 3 gives hits up to θ = 9/20, e.g. (X, 1, X+3, 1) with runs 1 and 3 marked. They are **artifacts**: effectively two-variable slices whose complement is a half-plane with normal ((1−θ), −θ). Once p exceeds the denominator of θ/(1−θ), a pump parallel to the boundary exists and survives.

**Open (conjecture):** MP_c is not CF for every c < 2. A gadget for the α = β case cheaper than the square target would be needed.

---

## 6. Transfer analysis (Task 2)

- **Thm A → Q: no.** Three classes are killed by primitive words that have a long non-periodic border. Q's complement (exact powers) has no full-dimensional piece and no half-spaces (J §3). Only α = β lands in Q's complement (a square).
- **Thm A → MP: no.** The same kill words have period ≈ 3n/4 > n/2, so they lie in MP. At θ = 1/2 the one-block-border piece is empty (§2, anatomy).
- **Thm B → MP or Q: no.** The kills use L_mid's thick complement (a centered square at the middle). MP's complement {u^k u' : k ≥ 2} is thin (≤ Σ_{P≤n/2} 2^P), as is Q's.
- **Difference between MP's and Q's complements.** MP's complement also contains sesquipowers. These contribute exactly the boundary rays of Prop 5.2. Those rays are not enough for a J-type proof, and they do not exist for Q.

---

## 7. Precise obstructions and open lemmas

1. **Negative, MP.** One needs a witness family in which every unmarked interior co-pump is killed. By Prop 5.2 each complement piece kills at most one exponent for such a pump, so this requires the same "near-power along every admissible direction" rigidity as Q (H's Gap G / J's barrier). It is of theorem strength. An analogue of J's Thm 5 ("MP ∩ (a⁺b)^r satisfies Ogden for p ≥ p₀(r)") is supported by the searches but **not proved**.
2. **Negative, MP_c for c ∈ [5/4, 2).** Open. The missing piece is a gadget that resolves the ratio-1:1 pump without two extra runs of length ≈ X. This is probably *not* of theorem strength, but I did not find it.
3. **Affirmative.** One needs a CF certificate for "lp(c) > n/2 at a *guessed* cut". It cannot be pinned to the middle or to any bounded window (Thm B, Cor B'). Mirror walks fail (§4b–c). This is equivalent to handling ∀ℓ ∈ (n/4, n/2] with crossing translation comparisons, the same structural core as Q's universal over divisors. It is of theorem strength.

## 8. New artifacts

- Thm A: MP_c is not CF for 1 < c < 5/4, sharp for its witness family.
- Thm B: L_mid is a sound transversal (via the CFT) but not CF. Cor B': bounded windows are not CF either.
- Props 1.1–1.4: structure of MP, including the exact slice formula and the run-length recursion.
- Props 5.1–5.2: MP's slice geometry is Q's plus one boundary ray.
- Data: AB is not a transversal (fails at n = 16); search tables for MP and MP^θ.
