# Agent "transduce": closure reductions in the correct direction (images of Q, Q ∩ R under CF-preserving maps)

**Claim: no proof of either resolution.** I give three barrier theorems: T1, T2 and Prop D. T1 says the
whole family of "equality-forcing" targets is unreachable. T2 says the bounded part of the closure route is
exactly the (generalised) Kászonyi–Katsura question. Prop D says that in every bounded slice the forced
non-primitive set is "half-dimensional". I also give two proved non-CF "co-equality" targets (DIST3,
CROSS≠), which are the right kind of target, and explain why slices cannot produce them directly.
Tags: PROVED / COMPUTER-CHECKED / LIT / CONJ / IDEA. Proofs build on `context-free/reports/closure.md`
(cited as CL; its Prop P, Lemma I, Theorem B′ Step A are used as proved there, not re-audited here).

Notation: M(Q) = full trio of Q = {τ(Q) : τ rational} = {g(h⁻¹(Q) ∩ R)} (Nivat). If Q is CF then M(Q) ⊆ CFL.
A *slice* is B = x₀y₁*x₁⋯y_r*x_r ⊆ {a,b}*; N_B = {e ∈ ℕʳ : W(e) := x₀y₁^{e₁}x₁⋯y_r^{e_r}x_r ∉ Q}.

Scripts: `context-free/round4/scripts/transduce/halfdim_check.py`, `one.py`.

---------------------------------------------------------------------------------------------------
## T1. Equality barrier (PROVED)

> **T1.** If T ∈ M(Q) then M(T) ⊆ M(Q) contains no language with an infinite member lacking a subset
> {u vᵏ w : k ≥ k₀}, v ≠ ε. In particular {aⁿbⁿ} ∉ M(T). Hence none of the following is in M(Q):
> COPY = {ww}, {aⁿbⁿcⁿ}, {aⁿbᵐcⁿdᵐ}, MIX = {|w|_a=|w|_b=|w|_c}, {|w|_a=|w|_b}, {a^n b a^n b},
> and no language from which one of these can be obtained by ∩ regular / morphism / inverse morphism.

*Proof.* M(Q) is closed under rational transductions (composition), so M(T) ⊆ M(Q). CL Prop. P: every
infinite member of M(Q) contains some u v^{≥k₀} w. {aⁿbⁿ} is infinite and contains no such set.
Reductions: COPY ∩ a*ba*b = {aⁿbaⁿb}, and erasing the b's and renaming the second block gives {aⁿcⁿ}.
{aⁿbᵐcⁿdᵐ} ∩ a*c* = {aⁿcⁿ}. MIX ∩ a*b*c* = {aⁿbⁿcⁿ}, and erasing c (a morphism) gives {aⁿbⁿ}; {|w|_a=|w|_b} ∩ a*b* = {aⁿbⁿ}. ∎

So **targets must be "co-equality" languages**, i.e. defined by negated equalities. This matches the
structure of Q itself (CL §7: images express negations of conjunctions of equalities).

## Two proved non-CF co-equality targets (PROVED, via Ginsburg's theorem)

(GI, LIT: Ginsburg 1966 Thm 5.4.2) L ⊆ a₁*⋯a_k* (distinct letters) is CF iff its exponent set is a finite
union of stratified linear sets: each period has ≤ 2 nonzero coordinates, and no two periods p, p′ have
p_i p_k ≠ 0 and p′_j p′_l ≠ 0 with i<j<k<l.

* **DIST3 = {aⁱbʲcᵏ : i,j,k pairwise distinct} is not CF.** Take P = (N, N+N!, N+2N!), with N larger than all base/period
  entries. Some period p = (α,β,γ) used in P's representation has α ≥ 1 (since i = N exceeds every base entry),
  and P + m p ∈ E for all m ≥ 0. If γ = 0, k is unchanged and m = 2N!/α (an integer, as α < N) gives i = k.
  If γ > 0, then by the ≤ 2-nonzero rule p = (α,0,γ), so j is unchanged and m = N!/α gives i = j.
  Both cases leave E. ∎
* **CROSS≠ = {aⁱbʲcᵏdˡ : i ≠ k and j ≠ l} is not CF** (crossing disequalities; the plain Ogden attempt fails
  because pumping aᵖ,cᵖ together preserves i≠k). Take P_N = (N,N,N+N!,N+N!), with N > C := max base/period entry.
  P_N = c + Σ n_t p_t. Some used period p has p₁ ≥ 1, and P_N + m p ∈ E for all m ≥ 0. If p₃ = 0, m = N!/p₁ gives i = k: contradiction.
  So p₃ > 0, which by stratification means p = (α,0,γ,0). If α > γ, m = N!/(α−γ) gives i = k: contradiction. So α ≤ γ.
  Symmetrically, some used period p′ = (0,β,0,δ) has β,δ ≥ 1. Then p and p′ cross (1<2<3<4), so the set is not
  stratified. ∎

Neither DIST3 nor CROSS≠ is excluded by T1 or by the Parikh barrier, since both have semilinear Parikh image and contain regular infinite subsets.
**Whether either lies in M(Q) is OPEN.** By T2 + Prop D below, a single slice with an injective linear readout cannot produce them.

---------------------------------------------------------------------------------------------------
## T2. Bounded reduction theorem (PROVED, modulo CL Theorem B′ Step A)

> **T2.** Let L ∈ M(Q) be bounded, L ⊆ c₁*⋯c_k* (distinct letters). Then there are a regular L₀, a rational τ′
> and a bounded regular B ⊆ {a,b}* (a finite union of slices) with L = L₀ ∪ τ′(Q ∩ B).

*Proof.*
1. Write L = g(h⁻¹(Q) ∩ R). Replace R by R ∩ g⁻¹(c₁*⋯c_k*), which leaves L unchanged.
2. Let G be the transition graph of a DFA for R, with input label λ = h and output label g on edges.
   L = {g(π) : π accepting walk, λ(π) ∈ Q}. For walks π, the output g(π) ∈ c₁*⋯c_k* is determined by its
   Parikh vector, which is a linear function of the edge-count vector v = Ψ_E(π). So **all walks with the same v have the same output.**
3. Fix the constants K₁, K₂, L₀ and the "types" of CL §5. The type of v is (supp v, the set of simple cycles all of
   whose edges are used ≥ K₁ times). This is a regular property of walks: count each edge up to K₁. So "accepting
   walk of type 𝔱 with ℓ ≥ L₀" defines a regular set R_𝔱. Short labels (ℓ < L₀) contribute g of a regular set
   restricted to finitely many inputs. That part is regular.
4. *Non-commuting type, ℓ ≥ L₀.* CL Step A applies to every v of this type. Inserting γ₁γ₂ or γ₂γ₁ gives two walks
   with the same v, and one of their labels is primitive. By (2) they have the same output. So the image of R_𝔱
   restricted to λ⁻¹(Q) equals g(R_𝔱), which is regular.
5. *Commuting type, ℓ ≥ L₀.* By CL B2–B3, every walk of the type is σ⊕γ with |σ| ≤ B. Its label is
   W_σ(e) = ρ_{q₀}^{e₀}λ(f₁)ρ_{q₁}^{e₁}⋯, which lies in the slice B_σ := ρ_{q₀}*λ(f₁)ρ_{q₁}*⋯λ(f_k)ρ_{q_k}*.
   Put B = ∪_σ B_σ (a finite union). Then the contribution is g(R_𝔱 ∩ λ⁻¹(Q ∩ B)) = τ_𝔱(Q ∩ B), with
   τ_𝔱(x) := g(R_𝔱 ∩ λ⁻¹(x)), which is rational.
6. L is the finite union of these pieces, and the union of rational transductions is rational. ∎

**Consequence.** For bounded images, the closure route is equivalent to the
**generalised KK question: is there a bounded regular B with Q ∩ B not CF?** (⇐ is trivial.) By Ginsburg, this is the
question whether every slice exponent set ℕʳ \ N_B is stratifiable. Bounded images of Q with arbitrary transductions add nothing beyond slices.

---------------------------------------------------------------------------------------------------
## Prop D. Half-dimension of forced sets (PROVED; COMPUTER-CHECKED growth)

Call B merge-free if, after the reductions (a)–(c) of CL Lemma I (all y_i primitive and nonempty, cyclic form),
no index merges (CL (d1)). By CL (d1)–(d3), every slice equals, *as a language*, a merge-free slice, so for
CF-ness only merge-free slices matter.

> **Prop D.** For a merge-free slice with r blocks, N_B is contained in a finite union of affine subspaces of ℚʳ,
> each of dimension ≤ ⌊r/2⌋. The bound is attained by (ab*)⁴, where N ⊇ {e₁=e₃, e₂=e₄}.

*Proof.* Induction along the proof of CL Lemma I.
* **Rigid range [T,∞)ʳ.** N is a finite union of sets A_s = {e : e_i − e_{i+s} = δ_{i,s} ∀i}, s ∈ {1,…,r−1}.
  The orbits of i ↦ i+s on ℤ/r have size r/gcd(r,s) ≥ 2, and on each orbit the coordinates are determined by
  one of them. So dim A_s = gcd(r,s) ≤ r/2. (For r = 1, N ∩ [T,∞) = ∅.)
* **Small exponents.** If e_i = t for i in a set I with |I| = k, the constants are absorbed into the gaps. The
  remaining r−k blocks can merge only across a maximal run of fixed indices: adjacent original blocks do not
  merge by hypothesis. Let m be the number of merges, so m ≤ (number of fixed runs) ≤ k. In merged coordinates
  there are r−k−m free classes, and the merged slice is merge-free unless it falls into the r′=1
  self-merge case (CL (d3), r=1).
  - Generic case: by induction the forced set has dimension ≤ (r−k−m)/2 in class coordinates. The preimage under the
    summation map adds m. Total ≤ (r−k+m)/2 ≤ r/2.
  - Self-merge case: every cyclic gap between free blocks crosses a fixed run, so r−k ≤ k. The forced set is all of
    ℕ^{r−k} minus a hyperplane, of dimension r−k ≤ r/2.
* Scaling a coordinate (y = zʲ) does not change dimensions. ∎

COMPUTER-CHECKED (`halfdim_check.py`, `one.py`). For random merge-free slices with r = 3, 4 we counted
#N_B ∩ [0,R)ʳ for R up to 64 (r=3) and 20 (r=4). The growth was linear for every r=3 instance (e.g. 19, 43, 91, 187),
≤ R^{1.08} for r=4, and exactly R² for (ab*)⁴ (64, 256, 1024, 4096).
This is consistent with the bound ⌊r/2⌋ and gives no counterexample.

**Consequence (PROVED, for linear readouts).** Suppose a transduction reads a slice out *injectively and linearly*
(W(e) ↦ c₁^{(Me)₁}⋯, M injective on ℤʳ). Then the excluded set of the image inside M(ℕʳ) lies in affine subspaces of dimension ≤ rank(M)/2.
DIST3 and CROSS≠ have excluded sets that are (unions of) hyperplanes: dimension 2 in ℕ³ and 3 in ℕ⁴, and 2 > 3/2, 3 > 4/2.
So they cannot arise this way. With a kernel K = ker M ≠ 0, an excluded u with a preimage e of large minimum coordinate
needs a whole box e + (K ∩ box) inside N_B. A finite union of affine subspaces can cover such a box only if
one component contains e + K, so u ∈ M(A) with dim M(A) ≤ r/2 − dim K = (rank M − dim K)/2 (PROVED for these
"interior" u). For "boundary" u, whose preimages all have a small coordinate, this fails: an example is
B = a^{e₁} b^{e₂} a^{e₃} b^{e₄}, M(e) = (e₁, e₃, e₂+e₄), whose excluded set ⊇ {(x,y,0) : x+y ≥ 2} is a plane in ℕ³.
Such boundary planes are coordinate planes in all the examples I tried, but I have no proof in general (IDEA).

---------------------------------------------------------------------------------------------------
## Why the suggested "two crossing constraints" plan fails (PROVED analysis)

The brief's idea was: on a slice, primitivity = "not a p-th power AND not a q-th power", giving two crossing ≠-constraints.
* In a bounded slice, a shift s moves **every** free block (no non-trivial rotation of ℤ/r has fixed points).
  So each forced condition A_s ties *every* free coordinate to another coordinate or to a constant.
  One shift can never yield a lone condition such as "i = k" while leaving j, l free. With 3 free blocks,
  "x=y" alone is impossible: z's orbit pins it to a constant or to another free block. This is the
  dimension count of Prop D. So the CROSS≠/DIST3 shape (independent hyperplanes) is not available from
  primitivity; only "half-dimensional" exclusions are. The question is then whether the complement of a finite union of
  ≤ r/2-dimensional subspace patterns can be non-stratifiable. That is precisely KK (for n with ≥ 4 primes;
  CF is known for ≤ 3 prime powers, see `scout.md`), hence T2.
* Unbounded R (e.g. lengths ≡ 0 mod 6) cannot isolate primes: every prime divisor of the length counts.
  The "intersection" structure Σ⁶ᵐ ∩ coPow₂ ∩ coPow₃ (which is ⊋ Q ∩ (Σ⁶)*) is not an image of Q.
* Erasing letters (morphic image) existentially quantifies the erased freedom. An output is excluded only if
  **all** of its preimages are forced. By CL Step A, forced outputs have rigid (commuting-type) preimages. So a long
  erased stretch with two non-commuting cycles makes every output primitive-witnessed. Erasure therefore enlarges
  images towards regular sets and does not expose non-CF shapes.

---------------------------------------------------------------------------------------------------
## Registry entry

1. **Aim:** find rational τ and regular R with τ(Q ∩ R) provably non-CF.
2. **Proved:** T1 (no equality-forcing targets: COPY, aⁿbⁿcⁿ, aⁿbᵐcⁿdᵐ, MIX, {aⁿbⁿ} ∉ M(Q)). T2 (every bounded
   member of M(Q) is regular ∪ τ′(Q ∩ B) with B a bounded slice union). Prop D (forced sets of merge-free slices lie in
   finitely many affine subspaces of dimension ≤ r/2), and its interior-point version for linear readouts.
   DIST3 and CROSS≠ are non-CF (Ginsburg), the natural co-equality targets.
3. **Missing step (bounded route):** ∃ merge-free slice B with ℕʳ∖N_B not a finite union of stratified linear sets.
   This is the generalised KK conjecture's negation, open for ω(n) ≥ 4. **(Unbounded route):** an explicit non-bounded
   member of M(Q) together with an Ogden argument whose pumped words have *all* preimages forced. No candidate found.
4. **Counterexamples:** none to any claim. Prop D's bound is tight ((ab*)⁴). The boundary example above shows that Prop D does not
   transfer verbatim to non-injective readouts.
5. **Strength:** the bounded missing step is strictly stronger than "Q not CF" in the sense that it implies it,
   and it is believed false by the experts (KK conjecture). The unbounded step is incomparable / not reduced.
6. **Reopen:** a slice (or KK length n with ≥ 4 primes) with a non-stratifiable exponent set; or a proof that
   DIST3- or CROSS≠-like languages lie in M(Q) (T1 does not exclude them); or an Ogden argument on an unbounded image
   where "forced" (all preimages periodic) can be certified, e.g. via CL Step A rigidity.
