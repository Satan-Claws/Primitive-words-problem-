# audit1: adversarial audit of `uniform.md` and `kk.md`

I wrote independent scripts and did not reuse the audited code. They are in `infinite-ambiguity/claude_round4-5_2026-11-18/scripts/audit1/`:
* `uniform_audit.py` (about 1 min)
* `kk_audit.py` (about 2 min)
* `kk_gap2.py` (under 1 min)

**Outcome.** Every central mathematical claim in both reports **survives**. I found no FALSE theorem.
The gaps are in auxiliary claims and in how far the headlines reach. They are listed below.

---

## Part 1: `uniform.md`

### (a) Lemma 1.1: every non-primitive word of R = a(ab⁺)*a(ab⁺)* is a square. CONFIRMED

**Multiplicativity.** If w = z^k, then w_{(i+1) mod |w|} = z_{(i+1) mod |z|}. So the cyclic `aa`-count of w is
exactly k·c(z). This uses the cyclic, not the linear, count; the report uses the cyclic one.

**Case analysis.** I checked every case, including u = ε, v = ε and both empty:
* w = `aa` has count 2 and equals a², a square. The root `a` has cyclic count 1, because with n = 1 the
  index i+1 wraps onto itself.
* If v ≠ ε, the last letter of w is b, and b→a is not `aa`.
* If v = ε, the second explicit a wraps onto w_0 = a. That occurrence is counted once.

So the count is exactly 2. Then k·c(z) = 2 with k ≥ 2 forces k = 2 and c(z) = 1. ε ∉ R.

**Computer check.** I generated R independently and cross-checked it by brute-force regex up to length 14.
* There are 70 101 words of length ≤ 22 (matches the report). None is non-primitive without being a square.
* The cyclic count equals 2 on all of them.
* Multiplicativity holds on 3000 random z.

### (b) G* generates exactly coPow₂. CONFIRMED
* The proof is classical. A ⇒ Σ^i a Σ^i, and in AB the a sits at offset i in the first half and the b at
  offset i in the second half.
* Brute force: I counted parse trees by dynamic programming over **all** words of length ≤ 14, ε included.
  L(G*) = Σ* ∖ {uu} with 0 mismatches.
* The maximum number of trees on R for lengths 4, 6, …, 22 is 1, 3, 3, 5, 5, 7, 7, 9, 9, 11 (matches the
  report). Length 2 (`aa`) has 0 trees, as it should.

### (c) Proposition 2.1. CONFIRMED
* E(R) is defined through the exponent of the **primitive root**: k with w = z^k, z primitive.
* So a non-primitive w = z^k with d | k gives w = (z^{k/d})^d, which is a d-th power.
* Had E(R) used arbitrary exponents, d | (some exponent) would still be enough. Either way the step holds.
* ε is a d-th power, so it is correctly excluded from coPow_d. If E = ∅, only ε needs removing.

The instances R_p and R_{p^e} are confirmed by the counting argument and by sampling. Exponents seen:
| R_k | exponents seen |
|---|---|
| R_4 | {2, 4} |
| R_8 | {2, 4, 8} |
| R_9 | {3, 9} |
| R_12 | {2, 3, 4, 6, 12} |
| R_p, p = 2, 3, 5 | {p} |

**GAPs, all minor and all outside the Proposition itself:**

* **Corollary 2.2, wording.** "gcd E(R) = 1, so E(R) contains two coprime exponents" is false.
  *Counterexample:* R = (aab)^6 ∪ (aab)^{10} ∪ (aab)^{15} is regular with E(R) = {6, 10, 15}. Its gcd is 1, but no
  two of its elements are coprime. The hedge "or exponents with coprime parts" is undefined.
* **Corollary 2.2, scope.** "Every existence argument … must exploit an interaction between at least two
  distinct prime exponents" is not proved. What is proved is narrower: a proof of the form "Q ∩ R is not CF,
  R regular" needs gcd E(R) = 1. A pumping argument on Q itself has R = Σ*, where gcd E = 1 trivially, so the
  barrier says nothing about it. The general sentence is IDEA, not PROVED.
* **§1 (2), transfer claim.** "|𝓗| ≥ M+1 transfers to any CFG through Ginsburg's stratified decomposition,
  refined by Eilenberg–Schützenberger/Ito … keeps laminarity" is tagged LITERATURE but no exact statement is
  given. In particular the claim that the refinement to independent periods keeps the pieces non-crossing is
  unproved. It is not used later.
* **§3, KK slices.** "With a fixed number of blocks per z_i the slice is a KK slice, CF by LITERATURE for small
  block counts" holds only for those n = Σ(c_i + 1) where KK is actually known. The tag is too broad.

### (d) Lemma 3.1: Q ∩ R6 = R6 ∩ coPow₂ ∩ coPow₃. CONFIRMED
* The cyclic count is 6, so k ∈ {2, 3, 6}, and a 6th power is a square.
* The rewrite as {z₁z₂z₃ ≠ z₄z₅z₆ and ¬(z₁z₂ = z₃z₄ = z₅z₆)} needs a step the report does not write: if
  w = u², then u is a prefix of w beginning with `aa` and ending in b. Hence u ∈ (a(ab⁺)⁺)^3, and the
  factorisation of w is unique because factors start exactly at the occurrences of `aa`. The same holds for
  cubes. With this step the rewrite is valid.
* Exhaustive check over all 6⁶ = 46 656 words built from the 6 factors with ≤ 2 blocks of exponent ≤ 2: the
  three sets coincide. The exponents seen are exactly {2, 3, 6}.

---

## Part 2: `kk.md`

### Ginsburg's theorem and the encoding. CONFIRMED (with one unwritten step)
* **Statement (LITERATURE: Ginsburg 1966, §5.4; Ginsburg–Spanier).** For L ⊆ w₁*⋯w_k*, L is CF iff
  φ⁻¹(L) = {(i₁, …, i_k) : w₁^{i₁}⋯w_k^{i_k} ∈ L} is a finite union of linear sets with stratified period sets.
* **Stratified** means: each period has ≤ 2 nonzero coordinates, and there are no p, p′ and i < j < k < l
  with p_i p_k p′_j p′_l ≠ 0. kk.md uses this definition.
* **Encoding.** With the 2n bounding words a, b, a, b, …, φ⁻¹(Q_n) also contains tuples whose a-exponents are
  not 1 (for example a² b⁰ a⁰ …). The reduction to E_n ⊆ N^n therefore needs one step that the report cites
  (bounded.md L1/L2) but does not write:
  1. Intersect with {a-coordinates = 1}. Only the periods with zero a-coordinates survive.
  2. Delete the a-coordinates. Deleting coordinates preserves non-crossing.
  3. The converse is Ginsburg's "if" direction.
  
  I checked this step and it holds.

### Rotation remark ("Cyc-closure gives nothing new"). GAP (informal)
* Stratification is rotation-invariant: interleaving of chords on a circle is invariant under rotation. That
  part is CONFIRMED.
* But a CF L ⊆ Q containing a conjugate of each primitive word need not have L ∩ (ab*)^n rotation-dense in
  E_n. Conjugates that cut inside a b-block leave (ab*)^n.
* What is actually proved is weaker: if finitely many rotations of stratified subsets of E_n cover E_n, then
  E_n is stratified-coverable.

### §0 one-scale criterion (soundness). CONFIRMED, sketch only
I completed the proof. Pigeonhole for fixed M as N → ∞ gives one piece.
1. Pass to a subsequence where every λ_p/N converges, and let P₁ = {p : lim λ_p/N > 0}. Then h is a strictly
   positive combination of P₁, and real coefficients can be replaced by rational ones because h is rational.
2. Choose M as a common denominator over the finitely many candidate pairs (piece, P₁).
3. Then y − MΣ r_p p = Nh + Mv ∈ V_d, and it stays in the piece because λ_p ≍ N ≫ M r_p.

The proof is correct, but these steps are only sketched in the report.

### Theorem A, Lemmas A1, A2, CRT. CONFIRMED
* **P_c stratified.** The chords split into two nested families, on [0, c] and [c+1, n−1]. Checked by script
  for all n ≤ 40 and all c.
* **span P_c = Sym_c.** Clear.
* **A1.** (⇒) ρ_c preserves V_D. (⇐) δ − v/2 is symmetric. Correct.
* **A2.** Each step checks out:
  * The reindexing is valid because the reflection i ↦ c − i preserves V_D.
  * If v_p(s) < a_p, then g = gcd(s, n) | D: compare v_p, and every other prime is unaffected.
  * z is s-periodic and n-periodic, hence g-periodic, hence D-periodic.
  * Telescoping gives p·z = 0.
* **CRT.** Each p^{a_p} ≥ 2 leaves a residue to avoid.

Computer checks:
| check | scope | failures |
|---|---|---|
| A2 single class + good c exists | exhaustive: n = 4, 6, 8 over {0,1,2}^n; n = 9, 10, 12 over {0,1}^n (13 003 vectors) | 0 |
| same | 1080 random hard vectors in W_n (+ noise), n up to 210 | 0 |

### Corollary A3. CONFIRMED, with two minor wording issues
* The pieces δ⁺ + N P_c are genuinely stratified and lie inside E_n. The proof is: (1 − ρ_c) kills
  Sym_c ∋ const·1, and ρ_c preserves V_D.
* I sampled 4000 points of such pieces for n = 6, 12, 30: all primitive.
* The slab-covering consequence follows: δ = x − min(x)·1 ∈ {0..B}^n, which is a finite set.
* "Contains all of N·1 + δ" holds only for its nonnegative members, and only if const is chosen minimal.
* "Covered at level B iff …" uses an undefined notion. Only the "if" direction is shown (pair off
  min(x_i, x_{c−i})).

### Theorem B. CONFIRMED as stated; GAP in what the report concludes from it
* What is proved is exactly this: **the §0 criterion (rational-span version, h ∈ Z_{>0}^n) never holds.**
  * P_{c,h} is stratified because it has the same supports as P_c.
  * span P_{c,h} = diag(h)·Sym_c.
  * diag(h)^{±1} preserves V_d for d ∈ D_h.
  * δ ∉ V_{n/p} ⇔ h⁻¹δ ∉ V_{n/p} for p ∈ 𝒫.
  * Non-maximal d ∈ D_h are handled, because V_d ⊆ V_{n/p} and n/p ∈ D_h.
* **GAP.** The abstract says "the obstruction is defeated by an explicit, uniform family of stratified
  structures", and the registry says "cannot prove non-CF of any Q_n". For h ≠ 1, however, **no covering pieces
  inside E_n are produced**. Escaping V_d for d ∈ D_h at the level of spans says nothing about V_d with
  d ∉ D_h at bounded scales.
* **Counterexample to the naive covering** (`kk_audit.py`): n = 6, h = (1,2,1,2,1,2), δ = (0,0,0,0,1,0).
  * c = 5 is a good axis in the sense of Theorem B.
  * But δ + 1·(h₁e₁ + h₄e₄) = (0,2,0,0,2,0) ∈ V₃, which is non-primitive.
  * So δ + N P_{5,h} ⊄ E₆.
* For n = 6 some pair (c, shift K) always gives a clean piece (`kk_gap2.py`, all 720 admissible δ ∈ {0,1,2}⁶).
  This is expected, since Q₆ is CF. But no general argument for it is given.
* So "every one-scale obstruction fails" means only "the §0 criterion fails". A sharpened one-scale argument
  that also uses V_d with d ∉ D_h, or integrality, is not excluded for h ≠ 1. For h = 1, Corollary A3 does
  give a genuine covering.
* h with zero entries is untreated; the report acknowledges this.

---

## Verdict table
| Claim | Verdict |
|---|---|
| uniform (a) Lemma 1.1 | CONFIRMED |
| uniform (b) L(G*) = coPow₂ | CONFIRMED |
| uniform (c) Prop 2.1 | CONFIRMED; Cor 2.2 "two coprime exponents" FALSE as worded (E = {6,10,15}); general barrier sentence is IDEA |
| uniform (d) Lemma 3.1 | CONFIRMED (unique-factorisation step unwritten but true) |
| uniform §1(2) Ginsburg/ES/Ito transfer | GAP (unsupported LITERATURE) |
| kk Ginsburg criterion and encoding | CONFIRMED (projection step cited, not written) |
| kk rotation remark | GAP (informal) |
| kk A1, A2, Theorem A, CRT | CONFIRMED |
| kk Cor A3 | CONFIRMED (minor wording) |
| kk Theorem B | CONFIRMED as "§0 criterion never holds"; GAP for the stronger "defeated / no one-scale obstruction" reading when h ≠ 1 (naive pieces leave E_n; explicit example) |

## Registry entry
1. **Aimed at:** refuting claims in `uniform.md` and `kk.md`.
2. **Proved:** all core lemmas confirmed. Gaps are located above.
3. **Missing steps** (for the audited authors):
   * kk: for every n and every h > 0, a finite stratified covering inside E_n of {Nh + Mδ : N ≫ M}. This is
     needed to justify "no one-scale obstruction" beyond the §0 criterion.
   * uniform: an exact citation for the laminarity-preserving refinement.
4. **Counterexamples:**
   * E = {6, 10, 15} (Corollary 2.2 wording).
   * (n=6, h=(1,2,1,2,1,2), δ=e₄, c=5): the naive weighted-reflection piece leaves E₆.
5. **Relation to "Q not CF":** not applicable (this is an audit).
6. **What would reopen:** not applicable.
7. **No proof of either resolution is claimed.**
