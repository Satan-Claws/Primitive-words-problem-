/-
# Conversion of a cycle-free grammar to CNF without increasing tree counts
(PROOF.md §2, Lemma 1.1 of research/reports/ambiguity.md.)  OWNER: agent S1.
-/
import FiniteAmbiguity.CNFDefs
import FiniteAmbiguity.Prelude

namespace FA

/-- Every cycle-free grammar has a CNF grammar with the same non-empty words and no more trees on
any word. -/
theorem to_cnf (G : CFG) (hcf : G.CycleFree) :
    ∃ C : CNF, (∀ w, w ≠ [] → (C.Generates w ↔ G.Generates w)) ∧ (∀ w, C.amb w ≤ G.amb w) := by
  sorry

end FA
