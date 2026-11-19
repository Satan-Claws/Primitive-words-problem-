# Round 1 / Route B: the Interchange Lemma and the Bader–Moura lemma (negative direction)

**Verdict, short.**
1. **The interchange route is provably dead, not just stalled.** I prove that Q satisfies the *conclusion* of the Ogden–Ross–Winklmann interchange lemma for every n, every R ⊆ Q ∩ Σⁿ, every m and **every** window position. The constant is c = e, and the guaranteed fraction is 1/(e(ω(n)+1)), where ω(n) is the number of distinct primes dividing n. The lemma only asks for 1/(c n²). So no family L_n, however clever (two halves, near-p-th powers, n with many prime factors), can work (Theorem 1).
2. The barrier extends to **every "box/rectangle-type" necessary condition with a bounded number of pieces**: multi-window or nested interchange of any depth, Ogden-marked interchange, and single-cut rectangle (communication-complexity) lower bounds for ambiguous CFGs (Theorem 2, Corollaries 1–3). Any per-length argument of this shape is ruled out. A refutation of CF-ness has to use cross-length information (pumping), or a non-rectangle lower-bound technique for CFG size. Both are of theorem strength.
3. **Bader–Moura.** I give the precise statement and reduce the negative direction to the existence of "pump-rigid" triples (z, D, E) (§6). I prove that the natural block/defect designs fail (Proposition 6.2): a one-letter or two-letter pump inside a single run always escapes. Exhaustive computation for n ≤ 13 (|E| ≤ 2) finds that a safe admissible decomposition always exists with Bader–Moura cost p ≤ 2. The missing statement (§6.4) is *equivalent* to the full negative result, so the BM route has no sub-lemma of lower strength. The evidence points to it being false.

All code and outputs are in `/tmp/claude-5714/-home-shobhit--claude-spares-spare-fauO4P/6f48459d-5790-4a18-bccc-eabb8efc4544/scratchpad/interchange/` (`barrier.py` for F0/F1, `f23.py` for F2/F3, `boxbarrier.py`, `bm.py`, `bm2.py`, and the `*_out.txt` files).

---

## 1. Precise statements

### 1.1 Interchange lemma (Ogden, Ross, Winklmann, SIAM J. Comput. 14 (1985))
Let L be a CFL, and write L_n = L ∩ Σⁿ. **There is a constant c_L** (it depends only on the grammar; c_L = number of nonterminals of a CNF grammar works) such that

> **for all** n ≥ 2, **for all** R ⊆ L_n, **for all** integers m with 2 ≤ m ≤ n, **there exist** k ≥ |R| / (c_L n²) and distinct z_1,…,z_k ∈ R with factorizations z_i = w_i x_i y_i such that
> (a) |w_1| = … = |w_k|, (b) |y_1| = … = |y_k|, (c) m/2 < |x_1| = … = |x_k| ≤ m, and
> (d) w_i x_j y_i ∈ L for all i, j ∈ {1,…,k}.

The quantifier order is c_L ∃, then n, R, m ∀ (the attacker chooses them), then Z and the window ∃ (the grammar chooses them). The middles x_i do *not* need to be distinct. The proof groups the derivation trees by (position, length, nonterminal) of a node with yield length in (m/2, m]. There are ≤ |N| n² classes.

**To refute Q with it** one needs: for every c there are n, R ⊆ Q_n and m such that for every window (a, ℓ) with m/2 < ℓ ≤ m, every Z ⊆ R with all cross-swaps primitive has |Z| < |R|/(c n²).

### 1.2 Bader–Moura lemma (J. ACM 29 (1982), "A generalization of Ogden's lemma")
For every CFL L **there is p** such that

> **for all** z ∈ L and all disjoint position sets D ("distinguished") and E ("excluded") with |D| = d, |E| = e and **d > p^{e+1}**, **there exist** u, v, w, x, y with z = uvwxy such that
> (1) vx contains at least one position of D and no position of E;
> (2) if r = |vwx ∩ D| and s = |vwx ∩ E|, then **r ≤ p^{s+1}**;
> (3) u v^i w x^i y ∈ L for **all i ≥ 0**.

With e = 0 this is Ogden's lemma (d > p, r ≤ p). The lemma requires *all* i, so a refutation only needs **one** bad exponent i per admissible decomposition. Positions in neither D nor E ("neutral") are free and do not count in r.

---

## 2. Reformulation of the interchange conclusion as a rectangle problem

Fix n and a window (a, ℓ). A word is a pair (context c = (w, y), middle x). Let M be the 0/1 matrix with M[c, x] = 1 iff w x y ∈ Q. A set Z ⊆ R satisfies (d) **iff** Z ⊆ A × S for some all-ones combinatorial rectangle A × S of M (take A = contexts of Z, S = middles of Z). So the interchange conclusion for Q at this window says exactly:

> some all-ones rectangle of M contains ≥ |R|/(c n²) points of R.

**Zeros are extremely sparse and rigid.** w x y ∉ Q iff it is (n/p)-periodic for some prime p | n. (If z = u^q with q ≥ 2, pick a prime p | q; then z has period n/p.) So only ω(n) periods matter, not all divisors.

**Lemma 2.1 (≤ ω(n) zeros per line).**
- If ℓ ≤ n/2, every row c has at most ω(n) zeros.
- If ℓ ≥ n/2, every column x has at most ω(n) zeros.

*Proof.* When ℓ ≤ n/2, the context occupies the cyclic interval [a+ℓ, n) ∪ [0, a) of length n − ℓ ≥ n/2 ≥ n/p. A cyclic interval of length ≥ d in ℤ_n with d | n meets every residue class mod d. So a d-periodic word is determined by its restriction to the context. Hence for each prime p there is at most one middle x making w x y (n/p)-periodic. The case ℓ ≥ n/2 is symmetric: the middle is an interval of length ≥ n/p. ∎

---

## 3. Theorem 1 (single-window barrier)

**Theorem 1.** Let n ≥ 2, R ⊆ Q ∩ Σⁿ (any alphabet), and let 1 ≤ ℓ ≤ n−1 and 0 ≤ a ≤ n−ℓ be arbitrary. Then there is Z ⊆ R with
  |Z| ≥ |R| / (e (ω(n)+1)),
such that, writing z = w_z x_z y_z with |w_z| = a and |x_z| = ℓ, we have w_z x_{z'} y_z ∈ Q for all z, z' ∈ Z.

*Proof.* Let ω = ω(n) and π = 1/(ω+1). Assume ℓ ≤ n/2 (otherwise swap the roles of rows and columns, using Lemma 2.1 for columns).
- Let S be a random set of middles, each included independently with probability π.
- Let A(S) = {contexts c : no x' ∈ S has M[c, x'] = 0}.

A(S) × S is all-ones by construction. Fix z = (c, x) ∈ R. Since z is primitive, x ∉ zeros(c). So
P[z ∈ A(S) × S] = P[x ∈ S] · P[S ∩ zeros(c) = ∅] = π (1−π)^{|zeros(c)|} ≥ π(1−π)^ω = (1/(ω+1)) (ω/(ω+1))^ω ≥ 1/(e(ω+1)).
By linearity of expectation some S gives |R ∩ (A(S) × S)| ≥ |R|/(e(ω+1)). Take Z = R ∩ (A(S) × S). ∎

**Corollary 1 (Q satisfies the interchange lemma).** For c_L = e and every n ≥ 2, R ⊆ Q_n and m ∈ [2, n], the conclusion (a)–(d) holds: take any ℓ ∈ (m/2, m] and any a, and use ω(n)+1 ≤ n². The guarantee is not just met but exceeded: the slack factor is c n² / (e(ω(n)+1)) ≥ n^{2−o(1)}.

Consequences for the design question in the task:
- **"Must rule out many exponents."** The number of exponents enters only through ω(n)+1. For a contradiction we would need ω(n)+1 > c n²/e. But ω(n) ≤ log₂ n, and ω(n) ≤ (1+o(1)) ln n / ln ln n. Choosing n = p·q, primorials, or highly composite n gains at most a logarithmic factor against a quadratic budget.
- **"Two halves xy with x ≠ y."** For n = 2^k, ω = 1, the matrix is the complement of a partial matching per line, and the theorem gives fraction ≥ 1/(2e). Adding more primes only reduces the constant.
- **"Size condition."** |R| can be made as large as |Q_n| ≈ |Σ|ⁿ, so the hypothesis side is trivially satisfiable. The obstruction is on the other side: the conclusion is *always* satisfiable with room to spare.
- **Window choice is irrelevant.** Theorem 1 holds for *every* (a, ℓ). So "marked" or Ogden-style interchange variants, which force the window to cover marked positions, fail as well.
- **Distinct middles.** ORW require no distinctness. If R has every middle class of size ≤ s at the window, then Z has ≥ |Z|/s distinct middles, so the swaps are genuinely nontrivial (see the "distinct middles" column of the experiments).

**Corollary 2 (rectangle / nondeterministic communication complexity).** For any fixed cut (a, ℓ), all of Q_n can be covered by K ≤ ⌈e(ω(n)+1) · n ln|Σ|⌉ + 1 all-ones rectangles. (Take K independent copies of the random rectangle. A fixed 1-entry is missed with probability ≤ (1 − 1/(e(ω+1)))^K < |Σ|^{−n}. Then take a union bound over the ≤ |Σ|ⁿ entries.)

So the nondeterministic communication complexity of primitivity is ≤ log₂ n + O(log log n) **for every cut**. The standard rectangle method for CFG size gives "size·n² ≥ cover number", and here that yields only s ≥ O(1). This makes precise the dead-end note "communication bounds known only for unambiguous CFGs": for ambiguous CFGs the rectangle method provably cannot give anything for Q.

---

## 4. Theorem 2 (universal box barrier: any number of windows, any nesting)

Let 0 < b_1 < … < b_{m−1} < n cut [0, n) into m intervals ("pieces"). Group the pieces into coordinates G_1, …, G_g; a coordinate value is the concatenation of its pieces. A *box* is B_1 × … × B_g, and its words are all the reassemblies.

**Theorem 2.** For every such structure and every R ⊆ Q_n there is a box all of whose reassembled words are primitive and which contains ≥ |R| / (8m)^{ω(n)} elements of R.

*Proof.* For a prime p | n let d = n/p and φ(k) = (k+d) mod n.
- Split [0, n) into maximal runs on which (piece(k), piece(φ(k))) is constant ("classes"). Breakpoints come from piece boundaries of k (≤ m−1, plus k = 0) and of φ(k) (≤ m, including the wrap of φ). So there are ≤ 2m classes.
- A primitive z is not d-periodic, so some class β has z|β ≠ z|φ(β) (as strings).
- Pigeonhole over tuples (β_p)_p gives R' ⊆ R with |R'| ≥ |R|/(2m)^ω in which every z mismatches on every β_p.
- Choose independent uniformly random sets T_p ⊆ Σ^{|β_p|}.
- Let B_h consist of the coordinate values y of G_h that satisfy: y|β_p ∈ T_p whenever β_p lies in G_h, and y|φ(β_p) ∉ T_p whenever φ(β_p) lies in G_h. Each of β_p and φ(β_p) lies inside a single piece, so these are conditions on single coordinates and the box is a genuine product.
- Every reassembled word w has w|β_p ≠ w|φ(β_p) for every p, so it is primitive.
- Each z ∈ R' lies in the box with probability exactly 4^{−ω}. The events for different p are independent because the T_p are, and z|β_p ≠ z|φ(β_p).

Taking expectations gives the bound. ∎

**Corollary 3 (multi-window and nested interchange of any depth are useless).** Suppose a lemma has the form "∀R ⊆ L_n ∃ a product structure with ≤ 2t+1 pieces (whoever chooses it) and a box with ≥ |R|/(c n²)^t points of R inside L". This covers the depth-t nested interchange obtained from t nested tree nodes, and t disjoint windows. Q satisfies every such lemma for an absolute constant c:
(16t+8)^{ω(n)} ≤ 24^{ω(n)} · t^{ω(n)} ≤ (C₁ n²) · n^{2(t−1)} ≤ (C₁ n²)^t.
Here 24^{ω(n)} = n^{o(1)}, so C₁ = sup_n 24^{ω(n)}/n² < ∞, and t^{ω(n)} ≤ t^{log₂ n} = n^{log₂ t} ≤ n^{2(t−1)}.

Theorem 1 is the sharp single-window version: a constant fraction instead of n^{−o(1)}.

**The structural reason.** Non-primitivity of a length-n word is a disjunction of only ω(n) ≤ log₂ n "global equality" events (d-periodicity). Each one can be killed inside a product set by fixing a single mismatch class, at a constant-factor cost. Any argument that only uses "a CFL restricted to one length contains large product sets" therefore cannot separate Q from Σⁿ.

---

## 5. Computational falsification of candidate families (Theorems 1–2 in action)

`barrier.py` builds the random rectangle of Theorem 1 (best of 10–20 trials) for **every** window (a, ℓ) and every ℓ (step noted). It then verifies the cross-swaps by brute force: all of them when |A|·|S| ≤ 2·10⁵, otherwise 2·10⁵ random swaps. Alphabet {a, b}. "min |Z|/|R|" is the minimum over all windows. "Bound" is 1/(e(ω+1)).

| family | n | ω | \|R\| | windows | min \|Z\|/\|R\| | bound | distinct middles (worst window) |
|---|---|---|---|---|---|---|---|
| F0: all of Q_n | 6 | 2 | 54 | 20 | 0.278 | 0.123 | 8 |
| F0 | 8 | 1 | 240 | 35 | 0.267 | 0.184 | 16 |
| F0 | 9 | 1 | 504 | 44 | 0.556 | 0.184 | 16 |
| F0 | 10 | 2 | 990 | 54 | 0.242 | 0.123 | 32 |
| F0 | 12 | 2 | 4020 | 77 | 0.227 | 0.123 | 64 |
| F1: Hamming-1 from a p-th power, all p \| n | 12 | 2 | 528 | 77 | 0.222 | 0.123 | 64 |
| F1 | 18 | 2 | 3000 | 170 | 0.214 | 0.123 | 512 |
| F1 | 30 | 3 | 3000 | 239 | 0.191 | 0.092 | 2852 |
| F2: near-squares xy, x and y at Hamming distance 1 | 12 | 2 | 384 (all) | 77 | 0.224 | 0.123 | 64 |
| F2 | 20 | 2 | 3000 | 209 | 0.226 | 0.123 | 995 |
| F2 | 30 | 3 | 3000 | 239 | 0.191 | 0.092 | 2895 |
| F3: 1–2 flips from words of period d \| 30 (near-powers for several exponents at once) | 30 | 3 | 500 | 239 | 0.186 | 0.092 | 384 |

All verifications passed. The worst windows sit at ℓ ≈ n/2, as the proof predicts: there the zero lines are tightest.

`boxbarrier.py` (Theorem 2) uses adversarial R: 1500 words made by 1–3 flips from words with period d | n, so they are near-powers for many exponents at once. It builds the pigeonhole + random-cut box, and verifies by 2·10⁴ random reassemblies (all primitive). Results:

| n (ω=3) | structure | classes per prime | \|Z\|/\|R\| |
|---|---|---|---|
| 30 | single window w·x·y | [6,3,6] | 0.018 |
| 30 | nested 3-level contiguous x\|r\|c | [6,6,6] | 0.015 |
| 30 | nested with two-sided ring c1 r1 x r2 c2 | [8,9,9] | 0.015 |
| 30 | 4 coordinates, 6 interleaved pieces | [6,6,12] | 0.018 |
| 42 | the same four structures | — | 0.018 / 0.017 / 0.010 / 0.013 |
| 60 | the same four structures | — | 0.014 / 0.015 / 0.013 / 0.013 |

These fractions are constants independent of n, as predicted, against the 1/(cn²)^t that the lemmas would need.

---

## 6. Bader–Moura, negative direction

### 6.1 Reduction
BM refutes Q iff:

> **(P-rigid)** for every p there exist z ∈ Q and disjoint D, E with |D| > p^{|E|+1} such that every factorization z = uvwxy with vx ∩ D ≠ ∅, vx ∩ E = ∅ and |vwx ∩ D| ≤ p^{|vwx ∩ E|+1} has some i ≥ 0 with u v^i w x^i y ∉ Q.

z is chosen **after** p. This is what makes the a^n b^{n+n!} trick possible: with M = lcm(1..P), a run that is exactly M short of the length needed for a power is "bad" for every pump length s ≤ P, via i = 1 + M/s.

### 6.2 Proposition (block/defect designs always fail)
Let z = a^{k_1} b a^{k_2} b ⋯ a^{k_r} b be primitive, so (k_1, …, k_r) is aperiodic. Note z = t^q iff (k_j) has period r/q. Allow E to contain any b-positions. Call block j *unsafe* if both pumps v = a and v = aa inside block j (w = x = ε, so r ≤ 2) have a bad exponent. Then **at most (3/2)(τ(r)−1) blocks are unsafe**, where τ is the number of divisors.

*Proof.* Pumping v (|v| = s) inside block j changes k_j by λ = (i−1)s ∈ {−s} ∪ {0, s, 2s, …}. The result is a power iff k + λ e_j is d-periodic for some d | r, d < r.

Fix d. Then all residue classes mod d other than class(j) are constant, and class(j) is constant except at j. So λ_j(d) is determined.

Suppose j ≠ j' both use the same d:
- If j and j' lie in different classes, we get a contradiction: each forces the other's class to be constant.
- If they lie in the same class of size ≥ 3, then λ = 0, a contradiction.
- If they lie in a class of size 2, then λ_j(d) = −λ_{j'}(d).

So each d gives at most one positive target and at most one negative target.

Being bad for s = 1 and for s = 2 needs either a positive target, or the two negative targets −1 and −2, which come from two different d's. There are τ(r)−1 values of d. So
#unsafe ≤ (τ(r)−1) + (τ(r)−1)/2. ∎

Hence, if D meets more than (3/2)(τ(r)−1) blocks of length ≥ 2, BM is satisfied with p = 2 by a single-run pump. `bm.py` Part A confirms by brute force that no aperiodic k ∈ {0..5}^r, r ≤ 7, has all blocks unsafe.

If instead D is concentrated in a few "defect" blocks, the adversary **co-pumps**: v at the end of the defect block, x at the start of the neighbouring block (w = b, so r ≤ 2, s ≤ 1), and preserves the defect. Example: z = a^K b a^{K+M} b with D = first block and E = the two b's. The pump (v, x) = (a, a) keeps the difference M forever, so every pumped word is primitive. To block this, one must exclude the partner block, which costs |E| ≥ K+M. But |D| ≤ K then cannot exceed p^{|E|+1}.

This is exactly the mechanism of the CFG for non-p-th powers: mismatched pairs are pumped together. Multiple exponents do not obviously help. A safe co-pump for squares has to be killed by a cube, 5th power, etc. *at the same location*. The counting above (one positive target per period, per location) suggests there are not enough exponents. Every period d and every resulting length n + (i−1)(|v|+|x|) gives one target; ω(·) and τ(·) are n^{o(1)}, while the adversary has Ω(|D|/p^{O(1)}) disjoint local pump locations.

### 6.3 Computation
`bm.py` / `bm2.py` cover all primitive binary z with z_1 = a (the a↔b symmetry), all E with |E| ≤ 2, and D = complement of E. They search decompositions with |vwx| ≤ 4 and check u v^i w x^i y ∈ Q for 0 ≤ i ≤ 3n+6. For each (z, E) they record the minimum cost p_needed = ⌈r^{1/(s+1)}⌉:

| n | (z, E) pairs | p_needed = 1 | p_needed = 2 | worst instance |
|---|---|---|---|---|
| 8 | 4440 | 4440 | 0 | — |
| 9 | 11592 | 11583 | 9 | aaaabaaab, E = both b's |
| 10 | 27720 | 27720 | 0 | — |
| 11 | 68541 | 68530 | 11 | aaaaabaaaab, E = both b's |
| 12 | 158790 | 158790 | 0 | — |
| 13 | 376740 | 376727 | 13 | aaaaaabaaaaab, E = both b's |
| 14 (\|E\| ≤ 1, span ≤ 3) | 121905 | 121905 | 0 | — |

So on every instance up to these sizes, BM holds with p = 2. The only instances needing p = 2 are the predicted a^k b a^{k±1} b with excluded separators. The pump range i ≤ 3n+6 is a heuristic cutoff; this is evidence, not proof.

### 6.4 Exact missing statement and its strength
- **For a non-CF proof via BM:** (P-rigid) above. It is *equivalent* to the BM route succeeding, so there is no smaller sub-lemma. It needs words that are within one local pump of a power **at Ω(|D|/p^{O(1)}) independent locations** at once, with only log_p|D| excluded positions.
  - For large exponents (q ≥ 11) Fine–Wilf constrains this heavily, but **heuristically only, not proved here**. Two approximate periods P, P' ≤ n/11, each valid off two short windows, leave a defect-free stretch longer than P + P', so they share the period gcd(P, P') there. That should pin down the defect locations.
  - For small exponents q ∈ {2, …, 10}, with periods (n + Δ)/q that vary with i, I could neither prove nor refute rigidity. **This is the precise open core:** a "local-repair rigidity lemma for small exponents with varying length." If true, it makes BM provably useless for Q; if false, its counterexamples refute CF-ness. It is of theorem strength either way.
- **For any per-length rectangle method:** provably impossible (Theorems 1, 2).
- **Remaining non-pumping alternative:** a superpolynomial lower bound on CFG size for Q ∩ Σⁿ by a *non-rectangle* method. CF-ness of Q would give CFGs of size O(|G| n³) for Q_n, so such a bound would suffice. Corollary 2 shows every rectangle bound is vacuous. No non-rectangle technique for general ambiguous CFGs is known to me, and the true size might well be polynomial; the trivial upper bound is n^{O(ω(n))} by guessing one mismatch per prime. Theorem strength, and possibly false.

**Bottom line for the campaign.** Drop interchange-type, box-type and fooling-set-type attacks completely; they are refuted in §3–4, not merely stalled. A negative proof must exploit **uniformity across lengths** (pumping with free exponent i, or the finiteness of the grammar across all n). The concrete test case is the small-exponent local-repair question in §6.4.
