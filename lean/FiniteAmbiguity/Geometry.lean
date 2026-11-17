/-
# The geometric lemma (PROOF.md §5).  OWNER: agent G2.
Helper files: `G2_Basic.lean` (elementary lemmas), `G2_Lin.lean` (linear algebra of one linear set),
`G2_Classify.lean` (test points and the classification of one linear set).
-/
import FiniteAmbiguity.LemmaX
import FiniteAmbiguity.G2_Classify

namespace FA

open Filter G2 in
/-- **Geometric lemma.** Let laminar simple linear sets in `ℕ^{M+M}` (coordinates `x₁…x_M,y₁…y_M`)
avoid the diagonal `x = y`, and cover every positive off-diagonal point. Then some point is covered
at least `⌈(M+1)/2⌉ = (M+2)/2` times. -/
theorem geometric_lemma (M : ℕ) (hM : 1 ≤ M) (Ls : List (LamLinSet (M + M)))
    (hdiag : ∀ L ∈ Ls, ∀ p, L.Mem p →
      (fun i => p (Fin.castAdd M i)) ≠ (fun i => p (Fin.natAdd M i)))
    (hcover : ∀ p : Fin (M + M) → ℕ, (∀ i, 1 ≤ p i) →
      (fun i => p (Fin.castAdd M i)) ≠ (fun i => p (Fin.natAdd M i)) → 1 ≤ ply Ls p) :
    ∃ p, (M + 2) / 2 ≤ ply Ls p := by
  classical
  /- Step 1: a generic direction `ω`. -/
  let cs : Finset (Fin M → ℚ) := Ls.toFinset.biUnion fun L =>
    (Finset.univ.image fun j : Fin L.r => fun i => A L (diagVec M i) j) ∪
    (Finset.univ.image fun l : Fin (M + M) => fun i => R L (diagVec M i) l)
  obtain ⟨ω, hω1, hωgen⟩ := exists_generic cs
  have hgen : ∀ L ∈ Ls, (∀ j, A L (Ωq ω) j = 0 → ∀ i, A L (diagVec M i) j = 0) ∧
      (R L (Ωq ω) = 0 → ∀ i, R L (diagVec M i) = 0) := by
    intro L hL
    constructor
    · intro j hj
      by_contra hne
      push Not at hne
      obtain ⟨i₀, hi₀⟩ := hne
      have hc : (fun i => A L (diagVec M i) j) ∈ cs :=
        Finset.mem_biUnion.2 ⟨L, List.mem_toFinset.2 hL,
          Finset.mem_union_left _ (Finset.mem_image.2 ⟨j, Finset.mem_univ _, rfl⟩)⟩
      apply hωgen _ hc (fun h => hi₀ (congrFun h i₀))
      rw [Ωq_eq, map_sum] at hj
      simpa [Finset.sum_apply, mul_comm] using hj
    · intro hR i
      funext l
      by_contra hne
      have hc : (fun i => R L (diagVec M i) l) ∈ cs :=
        Finset.mem_biUnion.2 ⟨L, List.mem_toFinset.2 hL,
          Finset.mem_union_right _ (Finset.mem_image.2 ⟨l, Finset.mem_univ _, rfl⟩)⟩
      apply hωgen _ hc (fun h => hne (congrFun h i))
      rw [Ωq_eq, map_sum] at hR
      have := congrFun hR l
      simpa [Finset.sum_apply, mul_comm] using this
  /- Step 2: classify every linear set. -/
  have hdiag0 : ∀ L ∈ Ls, ∀ F s, ¬ memQ L (Xq F ω s 0) := by
    intro L hL F s hm
    have hY : ∀ k, 0 ≤ Y ω s 0 k := by
      intro k
      refine Fin.addCases (fun i => ?_) (fun i => ?_) k <;>
        simp only [Y, Fin.append_left, Fin.append_right, Pi.zero_apply, add_zero] <;> positivity
    rw [← Pn_cast F ω s 0 hY, ← mem_iff_memQ] at hm
    apply hdiag L hL _ hm
    funext i
    simp [-Fin.natAdd_eq_addNat, Pn, Y]
  have hcl : ∀ L ∈ Ls, ∃ D : ℕ, 0 < D ∧ ∃ B : ℚ, 0 ≤ B ∧ ∀ F : ℕ, D ∣ F → B < F →
      ∃ ψ : (Fin M → ℚ) →ₗ[ℚ] ℚ, ∀ δ : Fin M → ℤ, ∀ᶠ s in atTop,
        (memQ L (Xq F ω s δ) ↔ 0 < ψ (fun i => (δ i : ℚ))) :=
    fun L hL => classify L ω (hgen L hL).1 (hgen L hL).2 (hdiag0 L hL)
  choose! D hD B hB0 hB using hcl
  set N := ∑ L ∈ Ls.toFinset, (D L + ⌈B L⌉₊) + 1 with hNdef
  set F := N.factorial with hFdef
  have hF : ∀ L ∈ Ls, D L ∣ F ∧ B L < F := by
    intro L hL
    have hle : D L + ⌈B L⌉₊ ≤ ∑ L ∈ Ls.toFinset, (D L + ⌈B L⌉₊) :=
      Finset.single_le_sum (f := fun L => D L + ⌈B L⌉₊) (fun _ _ => Nat.zero_le _)
        (List.mem_toFinset.2 hL)
    have hN : N ≤ F := Nat.self_le_factorial N
    constructor
    · exact Nat.dvd_factorial (hD L hL) (by omega)
    · have h1 : B L ≤ ⌈B L⌉₊ := Nat.le_ceil _
      have h2 : (⌈B L⌉₊ : ℚ) < F := by exact_mod_cast (by omega : ⌈B L⌉₊ < F)
      linarith
  have hF1 : 1 ≤ F := Nat.one_le_iff_ne_zero.2 (Nat.factorial_ne_zero N)
  have hψex : ∀ L ∈ Ls, ∃ ψ : (Fin M → ℚ) →ₗ[ℚ] ℚ, ∀ δ : Fin M → ℤ, ∀ᶠ s in atTop,
      (memQ L (Xq F ω s δ) ↔ 0 < ψ (fun i => (δ i : ℚ))) :=
    fun L hL => hB L hL F (hF L hL).1 (hF L hL).2
  choose! ψ hψ using hψex
  /- Step 3: for each `δ`, eventually the ply is a count of signs. -/
  have hYev : ∀ δ : Fin M → ℤ, ∀ᶠ s in atTop, 1 ≤ s ∧ ∀ i, (δ i).natAbs + 1 ≤ s := by
    intro δ
    filter_upwards [eventually_ge_atTop 1,
      eventually_all.2 fun i => eventually_ge_atTop ((δ i).natAbs + 1)] with s h1 h2
    exact ⟨h1, h2⟩
  have hYpos : ∀ δ s, 1 ≤ s ∧ (∀ i, (δ i).natAbs + 1 ≤ s) → ∀ k, 1 ≤ Y ω s δ k := by
    rintro δ s ⟨hs, h⟩ k
    have hs' : (1 : ℤ) ≤ s := by exact_mod_cast hs
    refine Fin.addCases (fun i => ?_) (fun i => ?_) k <;>
      simp only [Y, Fin.append_left, Fin.append_right]
    · have : (1 : ℤ) ≤ ω i := by exact_mod_cast hω1 i
      nlinarith
    · have : (1 : ℤ) ≤ ω i := by exact_mod_cast hω1 i
      have h3 : ((δ i).natAbs : ℤ) + 1 ≤ s := by exact_mod_cast h i
      have h4 : -((δ i).natAbs : ℤ) ≤ δ i := by omega
      nlinarith
  have hply : ∀ δ : Fin M → ℤ, ∀ᶠ s in atTop,
      ply Ls (Pn F ω s δ) = Ls.countP (fun L => decide (0 < ψ L (fun i => (δ i : ℚ)))) := by
    intro δ
    have hall : ∀ᶠ s in atTop, ∀ L ∈ Ls.toFinset,
        (memQ L (Xq F ω s δ) ↔ 0 < ψ L (fun i => (δ i : ℚ))) :=
      (eventually_all_finset _).2 fun L hL => hψ L (List.mem_toFinset.1 hL) δ
    filter_upwards [hall, hYev δ] with s hs hY
    unfold ply
    apply List.countP_congr
    intro L hL
    simp only [decide_eq_true_eq]
    rw [mem_iff_memQ, Pn_cast F ω s δ (fun k => le_trans zero_le_one (hYpos δ s hY k))]
    exact hs L (List.mem_toFinset.2 hL)
  /- Step 4: every non-zero direction is covered. -/
  have hcov : ∀ δ : Fin M → ℤ, δ ≠ 0 → ∃ L ∈ Ls, 0 < ψ L (fun i => (δ i : ℚ)) := by
    intro δ hδ
    obtain ⟨s, hs1, hs2⟩ := ((hply δ).and (hYev δ)).exists
    have hF1' : (1 : ℤ) ≤ F := by exact_mod_cast hF1
    have hpos : ∀ k, 1 ≤ Pn F ω s δ k := by
      intro k
      have h1 := hYpos δ s hs2 k
      have h2 : (1 : ℤ) ≤ (F : ℤ) * Y ω s δ k := by nlinarith
      simp only [Pn]
      omega
    have hne : (fun i => Pn F ω s δ (Fin.castAdd M i)) ≠
        (fun i => Pn F ω s δ (Fin.natAdd M i)) := by
      intro h
      apply hδ
      funext i
      have h0 := congrFun h i
      have hx := hYpos δ s hs2 (Fin.castAdd M i)
      have hy := hYpos δ s hs2 (Fin.natAdd M i)
      simp only [Pn] at h0
      have e1 : 0 ≤ (F : ℤ) * Y ω s δ (Fin.castAdd M i) := by positivity
      have e2 : 0 ≤ (F : ℤ) * Y ω s δ (Fin.natAdd M i) := by positivity
      have h0' := congrArg (fun n : ℕ => (n : ℤ)) h0
      simp only [Int.toNat_of_nonneg e1, Int.toNat_of_nonneg e2] at h0'
      simp only [Y, Fin.append_left, Fin.append_right] at h0'
      have hF0 : (F : ℤ) ≠ 0 := by omega
      have : (F : ℤ) * δ i = 0 := by linarith
      exact (mul_eq_zero.1 this).resolve_left hF0
    have := hcover _ hpos hne
    rw [hs1] at this
    obtain ⟨L, hL, hLp⟩ := List.countP_pos_iff.1 this
    exact ⟨L, hL, by simpa using hLp⟩
  have hM1 := many_forms hM Ls ψ hcov
  /- Step 5: a generic direction `δ` and its opposite. -/
  obtain ⟨ω', -, hω'gen⟩ := exists_generic
    (Ls.toFinset.image fun L => fun i => ψ L (fun j => if i = j then 1 else 0))
  set δ : Fin M → ℤ := fun i => (ω' i : ℤ) with hδdef
  have hδgen : ∀ L ∈ Ls, ψ L ≠ 0 → ψ L (fun i => (δ i : ℚ)) ≠ 0 := by
    intro L hL hne h0
    apply hω'gen _ (Finset.mem_image.2 ⟨L, List.mem_toFinset.2 hL, rfl⟩)
    · intro hc
      apply hne
      apply LinearMap.ext
      intro x
      rw [LinearMap.pi_apply_eq_sum_univ]
      simp only [LinearMap.zero_apply]
      refine Finset.sum_eq_zero fun i _ => ?_
      have := congrFun hc i
      simp only [Pi.zero_apply] at this
      rw [this, smul_zero]
    · rw [LinearMap.pi_apply_eq_sum_univ] at h0
      simpa [δ, mul_comm] using h0
  have hsum := count_pm Ls ψ (fun i => (δ i : ℚ)) hδgen
  have hneg : (fun i => ((-δ) i : ℚ)) = -(fun i => (δ i : ℚ)) := by
    funext i
    simp
  obtain ⟨s, hs1, hs2⟩ := ((hply δ).and (hply (-δ))).exists
  rw [hneg] at hs2
  by_cases hc : (M + 2) / 2 ≤ Ls.countP (fun L => decide (0 < ψ L (fun i => (δ i : ℚ))))
  · exact ⟨_, hs1 ▸ hc⟩
  · refine ⟨Pn F ω s (-δ), ?_⟩
    rw [hs2]
    omega

end FA
