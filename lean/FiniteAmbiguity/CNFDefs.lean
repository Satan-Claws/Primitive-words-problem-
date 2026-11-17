/-
# Chomsky normal form grammars (shared interface)

A CNF grammar has binary rules `A → B C` and terminal rules `A → c`; it never derives `[]`.
Its derivation trees form a plain (non-nested) inductive type, which keeps tree surgery simple.
-/
import FiniteAmbiguity.Defs

namespace FA

/-- A grammar in Chomsky normal form over `{a, b}`. -/
structure CNF where
  N : Type
  [fin : Fintype N]
  [dec : DecidableEq N]
  start : N
  bin : Finset (N × N × N)
  term : Finset (N × Bool)

attribute [instance] CNF.fin CNF.dec

/-- Binary derivation trees. -/
inductive CTree (N : Type) where
  | leaf : N → Bool → CTree N
  | node : N → CTree N → CTree N → CTree N
  deriving DecidableEq

namespace CTree
variable {N : Type}

/-- Root label. -/
def root : CTree N → N
  | leaf A _ => A
  | node A _ _ => A

/-- Yield. -/
def yield : CTree N → Word
  | leaf _ c => [c]
  | node _ l r => l.yield ++ r.yield

end CTree

namespace CNF
variable (C : CNF)

/-- Every node uses a rule of `C`. -/
def Valid : CTree C.N → Prop
  | .leaf A c => (A, c) ∈ C.term
  | .node A l r => (A, l.root, r.root) ∈ C.bin ∧ Valid l ∧ Valid r

/-- `t` is a derivation tree of `w` from `X`. -/
def IsDerivFrom (X : C.N) (t : CTree C.N) (w : Word) : Prop :=
  C.Valid t ∧ t.root = X ∧ t.yield = w

/-- Generated language. -/
def Generates (w : Word) : Prop := ∃ t, C.IsDerivFrom C.start t w

/-- Number of derivation trees of `w` from the start symbol. -/
noncomputable def amb (w : Word) : ℕ∞ := {t | C.IsDerivFrom C.start t w}.encard

end CNF

end FA
