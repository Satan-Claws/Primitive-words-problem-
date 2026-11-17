/-
# S2: shifts, convolutions and pumping lemmas for functions `(ℕ → ℕ) → ℕ∞`
-/
import FiniteAmbiguity.S2_Sys

namespace FA
namespace S2

open Finset

/-! ## Shifts -/

lemma shiftF_zero_vec (m : ℕ) (f : (ℕ → ℕ) → ℕ∞) (x : ℕ → ℕ) : shiftF m 0 f x = f x := by
  unfold shiftF
  rw [if_pos (show Ge m x 0 from fun k _ => Nat.zero_le _)]
  exact congrArg f (funext fun k => Nat.sub_zero _)

lemma shiftF_mono (m : ℕ) (p : ℕ → ℕ) {f g : (ℕ → ℕ) → ℕ∞} (h : ∀ y, f y ≤ g y) (x : ℕ → ℕ) :
    shiftF m p f x ≤ shiftF m p g x := by
  unfold shiftF; split_ifs; exacts [h _, le_rfl]

lemma shiftF_comp (m : ℕ) (p q : ℕ → ℕ) (f : (ℕ → ℕ) → ℕ∞) (x : ℕ → ℕ) :
    shiftF m p (shiftF m q f) x = shiftF m (p + q) f x := by
  unfold shiftF
  by_cases h1 : Ge m x p
  · rw [if_pos h1]
    by_cases h2 : Ge m (x - p) q
    · rw [if_pos h2, if_pos]
      · congr 1; funext k; simp only [Pi.sub_apply, Pi.add_apply]; omega
      · intro k hk; have := h1 k hk; have := h2 k hk; simp only [Pi.sub_apply] at *
        simp only [Pi.add_apply]; omega
    · rw [if_neg h2, if_neg]
      intro h; apply h2; intro k hk; have := h k hk; simp only [Pi.sub_apply, Pi.add_apply] at *
      omega
  · rw [if_neg h1, if_neg]
    intro h; apply h1; intro k hk; have := h k hk; simp only [Pi.add_apply] at this; omega

lemma shiftF_at (m : ℕ) (p : ℕ → ℕ) (f : (ℕ → ℕ) → ℕ∞) (y : ℕ → ℕ) :
    shiftF m p f (y + p) = f y := by
  unfold shiftF
  rw [if_pos (show Ge m (y + p) p from fun k _ => by simp)]
  congr 1; funext k; simp

lemma shiftF_zero_fun (m : ℕ) (p x : ℕ → ℕ) : shiftF m p (fun _ => 0) x = 0 := by
  unfold shiftF; split_ifs <;> rfl

/-- The vector `s · e_i`. -/
def sg (i s : ℕ) : ℕ → ℕ := fun k => if k = i then s else 0

/-- Functions on level 0 depend only on coordinate 0. -/
def Dep0 (f : (ℕ → ℕ) → ℕ∞) : Prop := ∀ x y : ℕ → ℕ, x 0 = y 0 → f x = f y

lemma conv_right (m : ℕ) (f g : (ℕ → ℕ) → ℕ∞) (hg : Dep0 g) (x : ℕ → ℕ) :
    conv m f g x = ∑ s ∈ range (x m + 1), g (fun _ => s) * shiftF m (sg m s) f x := by
  unfold conv
  rw [← Finset.sum_range_reflect]
  refine Finset.sum_congr rfl fun s hs => ?_
  simp only [mem_range] at hs
  rw [mul_comm]
  congr 1
  · apply hg; simp [zf]; omega
  · unfold shiftF
    rw [if_pos]
    · congr 1; funext k; simp only [sg, Pi.sub_apply]
      by_cases hk : k = m
      · subst hk; simp
      · simp [hk]
    · intro k _; simp only [sg]; split_ifs with hk
      · subst hk; omega
      · exact Nat.zero_le _

lemma conv_left (m : ℕ) (f g : (ℕ → ℕ) → ℕ∞) (hf : Dep0 f) (x : ℕ → ℕ) :
    conv 0 f g x = ∑ s ∈ range (x 0 + 1), f (fun _ => s) * shiftF m (sg 0 s) g x := by
  unfold conv
  refine Finset.sum_congr rfl fun s hs => ?_
  simp only [mem_range] at hs
  congr 1
  · apply hf; simp
  · unfold shiftF
    rw [if_pos]
    · congr 1; funext k; simp only [sg, Pi.sub_apply, zf]
      by_cases hk : k = 0
      · subst hk; simp
      · simp [hk]
    · intro k _; simp only [sg]; split_ifs with hk
      · subst hk; omega
      · exact Nat.zero_le _

lemma sum_extend (m i : ℕ) (hi : i ≤ m) (w : ℕ → ℕ∞) (f : (ℕ → ℕ) → ℕ∞) (x : ℕ → ℕ) (N : ℕ)
    (hN : x i + 1 ≤ N) :
    ∑ s ∈ range (x i + 1), w s * shiftF m (sg i s) f x =
      ∑ s ∈ range N, w s * shiftF m (sg i s) f x := by
  apply Finset.sum_subset
  · intro s; simp only [mem_range]; omega
  · intro s hs hs'
    simp only [mem_range] at hs hs'
    unfold shiftF
    rw [if_neg, mul_zero]
    intro h
    have := h i hi
    simp [sg] at this
    omega

lemma conv_mono (i : ℕ) {f f' g g' : (ℕ → ℕ) → ℕ∞} (hf : ∀ y, f y ≤ f' y) (hg : ∀ y, g y ≤ g' y)
    (x : ℕ → ℕ) : conv i f g x ≤ conv i f' g' x := by
  unfold conv
  exact Finset.sum_le_sum fun j _ => mul_le_mul' (hf _) (hg _)

/-! ## Pumping: two shifted copies below `f` make `f` unbounded -/

lemma pump_linear (m : ℕ) (f : (ℕ → ℕ) → ℕ∞) (α β : ℕ → ℕ)
    (hf : ∀ x, shiftF m α f x + shiftF m β f x ≤ f x) (a : ℕ → ℕ) (ha : f a ≠ 0) (K : ℕ)
    (hK : ∀ x, f x ≤ K) : False := by
  let pt : ℕ → ℕ → ℕ → ℕ := fun i j k => a k + i * α k + j * β k
  have hα : ∀ i j, pt (i + 1) j = pt i j + α := by
    intro i j; funext k; simp only [pt, Pi.add_apply]; ring
  have hβ : ∀ i j, pt i (j + 1) = pt i j + β := by
    intro i j; funext k; simp only [pt, Pi.add_apply]; ring
  have h00 : pt 0 0 = a := by funext k; simp [pt]
  have h1 : ∀ i, 1 ≤ f (pt i 0) := by
    intro i
    induction i with
    | zero => rw [h00]; exact Order.one_le_iff_ne_zero.mpr ha
    | succ i ih =>
      calc 1 ≤ f (pt i 0) := ih
        _ = shiftF m α f (pt (i + 1) 0) := by rw [hα, shiftF_at]
        _ ≤ f (pt (i + 1) 0) := le_trans le_self_add (hf _)
  have h2 : ∀ i : ℕ, ((i + 1 : ℕ) : ℕ∞) ≤ f (pt i 1) := by
    intro i
    induction i with
    | zero =>
      calc ((0 + 1 : ℕ) : ℕ∞) = 1 := by simp
        _ ≤ f (pt 0 0) := h1 0
        _ = shiftF m β f (pt 0 1) := by rw [hβ, shiftF_at]
        _ ≤ f (pt 0 1) := le_trans le_add_self (hf _)
    | succ i ih =>
      calc ((i + 1 + 1 : ℕ) : ℕ∞) = ((i + 1 : ℕ) : ℕ∞) + 1 := by push_cast; ring
        _ ≤ f (pt i 1) + f (pt (i + 1) 0) := add_le_add ih (h1 _)
        _ = shiftF m α f (pt (i + 1) 1) + shiftF m β f (pt (i + 1) 1) := by
          congr 1
          · rw [hα i 1, shiftF_at]
          · rw [hβ (i + 1) 0, shiftF_at]
        _ ≤ f (pt (i + 1) 1) := hf _
  have := (h2 K).trans (hK _)
  norm_cast at this
  omega

lemma shiftF_dep0 (p : ℕ → ℕ) (f : (ℕ → ℕ) → ℕ∞) (hf : Dep0 f) (y : ℕ → ℕ) :
    shiftF 0 p f y = if p 0 ≤ y 0 then f (fun _ => y 0 - p 0) else 0 := by
  unfold shiftF Ge
  by_cases h : p 0 ≤ y 0
  · rw [if_pos (fun k hk => by rw [Nat.le_zero.mp hk]; exact h), if_pos h]
    apply hf; simp
  · rw [if_neg (fun h' => h (h' 0 le_rfl)), if_neg h]

lemma dep0_shiftF (p : ℕ → ℕ) (f : (ℕ → ℕ) → ℕ∞) (hf : Dep0 f) : Dep0 (shiftF 0 p f) := by
  intro x y h; rw [shiftF_dep0 p f hf, shiftF_dep0 p f hf, h]

lemma pump_quadratic (f : (ℕ → ℕ) → ℕ∞) (hdep : Dep0 f) (h0 : ∀ x, x 0 = 0 → f x = 0)
    (a b : ℕ → ℕ) (hf : ∀ x, conv 0 (shiftF 0 a f) (shiftF 0 b f) x ≤ f x)
    (c : ℕ → ℕ) (hc : f c ≠ 0) (K : ℕ) (hK : ∀ x, f x ≤ K) : False := by
  let F : ℕ → ℕ∞ := fun n => f (fun _ => n)
  have hFc : f c = F (c 0) := hdep _ _ rfl
  have hc0 : c 0 ≠ 0 := fun h => hc (h0 c h)
  set c' := c 0
  set a' := a 0
  set b' := b 0
  -- the convolution at a constant vector
  have hconv : ∀ n, ∑ j ∈ range (n + 1),
      (if a' ≤ j then F (j - a') else 0) * (if b' ≤ n - j then F (n - j - b') else 0) ≤ F n := by
    intro n
    refine le_trans (le_of_eq ?_) (hf (fun _ => n))
    unfold conv
    refine Finset.sum_congr rfl fun j _ => ?_
    rw [shiftF_dep0 a f hdep, shiftF_dep0 b f hdep]
    simp only [Function.update_self, zf, ite_true]
    split_ifs <;> rfl
  have hF1 : 1 ≤ F c' := by rw [← hFc]; exact Order.one_le_iff_ne_zero.mpr hc
  let d := c' + a' + b'
  have step : ∀ w, 1 ≤ F w → c' < w → F w + 1 ≤ F (w + d) := by
    intro w hw hcw
    have hsub : ({a' + w, a' + c'} : Finset ℕ) ⊆ range (w + d + 1) := by
      intro j; simp only [mem_insert, mem_singleton, mem_range]; omega
    have hne : a' + w ≠ a' + c' := by omega
    refine le_trans ?_ (le_trans (Finset.sum_le_sum_of_subset hsub) (hconv (w + d)))
    rw [Finset.sum_pair hne]
    simp only [show a' ≤ a' + w by omega, show a' ≤ a' + c' by omega, if_true,
      show b' ≤ w + d - (a' + w) by omega, show b' ≤ w + d - (a' + c') by omega,
      show a' + w - a' = w by omega, show a' + c' - a' = c' by omega,
      show w + d - (a' + w) - b' = c' by omega, show w + d - (a' + c') - b' = w by omega]
    calc F w + 1 ≤ F w * F c' + F c' * F w := by
          gcongr
          · exact le_mul_of_one_le_right' hF1
          · exact le_trans hw (le_mul_of_one_le_left' hF1)
      _ = _ := rfl
  have base : 1 ≤ F (c' + d) := by
    have hsub : ({a' + c'} : Finset ℕ) ⊆ range (c' + d + 1) := by
      intro j; simp only [mem_singleton, mem_range]; omega
    refine le_trans ?_ (le_trans (Finset.sum_le_sum_of_subset hsub) (hconv (c' + d)))
    rw [Finset.sum_singleton]
    simp only [show a' ≤ a' + c' by omega, if_true, show b' ≤ c' + d - (a' + c') by omega,
      show a' + c' - a' = c' by omega, show c' + d - (a' + c') - b' = c' by omega]
    exact le_trans hF1 (le_mul_of_one_le_right' hF1)
  have grow : ∀ n : ℕ, ((n + 1 : ℕ) : ℕ∞) ≤ F (c' + (n + 1) * d) := by
    intro n
    induction n with
    | zero => simpa using base
    | succ n ih =>
      have h1 : 1 ≤ F (c' + (n + 1) * d) := le_trans (by simp) ih
      have := step _ h1 (by have : 0 < d := by omega
                            nlinarith)
      rw [show c' + (n + 1) * d + d = c' + (n + 1 + 1) * d by ring] at this
      calc ((n + 1 + 1 : ℕ) : ℕ∞) = ((n + 1 : ℕ) : ℕ∞) + 1 := by push_cast; ring
        _ ≤ F (c' + (n + 1) * d) + 1 := add_le_add ih le_rfl
        _ ≤ _ := this
  have := (grow K).trans (hK _)
  norm_cast at this
  omega

end S2
end FA
