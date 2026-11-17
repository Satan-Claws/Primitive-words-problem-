# Lean formalisation brief (shared by all formalisation agents)

Goal: remove every `sorry` from `finitely-ambiguous/lean/FiniteAmbiguity/`, so that
`FA.primitive_not_finitelyAmbiguous` (in `Main.lean`) depends only on `propext`,
`Classical.choice`, `Quot.sound`. The paper proof is `finitely-ambiguous/PROOF.md`
(read it, including the audit-fix sections and §7).

## Layout (Lean 4.36.0, Mathlib v4.36.0; project root `finitely-ambiguous/lean/`)
| File | Content | Owner |
|---|---|---|
| `Defs.lean` | words, `IsPrimitive`, `CFG`, `Tree`, `amb`, `CycleFree`, `sliceWord`, `blockWord`, `LamLinSet`, `ply` | frozen |
| `Slice.lean` | Lemma 1 — proved | frozen |
| `CNFDefs.lean` | `CNF`, `CTree`, `CNF.Valid`, `CNF.IsDerivFrom`, `CNF.Generates`, `CNF.amb` | frozen |
| `Prelude.lean` | shared Mathlib imports (pre-built) | frozen |
| `ToCNF.lean` | `to_cnf` | agent S1 |
| `CNFStructure.lean` | `cnf_structure_blocks` (structure lemma on block words `blockWord e`) | agent S2 |
| `SliceStructure.lean` | `cnf_structure` (restriction from block words to slice words) | agent S3 |
| `LemmaX.lean` | `diagVec`, `lemmaX` | agent G1 |
| `Geometry.lean` | `geometric_lemma` (uses `lemmaX`) | agent G2 |
| `Main.lean` | assembly — proved modulo the four theorems above | frozen |

## Rules
* Edit only your own file(s). You may create extra files named `FiniteAmbiguity/<YourTag>_*.lean`
  (e.g. `S2_Product.lean`) and import them from your file. Never edit frozen files or other
  agents' files. **Do not change the statement of your main theorem** (name, hypotheses,
  conclusion) — other files depend on it verbatim.
* Check your file with `cd lean && PATH=$HOME/.elan/bin:$PATH lake env lean FiniteAmbiguity/<File>.lean`.
  **Do not run `lake build`** (several agents share the workspace; concurrent builds clash),
  except `lake build FiniteAmbiguity.<YourHelperFile>` when a file of yours must be imported by
  another file of yours (then build only that module).
* Imports: `FiniteAmbiguity.*` and anything already built under
  `finitely-ambiguous/lean/.lake/packages/mathlib/.lake/build/lib/lean/` (check that the `.olean` exists). Do not
  trigger builds of new Mathlib modules.
* Forbidden: `sorry` in final code, `axiom`, `native_decide`, `implemented_by`, `@[extern]`,
  `unsafe`, changing options that weaken checking. `decide` is fine.
* Before reporting, run `#print axioms <your theorem>` (in a scratch file outside `FiniteAmbiguity/`, e.g.
  `/tmp/claude-0/<tag>_ax.lean` with `import FiniteAmbiguity.<File>`) and report the output.
  For that, you may `lake build FiniteAmbiguity.<File>` once at the end.
* If you discover the statement you own is FALSE or unprovable as stated, stop and report a
  precise counterexample/explanation rather than weakening it.
* Report: what is proved, the axioms output, line count, and any remaining `sorry` with an exact
  description of what it needs. No vague status reports.

## Conventions
* `Fin (M + M)`: coordinate `Fin.castAdd M i` is `x_i` (block i+1 of the first half), `Fin.natAdd M i`
  is `y_i`. All `x` coordinates precede all `y` coordinates, so the order used for "crossing" in
  `LamLinSet.laminar` is the order of blocks in the word.
* `sliceWord p = half x ++ half y`, `half x = a · (a b^{x_1}) ⋯ (a b^{x_M})` (`false = a`, `true = b`).
