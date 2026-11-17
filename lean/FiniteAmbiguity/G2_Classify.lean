/-
# Test points and the per-set classification (agent G2).
Test points `P(s,δ) = F·(s ω, s ω + δ)`. For a fixed laminar linear set `L` (and generic `ω`), membership
of `P(s,δ)` is, for `s` large, decided by the sign of a linear form `ψ_L(δ)` (PROOF.md §5, cases 1–4).
-/
import FiniteAmbiguity.G2_Lin
import FiniteAmbiguity.LemmaX

namespace FA.G2
open Filter

variable {M : ℕ}

theorem castAdd_ne_natAdd' (i j : Fin M) : Fin.castAdd M i ≠ Fin.natAdd M j := by
  intro h
  have := congrArg Fin.val h
  simp [-Fin.natAdd_eq_addNat] at this
  omega

theorem natAdd_ne_castAdd' (i j : Fin M) : Fin.natAdd M i ≠ Fin.castAdd M j :=
  fun h => castAdd_ne_natAdd' j i h.symm

/-- Integer test vector `(s ω, s ω + δ)`. -/
def Y (ω : Fin M → ℕ) (s : ℕ) (δ : Fin M → ℤ) : Fin (M + M) → ℤ :=
  Fin.append (fun i => (s : ℤ) * ω i) (fun i => (s : ℤ) * ω i + δ i)

/-- Rational test point `F·(s ω, s ω + δ)`. -/
def Xq (F : ℕ) (ω : Fin M → ℕ) (s : ℕ) (δ : Fin M → ℤ) : Fin (M + M) → ℚ :=
  fun k => (F : ℚ) * (Y ω s δ k : ℚ)

/-- Natural test point. -/
def Pn (F : ℕ) (ω : Fin M → ℕ) (s : ℕ) (δ : Fin M → ℤ) : Fin (M + M) → ℕ :=
  fun k => ((F : ℤ) * Y ω s δ k).toNat

/-- `(ω, ω)`. -/
def Ωq (ω : Fin M → ℕ) : Fin (M + M) → ℚ :=
  Fin.append (fun i => (ω i : ℚ)) (fun i => (ω i : ℚ))

/-- `δ ↦ (0, δ)`. -/
def Eₗ : (Fin M → ℚ) →ₗ[ℚ] (Fin (M + M) → ℚ) where
  toFun δ := Fin.append 0 δ
  map_add' a b := by
    funext k
    refine Fin.addCases (fun i => ?_) (fun i => ?_) k <;> simp [-Fin.natAdd_eq_addNat]
  map_smul' c a := by
    funext k
    refine Fin.addCases (fun i => ?_) (fun i => ?_) k <;> simp [-Fin.natAdd_eq_addNat]

@[simp] theorem Eₗ_apply (δ : Fin M → ℚ) : (Eₗ : (Fin M → ℚ) →ₗ[ℚ] _) δ = Fin.append 0 δ := rfl

theorem Eₗ_cast (δ : Fin M → ℤ) :
    (Eₗ : (Fin M → ℚ) →ₗ[ℚ] _) (fun i => (δ i : ℚ)) =
      fun k => ((Fin.append (0 : Fin M → ℤ) δ k : ℤ) : ℚ) := by
  funext k
  refine Fin.addCases (fun i => ?_) (fun i => ?_) k <;> simp [-Fin.natAdd_eq_addNat]

theorem Y_cast (ω : Fin M → ℕ) (s : ℕ) (δ : Fin M → ℤ) :
    (fun k => (Y ω s δ k : ℚ)) = (s : ℚ) • Ωq ω + Eₗ (fun i => (δ i : ℚ)) := by
  funext k
  refine Fin.addCases (fun i => ?_) (fun i => ?_) k <;> simp [-Fin.natAdd_eq_addNat, Y, Ωq]

theorem Xq_eq (F : ℕ) (ω : Fin M → ℕ) (s : ℕ) (δ : Fin M → ℤ) :
    Xq F ω s δ = (F : ℚ) • fun k => (Y ω s δ k : ℚ) := by
  funext k
  simp [Xq]

theorem Xq_decomp (F : ℕ) (ω : Fin M → ℕ) (s : ℕ) (δ : Fin M → ℤ) :
    Xq F ω s δ = ((F : ℚ) * s) • Ωq ω + (F : ℚ) • Eₗ (fun i => (δ i : ℚ)) := by
  rw [Xq_eq, Y_cast, smul_add, smul_smul]

theorem Ωq_eq (ω : Fin M → ℕ) : Ωq ω = ∑ i, (ω i : ℚ) • diagVec M i := by
  funext k
  refine Fin.addCases (fun i => ?_) (fun i => ?_) k <;>
    simp [-Fin.natAdd_eq_addNat, castAdd_ne_natAdd', natAdd_ne_castAdd', Ωq, diagVec,
      Finset.sum_apply, Pi.single_apply]

theorem Pn_cast (F : ℕ) (ω : Fin M → ℕ) (s : ℕ) (δ : Fin M → ℤ) (h : ∀ k, 0 ≤ Y ω s δ k) :
    (fun k => (Pn F ω s δ k : ℚ)) = Xq F ω s δ := by
  funext k
  have h1 : 0 ≤ (F : ℤ) * Y ω s δ k := mul_nonneg (Int.natCast_nonneg F) (h k)
  have h2 : ((((F : ℤ) * Y ω s δ k).toNat : ℤ) : ℚ) = (((F : ℤ) * Y ω s δ k : ℤ) : ℚ) := by
    rw [Int.toNat_of_nonneg h1]
  simp only [Pn, Xq]
  push_cast at h2
  exact h2

/-! ### The classification of one linear set -/

theorem classify (L : LamLinSet (M + M)) (ω : Fin M → ℕ)
    (hgenA : ∀ j, A L (Ωq ω) j = 0 → ∀ i, A L (diagVec M i) j = 0)
    (hgenR : R L (Ωq ω) = 0 → ∀ i, R L (diagVec M i) = 0)
    (hdiag : ∀ F s, ¬ memQ L (Xq F ω s 0)) :
    ∃ D : ℕ, 0 < D ∧ ∃ B : ℚ, 0 ≤ B ∧ ∀ F : ℕ, D ∣ F → B < F →
      ∃ ψ : (Fin M → ℚ) →ₗ[ℚ] ℚ, ∀ δ : Fin M → ℤ, ∀ᶠ s in atTop,
        (memQ L (Xq F ω s δ) ↔ 0 < ψ (fun i => (δ i : ℚ))) := by
  classical
  obtain ⟨D1, hD1, hz1⟩ := exists_den_linear (A L)
  obtain ⟨D2, hD2, hz2⟩ := exists_den_linear (R L)
  set c := cq L with hc
  set Ω := Ωq ω with hΩ
  set D : ℕ := D1 * D2 with hD
  have hDpos : 0 < D := Nat.mul_pos hD1 hD2
  have hDq : (0 : ℚ) < D := by exact_mod_cast hDpos
  have hDA : ∀ (y : Fin (M + M) → ℤ) j, ∃ z : ℤ, (D : ℚ) * A L (fun k => (y k : ℚ)) j = z := by
    intro y j
    obtain ⟨z, hz⟩ := hz1 y j
    exact ⟨D2 * z, by rw [hD]; push_cast; rw [← hz]; ring⟩
  have hDR : ∀ (y : Fin (M + M) → ℤ) l, ∃ z : ℤ, (D : ℚ) * R L (fun k => (y k : ℚ)) l = z := by
    intro y l
    obtain ⟨z, hz⟩ := hz2 y l
    exact ⟨D1 * z, by rw [hD]; push_cast; rw [← hz]; ring⟩
  set B : ℚ := ∑ j, (D : ℚ) * |A L c j| + ∑ l, (D : ℚ) * |R L c l| with hB
  have hB0 : 0 ≤ B := by positivity
  have hBA : ∀ j, (D : ℚ) * |A L c j| ≤ B := by
    intro j
    have h1 : (D : ℚ) * |A L c j| ≤ ∑ j, (D : ℚ) * |A L c j| :=
      Finset.single_le_sum (f := fun j => (D : ℚ) * |A L c j|) (fun _ _ => by positivity)
        (Finset.mem_univ j)
    have h2 : 0 ≤ ∑ l, (D : ℚ) * |R L c l| := by positivity
    linarith
  have hBR : ∀ l, (D : ℚ) * |R L c l| ≤ B := by
    intro l
    have h1 : (D : ℚ) * |R L c l| ≤ ∑ l, (D : ℚ) * |R L c l| :=
      Finset.single_le_sum (f := fun l => (D : ℚ) * |R L c l|) (fun _ _ => by positivity)
        (Finset.mem_univ l)
    have h2 : 0 ≤ ∑ j, (D : ℚ) * |A L c j| := by positivity
    linarith
  refine ⟨D, hDpos, B, hB0, fun F hDF hBF => ?_⟩
  have hF0 : (0 : ℚ) < F := lt_of_le_of_lt hB0 hBF
  obtain ⟨t, ht⟩ := hDF
  have hFA : ∀ (y : Fin (M + M) → ℤ) j, ∃ z : ℤ, (F : ℚ) * A L (fun k => (y k : ℚ)) j = z := by
    intro y j
    obtain ⟨z, hz⟩ := hDA y j
    exact ⟨t * z, by rw [ht]; push_cast; rw [← hz]; ring⟩
  -- linear expansions
  have hXA : ∀ s δ j, A L (Xq F ω s δ - c) j =
      (F : ℚ) * A L Ω j * s + ((F : ℚ) * A L (Eₗ (fun i => (δ i : ℚ))) j - A L c j) := by
    intro s δ j
    rw [Xq_decomp, map_sub, map_add, map_smul, map_smul]
    simp only [Pi.sub_apply, Pi.add_apply, Pi.smul_apply, smul_eq_mul]
    ring
  have hXR : ∀ s δ, R L (Xq F ω s δ - c) =
      ((F : ℚ) * s) • R L Ω + ((F : ℚ) • R L (Eₗ (fun i => (δ i : ℚ))) - R L c) := by
    intro s δ
    rw [Xq_decomp, map_sub, map_add, map_smul, map_smul]
    abel
  have hXint : ∀ s δ j, ∃ z : ℤ, A L (Xq F ω s δ) j = z := by
    intro s δ j
    obtain ⟨z, hz⟩ := hFA (Y ω s δ) j
    refine ⟨z, ?_⟩
    rw [Xq_eq, map_smul, Pi.smul_apply, smul_eq_mul, hz]
  by_cases h1 : R L Ω = 0 ∧ ∀ j, 0 ≤ A L Ω j
  swap
  · -- Case 1: eventually no test point lies in `L`.
    refine ⟨0, fun δ => ?_⟩
    simp only [LinearMap.zero_apply, lt_self_iff_false, iff_false]
    rw [not_and_or] at h1
    rcases h1 with h | h
    · obtain ⟨l, hl⟩ : ∃ l, R L Ω l ≠ 0 := by
        by_contra hcon
        push Not at hcon
        exact h (funext hcon)
      filter_upwards [ev_ne (mul_ne_zero hF0.ne' hl)
        ((F : ℚ) * R L (Eₗ (fun i => (δ i : ℚ))) l - R L c l)] with s hs hm
      have := congrFun ((memQ_iff L _).1 hm).1 l
      rw [hXR] at this
      simp only [Pi.add_apply, Pi.smul_apply, Pi.sub_apply, smul_eq_mul, Pi.zero_apply] at this
      apply hs
      linarith
    · push Not at h
      obtain ⟨j, hj⟩ := h
      filter_upwards [ev_neg (mul_neg_of_pos_of_neg hF0 hj)
        ((F : ℚ) * A L (Eₗ (fun i => (δ i : ℚ))) j - A L c j)] with s hs hm
      obtain ⟨m, hm⟩ := ((memQ_iff L _).1 hm).2 j
      rw [hXA] at hm
      have : (0 : ℚ) ≤ m := by positivity
      linarith
  obtain ⟨hRΩ, hαnn⟩ := h1
  by_cases hpt : ∃ s₁ δ₁, memQ L (Xq F ω s₁ δ₁)
  swap
  · push Not at hpt
    refine ⟨0, fun δ => Eventually.of_forall fun s => ?_⟩
    simp [hpt s δ]
  obtain ⟨s₁, δ₁, hm₁⟩ := hpt
  obtain ⟨hR₁, hA₁⟩ := (memQ_iff L _).1 hm₁
  -- `R c = 0`
  have hRc : R L c = 0 := by
    funext l
    have e : R L c l = R L (Xq F ω s₁ δ₁) l := by
      have := congrFun hR₁ l
      rw [map_sub] at this
      simp only [Pi.sub_apply, Pi.zero_apply] at this
      linarith
    obtain ⟨z, hz⟩ := hDR (Y ω s₁ δ₁) l
    have hcz : (D : ℚ) * R L c l = F * z := by
      rw [e, Xq_eq, map_smul, Pi.smul_apply, smul_eq_mul, ← hz]
      ring
    have hz0 : z = 0 := by
      by_contra hz0
      have h1 : (1 : ℚ) ≤ |(z : ℚ)| := by exact_mod_cast Int.one_le_abs hz0
      have h2 : |(D : ℚ) * R L c l| = F * |(z : ℚ)| := by
        rw [hcz, abs_mul, abs_of_pos hF0]
      rw [abs_mul, abs_of_pos hDq] at h2
      have h3 := hBR l
      nlinarith
    rw [hz0, Int.cast_zero, mul_zero] at hcz
    simpa [hDq.ne'] using hcz
  -- integrality of all coordinates
  have hval_int : ∀ s δ j, ∃ z : ℤ, A L (Xq F ω s δ - c) j = z := by
    intro s δ j
    obtain ⟨m, hm⟩ := hA₁ j
    obtain ⟨z1, hz1⟩ := hXint s₁ δ₁ j
    obtain ⟨z, hz⟩ := hXint s δ j
    refine ⟨z - z1 + m, ?_⟩
    rw [map_sub] at hm ⊢
    simp only [Pi.sub_apply] at hm ⊢
    push_cast
    linarith
  have hmem : ∀ s δ, memQ L (Xq F ω s δ) ↔
      (R L (Xq F ω s δ - c) = 0 ∧ ∀ j, 0 ≤ A L (Xq F ω s δ - c) j) := by
    intro s δ
    rw [memQ_iff]
    apply and_congr_right
    intro _
    apply forall_congr'
    intro j
    constructor
    · rintro ⟨m, hm⟩
      rw [hm]
      positivity
    · intro h
      obtain ⟨z, hz⟩ := hval_int s δ j
      rw [hz] at h ⊢
      have hz0 : 0 ≤ z := by exact_mod_cast h
      refine ⟨z.toNat, ?_⟩
      have : ((z.toNat : ℤ) : ℚ) = (z : ℚ) := by rw [Int.toNat_of_nonneg hz0]
      rw [← this]
      rfl
  have hXR' : ∀ s δ, R L (Xq F ω s δ - c) = (F : ℚ) • R L (Eₗ (fun i => (δ i : ℚ))) := by
    intro s δ
    rw [hXR, hRΩ, hRc, smul_zero, zero_add, sub_zero]
  have hev : ∀ δ, ∀ᶠ s in atTop, ∀ j, A L Ω j ≠ 0 → 0 ≤ A L (Xq F ω s δ - c) j := by
    intro δ
    rw [eventually_all]
    intro j
    by_cases hj : A L Ω j = 0
    · exact Eventually.of_forall fun s h => absurd hj h
    · have hpos : 0 < A L Ω j := lt_of_le_of_ne (hαnn j) (Ne.symm hj)
      filter_upwards [ev_pos (mul_pos hF0 hpos)
        ((F : ℚ) * A L (Eₗ (fun i => (δ i : ℚ))) j - A L c j)] with s hs _
      rw [hXA]
      exact hs.le
  have hzero : ¬ ∀ᶠ s in atTop, ∀ j, 0 ≤ A L (Xq F ω s 0 - c) j := by
    intro h
    obtain ⟨s, hs⟩ := h.exists
    apply hdiag F s
    rw [hmem]
    refine ⟨?_, hs⟩
    rw [hXR']
    have h0 : (fun i => (((0 : Fin M → ℤ) i : ℤ) : ℚ)) = 0 := by funext i; simp
    rw [h0, map_zero, map_zero, smul_zero]
  -- Lemma X
  let ι := {j : Fin L.r // A L Ω j ≠ 0}
  have hW : ∀ i, diagVec M i ∈ Submodule.span ℚ (Set.range (fun j : ι => Vq L j.1)) := by
    intro i
    have hRi := hgenR hRΩ i
    rw [R_eq_zero_iff, Φ_apply] at hRi
    rw [hRi]
    apply Submodule.sum_mem
    intro j _
    by_cases hj : A L Ω j = 0
    · rw [hgenA j hj i, zero_smul]
      exact Submodule.zero_mem _
    · exact Submodule.smul_mem _ _ (Submodule.subset_span ⟨⟨j, hj⟩, rfl⟩)
  have hLX := lemmaX (fun j : ι => Vq L j.1) (fun j => L.pair j.1) (fun j => L.le j.1)
    (fun j i => Nat.cast_nonneg _)
    (fun j i h => L.supp j.1 i (by intro h0; apply h; simp [Vq, h0]))
    (fun j j' => L.laminar j.1 j'.1) hW
  have hli : LinearIndependent ℚ (fun j : ι => Vq L j.1) :=
    (linIndep L).comp _ Subtype.val_injective
  rw [finrank_span_eq_card hli] at hLX
  have hr := r_le L
  have hcard : Fintype.card ι = (Finset.univ.filter fun j => A L Ω j ≠ 0).card :=
    Fintype.card_subtype _
  by_cases hJ : ∃ j₀, A L Ω j₀ = 0
  swap
  · exfalso
    push Not at hJ
    apply hzero
    filter_upwards [hev 0] with s hs j
    exact hs j (hJ j)
  obtain ⟨j₀, hj₀⟩ := hJ
  have huniq : ∀ j, A L Ω j = 0 → j = j₀ := by
    intro j hj
    by_contra hne
    have hsub : (Finset.univ.filter fun j => A L Ω j ≠ 0) ⊆ (Finset.univ.erase j).erase j₀ := by
      intro x hx
      simp only [Finset.mem_filter, Finset.mem_univ, true_and] at hx
      simp only [Finset.mem_erase, Finset.mem_univ, and_true]
      exact ⟨fun h => hx (h ▸ hj₀), fun h => hx (h ▸ hj)⟩
    have h1 := Finset.card_le_card hsub
    rw [Finset.card_erase_of_mem (by simp [Ne.symm hne]), Finset.card_erase_of_mem
      (Finset.mem_univ _), Finset.card_univ, Fintype.card_fin] at h1
    have h2 : j.1 ≠ j₀.1 := fun h => hne (Fin.ext h)
    have h3 := j.2
    have h4 := j₀.2
    omega
  have hrn : L.r = M + M := by
    have hsub : (Finset.univ.filter fun j => A L Ω j ≠ 0) ⊆ Finset.univ.erase j₀ := by
      intro x hx
      simp only [Finset.mem_filter, Finset.mem_univ, true_and] at hx
      simp only [Finset.mem_erase, Finset.mem_univ, and_true]
      exact fun h => hx (h ▸ hj₀)
    have h1 := Finset.card_le_card hsub
    rw [Finset.card_erase_of_mem (Finset.mem_univ _), Finset.card_univ, Fintype.card_fin] at h1
    have h4 := j₀.2
    omega
  have hR0 := R_eq_zero_of_r_eq L hrn
  let ψ : (Fin M → ℚ) →ₗ[ℚ] ℚ := LinearMap.proj j₀ ∘ₗ A L ∘ₗ Eₗ
  have hψ : ∀ δ, ψ δ = A L (Eₗ δ) j₀ := fun δ => rfl
  have hval0 : ∀ s δ, A L (Xq F ω s δ - c) j₀ = F * ψ (fun i => (δ i : ℚ)) - A L c j₀ := by
    intro s δ
    rw [hXA, hj₀, hψ]
    ring
  have hγ : 0 < A L c j₀ := by
    by_contra hγ
    push Not at hγ
    apply hzero
    filter_upwards [hev 0] with s hs j
    by_cases hj : A L Ω j = 0
    · rw [huniq j hj, hval0]
      simp only [Pi.zero_apply, Int.cast_zero]
      have : ψ (fun _ => (0 : ℚ)) = 0 := map_zero ψ
      rw [this]
      linarith
    · exact hs j hj
  refine ⟨ψ, fun δ => ?_⟩
  filter_upwards [hev δ] with s hs
  rw [hmem]
  constructor
  · rintro ⟨_, h⟩
    have := h j₀
    rw [hval0] at this
    by_contra hneg
    push Not at hneg
    nlinarith [mul_nonpos_of_nonneg_of_nonpos hF0.le hneg]
  · intro hψpos
    refine ⟨hR0 _, fun j => ?_⟩
    by_cases hj : A L Ω j = 0
    · rw [huniq j hj, hval0]
      obtain ⟨z, hz⟩ := hDA (Fin.append (0 : Fin M → ℤ) δ) j₀
      rw [← Eₗ_cast, ← hψ] at hz
      have hzpos : (0 : ℚ) < z := by rw [← hz]; positivity
      have hz1 : (1 : ℚ) ≤ z := by
        have : (0 : ℤ) < z := by exact_mod_cast hzpos
        exact_mod_cast this
      have hγB := hBA j₀
      rw [abs_of_pos hγ] at hγB
      -- `D * (F ψ - γ) = F z - D γ ≥ F - B > 0`
      have key : (D : ℚ) * (F * ψ (fun i => (δ i : ℚ)) - A L c j₀) = F * z - D * A L c j₀ := by
        rw [← hz]
        ring
      have : 0 ≤ (D : ℚ) * (F * ψ (fun i => (δ i : ℚ)) - A L c j₀) := by
        rw [key]
        nlinarith
      exact (mul_nonneg_iff_of_pos_left hDq).1 this
    · exact hs j hj

end FA.G2
