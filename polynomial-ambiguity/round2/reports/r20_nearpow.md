# r20_nearpow.md: R20-C. Near-powers over ALL exponents + IF ⇒ C_exp?

Status: **COLLAPSES. No C_exp proof. The obstruction is exact and has a structural cause.** Near-powers are the
*witness-poorest* primitive words (Lemma WP). Every constraint they impose is soundness-only, i.e. of FE type, and
r3_nonunif Prop 1 showed FE data is ambiguity-blind. Both halves of the brief fail as stated:
- (1) "the spine must carry the defect phase mod |u|" is false. Nesting matches the defect with its partner at
  distance n/p, and no phase needs to be stored (Prop N).
- (2) the counting "≈2^d·n near-powers vs ≤n^k trees" yields nothing. It reduces to FE (Prop C).
What remains is the old W-forcing gap, restricted to near-powers, where it is additionally implausible (§5).

Notation:
- NP = {u^p with exactly one letter flipped : u ∈ {a,b}^+, p ≥ 2}.
- NP_d: those with |u| = d. NP_p: those with exponent p.
- W_q(w) := #{j ∈ Z_n : w_j ≠ w_{j+n/q}} for a prime q | n = |w|.
- w ∈ Q ⟺ W_q(w) > 0 for every prime q | n.

## 0. Facts used [computational + written]
- NP ⊆ Q. Check: 0 non-primitive near-powers, n ≤ 16 (`scripts/r20_nearpow_witness.py`). This is the standard fact
  of `PA/poly_A2.md`.
- Lemma D (r3_nonunif): every node covering the defect has x_v ∈ L_A and x̂_v ∉ L_A. This is soundness only.

## 1. Lemma WP (witness poverty) [written proof + check]
Let w = u^p with one letter flipped at position i, n = p|u|, and q a prime with q | p. Then W_q(w) = 2 exactly, namely
j = i and j = i − n/q (mod n).
*Proof.*
1. n/q is a multiple of |u|, so the restored word u^p satisfies (u^p)_j = (u^p)_{j+n/q} for all j.
2. w differs from u^p only at i. So w_j ≠ w_{j+n/q} if and only if exactly one of j, j+n/q equals i. ∎

Check (n = 12, 16):
- max over NP of min_q W_q = 2;
- mean of min_q W_q over Q_n is 4.96 (n = 12) and 8.03 (n = 16).

Consequence: in every witness-based certificate scheme (mismatch pair at shift n/q), a near-power has O(ω(n)) certificates.
Generic words have Θ(n) certificates. Every lower-bound route for inherent ambiguity known to us (Ogden-type, Wich
C_exp) needs words with *many* certificate choices that the grammar cannot canonicalise. Near-powers have a canonical
certificate: the defect, paired with its partner at shift n/q. So they are the wrong family to force multiplicity.

## 2. Prop N: no spine memory is needed [written proof]
(a) **Fixed d.** NP_d (all p ≥ 2) is regular, with an unambiguous DFA of O(2^d·d) states (guess nothing: read u, then
track the phase and whether the one flip has been seen).
- So for |u| bounded, near-powers impose no constraint on the ambiguity of any sub-grammar.
- Any argument must take d → ∞.

(b) **d → ∞, fixed p.** The CFG G_p for {s σ t σ̄ r : |t| + 1 = n/p}, i.e. |s|+|r| = (p−1)(|t|+1) (CF for fixed p by splitting t) (mismatch at distance n/p, length
constraints by nesting, as in the classic non-square grammar) generates NP_p. Each near-power has ≤ 2 trees in G_p:
the pairs (i − n/p, i) and (i, i + n/p) that lie in range (Lemma WP).
- The defect's phase mod |u| is never stored along a spine. The partner position is reached by length-nesting.
- So claim (1) of the brief ("finite state along a spine cannot remember position mod |u| as |u| grows") does not
  constrain G. A CFG does not need to remember it.

(c) What G_p lacks is **soundness against other exponents**. L(G_p) contains q-powers for q ≠ p (for example v^3 with
|v| even lies in the non-square language). Excluding all of them simultaneously is the intersection over all p. That is
exactly the "Q ∉ CFL?" question, which is open (F1). So the real content of (1) is F1, not ambiguity.

## 3. Pumping on near-powers across p [written proof]: every constraint is soundness-only
Let w ∈ NP_d, and let X ⇒⁺ U X V be a loop in a tree of w, at word positions x U y V z.
- **(PA) aligned, defect outside U and V.** If |U|, |V| ≡ 0 (mod d), then x U^m y V^m z ∈ NP for all m. Completeness
  of these words is automatic, because the pumped tree generates them. No constraint.
- **(PD) aligned, defect inside U** (or V). Pumping down gives u^{p'}, a power, contradicting soundness. So in every
  tree such loops are forbidden. This is a soundness (FE) constraint, the pumping form of Lemma D.
- **(PU) unaligned.** The pumped words leave NP: they are phase-shifted words. Only soundness (primitivity) is required
  of them, so again the constraint is FE type.

None of (PA), (PD), (PU) produces a *second tree* of any word. The brief's "IF hook" needs two distinct pumping trees at
one X with one interface (U, V). In a C_exp-free grammar, one canonical pumping tree per periodic interface can serve
every context: defect left, right, or inside, and every p. Nothing in (PA)–(PU) distinguishes those contexts at the
pumping tree. Their difference sits in the inner X-yield (Lemma D), and the pumping tree does not see it.

## 4. Prop C: the counting collapses [written proof]
- The map near-power ↦ (label, span) of a defect-covering node has image of size ≤ |N|·n². Its fibres are
  unconstrained, because words with different u have different yields at that span.
- The only way to couple two words through a shared (label, span) is to exchange subtrees. That gives C₁[x₂], which is
  exactly the forbidden-exchange data FE.
- By r3_nonunif Prop 1, FE (including the cross-slice form, which covers varying p) gives multiplicity ≤ |V|·L² for
  every grammar.
So "≈2^d·n near-powers vs ≤ n^k trees" cannot produce a contradiction. Every word needs just one tree, and the total
tree count ≥ |Q_n| ≈ 2^n anyway.

## 5. F1 audit and the exact gap
- **Ambiguity-free part.** Everything in §§2–4 uses only NP ⊆ L(G) ⊆ Q. A contradiction drawn from it would show that
  no CFL L satisfies NP ⊆ L ⊆ Q. That implies Q ∉ CFL (open). So it cannot be the source of the proof, and indeed none
  arises.
- **Where ambiguity could enter.** Only through IF/SU/TR (r17_gstruct): a C_exp-free G has unique pumping trees per
  interface and unambiguous sides, so all its multiplicity is O(1) junction slides on the trunk. To use this, one needs:
  - **Forcing Lemma NF (OPEN):** completeness on NP forces, in every G with NP ⊆ L(G) ⊆ Q, some X with two distinct
    pumping trees of one interface (or a super-constant trunk-junction freedom on a single near-power).
  - NF is the W-forcing lemma of `newmech.md` §5 restricted to NP.
  - By Lemma WP and Prop N(b), NF is *implausible on NP*. Near-powers admit canonical, ≤ 2-fold certificates for each
    exponent separately. The difficulty of NP is the conjunction over exponents (an F1 matter), not certificate
    multiplicity.
- **Recommendation.** Abandon near-powers as a forcing family. Multiplicity must come from witness-rich words, i.e.
  the dense/generic regime of T8_poly. That is consistent with "slices capped at linear" in prompt §6.

## Ledger
| item | status |
|---|---|
| NP ⊆ Q (n ≤ 16) | [computational]; standard |
| Lemma WP: W_q = 2 on near-powers for q \| p | [written proof + check n = 12, 16] |
| Prop N(a): NP_d is regular and unambiguous | [written proof] |
| Prop N(b): NP_p ⊆ L(G_p), ≤ 2 trees; spine-memory claim false | [written proof] |
| §3 pumping on NP over all p: all constraints are soundness/FE | [written proof] |
| Prop C: counting reduces to FE ⇒ ambiguity-blind | [written proof, via r3 Prop 1] |
| Forcing Lemma NF | OPEN; heuristically false-direction on NP |
| Near-power route to C_exp | **COLLAPSES** |
