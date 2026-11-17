/-
# From block words to slice words.  OWNER: agent S3.
Slice words are block words with two forced zero blocks; restrict the linear sets accordingly.
-/
import FiniteAmbiguity.CNFStructure

namespace FA

/-- The structure lemma on slice words. -/
theorem cnf_structure (C : CNF) (k : ℕ) (hk : ∀ w, C.amb w ≤ k) (M : ℕ) :
    ∃ Ls : List (LamLinSet (M + M)),
      ∀ p : Fin (M + M) → ℕ, C.amb (sliceWord p) = (ply Ls p : ℕ∞) := by
  sorry

end FA
