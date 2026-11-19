# Round 2, Route J: unbordered words and sound transversal supersets

**Verdict.**
1. **UB (unbordered words over {a,b}) is NOT context-free.** There is a short, fully rigorous Ogden proof on the slice UB ∩ (a⁺b)⁴. I checked it by exhaustive simulation of every Ogden decomposition for p ≤ 4.
2. The same proof kills a whole family of sound transversals: Q ∩ {no border of length ≤ f(n)} for every non-decreasing unbounded f, and the bounded-rotation closures rot_{≤c}(UB). For bounded f the problem becomes *equivalent* to the main problem. This gives a sharp dichotomy (Thm 3).
3. **The proof does not transfer to Q.** I prove a barrier, Thm 5: Q ∩ (a⁺b)^r satisfies the conclusion of Ogden's lemma for every fixed r. The exact reason is that 3 of the 4 decomposition classes in the UB proof are killed by *primitive* bordered words (a half-space {x₁ ≤ x₄}), and a half-space has no analogue in Q's complement.

Code is in `/tmp/claude-5714/-home-shobhit--claude-spares-spare-fauO4P/6f48459d-5790-4a18-bccc-eabb8efc4544/scratchpad/r2_ub/`: `lib.py`, `verify_formula.py`, `ogden_proof_check.py`, `check_variants.py`, `transversals.py` (output in `out_transversals.txt`), the search scripts `seg.py`, `ogden3.py`, `ogden5.py`, `ogden_gen.py`, `rotations.py`, and the grammar `qslice4.txt`.

Background used:
- **Maslov 1973 / Oshiba 1972.** If L is CF then cyc(L) = {vu : uv ∈ L} is CF.
- **Ogden's lemma.** For CF L there is p such that every z ∈ L with ≥ p marked positions factors as z = uvwxy with (i) vx containing ≥ 1 marked position, (ii) vwx containing ≤ p marked positions, (iii) uvⁱwxⁱy ∈ L for all i ≥ 0.
- **Berstel–Boasson** (Lyndon words are not CF), as background only.

---

## 0. Preliminaries

**Lemma 0.1 (UB is a sound transversal).** Unbordered ⇒ primitive, since u^k with k ≥ 2 has border u. Every Lyndon word is unbordered, so UB meets every primitive class. Hence UB CF ⇒ Q = cyc(UB) CF.

**Lemma 0.2 ("no short border" = UB).** Every bordered word w has a border of length ≤ |w|/2.
*Proof.* Let u be the shortest border, and suppose |u| > n/2. Then q = n − |u| < |u| is a period of w, hence of u. So u has the border u[1..|u|−q], of length 2|u| − n > 0. A border of a border is a border of w, and this one is shorter than u, a contradiction. ∎
So NSB := {no border of length ≤ n/2} = UB. Brute force confirms this for n ≤ 16.

**Lemma 0.3 (border formula on (a⁺b)^r).** For w = a^{x₁}b a^{x₂}b ⋯ a^{x_r}b (all x_i ≥ 1), put X = (x₂,…,x_r). Then

  w ∈ UB ⇔ x₁ > X[|X| − β] for every border β of the sequence X (0 ≤ β < |X|, including β = 0).

*Proof.* A border starts with a and ends with b, so it is a^{x₁}b a^{x₂}b ⋯ a^{x_s}b for some s < r. It is a suffix iff (x₂..x_s) = (x_{r−s+2}..x_r) and x₁ ≤ x_{r−s+1}. ∎
Checked by brute force on 5460 tuples (`verify_formula.py`, 0 mismatches).

For r = 4 this gives

  **L₄ := UB ∩ (a⁺b)⁴ = { x₁ > x₄ ∧ (x₂ ≠ x₄ ∨ x₁ > x₃) }**

(β = 2 collapses). Checked on all x_i ≤ 12, 0 mismatches.

---

## 1. Theorem 1: UB is not context-free

Since (a⁺b)⁴ is regular, it suffices to show that L₄ is not CF. Suppose it is, with Ogden constant p. Let D = p! and

  z = a^{p+1} b a^{p+D} b a^{p+1+D} b a^{p} b

and mark the p+1 letters of the first run.

**z ∈ L₄.** x₁ = p+1 > p = x₄, and x₂ = p+D ≠ p = x₄.

**Every Ogden decomposition fails.** Let z = uvwxy satisfy (i) and (ii).

- **v or x contains a b.** Then uv²wx²y has more than 4 b's, so it is not in (a⁺b)⁴. Done.
- **Otherwise v = a^α and x = a^β, each inside one run.** Since vx contains a marked letter and v precedes x, v lies in run 1; if v = ε, then x lies in run 1. By (ii), α ≤ p.
  - **(a) v, x both in run 1, or one of them empty.** Run 1 changes by δ = α + β ∈ [1, p]. For i = 0, x₁′ = p+1−δ ≤ p = x₄, so x₁ > x₄ fails (the border is a^{x₁′}b).
  - **(b) α ≥ 1, x inside run 2 or run 3.** For i = 0, x₁′ = p+1−α ≤ p = x₄, which fails. If x was the whole run, a run vanishes and the word leaves (a⁺b)⁴.
  - **(c) α ≥ 1, x = a^β inside run 4, β ≥ 1.**
    - α > β: for i = 0, x₁′ = p+1−α ≤ p−β = x₄′. Here x₄′ ≥ 1, because β < α ≤ p.
    - α < β: for i = 2, x₁′ = p+1+α ≤ p+β = x₄′.
    - α = β: for i = 1 + D/α (an integer, since α ≤ p), x₁′ = p+1+D = x₃ and x₄′ = p+D = x₂. Then x₂ = x₄ and x₁ ≤ x₃, so the pumped word is not in L₄. In fact it is (a^{p+1+D}b a^{p+D}b)², a square.

Every case yields a pumped word outside L₄, which contradicts Ogden's lemma. So **L₄ is not CF, and hence UB is not CF.** ∎

**Verification.** `ogden_proof_check.py` enumerates every factorization uvwxy of z that satisfies (i) and (ii) under this marking, for p = 1..4 (up to 215,105 decompositions at p = 4). It finds 0 decompositions that survive all i ∈ {0, 2, …, p!+1}.

**Notes.**
- The plain pumping lemma does **not** suffice on any slice I tried. Exhaustive and random searches over run and segment models (`robust*.py`, `seg.py`) found no unbordered z that is robust to all single-run pumps once ≥ 3 runs are variable. Even with R = Σ*, every unbordered word of length ≤ 16 has one letter whose pumping (all i) keeps it unbordered (`strpump.py`, `safe.py`). Ogden is essential: marking only run 1 removes the "lone middle run" pumps.
- The search harness was validated on known cases. It finds the Berstel–Boasson-type witness a^N b^N a^N b^{N+k} for Lyndon words, and a witness for the bordered words. The bordered words are also not CF, by classical pumping on (ab⁺)⁴ with z = (N, 2N, N, 2N).
- This proof is a direct analogue of Berstel–Boasson for Lyndon words. It is probably folklore; I reconstructed it here line by line.

**Anatomy (important for §3).** Classes (a), (b) and (c) with α ≠ β pump into **primitive** words with a **short** border a^{x₁′}b, of length ≤ 2p+2. Only class (c) with α = β needs the factorial trick, and it lands on a **square**.

---

## 2. Weaker sound transversal supersets

Notation: P_f := {w : w has no border of length ≤ f(|w|)}; per(w) is the minimal period. Each entry is "sound?" (P ⊆ Q), then "meets every class?", then "CF?".

### Table (counts are unsound words / missed primitive classes, all lengths n ≤ 18; `out_transversals.txt`)

| P | n=12 | n=14 | n=16 | n=18 | sound | meets all | CF? |
|---|---|---|---|---|---|---|---|
| UB | 0/0 | 0/0 | 0/0 | 0/0 | yes | yes | **no** (Thm 1) |
| NSB (no border ≤ n/2) | 0/0 | 0/0 | 0/0 | 0/0 | = UB (Lemma 0.2) | yes | no |
| Q ∩ P_f, f ↑ ∞ | – | – | – | – | yes | yes (⊇ UB) | **no** (Thm 2) |
| Q ∩ P_c, c constant (data: c=2) | 0/0 | 0/0 | 0/0 | 0/0 | yes | yes | **⇔ Q is CF** (Thm 3) |
| P_half = {per(w) > n/2} | 0/0 | 0/0 | 0/0 | 0/0 | yes | yes | open; P_half CF ⇒ Q CF |
| rot_{≤c}(UB) (data: c=2) | 0/0 | 0/0 | 0/0 | 0/0 | yes | yes | **no** (Thm 4) |
| unique longest a-run at front (or b-version) | 0/22 | 0/75 | 0/267 | 0/979 | yes | no | no (E, Lemma 3) |
| unique lex-max cyclic k-factor, k=5 | 0/54 | 0/229 | 0/921 | 0/3656 | yes | no | regular |
| same, k=3 | 0/189 | 0/723 | 0/2734 | 0/10320 | yes | no | regular |
| gcd(\|w\|_a, \|w\|_b) = 1 | 0/201 | 0/821 | 0/2032 | 0/10042 | yes | no | no (Parikh image not semilinear) |

### Theorem 2 (sound transversals with "no short border" are not CF)
Let f be non-decreasing and unbounded. Then Q ∩ P_f is not CF. The same holds for P_f* := {w : every border has length in (f(n), n/2)}, which is ⊆ Q.

*Proof.* Use the z of Thm 1 with D = K·p!, choosing K so that f(K·p!) ≥ 2p+2. Then z ∈ UB, so z is in both sets. In the case analysis:
- Classes (a), (b) and (c) with α ≠ β produce words with a border a^{x₁′}b of length ≤ 2p+2. Every pumped word keeps a run of length ≥ D, so its length is n′ ≥ D and f(n′) ≥ 2p+2. Such a word therefore has a border of length ≤ f(n′), so it is excluded.
- Class (c) with α = β produces a square. A square is not in Q and has a border of length n′/2.
- The remaining decompositions leave the slice.

Simulated for p ≤ 4 (`check_variants.py`): every decomposition is killed by a word that is out of R, non-primitive, or has a border ≤ 2p+2. ∎

### Theorem 3 (dichotomy)
- If f is bounded (f ≤ c), then P_c is regular: it only compares the first ≤ c and last ≤ c letters. Also Q ∩ P_c ⊇ UB meets every class. So **Q ∩ P_c is CF ⇔ Q is CF**: one direction is ∩ regular, the other is cyclic shift.
- If f is unbounded, Q ∩ P_f is not CF (Thm 2).

So sound transversals that forbid short borders are non-CF exactly when "short" means unboundedly long. The ≤ 2p+2 border created by pumping is the precise obstruction. A border of constant length is a regular condition, and the problem then becomes the original one.

### Theorem 4 ("UB up to padding": bounded rotations)
P_pad := {rot_j(w) : w ∈ UB, 0 ≤ j ≤ c} is sound and meets every class, but it is not CF.

*Proof.* Use the uniform morphism φ(a) = a^{c+2}b a b^{c+1}, φ(b) = a^{c+2}b b b^{c+1}. Both images have length 2c+5. Block starts are the only occurrences of a^{c+2}b, and both images end with b^{c+1}.
- **φ preserves UB both ways.** A border of φ(w) must start at an occurrence of a^{c+2}b, so it is block-aligned and decodes to a border of w.
- **If w = uxu is bordered, every inverse rotation of φ(w) by 1 ≤ j ≤ c is bordered.** Write φ(u) = πs with |s| = j. The rotated word is sπ s φ(x) π, and since φ(x) also ends with s = b^j, it has the border sπ.

Hence φ⁻¹(P_pad) = UB. Inverse morphisms preserve CF, so P_pad CF would make UB CF. Checked for c = 1, 2, 3 on all |w| ≤ 10 (0 mismatches). ∎

### P_half = {per(w) > n/2}: the thin-complement case (open)
- P_half is sound and contains UB. Its complement in Σⁿ has Θ(2^{n/2}) words, the same order as Q's complement.
- The proof of Thm 1 fails on it: the short-border words a^{x₁′}b… have no long border, so they lie in P_half.
- In the slice (a⁺b)⁴, P_half ∩ R = R \ ({x₁ = x₃, x₂ = x₄} ∪ {x₂ = x₃ = x₄ ≥ x₁}), which is a codim-2 complement and looks CF. On (a⁺b)³ it is {x₂ ≠ x₃} ∪ {x₁ > x₂}, which is CF.
- Ogden-marking searches (`ogden_gen.py PHALF`, about 26,000 run-slice candidates with up to 9 runs, values clustered so that equalities occur) found **0** witnesses. The same harness finds UB witnesses readily (13 hits in 1123).
- So P_half sits with Q, not with UB. P_half CF ⇒ Q CF; the converse is unknown.

### Rotation-invariant witnesses, and "unique largest factor of fixed shape"
- **Rotation-closed P.** If P is rotation-closed, "meets every class" forces P = Q. Any invariant built from cyclic m-gram counts with bounded m fails on a 2-parameter family. For K ≠ K′, K + K′ = 2L and m ≤ min(K, K′)+1, the primitive word a^K b a^{K′} b and the square (a^L b)² have identical cyclic m-gram multisets, so the invariant cannot separate them. This is E's Lemma 6, and the gcd row of the table is an instance.
- **Linear normal forms of a unique maximal feature.** For an unbounded feature such as the longest a-run, the condition is a one-vs-many comparison and is not CF (E, Lemma 3). For a bounded feature (a fixed-length lex-max factor), the set is regular but misses near-power classes; the first misses are aabaabab and ababbabb (UL, n = 8), and aabbbbbb (k = 5).
- **Common failure.** Every bounded-description witness is repeated in near-powers u^k v. The only sound sets that meet all classes are "global" ones (UB, P_f∩Q, P_half). The first two are non-CF by Thms 1–2.

### Refinement that does NOT follow: arbitrary transversals avoiding short borders
Thm 2 is about the specific set Q ∩ P_f, not about every CF transversal contained in it. A transversal may pick a different rotation of z's class. `rotations.py` (p = 2, 3) shows the obstacle: of the short-border-free rotations of z, only rotation 0 admits a killing Ogden marking. For example, the rotation a^{p+D} b a^{p+1+D} b a^p b a^{p+1} b lies deep inside UB (x₁ − x₄ = D − 1).

The precise open lemma is: *every CF P ⊆ Q meeting all classes contains words with a border of length ≤ f(n), for every f ↑ ∞.* It sits strictly between Thm 2 and "Q is not CF". It would need a z-family all of whose short-border-free rotations are Ogden-tight; I found none.

---

## 3. Does the technique transfer to Q? No, and here is why

**Mechanism of Thm 1.** On the slice, the complement of UB contains the **half-space** H = {x₁ ≤ x₄} of primitive bordered words. For a 2-run pump direction (α, β) on runs (1, 4), H is reached by i = 0 whenever α > β and by i = 2 whenever α < β, with no arithmetic needed. Only the single ratio 1:1 needs an exact hit (factorial trick) on the codim-2 square subspace.

For Q, the complement of Q ∩ (a⁺b)^r is ⋃_{d | r, d < r} V_d, where V_d is the set of d-periodic vectors. These are subspaces of codim r − d ≥ r/2, and contain no half-spaces.

**Lemma 5.1 (direction lemma; rigorous).** Let z = ∏ a^{x_i}b be primitive, let m ≠ j, and assume j ≢ m ± r/2 (mod r). Each V_d kills at most one ratio α:β, where "δ = αe_m + βe_j is killed" means X + tδ ∈ V_d for some integer t.

*Proof.* A vector of V_d supported on {m, j} is constant on the orbit m + dℤ, which has size r/d ≥ 2. So the vector is 0 unless that orbit is {m, j}, i.e. j ≡ m + r/2. Hence V_d ∩ span(e_m, e_j) = 0. If X + t₁δ₁ and X + t₂δ₂ both lie in V_d with δ₁ ∦ δ₂, their difference t₁δ₁ − t₂δ₂ lies in V_d ∩ span(e_m, e_j) = 0. That forces t₁ = t₂ = 0, so X ∈ V_d, contradicting primitivity. ∎

So at most τ(r) − 1 of the ratios 1:1, …, 1:τ(r) are killed. Here τ(r) is the number of divisors of r. For an antipodal pair j = m + r/2, V_{r/2} kills only ratios with (α − β) | (x_j − x_m), or with β − α = x_j − x_m exactly; it never kills 1:1. So again some α ≤ β ratios survive.

**Theorem 5 (Ogden barrier for Q on fixed-run slices).** For every r ≥ 2 there is p₀(r) (for example (r+2)(τ(r)+4)) such that, for p ≥ p₀, Q ∩ (a⁺b)^r satisfies the conclusion of Ogden's lemma.

*Proof sketch, all steps elementary.* Call a run long if its length is ≥ τ(r)+3. Short runs and b's carry < p marks in total, so some long run m carries a mark.
- **Another long run j exists, with only short runs between m and j.** Choose j on the side where j ≢ m ± r/2; at most one side is antipodal, and if only an antipodal neighbour exists, use the V_{r/2} remark above. Put v = 1 letter containing the extreme mark of run m (or x, if j < m). Put x = β letters at the near end of run j, β ∈ [1, τ(r)]. Then vwx contains ≤ p marks. By Lemma 5.1 some β gives a direction that is never killed. All pumpings stay in R, since no run is deleted, and they stay primitive.
- **Run m is the only long run.** Every orbit partner of m has length < x_m, so a single-run pump δe_m can be killed only by i = 0 with x_m − δ equal to a partner value. That kills ≤ τ(r) − 1 values of δ, so some δ ∈ [1, τ(r)] survives (v = δ letters containing a mark, x = ε). ∎

The search agrees: `ogden_gen.py Q` found 0 witnesses on about 2900 slices with up to 6 runs. Also Q ∩ (a⁺b)⁴ = {x₁ ≠ x₃} ∪ {x₂ ≠ x₄} is CF. The grammar `qslice4.txt` was checked exactly against Q ∩ R for all lengths ≤ 18: 980 words, 0 mismatches.

**Precise reasons the technique fails for Q.**
1. **Short borders are boundary effects.** The kill set {x₁ ≤ x₄} compares the first run with the last run, which is a feature of the linear representative. Under rotation, runs 1 and 4 are adjacent, and the border a^{x₁}b is invisible to Q, which is rotation-closed. Q's complement has no boundary-anchored, inequality-defined pieces.
2. **Codimension.** One Ogden pump moves along a ray in a 2-coordinate plane. A half-space captures a whole open cone of ratios. A subspace that meets the plane only at 0 captures at most one ratio (Lemma 5.1). The factorial trick buys one exact equality per ratio, never a cone.
3. **Consequence.** Any Ogden/pumping refutation of Q must use R with pumps that change the run structure (v containing both letters, e.g. R ⊇ (a^k b)^*), or must use non-pumping tools. Fixed-run slices are provably useless (Thm 5). This matches the registry lesson that single-slice combinatorics is dead, and Route A's no-go theorem (OG preserved by transductions).

**What would be needed.** A family z whose kill sets are all non-primitive. By Lemma 5.1, z would have to be a near-power along every admissible pump direction simultaneously. The run-changing version of this (pumping whole periods of a near-power) preserves the defect and keeps z primitive. I see no candidate, and I consider this gap to be of theorem strength.

---

## 4. Summary of new artifacts
- **Thm 1:** UB is not CF (Ogden on (a⁺b)⁴; simulated for p ≤ 4).
- **Thm 2–3:** Q ∩ P_f is not CF for f ↑ ∞; for f bounded it is CF ⇔ Q is CF.
- **Thm 4:** rot_{≤c}(UB) is not CF (via an inverse morphism).
- **Thm 5 + Lemma 5.1:** Ogden cannot refute Q on any fixed-run slice (a⁺b)^r; precise codimension reason.
- **Open:** whether P_half (per > n/2) is CF; it is thin-complement and Q-like. Also the "adaptive transversal" lemma of §2.
