# Round 4 report of agent "periodic" (near-powers, periodicity, pumping)

**Claim status: no proof of either resolution.** I have some small proved lemmas, one explicit
near-power family F_ins together with barrier theorems that rule out every "single-pump" and
"one-parameter" argument for it, and one candidate lemma (CL1) that survives all the test languages.
Scripts are in `infinite-ambiguity/claude_round4-5_2026-11-18/scripts/periodic/` (`common.py`, `near.py`, `pumps.py`, `classify.py`).
Each script runs in under 2 minutes on one core.

Notation: Σ = {a,b}, Q = primitive words, NP = Σ^+ \ Q. A word t ∈ (a^*b)^+ ends in b. Its **block vector** is
β(t) = (y_0,…,y_{k-1}) ∈ N^k, where t = a^{y_0}b⋯a^{y_{k-1}}b.

**Fact B (PROVED).** A word t ∈ (a^*b)^+ is non-primitive iff β(t) is invariant under some cyclic shift by d,
with 0 < d < k. Proof: t = v^q (q ≥ 2) forces v to end in b, so β(t) = β(v)^q. Conversely, a shift-invariant
β gives β = β'^{k/d}, so t = v^{k/d}. Consequence: if some value occurs exactly once among the y_i
(k ≥ 2), then t is primitive.

## 1. Near-power lemmas

**L1 (PROVED; COMPUTER-CHECKED n ≤ 14, `near.py`).** Two distinct non-primitive words of the same length
differ in at least 2 positions. So every word at Hamming distance 1 from u^k (k ≥ 2) is primitive.
*Proof.* Work over Z with w, P ∈ {0,1}^n (cyclic indices), P of period m (m | n, m < n), w of period d (d | n, d < n), and w − P = εe_i with ε = ±1. Apply σ_d (σ_d f(t) = f(t+d)) and use σ_d w = w: P − σ_d P = ε(σ_d e_i − e_i) = ε(e_{i−d} − e_i). The left side is m-periodic (σ_d commutes with σ_m). The right side has support {i−d, i} of size 2 (d ≢ 0 mod n), and its two nonzero values have opposite signs. An m-periodic vector with k = n/m ≥ 2 has, on each residue class mod m, constant value on
all k ≥ 2 positions. So the support is a union of full classes. The only option is k = 2 with
i−d ≡ i+m (mod n), but then the two values in that class would have to be equal, not opposite. ∎

**L2 (COMPUTER-CHECKED for |u^k| ≤ 15, `near.py`; PROVED only in the sub-case below).** If u is
primitive with |u| = m ≥ 2, k ≥ 2, and one letter is inserted anywhere into u^k, the result is primitive.
For m = 1 this fails trivially (a^{k+1}).
*Partial proof (q ≥ 3, k ≥ 6).* Write w = x c y with xy = u^k and w = v^q, d = |v| ≤ (km+1)/3.
One of x, y has length ≥ km/2 ≥ m + d − 1 (this uses k ≥ 6). By Fine–Wilf that factor has period gcd(m,d).
It contains a conjugate of u, which is primitive, so m | d. Then n = qd ≡ 0 mod m, contradicting
n = km+1 with m ≥ 2. The cases q = 2 and k ≤ 5 need a finer two-segment argument, which I did not finish.

**Family F_ins = { a(a^m b)^k : m ≥ 1, k ≥ 2 }**, an insertion near-power: a letter a is inserted into (a^m b)^k.
- **Primitive (PROVED):** ψ = (km+1, k) and gcd(km+1, k) = 1.
- **Neighbouring powers:** (a^m b)^k (delete one a), (a^{m+1}b)^2-type words, and so on.

## 2. Barriers for F_ins: which arguments cannot work

**Bar1, one-parameter slices (PROVED).**
- For fixed m, F_ins ∩ {m} = a^{m+1}b(a^m b)^* is regular and lies in Q.
- For fixed k, F_ins ∩ {k} ⊆ R_k = {w : |w|_b = k, |w|_a ≡ 1 (mod k)}. R_k is regular and R_k ⊆ Q, since
  gcd(|w|_a, k) = 1 and a power v^q has q | gcd(|w|_a, |w|_b).
- So an argument must use both parameters unbounded at once. In particular no argument through a
  bounded slice, Ginsburg semilinearity for fixed k, or a fixed block alphabet can work.

More generally (LITERATURE-dependent): any family with sup |w|_b ≤ 209 (or sup |w|_a ≤ 209) is covered by
Q ∩ {|w|_b ≤ 209}. That language is CF by Kászonyi–Katsura for n with ≤ 3 distinct prime factors, plus
rotation (devil T3).

**Bar2, Parikh/commutative certificates (PROVED).** No semilinear set S of coprime vectors contains ψ(F_ins).
So no CF language of the form ψ^{-1}(S) ⊆ Q covers F_ins. Steps:
1. Take a linear set c + Np + Nq with p, q linearly independent, and a prime r ∤ det(p,q).
2. p and q span (Z/r)^2, so some 0 ≤ s, t < r gives c + sp + tq ≡ 0 (mod r). Such a set always contains a
   non-coprime vector.
3. Hence a coprime semilinear set is a finite union of points and rays c + Np. (Parallel periods reduce to
   finitely many rays.)
4. A ray with p_2 > 0 meets the horizontal line y = k at most once, and a ray with p_2 = 0 lies on its own
   line y = c_2.
5. ψ(F_ins) has infinitely many points on every line y = k. ∎

Note that this only rules out commutative certificates. A CF L ⊆ Q need not have a coprime Parikh image.

**Bar3, exact classification of power-producing pumps (case A PROVED; full statement COMPUTER-CHECKED,
`classify.py`: m = 3..7, k = 4..8, j ≤ 6, all decompositions with |uyv| ≤ m).**
Let w = a(a^m b)^k with k ≥ 4, and let w = xuyvz with |uyv| ≤ m and |uv| ≥ 1. Then x u^j y v^j z is
non-primitive for some j ≥ 0 iff one of the following holds:
- (A0) uv = a, the letter lies in block 0, and j = 0. The result is (a^m b)^k.
- (A2) uv = a, the letter lies in block k/2 (k even), and j = 2. The result is (a^{m+1}b a^m b⋯)^2.
- (B) uv contains exactly one b and m−1 letters a, j = 0, and the merged block lands at position (k−1)/2
  (k odd). Example: m = 5, k = 5 gives (a^6 b a^5 b)^2.

*Proof of case A* (uv ∈ a^+, so u lies in block i and v in block i' ∈ {i, i+1}):
- β(pumped word) = m·1 + D, where D = e_0 + (j−1)(|u|e_i + |v|e_{i'}). The word is non-primitive iff D is
  shift-invariant by some d.
- If D = 0, then j = 0 and |u|e_i + |v|e_{i'} = e_0. This is (A0).
- Otherwise supp D ⊆ {0, i, i'} is a union of orbits of size q = k/d ≥ 2. For k ≥ 4 an orbit of size 3 would
  be {0, d, 2d} with d ≥ 2, and {i, i'} cannot contain the non-adjacent pair {d, 2d}. So q = 2 and
  supp D = {0, k/2}.
- 0 ∈ {i, i'} would force {0, k/2} ⊆ {0, 1}, which is impossible for k ≥ 4. So D_0 = 1 = D_{k/2}, the other
  touched block has coefficient 0, j = 2, and |uv| = 1. This is (A2).

Case B: done by computer only. (Other relevant cases: k = 3 has the extra cube pump uyv = aba with j = 2;
for k = 2, |uyv| ≤ m pumps are covered by A.)

**Bar4, Ogden and Bader–Moura cannot force those pumps (PROVED).** Let m ≥ 3, k ≥ 2, and mark any
non-empty set of positions of w ∈ F_ins.
- If a marked position is an a, take u = that a together with a neighbouring a in the same block
  (u = aa, y = v = ε). Every pump changes one block by 2(j−1). For j ≠ 1 this creates a block value that occurs exactly once, so by Fact B every pumped word is primitive. (Block 0 pumped down
  gives m−1, which is unique; other blocks give m−2 or m+2(j−1) ≠ m, m+1, which is unique.)
- If the marked position is a b, take u = b. For j = 0 two blocks merge into one of length ≥ 2m > m+1,
  which is unique. For j ≥ 2 the value m+1 stays unique.

So every pumping/Ogden/Bader–Moura-type lemma, which applies one decomposition per word, is satisfied on F_ins.
The power-producing pumps A0/A2/B are an exact length-1 or length-m pump at an exact position, and no iteration
lemma forces them. **Answer to the briefing question "when can one prove a pump producing u^{k'} exactly?":**
only if the grammar is forced to use a pump with |uv| = 1 at block 0 or k/2, or the B-merge. Single-tree
iteration theorems never force this.

## 3. Candidate lemma and test bank

**CL1 (CONJECTURED).** Every CFL L ⊇ F_ins contains a non-primitive word.
- CL1 implies "Q is not CF".
- It survives every CF subset of Q I know of:
  - E' and {|w|_b = |w|_a + c} (they miss most of F_ins);
  - coprime-Parikh lines (Bar2);
  - coPow_k and finite intersections of coPow_k (these contain non-primitive words, so they are not test
    languages for "⊆ Q", only for intersections at fixed lengths);
  - bounded slices and Q ∩ {|w|_b ≤ K}, which miss F_ins for large k.
- Natural CF-looking supersets inside Q all fail to be CF:
  - "unique longest block": its slice {a^r b a^s b a^t b : s, t < r} is not CF. This is PROVED by the pumping
    lemma; the only surviving pump (a^δ in the r- and s-blocks) breaks t < r at j = 0.
  - {w : |w|_a ≡ 1 mod |w|_b}: its Parikh image is not semilinear. Shift by one and project (Presburger) to
    the composite numbers.
  - The first-vs-last block comparison contains (a^{s+1}b x a^s b)^2.

**IDEA (not proved): parity.** A pump changing block lengths by an even amount, or a b-pump, keeps a unique
block forever (Bar4). To produce F_ins words for both m and m+1 with k fixed and large, a grammar needs pumps
that shift a block by an odd amount. Combining the derivation trees of a(a^m b)^k and a(a^{m+1}b)^k inside
one grammar might force an odd single-block pump at block 0 or k/2. I did not make this rigorous. A two-word
surgery argument across different m seems to be the minimum needed.

## Registry entry
1. **Aimed at:** CL1, that every CFL containing {a(a^m b)^k : m ≥ 1, k ≥ 2} contains a non-primitive word.
   This implies Q is not CF.
2. **Proved:**
   - L1 (Hamming-1 neighbours of powers are primitive).
   - L2 in the sub-case q ≥ 3, k ≥ 6.
   - Fact B.
   - Bar1: each one-parameter slice of F_ins lies in a regular subset of Q.
   - Bar2: no coprime semilinear Parikh certificate exists.
   - Bar3 case A: classification of power-producing short pumps.
   - Bar4: Ogden/Bader–Moura marking cannot force them.
   - Non-CF-ness of the natural supersets.
3. **Missing step:** a lemma of the form "if G is a CFG with F_ins ⊆ L(G), then for some m, k a derivation
   of a(a^m b)^k admits a pump of type A0, A2 or B (|uv| = 1 at block 0 or k/2, or the m-merge)". This
   requires a multi-derivation (cross-m) surgery argument.
4. **Counterexamples found:**
   - Insertion into u^k with |u| = 1 (trivial).
   - k = 3 cube pump aba.
   - B-type pumps with |uv| = m for odd k (e.g. m = 5, k = 5).
   - The supersets "first block > last block" and "first block ≠ second block" contain powers.
5. **Strength:** CL1 is stronger than "Q is not CF" (it implies it). The missing step is equivalent to CL1.
6. **What would reopen the route:** a tree-surgery lemma that combines derivations of words differing in
   one parameter (m → m+1 for all blocks), forcing an odd-length single-block pump. Alternatively, a CF
   language L with F_ins ⊆ L ⊆ Q, which would refute CL1 and be a strong hint toward the positive side.
