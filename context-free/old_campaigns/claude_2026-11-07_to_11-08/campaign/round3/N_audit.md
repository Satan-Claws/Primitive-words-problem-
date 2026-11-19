# Round 3 / N: adversarial audit of the round-2 reports H, I and J

Auditor N. For every claimed proof below I re-derived each step in my own words, using the PROBLEM.md checklist:
- quantifier order;
- closure misuse;
- off-by-one errors in lengths, periods and divisors;
- the length-1 and single-letter cases;
- numerics presented as proof;
- misquoted named theorems.

Scripts and their outputs (`*.out`) are in
`/tmp/claude-5714/-home-shobhit--claude-spares-spare-fauO4P/6f48459d-5790-4a18-bccc-eabb8efc4544/scratchpad/r3_audit/`.
All computations are cross-checks only. No verdict below rests on them.

## Verdict table

| # | Claim | Verdict |
|---|---|---|
| I-1 | Reduction: F_m CF ⇔ S_m stratifiable (Ginsburg–Spanier; gsm both ways; a⁺b vs a\*b) | **CERTIFIED.** The theorem is quoted correctly in the letter-bounded form. The section number is unverified ("from memory"). |
| I-2 | Merge Lemma 1 | **CERTIFIED WITH FIXES.** Two cosmetic fixes: "u_s < k" should read "u_s ≤ k", and paths may skip indices (zero blocks). |
| I-3 | F₆ = Q∩(a⁺b)⁶ is CF (cover N1∪N2∪C0∪C1) | **CERTIFIED.** The hand proof is complete. The JSON is exactly the Lemma-1 sets, and it equals S₆ on [0,12]⁶. |
| I-4 | Q∩(a⁺b)⁺ CF ⇔ Q CF (Prop. 4.1) | **CERTIFIED** |
| I-5 | Gap-framework coverage for m ≤ 24 | **UNVERIFIABLE as proof.** It is computer evidence that uses mod-P ranks without certificates. I's report labels it as computer evidence, which is correct. |
| J-1 | Slice formula for UB∩(a⁺b)⁴ | **CERTIFIED** |
| J-2 | Thm 1: UB is not CF (Ogden) | **CERTIFIED** |
| J-3 | Direction Lemma 5.1 | **CERTIFIED.** The antipodal remark after it is imprecise but harmless. |
| J-4 | Thm 5: Q∩(a⁺b)^r satisfies the Ogden conclusion for p ≥ p₀(r) | **CERTIFIED WITH FIXES.** As written it is a *sketch*: the antipodal-only case is incomplete. I supply the missing step below, and with it the theorem is proved. The scope of the claim must also be narrowed: it is a statement about the slice language itself, not about annotated slices. |
| H-1 | Thm 1: OG(Q) ⇔ ∀s CPL_s | **CERTIFIED** |
| H-2 | Thm 2 (power of colourings) | **CERTIFIED** (two implicit side conditions, stated below) |
| H-3 | Lemma 3 and Lemma U | **CERTIFIED** |
| H-4 | Thm 5 (labelled-sequence rigidity) | **CERTIFIED** |
| H-5 | Lemma 5.1, Thm 5\*, Lemma 5.2 | **CERTIFIED WITH FIXES.** One justification is wrong ("σ^{(i)} never the whole cycle"); the correct reason is given below. |
| H-6 | Cor 5.3 (partner principle) | **CERTIFIED WITH FIXES.** The constant Λ is too small for s ≥ 2, which makes the hypothesis vacuous at the threshold length. The fix is to use interior margin 2π₀+1. |
| M-1 | Round 3 M, Theorem M1 (Gap G, dense case): one-sided colour loop of length ≤ s in a run-free buffer is good | **CERTIFIED WITH FIXES** (§5). The R = 1 identity needs one extra justification, which I supply. |
| M-2 | Round 3 M, Corollary M3 (colour Bar-Hillel for Q) | **FLAWED.** The re-thresholding step is false as stated: H's Lemma 5.1 does *not* survive replacing the skeleton threshold 2π₀ by T′ (i = 0 can push the pumped run below T′). M3 also inherits the Λ defect of H-6. The conclusion is plausible and a repair route exists, but M3 is **not proved**. |

None of these items resolves the main problem. The registry's round-2 statuses stand, with the wording changes listed in §4.

---

## 1. Report I (bounded slices)

### 1.1 The theorem and the reduction (I-1)

**What Ginsburg–Spanier actually says.** The source is "Bounded ALGOL-like languages", Trans. AMS 113 (1964), reproduced in Ginsburg's 1966 book, chapter on bounded languages.
- **General-word form.** L ⊆ w₁\*⋯w_m\* is CF iff L is a finite union of sets {w₁^{k₁}⋯w_m^{k_m} : k ∈ S_j} with each S_j a stratified linear set.
- **Letter form.** For distinct letters c_i the representation of a word is unique. So in that case the general form says exactly: "E(L) is a finite union of stratified linear sets". This is the version I uses.
- **Stratified.** P is stratified when every element has ≤ 2 nonzero coordinates and no π, π′ ∈ P satisfy π_iπ′_jπ_kπ′_l ≠ 0 for any i<j<k<l. I's definition matches this exactly.
- The constant of a linear set is unrestricted.
- I's numbering ("§5.4, from memory") is not checked. That does not matter.

**gsm, forward direction.** The input is in (a\*b)^m. The state holds the block index i ≤ m; the machine outputs c_i for each a and ε for each b. A gsm image of a CFL is CF. ✓

**Backward direction.** g⁻¹(L_m) inserts the letter d anywhere. Intersecting with c₁\*d⋯c_m\*d forces exactly one d after each block, and h maps the result onto (a\*b)^m. Each step is an allowed operation. ✓

**Exponent set.** If a^{x₁}b⋯a^{x_m}b = u^k with k ≥ 2:
- u ends in b, so |u|_b ≥ 1 and k | m;
- u consists of the first m/k blocks;
- so x is (m/k)-periodic. The converse is clear.

So E = S_m. The zero vector is periodic, which correctly excludes b^m for m ≥ 2. For m = 1, S₁ = ℕ and a\*b ⊆ Q. ✓

**The a⁺b shift.**
- The exponent set of F_m is 1 + S_m, because x − 𝟙 is periodic iff x is.
- If 1 + S_m = ∪(c_j + P_j\*), then each c_j ≥ 𝟙, since c_j is itself a point of the set. So S_m = ∪((c_j − 𝟙) + P_j\*) with c_j − 𝟙 ∈ ℕ^m.
- The converse is immediate, or follows from F_m = Q∩(a\*b)^m∩(a⁺b)^m. ✓

**Closure misuse.** None. Only gsm maps, inverse morphisms, ∩ regular and morphisms are used.

### 1.2 Merge Lemma 1 (I-2)

**My re-derivation.**
- For x ∈ ℕ^m, the breakpoints λ_k (left partial sums) and ρ_k (right partial sums) cut [0, max) into unit-free segments. Segment s lies in left block u_s ∈ {1..a, ∞} and right block v_s ∈ {1..b, ∞}.
- Consecutive segments differ in at least one coordinate, and both coordinates are non-decreasing.
- **Indices can jump.** A zero block contributes no segment, so the path skips that index. I's phrase "strictly increasing in product order" is correct only if read as "≤ in both coordinates and ≠", which is how I read it.
- Map x to (segment lengths ℓ_s ≥ 1, free values). This is a bijection from X_π onto ℕ₊^{#seg} × ℕ^{free}, so X_π = c_π + P_π\*.
- **Non-crossing.** For s < s′ in inside-out orientation, i_{u_{s′}} ≤ i_{u_s} < j_{v_s} ≤ j_{v_{s′}}. So the supports are nested, possibly sharing an endpoint, and never strictly interleaved. Outside-in is the mirror case.
- **Sign constancy.** {s : u_s ≤ k} and {s : v_s ≤ k′} are both prefixes of the segment sequence. So λ_k − ρ_{k′} is a sum of positive ℓ_s over their symmetric difference, and its sign is fixed by π.

**Fix (typo).** I writes "λ_k is the total length of the segment prefix {s : u_s < k}". It must be **u_s ≤ k**. This is harmless.

**Independent check** (`i_paths.py`). I regenerated every path, with jumps allowed, for the four frameworks:

| piece | framework |
|---|---|
| N1 | ℓ=(2,1), r=(4,5), free 3,6 |
| N2 | ℓ=(3,2), r=(5,6), free 1,4 |
| C0 | ℓ=(3,2,1), r=(4,5,6) |
| C1 | ℓ=(1,2), r=(4,3), free 5,6, outside-in |

I filtered by each piece's predicate and built (c_π, P_π). The resulting families coincide **exactly**, as sets of (constant, period-set) pairs, with the JSON: 40/40/352/32 = 464.

### 1.3 F₆ is CF (I-3)

**Soundness, by hand.**
- On a 2-periodic vector (A,B,A,B,A,B):
  - ν₁ = ν₂ = 0;
  - x₂+x₃ = x₄+x₅;
  - x₁+x₂ = x₃+x₄.
- On a 3-periodic vector (A,B,C,A,B,C):
  - ν₁ = ν₂ = 0;
  - Σ₁³ = Σ₄⁶;
  - x₁ = x₄.
- So each piece avoids P₂ ∪ P₃. ✓

**Coverage, by hand.**
- If x ∉ W, then x ∈ N1 ∪ N2.
- I re-derived the parametrisation x = (A+C, B+D, A+E, B+C, A+D, B+E) and the explicit preimage (B=0, A=x₁−x₄, C=x₄, D=x₂, E=x₃−x₁+x₄). The last two coordinates match exactly when ν₁ = ν₂ = 0. ✓
- On W the invariants are linear functionals of x, so they are well defined:
  - A − B = x₁ − x₄ = Σ₁³ − Σ₄⁶;
  - E − C = x₂+x₃−x₄−x₅;
  - D − E = x₁+x₂−x₃−x₄.
- **P₃ ∩ W = {A=B}.** The differences x₁−x₄, x₂−x₅, x₃−x₆ equal A−B, B−A, A−B.
- **P₂ ∩ W = {C=D=E}.** The differences x₁−x₃, x₂−x₄ and x₃−x₅ equal C−E, D−C and E−D.
- C0 ∩ W = {A≠B, E≠C} and C1 ∩ W = {A≠B, D≠E}. Their union is W \ (P₂∪P₃). ✓
- The lattice and cone statements about W are not needed for the proof.

**JSON spot-check** (`i_json_check.py`).
- **Stratification.** All 464 period sets have ≤ 2 nonzero coordinates per period, no zero period, and no crossing pair: **0 violations**.
- **Global soundness, a proof independent of Lemma 1.** For every linear set c + P\*, each defining functional f of its piece satisfies either (f(c) > 0 and f(p) ≥ 0 for all p ∈ P) or (f(c) < 0 and f(p) ≤ 0 for all p ∈ P). So f ≠ 0 on the whole set: **0 violations**. Every JSON set therefore avoids P₂∪P₃ on all of ℕ⁶, not only on a box.
- **Box equality.** I enumerated every linear set inside [0,B]⁶. This is exact, because all periods are nonnegative, so points outside the box never lead back inside.
  - B = 6, 10, 12: union = S₆ ∩ box, with 0 extra and 0 missing points.
  - At B = 12 that is 4,824,456 points, matching I's figure.
- **Predicate level** (`i_pred.py`). N1∪N2∪C0∪C1 = S₆ on [0,14]⁶. I's side claim that the 6 rotations of C0 alone cover S₆ also holds on [0,14]⁶. That claim is not used.

**Conclusion.** S₆ is a finite union of 464 stratified linear sets. So Q∩(a\*b)⁶ and Q∩(a⁺b)⁶ are CF. **Proved.**

### 1.4 Prop 4.1: Q∩(a⁺b)⁺ CF ⇔ Q CF (I-4)

**Setup.** Let φ(a) = a and φ(b) = ab. {a, ab} is a suffix code (a is not a suffix of ab), so φ is injective.

**φ preserves primitivity on Σ\*b.**
- For w ∈ Σ\*b, φ(w) ∈ (a⁺b)⁺.
- Suppose φ(w) = u^k. Then u ends in b. Every b of φ(w) ends a codeword, so u = φ(v) for a prefix v of w, and injectivity gives w = v^k. ✓

**Pulling back.** For w ending in a, and for w = ε, φ(w) ∉ (a⁺b)⁺. Hence φ⁻¹(Q∩(a⁺b)⁺) = Q∩Σ\*b. ✓

**Rotating back.** Q = cyc(Q∩Σ\*b) ∪ {a}:
- every primitive word containing b has a rotation ending in b;
- cyc stays inside Q;
- the only b-free primitive word is a;
- ε is correctly excluded.

The operations used are inverse morphism, cyclic shift (Maslov/Oshiba) and union with a finite set. All are allowed. ✓

**Side claim.** The remark about {b, ab} is also correct: it is a prefix code whose codewords all end in b.

### 1.5 Other items in I

**Gap-framework coverage, m ≤ 24 (I-5).** For m ≥ 10 the ranks are computed mod P = 2³¹−19 or 2²⁵−39, with no rational certificate for the "covered" verdicts. A rank deficiency mod P can make a subspace look larger or smaller, so "covered" is **not** a proof for those m. The explicit integer failure witnesses are exact.
- Two theoretical ingredients of the test are certified:
  - **The functional criterion.** E_{c,g}(a) ∈ A_p^⊥ ⇔ d_p | a or d_p | a+g. The residue multisets of two equal-length intervals agree iff the length is ≡ 0 or the shift is ≡ 0 mod d.
  - **The perturbation argument.** 𝟙 lies in every U_σ, and a rational subspace not contained in a finite union of subspaces has positive integer points outside that union.
- The status "computer-verified, not proved" is correct as I labels it. The registry wording "(computer)" is fine.

**Prime powers.** For m = p^k, S_m is the complement of a single subspace A_p, which is a finite union of single ≠ conditions. That is trivially stratifiable. ✓

**U_K (Thm 4.2).**
- Soundness is correct. With d < m blocks on one side, that side weighs ≤ s′ − (K+1), which forces an imbalance ≥ 2K+2. Otherwise λ_d = ρ_d = s′ is a tie.
- The PDA description is plausible. I did not check it formally; it is not on the audit list.

**Nested-matching lemma and index-mass rigidity.** I labels both correctly as certificate-model or open statements, not theorems about PDAs.

---

## 2. Report J (unbordered words)

### 2.1 The slice formula (J-1)

Write w = a^{x₁}b⋯a^{x₄}b with x_i ≥ 1. A proper border starts with a and ends with b, so it has the form a^{x₁}b⋯a^{x_s}b with s ∈ {1,2,3}.

| s | condition for a border | note |
|---|---|---|
| 1 | x₁ ≤ x₄ | |
| 2 | x₂ = x₄ and x₁ ≤ x₃ | |
| 3 | x₂ = x₃ = x₄ ≥ x₁ | implies s=1, so redundant |

So L₄ = {x₁ > x₄ ∧ (x₂ ≠ x₄ ∨ x₁ > x₃)}. ✓ The brute-force check on [1,10]⁴ found 0 mismatches (`j_misc.py`).

The general Lemma 0.3 indexing also checks out: β = s−1 gives X[|X|−β] = x_{r−s+1}.

Lemma 0.2 (shortest border ≤ n/2) is correct: a border u with |u| > n/2 yields a shorter border of length 2|u|−n. Lemma 0.1 is correct.

### 2.2 Thm 1: UB is not CF (J-2)

**Quantifier order.** Ogden: ∃p ∀z ∈ L (≥ p marks) ∃ uvwxy [vx marked, |vwx|_marks ≤ p] ∀i: z_i ∈ L. The refutation must be: ∀p ∃z ∀ admissible decomposition ∃i: z_i ∉ L. J's proof has exactly this shape: z depends on p, and i depends on the decomposition. ✓

**Ogden version.** J uses the weaker form (vx contains ≥ 1 mark), which is implied by the standard statement. p+1 ≥ p marks. ✓

**The decomposition cases.**
- **v or x contains a b.** Then i = 2 gives more than 4 b's, so the word leaves the slice. ✓
- **Otherwise v and x are a-factors inside single runs.** Marks occur only in run 1 and v precedes x, so one of two things holds:
  - v ≠ ε lies in run 1, and α ≤ p because v is fully marked;
  - v = ε and x lies in run 1.
- **(a) Both in run 1, or one empty.** vwx lies inside run 1, so |vwx| ≤ p and δ ∈ [1,p]. At i = 0, x₁′ = p+1−δ ∈ [1,p] ≤ x₄. ✓
- **(b) x in run 2 or 3.** At i = 0, x₁′ ≤ p = x₄. If x is the whole run, the word leaves the slice. ✓
- **(c) x in run 4, β ≥ 1.**
  - α > β, i = 0: x₁′ = p+1−α ≤ p−β = x₄′ ≥ 1. ✓
  - α < β, i = 2: x₁′ = p+1+α ≤ p+β. ✓
  - α = β, i = 1+D/α: since α ≤ p, α | p!. This gives (a^{p+1+D}b a^{p+D}b)², a square. ✓

The case split is exhaustive.

**Independent brute force** (`j_ogden.py`, real strings, KMP border test). For p = 1..4 there are 299 / 1,841 / 12,391 / 215,105 admissible decompositions, and **0 survivors**. The p = 4 count matches J's figure exactly.

**Single-letter and length-1 cases.** These are irrelevant to the slice. UB contains a and b, and cyc(UB) = Q. ✓

### 2.3 Direction Lemma 5.1 (J-3)

**Re-derivation.**
- Take a vector of V_d supported on {m, j}. It is constant on the d-orbit of m, which has r/d ≥ 2 elements. Unless that orbit is exactly {m, j} (that is, d = r/2 and j = m + r/2), the orbit contains a zero coordinate, so the coefficient at m vanishes; the same holds at j.
- So V_d ∩ span(e_m, e_j) = 0.
- If two non-parallel directions were both killed by V_d, their difference would lie in this intersection, forcing t₁ = t₂ = 0 and X ∈ V_d. ✓
- Brute force (`j_misc.py`): r ≤ 8, X ∈ {1,2,3}^r primitive, all non-antipodal (m,j), all proper d, and coprime ratios with entries ≤ 6 (1,081,056 cases). **0 violations.**

**Antipodal remark: imprecise.** The exact condition for V_{r/2} to kill α:β is:
- all other antipodal pairs of X are equal, **and**
- t(α−β) = x_j − x_m for some integer t ≥ −1 with t ≠ 0.

The extra clause "or β−α = x_j − x_m" is redundant (it is t = −1). "Never kills 1:1" is correct.

### 2.4 Thm 5: Ogden for Q∩(a⁺b)^r (J-4)

**This is a sketch, but it can be completed.** I checked every step.
- **Some long run carries a mark.** Short runs and b's carry ≤ r(τ+3) < p₀ positions, where τ = τ(r).
- **Mark budget.** With v = the extreme mark of run m (the last mark if j > m, the first if j < m), w contains only unmarked letters of run m, the intervening short runs and the b's. So |vwx|_marks ≤ 1 + r(τ+3) + τ ≤ (r+2)(τ+4). ✓
- **No run vanishes at i = 0,** because long runs have length ≥ τ+3 > β, δ.
- **Single-long-run case.** All orbit partners of run m are shorter than run m, so t ≥ 1 never kills. At t = −1 each proper d kills ≤ 1 value of δ, so some δ ≤ τ survives. ✓
- **Side choice.** Only one index is antipodal to m. So if the nearest long runs on the two sides are different runs, one of them is non-antipodal.

**Missing step: the antipodal-only case.** This case arises when the only usable long neighbour is j = m + r/2: either exactly two long runs, or m is extreme on one side. J only says "use the V_{r/2} remark". That remark shows V_{r/2} does not kill 1:1, but **other V_d could a priori kill 1:1**, and V_{r/2} *can* kill every 1:β with β ≥ 2. For example, r = 4, X = (5,1,3,1), m = 0, j = 2: β = 2 and β = 3 are both killed (`j_misc.py`). The fix:

> **Scenario A.** Some other antipodal pair of X is unequal. Then V_{r/2} kills no direction at all, the other τ−2 proper divisors kill ≤ 1 ratio each, and some 1:β with β ≤ τ survives.
>
> **Scenario B.** All other antipodal pairs are equal. Write X = Y + c·e_j with Y (r/2)-periodic and c = x_j − x_m ≠ 0.
> - Suppose X + t(e_m+e_j) ∈ V_d. Put Y′ = Y + t(e_m+e_j), which is (r/2)-periodic, so Y′ + c·e_j ∈ V_d.
> - Rotation by r/2 preserves V_d and Y′ and swaps e_j with e_m. So Y′ + c·e_m ∈ V_d.
> - Subtracting gives c(e_j − e_m) ∈ V_d. That forces d = r/2, and for d = r/2 it forces c = 0, a contradiction.
> - Hence **1:1 is never killed**.

Checks (`j_antipodal.py`):
- Scenario B over all even r ≤ 10: 1,052 vectors, 1:1 killed 0 times.
- All 70,542 antipodal configurations: some 1:β with β ≤ τ(r) always survives.

With this step, Thm 5 is a **theorem**.

**Scope.** Thm 5 says that the slice language Q∩(a⁺b)^r satisfies the Ogden conclusion. It does **not** say that annotated slices π⁻¹(Q∩(a⁺b)^r)∩R′ do. In H's language, it is CPL₁ restricted to the slice, not CPL_s. So J's phrases "fixed-run slices are provably useless" and "can't refute Q by pumping" are justified only for plain Ogden on the slice itself, with no further regular annotation.

The CFG for Q∩(a⁺b)⁴ was checked to length 18, which is evidence only. CF-ness follows anyway from Ginsburg, since S₄ = {x₁≠x₃} ∪ {x₂≠x₄} is trivially stratified.

**Not on the audit list, but checked in passing.** Thm 2 is correct: D = K·p!, f non-decreasing, and every pumped length is ≥ D.

---

## 3. Report H (OG(Q))

### 3.1 Thm 1: OG(Q) ⇔ ∀s CPL_s (H-1)

**(⇐).**
- Let A be a complete s-state DFA for R, and colour each cut point by the state reached there.
- A colour loop is then a state loop, so ζ_i ∈ R for every i, including i = 0.
- π is letter-to-letter, so π(ζ_i) = z_i ∈ Q.
- The constant p is uniform, and the marks transfer position by position. ✓

**(⇒).** Take R_s over Δ = {a,b}×[s]×[s], with the local constraint "after-colour of a letter = before-colour of the next".
- **v not a colour loop.** The v|v junction in ζ₂ violates the constraint.
- **v and x both colour loops.** Every junction is consistent for every i, including u|w and w|y at i = 0 and the case w = ε. The failure of CPL_s then gives some z_i ∉ Q.
- ζ ∈ π⁻¹(Q)∩R_s. So Ogden fails for that language at every p. ✓

**Quantifiers.** The colouring χ is chosen after p, matching the order in OG. **Certified.**

### 3.2 Thm 2 (H-2)

**(a), (b).** Correct pigeonholes. In (b), 2s+1 points give a colour with 3 occurrences, hence two colour loops with a common start and different lengths, both multiples of π.

**(c).** The product colouring gives s² classes, so s²+1 points suffice. Implicit side condition: f(c_j) ≥ c_k, so that x lies after v. This is satisfied in every later use.

**(d).** Correct. Implicit details:
- the wall cut points themselves need a colour (any choice works);
- combining walls with mod-m colouring needs (s′·m) colours.

"Cannot force divisibility by m > s" follows from (b) with π = 1. **Certified.**

### 3.3 Lemma 3 and Lemma U (H-3)

**Lemma 3.** Suppose (i−1)ℓ ≥ n−1. Then P ≤ (i−1)ℓ.
- The factor vⁱ has length ≥ P + ℓ ≥ P + ρ − gcd(P, ρ), so Fine–Wilf applies.
- Primitivity of root(v) gives ρ | P.
- z_i contains a length-P window with period ρ | P, so z_i is cyclically ρ-periodic.
- ρ | n_i, and deleting (i−1)ℓ ≡ 0 (mod ρ) letters from a cyclically ρ-periodic word keeps it ρ-periodic.
- So z is cyclically ρ-periodic with ρ | n and ρ ≤ ℓ < n. That contradicts primitivity. ✓

**Lemma U.**
- **Windows avoiding interior junctions are cyclic factors of z.** Such a window lies inside some v_t or inside vCv, and vCv is a factor of (vyu)², a square of a conjugate of z.
- **f occurs at every interior junction.** f = v[e,ℓ)v[0,e) with 0 < e < ℓ.
- **Every occurrence of f is a junction occurrence.** So all start positions lie in an arc of diameter (i−1)ℓ − 2.
- **Rotation invariance.** The occurrence set of a power r^q is invariant under rotation by P. So it spans an arc ≥ (q−1)P ≥ n_i/2, which gives (i−1)ℓ ≥ n+4. That contradicts Lemma 3. ✓
- ℓ = 1 is vacuous, since the only conjugate of v is v itself, which is a factor.

**Brute force** (`h_checks.py`). All primitive z with |z| ≤ 11, all v, all i ≤ 3n+6:
- Lemma 3: 0 violations;
- Lemma U: 87,518 fresh pumps, 0 violations.

**Certified.**

### 3.4 Thm 5: labelled-sequence rigidity (H-4)

**Case d = d′.** No d-class lies inside S. For |S| = 2 that would need a 2-element class {j, j+R/2}, which is excluded by the non-antipodal hypothesis. So h′ = h″. ✓

**Case d ≠ d′.** Two distinct proper divisors cannot both equal R/2, so one of them has R/d ≥ 3.
- In the coset C of gℤ_R there are c = d/g super-vertices, and d′/g is a unit mod c, so the d′-steps form one cycle.
- Each link carries R/d edges, or 2R/d when c = 2.
- At most 2|S| ≤ 4 edges are blocked. Disconnecting the cycle needs ≥ 2R/d ≥ 6 blocked edges, so it stays connected.
- Hence h′ ∈ P_g ⊆ P_{d′}, and the case d = d′ applies. ✓
- For |S| = 1, R/d ≥ 2 suffices.

**Brute force.** R ≤ 8, every S of size 1 or 2, alphabet {0,1,2} plus a fresh symbol: 23,360 cases, 0 non-antipodal violations. Degeneracy occurs only at antipodal pairs (140 cases), as H states. **Certified.**

### 3.5 Lemma 5.1, Thm 5\*, Lemma 5.2 (H-5)

**F1–F3.**
- F1 is correct: Fine–Wilf, then primitivity of both roots, then merging.
- F3 is correct: rotation by P is an automorphism and shifts the skeleton by d ≢ 0, using F2.
- For R = 1, F3 gives "always primitive". ✓

**Lemma 5.1.** Overlaps with other skeleton runs are < π+π′ ≤ 2π₀ (by F1). So every other skeleton run, together with its maximality witnesses, lies in the border zone E, which the pump does not change.

**Fix 1: a wrong justification.** H says σ^{(i)} is never the whole cycle because "that would make z_i, hence z, cyclically π-periodic". That inference is false. A linear arc of length n can be π-periodic without the cyclic word being π-periodic: aabaaba (period 3, length 7) is primitive. The correct reason:
- the complement of σ and the 2π₀+1 boundary letters on each side are unchanged by the interior pump;
- so the maximality witnesses at both ends of σ^{(i)} persist, and σ^{(i)} ends exactly where σ did relative to the rest of the word.
- The same argument rules out a whole-cycle π-periodic arc in z_i that would swallow σ^{(i)}.

The conclusion of the lemma stands.

**Thm 5\*.** z(m₁, m₂) is well defined, because inserting or deleting a multiple of π inside a π-periodic stretch does not depend on the offset or on which factor is inserted. The label families are injective in m by length. So Thm 5 gives |T| ≤ 1. ✓

**Lemma 5.2.** Let R = 2 and m₁π = m₂π′ = Δ.
- Both gap words share a periodic prefix of length ≥ 4π₀ ≥ π+π′, so π = π′ with the same phase.
- Deleting or inserting Δ ≡ 0 (mod π) letters inside that prefix gives the same word whatever the offset. So g_σ = g_{σ′}, and z is a square, a contradiction. ✓ This also holds for Δ < 0.

### 3.6 Cor 5.3: partner principle (H-6)

**Argument re-derived.**
- **R ≥ 3.** Consecutive skeleton runs are non-antipodal. The pump lines (c,0), (c,e), (c′,e) through the origin are pairwise non-parallel. The single bad point allowed by Thm 5\* is nonzero, so it lies on at most one line, and at least two of the three pumps are good. All three use the same insertion points, so the copy space is shared. ✓
- **R = 2.** Equal-length partners at step lcm(π, π′) ≤ π₀², by Thm 2(c), and Lemma 5.2. ✓
- **Mark budget.** Each vwx lies between the start of F and position 2π₀+1+s²π₀² of σ′, so it carries ≤ M marks. ✓

**Fix 2: the constant Λ is inconsistent.** F has length 2s²π₀²+1 and margin ≥ 2π₀+2s²π₀²+1 on both sides. So σ must have length ≥ 6s²π₀² + 4π₀ + 3. But Λ = (8+4s²)π₀² + 2 is smaller whenever s ≥ 2. For example, π₀ = 1, s = 2 gives Λ = 26 against a requirement of 31 (`i_pred.py`).

As stated, the corollary is still true, but vacuous for runs of length just above Λ. The fix: Lemma 5.1 needs only margin 2π₀+1 (and λ ≥ 4π₀+2+|v|). With margin 2π₀+1, σ needs length 2s²π₀² + 4π₀ + 3 ≤ Λ, and the corollary holds as intended. Alternatively, take Λ′ = 6s²π₀² + 4π₀ + 3.

**Not proofs.** §6, Gap G and §8 are correctly labelled as necessary conditions, an open lemma and evidence. The phrase "Evidence suggests OG(Q) is TRUE" is evidence only, as stated.

---

## 5. Round 3 / M: the claimed proof of Gap G (priority item)

Source: `campaign/round3/M_gapG.md`. My independent numerical check is `m_check.py` / `m_check.out` (s = 2, λ = 6, designed near-square, near-cube and mixed families). In 59 words, 30 had large-exponent failures, with 0 violations of M1.3 and M1.4, and every word had a fully good block of s+1 cut points. This is evidence only.

### 5.1 Quantifier order
- **M1** has the shape ∀s, λ ∃p ∀(z, χ, B) ∃(c, c′) ∀i ≥ 0.
  - p = p(s, λ) is fixed before z.
  - The decomposition is chosen by the prover after χ.
  - All i are covered: i = 1 trivially, small i ∈ {0} ∪ [2, i₀(ℓ)) by M1.4, and **all** large k ≥ i₀(ℓ), unbounded, by M1.3. The large case is structural, not a finite check.
- **M3** has the shape ∀s ∃p ∀z (n ≥ p) ∀χ ∃ decomposition (|vwx| ≤ p) ∀i. This is the correct Bar-Hillel shape.
- **The Bar-Hillel transfer.** Using H Thm 1 with D = all positions is legitimate: full-marking Ogden is Bar-Hillel. ✓

### 5.2 Lemma M1.1
T-runs have period ≤ s, so they meet B in < λ positions, and no T-run meets B[λ, p−λ).

The phrase "the intersection is a prefix or a suffix" is imprecise when the run and B together cover the cycle (then it can be both). The conclusion actually used, "no T-run meets the middle, which lies in one gap", is correct. ✓

### 5.3 Lemma M1.2: margin bookkeeping (checked as requested)

**(1)**
- Deleting v^{k−1} (length ≡ 0 mod ρ) from the ρ-periodic word N leaves z[β, α+ℓ+e′) ρ-periodic.
- Only the truncation z[α−min(e,λ), α+ℓ+min(e′,λ)) is used.
- It lies in B because α ≥ μ and α+ℓ+λ ≤ (p−μ) + s + λ ≤ p. This needs μ ≥ λ + s, and μ = T+λ+2s+2. ✓
- Hence e, e′ < λ and e + ℓ + e′ < λ.
- **N's minimal period is ρ.** v^k ⊆ N has length kℓ ≥ T ≥ 2ρ, so Fine–Wilf and primitivity of root(v) apply. k ≥ 2 because T > s.
- **N is not the whole cycle,** since |N| < kℓ + λ ≤ n_k ⇔ ℓ + λ ≤ n. ✓
- **The whole-cycle case.** If z_k were cyclically ρ-periodic, z would be too (ρ | n). That is impossible, so N is a genuine arc. ✓

**(2)**
- Let M ≠ N be a T-run of z_k. By F1, |M ∩ K| ≤ |M ∩ N| ≤ 2s − 1.
- If M meets K, or is adjacent to it, on the right: M ⊄ K, and its part after K has ≥ T − 2s + 1 = λ + 2 letters. The first λ+1 of these are z[α+ℓ, α+ℓ+λ+1).
  - This lies in B iff α + ℓ + λ + 1 ≤ p. That holds, since μ ≥ s + λ + 1.
  - The left side needs α − λ − 1 ≥ 0, i.e. μ ≥ λ + 1. ✓
  - A run wrapping round the cycle and re-entering K changes nothing: the first λ+1 letters after K are still these.
- Otherwise M, with its two neighbours (which, together with M's letters, determine maximality), avoids K. The complement of K in z_k is literally the cyclic interval [α+ℓ, α) of z, so M ∈ Sk_T(z).
- Conversely, runs of z are at distance ≥ μ − λ > 1 from v.

**The bookkeeping is correct, with room to spare.**

**(3)** β ∈ (α−λ, α] lies in B[λ, p−λ), so N starts inside the gap S_R → S_1, and only that gap word splits. ✓

### 5.4 Prop M1.3

**R = 0.** The skeleton is {N} alone, and a one-label ring has no proper period, so z_k ∈ Q by F3. ✓

**R ≥ 2: the cross-candidate use of H's Theorem 5 (checked as requested).**
- For every failing triple (α, ℓ, k), z_k has the same skeleton order S₁, …, S_R, N, with the same R. The labels at ring positions 1..R−1 are the unchanged words g₁, …, g_{R−1}, because those gaps avoid K. Positions R and R+1 carry (X, Y).
- So every candidate gives an h′ on the *same* ring ℤ_{R+1} that agrees with the *same* fixed h off S = {R, R+1}.
- S is adjacent, and R + 1 ≥ 3, so S is non-antipodal.
- Theorem 5 is a statement about arbitrary labellings with values in any set X. It does not care which divisor d makes each h′ periodic. So at most one (X, Y) is periodic, all failures share X, and hence they share β.
- **The hypotheses are met.** Different ℓ, k, ρ and target runs are irrelevant, because Theorem 5 never sees them. ✓ (Theorem 5 itself is certified in §3.4.)

**R = 1: the length identity z = N U N⁻ U (checked as requested).**
- Read z_k from s₁ = start(S₁). Failure ⇔ X = Y (ring of size 2, F3).
- Rotation by |X| = n_k/2 is an automorphism sending S₁ to N, so |N| = |S₁|.
- **Missing justification.** "Y = N·U" requires |N| ≤ |Y| = |X|. M does not justify this, and for large k, |N| ≈ kℓ grows. The fix: S₁ = [s₁, s₁+|N|) lies in X's region, which is unchanged between z and z_k, and S₁ cannot contain β because β ∈ B[λ, p−λ) (M1.1). So |S₁| ≤ |X|, i.e. |N| ≤ |X|. ✓
- Then X = N U and Y = N U. Undoing the pump inside N replaces N by N⁻ of length e + ℓ + e′ < λ, so z = N U N⁻ U.
- **The length identity.** n = |N| + 2|U| + |N⁻|, so |X| = (n + |S₁| − |N⁻|)/2. Two triples therefore have |β − β′| < λ/2. ✓

**Site spread.** α − β ∈ [0, λ), so the sites lie in an interval of length < 1.5λ. ✓

### 5.5 Prop M1.4 and the count
- **Lemma 4 applies** (§3, certified; I re-derived the cancellation v^{i−1}Y = Yv′^{i−1} ⇒ Yv′ is a prefix of v^∞).
  - α′ − α + (i−1)ℓ < w + T, because i < ⌈T/ℓ⌉ gives (i−1)ℓ < T.
  - n_i ≥ n − s ≥ 6(w+T).
- **Small-exponent clusters.** Failing sites for fixed (ℓ, i) span a factor with period ℓ ≤ s inside B, so the span is < λ. ✓
- **C, the number of bad intervals.** It is 1 + Σ_ℓ (number of small i) = 1 + Σ_ℓ (i₀(ℓ) − 1). ✓
- **Pigeonhole.** The ⌊w/(s+1)⌋ = C(⌈1.5λ/(s+1)⌉+2) + 1 disjoint blocks exceed the number of blocks hit. A clean block gives a colour loop with site c outside every bad interval, so it is good for every i. ✓
- **Length-1 and single-letter cases.**
  - s = 1 gives ℓ = 1: fine.
  - With ℓ = 1 the root is a letter and N is a unary run: fine.

**Verdict M-1: CERTIFIED WITH FIXES.** Theorem M1 is proved for π₀ = s and every λ ≥ 2s, which implies H's Gap G for any π₀ ≥ s by taking λ = Λ. Two fixes:
- the justification |N| ≤ |X| in the R = 1 case (supplied above);
- the wording of M1.1.

This overturns H's assessment that Gap G is "theorem-strength". It does **not** settle OG(Q): sparse markings remain open, as M says.

### 5.6 Corollary M3: re-thresholding (checked as requested). FLAWED

M3 claims that H's Lemma 5.1, Lemma 5.2, Thm 5\* and Cor 5.3 hold with skeleton threshold T′ in place of 2π₀, because "their proofs only use T′ ≥ 2π₀". **This is false for Lemma 5.1, at i = 0.**
- Lemma 5.1 asserts Sk(z_i) = Sk(z) with σ replaced by σ^{(i)}. That needs σ^{(i)} to stay in the skeleton.
- H secures this with |σ| ≥ 4π₀ + 2 + |v| against a threshold of 2π₀: the "extra |v|" clause.
- With threshold T′ the requirement becomes |σ| ≥ T′ + |v|. In M3, σ and σ′ are merely T′-runs. A T′-run of length T′ ≤ |σ| < T′ + |v| leaves the T′-skeleton after the deletion i = 0. Trivial instance: s = π₀ = 1, T′ = 14, σ = a¹⁴, v = a.
- The label sequence of z₀ then has R − 1 entries, with two gap words merged. Neither Thm 5\* nor Lemma 5.2 speaks about that word.
- Case (iii) of M3 (consecutive T′-runs, Cor 5.3) is exactly where this happens.

**Second defect.** M3 sets T′ := Λ_H, "the run length required by Cor 5.3". By H-6 (§3.6), Λ_H is too small for F and its margins when s ≥ 2. So T′-runs of length near T′ do not even satisfy Cor 5.3's hypotheses. That one is fixable by the margin fix of H-6.

**Further gaps in the sketch.**
- p = p_G + O(s²π₀²) + 2T′ has an unspecified constant.
- The cases (i)–(iii) are exhaustive only if "gap" means the space *between* runs. With gap words, which include the run, a huge σ with small spaces falls into none of the cases.
- Cases (i) and (ii) are fine. In (ii), σ is far longer than T′, so it stays in the skeleton.

**Plausible repair (not certified).** If σ′ drops out at i = 0:
- R = 2 ⇒ the T′-skeleton of z₀ has one run, so z₀ ∈ Q automatically.
- R ≥ 3 ⇒ the two i = 0 words of the pumps (v, x) and (v′, x) differ only in σ's label in the merged (R−1)-ring. Single-site Theorem 5 then allows ≤ 1 of them to be bad, and together with Thm 5\*'s ≤ 1 bad point in the unmerged space, one of the three pumps survives.

To make this rigorous one must also:
- choose σ long enough (≥ T′ + max|v|), for example via a two-threshold skeleton;
- handle σ itself dropping out;
- redo the mark count.

Until this is written and audited, **M3, and the registry claim that "π⁻¹(Q)∩R satisfies Bar-Hillel for every letter-to-letter π and regular R", is unproved.**

**Verdict M-2: FLAWED** at the re-thresholding step. The conclusion is plausible but open.

## 6. Recommended registry edits

1. **I.** Keep "F₆ CF (PROVED)". Add "audit N: JSON = exact Lemma-1 path sets; globally sound by sign certificates; = S₆ on [0,12]⁶". Keep "m ≤ 24 (computer, mod-P ranks, not a proof)".
2. **J.**
   - "Proof sketch" → "proved (audit N supplied the antipodal step)".
   - Narrow the scope: "Q∩(a⁺b)^r itself satisfies plain Ogden; annotated slices (CPL_s, s ≥ 2) are not covered".
3. **H.** Cor 5.3: replace the margin by 2π₀+1, or replace Λ by 6s²π₀²+4π₀+3. Lemma 5.1: replace the whole-cycle justification.
4. **M.**
   - "Gap G: PROVED (audit N, with the R = 1 fix)".
   - "Colour Bar-Hillel for Q (M3): CLAIMED, re-thresholding gap at i = 0 deletion; unproved".
   - The residual of OG(Q) is G_sp (sparse markings) **plus** a rigorous M3.
5. No item changes the overall status. F₆ gives no negative resolution, UB is dead, and OG(Q) remains open.
