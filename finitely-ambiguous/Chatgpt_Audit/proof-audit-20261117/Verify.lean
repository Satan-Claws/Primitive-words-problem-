/- Independent audit of repository commit eb029bfcc22cb584121620477d9a0c54a6e3dcfb.
The next three proofs copy the original proof bodies, removing only the unused
CycleFree assumption and renaming the resulting theorems. Original files are unchanged.
-/
import FiniteAmbiguity.Main

namespace FA.Audit

open FA.S1 in
theorem to_cnf_unrestricted (G : CFG) :
    ∃ C : CNF, (∀ w, w ≠ [] → (C.Generates w ↔ G.Generates w)) ∧ (∀ w, C.amb w ≤ G.amb w) := by
  -- Every CNF derivation of `w` is the normal form of a `G`-derivation of `w`.
  have key : ∀ w t, (cnf G).IsDerivFrom (cnf G).start t w →
      ∃ s, G.IsDerivation s w ∧ norm G s = some t := by
    rintro w t ⟨hv, hroot, hy⟩
    obtain ⟨s, hsr, hsv, hs⟩ := realized_sym (realized_of_valid t hv) hroot
    exact ⟨s, ⟨hsv, hsr, (norm_yield hs).symm.trans hy⟩, hs⟩
  refine ⟨cnf G, fun w hw => ⟨?_, ?_⟩, fun w => ?_⟩
  · rintro ⟨t, ht⟩
    obtain ⟨s, hs, -⟩ := key w t ht
    exact ⟨s, hs⟩
  · rintro ⟨s, hv, hroot, hy⟩
    obtain ⟨t, ht⟩ : ∃ t, norm G s = some t := by
      cases h : norm G s with
      | none => exact absurd ((norm_eq_none.1 h).symm.trans hy).symm hw
      | some t => exact ⟨t, rfl⟩
    refine ⟨t, ?_, ?_, ?_⟩
    · rw [← relabel_self t]
      have := norm_valid s hv t ht
      exact valid_relabel (by rw [norm_root ht]; exact this.1) this.2
    · exact (norm_root ht).trans (by rw [hroot]; rfl)
    · exact (norm_yield ht).trans hy
  · unfold CNF.amb CFG.amb
    let f : Tree G.N → CTree (cnf G).N := fun s => (norm G s).getD (.leaf (cnf G).start false)
    calc {t | (cnf G).IsDerivFrom (cnf G).start t w}.encard
        ≤ (f '' {s | G.IsDerivation s w}).encard := by
          apply Set.encard_le_encard
          intro t ht
          obtain ⟨s, hs, hn⟩ := key w t ht
          exact ⟨s, hs, by show (norm G s).getD _ = t; rw [hn]; rfl⟩
      _ ≤ _ := Set.encard_image_le _ _


theorem structure_lemma_unrestricted (G : CFG) (k : ℕ) (hk : G.KAmbiguous k) (M : ℕ) :
    ∃ Ls : List (LamLinSet (M + M)),
      (∀ p : Fin (M + M) → ℕ, 1 ≤ ply Ls p ↔ G.Generates (sliceWord p)) ∧
      (∀ p : Fin (M + M) → ℕ, ply Ls p ≤ k) := by
  obtain ⟨C, hgen, hamb⟩ := to_cnf_unrestricted G
  have hkC : ∀ w, C.amb w ≤ k := fun w => (hamb w).trans (hk w)
  obtain ⟨Ls, heq⟩ := cnf_structure C k hkC M
  refine ⟨Ls, fun p => ?_, fun p => ?_⟩
  · rw [← hgen _ (sliceWord_ne_nil p), ← CNF.one_le_amb_iff, heq p]
    exact_mod_cast Iff.rfl
  · have := hkC (sliceWord p)
    rw [heq p] at this
    exact_mod_cast this


theorem primitive_not_finitelyAmbiguous_unrestricted (G : CFG)
    (hlang : ∀ w, G.Generates w ↔ IsPrimitive w) : ¬ G.FinitelyAmbiguous := by
  rintro ⟨k, hk⟩
  set M := 2 * k + 2 with hMdef
  obtain ⟨Ls, hgen, hle⟩ := structure_lemma_unrestricted G k hk M
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


/-- Language-level formulation: no CFG for Q has a uniform finite ambiguity bound. -/
theorem no_finitely_ambiguous_grammar_for_Q :
    ¬ ∃ G : CFG, (∀ w, G.Generates w ↔ IsPrimitive w) ∧ G.FinitelyAmbiguous := by
  rintro ⟨G, hlang, hfin⟩
  exact primitive_not_finitelyAmbiguous_unrestricted G hlang hfin

/-- Explicit quantifiers: every bound is exceeded on a primitive word. -/
theorem arbitrarily_many_parses (G : CFG)
    (hlang : ∀ w, G.Generates w ↔ IsPrimitive w) (k : ℕ) :
    ∃ w : Word, IsPrimitive w ∧ (k : ℕ∞) < G.amb w := by
  classical
  have hnot : ¬ ∀ w, G.amb w ≤ (k : ℕ∞) := by
    intro hk
    exact primitive_not_finitelyAmbiguous_unrestricted G hlang ⟨k, hk⟩
  push_neg at hnot
  obtain ⟨w, hw⟩ := hnot
  refine ⟨w, (hlang w).mp ((FA.one_le_amb_iff G w).mp ?_), hw⟩
  have hpos : 0 < G.amb w := lt_of_le_of_lt (by simp) hw
  exact Order.one_le_iff_pos.mpr hpos

end FA.Audit

#print axioms FA.primitive_not_finitelyAmbiguous
#print axioms FA.Audit.primitive_not_finitelyAmbiguous_unrestricted
#print axioms FA.Audit.no_finitely_ambiguous_grammar_for_Q
#print axioms FA.Audit.arbitrarily_many_parses
#check FA.Audit.no_finitely_ambiguous_grammar_for_Q
#check FA.Audit.arbitrarily_many_parses
