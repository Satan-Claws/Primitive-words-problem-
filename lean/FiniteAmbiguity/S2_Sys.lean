/-
# S2: laminar linear systems with multiplicities, and their closure properties
-/
import FiniteAmbiguity.S2_Trees

namespace FA
namespace S2

open Finset

/-- A linear system `c + Σ ℕ v_j` on vectors `ℕ → ℕ`, periods supported on non-crossing pairs. -/
structure Sys where
  ι : Type
  [fin : Fintype ι]
  [dec : DecidableEq ι]
  c : ℕ → ℕ
  v : ι → ℕ → ℕ
  pair : ι → ℕ × ℕ
  le : ∀ j, (pair j).1 ≤ (pair j).2
  supp : ∀ j k, v j k ≠ 0 → k = (pair j).1 ∨ k = (pair j).2
  laminar : ∀ j j', ¬ ((pair j).1 < (pair j').1 ∧ (pair j').1 < (pair j).2 ∧
    (pair j).2 < (pair j').2)

attribute [instance] Sys.fin Sys.dec

namespace Sys

/-- Value of the parametrisation. -/
def val (S : Sys) (q : S.ι → ℕ) : ℕ → ℕ := fun k => S.c k + ∑ j, q j * S.v j k

/-- All pairs lie in `[0, m]`. -/
def Within (S : Sys) (m : ℕ) : Prop := ∀ j, (S.pair j).2 ≤ m

/-- The fibre of `x` (compared on coordinates `≤ m`). -/
def fib (S : Sys) (m : ℕ) (x : ℕ → ℕ) : Set (S.ι → ℕ) := {q | ∀ k ≤ m, S.val q k = x k}

lemma v_eq_zero_of_lt (S : Sys) (j : S.ι) (k : ℕ) (hk : (S.pair j).2 < k) : S.v j k = 0 := by
  by_contra h
  rcases S.supp j k h with h' | h' <;> have := S.le j <;> omega

end Sys

/-- Multiplicity of `x` in the system (number of parameter vectors). -/
noncomputable def cnt (m : ℕ) (S : Sys) (x : ℕ → ℕ) : ℕ∞ := (S.fib m x).encard

/-- Representable functions on level `m`: finite sums of system multiplicities. -/
def Rep (m : ℕ) (f : (ℕ → ℕ) → ℕ∞) : Prop :=
  ∃ Ls : List Sys, (∀ S ∈ Ls, S.Within m) ∧ ∀ x, f x = (Ls.map fun S => cnt m S x).sum

lemma rep_zero (m : ℕ) : Rep m (fun _ => 0) := ⟨[], by simp, by simp⟩

lemma rep_add {m : ℕ} {f g : (ℕ → ℕ) → ℕ∞} (hf : Rep m f) (hg : Rep m g) :
    Rep m (fun x => f x + g x) := by
  obtain ⟨L1, h1, e1⟩ := hf
  obtain ⟨L2, h2, e2⟩ := hg
  refine ⟨L1 ++ L2, ?_, ?_⟩
  · intro S hS; rcases List.mem_append.mp hS with h | h; exacts [h1 S h, h2 S h]
  · intro x; simp [e1, e2]

lemma rep_congr {m : ℕ} {f g : (ℕ → ℕ) → ℕ∞} (hf : Rep m f) (h : ∀ x, f x = g x) : Rep m g := by
  have : f = g := funext h
  exact this ▸ hf

lemma rep_sum {m : ℕ} {α : Type*} (s : Finset α) (f : α → (ℕ → ℕ) → ℕ∞)
    (h : ∀ a ∈ s, Rep m (f a)) : Rep m (fun x => ∑ a ∈ s, f a x) := by
  classical
  induction s using Finset.induction_on with
  | empty => simpa using rep_zero m
  | insert a s ha ih =>
    refine rep_congr (rep_add (h a (by simp)) (ih fun b hb => h b (by simp [hb]))) ?_
    intro x; rw [Finset.sum_insert ha]

lemma rep_ite {m : ℕ} (P : Prop) [Decidable P] {f : (ℕ → ℕ) → ℕ∞} (hf : P → Rep m f) :
    Rep m (fun x => if P then f x else 0) := by
  by_cases hP : P
  · simpa [hP] using hf hP
  · simpa [hP] using rep_zero m

/-- The point system `{c}`. -/
def pointSys (c : ℕ → ℕ) : Sys where
  ι := Empty
  c := c
  v := fun j => j.elim
  pair := fun j => j.elim
  le := fun j => j.elim
  supp := fun j => j.elim
  laminar := fun j => j.elim

lemma cnt_point (m : ℕ) (c x : ℕ → ℕ) :
    cnt m (pointSys c) x = if (∀ k ≤ m, c k = x k) then 1 else 0 := by
  have hv : ∀ (q : (pointSys c).ι → ℕ) k, (pointSys c).val q k = c k := by
    intro q k; show c k + ∑ j : Empty, _ = c k; simp
  unfold cnt Sys.fib
  split_ifs with h
  · rw [Set.encard_eq_one]
    refine ⟨fun j => j.elim, Set.ext fun q => ⟨fun _ => funext fun j => j.elim, fun _ k hk => ?_⟩⟩
    rw [hv]; exact h k hk
  · rw [Set.encard_eq_zero, Set.eq_empty_iff_forall_notMem]
    intro q hq
    exact h fun k hk => (hv q k).symm.trans (hq k hk)

lemma rep_point (m : ℕ) (c : ℕ → ℕ) : Rep m (fun x => if (∀ k ≤ m, c k = x k) then 1 else 0) :=
  ⟨[pointSys c], by simp [Sys.Within, pointSys], by simp [cnt_point]⟩

/-! ## Shifts -/

/-- `x ≥ p` on coordinates `≤ m`. -/
def Ge (m : ℕ) (x p : ℕ → ℕ) : Prop := ∀ k ≤ m, p k ≤ x k

/-- `f` shifted by `p`. -/
noncomputable def shiftF (m : ℕ) (p : ℕ → ℕ) (f : (ℕ → ℕ) → ℕ∞) (x : ℕ → ℕ) : ℕ∞ :=
  by classical exact if Ge m x p then f (x - p) else 0

/-- Shifted system. -/
def Sys.shift (S : Sys) (p : ℕ → ℕ) : Sys := { S with c := S.c + p }

lemma cnt_shift (m : ℕ) (S : Sys) (p x : ℕ → ℕ) :
    cnt m (S.shift p) x = shiftF m p (cnt m S) x := by
  have hv : ∀ (q : S.ι → ℕ) k, (S.shift p).val q k = S.val q k + p k := by
    intro q k; show S.c k + p k + _ = S.c k + _ + p k; ring
  unfold shiftF cnt
  split_ifs with h
  · congr 1
    refine Set.ext fun q => forall_congr' fun k => imp_congr_right fun hk => ?_
    show (S.shift p).val q k = x k ↔ S.val q k = (x - p) k
    rw [hv, Pi.sub_apply]
    have := h k hk
    omega
  · rw [Set.encard_eq_zero, Set.eq_empty_iff_forall_notMem]
    intro q hq
    apply h
    intro k hk
    have := hq k hk
    change (S.shift p).val q k = x k at this
    rw [hv] at this
    omega

lemma rep_shift {m : ℕ} (p : ℕ → ℕ) {f : (ℕ → ℕ) → ℕ∞} (hf : Rep m f) : Rep m (shiftF m p f) := by
  obtain ⟨Ls, hW, he⟩ := hf
  refine ⟨Ls.map (fun S => S.shift p), ?_, ?_⟩
  · intro S hS
    obtain ⟨S', hS', rfl⟩ := List.mem_map.mp hS
    exact hW S' hS'
  · intro x
    simp only [List.map_map, Function.comp_def, cnt_shift]
    unfold shiftF
    split_ifs
    · rw [he]
    · simp

/-! ## Convolution -/

/-- Convolution of two systems at block `i`. -/
def Sys.conv (i : ℕ) (S T : Sys) (hS : S.Within i) : Sys where
  ι := S.ι ⊕ T.ι
  c := fun k => if k < i then S.c k else if k = i then S.c i + T.c 0 else T.c (k - i)
  v := fun j => match j with
    | .inl j => S.v j
    | .inr j => fun k => if i ≤ k then T.v j (k - i) else 0
  pair := fun j => match j with
    | .inl j => S.pair j
    | .inr j => ((T.pair j).1 + i, (T.pair j).2 + i)
  le := by
    rintro (j | j)
    · exact S.le j
    · have := T.le j; simp only; omega
  supp := by
    rintro (j | j) k hk
    · exact S.supp j k hk
    · simp only at hk ⊢
      split_ifs at hk with h
      · rcases T.supp j _ hk with h' | h' <;> [left; right] <;> omega
      · exact absurd rfl hk
  laminar := by
    rintro (j | j) (j' | j')
    · exact S.laminar j j'
    · have := hS j; have := T.le j'; simp only; omega
    · have := hS j'; have := T.le j; simp only; omega
    · have := T.laminar j j'; simp only; omega

lemma Sys.conv_within (i l : ℕ) (S T : Sys) (hS : S.Within i) (hT : T.Within l) :
    (S.conv i T hS).Within (i + l) := by
  rintro (j | j)
  · have := hS j; simp only [Sys.conv]; omega
  · have := hT j; simp only [Sys.conv]; omega

lemma cnt_conv (i l : ℕ) (S T : Sys) (hS : S.Within i) (x : ℕ → ℕ) :
    cnt (i + l) (S.conv i T hS) x = conv i (cnt i S) (cnt l T) x := by
  classical
  unfold cnt conv
  let φ := Equiv.sumArrowEquivProdArrow S.ι T.ι ℕ
  have hval : ∀ (q : S.ι ⊕ T.ι → ℕ) (k : ℕ), (S.conv i T hS).val q k =
      if k < i then S.val (fun j => q (.inl j)) k
      else if k = i then S.val (fun j => q (.inl j)) i + T.val (fun j => q (.inr j)) 0
      else T.val (fun j => q (.inr j)) (k - i) := by
    intro q k
    simp only [Sys.val, Sys.conv, Fintype.sum_sum_type]
    split_ifs with h1 h2
    · have : ∀ j, (if i ≤ k then T.v j (k - i) else 0) = 0 := fun j => by simp; omega
      simp [this]
    · subst h2; simp; ring
    · have : ∀ j, S.v j k = 0 := fun j => S.v_eq_zero_of_lt j k (by have := hS j; omega)
      have h3 : i ≤ k := by omega
      simp [this, h3]
  have hset : φ '' ((S.conv i T hS).fib (i + l) x) =
      ⋃ j ∈ range (x i + 1), S.fib i (Function.update x i j) ×ˢ T.fib l (zf i j x) := by
    ext ⟨q1, q2⟩
    simp only [Set.mem_image, Set.mem_iUnion, Set.mem_prod, mem_range, exists_prop]
    constructor
    · rintro ⟨q, hq, hqe⟩
      have e1 : q1 = fun j => q (.inl j) := (congrArg Prod.fst hqe).symm
      have e2 : q2 = fun j => q (.inr j) := (congrArg Prod.snd hqe).symm
      subst e1 e2
      have hq' : ∀ k ≤ i + l, _ := fun k hk => (hval q k).symm.trans (hq k hk)
      have hi := hq' i (by omega)
      simp only [lt_irrefl, ite_false, ite_true] at hi
      refine ⟨S.val (fun j => q (.inl j)) i, by omega, ?_, ?_⟩
      · intro k hk
        rcases Nat.lt_or_ge k i with h | h
        · have := hq' k (by omega); simp only [h, ite_true] at this
          rw [this, Function.update_of_ne (by omega)]
        · have : k = i := by omega
          subst this; simp
      · intro k hk
        simp only [zf]
        split_ifs with h0
        · subst h0; omega
        · have := hq' (k + i) (by omega)
          simp only [show ¬ k + i < i by omega, show k + i ≠ i by omega, ite_false,
            Nat.add_sub_cancel] at this
          exact this
    · rintro ⟨j, hj, h1, h2⟩
      refine ⟨φ.symm (q1, q2), ?_, by simp⟩
      intro k hk
      rw [hval]
      have e1 : (fun j => φ.symm (q1, q2) (.inl j)) = q1 := rfl
      have e2 : (fun j => φ.symm (q1, q2) (.inr j)) = q2 := rfl
      rw [e1, e2]
      split_ifs with h h'
      · rw [h1 k (by omega), Function.update_of_ne (by omega)]
      · subst h'
        rw [h1 k le_rfl, h2 0 (Nat.zero_le _)]
        simp [zf]; omega
      · rw [h2 (k - i) (by omega)]
        simp only [zf, show k - i ≠ 0 by omega, ite_false]
        congr 1; omega
  rw [show ((S.conv i T hS).fib (i + l) x).encard = (φ '' ((S.conv i T hS).fib (i + l) x)).encard
    from (φ.injective.encard_image _).symm, hset, encard_biUnion_finset]
  · refine Finset.sum_congr rfl fun j _ => ?_
    rw [Set.encard_prod]
  · intro j _ j' _ hjj
    rw [Set.disjoint_left]
    rintro ⟨q1, q2⟩ ⟨h1, -⟩ ⟨h1', -⟩
    have a := h1 i le_rfl
    have b := h1' i le_rfl
    simp only [Function.update_self] at a b
    exact hjj (a.symm.trans b)

lemma conv_add_left (i : ℕ) (f f' g : (ℕ → ℕ) → ℕ∞) (x : ℕ → ℕ) :
    conv i (fun y => f y + f' y) g x = conv i f g x + conv i f' g x := by
  simp [conv, add_mul, Finset.sum_add_distrib]

lemma conv_add_right (i : ℕ) (f g g' : (ℕ → ℕ) → ℕ∞) (x : ℕ → ℕ) :
    conv i f (fun y => g y + g' y) x = conv i f g x + conv i f g' x := by
  simp [conv, mul_add, Finset.sum_add_distrib]

lemma rep_conv {i l : ℕ} {f g : (ℕ → ℕ) → ℕ∞} (hf : Rep i f) (hg : Rep l g) :
    Rep (i + l) (conv i f g) := by
  obtain ⟨L1, h1, e1⟩ := hf
  obtain ⟨L2, h2, e2⟩ := hg
  have hfe : f = fun x => (L1.map fun S => cnt i S x).sum := funext e1
  have hge : g = fun x => (L2.map fun S => cnt l S x).sum := funext e2
  subst hfe hge
  clear e1 e2
  induction L1 with
  | nil => exact rep_congr (rep_zero (i + l)) (fun x => by simp [conv])
  | cons S L1 ih =>
    have hS := h1 S (by simp)
    refine rep_congr (rep_add ?_ (ih fun S' h => h1 S' (by simp [h]))) (fun x => ?_)
    · exact (fun x => conv i (cnt i S) (fun y => (L2.map fun S => cnt l S y).sum) x)
    · clear ih
      induction L2 with
      | nil => exact rep_congr (rep_zero (i + l)) (fun x => by simp [conv])
      | cons T L2 ih2 =>
        refine rep_congr (rep_add ?_ (ih2 fun S' h => h2 S' (by simp [h]))) (fun x => ?_)
        · exact cnt (i + l) (S.conv i T hS)
        · exact ⟨[S.conv i T hS], by simpa using Sys.conv_within i l S T hS (h2 T (by simp)),
            by simp⟩
        · simp only [List.map_cons, List.sum_cons]
          rw [conv_add_right, cnt_conv]
    · simp only [List.map_cons, List.sum_cons]
      rw [conv_add_left]

end S2
end FA
