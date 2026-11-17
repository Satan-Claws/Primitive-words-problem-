# Report of agent "redteam": adversarial review of the PROVED claims

**Claim level: review only. I do not claim a proof of the conjecture. I found NO fatal flaw in any
result marked PROVED.** I found a few overstatements and presentational slips (listed in §6), and some
items are labelled PROVED without a written proof (marked UNVERIFIED below).

Method. For each claim: (R) I re-derived every step of the written proof by hand; (S) I wrote an independent
script in `scripts/redteam/` (sharing no code with the authors' scripts) and ran it. Verdicts:
CONFIRMED = R done (every step checked) and, where possible, S passes; FLAWED = broken step or counterexample;
UNVERIFIED = I did not check every step.

Scripts (all in `scripts/redteam/`):
| script | what it checks | result |
|---|---|---|
| `rt_common.py` | helpers; non-primitive words built as v^p (p prime, p \| n); primitivity tested as "s does not occur in (ss)[1:-1]" | cross-checked against each other for all n ≤ 14 |
| `thmA_check.py 40` → `thmA_out.txt` | rect. Thm A(1) for 2 ≤ n ≤ 40: every prefix (cyclic arc) of length ≥ ⌊2n/3⌋ has ≤ 1 non-primitive completion; devil R1(a),(b); the exact threshold length | pass for all n ≤ 40. The threshold is exactly max(d_p, d_p+d_q−gcd), e.g. 2n/3 for 6 \| n, 3n/5 for n = 10, 20, n/2 for 2-powers |
| `cover_check.py 20` | builds the 2⌈n/3⌉ rectangles R_{j,c} of Thm A(2) explicitly. Checks each one lies inside Q (direct test), their union is exactly Q_n, π is onto for even n (Prop 2.8), and devil R4 | pass for 2 ≤ n ≤ 20 |
| `affine_check.py` | Lemma 3.1 (S_p by its definition = span of e_i+e_{i+d}; exact half/zero counts for every w), Thm B (T ⊆ Q_n, random cover), builds the NFA of Cor 3.3 and tests its language against Q_n | pass for 2 ≤ n ≤ 14; tuples used are always ≤ the bound ⌈2^k n ln 2⌉ |
| `swapW_check.py` | closure Lemma W for n ≤ 36 | holds. The largest n/\|x\| at which both words are non-primitive is 36/13 ≈ 2.77 (n = 36). Closure reported 18/7 (n ≤ 20); this is consistent, since Thm A forces the ratio below 3 |
| `lemmaI_check.py seed count` | closure Lemma I rigid case (f): the equivalence "W(e) ∉ Q ⇔ ∃s ∀i U′_i = U′_{i+s}", with a_i, b_i computed directly from the word, not from the formulas; also F1 (a_i, b_i independent of e, < A\*) and \|R_i\| ≤ n−2 | seeds 1, 2 (alphabets {a,b} and {a,b,c}): 3000 merge-free instances, 120000 tests, 14061 of them non-primitive, 0 mismatches, 0 assertion failures |
| `lemmaOB_check.py` | closure Lemma OB: for m ≥ M\*, S is empty or a full tail | 20000 instances, 303 with nonempty tails, 0 violations |
| `counting_check.py` | rect. Prop 5.1 and the formulas for ψ(n), ψ(i,j) | ψ, ψ(i,j) match brute force for n ≤ 14; inequalities hold for n < 1500 and i, j < 300 |
| `devil_cert_check.py 6 10 12 14 15` | devil C1 (no certificate has ≤ ω letters; ω+1 suffices except for listed words), C4, C5 | n=12: 24 / 24 / 24 exceptions, all other n: 0; matches devil exactly |
| `devilB2_check.py` | devil B2 example (0,3,1,3,0,4) | no sound labelled vertex-disjoint non-crossing matching, confirmed |
| `bounded_cert_verify.py`, `bounded_struct_check.py` | independent verifier of bounded C1 certificates. Every choice function i ↦ d_i must give a subspace ∩_i(span M_i + V_{d_i}) that lies inside some V_d (annihilator / row-space arithmetic mod 2^61−1); also checks the structures are valid non-crossing (near-)perfect matchings | VERIFIED for n = 6, 10, 12, 14, 15, 18, 20, 21, 30. Negative controls (certificates with structures removed) correctly FAIL |
| `scoutF5_check.py` | scout F5 conjecture, independent search | 0 failures: exhaustive for n = 6, 10, 12, 14, 15, 18, 20, 21; 3000 near-periodic samples each for n = 30, 42, 60 |

---------------------------------------------------------------------------------------------------

## 1. rectangles.md

**Lemma 1.1, Cor 1.2, Lemma 1.3: CONFIRMED (R).** The descent argument is right. Above 2n/3 ≥ 4/3 the span is an
integer ≥ 2, so the node is binary. The larger child of a span > 2n/3 has span > n/3. The count n(n/3+1) ≤ n²
holds for n ≥ 2.

**Lemma 2.1, 2.2: CONFIRMED (R).**

**Lemma 2.3 (the Fine–Wilf step): CONFIRMED (R+S).** I checked each step:
* gcd(n/p, n/q) = n/(pq), and d_p+d_q−gcd = n(1−(1−1/p)(1−1/q)). This is decreasing in p and in q, so it is
  maximal at {2,3} (value 2n/3, with 3 | n, so ⌊2n/3⌋ = 2n/3). The next case is {2,5}, with value 3n/5 and n ≥ 10;
  any pair with both primes ≥ 3 gives at most 7n/15. ⌊2n/3⌋ ≥ (2n−2)/3 ≥ 3n/5 ⇔ n ≥ 10.
* (a) d_p ≤ n/2 ≤ ⌊2n/3⌋: this holds for n ≥ 4, and for n = 2, 3 by hand.
* Both periods are ≤ L and L ≥ d_p+d_q−gcd, so Fine–Wilf applies as stated.

Devil R1(c) gives a slicker version: the value n(p+q−1)/(pq) is an integer ≤ 2n/3, hence ≤ ⌊2n/3⌋.
`thmA_check.py` shows the bound is tight: uniqueness fails at length ⌊2n/3⌋−1 whenever 6 | n (n ≤ 40).

**Theorem A (1)–(3): CONFIRMED (R+S).**
* (1) The merging step is valid. y has period g = n/(pq), g | d_p and i mod d_p < L, so ŵ_p(i) = y_{i mod g}.
* (2) Rectangle containment and covering are correct, and the edge cases n = 2, 3 work (L = 1, 2). The span (0, L) is
  balanced, because n/3 ≤ ⌊2n/3⌋ ≤ 2n/3. Explicitly verified for n ≤ 20.
* (3) The independence argument is correct, including the case π(y) = ⊥.

**Cor 2.4, 2.5, 2.6, 2.7: CONFIRMED (R).** Rotation reduces every span to span (0, ℓ). For 2.6 I checked both
cases: m ≥ 2⌈n/3⌉ ⇒ m ≥ ⌊2n/3⌋, and otherwise min(m, ⌈n/3⌉) > m/2. For 2.5: a fooling set for the family of all
balanced rectangles meets each of the 2s rectangles at the fixed span at most once.

**Prop 2.8: CONFIRMED (R+S)** for even n. π is not onto for prime n (5, 7, 11, …), which is consistent with the
restriction to even n. The de Caen et al. refinement is FROM LITERATURE and UNVERIFIED.

**Lemma 3.1, Theorem B, Cor 3.2, 3.3, 3.4: CONFIRMED (R+S).**
* Union bound: |Q_n|·e^{−N/2^k} < 2^n·2^{−n} = 1.
* Cor 3.2: 4^k/∏p_i is maximal at n = 6 (value 8/3), so the count is ≤ 1.85n² + n ≤ 3n².
* Cor 3.3: the state count (n+1)(4^k n ln 2 + 2^k) + 1 ≤ 1.85n³ + 2.85n² + n + 1 is correct, and it is n^{2+o(1)}
  because 4^{ω(n)} = n^{o(1)}.
* An NFA built this way recognises exactly Q_n for n ≤ 14.

**Remark 3.5: CONFIRMED (R)**, modulo the cited ε-biased construction. s_p = r_p + σ^{d_p} r_p lies in S_p, and the
standard Fourier bound gives ≥ 2^{−k}(1−(2^k−1)ε).

**Prop 4.1: CONFIRMED (R).** |J| = min(ℓ, n−ℓ), the positions of J are distinct mod n/2, and the hybrid argument works.

**Prop 5.1: CONFIRMED (R+S).**

**Theorem 5.2 (exponential excess ambiguity): CONFIRMED (R)**, using Chomsky–Schützenberger (FROM LITERATURE).
* Ψ(z) = Σ_d μ(d)·2z^d/(1−2z^d) has a genuine simple pole at each root of z^d = 1/2 (d squarefree). At such a point
  every other term is analytic, because |z^{d′}| = 2^{−d′/d} ≠ 1/2.
* The "algebraic functions have finitely many poles" step is correct, since Ex contains the zeros of the leading
  coefficient.
* Caveat on the wording: the theorem gives **limsup** e_G(n)^{1/n} > 1, i.e. exponential growth **along a
  subsequence**, not for all n. The coordinator's paraphrase "grows exponentially" should carry "infinitely often".
* The corollaries (k-ambiguity, unions of unambiguous CFLs, non-ℤ-algebraicity, level sets) follow correctly.

**split_lp table (fractional cover values): UNVERIFIED** (not re-run; not load-bearing).

## 2. closure.md

**Lemma W, Cor W′: CONFIRMED (R+S).**
* Case m = l: s = t, contradiction.
* Case m < l: |s|+|t|−gcd ≤ 5n/6 − 1 < |Y|; FW gives a common root r, so x = y.

**Lemma OB: CONFIRMED (R+S).**
* The overlap O has length ≥ 2|y|+2|y′|, so FW forces |y| = |y′|.
* Inserting or deleting a period-length factor at offset o inside both blocks is valid. Deletion yields a prefix of
  the periodic word, insertion its periodic extension.
* One point of S with m ≥ M\* determines the whole tail.

**Lemma I: CONFIRMED (R+S).** I checked (a)–(e) and the rigid case (f), including:
* (d1): c = Y+1 gives length ≥ |y_{i+1}|+|z| for FW.
* (d2): the suffix form p·(sp)^k.
* The r = 1 merge case: p = ε by primitivity.
* r = 1 rigid: e|y| ≥ 2|y|+|x| is enough for FW.
* F1: the strict bounds come from "no merge at i" and, via (d2), "no merge at i−1"; |R_i| ≤ n−2.
* (M).
* F2: an arc containing no full block lies in tail(B_j) ∪ x_j ∪ head(B_{j+1}).
* F3: both inclusions R_i + d ⊆ R_j and R_j − d ⊆ R_i; |Ĵ| ≥ n is impossible; π is a cyclic shift because
  translation preserves cyclic order and the start points t_i are distinct; s ≠ 0.
* The final equivalence in both directions.
* U′_i = α_i y_i^{e_i−c} β_i, using a_i, a_{i+1} < A\* ≤ |y^c x|.

The displayed rigid equivalence survives 120000 independent random tests in which a_i, b_i are computed from the
word itself.

**Theorem B′ / Theorem B (every rational image of Q has a semilinear Parikh image): CONFIRMED (R).**
* Nivat reduction to walks.
* (T1), and (T2) via cycle decomposition: n_C ≤ K₁−1 for cycles through a non-H edge.
* Step A:
  * γ₁γ₂ uses each edge ≤ 4n_V−2 < K₁ times, so supp is unchanged.
  * Euler (EU) gives P_{v′} ≠ ∅, and π′ visits q_K.
  * 6|g₁g₂| < 24 n_V Λ.
* B1: the telescoping identity in the free group holds. If S_K ⊆ ρ\*, then every closed walk at q_K is in ρ\*. The
  conjugate ρ_p is derived correctly, and the x = ε case works.
* B2: a walk with ≥ n_V H-edges in a row has a simple-cycle factor, so |σ| ≤ B.
* B3, B4: the label depends only on the Parikh vectors of the inserted closed walks, and the Presburger formula is
  correct. Step C is correct.

This supersedes devil §5, which lists the same statement as CONJECTURED. There is no contradiction between the two
reports: devil simply did not prove it.

**Theorem C, C1, C2 (Cyc), C5, Lemma RC′, RC, Prop P, Cor P′: CONFIRMED (R).**
* Substitution: τ′(σ(L)) = σ′(τ″(L)), plus "Parikh image of a substitution depends only on Parikh images"; replacing
  the pieces by regular languages is valid.
* Cyc construction (letters L_{c,c′,c″}, R_{…}): checked.
* RC′: the k₀ bound is enough for FW, and deletion or insertion of period multiples gives prefixes or extensions.
* Prop P: the pigeonhole step gives two disjoint closed sub-walks with nonempty output; Z ≠ ε rules out the second
  alternative.
* Q·Q regular: only CHECKED (n ≤ 16), as labelled (it is a classical fact, Reis–Shyr).

## 3. devil.md

* **T1: CONFIRMED (R).** I checked the split |y₁| = ⌊|x|/(k−1)⌋ ≤ |y|, the lengths, and ε ∉ L(S).
* **T2, T3: CONFIRMED (R).**
* **R1 (a), (b), (c): CONFIRMED (R+S, n ≤ 40).**
* **R2: CONFIRMED (R).** Inners are pairwise distinct, out-degree ≤ ω, so |F|(|F|−1)/2 ≤ ω|F|.
* **R3: CONFIRMED (R).**
* **R4: CONFIRMED (R+S, n ≤ 20).** The chain P_k = P_{k+1} uses the outer of split (k+1, m), which is
  [0,k] ∪ [k+m+1,n); the endpoints k = 0 and k = m−1 recover all of w.
  Presentational slip: as a rectangle, the inner side is c·Σ^{m−1} at span (k, ⌈n/3⌉), which is balanced. The text
  calls it "inner length ⌈n/3⌉−1", which taken literally is below n/3 and so not balanced. Harmless.
* **R5: CONFIRMED (R).** I checked the three cases for m′ and q(1−q)^{ω+1} ≥ 1/(e(ω+2)).
* **C0, C1 ("no bounded certificate"): CONFIRMED (R+S).**
  * The valuation argument rules out cycles, including 2-cycles, i.e. two primes sharing one pair.
  * The bound ω+1 is attained exactly as reported for n = 6, 10, 12, 14, 15.
  * Scope note: this is a barrier only for "certificate = set of inspected positions"; it says nothing against
    ambiguous or non-local PDA strategies. The text says so.
* **C2: CONFIRMED (R)**, modulo Ginsburg. j₁/p₁ = 1 − j₂/p₂ would force p₁ | j₁. The claim that every feasible
  arrangement is infinite is only asserted and is UNVERIFIED; the proof covers the "finite or not CF" dichotomy.
* **C3: CONFIRMED (R).** n = 6m and the length set {6·2^α3^β} is not semilinear.
* **C4, C5: CONFIRMED (S)** for n ≤ 15.
* **B1: CONFIRMED (R).**
* **B2: CONFIRMED** for the cited example (S); the 192 count was reproduced by re-running devil's own script.

## 4. scout.md F4/F5

* **F4: CONFIRMED (R).**
  * Each non-constant residue class mod n/p contains a non-wrapping adjacent mismatch (i, i+n/p). So the NFA
    needs, per prime, a status ∈ {none, (start position, letter), done}, i.e. 2n+2 values, plus the position:
    ≤ (n+1)(2n+2)^{ω(n)} states.
  * Rectangles Cor 3.3 makes this obsolete: an n^{2+o(1)} NFA exists unconditionally.
* **F5:** correctly labelled CONJECTURED. My independent search finds no counterexample (table above).
  * The claimed n^{2+o(1)} grammar from F5 is only a sketch, and it is moot given Cor 3.3.
  * bounded L5 shows that the shared-endpoint version would not give stratified pieces for the analogous
    (ab\*)^n problem.

## 5. bounded.md

* **L1, L2, L3, L4: CONFIRMED (R).**
* **L5 (a)–(d): CONFIRMED (R).** For (d) I redid the argument: any admissible P₁ has a span of dimension ≥ 2
  containing 1, and it cannot equal both planes {a=b} and {a=c}, so δ = (0,1,1) satisfies the L6 hypothesis.
* **L6: CONFIRMED (R).** The Dickson step, the integrality of Lv, and the conclusion that the shifted point lies in
  S_k ∩ V_d are all correct.
* **C1: CONFIRMED (S, independent verifier)** for n ∈ {6, 10, 12, 14, 15, 18, 20, 21, 30}. One caveat: my
  arithmetic is mod 2^61−1, which matches the exact result over ℚ except with negligible probability; the authors
  report exact rational checks.
* **C2:** a computational negative remark, UNVERIFIED and not load-bearing.
* **L7: UNVERIFIED** (stated without a full proof).
* **L8:** the reduction is UNVERIFIED, and the n = 30 conclusion is a "hand argument, not machine-checked".
* **L9:** labelled "PROVED (sketch … summarized)". This does not meet briefing rule 1 and should be relabelled
  CONJECTURED/SKETCH.

## 6. Issues found (none fatal)

1. **rectangles 5.2 / coordinator summary:** the excess ambiguity is exponential only *along a subsequence*
   (limsup), not for every n.
2. **bounded L8, L9** are labelled PROVED without full written proofs. Downgrade them to SKETCH. L7 is also
   unproved in the text.
3. **devil R4** wording "inner length ⌈n/3⌉−1": the balanced reading is the span (k, ⌈n/3⌉) with inner set c·Σ^{m−1}.
4. **closure Lemma W remark:** the observed optimal constant grows past 18/7 (36/13 at n = 36). The true supremum is
   ≤ 3 by Theorem A. This is not an error; the remark said "observed".
5. **devil §5 versus closure Theorem B:** devil's "CONJECTURED" is now a theorem; update the summary.

No counterexample to any PROVED statement was found. The Fine–Wilf step in Theorem A is tight, exactly at the
claimed threshold.
