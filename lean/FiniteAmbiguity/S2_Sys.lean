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
    intro q k; show S.c k + p k + _ = S.c k + _ + p k; rw [add_right_comm]; rfl
  unfold shiftF cnt
  split_ifs with h
  · congr 1
    refine Set.ext fun q => forall_congr' fun k => imp_congr_right fun hk => ?_
    show (S.shift p).val q k = x k ↔ S.val q k = (x - p) k
    rw [hv q k, Pi.sub_apply]
    have := h k hk
    omega
  · rw [Set.encard_eq_zero, Set.eq_empty_iff_forall_notMem]
    intro q hq
    apply h
    intro k hk
    have := hq k hk
    change (S.shift p).val q k = x k at this
    rw [hv q k] at this
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
    have hs : (S.conv i T hS).val q k = (S.conv i T hS).c k + (∑ j : S.ι, q (.inl j) * S.v j k +
        ∑ j : T.ι, q (.inr j) * (if i ≤ k then T.v j (k - i) else 0)) := by
      show _ + _ = _ + _
      congr 1
      exact Fintype.sum_sum_type _
    rw [hs]
    rcases lt_trichotomy k i with h | h | h
    · have e : ∀ j : T.ι, (if i ≤ k then T.v j (k - i) else 0) = 0 := fun j => if_neg (by omega)
      simp only [e, mul_zero, Finset.sum_const_zero, add_zero, Sys.val, Sys.conv, if_pos h]
    · subst h
      have e : ∀ j : T.ι, (if k ≤ k then T.v j (k - k) else 0) = T.v j 0 := fun j => by simp
      simp only [e, Sys.val, Sys.conv, lt_irrefl, if_false, if_true]; ring
    · have e : ∀ j : T.ι, (if i ≤ k then T.v j (k - i) else 0) = T.v j (k - i) :=
        fun j => if_pos (by omega)
      have e2 : ∀ j, S.v j k = 0 := fun j => S.v_eq_zero_of_lt j k (by have := hS j; omega)
      simp only [e, e2, mul_zero, Finset.sum_const_zero, zero_add, Sys.val, Sys.conv,
        if_neg (show ¬ k < i by omega), if_neg (show k ≠ i by omega)]
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
    have hA : Rep (i + l) (conv i (cnt i S) (fun y => (L2.map fun S => cnt l S y).sum)) := by
      clear ih
      induction L2 with
      | nil => exact rep_congr (rep_zero (i + l)) (fun x => by simp [conv])
      | cons T L2 ih2 =>
        have hT : Rep (i + l) (cnt (i + l) (S.conv i T hS)) :=
          ⟨[S.conv i T hS], by simpa using Sys.conv_within i l S T hS (h2 T (by simp)), by simp⟩
        refine rep_congr (rep_add hT (ih2 fun S' h => h2 S' (by simp [h]))) (fun x => ?_)
        simp only [List.map_cons, List.sum_cons]
        rw [conv_add_right, cnt_conv]
    refine rep_congr (rep_add hA (ih fun S' h => h1 S' (by simp [h]))) (fun x => ?_)
    simp only [List.map_cons, List.sum_cons]
    rw [conv_add_left]

/-! ## Adding a period (rings) -/

/-- Add one period `v`, supported on `{0, m}`, to a system within `[0, m]`. -/
def Sys.addPeriod (S : Sys) (m : ℕ) (hS : S.Within m) (v : ℕ → ℕ)
    (hv : ∀ k, v k ≠ 0 → k = 0 ∨ k = m) : Sys where
  ι := Option S.ι
  c := S.c
  v := fun o => match o with
    | none => v
    | some j => S.v j
  pair := fun o => match o with
    | none => (0, m)
    | some j => S.pair j
  le := by
    rintro (_ | j)
    · exact Nat.zero_le _
    · exact S.le j
  supp := by
    rintro (_ | j) k hk
    · exact hv k hk
    · exact S.supp j k hk
  laminar := by
    rintro (_ | j) (_ | j')
    · simp
    · have := hS j'; simp only; omega
    · simp only; omega
    · exact S.laminar j j'

lemma Sys.addPeriod_within (S : Sys) (m : ℕ) (hS : S.Within m) (v : ℕ → ℕ)
    (hv : ∀ k, v k ≠ 0 → k = 0 ∨ k = m) : (S.addPeriod m hS v hv).Within m := by
  rintro (_ | j)
  · exact le_rfl
  · exact hS j

lemma shiftF_add (m : ℕ) (p : ℕ → ℕ) (f g : (ℕ → ℕ) → ℕ∞) (x : ℕ → ℕ) :
    shiftF m p (fun y => f y + g y) x = shiftF m p f x + shiftF m p g x := by
  unfold shiftF; split_ifs <;> simp

lemma cnt_addPeriod (S : Sys) (m : ℕ) (hS : S.Within m) (v : ℕ → ℕ)
    (hv : ∀ k, v k ≠ 0 → k = 0 ∨ k = m) (x : ℕ → ℕ) :
    cnt m (S.addPeriod m hS v hv) x = cnt m S x + shiftF m v (cnt m (S.addPeriod m hS v hv)) x := by
  classical
  set S' := S.addPeriod m hS v hv with hS'
  have hval : ∀ (q : Option S.ι → ℕ) k, S'.val q k = S.val (fun j => q (some j)) k + q none * v k := by
    intro q k
    have : S'.val q k = S.c k + (q none * v k + ∑ j : S.ι, q (some j) * S.v j k) := by
      show _ + _ = _ + _
      congr 1
      exact Fintype.sum_option _
    rw [this]; simp only [Sys.val]; ring
  let ext : (S.ι → ℕ) → (Option S.ι → ℕ) := fun q o => Option.elim o 0 q
  have hext : Function.Injective ext := by
    intro a b h; funext j; exact congrFun h (some j)
  let inc : (Option S.ι → ℕ) → (Option S.ι → ℕ) := fun q => Function.update q none (q none + 1)
  have hinc : Function.Injective inc := by
    intro a b h
    funext o
    have := congrFun h o
    cases o with
    | none => simp [inc] at this; exact this
    | some j => simpa [inc] using this
  have hsplit : S'.fib m x = {q | q ∈ S'.fib m x ∧ q none = 0} ∪ {q | q ∈ S'.fib m x ∧ q none ≠ 0} := by
    ext q; simp only [Set.mem_union, Set.mem_ofPred_eq]; tauto
  have hA : {q | q ∈ S'.fib m x ∧ q none = 0} = ext '' S.fib m x := by
    ext q
    constructor
    · rintro ⟨hq, h0⟩
      refine ⟨fun j => q (some j), ?_, ?_⟩
      · intro k hk
        have := hq k hk
        change S'.val q k = x k at this
        rw [hval q k, h0, zero_mul, add_zero] at this
        exact this
      · funext o; cases o with
        | none => exact h0.symm
        | some j => rfl
    · rintro ⟨q', hq', rfl⟩
      refine ⟨fun k hk => ?_, rfl⟩
      change S'.val (ext q') k = x k
      rw [hval]; simp only [ext, Option.elim, zero_mul, add_zero]; exact hq' k hk
  have hAe : {q | q ∈ S'.fib m x ∧ q none = 0}.encard = (S.fib m x).encard := by
    rw [hA]; exact hext.encard_image _
  unfold cnt
  rw [hsplit, Set.encard_union_eq, hAe]
  · congr 1
    unfold shiftF
    split_ifs with hge
    · refine Eq.trans ?_ (hinc.encard_image (S'.fib m (x - v)))
      congr 1
      ext q
      constructor
      · rintro ⟨hq, h0⟩
        let q0 : Option S.ι → ℕ := q
        have h0' : q0 none ≠ 0 := h0
        refine ⟨Function.update q0 none (q0 none - 1), ?_, ?_⟩
        · intro k hk
          change S'.val _ k = (x - v) k
          have := hq k hk
          change S'.val q0 k = x k at this
          rw [hval q0 k] at this
          rw [hval]
          have e : (fun j => Function.update q0 none (q0 none - 1) (some j)) =
              fun j => q0 (some j) := by
            funext j; rw [Function.update_of_ne (Option.some_ne_none j)]
          rw [e, Function.update_self, Pi.sub_apply]
          have h1 : q0 none = (q0 none - 1) + 1 := by omega
          rw [h1, add_mul, one_mul] at this
          have := hge k hk
          omega
        · funext o; cases o with
          | none =>
            simp only [inc, Function.update_self]
            show q0 none - 1 + 1 = q0 none
            omega
          | some j =>
            simp only [inc]
            rw [Function.update_of_ne (Option.some_ne_none j),
              Function.update_of_ne (Option.some_ne_none j)]
      · rintro ⟨q', hq', rfl⟩
        refine ⟨fun k hk => ?_, by simp [inc]⟩
        change S'.val (inc q') k = x k
        have := hq' k hk
        change S'.val q' k = (x - v) k at this
        rw [hval] at this ⊢
        have e : (fun j => inc q' (some j)) = fun j => q' (some j) := by funext j; simp [inc]
        rw [e]
        simp only [inc, Function.update_self, Pi.sub_apply] at this ⊢
        have := hge k hk
        rw [add_mul, one_mul]
        omega
    · rw [Set.encard_eq_zero, Set.eq_empty_iff_forall_notMem]
      rintro q ⟨hq, h0⟩
      let q0 : Option S.ι → ℕ := q
      have h0' : q0 none ≠ 0 := h0
      apply hge
      intro k hk
      have := hq k hk
      change S'.val q0 k = x k at this
      rw [hval q0 k] at this
      have h1 : v k ≤ q0 none * v k := Nat.le_mul_of_pos_left _ (Nat.pos_of_ne_zero h0')
      omega
  · rw [Set.disjoint_left]
    rintro q ⟨-, h0⟩ ⟨-, h1⟩
    exact h1 h0

lemma ring_unique (m : ℕ) (v : ℕ → ℕ) (hv0 : ∃ k ≤ m, v k ≠ 0) (E G H : (ℕ → ℕ) → ℕ∞)
    (hG : ∀ x, G x = E x + shiftF m v G x) (hH : ∀ x, H x = E x + shiftF m v H x) :
    ∀ x, G x = H x := by
  classical
  suffices ∀ n, ∀ x, ∑ k ∈ range (m + 1), x k = n → G x = H x from fun x => this _ x rfl
  intro n
  induction n using Nat.strong_induction_on with
  | _ n ih =>
    intro x hx
    rw [hG, hH]
    congr 1
    unfold shiftF
    split_ifs with hge
    · refine ih _ ?_ _ rfl
      rw [← hx]
      obtain ⟨k0, hk0, hvk0⟩ := hv0
      apply Finset.sum_lt_sum
      · intro k hk; simp
      · exact ⟨k0, by simp; omega, by simp; have := hge k0 hk0; omega⟩
    · rfl

lemma rep_ring {m : ℕ} (v : ℕ → ℕ) (hv : ∀ k, v k ≠ 0 → k = 0 ∨ k = m) (hv0 : ∃ k ≤ m, v k ≠ 0)
    {E G : (ℕ → ℕ) → ℕ∞} (hE : Rep m E) (hG : ∀ x, G x = E x + shiftF m v G x) : Rep m G := by
  obtain ⟨Ls, hW, he⟩ := hE
  have key : ∀ Ls : List Sys, (∀ S ∈ Ls, S.Within m) → ∃ Ls' : List Sys, (∀ S ∈ Ls', S.Within m) ∧
      ∀ x, (Ls'.map fun S => cnt m S x).sum = (Ls.map fun S => cnt m S x).sum +
        shiftF m v (fun y => (Ls'.map fun S => cnt m S y).sum) x := by
    intro Ls
    induction Ls with
    | nil => exact fun _ => ⟨[], by simp, fun x => by simp [shiftF]⟩
    | cons S Ls ih =>
      intro hW
      obtain ⟨Ls', hW', he'⟩ := ih fun S' h => hW S' (by simp [h])
      have hS := hW S (by simp)
      refine ⟨S.addPeriod m hS v hv :: Ls', ?_, fun x => ?_⟩
      · intro S' h
        rcases List.mem_cons.mp h with rfl | h
        · exact Sys.addPeriod_within S m hS v hv
        · exact hW' S' h
      · simp only [List.map_cons, List.sum_cons]
        rw [shiftF_add, cnt_addPeriod, he']
        ring
  obtain ⟨Ls', hW', he'⟩ := key Ls hW
  refine ⟨Ls', hW', fun x => ?_⟩
  refine ring_unique m v hv0 E G (fun x => (Ls'.map fun S => cnt m S x).sum) hG (fun x => ?_) x
  rw [he', he]

end S2
end FA
