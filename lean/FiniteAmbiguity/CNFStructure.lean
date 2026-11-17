/-
# Structure of finitely ambiguous CNF grammars on block words
(PROOF.md §3, Lemma 3.)  OWNER: agent S2.
-/
import FiniteAmbiguity.CNFDefs
import FiniteAmbiguity.Prelude

namespace FA

/-- **Structure lemma.** If a CNF grammar is `k`-ambiguous then, for every `n`, its tree count on
block words `a b^{e_0} ⋯ a b^{e_{n-1}}` is the ply of a finite list of laminar simple linear sets. -/
theorem cnf_structure_blocks (C : CNF) (k : ℕ) (hk : ∀ w, C.amb w ≤ k) (n : ℕ) :
    ∃ Ls : List (LamLinSet n), ∀ e : Fin n → ℕ, C.amb (blockWord e) = (ply Ls e : ℕ∞) := by
  sorry

end FA
