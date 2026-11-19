# Lean target: are the primitive words context-free?

`PrimitiveWords/Statement.lean` is the **frozen** statement. It defines `IsPrimitive`, `primitiveWords`, and two targets:

- `Target.negative : Prop := ¬ (primitiveWords Bool).IsContextFree`
- `Target.affirmative : Prop := ∀ α [Fintype α], 2 ≤ card α → (primitiveWords α).IsContextFree`

A solution proves exactly one of these, in a separate file:

```lean
import PrimitiveWords.Statement
theorem solution : PrimitiveWords.Target.negative := by
  ...
```

**Not yet typechecked.** This file has not been built against Mathlib. Run `lake build` once before any proof work. A sanity proof such as `primitive_single` may need a renamed `simp` lemma, but the definitions and targets should not change.

**No `sorry` in `Statement.lean` does not mean anything is proved.** The targets are `def`s (propositions), not theorems. A solution is a separate `theorem` whose type is exactly `PrimitiveWords.Target.negative` (or `.affirmative`), with a complete proof.

`Language.IsContextFree` is Mathlib's own definition: some `ContextFreeGrammar` (with a finite `Finset` of rules) generates exactly `L`. Nothing about grammars is redefined here.

## Human audit of the statement (do this once, before trusting any proof)

1. `IsPrimitive w ↔ w ≠ [] ∧ ∀ u n, uⁿ = w → n = 1`. Check that ε is excluded, that `n = 0` and `u = []` are vacuous, and that exponent 1 is allowed.
2. Check that Mathlib's `ContextFreeGrammar.language` / `Generates` / `Derives` is the standard derivation relation. Pin the Mathlib commit in `lake-manifest.json` and read the definitions at that commit.
3. Run the sanity theorems in the file. They show `abab` is not primitive, `ε` is not primitive, and single letters are primitive.

## Acceptance check for an agent's proof (all must pass)

1. **Fresh checkout.** Clone this project at the pinned Mathlib commit into a clean directory. Copy in **only** the agent's proof file. Never reuse the agent's working tree: it could contain modified Mathlib sources in `.lake/packages`.
2. **The statement file must be byte-identical** to the frozen one: `sha256sum PrimitiveWords/Statement.lean` must match the recorded hash:
   `1ae01f2fced7733160024e6096ff47cc5aa3497b974fcbd724444608bee12d59`
   If a sanity proof has to be fixed after the first build, record the new hash here, and check that the diff touches only the sanity proofs.
3. **It must build:** `lake build` succeeds with no errors.
4. **Axioms.** Add `#print axioms solution`. The output must list only `propext`, `Classical.choice` and `Quot.sound`. Reject on any of the following:
   - `sorryAx` (an unfinished proof);
   - `Lean.ofReduceBool` (`native_decide`, which trusts the compiler);
   - any user-declared `axiom`.
5. **Kernel replay.** Run `lake env leanchecker` (shipped with the toolchain) on the solution module, so the kernel re-checks every declaration independently of the elaborator.
6. **Grep the proof file** for `axiom`, `sorry`, `native_decide`, `implemented_by`, `extern`, `unsafe`, `set_option debug`, `macro`, `elab` and `#eval`. Anything found must be justified by hand.

If all six pass, the theorem is proved as stated, with the trust base of the Lean kernel and Mathlib's definitions. Whether it answers the *mathematical* question depends only on the human audit above. It is about 20 lines.

For the result to be accepted as a solution of the open problem, also write a human-readable account of the argument. The Lean proof establishes that the result is correct; readers will want to see why it works.
