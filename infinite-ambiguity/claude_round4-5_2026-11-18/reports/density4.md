# density4: density obstructions for arbitrary CFLs

Agent "density4", round 4. Scripts: `infinite-ambiguity/claude_round4-5_2026-11-18/scripts/density4/checks.py` (one core, about 1 minute).

**Bottom line.** No proof of either resolution is claimed. This report gives:
- one new barrier theorem, Theorem P (PROVED);
- one small equivalence, Proposition C (PROVED);
- explicit counterexamples to the natural "dense CFLs contain ideal-like sets" lemmas, at every Parikh level (PROVED, and partly already in the literature);
- a literature correction: the strong "density ⇒ powers" claim for DCFL was already refuted (Koga 2022);
- a precise open question, (Q½), that would settle the problem negatively.

Notation:
- Σ = {a,b}, L_n = L ∩ Σ^n, Δ(w) = |w|_a − |w|_b.
- V_k(w) ∈ N^{Σ^k} is the vector of *cyclic* k-gram counts (positions i ∈ Z_n, factor w_i…w_{i+k−1} read cyclically).

## 0. Literature (LITERATURE, exact statements, checked in the PDF of Koga's paper)

- **Sin'ya, SOFSEM 2021, "Asymptotic approximation by regular languages".** Let R be regular with D*(R) > 0, where D* is the Cesàro density. Then there are z ∈ Σ^+ and p ≥ 1 with z^{pn+1} ∈ R for all n ≥ 0.
- **Sin'ya, EPTCS 193 (2015).** A regular R has lim D_n(R) = 0 iff Σ* s Σ* ∩ R = ∅ for some s.
- **Koga, Acta Cybernetica 25 (2022) 717–731, "Dense languages and non primitive words".**
  - Here "dense" means *every* word occurs as a factor of some word of L. This is not asymptotic density.
  - Main Thm 2.3: every dense L in the regular closure Γ(TL) of the thin languages satisfies ∀u,v ∃z ∈ Σ*vΣ* ∃p ∀n: (zu)^{pn}z ∈ L.
  - Sec. 1.2 states that "Claim 1.1" is FALSE: a density-1 CFL need not contain a regular sublanguage of positive density. The counterexample is L = {v : |v|_a ≤ 2|v|_b} (Sin'ya [16, Thm 14] and his OWLS slides).
  - Sec. 6.2: R = {v⟩ : v ∈ Dyck} is DCF, dense in the factor sense, and contained in Q. So "factor-dense CFL ⇒ powers" fails already for DCFL. This R has asymptotic density Θ(n^{-3/2}) up to parity; it is the analogue of our E′.
- **Consequence for this campaign.** The direction "density 1 (or positive) ⇒ non-primitive words" for CFLs is explicitly open in the literature, and it is noted there as implying the Dömösi–Horváth–Ito conjecture. No one has a counterexample, i.e. a CF L ⊆ Q of positive density.

## 1. Proposition C: positive density is equivalent to hitting a positive fraction of conjugacy classes (PROVED)

**Proposition C.** For c ∈ (0,1], the following are equivalent:
- (a) there is a CFL L ⊆ Q with |L_n| ≥ c·2^n for all large n in an infinite set S of lengths;
- (b) there is a CFL L′ ⊆ Q that meets at least c·2^n/n primitive conjugacy classes of length n, for all large n ∈ S.

*Proof.*
1. Each primitive class of length n has exactly n elements.
2. (a) ⇒ (b): L meets at least |L_n|/n ≥ c2^n/n classes.
3. (b) ⇒ (a): Cyc(L′) is CF (LITERATURE: CFLs are closed under cyclic shift; Maslov 1973, Oshiba 1972).
4. Cyc(L′) ⊆ Q, because Q is closed under conjugation.
5. |Cyc(L′)_n| = n·#(classes met) ≥ c·2^n. ∎

So "is there a positive-density CF L ⊆ Q?" is the same question as "is there a CF set of primitive-certified representatives for a positive fraction of the necklaces?". The same holds with c → 1, which is devil.md's criterion in density form. In particular one may assume L is closed under conjugation.

## 2. Theorem P: count certificates give density O(n^{-1/2}) (PROVED)

**Class CS_k.** These are the languages L = {w ∈ Σ^+ : V_k(w) ∈ S} with S ⊆ N^{Σ^k} semilinear.
- Examples: E′ = {Δ = −1} (k = 1); every one-counter "statistic = const" certificate with bounded-window increments, read cyclically.
- Every such L is closed under conjugation. L need not be CF; the theorem holds for all of them.
- Remark P.4 below covers linear (non-cyclic) counts with boundary data.

**Theorem P.** If L ∈ CS_k contains no word s^q with q ≥ 2 (for example, if L ⊆ Q), then |L_n| ≤ C_L·2^n·n^{-1/2} for all n ≥ 1.

Hence E′ (|E′_n| ~ 2^n√(2/(πn)) for odd n) is optimal up to a constant in this class. Together with density.md's Theorem 2 (FR ⊆ Q ⇒ exponentially small density), neither known mechanism can produce a CF L ⊆ Q of density ≫ n^{-1/2}.

*Setup.*
- Let G_k be the de Bruijn graph: vertices Σ^{k−1}, edges Σ^k (for k = 1, one vertex with two loops).
- Let E ⊆ R^{Σ^k} be its flow space (balanced vectors). Then dim E = e := 2^{k−1}+1, and V_k(w) ∈ E ∩ N^{Σ^k}.
- The lattice Λ_E = E ∩ Z^{Σ^k} is spanned by directed-cycle vectors (nonnegative balanced integer vectors decompose into cycles, and the all-ones vector is in E, so E ∩ R_{≥0} spans E).
- E ∩ N^K is semilinear (Hilbert basis), and semilinear sets are closed under ∩ (Ginsburg–Spanier, LITERATURE). So WLOG S = ⋃ M_j with M_j = c + N p_1 + … + N p_r and c, p_i ∈ E ∩ N^K.

*Step (i): a linear set M of full rank e contains V_k(s^q) for some s and prime q, so L contains s^q.*
1. ZΛ := Σ Z p_i has finite index I in Λ_E. Pick a prime q ∤ I.
2. Then ZΛ + qΛ_E = Λ_E. The quotient Λ_E/(ZΛ + qΛ_E) is killed both by I and by q.
3. So there are z_i ∈ Z with c + Σ z_i p_i ∈ qΛ_E.
4. Put n_i = z_i + qT with T large. Then P = c + Σ n_i p_i ∈ M and P = q·v, with v = (c + Σz_ip_i)/q + TΣp_i.
5. Σp_i has full support, since span(p_i) = E contains the all-ones vector. So v > 0 coordinatewise for T large.
6. A positive balanced v on the strongly connected graph G_k has an Eulerian circuit. This gives a cyclic word s with V_k(s) = v.
7. V_k(s^q) = qv = P ∈ M ⊆ S, so s^q ∈ L, which contradicts the hypothesis. Hence every M_j has rank < e.

*Step (ii): a linear set of rank < e contributes O(2^n n^{-1/2}).*
1. Choose an integer functional ℓ with ℓ|_{span M−c} = 0 and ℓ|_E ≠ 0. Then ℓ(V_k(w)) = ℓ(c) for every w with V_k(w) ∈ M.
2. If ℓ|_E = λΣ|_E, then Σp_i = 0 forces p_i = 0, so M = {c} is finite.
3. Otherwise apply Lemma AC.

**Lemma AC (anti-concentration, PROVED).** If ℓ|_E is not a multiple of Σ|_E, then sup_t #{w ∈ Σ^n : ℓ(V_k(w)) = t} ≤ C·2^n n^{-1/2}.

*Proof.*
1. *Switch pair.* For a word y with |y| ≥ k−1, let f(y) = ℓ(linear k-gram counts of y). This is additive under gluing along a common (k−1)-window, i.e. along paths of G_k.
2. Suppose f(y) depended only on (prefix_{k−1}, suffix_{k−1}, |y|) for all y. Then the value on closed walks at vertex u of length L would be additive in L for L ≥ L_0. Hence it equals λ_u·L, by Cauchy's equation on [L_0, ∞): L_0 g(L) = g(L·L_0) = L g(L_0).
3. λ_u is the same for all u, because a closed walk through u and v gives the same multiset of edges from either base point.
4. Every cyclic s satisfies ℓ(V_k(s)) = λ|s|, via s^{L_0}. So ℓ = λΣ on E, a contradiction.
5. Hence there are y_1, y_2 of equal length m ≥ k, with equal (k−1)-prefix and equal (k−1)-suffix, and f(y_1) ≠ f(y_2).
6. *Littlewood–Offord.* Cut [0,n) into ⌊n/m⌋ disjoint blocks of length m. Let J be the set of blocks equal to y_1 or y_2.
7. Swapping y_1 ↔ y_2 inside a block changes V_k by exactly N(y_2) − N(y_1). This is because the k-grams that straddle a block boundary, including the cyclic wrap, see only the shared (k−1)-boundaries.
8. Conditioned on J and on everything outside J, ℓ(V_k(w)) = const + δ·Bin(|J|, 1/2) with δ ≠ 0. The probability of any single value is ≤ C/√(|J|+1).
9. |J| ~ Bin(⌊n/m⌋, 2^{1−m}) is at least a positive constant times n, except with exponentially small probability (Chernoff). ∎

Summing over the finitely many M_j proves Theorem P. ∎

**Remark P.4 (PROVED in outline).** Let L = {w : linear k-gram counts ∈ S}, or more generally ⋃_{α,β} (αΣ* ∩ Σ*β ∩ V_k^{-1}(S_{αβ})).
- Step (ii) is unchanged: the boundary terms take finitely many values.
- In step (i), choose v = v′ + χ(PP′), where P is the path of G_k spelling βα and P′ is a fixed return path. Splice the closed walk PP′ into an Eulerian circuit of v′ and cut the circuit between β and α. This gives s ∈ αΣ* ∩ Σ*β with V_k(s) = v, and s^q has the same boundary words.

COMPUTER-CHECKED (`checks.py`):
- (b) sup_t P(ℓV_k = t)·√n is stable for n = 20…160 for four non-degenerate ℓ (k = 1,2,3). The degenerate cyclic #ab − #ba is identically 0, as predicted.
- (c) 149 random full-rank linear sets for k ∈ {1,2}: the construction of step (i) produced s with V_k(s^q) ∈ M every time.
- (a) E′ and the conjugation-closed CF language U = Cyc{b·x·a : x a Dyck word} have 0 non-primitive words for n ≤ 16, with |·|/2^n·√n ≈ 0.76 and 0.42 respectively.

## 3. "Dense CFL ⊇ ideal-like set" lemmas are false at every Parikh level (PROVED)

These would have been the natural bridge from "dense" to "contains u^k". Sin'ya's L = {|v|_a ≤ 2|v|_b} already refutes the regular-sublanguage version. Sharper:

1. **L0 = {w : Δ(w) ∉ {0,1}}.**
   - It is deterministic one-counter and has density → 1 (P(Δ ∈ {0,1}) = O(n^{-1/2})).
   - For all x, z ∈ Σ* and D ≥ 1 there is t with D | |t| and xtz ∉ L0: take |t| = Dj ≥ |xz|+1 and pick Δ(t) of the right parity so that Δ(xtz) ∈ {0,1}.
   - So L0 contains no x(Σ^D)*z.
2. **L1 = {w : Δ(w) ∉ {0,1}, the walk of w does not end at its max, and does not end at its min}.**
   - Its reversal is accepted by a deterministic one-counter automaton with two flags, so L1 is DCF.
   - Its complement has density O(n^{-1/2}).
   - It does contain x{t : Δ(t) ≥ c}z when z has suffixes of both signs. So it does *not* refute the half-plane version; this is recorded honestly.
3. **L5 = {w : F(w) ∉ {0,1,2,3}} with F = |w|_a − 4|w|_{aa}.** This kills cone and half-plane versions.
   - It is DCF: a one-counter with a one-letter memory.
   - Its density → 1, exponentially fast, because E F ≈ −n/2.
   - *Claim (PROVED).* For all x, z, all A ≥ 3|xz|+3 and all B ≥ A+1, some t with Parikh vector (A,B) has xtz ∉ L5.
   - Witness: t = b a^{j+1} (ba)^{A−j−1} b^{B−A+j}, with j = ⌊(A + F(x) + F(z))/4⌋. This t starts and ends with b, so F(xtz) = F(x) + F(z) + A − 4j ∈ [0,3].
   - Consequently L5 contains no x·T·z with T ⊇ {one word for each Parikh vector in an open cone around the diagonal (1,1) at lengths ≡ 0 mod D}.
   - COMPUTER-CHECKED for |x|,|z| ≤ 2 and 4 × 4 values of (A,B): 784 cases, 0 failures.
   - The same trick with a (k+1)-gram statistic defeats any version phrased with k-gram-count cones.

**Lesson.** Any true "structure in dense CFLs" lemma must allow the inner language T to be cut by arbitrary order-insensitive CF statistics. The form that would still suffice for Q is:

- **(K\*) CONJECTURED.** If L is CF with lim inf |L_n|/2^n > 0, then there are x, z, k, D and a linear set c + Λ ⊆ E of full rank e such that x{t : D | |t|, V_k(t) ∈ c+Λ}z ⊆ L.
- (K\*) ⇒ Q not CF, by the argument of Theorem P(i) with the boundary handling of P.4 and q ∤ D.
- (K\*) holds for regular languages: Sin'ya; density 1 ⇒ L ⊇ xΣ*.
- (K\*) is untested beyond the examples above. L5 satisfies it with k = 2.

## 4. What was attempted towards "CF L ⊆ Q ⇒ lim inf density < 1"

- **Single-length substitution arguments are dead.** A typical word has a node A with yield in [n/3, 2n/3]. Pigeonhole gives a rectangle C×L(A)_j ⊆ L of size ≥ 2^n/poly(n). But Q_n is a union of 2⌈n/3⌉ rectangles (rectangles.md).
- **Forcing a square by substitution needs too much.** Forcing x y′ z = ss needs y′ = t z x t ∈ L(A). That set has relative density 2^{-|y|/2} in L(A)_{|y|}, which density alone cannot force.
- **Mismatch certificates (the coPow_p mechanism) are hopeless for Q.** A mismatch at distance d excludes exactly the periods dividing d. Excluding all maximal periods n/p of n needs ω(n) mismatches. Fixed-ratio distances each handle one prime.
- **"Unique longest run" certificates are not CF.** These would give positive density. The bounded slice {a^i b a^j b a^k : i > j, i > k} has the non-stratified Parikh set (t+1,t,t), so it is not CF.
- **Cycle-lemma reduction.** w with Δ(w) = D ≥ 1 is primitive iff the cyclic sequence of its D first-passage excursions is primitive (PROVED, standard cycle lemma). This only moves the problem to an infinite alphabet.

## 5. Precise open question

**(Q½).** Is |L_n| = O(2^n n^{-1/2}) for every CFL L ⊆ Q?
- YES ⇒ Q is not CF, since |Q_n| ~ 2^n. It is strictly stronger than DHI.
- Known: YES for FR (exponentially small), for CS_k (Theorem P), and for unions of these.
- No CF L ⊆ Q with density ≫ n^{-1/2} is known. By Proposition C, one would need CF representatives of a ≫ n^{-1/2} fraction of necklaces with built-in primitivity certificates.

## Registry entry

1. **Exact statement aimed at:** every CFL L with lim inf (or lim) |L_n|/2^n > 0 (or = 1) contains a non-primitive word. This would give Q ∉ CF.
2. **Strongest lemma proved:**
   - Theorem P: every L ∈ CS_k (cyclic or linear k-gram counts in a semilinear set, any k) containing no proper power has |L_n| = O(2^n n^{-1/2}); this is sharp, attained by E′.
   - Proposition C: density of CF subsets of Q is equivalent to the fraction of necklaces hit by CF subsets of Q.
   - L0 and L5 are explicit DCF density-1 languages refuting the "x(Σ^D)*z ⊆ L" and "Parikh-cone ideal" lemmas.
3. **Missing step:** (K\*) of Sec. 3, or (Q½) of Sec. 5, for arbitrary CFGs.
4. **Counterexamples found:**
   - L0 and L5 against the ideal/cone lemmas (Sin'ya and Koga have analogous ones).
   - No counterexample to the target. No CF L ⊆ Q of density ≫ n^{-1/2} was found.
5. **Strength of the missing step:** both (K\*) and (Q½) are STRONGER than "Q not CF". The density-1 version of the target is also stronger. It is equivalent only if Q's own CF-ness is the sole obstruction, which is not known.
6. **What would reopen or kill the route:**
   - Kill: a CF L ⊆ Q with lim sup density > 0. By Prop. C it suffices to have CF primitive-certified representatives of a positive fraction of necklaces.
   - Reopen: a proof of (K\*) for linear or finite-index CFLs, extending density.md's Problem 6.2. Or a version of Theorem P for languages combining one-counter statistics with an FR shell (regular ∩ CS_k was not done; IDEA).

## Sources
- [Koga, Dense Languages and Non Primitive Words, Acta Cybernetica 25 (2022)](https://cyber.bibl.u-szeged.hu/index.php/actcybern/article/view/4253/4058)
- [Sin'ya, zero-one law for regular languages (arXiv 1505.03343)](https://arxiv.org/abs/1505.03343v3)
