/-
# Main theorem: the primitive words have no finitely ambiguous grammar

The proof is assembled from three ingredients (see `research/finite_ambiguity/PROOF.md`):

* `slice_primitive_iff` (Lemma 1, **proved** in `Slice.lean`);
* `structure_lemma` (§2–§3 of PROOF.md: CNF conversion, product with a DFA, and the
  Ginsburg–Ullian-type structure of finitely ambiguous grammars of bounded languages) — **`sorry`**;
* `geometric_lemma` (§4–§5 of PROOF.md: Lemma X and the half-space covering argument) — **`sorry`**.

The final assembly `primitive_not_finitelyAmbiguous` is proved from these without further gaps.
-/
import FiniteAmbiguity.Slice

namespace FA

/-- **Structure lemma (specialised to the slice).** If `G` is cycle-free and `k`-ambiguous, then
for every `M` the tree counts of the slice words are the ply of a finite list of laminar simple
linear sets, all of whose points have positive coordinates.

PROOF.md §2–§3. Not yet formalised. -/
theorem structure_lemma (G : CFG) (hcf : G.CycleFree) (k : ℕ) (hk : G.KAmbiguous k) (M : ℕ) :
    ∃ Ls : List (LamLinSet (M + M)),
      (∀ L ∈ Ls, ∀ p, L.Mem p → ∀ i, 1 ≤ p i) ∧
      ∀ p : Fin (M + M) → ℕ, (∀ i, 1 ≤ p i) → G.amb (sliceWord p) = (ply Ls p : ℕ∞) := by
  sorry

/-- **Geometric lemma.** Let laminar simple linear sets in `ℕ^{M+M}` (coordinates `x₁…x_M,y₁…y_M`)
avoid the diagonal `x = y`, and cover every positive off-diagonal point. Then some point is covered
at least `⌈(M+1)/2⌉ = (M+2)/2` times.

PROOF.md §4–§5. Not yet formalised. -/
theorem geometric_lemma (M : ℕ) (hM : 1 ≤ M) (Ls : List (LamLinSet (M + M)))
    (hdiag : ∀ L ∈ Ls, ∀ p, L.Mem p →
      (fun i => p (Fin.castAdd M i)) ≠ (fun i => p (Fin.natAdd M i)))
    (hcover : ∀ p : Fin (M + M) → ℕ, (∀ i, 1 ≤ p i) →
      (fun i => p (Fin.castAdd M i)) ≠ (fun i => p (Fin.natAdd M i)) → 1 ≤ ply Ls p) :
    ∃ p, (M + 2) / 2 ≤ ply Ls p := by
  sorry

lemma exists_mem_of_ply_pos {n : ℕ} {Ls : List (LamLinSet n)} {p : Fin n → ℕ}
    (h : 1 ≤ ply Ls p) : ∃ L ∈ Ls, L.Mem p := by
  classical
  unfold ply at h
  obtain ⟨L, hL, hp⟩ := List.countP_pos_iff.mp (Nat.lt_of_lt_of_le Nat.zero_lt_one h)
  exact ⟨L, hL, of_decide_eq_true hp⟩

lemma ply_pos_of_mem {n : ℕ} {Ls : List (LamLinSet n)} {p : Fin n → ℕ} {L : LamLinSet n}
    (hL : L ∈ Ls) (hp : L.Mem p) : 1 ≤ ply Ls p := by
  classical
  unfold ply
  exact List.countP_pos_iff.mpr ⟨L, hL, by simpa using hp⟩

/-- `amb_G(w) ≥ 1` iff `w ∈ L(G)`. -/
lemma one_le_amb_iff (G : CFG) (w : Word) : 1 ≤ G.amb w ↔ G.Generates w := by
  rw [CFG.amb, Set.one_le_encard_iff_nonempty]
  rfl

/-- **Main theorem.** No cycle-free context-free grammar generating exactly the primitive words
over `{a, b}` is finitely ambiguous. -/
theorem primitive_not_finitelyAmbiguous (G : CFG) (hcf : G.CycleFree)
    (hlang : ∀ w, G.Generates w ↔ IsPrimitive w) : ¬ G.FinitelyAmbiguous := by
  rintro ⟨k, hk⟩
  set M := 2 * k + 2 with hMdef
  obtain ⟨Ls, hpos, hamb⟩ := structure_lemma G hcf k hk M
  -- every member of a linear set is a primitive slice word, hence off-diagonal
  have hdiag : ∀ L ∈ Ls, ∀ p, L.Mem p →
      (fun i => p (Fin.castAdd M i)) ≠ (fun i => p (Fin.natAdd M i)) := by
    intro L hL p hp
    have hp1 := hpos L hL p hp
    rw [← slice_primitive_iff p hp1, ← hlang, ← one_le_amb_iff, hamb p hp1]
    exact_mod_cast ply_pos_of_mem hL hp
  -- every positive off-diagonal point is a primitive word, hence has a tree
  have hcover : ∀ p : Fin (M + M) → ℕ, (∀ i, 1 ≤ p i) →
      (fun i => p (Fin.castAdd M i)) ≠ (fun i => p (Fin.natAdd M i)) → 1 ≤ ply Ls p := by
    intro p hp hxy
    have h1 : 1 ≤ G.amb (sliceWord p) :=
      (one_le_amb_iff G _).mpr ((hlang _).mpr ((slice_primitive_iff p hp).mpr hxy))
    rw [hamb p hp] at h1
    exact_mod_cast h1
  obtain ⟨p, hp⟩ := geometric_lemma M (by omega) Ls hdiag hcover
  -- that point has more than `k` trees
  obtain ⟨L, hL, hmem⟩ := exists_mem_of_ply_pos (le_trans (by omega) hp)
  have hp1 := hpos L hL p hmem
  have hle := hk (sliceWord p)
  rw [hamb p hp1] at hle
  have : ply Ls p ≤ k := by exact_mod_cast hle
  omega

end FA
