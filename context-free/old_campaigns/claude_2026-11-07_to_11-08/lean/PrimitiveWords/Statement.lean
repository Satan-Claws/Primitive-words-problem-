/-
  Is the language of primitive words context-free?  (Dömösi–Horváth–Ito)

  FROZEN STATEMENT FILE. Agents must not edit this file. A solution is a
  separate file that imports this one and proves EXACTLY ONE of the two
  targets `Target.negative` or `Target.affirmative` (see README.md).

  Every definition below is either Mathlib's own (`Language`,
  `ContextFreeGrammar`, `Language.IsContextFree`) or one of the three short
  definitions in this file, which a human must audit:
  `IsPrimitive`, `primitiveWords`, and the two targets.
-/
import Mathlib.Computability.ContextFreeGrammar

namespace PrimitiveWords

/-- `w` is primitive iff it is non-empty and is not `u ^ n` for any `n ≠ 1`.
For `u = []` the power is `[]`, which is never a non-empty `w`, so that case
is vacuous. `n = 0` likewise gives `[]`. So this says exactly: `w ≠ ε`, and
`w = uⁿ` with `u ∈ Σ⁺` forces `n = 1`. -/
def IsPrimitive {α : Type*} (w : List α) : Prop :=
  w ≠ [] ∧ ∀ (u : List α) (n : ℕ), (List.replicate n u).flatten = w → n = 1

/-- The language of primitive words over the alphabet `α`. -/
def primitiveWords (α : Type*) : Language α :=
  {w | IsPrimitive w}

/-- NEGATIVE resolution: the primitive words over the binary alphabet `Bool`
are not context-free. By intersecting with the regular language
`{a, b}*`, this also gives every alphabet with at least 2 letters, so the
binary case suffices. -/
def Target.negative : Prop :=
  ¬ (primitiveWords Bool).IsContextFree

/-- AFFIRMATIVE resolution: for every finite alphabet with at least two
letters, the primitive words are context-free. -/
def Target.affirmative : Prop :=
  ∀ (α : Type) [Fintype α], 2 ≤ Fintype.card α → (primitiveWords α).IsContextFree

/-! ### Sanity checks on the definitions (these must stay provable) -/

/-- `abab = (ab)²` is not primitive. -/
theorem not_primitive_abab : ¬ IsPrimitive [true, false, true, false] := by
  rintro ⟨-, h⟩
  have := h [true, false] 2 (by decide)
  omega

/-- The empty word is not primitive. -/
theorem not_primitive_nil {α : Type*} : ¬ IsPrimitive ([] : List α) :=
  fun h => h.1 rfl

/-- A single letter is primitive. -/
theorem primitive_single {α : Type*} (a : α) : IsPrimitive [a] := by
  refine ⟨List.cons_ne_nil _ _, fun u n h => ?_⟩
  have hlen := congrArg List.length h
  simp [List.length_flatten, List.map_replicate, List.sum_replicate] at hlen
  -- hlen : n * u.length = 1
  rcases Nat.mul_eq_one.mp hlen with ⟨hn, -⟩
  exact hn

end PrimitiveWords
