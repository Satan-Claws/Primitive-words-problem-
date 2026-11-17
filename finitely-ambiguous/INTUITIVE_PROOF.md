# Why the primitive words are not finitely ambiguous — an intuitive proof

**Theorem.** No context-free grammar (CFG) that generates exactly the primitive words over {a, b}
is finitely ambiguous. In other words, for every such grammar G and every k, some word has more
than k derivation trees.

(Whether the primitive words are context-free at all is still open. The theorem says: *if* they
are, every grammar for them is infinitely ambiguous.)

Formal versions: Lean proof in `finitely-ambiguous/lean/` (no `sorry`; axioms `propext`, `Classical.choice`,
`Quot.sound`), detailed paper proof in `PROOF.md`.

---

## The idea in one paragraph

Look only at words of the form "first half, second half", where the word is primitive exactly
when the two halves differ. A grammar has to "certify" that the halves differ. Comparing position
i of the first half with position i of the second half is a long-range link, and all these links
**cross** each other. A context-free grammar can't follow two crossing links in one derivation
tree, so each tree can only certify differences "in one direction". Covering every way the halves
can differ then forces many trees on some word, and the number grows with the length of the halves.

---

## Step 1 — Zoom in on a slice where primitivity is just "x ≠ y"

Write a word as a sequence of blocks `a b^n`. Take words of the shape

    a · (a b^{x_1}) ⋯ (a b^{x_M}) · a · (a b^{y_1}) ⋯ (a b^{y_M}),   all x_i, y_i ≥ 1.

There are exactly two places where two a's are adjacent (the "aa" markers). A power uᵏ has as many
markers as k times those in u, so the only possible power is a square, with one marker per
half. So:

> **Lemma 1 (slice).** Such a word is primitive ⇔ (x_1,…,x_M) ≠ (y_1,…,y_M).

These words form a regular set R. Intersecting a grammar with a regular set (product with a DFA)
does not change any tree count. So a k-ambiguous grammar for the primitive words gives a
k-ambiguous grammar for

    NE_M = { (x, y) : x ≠ y }   (written as words in R).

From now on we only have to show that NE_M needs more than k trees on some word, once M is large.

## Step 2 — What a finitely ambiguous grammar on block words looks like

**Structure lemma (used as a known result).** If a grammar for a language of block words
`a b^{e_1} ⋯ a b^{e_n}` has at most k trees per word, then its tree count is a sum of indicator
functions of linear sets

    L = c + ℕ·v_1 + ⋯ + ℕ·v_r,

where:
* each period v_j only changes **two** blocks (s_j, t_j). It is the "pump" of a repeated
  nonterminal, adding b's on its left side and its right side;
* the pumps in one set are **non-crossing**: there are no s < s' < t < t'. A tree nests its
  subtrees, so its pumps nest too;
* the parametrisation is one-to-one, otherwise some word would get unboundedly many trees.

This is essentially Ginsburg–Ullian (1966). In Lean it is `cnf_structure_blocks` (after a
conversion to Chomsky normal form that never increases tree counts).

So "number of trees of the word (x, y)" = "number of these sets L containing the point (x, y)".
Every set L lies inside NE_M (it never touches the diagonal x = y), and the sets together cover
all of NE_M.

## Step 3 — Crossing kills dimension (Lemma X)

The pair "block x_i, block y_i" crosses the pair "block x_j, block y_j" for every i ≠ j, since
x_i < x_j < y_i < y_j. So no single set L can pump along two different diagonal directions
(x_i, y_i) and (x_j, y_j) with a single period each.

**Lemma X.** If a non-crossing family of pumps can still move freely along the whole diagonal
(all directions "add the same to x_i and y_i"), then it spans at least 2M − 1 of the 2M
dimensions.

Intuition: the non-crossing pumps split the blocks into groups (connected components). Two
groups can't interleave. Only one group can contain a matched pair (x_i, y_i), so only one group
can be "rigid", and it loses at most one dimension.

## Step 4 — Near the diagonal, each set is a half-space

Look at points just next to the diagonal:

    P(t, δ) = (t·ω, t·ω + N!·δ),

where t is huge, ω is a generic direction, δ ∈ ℤ^M is a small offset, and N! clears every
denominator in sight.

Fix one set L that reaches these points. By Lemma X it has at most **one** pump direction that
is not used for moving along the diagonal. If it had none, it would also contain the diagonal
point δ = 0, which is impossible. So exactly one coordinate, a linear function ψ_L(δ), decides
membership:

> for t large: P(t, δ) ∈ L ⇔ ψ_L(δ) > 0.

**Each set L, seen from the diagonal, is an open half-space of offsets δ.** It covers "the
halves differ in one particular direction" and never more.

## Step 5 — Counting half-spaces

Every offset δ ≠ 0 is a word of NE_M, so it lies in at least one half-space {ψ_L > 0}.

* Covering all of ℤ^M ∖ {0} with open half-spaces needs **at least M + 1** of them. With only M
  of them, M − 1 of the forms vanish along some nonzero direction, and that direction or its
  negative is missed.
* Take a generic δ (no ψ_L vanishes). Each half-space contains exactly one of δ and −δ, so

      #trees(δ) + #trees(−δ) = (number of half-spaces) ≥ M + 1.

So one of the two words has at least (M+1)/2 trees.

## Step 6 — Conclusion

Take M = 2k + 2. Some word in the slice has at least k + 2 > k trees. So the grammar is not
k-ambiguous. Since k was arbitrary, no grammar for the primitive words is finitely ambiguous. ∎

---

### Where each step is formalised (Lean, `finitely-ambiguous/lean/FiniteAmbiguity/`)

| Step | Lean |
|---|---|
| 1 Slice | `Slice.lean` (`slice_primitive_iff`) |
| 2 Structure | `ToCNF.lean`, `CNFStructure.lean` + `S2_*.lean`, `SliceStructure.lean` |
| 3 Lemma X | `LemmaX.lean` |
| 4–5 Half-spaces | `Geometry.lean` + `G2_*.lean` |
| 6 Assembly | `Main.lean` (`primitive_not_finitelyAmbiguous`) |

Caveats: not peer-reviewed, and the novelty check was incomplete (see `NOVELTY.md`).
