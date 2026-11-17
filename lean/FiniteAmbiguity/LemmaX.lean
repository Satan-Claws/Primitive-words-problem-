/-
# Lemma 4.1 (non-interleaving) and Lemma X (PROOF.md §4).  OWNER: agent G1.
Coordinates of `Fin (M + M)`: `Fin.castAdd M i` is `x_i`, `Fin.natAdd M i` is `y_i`.
-/
import FiniteAmbiguity.Defs
import FiniteAmbiguity.Prelude

namespace FA

/-- The diagonal vector `e_{x_i} + e_{y_i}`. -/
def diagVec (M : ℕ) (i : Fin M) : Fin (M + M) → ℚ :=
  Pi.single (Fin.castAdd M i) 1 + Pi.single (Fin.natAdd M i) 1

/-- **Lemma X.** A family of non-negative vectors, each supported on a pair `s ≤ t`, with pairwise
non-crossing pairs, whose span contains every diagonal vector, spans a space of dimension at least
`2M - 1`. -/
theorem lemmaX {M : ℕ} {ι : Type*} (v : ι → Fin (M + M) → ℚ) (pair : ι → Fin (M + M) × Fin (M + M))
    (hle : ∀ j, (pair j).1 ≤ (pair j).2)
    (hnonneg : ∀ j i, 0 ≤ v j i)
    (hsupp : ∀ j i, v j i ≠ 0 → i = (pair j).1 ∨ i = (pair j).2)
    (hlam : ∀ j j', ¬ ((pair j).1 < (pair j').1 ∧ (pair j').1 < (pair j).2 ∧
      (pair j).2 < (pair j').2))
    (hW : ∀ i : Fin M, diagVec M i ∈ Submodule.span ℚ (Set.range v)) :
    M + M ≤ Module.finrank ℚ (Submodule.span ℚ (Set.range v)) + 1 := by
  sorry

end FA
