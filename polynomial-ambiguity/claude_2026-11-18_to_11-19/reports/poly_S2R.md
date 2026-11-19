# poly_S2R — two-letter pumpable slices (a⁺b⁺)^n

Status summary: **PROVED (reduction, negative for the mechanism).** For n even, the slice
(a⁺b⁺)^n is *the same covering problem* as (ab⁺)^{2n}; for n odd it is (ab⁺)^{2n} with the
single period-n component deleted. Crossing pairs (α_i,β_j) are ordinary pairs of [2n]; nothing
new is gained. No extra ply mechanism beyond the existing (ab*)^{n'} family.

## 0. Setup
w = a^{α_1}b^{β_1}⋯a^{α_n}b^{β_n}, all ≥ 1. Run vector r = (r_1,…,r_{2n}) := (α_1,β_1,…,α_n,β_n)
∈ ℕ_{≥1}^{2n}; run order r_1<r_2<⋯ is the interleaved order α_1<β_1<α_2<⋯.
DFA E_n: states 0, R_1,…,R_{2n}, sink; R_j loops on c_j (c_j = a for j odd, b for j even), R_j→R_{j+1}
on c_{j+1}, 0→R_1 on a. Its only cycles are self-loops (partially ordered DFA, unary loops).

## 1. Structure lemma (PROVED; PROOF.md §3 with b⁺ replaced by c_s⁺)
**Lemma 3″.** For a reduced finitely ambiguous CNF G × E_n, L ⊆ (a⁺b⁺)^n:
amb(w) = Σ_σ 1[r(w) ∈ c_σ + ℕV_σ], V_σ linearly independent, supp v ⊆ pair π ⊆ [2n],
pairs laminar in the run order.

*Proof deltas.* (a) Step 1 of Theorem A (ambiguity.md): X ⇒ uXvXz needs a DFA path t→s through v,
so s = t (only self-loops), so L(X), u, v, z ⊆ c_s^* (unary); the Catalan argument runs verbatim
(yields differ in length). Step 2: a side child Z sits in the context of a cycle X ⇒⁺ uXv, and u
(resp. v) labels a loop at s (resp. t), so u ∈ c_s^*, v ∈ c_t^*, L(Z) ⊆ c_s^+ or c_t^+; annotation
constant on C. This uses only "all DFA cycles are self-loops", not the letter b.
(c) Unique first return: two first-return contexts at X ∈ C insert u_1,u_2 ∈ c_s^* at the left
boundary of X and v_1,v_2 ∈ c_t^* at its right boundary. **The question is whether they commute.** Left
insertions are all powers of the one letter c_s and right insertions are all powers of c_t. So any two
sequences ε ∈ {12,21}^N give the same yield, even when c_s ≠ c_t (one side is an a-run, the
other a b-run): each side is a power of a single letter, and both sequences use each context N times.
Distinctness of the 2^N trees is the same as before. Hence C is a simple ring and v_C has support in
{s,t} (a singleton if s = 0 or s = t).
(d)–(f) verbatim: the yield of a C-node spans the run interval [s,t], and nested or disjoint intervals give
non-crossing pairs. **A ring can pump an a-run and a b-run in different blocks** (π = {2i−1, 2j}),
and these pairs are laminar in the interleaved order. ∎

## 2. Geometry (PROVED)
**Lemma S.** w ∈ (a⁺b⁺)^n is a proper power ⇔ r has period 2d for some d | n, d < n.
(u^k = w forces u to start with a and end with b, so runs do not merge and u has 2n/k runs. The converse
is immediate.) So the non-primitive set is F_new(n) = ∪_{d|n,d<n} V_{2d} ⊆ ℤ^{2n}, where V_e = {period e}.

**Proposition S2R.** Let F_old(N) = ∪_{e|N,e<N} V_e be the non-primitive set of the slice (ab⁺)^N, with the
identity r ↔ x.
 (i) n even ⇒ F_new(n) = F_old(2n).
 (ii) n odd ⇒ F_new(n) = ∪_{e|2n, e<2n, e≠n} V_e (only the half-shift class V_n, "α_i = β_{i+(n−1)/2}", is lost).
*Proof.* An odd e | 2n divides n. If e < n then 2e | 2n, 2e < 2n and V_e ⊆ V_{2e}. The only odd e with
no even multiple below 2n is e = n, which happens when n is odd. ∎

The constraint classes also coincide. In both slices a piece is c + ℕV with V independent,
pair supports, and laminarity in the natural order on [2n] (Lemma 3″ vs PROOF.md Lemma 3). Every
abstract covering statement therefore transfers verbatim between "(a⁺b⁺)^n, n even" and
"(ab⁺)^{2n}": Lemma X, §5, Lemma 3P, T1-P1, LAM, GLAM, G3, G4. This includes upper-bound piece configurations.

## 3. Answers
* Crossing pairs (α_i,β_j): these are the pairs {2i−1,2j} of [2n], already available in (ab*)^{2n}.
  They neither loosen nor tighten laminarity.
* "Two interleaved diagonals": in the 2-class analogue (period m' only), the diagonal pairs {α_i,α_{m'+i}}
  and {β_i,β_{m'+i}} are 2m' pairwise-crossing pairs. Lemma X gives dim ≥ 4M−1 and §5 gives ply
  ⌈(2M+1)/2⌉. This is exactly R-type data with 2M free coordinates. There is no gain per coordinate.
* Lower-bound transfer: restricting to α ≡ 1 (a DFA, Lemma 1.2) shows inherent amb of (a⁺b⁺)^n ≥ that of
  (ab⁺)^n (the spaced-slice deletion of R3a applies). By S2R it equals the (ab⁺)^{2n} problem for even n.
* T1 candidate: (a⁺b⁺)^{P_N²} ≅ (ab⁺)^{2P_N²}, which is another member of the existing (ab*)^{n'} family.
  **No new ply mechanism.** Gaps G-LAM′ and G3** are unchanged.
* Residual (OPEN, minor): an odd n with the half-shift deleted. This is a strictly smaller forbidden set than
  F_old(2n) with no obvious comparison, and it is not expected to help.
