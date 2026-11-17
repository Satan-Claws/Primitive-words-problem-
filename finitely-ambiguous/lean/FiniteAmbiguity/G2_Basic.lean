/-
# Elementary helpers for the geometric lemma (agent G2).
-/
import FiniteAmbiguity.Prelude

namespace FA.G2
open Filter

/-! ### Eventual sign of an affine function of `s : ℕ` -/

theorem ev_pos {a : ℚ} (ha : 0 < a) (b : ℚ) : ∀ᶠ s : ℕ in atTop, 0 < a * s + b := by
  obtain ⟨N, hN⟩ := exists_nat_gt (-b / a)
  filter_upwards [eventually_ge_atTop N] with s hs
  have h1 : (N : ℚ) ≤ s := by exact_mod_cast hs
  have h2 : -b < N * a := by rwa [div_lt_iff₀ ha] at hN
  nlinarith

theorem ev_neg {a : ℚ} (ha : a < 0) (b : ℚ) : ∀ᶠ s : ℕ in atTop, a * s + b < 0 := by
  filter_upwards [ev_pos (neg_pos.2 ha) (-b)] with s hs
  linarith

theorem ev_ne {a : ℚ} (ha : a ≠ 0) (b : ℚ) : ∀ᶠ s : ℕ in atTop, a * s + b ≠ 0 := by
  rcases lt_or_gt_of_ne ha with h | h
  · filter_upwards [ev_neg h b] with s hs
    exact hs.ne
  · filter_upwards [ev_pos h b] with s hs
    exact hs.ne'

/-! ### Common denominators -/

theorem exists_common_den {ι : Type*} [Fintype ι] (x : ι → ℚ) :
    ∃ D : ℕ, 0 < D ∧ ∀ i, ∃ z : ℤ, (D : ℚ) * x i = z := by
  classical
  refine ⟨∏ i, (x i).den, Finset.prod_pos fun i _ => (x i).den_pos, fun i => ?_⟩
  obtain ⟨k, hk⟩ : (x i).den ∣ ∏ i, (x i).den := Finset.dvd_prod_of_mem _ (Finset.mem_univ i)
  refine ⟨k * (x i).num, ?_⟩
  rw [hk]
  push_cast
  rw [← Rat.mul_den_eq_num]
  ring

theorem exists_den_linear {n : ℕ} {ι : Type*} [Fintype ι] (G : (Fin n → ℚ) →ₗ[ℚ] (ι → ℚ)) :
    ∃ D : ℕ, 0 < D ∧ ∀ (y : Fin n → ℤ) (j : ι), ∃ z : ℤ,
      (D : ℚ) * G (fun k => (y k : ℚ)) j = z := by
  classical
  obtain ⟨D, hD, hz⟩ :=
    exists_common_den (fun p : Fin n × ι => G (fun k' => if p.1 = k' then 1 else 0) p.2)
  choose z hz using hz
  refine ⟨D, hD, fun y j => ⟨∑ k, y k * z (k, j), ?_⟩⟩
  rw [LinearMap.pi_apply_eq_sum_univ G]
  simp only [Finset.sum_apply, Pi.smul_apply, smul_eq_mul, Finset.mul_sum]
  push_cast
  refine Finset.sum_congr rfl fun k _ => ?_
  have := hz (k, j)
  simp only at this
  rw [← this]
  ring

/-! ### Generic vectors -/

open Polynomial in
theorem exists_generic {M : ℕ} (cs : Finset (Fin M → ℚ)) :
    ∃ ω : Fin M → ℕ, (∀ i, 1 ≤ ω i) ∧ ∀ c ∈ cs, c ≠ 0 → ∑ i, c i * (ω i : ℚ) ≠ 0 := by
  classical
  let p : (Fin M → ℚ) → ℚ[X] := fun c => ∑ i : Fin M, C (c i) * X ^ (i : ℕ)
  have hp_eval : ∀ c (K : ℚ), (p c).eval K = ∑ i, c i * K ^ (i : ℕ) := by
    intro c K
    simp [p, eval_finsetSum]
  have hp_ne : ∀ c, c ≠ 0 → p c ≠ 0 := by
    intro c hc h
    apply hc
    funext i
    have := congrArg (fun q => q.coeff i) h
    simpa [p, finsetSum_coeff, coeff_C_mul_X_pow, Fin.val_inj] using this
  let Q : ℚ[X] := ∏ c ∈ cs.filter (· ≠ 0), p c
  have hQ : Q ≠ 0 := by
    rw [Finset.prod_ne_zero_iff]
    intro c hc
    exact hp_ne c (Finset.mem_filter.1 hc).2
  have : ∃ K : ℕ, Q.eval ((K : ℚ) + 1) ≠ 0 := by
    by_contra h
    push Not at h
    apply hQ
    apply Polynomial.eq_zero_of_infinite_isRoot
    apply Set.infinite_of_injective_forall_mem (f := fun K : ℕ => (K : ℚ) + 1)
    · intro a b hab
      simpa using hab
    · intro K
      exact h K
  obtain ⟨K, hK⟩ := this
  refine ⟨fun i => (K + 1) ^ (i : ℕ), fun i => Nat.one_le_pow _ _ (Nat.succ_pos K),
    fun c hc hc0 => ?_⟩
  rw [eval_prod, Finset.prod_ne_zero_iff] at hK
  have := hK c (Finset.mem_filter.2 ⟨hc, hc0⟩)
  rw [hp_eval] at this
  push_cast
  exact this

/-! ### Few linear forms leave a non-zero direction uncovered -/

theorem exists_neg_dir_rat {M : ℕ} (hM : 1 ≤ M) (gs : List ((Fin M → ℚ) →ₗ[ℚ] ℚ))
    (hlen : gs.length ≤ M) : ∃ δ : Fin M → ℚ, δ ≠ 0 ∧ ∀ g ∈ gs, g δ ≤ 0 := by
  cases gs with
  | nil =>
    refine ⟨fun _ => 1, fun h => ?_, by simp⟩
    have := congrFun h ⟨0, hM⟩
    simp at this
  | cons g t =>
    simp only [List.length_cons] at hlen
    let T : (Fin M → ℚ) →ₗ[ℚ] (Fin t.length → ℚ) := LinearMap.pi fun k => t.get k
    have hker : LinearMap.ker T ≠ ⊥ := LinearMap.ker_ne_bot_of_finrank_lt (by simp; omega)
    obtain ⟨δ₀, hδ₀, hne⟩ := Submodule.exists_mem_ne_zero_of_ne_bot hker
    have ht : ∀ h ∈ t, h δ₀ = 0 := by
      intro h hh
      obtain ⟨k, rfl⟩ := List.mem_iff_get.1 hh
      have := congrFun (LinearMap.mem_ker.1 hδ₀) k
      simpa [T] using this
    by_cases hg : g δ₀ ≤ 0
    · refine ⟨δ₀, hne, ?_⟩
      intro h hh
      rcases List.mem_cons.1 hh with rfl | hh
      · exact hg
      · exact (ht h hh).le
    · refine ⟨-δ₀, neg_ne_zero.2 hne, ?_⟩
      intro h hh
      rcases List.mem_cons.1 hh with rfl | hh
      · rw [map_neg]
        linarith
      · rw [map_neg, ht h hh, neg_zero]

theorem exists_neg_dir {M : ℕ} (hM : 1 ≤ M) (gs : List ((Fin M → ℚ) →ₗ[ℚ] ℚ))
    (hlen : gs.length ≤ M) :
    ∃ δ : Fin M → ℤ, δ ≠ 0 ∧ ∀ g ∈ gs, g (fun i => (δ i : ℚ)) ≤ 0 := by
  obtain ⟨δ, hne, hδ⟩ := exists_neg_dir_rat hM gs hlen
  obtain ⟨D, hD, hz⟩ := exists_common_den δ
  choose z hz using hz
  have hcast : (fun i => (z i : ℚ)) = (D : ℚ) • δ := by
    funext i
    simp [← hz i]
  refine ⟨z, ?_, fun g hg => ?_⟩
  · intro h0
    apply hne
    funext i
    have := hz i
    rw [h0] at this
    simp only [Pi.zero_apply, Int.cast_zero, mul_eq_zero, Nat.cast_eq_zero] at this
    rcases this with h | h
    · omega
    · simpa using h
  · rw [hcast, map_smul, smul_eq_mul]
    exact mul_nonpos_of_nonneg_of_nonpos (by positivity) (hδ g hg)

open Classical in
theorem many_forms {M : ℕ} (hM : 1 ≤ M) {α : Type*} (l : List α)
    (ψ : α → (Fin M → ℚ) →ₗ[ℚ] ℚ)
    (h : ∀ δ : Fin M → ℤ, δ ≠ 0 → ∃ a ∈ l, 0 < ψ a (fun i => (δ i : ℚ))) :
    M + 1 ≤ l.countP (fun a => decide (ψ a ≠ 0)) := by
  classical
  by_contra hlt
  push Not at hlt
  let gs := (l.filter (fun a => decide (ψ a ≠ 0))).map ψ
  have hlen : gs.length ≤ M := by
    simp only [gs, List.length_map, ← List.countP_eq_length_filter]
    omega
  obtain ⟨δ, hne, hδ⟩ := exists_neg_dir hM gs hlen
  obtain ⟨a, ha, hpos⟩ := h δ hne
  have hψa : ψ a ≠ 0 := by
    intro h0
    rw [h0] at hpos
    simp at hpos
  have hmem : ψ a ∈ gs := List.mem_map.2 ⟨a, List.mem_filter.2 ⟨ha, by simpa using hψa⟩, rfl⟩
  exact absurd (hδ _ hmem) (not_le.2 hpos)

open Classical in
theorem count_pm {M : ℕ} {α : Type*} (l : List α) (ψ : α → (Fin M → ℚ) →ₗ[ℚ] ℚ)
    (δ : Fin M → ℚ) (h : ∀ a ∈ l, ψ a ≠ 0 → ψ a δ ≠ 0) :
    l.countP (fun a => decide (0 < ψ a δ)) + l.countP (fun a => decide (0 < ψ a (-δ))) =
      l.countP (fun a => decide (ψ a ≠ 0)) := by
  induction l with
  | nil => simp
  | cons a t ih =>
    have ih' := ih (fun b hb => h b (List.mem_cons_of_mem _ hb))
    by_cases h0 : ψ a = 0
    · have e1 : decide (0 < ψ a δ) = false := by simp [h0]
      have e2 : decide (0 < ψ a (-δ)) = false := by simp [h0]
      have e3 : decide (ψ a ≠ 0) = false := by simp [h0]
      simp only [List.countP_cons, e1, e2, e3]
      simp only [Bool.false_eq_true, ite_false]
      omega
    · have hne := h a List.mem_cons_self h0
      have e3 : decide (ψ a ≠ 0) = true := by simp [h0]
      rcases lt_or_gt_of_ne hne with hl | hl
      · have e1 : decide (0 < ψ a δ) = false := by simp [not_lt.2 hl.le]
        have e2 : decide (0 < ψ a (-δ)) = true := by
          rw [map_neg]; simp only [decide_eq_true_eq]; linarith
        simp only [List.countP_cons, e1, e2, e3]
        simp only [Bool.false_eq_true, ite_false, ite_true]
        omega
      · have e1 : decide (0 < ψ a δ) = true := by simp [hl]
        have e2 : decide (0 < ψ a (-δ)) = false := by
          rw [map_neg]; simp only [decide_eq_false_iff_not, not_lt]; linarith
        simp only [List.countP_cons, e1, e2, e3]
        simp only [Bool.false_eq_true, ite_false, ite_true]
        omega

end FA.G2
