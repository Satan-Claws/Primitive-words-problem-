/-
# Definitions: primitive words, context-free grammars, derivation trees, ambiguity

Words are lists of `Bool`; `false` stands for the letter `a`, `true` for `b`.
-/
import Mathlib.Data.Set.Card
import Mathlib.Logic.Relation
import Mathlib.Algebra.BigOperators.Pi

namespace FA

/-- Words over `{a, b}`; `false = a`, `true = b`. -/
abbrev Word := List Bool

/-- `u` concatenated with itself `k` times. -/
def pow (u : Word) (k : ℕ) : Word := (List.replicate k u).flatten

/-- A word is primitive if it is non-empty and is not `u ^ k` with `k ≥ 2`.
(`k = 0` is excluded because then `w = []`.) -/
def IsPrimitive (w : Word) : Prop :=
  w ≠ [] ∧ ∀ (u : Word) (k : ℕ), w = pow u k → k = 1

/-- A context-free grammar over `{a, b}` with a finite set of nonterminals. -/
structure CFG where
  N : Type
  [fin : Fintype N]
  [dec : DecidableEq N]
  start : N
  rules : Finset (N × List (Bool ⊕ N))

attribute [instance] CFG.fin CFG.dec

/-- Derivation trees: leaves are terminal letters, inner nodes carry a nonterminal. -/
inductive Tree (N : Type) where
  | leaf : Bool → Tree N
  | node : N → List (Tree N) → Tree N

namespace Tree
variable {N : Type}

/-- The label of the root. -/
def root : Tree N → Bool ⊕ N
  | leaf c => .inl c
  | node A _ => .inr A

mutual
/-- The terminal word read off the leaves, left to right. -/
def yield : Tree N → Word
  | leaf c => [c]
  | node _ ts => yieldList ts
/-- Concatenated yields of a list of trees. -/
def yieldList : List (Tree N) → Word
  | [] => []
  | t :: ts => yield t ++ yieldList ts
end

end Tree

namespace CFG
variable (G : CFG)

mutual
/-- Every inner node `A` with children `t₁ … tₙ` uses a rule `A → root t₁ ⋯ root tₙ`. -/
def Valid : Tree G.N → Prop
  | .leaf _ => True
  | .node A ts => (A, ts.map Tree.root) ∈ G.rules ∧ ValidList ts
def ValidList : List (Tree G.N) → Prop
  | [] => True
  | t :: ts => Valid t ∧ ValidList ts
end

/-- `t` is a derivation tree of `w` from the start symbol. -/
def IsDerivation (t : Tree G.N) (w : Word) : Prop :=
  G.Valid t ∧ t.root = .inr G.start ∧ t.yield = w

/-- The language of `G`. -/
def Generates (w : Word) : Prop := ∃ t, G.IsDerivation t w

/-- `amb_G(w)`: the number of derivation trees of `w` (in `ℕ∞`, so infinitely many is allowed). -/
noncomputable def amb (w : Word) : ℕ∞ := {t | G.IsDerivation t w}.encard

/-- One derivation step on sentential forms. -/
def Step (u v : List (Bool ⊕ G.N)) : Prop :=
  ∃ A rhs l r, (A, rhs) ∈ G.rules ∧ u = l ++ [.inr A] ++ r ∧ v = l ++ rhs ++ r

/-- Cycle-free: no nonterminal derives itself in one or more steps. -/
def CycleFree : Prop := ∀ A : G.N, ¬ Relation.TransGen G.Step [.inr A] [.inr A]

/-- `G` is `k`-ambiguous: every word has at most `k` derivation trees. -/
def KAmbiguous (k : ℕ) : Prop := ∀ w, G.amb w ≤ k

/-- `G` is finitely ambiguous. -/
def FinitelyAmbiguous : Prop := ∃ k, G.KAmbiguous k

end CFG

/-! ## The slice `R_m = a (a b⁺)^M a (a b⁺)^M` -/

/-- `a b^n`. -/
def ab (n : ℕ) : Word := false :: List.replicate n true

/-- The word `a · (a b^{x_1}) ⋯ (a b^{x_M})` for a block vector `x`. -/
def half {M : ℕ} (x : Fin M → ℕ) : Word := false :: (List.ofFn fun i => ab (x i)).flatten

/-- The slice word `a (a b^{x_1}) ⋯ (a b^{x_M}) a (a b^{y_1}) ⋯ (a b^{y_M})`,
coded by `p = Fin.append x y : Fin (M + M) → ℕ` (x-blocks first, then y-blocks). -/
def sliceWord {M : ℕ} (p : Fin (M + M) → ℕ) : Word :=
  half (fun i => p (Fin.castAdd M i)) ++ half (fun i => p (Fin.natAdd M i))

/-- The block word `a b^{e_0} a b^{e_1} ⋯ a b^{e_{n-1}}`. -/
def blockWord {n : ℕ} (e : Fin n → ℕ) : Word := (List.ofFn fun i => ab (e i)).flatten

/-! ## Laminar simple linear sets (the output of the structure lemma) -/

/-- A linear set `c + ℕ v₁ + ⋯ + ℕ v_r ⊆ ℕⁿ` with injective parametrisation, each period supported
on a pair of coordinates `s ≤ t`, and the pairs pairwise non-crossing. -/
structure LamLinSet (n : ℕ) where
  c : Fin n → ℕ
  r : ℕ
  v : Fin r → Fin n → ℕ
  pair : Fin r → Fin n × Fin n
  le : ∀ j, (pair j).1 ≤ (pair j).2
  supp : ∀ j i, v j i ≠ 0 → i = (pair j).1 ∨ i = (pair j).2
  nonzero : ∀ j, v j ≠ 0
  inj : Function.Injective fun q : Fin r → ℕ => ∑ j, q j • v j
  laminar : ∀ j j', ¬ ((pair j).1 < (pair j').1 ∧ (pair j').1 < (pair j).2 ∧
    (pair j).2 < (pair j').2)

namespace LamLinSet
variable {n : ℕ}

/-- Membership in the linear set. -/
def Mem (L : LamLinSet n) (p : Fin n → ℕ) : Prop := ∃ q : Fin L.r → ℕ, p = L.c + ∑ j, q j • L.v j

end LamLinSet

open Classical in
/-- Number of members of a list of linear sets that contain `p`. -/
noncomputable def ply {n : ℕ} (Ls : List (LamLinSet n)) (p : Fin n → ℕ) : ℕ :=
  Ls.countP fun L => decide (L.Mem p)

end FA
