# r20_region.md — R20-B: other certificate regions R (forced + squeezable?)

Scripts: `scripts/r20_region_align.py` → `r20_region_align_out.txt`; `scripts/r20_region_powers.py` → `r20_region_powers_out.txt`.

## Verdict (short)

- **No region satisfying both (F) forced and (S) squeezable was found.** The mechanism does not yield the bridge.
- **Main result: a no-go for one side of the bridge.** [logically exact, with one numerically supported input marked (PR)]
  - T8-type squeezes are *power-robust*: they never use that the pumped words are primitive.
  - Under (PR), every forcing argument that does not use L(G) ∩ P = ∅ (soundness against proper powers P) contradicts
    every such squeeze. The contradiction comes from the trivial grammar for Σ\*, which is complete and unambiguous.
  - With r17's result (soundness alone is vacuous), this pins down where a bridge must get its strength: the forcing step
    has to use **power-exclusion together with completeness**. Neither ambiguity nor completeness alone can do it.
  - The hypothetical grammar structure behind the obstruction is "Σ\* with powers carved out". §4 describes it.
- **Positive lattice facts** [written proofs]:
  - (S) is closed under unions split by a regular partition and under bounded rotations.
  - So T8_poly extends verbatim to the full pure-sign fold F_[1,n/2] = G⁻ ⊔ G⁺ (Lemma U; exhaustive check n ≤ 16).
- **Classification of the natural candidate regions:**
  - Rot(G⁻), all rotation-closed regions, the window fold F_K and end windows E_h of bounded depth are all *outside the
    reach* of T8-type squeezes (end-blind or scale-relative).
  - Bounded-depth E_h is *forced* in the strongest sense, but its (S) already implies ¬P(Q) (a chain of regions, §3).
- **Numerical**:
  - The Lyndon (b<a) canonical rotation is **end-aligned** with G⁻ but **not centre-aligned**. P(Lyndon rotation ∈ E_h) ≈ 0.7
    for h = log²n, while P(∈ G⁻) = 0.63, 0.41, 0.24 at n = 64, 256, 1024. The offset to argmax T decorrelates
    (KS distance 0.41 → 0.18).
  - A canonical-rotation (cyclic-closure) Q-grammar would therefore meet end-window regions but not G⁻.

## 0. Framework (precise)

- Q is the set of primitive words and P the set of proper powers. A **region** is any R ⊆ Q.
- An *admissible sub-structure* of a grammar G is a language obtained from G by
  (a) taking a sub-grammar, i.e. a start nonterminal together with a terminal context, or
  (b) taking a product with a finite automaton (L(G) ∩ C, C regular).
  Both preserve the ambiguity bound.
- **(F) forced.** Every reduced, polynomially ambiguous G with L(G) = Q has an admissible sub-structure L′ ⊆ R that is
  rotation-dense.
- **(S) squeezable.** No polynomially ambiguous CFL L ⊆ R is rotation-dense. T8_poly is (S) for G⁻, conditional on M1/M1′.

**Lemma 0 (collapse) [exact].**
- (F) is upward closed in R and (S) is downward closed.
- A region with both exists ⟺ ¬P(Q).
  - (⇐) Take R = ∅: then (F) is vacuous.
  - (⇒) If G witnesses P(Q), then (F) gives a sub-structure L′ ⊆ R that contradicts (S).

So the question is never whether such an R *exists*, only whether one can be **proved** to have each property by methods
that do not already contain the whole problem. Everything below is about proof methods (as in r17_bridge).

## 1. Lattice operations that preserve (S) [written proofs]

**Lemma U (regular splitting).** Suppose R = R₁ ⊔ … ⊔ R_k with R_i = R ∩ C_i for regular C_i, and each R_i satisfies (S) in
its infinitely-often form (THEOREM_T8 Remark 3.2; T8_poly's summation is uniform in n ≥ n₀, so its i.o. form holds too).
Then R satisfies (S).

*Proof.*
1. Let L ⊆ R be polynomially ambiguous and rotation-dense, with constant δ.
2. Each L ∩ C_i is polynomially ambiguous (product with a DFA) and lies in R_i.
3. Rot(L)_n ⊆ ∪_i Rot(L ∩ C_i)_n, so for each n some i has |Rot(L ∩ C_i)_n| ≥ δ2ⁿ/k.
4. Some single i does this for infinitely many n, which contradicts the i.o. form of (S) for R_i. ∎

**Corollary U.** Let F_[1,n/2] := {w : d_k(w) ≠ 0 for all 1 ≤ k ≤ n/2} (pure sign). Then
- G⁻ = F ∩ bΣ\*a and G⁺ := φ(G⁻) = F ∩ aΣ\*b,
- because d_k changes by at most 1 per step, so its sign is fixed by d₁ = [w₁=a] − [w_n=a].

So **T8_poly holds for F_[1,n/2]** (with the same M1/M1′ caveat; φ preserves everything, THEOREM_T8 §1.1).
Exhaustive check for n ≤ 16: the identities hold and F_[1,n/2] ⊆ Q (0 failures, `r20_region_align_out.txt`).

**Lemma Rb (bounded rotation).** If R satisfies (S), then so does rot_j(R) for each fixed j, and so does any finite union
∪_{j≤J} rot_j(R) that is split by the regular partition "first j letters / last j letters".

*Proof.* rot_{−j} of a polynomially ambiguous CFL is again one: split L by its first j letters (a finite union) and move
those letters to the end. Rotation images are unchanged. ∎

*Open:* ∪_{j≤J} rot_j(G⁻) when the pieces overlap and are not regularly separable. Fold centres shifted by Θ(n) are
genuinely new regions; T8_poly says nothing about them.

## 2. Where T8-type squeezes can and cannot bite [assessment + proof sketches]

T8_poly uses L ⊆ G⁻ only through pumped words W′ ∈ L (Lemma NS, FR-pos, T-tol; r17_bridge §2). Two features of G⁻ are
essential.

- **(E) End-anchoring.** The constraint holds at small depths k ≤ h = log⁴n, where the bad-left/bad-right counting lives
  (r19_fixes §4, rows 2–3).
- **(H) Scale-heredity.** FR-pos inserts a level word x with |x| ≥ n near the start. It then needs W′ ∈ G⁻ at depths
  k ~ |W′|/2, where W lies *entirely inside the prefix of W′*. So G⁻'s constraint must hold at every scale.

Candidate regions against (E) and (H):

| region R | (E) | (H) | T8-type squeeze? | (F)? |
|---|---|---|---|---|
| G⁻, G⁺, F_[1,n/2] | yes | yes | **yes** (T8_poly, Cor U) | ≡ problem (r17_bridge) |
| Rot(G⁻), any rotation-closed R | no (rotation moves the ends anywhere) | no | no: the squeeze has nothing to grip | ≡ "dense poly-amb CF subset of Q" (open, r5_dense) |
| F_K, K = [n/3, n/2] (r5_dense) | no | no (the window scales with n′) | no | open (FOLD-COUNTER) |
| E_h := Q ∩ {d_k < 0 for all k ≤ h}, h = O(1) | yes | no | no (§3) | **yes**, trivially |
| E_h, h → ∞ slowly | yes | no | Lemma NS-type rows only; FR-pos fails | unknown |
| Lyn (Lyndon words, b<a) | partly (first run = longest run) | no | unknown; (S) ⟺ "no poly-amb CFL holds a positive fraction of Lyn_n" | yes for cyclic-closure grammars Cyc(G₀) with L(G₀) = Lyn (G₀ ⊆ Cyc(G₀)); otherwise unknown |

Rotation-closed regions get no help from T8. For rotation-closed R, rotation-dense means dense. A T8-type proof plays
renewal mass ≳ N^β against a quadrant of mass O(log N). Here the cone mass can legitimately be ≍ √N (count gadget
{#a = #b + 1} ⊆ Q, unambiguous and rotation-closed, r4_core), so no mass-squeeze of the T8 kind can work. Proving (S)
would mean telling density Θ(1) apart from density Θ(n^{−1/2}) inside Q, which is the DENSE-SOUND question (task D).

## 3. The chain E_h and the role of powers [written proof + numerics]

**Prop E.**
- (i) For constant h, E_h = Q ∩ C_h with C_h regular and rotation-dense, since C_h ⊇ G⁻ and Rot(G⁻) is dense. So (F)
  holds for E_h: L(G) ∩ C_h = E_h is an admissible sub-structure.
- (ii) Hence (S)(E_h) ⇒ ¬P(Q). The converse, ¬P(Q) ⇒ (S)(E_h), is not known.
- (iii) (S)(E_h ∪ P) is **false**: E_h ∪ P ⊇ C_h ∩ (Q ∪ P) = C_h, which is regular and rotation-dense.

Any proof of (S)(E_h) must therefore use primitivity of some pumped word. T8 never does: G⁻ ⊆ Q is a consequence of the
definition, not a hypothesis used in the proof. So between h = O(1), which is forced, and h = n/2, which is squeezable,
power-sensitivity has to enter somewhere.

**(PR) power-robustness [numerical + standard combinatorics on words].**
- Take a two-sided pumping family x_m = α sᵐ β tᵐ γ that is non-degenerate, i.e. its words do not all share one primitive
  root.
- Then x_m ∈ P for at most a bounded number of m. In 20000 random families with m ≤ 60, non-degenerate families had ≤ 2
  power values. The 465 degenerate families (all letters equal, or common root) were powers at 59–60 values
  (`r20_region_powers_out.txt`).
- The one-sided case is Lyndon–Schützenberger/Shyr–Yu type, and the two-sided bound is believed standard; **not proved
  here**.
- T8_poly's pumping steps choose m from an unbounded range (Lemma NS: any m ≥ C_W + c + 1; FR-pos/T-tol: all large i).
  So, given (PR), the T8_poly argument proves (S) for G⁻ ∪ P as well. The degenerate families are a single-root sub-case
  and are thin.

**Theorem NG (power-blind forcing is impossible against power-robust squeezes).** [exact, given (PR) for the squeeze in use]

Hypotheses:
- (S) for R is proved by an argument that also proves (S) for R ∪ P. By (PR), T8_poly is such an argument.
- (F) for R is proved by an argument that uses of L(G) only Q ⊆ L(G) ⊆ Q ∪ P (completeness, plus soundness *modulo powers*)
  and polynomial ambiguity, and that then yields a sub-structure inside R ∪ P.

Conclusion: these two arguments are inconsistent with each other.

*Proof.*
1. Apply the forcing argument to G_triv (S → aS | bS | a | b). It is unambiguous with L = Σ\* = Q ∪ P.
2. This gives an admissible, rotation-dense, unambiguous sub-structure L′ ⊆ R ∪ P.
3. That contradicts (S)(R ∪ P). ∎

**Consequence.**
- r17_bridge: soundness relative to Q alone is vacuous, since the padding-stable core of Q is Q.
- Theorem NG: completeness plus ambiguity, with soundness only modulo powers, cannot be combined with a T8-type squeeze.
- So any bridge through *any* region that is squeezed by T8-type (pumping) arguments must use **L(G) ∩ P = ∅
  substantively** in the forcing step, i.e. it must derive structure from the *absence* of powers. Neither G⁻ nor any
  candidate in §2 had a forcing mechanism of that kind. This is the precise gap.

## 4. Shape of a hypothetical polynomially ambiguous grammar for Q that defeats region forcing

Theorem NG and r17 §4 combine into the following picture [assessment]. If P(Q) holds, look at the grammar it would give.

- **Locally it is Σ\*.** Every admissible sub-structure that can be reached by completeness alone is a sub-structure of a
  free grammar with power-exclusion added. Its critical cones have "free" token laws, so their yields have density in
  any region equal to that region's density.
- **Power-exclusion is global and uses many mechanisms.**
  - Each word's derivation must certify primitivity.
  - The known certificates are count-based (density ~n^{−1/2}) or positional/fold (G⁻, F_K) (r4_core, r5_dense, r6_miss).
  - A dense union of them must change certificate family with the factorisation of n (r5_dense (iii)).
- **Anchoring floats.** A cyclic-closure grammar Cyc(G₀) over a canonical-rotation set has unambiguity equal to G₀'s.
  Its re-rooting point is the canonical position (e.g. Lyndon), not the fold centre. Numerics: the Lyndon offset from
  argmax T becomes uniform (KS 0.41, 0.30, 0.18 at n = 64, 256, 1024), and P(Lyndon rotation ∈ G⁻) → 0. But
  P(∈ E_{log²n}) ≈ 0.7, so the Lyndon rotation *is* end-aligned.
- So a "Lyndon-shaped" Q-grammar meets end-anchored regions but never the centred fold G⁻. A forcing theorem for G⁻ would
  have to show that such a G₀ cannot exist, which is the canonical-rotation-map form of the problem.

**Most promising residual candidate** (not resolved): R = end-window ∩ scale-hereditary, e.g.
R_h := Q ∩ {d_k < 0 for k ≤ h(n)} ∩ F_[n/3,n/2]. This keeps (E) and soundness (Lemma M) but drops the middle of the fold.
- (S) for R_h would need T8_poly without FR-pos. Rows 2–3 (Lemma NS/W) only use depth ≤ O(√n log n).
- (F) for R_h needs Lyndon-type end-alignment plus a [n/3, n/2] sign certificate.
- Both halves are open. Theorem NG says that the (F) half must use power-exclusion.

## Status table

| item | label |
|---|---|
| Lemma 0 (collapse: existence ⟺ ¬P(Q)) | exact |
| Lemma U, Cor U (T8_poly ⇒ (S) for F_[1,n/2]); Lemma Rb | written proof; identities exhaustive n ≤ 16 |
| §2 table: Rot-closed, F_K, bounded E_h out of reach of T8-type squeezes | assessment (from the structure of T8_poly) |
| Prop E (bounded E_h: forced; (S) ⇒ ¬P(Q); (S)(E_h ∪ P) false) | written proof |
| (PR) power-robustness of two-sided pumping families | numerical (20000 families) + standard; two-sided bound not proved here |
| Theorem NG (power-blind forcing vs power-robust squeeze) | exact given (PR) |
| Lyndon alignment (end-aligned yes, centre-aligned no) | Monte Carlo n ≤ 1024 |
| Region satisfying both (F) and (S) | **not found**; open; the gap is located (power-exclusion in forcing) |
