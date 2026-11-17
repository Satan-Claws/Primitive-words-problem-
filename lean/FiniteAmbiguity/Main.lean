/-
# Main theorem: the primitive words have no finitely ambiguous grammar

The proof is assembled from three ingredients (see `research/finite_ambiguity/PROOF.md`):

* `slice_primitive_iff` (Lemma 1, `Slice.lean`);
* `to_cnf` (CNF conversion, `ToCNF.lean`) and `cnf_structure` (§3, `CNFStructure.lean`),
  combined below into `structure_lemma`;
* `geometric_lemma` (§4–§5, `Geometry.lean`, using `lemmaX` from `LemmaX.lean`).

The final assembly `primitive_not_finitelyAmbiguous` is proved from these without further gaps.
-/
import FiniteAmbiguity.Slice
import FiniteAmbiguity.ToCNF
import FiniteAmbiguity.SliceStructure
import FiniteAmbiguity.Geometry

namespace FA

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

/-- `amb_C(w) ≥ 1` iff `w ∈ L(C)` for CNF grammars. -/
lemma CNF.one_le_amb_iff (C : CNF) (w : Word) : 1 ≤ C.amb w ↔ C.Generates w := by
  rw [CNF.amb, Set.one_le_encard_iff_nonempty]
  rfl

lemma sliceWord_ne_nil {M : ℕ} (p : Fin (M + M) → ℕ) : sliceWord p ≠ [] := by
  simp [sliceWord, half]

/-- **Structure lemma (specialised to the slice).** If `G` is cycle-free and `k`-ambiguous then,
for every `M`, there are laminar simple linear sets whose ply detects membership of slice words
in `L(G)` and is at most `k`. -/
theorem structure_lemma (G : CFG) (hcf : G.CycleFree) (k : ℕ) (hk : G.KAmbiguous k) (M : ℕ) :
    ∃ Ls : List (LamLinSet (M + M)),
      (∀ p : Fin (M + M) → ℕ, 1 ≤ ply Ls p ↔ G.Generates (sliceWord p)) ∧
      (∀ p : Fin (M + M) → ℕ, ply Ls p ≤ k) := by
  obtain ⟨C, hgen, hamb⟩ := to_cnf G hcf
  have hkC : ∀ w, C.amb w ≤ k := fun w => (hamb w).trans (hk w)
  obtain ⟨Ls, heq⟩ := cnf_structure C k hkC M
  refine ⟨Ls, fun p => ?_, fun p => ?_⟩
  · rw [← hgen _ (sliceWord_ne_nil p), ← CNF.one_le_amb_iff, heq p]
    exact_mod_cast Iff.rfl
  · have := hkC (sliceWord p)
    rw [heq p] at this
    exact_mod_cast this

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
  obtain ⟨Ls, hgen, hle⟩ := structure_lemma G hcf k hk M
  -- every member of a linear set is a primitive slice word, hence off-diagonal
  have hdiag : ∀ L ∈ Ls, ∀ p, L.Mem p →
      (fun i => p (Fin.castAdd M i)) ≠ (fun i => p (Fin.natAdd M i)) := by
    intro L hL p hp hxy
    exact not_primitive_of_eq p hxy ((hlang _).mp ((hgen p).mp (ply_pos_of_mem hL hp)))
  -- every positive off-diagonal point is a primitive word, hence has a tree
  have hcover : ∀ p : Fin (M + M) → ℕ, (∀ i, 1 ≤ p i) →
      (fun i => p (Fin.castAdd M i)) ≠ (fun i => p (Fin.natAdd M i)) → 1 ≤ ply Ls p :=
    fun p hp hxy => (hgen p).mpr ((hlang _).mpr ((slice_primitive_iff p hp).mpr hxy))
  obtain ⟨p, hp⟩ := geometric_lemma M (by omega) Ls hdiag hcover
  -- that point is covered more than `k` times
  have := hle p
  omega

end FA
