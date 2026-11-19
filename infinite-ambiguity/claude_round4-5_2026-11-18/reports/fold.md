# Report of agent "fold": line certificates n − 4m_c = R, the fold-balanced language, and density

**Claim status.** No proof of either resolution is claimed. Q½ is **not** refuted: I found no CF L ⊆ Q of density ≫ n^{-1/2}.
Scripts are in `infinite-ambiguity/claude_round4-5_2026-11-18/scripts/fold/`:
- `lines.py`: exact counts for n ≤ 22 (`out_exact.txt`) and Monte Carlo up to n = 1012 with 4000 samples per n (`out_mc.txt`).
- `slice.py`: checks for §3.

Each run takes under 4 minutes on one core.

Notation:
- Positions are in Z_n, and an axis c is the reflection i ↦ c − i.
- m_c = #{unordered mismatched pairs {i, c−i}}. One identity is used for computation: m_c = |w|_b − (w ⊛ w)(c), with cyclic convolution of the 0/1 vector.
- For a linear word, the "central axis" is c = n−1 (pairs t ↔ n−1−t). Write m(w) = m_{n−1}(w).
- Φ_R := {w : |w| − 4m(w) = R}.
- Let M be the number of matched pairs. Since M + m = ⌊n/2⌋, the coordinator's F_r = {M − m = r} equals Φ_{2r} on even lengths and Φ_{2r+1} on odd lengths.

## 1. Certificate G re-verified (PROVED)

Suppose w = u^p with p ≥ 2 and |u| = d. Then w_{i+d} = w_i, so χ_i := [w_i ≠ w_{c−i}] satisfies χ_{i+d} = χ_i.
- The set {i : χ_i = 1} is therefore a union of orbits of i ↦ i+d. Each orbit has size n/gcd(n,d) = p.
- This set has 2m_c elements: each mismatched unordered pair contributes both of its points, and fixed points never mismatch.
- Use instead the half-set {i : w_i = b, w_{c−i} = a}. It is also d-invariant, because both conditions are. It has exactly m_c elements, so p | m_c.
- Since also p | n, we get gcd(m_c, n) ≥ p.

Nothing in this argument depends on the parity of n or of c. So it holds for odd n (one fixed point), for even n with even c (two fixed points), and for even n with odd c (no fixed point). For n = 1, m = 0 and gcd = 1, which is correct.

**Lines.** gcd(m, 4m+R) = gcd(m, R). The following targets therefore guarantee coprimality:

| n | target m |
|---|---|
| n odd | m = (n∓1)/4, i.e. R = ±1 (always coprime) |
| n ≡ 2 (mod 8) | m = (n+2)/4, which is odd (R = −2) |
| n ≡ 6 (mod 8) | m = (n−2)/4, which is odd (R = 2) |
| n ≡ 0 (mod 8) | m = n/4 ± 1, which is odd (R = ∓4) |
| n ≡ 4 (mod 8) | m = n/4 ± 2, which is odd (R = ∓8) |

Any fixed R together with "m mod |R| a unit" also works. That condition is semilinear, which matches Lemma S.

The line-union language is LU := {w : ∃c, m_c ∈ T(|w|)}, with T(n) the targets above. It is sound: there are 0 non-primitive hits for n ≤ 22 (COMPUTER-CHECKED), as the proof predicts.

## 2. The union over axes has density → 1 (PROVED for odd n; COMPUTER-CHECKED for even n)

**Lemma I (PROVED).** Let n be odd and c ≠ c'. Then m_c and m_{c'} are independent.

*Proof.*
1. Form the graph on Z_n whose edges are the mirror pairs of c and of c'. Every vertex has degree ≤ 2.
2. The components are the orbits of ⟨ρ_c, ρ_{c'}⟩. Each is a union of cosets of the translation ρ_{c'}ρ_c, so each has odd size, since n is odd.
3. On an odd orbit, each reflection has exactly one fixed point. The two fixed points differ, because 2i ≡ c and 2i ≡ c' are incompatible.
4. So every component is a path, and the whole graph is a forest.
5. The XORs w_i ⊕ w_j over the edges of a forest are i.i.d. fair bits when w is uniform. Hence (m_c, m_{c'}) are sums over disjoint sets of independent bits. ∎

**Theorem U (PROVED).** For odd n, P(w ∉ LU) ≤ 1/(n·p_n) ≤ C n^{-1/2}.
- Here p_n = P(Bin(h, 1/2) = target) with h = (n−1)/2.
- p_n ≥ 1/√(n−1) for n ≡ 1 (mod 4), using C(2k,k)/4^k ≥ 1/(2√k).
- p_n ≥ (3/4)·1/√(n−1) for n ≡ 3 (mod 4).

*Proof.* Let X = #{c : m_c = target}. Then EX = n p_n. By Lemma I the indicators are pairwise independent, so Var X ≤ n p_n. Chebyshev gives P(X = 0) ≤ Var X/(EX)². ∎

So the line certificates, which are Cyc-closed and choose the axis for free, already have density 1 − O(n^{-1/2}). Monte Carlo suggests the true miss rate is much smaller.

For even n, components can be cycles, which impose parity constraints, so I have no proof there. The data:
- Exact: P(LU) = 0.925, 0.959, 0.968 at n = 18, 20, 22.
- Monte Carlo: P(LU) ≥ 0.998 for every tested even n ≥ 100, and 4000/4000 samples hit for n ≥ 104.
- Using only vertex-type axes (even c) gives similar numbers.

Exact and Monte Carlo numbers are in `out_exact.txt` and `out_mc.txt`. In those files, √n·P(fixed axis on line) ≈ 1.13 per target, which matches 2/√π.

## 3. The fold-balanced languages are not CF (PROVED)

**Theorem F.** For every R ∈ Z, Φ_R is not CF. Consequently, for every r ∈ Z:
- F_r = {w : M − m = r at the central axis} is not CF;
- the fixed-cut line language {w : m(w) ∈ T(|w|)} is not CF.

*Proof.*
1. **Reduce to three distinct letters.** Suppose Φ_R is CF. Then L' := h^{-1}(Φ_R) ∩ c₁*c₂*c₃* is CF, where h(c₁) = h(c₃) = a and h(c₂) = b. Its exponent set is E = {(i,j,k) ∈ N³ : a^i b^j a^k ∈ Φ_R}.
2. **Apply Ginsburg.** LITERATURE: Ginsburg, *The Mathematical Theory of Context-Free Languages* (1966), Thm 5.4.2 (Ginsburg–Spanier, bounded languages): for distinct letters, L ⊆ c₁*…c_k* is CF iff its exponent set is a finite union of linear sets with stratified period sets. Stratified means each period has ≤ 2 nonzero coordinates and supports do not cross.
3. **Compute E.** On a^i b^j a^k the b-blocks of w and w^R are [i, i+j) and [k, k+j). Hence m = min(j, |i−k|), and E = {x : f(x) = R} with f(i,j,k) = i + j + k − 4 min(j, |i−k|). This is COMPUTER-CHECKED for i, j, k < 14 (`slice.py`).
4. **f is homogeneous and Lipschitz.** f is positively homogeneous and 5-Lipschitz in ℓ¹.
5. **Every period is a zero of f.** If c + Np ⊆ E, then |f(c+tp) − t f(p)| ≤ 5|c|₁ for all t, so f(p) = 0.
6. **Classify the possible periods.** Let p ≥ 0 have ≤ 2 nonzero coordinates and f(p) = 0.
   - If p₂ = 0, then f(p) = |p|₁ > 0, so this case is impossible.
   - If p = (x, y, 0), then x + y = 4 min(y, x), which forces (3,1,0) or (1,3,0) up to scaling.
   - Symmetrically, if p = (0, y, z), the options are (0,1,3) and (0,3,1).
7. **No linear set has two non-parallel periods.** If p = αu and q = βv are non-parallel periods of one linear set, then c + t(xp + yq) ∈ E for all t, x, y ∈ N. So f(au + bv) = 0 for all a, b ∈ N. This fails for each of the 6 pairs:
   - (0,1,3) + (0,3,1) = (0,4,4), with f = 8;
   - (0,1,3) + 2(1,3,0) = (2,7,3), with f = 8;
   - (0,1,3) + (3,1,0) = (3,2,3), with f = 8;
   - (0,3,1) + (1,3,0) = (1,6,1), with f = 8;
   - (0,3,1) + 2(3,1,0) = (6,5,1), with f = −8;
   - (1,3,0) + (3,1,0) = (4,4,0), with f = −8.
8. **Bound E level by level.** Each linear set therefore has all its periods on one ray. A ray direction has positive coordinate sum, so each linear set meets each level {|x|₁ = N} in ≤ 1 point. Hence |E ∩ {|x|₁ = N}| = O(1).
9. **Count E directly and contradict.** For N ≡ R (mod 4), the points j = (N−R)/4, i + k = N − j, i − k ≥ j all satisfy f = N − 4j = R. There are ≥ N/4 − O(1) of them. This contradicts step 8, so Φ_R is not CF.
10. **Extend to F_r.** F_r ∩ (Σ²)* = Φ_{2r} ∩ (Σ²)*. Run the same argument on the levels N ≡ 2r (mod 4), which are even. The fixed-cut line language is handled the same way, intersecting with the regular set of lengths ≡ 1 (mod 8). ∎

**On the coordinator's 4-block sketch.** Its conclusion is right, but as stated it has a gap. The slice a*b*a*b* has pieces where the axis lies inside a block, and a stratified decomposition could in principle use periods from those pieces. The fix is the step "c + Np ⊆ E ⇒ f(p) = 0" from positive homogeneity (step 5). It constrains every period at once, whatever piece it comes from. The 3-block slice needs nothing else.

## 4. Searching for a dense CF sublanguage, and the barrier (PROVED parts marked)

**Target size (PROVED reduction).** Let n be odd. Rotation by s moves the central axis to c = n−1+2s, which is a bijection between rotations and axes. So for L ⊆ Φ_{±1}, each necklace ν meets L in ≤ X(ν) words.
- Hence |Cyc(L)_n| ≥ Σ_{w∈L_n} n/X(w).
- Typical X is about 1.13√n.
- So a CF L ⊆ Φ_{±1} with |L_n| ≥ 2^n n^{-1+δ}, concentrated on words with X = O(√n), would refute Q½.
- In other words, a relative density as small as n^{-1/2+δ} inside the fixed-axis line would suffice. Every word of Φ_{±1} is primitive.

**What I tried.** Each candidate failed:
- Regular control on the pair sequence.
- Coupling the agreement bits e_i to the letters themselves. For example, y = x̄-type rules force a letter count to balance, which needs a second counter. The words with all-a tails are exponentially rare.
- Nested "second folds" that pair e_i with e_{h−1−i}. These need a crossing four-position constraint, which is u u^R u u^R-type and not CF.
- Mixing global letter counts with the fold count. The identity A + 3B = |w|_b − [mid = b] (for n odd and R = 1, where A and B count the aa- and bb-pairs) still couples a fold count with a counter.

No CF sublanguage of density ≫ n^{-1/2} was found.

**Proposition B (PROVED: the barrier for fold-shaped CF certificates).** Let D be a regular language over the pair alphabet Σ² (plus a middle letter). Let L = {w : fold(w) ∈ D}; these are exactly the even-linear languages. Suppose L ⊆ ⋃_{R ∈ F} Φ_R for a finite set F, i.e. the fold balance M − m is bounded on L. Then |L_n| ≤ C λ^n 2^n for some λ < 1, and the same holds for |Cyc(L)_n| ≤ n|L_n|.

*Proof.*
1. Take a trim DFA for D. Every cycle that is both reachable and co-reachable has balance 0, since otherwise pumping it would make M − m unbounded.
2. So each strongly connected component carries a potential π with |π| ≤ |Q|. Hence every prefix balance of an accepted word is bounded by K = |Q|(2|Q|+1).
3. For uniform w, the pair letters are i.i.d. and the balance increments are i.i.d. ±1.
4. The probability that a simple random walk stays in [−K, K] for h = ⌊n/2⌋ steps is ≤ C_K cos(π/(2K+2))^h. ∎

This covers builder2's GB (bounded m) and all "regular-control fold" certificates. It overlaps with density.md's FR theorem when L ⊆ Q, but here only bounded balance is assumed.

**Missing barrier (CONJECTURED).** Every CF L ⊆ Φ_{±1} has |L_n| = O(2^n n^{-1}). Equivalently (heuristically), CF subsets of the line hit at most a 1/√n fraction of the line, which would keep Cyc(L) at O(n^{-1/2}). I have no proof for nonlinear grammars. Theorem F rules out only L = Φ_R itself.

## Registry entry
1. **Aim:** decide whether the line certificates (n − 4m_c = R, any axis) contain a CF set of density ≫ n^{-1/2}; this would refute Q½. Alternatively, prove a barrier.
2. **Proved:**
   - G re-verified for all n and both axis types.
   - Lemma I and Theorem U: for odd n the axis-union LU has density ≥ 1 − O(n^{-1/2}), and it is ⊆ Q.
   - Theorem F: Φ_R and F_r are not CF, for every R and r, via a clean 3-block Ginsburg argument.
   - Proposition B: regular-control (even-linear) fold sublanguages are exponentially sparse.
3. **Missing step:** "every CF L ⊆ Φ_{±1} has |L_n| = O(2^n/n), and Cyc(L) has density O(n^{-1/2})". The negative-side form is: every CF subset of LU has density → 0.
4. **Counterexamples:** none to Q½. The coordinator's 4-block sketch has a gap, fixed by the homogeneity step of §3.
5. **Strength:** the missing step is weaker than Q½ (it concerns one certificate family only), so it would not by itself imply "Q not CF". A positive answer (a dense CF L ⊆ LU) would refute Q½ but would not prove Q is CF.
6. **What would reopen the route:**
   - a CF mechanism that tests fold balance using the same stack as the fold, e.g. via nonlinear derivations that re-pair positions;
   - on the negative side, a Theorem-P-style anti-concentration bound for CF subsets of Φ_R.

## 5. Follow-up: is the axis-union U (= LU) context-free? (answer: UNDECIDED; bounded slices give no obstruction)

U is rotation-closed and sound, and has density → 1 (§2). Theorem F does not transfer to U.

Scripts and outputs in `scripts/fold/`:
- `slice4.py`, `slice4b.py`, with output `out_slice4b.txt`;
- `slice4c.py`, with outputs `out_slice4c_K2.txt` and `out_slice4c_K3.txt`.

**Lemma H (PROVED).** m_c ≤ min(|w|_a, |w|_b) for every axis c, since each mismatched pair holds one a and one b. Hence
U ⊆ H := {w : min(|w|_a, |w|_b) ≥ min T(|w|)}, where min T(n) = n/4 − O(1).

**Lemma NC (PROVED): no asymptotic Ginsburg obstruction exists on any slice (a*b*)^K.** The recession region of H on the slice is
{x ∈ R^{2K}_{≥0} : Σ x_a-blocks ≥ |x|/4 and Σ x_b-blocks ≥ |x|/4}. Every point of it is a nonnegative combination of 2-support vectors (one a-block, one b-block, ratio in [1/3, 3]) whose supports are pairwise non-crossing.

*Proof.*
1. Scale the b-masses by r = |x|_a/|x|_b ∈ [1/3, 3], so that the a-mass and the scaled b-mass have equal totals.
2. Cancel an adjacent a-block/b-block pair repeatedly. A sequence with equal totals of two kinds of mass in linear order always has adjacent blocks of opposite letters until it is exhausted.
3. Each cancellation gives an edge between a nonempty a-block and a nonempty b-block, with ratio exactly r.
4. Adjacent cancellation produces a planar (nested) edge family, so the edges are non-crossing. ∎

Consequence for the method. The obstruction used in Theorem F (§3) and in the earlier non-CF proofs needs a region of exponent space whose directions avoid every cone spanned by stratified periods. That obstruction is impossible for U ∩ (a*b*)^K, because U ⊆ H and every recession direction of H is covered. A non-CF proof for U via bounded slices would therefore have to use the lower-dimensional or congruence ("gap") structure. It cannot use the shape of the cone.

**What the gaps look like (COMPUTER-CHECKED).** On a^i b^j a^k b^l, with all (i,j,k,l) for n ≤ 40, and on random samples of 4- and 6-block slices up to n = 960:
- **Interval rule.** The interval rule "min_c m_c ≤ t ≤ max_c m_c for some t ∈ T(n)" agreed with H on every sample.
- **Exact pattern for n ≤ 40.** U equals the interval rule except on 843 words. 575 of these have i = k or j = l, i.e. they are reflection-symmetric or periodic. The other 268 are parity gaps: m_c takes only even values near the target. One example is (4,5,6,7) at n = 22, where the m_c values are {…, 4, 6, 7, …} and 5 is missing.
- **Odd n.** For 4 blocks, U ∩ slice = H ∩ slice in all samples (n = 121, 481). For 6 blocks there is a residue of about 0.3%.
- **Even n.** There is a stable 1–2% gap region. In it, m_c is piecewise linear in c with slopes in {−4, …, 4}, so the gaps are congruence conditions on the block lengths, which are semilinear.

All of this is consistent with U ∩ (every bounded slice) being CF: H minus congruence-defined and lower-dimensional pieces. I did not prove stratification of those pieces.

**Status of the decisive question (CONJECTURED, not proved).**
- U ∩ (a*b*)^K is CF for every K. A bounded-slice certificate of non-CF-ness for U, or for Cyc(Φ_R), would need Ginsburg's theorem applied to thin or congruence pieces.
- Whether U is CF is open. If U is CF, then Q½ is false: U is a density-1 CF subset of Q. If U is not CF, the proof needs an unbounded (non-slice) obstruction.

The same applies to Cyc(Φ_R) for a single R. Its recession region is also H, by Lemma H, and it has density → 1 for odd n (Theorem U).

Registry addendum:
- (2) Lemmas H and NC were added.
- (3) The new missing step is either "U is not CF (unbounded obstruction)" or "U ∩ slice has a non-stratified thin piece".
- (5) "U is CF" is stronger than refuting Q½ and still does not give Q ∈ CF. "U is not CF" is weaker than "Q is not CF" and does not imply it.
