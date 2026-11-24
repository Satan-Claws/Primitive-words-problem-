# r5_generic.md — R5-A: generic words against Wich structure ("bounded linear invariants", H*)

Script: `round2/scripts/r5_generic_maxrun.py` (exhaustive soundness of the box cover UMR up to n ≤ 18, plus Monte Carlo density).

**Why this is not a §6 route.** It concerns the *sets of words that share a derivation skeleton* (interchange families) and what
Wich's normal form lets one tree check. It is not about counts, and it is not about one-split rectangles.

**Verdict: H\* collapses as formulated.** Step (2) cannot see ambiguity: it is exactly soundness (Lemma FE0). Step (1) is false:
Wich's normal form bounds neither the branching nor the rates on typical words, even for unambiguous dense languages. The only
regime where H\* holds (bounded index, fixed rate = FR) is already a theorem for *every* ambiguity (`context-free/reports/density.md`,
Theorem 2), so it carries no ambiguity information. What is left is DENSE-SOUND itself, or newmech's W-forcing lemma, with no reduction gained.
Below are three rigorous by-products and one set-level barrier.

## 1. Where the ambiguity bound can enter (F1) [written proof]

**(a) The bound is indispensable.** Suppose a statement of the form (3) held for every CFL L ⊆ Q:
|L ∩ Σⁿ ∩ {p | g}| = o(|Σⁿ ∩ {p | g}|) for large primes p.
- Take n = p·m. Then |Σⁿ ∩ {p | g}| ≥ 2ⁿ/(p+1)·(1 − o(1)), while there are at most 2^{n/2+1} non-primitive words.
- So L = Q would violate the statement, and the statement would prove Q ∉ CF.
- Hence any proof of (3) must use amb ≤ C|w|^k essentially. The same holds for ¬DENSE-SOUND.

**(b) Interchange families are ambiguity-blind.**
- For a tree τ of w, its interchange family is the set of words obtained by replacing the subtrees at any antichain of nodes by other
  trees from the same nonterminals. It is a subset of L(G).
- "The family avoids all powers" for every τ is therefore equivalent to L(G) ⊆ Q (Lemma FE0, `R2/r3_nonunif.md`).
- This condition is downward closed and holds at every ambiguity. So step (2) of H\* can contribute nothing beyond soundness.
  Ambiguity could enter only through a structural statement (1).

## 2. Step (1) is false (F2) [written proof]

The hypothesis said a tree on a long typical word is a bounded-branching skeleton plus long linear ring chains with fixed rates.

**(a) Branching is unbounded.**
- G_D: S → T S | ε, T → a D b | b D′ a, D → a D b D | ε, D′ → b D′ a D′ | ε. This is the first-return decomposition of the ±1 walk.
- G_D is unambiguous, so it has no C_exp, and L(G_D) = Σ\*.
- On a uniform random word, the longest excursion has length Θ(n) w.h.p., and its D-subtree is a uniform random binary tree.
- So the Horton–Strahler number (equivalently the derivation index) is ~ log₄ n w.h.p. [cited: Flajolet–Raoult–Vuillemin 1979, register function].
- Wich's DAG-of-SCCs depth bounds the nesting of *distinct* SCCs. It does not bound the branching *inside* one non-linear SCC
  (D → aDbD is neither left- nor right-recursive in the sense of Cor 3.21).

**(b) Rates are not fixed.**
- A → aAb | bbAa | ε is unambiguous: the first letter determines the rule. One SCC holds pumps of rates 1:1 and 2:1.
- Wich's Cor 3.20 only compares interfaces that are powers of the *same* (α, β). So "unique pump per interface" ≠ fixed rate.
  Wich gives no bounded lag.

**(c) Language level: dense poly-ambiguous languages are far from FR.**
- L≥ = {w : #a ≥ #b} is a DCFL, hence unambiguous, with density ≥ 1/2.
- *Claim:* L≥ has no FR sublanguage of positive upper density.
- *Proof.* By density.md Theorem 2, an FR language F with δ̄(F) > 0 contains u₀(v u₀)^{Dj} for every v ∈ Σ\* and j ≥ 0
  (that is the form of Theorem 1, which Theorem 2 reduces to). Take v = b^N with N > |u₀|. Then #b > #a, so F ⊄ L≥. ∎
- So no "re-parse into bounded index + fixed rate" normal form exists for typical words of poly-ambiguous dense languages.
- The structure in (1) is only valid on slices (Structure (c), §4.3), where newmech §4 already found that it adds nothing.

## 3. Where H\* *is* a theorem, and its exact reach (F3)

**FR [written proof, density.md Thm 2].** Every FR language inside Q has growth rate < 2, so exponentially small density, at any
ambiguity. This is H\* for bounded index + fixed rate, and it is ambiguity-free (cf. F1(a)): a restricted-class result (§7).

**Prop P (Parikh-closed certificates) [written proof].** Let L ⊆ Q be CF and Parikh-closed (L = ψ⁻¹ψ(L)). Then
|L ∩ Σⁿ| ≤ c_L·√(2/(πn))·2ⁿ.

*Proof.*
1. ψ(L) is semilinear. Every (x, y) ∈ ψ(L) with x, y ≥ 1 has gcd 1, since otherwise (a^{x/g}b^{y/g})^g ∈ L. Off the axes, ψ(L) ⊆ {(1,0), (0,1)}.
2. Let Λ = c + ℕv₁ + … be a linear component with two independent periods v₁, v₂. Take a prime p ∤ det(v₁, v₂).
   Then c + i v₁ + j v₂ ≡ 0 (mod p) is solvable. Lift (i, j) by multiples of p until both coordinates are ≥ 1.
   This gives a point with gcd ≥ p, which is a contradiction.
3. So every component lies on a line r x − s y = const (r, s ≥ 0, not both 0). Such a line meets {x + y = n} in ≤ 1 point,
   of mass ≤ max_k C(n,k)/2ⁿ ≤ √(2/(πn)). ∎

This is the rigorous form of the LIN barrier in `r4_core.md` §4. The K-window analogue (FL), for L closed under equal cyclic
K-factor count vectors, follows the same way. The count vector is a lattice point of a circulation polytope of dimension
D = 2^{K−1}. A full-dimensional linear component contains p-multiples of realisable vectors by the same CRT step, and each
lower-dimensional component has mass O(n^{−1/2}). [sketch: the realisability of the CRT point as an Eulerian count vector is not written out]

## 4. Set-level barrier: box covers of constant density inside Q (F4)

**Prop B [written proof + computational].**
- Let UMR = {w : w[0] = a, w contains b, and the longest maximal b-run of w is unique}.
- Then UMR ⊆ Q. Since w[0] = a, no b-run wraps cyclically. If w = u^p with p ≥ 2 and w non-unary, every cyclic run occurs ≥ p times.
- For each n, UMR ∩ Σⁿ is a *disjoint* union of ≤ n² three-factor boxes X_{i,L}·{b^L}·Z_{i,L}, indexed by the position i and the
  length L of the maximal run. The boxes are X = {a-initial words ending in a with no b^L}, Z = {words starting with a with no b^L}.
- So each word lies in exactly one box: the set-level skeleton ambiguity is 1.

**Data** (`r5_generic_maxrun.py`):
- Exhaustive: |UMR| = 189 484 words with n ≤ 18, and 0 of them are non-primitive.
- Monte Carlo: P(UMR) ≈ 0.36 at n = 253, 1023, 4087, 16129. Conditioned on p | g (p = 11, 31, 61, 127): 0.359, 0.355, 0.359, 0.365.
  The density is constant, and the same on the class {p | g}.

**Consequence.**
- Step (2) of H\* ("most interchange families of a random w with p | g contain a p-th power") is *false* for skeleton families taken
  as products of arbitrary factor sets.
- Any proof of (3) must use the fact that the factor languages L_A are themselves CF and poly-ambiguous. That means recursion inside
  one inside language, which is newmech §5 (W-forcing) and r3_nonunif's conclusion.
- The UMR boxes are not uniformly CF as given: "no b^L" with L ~ log n is not CF-definable uniformly.

**Is UMR (or a dense CF subset) CF? [assessment, OPEN]**
- On three runs, S₃ = {(i, j, k) : unique max} is *not* blocked by stratification near the diagonal.
- Base (1,0,0) with periods (2,0,1) and (0,2,1) is a stratified linear set inside S₃ containing every (2a+1, 2a, 2a). Checked by hand:
  - if a = b, i = 2a+1 is the unique max;
  - if a > b, i > j and i > k;
  - if a < b, j > k and the parity of j differs from that of i.
- So the bounded 3-run restriction may well be CF. For an unbounded number of runs, one run must beat all others, which looks non-CF,
  but I have no proof.
- This is a concrete DENSE-SOUND test case for R5-B: a poly-ambiguous CFL L ⊆ UMR of density ≥ n^{−1/2+ε} would already beat every
  known gadget.

## 5. Exact gap

H\* yields no reduction. What remains is (i) or (ii); neither is easier than before.
- **(i) ¬DENSE-SOUND restricted to {p | g}** must use the ambiguity bound (F1a). It cannot go through interchange families (F1b, F4)
  or through a bounded-branching / fixed-rate normal form (F2).
- **(ii) The only identified mechanism that sees ambiguity inside a tree** is Lemma M plus W-forcing (`newmech.md` §5). Generic words make
  it no easier: F4 shows that the forcing would have to come from the CF-ness of the factor languages, not from set-level soundness.

A single lemma that would revive H\*, stated so that it is not refuted by F2(c):

**(Γ) [OPEN].** For every poly-ambiguous L ⊆ Q, the words of L ∩ {p | g} have trees whose *rings and counters* (not branching) see only
O(1) linear functionals of window counts, up to an o(1) fraction.

F2(c) shows this cannot be a statement about tree shape, so Γ would itself need a new ambiguity-sensitive argument. I found no handle.

## Status labels

| claim | label |
|---|---|
| F1(a), F1(b) | written proof (one-liners; F1b = Lemma FE0) |
| F2(a) unbounded Strahler number | written proof + cited (FRV 1979) |
| F2(b), F2(c) | written proof |
| Prop P | written proof; K-window version is a sketch |
| Prop B soundness and box structure | written proof; exhaustive check n ≤ 18 |
| Prop B density ≈ 0.36, also on {p \| g} | computational (MC) |
| S₃ near-diagonal stratified set | hand check |
| UMR CF? / Γ | open |
