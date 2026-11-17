/-
# The geometric lemma (PROOF.md §5).  OWNER: agent G2.
-/
import FiniteAmbiguity.LemmaX

namespace FA

/-- **Geometric lemma.** Let laminar simple linear sets in `ℕ^{M+M}` (coordinates `x₁…x_M,y₁…y_M`)
avoid the diagonal `x = y`, and cover every positive off-diagonal point. Then some point is covered
at least `⌈(M+1)/2⌉ = (M+2)/2` times. -/
theorem geometric_lemma (M : ℕ) (hM : 1 ≤ M) (Ls : List (LamLinSet (M + M)))
    (hdiag : ∀ L ∈ Ls, ∀ p, L.Mem p →
      (fun i => p (Fin.castAdd M i)) ≠ (fun i => p (Fin.natAdd M i)))
    (hcover : ∀ p : Fin (M + M) → ℕ, (∀ i, 1 ≤ p i) →
      (fun i => p (Fin.castAdd M i)) ≠ (fun i => p (Fin.natAdd M i)) → 1 ≤ ply Ls p) :
    ∃ p, (M + 2) / 2 ≤ ply Ls p := by
  sorry

end FA
