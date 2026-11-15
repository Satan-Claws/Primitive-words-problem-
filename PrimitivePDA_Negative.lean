/- A self-contained Lean 4 statement of the primitive-word PDA problem.
   No claim is made that the open conjecture is proved.

   Revision note: in the previous version a `PDA` could have infinitely many
   states and rules, so `PrimitiveIsContextFree` was trivially provable (store
   the whole input in the state, take `final := Primitive`) and the negative
   conjecture was false. The machine is now required to be finite: finite state
   and stack alphabets, a `Finset` of rules and a `Finset` of final states.
   A second statement uses Mathlib's `ContextFreeGrammar` / `Language.IsContextFree`. -/

import Mathlib

namespace PrimitivePDA

abbrev Symbol := Bool
abbrev Word := List Symbol

/-- Concatenate `base` with itself `n` times. -/
def power (base : Word) : Nat → Word
  | 0 => []
  | n + 1 => base ++ power base n

/-- A nonempty word that is a proper power. -/
def ProperPower (w : Word) : Prop :=
  ∃ (u : Word) (k : Nat), u ≠ [] ∧ 2 ≤ k ∧ w = power u k

/-- Primitive words are nonempty words that are not proper powers. -/
def Primitive (w : Word) : Prop := w ≠ [] ∧ ¬ ProperPower w

theorem empty_not_primitive : ¬ Primitive [] := by
  intro h
  exact h.1 rfl

/-- PDA transition: input may be consumed, or an epsilon step may be taken.
    The stack is represented with its top at the head of a list. -/
structure Rule (State Stack : Type) where
  source : State
  input : Option Symbol
  pop : Option Stack
  target : State
  push : List Stack

/-- A *finite* pushdown automaton. Finiteness of the state set, the stack
    alphabet and the transition relation is what makes this a PDA; without it
    every language over `Bool` is accepted by some machine. -/
structure PDA where
  State : Type
  Stack : Type
  [stateFintype : Fintype State]
  [stackFintype : Fintype Stack]
  [stateDecEq : DecidableEq State]
  [stackDecEq : DecidableEq Stack]
  initial : State
  bottom : Stack
  final : Finset State
  rules : Finset (Rule State Stack)

attribute [instance] PDA.stateFintype PDA.stackFintype
  PDA.stateDecEq PDA.stackDecEq

structure Config (M : PDA) where
  state : M.State
  remaining : Word
  stack : List M.Stack

/-- A single step, consuming zero or one input symbol. -/
inductive Step (M : PDA) : Config M → Config M → Prop where
  | epsilon (r : Rule M.State M.Stack) (xs : Word) (stk : List M.Stack)
      (hr : r ∈ M.rules) (hi : r.input = none)
      (hs : r.pop = none ∨
            ∃ t rest, r.pop = some t ∧ stk = t :: rest) :
      Step M
        ⟨r.source, xs, stk⟩
        ⟨r.target, xs,
          r.push ++ (if r.pop.isSome then stk.drop 1 else stk)⟩
  | consume (r : Rule M.State M.Stack) (a : Symbol)
      (xs : Word) (stk : List M.Stack)
      (hr : r ∈ M.rules) (hi : r.input = some a)
      (hs : r.pop = none ∨
            ∃ t rest, r.pop = some t ∧ stk = t :: rest) :
      Step M
        ⟨r.source, a :: xs, stk⟩
        ⟨r.target, xs,
          r.push ++ (if r.pop.isSome then stk.drop 1 else stk)⟩

/-- Zero or more PDA steps. -/
inductive Runs (M : PDA) : Config M → Config M → Prop where
  | refl (c : Config M) : Runs M c c
  | next {c d e : Config M} : Step M c d → Runs M d e → Runs M c e

/-- Acceptance by final state after consuming the entire input. -/
def Accepts (M : PDA) (w : Word) : Prop :=
  ∃ (q : M.State) (stk : List M.Stack),
    Runs M ⟨M.initial, w, [M.bottom]⟩ ⟨q, [], stk⟩ ∧ q ∈ M.final

/-- The existence of a (finite) PDA for the binary primitive-word language. -/
def PrimitiveIsContextFree : Prop :=
  ∃ M : PDA, ∀ w : Word, Accepts M w ↔ Primitive w

/-- The negative answer to the primitive-words open problem.
    OPEN CONJECTURE: the proof is deliberately missing. -/
theorem primitive_not_context_free : ¬ PrimitiveIsContextFree := by
  sorry

/-- Expanded form: no PDA accepts exactly the primitive words.
    Follows from the conjecture above, so it is NOT an unconditional
    verified result while that proof uses `sorry`. -/
theorem no_pda_for_primitive :
    ∀ M : PDA, ∃ w : Word, ¬ (Accepts M w ↔ Primitive w) := by
  intro M
  exact Classical.byContradiction fun h => primitive_not_context_free
    ⟨M, fun w => Classical.byContradiction fun hw => h ⟨w, hw⟩⟩

/-! ### The same conjecture via Mathlib's context-free grammars

`ContextFreeGrammar` has a `Finset` of rules, so it is finite by construction.
This form doesn't depend on the hand-rolled PDA semantics above. -/

/-- The primitive words as a Mathlib `Language Bool`. -/
def primitiveLanguage : Language Bool := {w | Primitive w}

/-- OPEN CONJECTURE (grammar form): the primitive words are not context-free. -/
theorem primitive_not_isContextFree : ¬ primitiveLanguage.IsContextFree := by
  sorry

end PrimitivePDA
