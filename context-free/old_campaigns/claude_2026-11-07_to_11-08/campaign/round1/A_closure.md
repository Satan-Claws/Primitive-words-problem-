# Round 1 / Route A: closure-property reductions (negative direction)

Researcher A. Status: **no proof that Q is non-CF.** What I do have:
(i) a rigorous no-go/normal-form theorem showing that any chain of permitted operations followed by Ogden's lemma reduces to Ogden's lemma for *regularly annotated* Q;
(ii) a proof that the obvious way to show annotated Q satisfies Ogden (Ramsey plus pumping between marked points) fails, with an explicit counterexample family;
(iii) a concrete finite-dimensional target, F6 ≅ Q ∩ (a⁺b)⁶. Its context-freeness is *exactly* characterised by Ginsburg's stratification theorem, and it is the smallest case containing the "two periods at once" difficulty.
(iv) evidence that the cheapest obstruction to stratifying F6 fails.

Scripts are in `/tmp/claude-5714/-home-shobhit--claude-spares-spare-fauO4P/6f48459d-5790-4a18-bccc-eabb8efc4544/scratchpad/closure/`. Script output is evidence only.

Notation: N = Σ⁺ \ Q is the set of non-primitive words. "Ogden(L)" means L satisfies the conclusion of Ogden's lemma: ∃p ∀z∈L with ≥p marked positions ∃ z=uvwxy, vx contains a mark, vwx contains ≤p marks, ∀i≥0 uvⁱwxⁱy ∈ L.

---------------------------------------------------------------------------

## 1. Structural facts about images τ(Q)

**1.1 Nivat normal form.** Every rational transduction τ has the form τ(L) = g(f⁻¹(L) ∩ R), with f, g alphabetic morphisms (each letter goes to a letter or to ε) and R regular. Inverse morphisms, morphisms, gsm maps, quotients by regular sets, ∩R, and union or concatenation with a regular set are all rational transductions. So any chain of these is one τ. Reversal and cyclic shift are not rational transductions, but Q is closed under both, and I handle them separately in §2.

**1.2 Existential-projection lemma (rigorous, elementary).**
- y ∈ τ(Q) iff τ⁻¹(y) ∩ Q ≠ ∅.
- Hence τ(Σ⁺) \ τ(N) ⊆ τ(Q) ⊆ τ(Σ⁺).
- The set of points the target misses, D = τ(Σ⁺) \ τ(Q), is the set of y whose *entire* preimage (a regular set) lies in N.

So any morphic or erasing step weakens the target. A projection replaces "z ∈ Q" by "some preimage is primitive", and this is closed under adding witnesses. Only f⁻¹ and ∩R preserve the conjunctive structure of Q (Q ∩ Σⁿ = ⋂_{p|n} non-p-th powers). That conjunctive structure is what a non-CF proof has to exploit.

Concrete instance (candidate C1). Take Q ∩ (a⁺b)⁺, which encodes primitive sequences over ℕ⁺. Code each block by its length mod q, or by any finite letter-to-letter quotient of block lengths. The image is *every* coded sequence: any coded sequence of length ≥ 2 lifts to a sequence with pairwise distinct entries, which is primitive, and a length-1 sequence aⁿb is always primitive. The target is regular. This is the generic fate of projections.

**1.3 Consequence.** The only steps that can help a pumping argument are those that **restrict the admissible decompositions** (∩R) or **coarsen positions** (f⁻¹). §2 makes this precise.

---------------------------------------------------------------------------

## 2. No-go meta-theorem: closure reductions add exactly "regular annotation"

**Definition.** L ⊆ Γ* has property **OG** if, for every letter-to-letter morphism π: Δ→Γ and every regular R ⊆ Δ*, the language π⁻¹(L) ∩ R satisfies Ogden's lemma.

Every CFL has OG, because π⁻¹(L) ∩ R is again CF.

**Theorem A.** OG is closed under:
- every rational transduction (hence ∩R, inverse morphism, morphism, gsm, regular quotients, union and concatenation with regular sets);
- reversal;
- cyclic shift.

Consequently: if some chain of permitted operations takes Q to a language T, and Ogden's lemma refutes T's context-freeness, then for some π and R, Ogden's lemma *already refutes π⁻¹(Q) ∩ R*. In other words, ¬OG(Q). Conversely, every such π⁻¹(Q) ∩ R is itself an image of Q.

**So "closure reductions + Ogden" is equivalent to "Ogden on Q with a finite-state colouring of positions".**

The same proofs work with the Bar-Hillel lemma (all positions marked) in place of Ogden's lemma.

*Proof.* Closure under ∩R and under letter-to-letter inverse images is built into the definition, since (π∘π')⁻¹ and π'⁻¹(R) ∩ R' are again of the same kind. By 1.1 it remains to handle alphabetic morphisms (images), erasing inverse alphabetic morphisms (letter insertion), reversal and cyclic shift.

(a) **Image under an alphabetic morphism g (possibly erasing).**
- First the alignment step. Words of π'⁻¹(g(L)) ∩ R' are first coordinates of aligned words over Ξ = {(θ,δ): π'(θ)=g(δ)} ∪ {(□,δ): g(δ)=ε}. Hence π'⁻¹(g(L)) ∩ R' = g₁(π₂⁻¹(L) ∩ g₁⁻¹(R')), where π₂ is letter-to-letter and g₁ is alphabetic. The inner language M satisfies Ogden by OG(L).
- Lemma: Ogden(M) implies Ogden(g₁(M)), with the same constant. Take y ∈ g₁(M) and a preimage ξ ∈ M. Mark the (unique) letter of ξ that produces each marked letter of y, and apply Ogden to ξ.
- Check the three conditions. "vx contains a marked letter" implies g₁(v)g₁(x) contains a marked position. "vwx has ≤p marked letters" implies g₁(vwx) has ≤p marks. The pumps g₁(uvⁱwxⁱy) lie in g₁(M).

(b) **Inverse image under an alphabetic f with erased letters E.**
- Fix ζ ∈ f⁻¹(L') ∩ R' with ≥P marks. Write ζ = e₀c₁e₁…c_m e_m with e_i ∈ E*. Let A be a DFA for R' with s states.
- Case 1: some e_i contains ≥ s+1 marks. Among the cut points just before s+1 of those marks, two carry the same state, so there is an A-loop v ⊆ e_i containing a mark. Pumping v changes neither f(ζ) nor membership in R'. The window holds ≤ s+1 marks.
- Case 2: every e_i contains ≤ s marks.
  - Annotate each cᵢ with three pieces of data: the transition-monoid element of the following block eᵢ, the number of marks in cᵢeᵢ (capped at s+1), and the data for e₀ on c₁. This gives a letter-to-letter π: Ξ→Γ and a regular R'' (the product of annotations lies in the accepting set) such that π(ξ) = f(ζ).
  - Mark ξ-letters whose factor cᵢeᵢ contains a mark. There are ≥ (P−s)/(s+1) of them.
  - Apply OG(L') to π⁻¹(L') ∩ R''. Lift the decomposition by replacing each ξ-letter with its factor cᵢeᵢ.
  - The lifted pumps have f-image in L'. They lie in R', because the A-behaviour equals the product of annotations. vx contains a mark. The window has ≤ (s+1)·p_ξ marks.

(c) **Reversal.** Ogden's lemma is symmetric, and π⁻¹ and R commute with reversal.

(d) **Cyclic shift.**
- Let t = yx be in the annotated cyc(L), so xy is (as π-image) in L. Choose the half (y or x) that holds ≥ half the marks, and inside it a window holding exactly P' marks. Mark only that window, on the rotated word s = xy.
- Annotate s with a part label (X or Y) and with the guessed DFA state q at the cut. The condition δ(q₀,y)=q, δ(q,x)∈F is regular on the annotated s.
- Ogden on s gives V and X'. Each lies inside one part, since otherwise V² violates the X*Y* label pattern.
- If both lie in the same part, the decomposition transfers to t directly.
- Otherwise V is in the x-part and X' in the y-part, and in t the order is X'…V. The new window is y₂x₁: y₂ is unmarked and x₁ lies inside the chosen window, so it holds ≤ P' marks.  ∎

**What Theorem A buys.** Any proposed closure reduction can be tested by "unfolding" it into a regular annotation of Q. The thin-complement obstacle is **not** removed by reductions. The prover's only new power is restricting admissible loops to those compatible with a finite monoid. The whole route therefore reduces to one combinatorial statement:

> **Missing lemma OG(Q)** (if true, the route is dead; if false, the route succeeds). For every finite monoid morphism φ: Δ*→M and letter-to-letter π: Δ→{a,b}, there is p such that every ζ with π(ζ) primitive and ≥p marks has an Ogden decomposition ζ = uvwxy whose pumps all satisfy φ(pump) = φ(ζ) and π(pump) ∈ Q for all i ≥ 0.

This is theorem-strength. It implies that plain Ogden/Bar-Hillel cannot refute CF-ness of Q. As far as I know that is unproved in the literature, though I believe it is true; see §3.

---------------------------------------------------------------------------

## 3. Attempt at OG(Q), and why the obvious proof fails

**Natural strategy.** Colour each pair of marked positions by φ of the factor between them. Ramsey's theorem then gives K marked cut points s₁<…<s_K whose factors all map to one idempotent e. Every pump with v = z[s_j, s_k) (and optionally x = z[s_l, s_m)), with j ≥ 2, preserves φ, since φ(u)e = φ(u). It would remain to prove:

(★) For K large, every primitive z and every K cut points admit such a pump all of whose iterates are primitive.

**(★) is FALSE.** Counterexample family: z = a^k b a^{k+L} b with L = lcm(1..k), and S = the k cut points inside the first a-run.
- Every one- or two-sided pump inside the first run grows that run by T ≤ k per step, and T | L.
- At i = 1 + L/T the word becomes a^{k+L} b a^{k+L} b, a square.

The script `star_counter.py` confirms this for k = 2..6 (all one- and two-sided pumps bad). This is the classical factorial trick.

Brute force (`pumpclique.py`, `pump2.py`, all primitive z up to length 13) gives the maximal adversarial |S| (one-sided / with two-sided pumps):

| n | 7 | 9 | 11 | 12 | 13 |
|---|---|---|----|----|----|
| one-sided | 3 | 4 | 4 | 4 | 4 |
| + two-sided | 3 | 3 | 3 | 4 | 3 |

|S| grows unboundedly through the family above.

**How plain Ogden escapes, and the open question for annotated Ogden.**
- In the family, the grammar pumps v in run 1 *together with* an equal-length x in the unmarked run 2. Both runs grow equally and never coincide.
- So any proof of OG(Q) must use partner loops outside the marked/Ramsey set.
- An annotation can constrain loop lengths in the two runs only through finite-monoid data, for example lengths ≡ 0 mod q₁ in run 1 and ≡ 0 mod q₂ in run 2. Those constraints still admit common lengths lcm(q₁,q₂)·j once runs are long, and p forces long runs. I could not find an annotation that blocks the partner pump, and I could not prove that none exists in general.
- Three ingredients for a proof are in hand:
  1. *Large-i lemma (proved).* If z = uvw is primitive and u v^i w ∈ N for some i ≥ 2, then (i−1)|v| < |z| and the root length exceeds (i−1)|v|. (Fine–Wilf: otherwise z has period |ρ(v)| dividing |z|, so z is non-primitive.) Bad i are therefore finite and small.
  2. *Unique-longest-run lemma (proved).* A cyclic word with a unique longest run, or more generally a run type whose multiplicity is coprime to the others, is primitive. So pumping up a uniquely longest run is safe for every i ≥ 1.
  3. The *partner-loop* trick described above.

  Assembling these into a proof for arbitrary annotations is the open step.

---------------------------------------------------------------------------

## 4. Bounded targets: the exact finite microcosm F6

The PROBLEM file lists bounded intersections as a dead end ("look CF"). I checked what is actually *known* there, and found that the smallest genuinely two-period case is open, at least to me, and decidable in principle.

**Reduction (rigorous).** a^{o₁}b a^{o₂}b … a^{o₆}b is non-primitive iff (o₁..o₆) has period 1, 2 or 3. (r^m with six b's forces m ∈ {2,3,6}.) Let h(cᵢ) = a, h(d) = b, and R = c₁⁺d…c₆⁺d. Then h⁻¹(Q) ∩ R, with d erased, is the letter-bounded language

  F6 = { c₁^{o₁}…c₆^{o₆} : o ∈ ℕ₊⁶, o ∉ P2 ∪ P3 },

where P2 is the set of 2-periodic vectors (o₁=o₃=o₅, o₂=o₄=o₆) and P3 the set of 3-periodic vectors (oₖ = oₖ₊₃). Hence **Q CF ⇒ F6 CF**. By Ginsburg's theorem for letter-bounded languages, F6 is CF iff its exponent set is a finite union of *stratified* linear sets: periods with ≤2 non-zero coordinates and pairwise non-crossing supports.

**Facts proved about F6.**
1. **The generic part is CF.** ν₁ = o₁+o₂−o₄−o₅ and ν₂ = o₁−o₂−2o₃−o₄+o₅+2o₆ vanish on P2 ∪ P3. Each of {ν₁≠0} and {ν₂≠0} is a one-counter language contained in F6.
2. **The hard core** is H = V \ (P2 ∪ P3), where V = P2+P3 = ker ν₁ ∩ ker ν₂ (dimension 4). Its points have the form o = (A+C, B+D, A+E, B+C, A+D, B+E) with A ≠ B and (C,D,E) non-constant.
3. **No laminar pair witness exists on H.** I proved this by case analysis, also using rotation and chords on the 6-cycle.
   - In H every 3-period mismatch pair (k,k+3) holds.
   - Every 2-period mismatch pair (j,j+2) or (j,j+4) *crosses or shares an endpoint* with every (k,k+3).
   - More generally, no μ ∈ P3^⊥ and δ ∈ P2^⊥ have nested or disjoint supports: a P2^⊥ functional needs two same-parity coordinates, and every gap of a P3^⊥ support has ≤ 2 consecutive positions.
   - Shared-endpoint conjunctions such as {o₁≠o₄ ∧ o₁≠o₃} are themselves non-CF (Ogden proofs in my notes; same shape as {i<j ∧ i<k}).
   - Consequence: **the "guess one mismatch per period" PDA idea cannot even recognise Q ∩ (a⁺b)⁶.** Any CFG for Q must contain a mechanism that is not a conjunction of laminar mismatch checks. The two-period obstruction already appears in dimension 6.
4. **Ogden cannot settle F6 (sketch proof).**
   - Pumps live in one block or two blocks; for two blocks the direction is d = s·e_k + t·e_l. A direction is killed only if π_P(d) points along the ray −π_P(o) for P ∈ {P2, P3}, or by a single i = 0 coincidence.
   - For k ≠ l, P3 and P2 each kill at most one ray. (P3 kills a 2-dimensional sector only when l = k±3, and then the diagonal s = t escapes P3. P2 never kills a 2-dimensional sector.)
   - Every marked large block has a large neighbour reachable by a window with few marks. The p choices of ratio there leave a surviving pump.
   - Small blocks of size 1 are rigid, but cannot hold ≥ p marks.
   - This is the same partner-pump escape as in §3.
5. **The cheapest Ginsburg obstruction fails (evidence).**
   - Suppose F6 = ∪ Lⱼ, stratified. Then some Lⱼ = c+Λ must cover a 3-dimensional slice W0 = span(P2, y₀) of H in the region Δ>0, with all differences divisible by a large M.
   - That forces three conditions: Λ ∩ W0 spans W0; cone π₃(Λ) misses the ray (−1,1,−1); cone π₂(Λ) misses the ray −π₂(y₀).
   - The script `strat_search.py` (LP plus enumeration of the 14 maximal non-crossing support families) finds stratified cones satisfying all three, for each y₀ ∈ {C, D, E}-directions. Example families are printed in the run log.
   - So local cone geometry does not rule out a stratified cover. A non-CF proof for F6 would need a global argument, and F6 may well be CF.

**F6 as a sharply posed subproblem (recommended).** "Is the letter-bounded language F6 context-free?" is equivalent to a stratifiability question about an explicit semilinear set.
- If F6 is **not** CF, then Q is not CF. This is a closure reduction ∩R, h⁻¹, erasing morphism, all permitted.
- If F6 **is** CF, its grammar must contain a non-laminar mechanism for two simultaneous periods. That is exactly the mechanism a positive construction for Q needs.

The general family is Fₙ = Q ∩ (a⁺b)ⁿ for n with ≥2 prime factors: n = 6, 10, 12, 30 (three periods).

---------------------------------------------------------------------------

## 5. Candidate reductions tried, and verdicts

| # | Reduction | Verdict |
|---|-----------|---------|
| C1 | Q∩(a⁺b)⁺ then block-length coding / any projection | Image is regular (lift to distinct entries). Dead, by the existential-projection lemma 1.2. |
| C2 | Erasing inverse morphism (padding letters) + ∩R | Adds nothing beyond annotation (Thm A(b)); pumping the padding is harmless. |
| C3 | Non-injective letter-to-letter h⁻¹ | Is an annotation by definition; covered by OG. |
| C4 | ∩R, R ⊆ (a⁺b)⁺ unbounded, then Ogden | Reduces to the annotated sequence game. The grammar escapes via equal-length partner loops (§3); Ramsey-only proofs fail (counterexample). Open = OG(Q). |
| C5 | Bounded Q ∩ (a⁺b)^k with one prime period | CF (single mismatch). Dead. |
| C6 | Bounded F6 = Q ∩ (a⁺b)⁶ (two periods) | Ogden fails (§4.4); local Ginsburg obstruction fails (§4.5); exact CF status **open**. Best concrete lead. |
| C7 | Run-level alternation Q∩(a⁺b⁺)⁶ (12 runs; periods 4 and 6) | Contains F6-type cores; same analysis, no advantage. |
| C8 | Quotients, cyclic shift, reversal mid-chain | Covered by Thm A; Q is closed under cyc and reversal anyway. |

---------------------------------------------------------------------------

## 6. Strongest concrete results

1. **Theorem A (rigorous).** Closure-reduction + Ogden/Bar-Hillel arguments are equivalent to Ogden for regularly annotated Q. No chain of permitted operations removes the thin-complement obstacle. The route succeeds iff OG(Q) fails.
2. **Counterexample to the Ramsey lemma (★)** (rigorous): z = a^k b a^{k+lcm(1..k)} b. Proofs of OG(Q) must use unmarked partner loops.
3. **F6 microcosm (rigorous reduction plus a non-laminarity lemma).** Q ∩ (a⁺b)⁶ is CF iff an explicit 6-dimensional semilinear set is stratifiable. No pair of mismatch witnesses on its hard core can be checked laminarly. Deciding F6 is a finite, well-posed problem whose negative answer would settle the conjecture.

Missing lemmas, both of theorem strength:
- (i) OG(Q), which would kill this route;
- (ii) non-stratifiability of F6, which would solve the problem; or its stratification, which would give a two-period gadget for the positive side.
