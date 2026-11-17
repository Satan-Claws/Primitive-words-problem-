# Lean formalisation: the primitive words are not finitely ambiguous

Main theorem (`FiniteAmbiguity/Main.lean`):

```lean
theorem FA.primitive_not_finitelyAmbiguous (G : CFG) (hcf : G.CycleFree)
    (hlang : ∀ w, G.Generates w ↔ IsPrimitive w) : ¬ G.FinitelyAmbiguous
```

`#print axioms FA.primitive_not_finitelyAmbiguous` gives `[propext, Classical.choice, Quot.sound]`
— no `sorry`. Lean 4.36.0, Mathlib v4.36.0. Build: `lake build` (toolchain from
`lean-toolchain`).

Definitions to review (`Defs.lean`): words over `Bool` (`false = a`), `IsPrimitive`, `CFG` (finite
nonterminals, `Finset` of rules), derivation `Tree`s, `amb` (number of derivation trees, in `ℕ∞`),
`CycleFree`, `KAmbiguous`, `FinitelyAmbiguous`.

| File | Content |
|---|---|
| `Defs.lean`, `CNFDefs.lean` | definitions |
| `Slice.lean` | Lemma 1: slice word primitive ⇔ halves differ |
| `ToCNF.lean` | CNF conversion never increasing tree counts |
| `CNFStructure.lean`, `S2_*.lean` | structure lemma: tree counts on block words = ply of laminar simple linear sets |
| `SliceStructure.lean` | restriction to slice words |
| `LemmaX.lean` | Lemma 4.1 / Lemma X |
| `Geometry.lean`, `G2_*.lean` | half-space covering argument |
| `Main.lean` | assembly |
