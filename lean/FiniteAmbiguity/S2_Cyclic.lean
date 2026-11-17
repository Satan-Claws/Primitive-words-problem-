/-
# S2: the cyclic case (nontrivial strongly connected components are rings) and the main induction
-/
import FiniteAmbiguity.S2_Induct

namespace FA
namespace S2

open Finset Relation

variable (C : CNF)

/-- `Z` lies in the strongly connected component of `X` on level `m`. -/
def InC (m : ℕ) (X Z : C.N) : Prop := ReflTransGen (Edge C m) X Z ∧ ReflTransGen (Edge C m) Z X

variable {C} {k m : ℕ} {X : C.N}

lemma inC_bdd (hX : Bdd C k m X) {Z : C.N} (hZ : InC C m X Z) : Bdd C k m Z := by
  obtain ⟨p, -, hp⟩ := path_dom C hZ.1
  exact dom_bdd C hp hX

lemma inC_nz (hcyc : TransGen (Edge C m) X X) {Z : C.N} (hZ : InC C m X Z) : NZ C m Z := by
  have : TransGen (Edge C m) X Z := hcyc.trans_left hZ.1
  cases this with
  | single e => exact e.1
  | tail _ e => exact e.1

lemma inC_out (hcyc : TransGen (Edge C m) X X) {Z : C.N} (hZ : InC C m X Z) :
    ∃ W, Edge C m Z W ∧ InC C m X W := by
  have h : TransGen (Edge C m) Z X := TransGen.trans_right hZ.2 hcyc
  obtain ⟨W, e, hW⟩ := TransGen.head'_iff.mp h
  exact ⟨W, e, hZ.1.tail e, hW⟩

lemma inC_child {Z W : C.N} (hZ : InC C m X Z) (e : Edge C m Z W) (hW : ¬ InC C m X W) :
    rank C m W < rank C m X :=
  rank_lt C (hZ.1.tail e) (fun h => hW ⟨hZ.1.tail e, h⟩)

lemma inC_to {Z Y : C.N} (hZ : InC C m X Z) (hY : InC C m X Y) : ReflTransGen (Edge C m) Y Z :=
  hY.2.trans hZ.1

/-- On level 0, no rule of the component has both children in the component. -/
lemma no_quadratic {X : C.N} (hcyc : TransGen (Edge C 0) X X) (hX : Bdd C k 0 X) {Z : C.N}
    (hZ : InC C 0 X Z) {r : C.N × C.N × C.N} (hr : r ∈ binOf C Z) (hU : InC C 0 X r.2.1)
    (hV : InC C 0 X r.2.2) : False := by
  obtain ⟨a, -, ha⟩ := path_dom C (inC_to hZ hU)
  obtain ⟨b, -, hb⟩ := path_dom C (inC_to hZ hV)
  obtain ⟨c, hc⟩ := inC_nz hcyc hZ
  refine pump_quadratic (G C Z 0) (G_dep0 C Z) (fun x hx => G_zero_level C Z x hx) a b
    (fun x => ?_) c hc k (inC_bdd hX hZ)
  calc conv 0 (shiftF 0 a (G C Z 0)) (shiftF 0 b (G C Z 0)) x
      ≤ conv 0 (G C r.2.1 0) (G C r.2.2 0) x := conv_mono 0 ha hb x
    _ = term C 0 r 0 x := rfl
    _ ≤ G C Z 0 x := term_le C hr le_rfl x

variable (C) in
open Classical in
/-- The part of the equation of `Z` whose level-`m` child lies in the component. -/
noncomputable def CP (m : ℕ) (X Z : C.N) (x : ℕ → ℕ) : ℕ∞ :=
  ∑ r ∈ binOf C Z, ((if InC C m X r.2.1 then term C m r m x else 0) +
    (if InC C m X r.2.2 then term C m r 0 x else 0))

lemma decomp (hlow : ∀ i < m, ∀ Z, Bdd C k i Z → Rep i (G C Z i))
    (hrank : ∀ Z, rank C m Z < rank C m X → Bdd C k m Z → Rep m (G C Z m))
    (hcyc : TransGen (Edge C m) X X) (hX : Bdd C k m X) {Z : C.N} (hZ : InC C m X Z) :
    ∃ R, Rep m R ∧ ∀ x, G C Z m x = CP C m X Z x + R x := by
  classical
  have hZb := inC_bdd hX hZ
  have hchild : ∀ W, Edge C m Z W → (fun W => ¬ InC C m X W) W → Bdd C k m W →
      Rep m (G C W m) := fun W e hW hb => hrank W (inC_child hZ e hW) hb
  match m, hlow, hrank, hcyc, hX, hZ, hZb, hchild with
  | 0, hlow, hrank, hcyc, hX, hZ, hZb, hchild =>
    refine ⟨fun x => leafT C Z (segWord 0 x) + ∑ r ∈ binOf C Z,
      (if ¬ InC C 0 X r.2.1 ∧ ¬ InC C 0 X r.2.2 then term C 0 r 0 x else 0), ?_, ?_⟩
    · refine rep_add (leaf_rep C Z 0) (rep_sum (binOf C Z)
        (fun r x => if ¬ InC C 0 X r.2.1 ∧ ¬ InC C 0 X r.2.2 then term C 0 r 0 x else 0)
        fun r hr => ?_)
      exact rep_ite _ fun h => term_rep C (fun W => ¬ InC C 0 X W) hlow hchild hZb hr le_rfl
        (fun _ => h.1) (fun _ => h.2)
    · intro x
      rw [G_eq']
      simp only [zero_add, Finset.range_one, Finset.sum_singleton]
      have per : ∀ r ∈ binOf C Z, term C 0 r 0 x =
          ((if InC C 0 X r.2.1 then term C 0 r 0 x else 0) +
            (if InC C 0 X r.2.2 then term C 0 r 0 x else 0)) +
          (if ¬ InC C 0 X r.2.1 ∧ ¬ InC C 0 X r.2.2 then term C 0 r 0 x else 0) := by
        intro r hr
        by_cases hU : InC C 0 X r.2.1 <;> by_cases hV : InC C 0 X r.2.2
        · exact (no_quadratic hcyc hX hZ hr hU hV).elim
        all_goals simp [hU, hV]
      rw [Finset.sum_congr rfl per, Finset.sum_add_distrib]
      unfold CP
      ring
  | m' + 1, hlow, hrank, hcyc, hX, hZ, hZb, hchild =>
    refine ⟨fun x => leafT C Z (segWord (m' + 1) x) + ∑ r ∈ binOf C Z,
      ((if ¬ InC C (m' + 1) X r.2.1 then term C (m' + 1) r (m' + 1) x else 0) +
       (if ¬ InC C (m' + 1) X r.2.2 then term C (m' + 1) r 0 x else 0) +
       ∑ i ∈ range m', term C (m' + 1) r (i + 1) x), ?_, ?_⟩
    · refine rep_add (leaf_rep C Z _) (rep_sum (binOf C Z) (fun r x =>
        (if ¬ InC C (m' + 1) X r.2.1 then term C (m' + 1) r (m' + 1) x else 0) +
        (if ¬ InC C (m' + 1) X r.2.2 then term C (m' + 1) r 0 x else 0) +
        ∑ i ∈ range m', term C (m' + 1) r (i + 1) x) fun r hr => ?_)
      refine rep_add (rep_add ?_ ?_) ?_
      · exact rep_ite _ fun h => term_rep C (fun W => ¬ InC C (m' + 1) X W) hlow hchild hZb hr
          le_rfl (fun _ => h) (fun h0 => absurd h0 (by omega))
      · exact rep_ite _ fun h => term_rep C (fun W => ¬ InC C (m' + 1) X W) hlow hchild hZb hr
          (Nat.zero_le _) (fun h0 => absurd h0 (by omega)) (fun _ => h)
      · exact rep_sum (range m') (fun i => term C (m' + 1) r (i + 1)) fun i hi =>
          term_rep C (fun W => ¬ InC C (m' + 1) X W) hlow hchild hZb hr
            (by have := Finset.mem_range.mp hi; omega)
            (fun h0 => absurd h0 (by have := Finset.mem_range.mp hi; omega))
            (fun h0 => absurd h0 (by omega))
    · intro x
      rw [G_eq']
      have per : ∀ r ∈ binOf C Z, ∑ i ∈ range (m' + 1 + 1), term C (m' + 1) r i x =
          ((if InC C (m' + 1) X r.2.1 then term C (m' + 1) r (m' + 1) x else 0) +
            (if InC C (m' + 1) X r.2.2 then term C (m' + 1) r 0 x else 0)) +
          ((if ¬ InC C (m' + 1) X r.2.1 then term C (m' + 1) r (m' + 1) x else 0) +
            (if ¬ InC C (m' + 1) X r.2.2 then term C (m' + 1) r 0 x else 0) +
            ∑ i ∈ range m', term C (m' + 1) r (i + 1) x) := by
        intro r hr
        rw [Finset.sum_range_succ, Finset.sum_range_succ']
        by_cases hU : InC C (m' + 1) X r.2.1 <;> by_cases hV : InC C (m' + 1) X r.2.2 <;>
          simp [hU, hV] <;> ring
      rw [Finset.sum_congr rfl per, Finset.sum_add_distrib]
      unfold CP
      ring

/-! ## Units of the component part -/

/-- A unit: a rule, a side (`true`: child on the left, side on the right), and the side length. -/
abbrev Unit' (C : CNF) := (C.N × C.N × C.N) × Bool × ℕ

def uchild (u : Unit' C) : C.N := if u.2.1 then u.1.2.1 else u.1.2.2
def uother (u : Unit' C) : C.N := if u.2.1 then u.1.2.2 else u.1.2.1
def upos (m : ℕ) (u : Unit' C) : ℕ := if u.2.1 then m else 0

open Classical in
noncomputable def wt (m : ℕ) (X : C.N) (u : Unit' C) : ℕ∞ :=
  if InC C m X (uchild u) then G C (uother u) 0 (fun _ => u.2.2) else 0

noncomputable def uval (m : ℕ) (X : C.N) (u : Unit' C) (x : ℕ → ℕ) : ℕ∞ :=
  wt m X u * shiftF m (sg (upos m u) u.2.2) (G C (uchild u) m) x

lemma CP_units (Z : C.N) (x : ℕ → ℕ) :
    CP C m X Z x = ∑ u ∈ binOf C Z ×ˢ (univ ×ˢ range (x 0 + x m + 1)), uval m X u x := by
  classical
  unfold CP
  rw [Finset.sum_product]
  refine Finset.sum_congr rfl fun r _ => ?_
  rw [Finset.sum_product, Fintype.sum_bool]
  simp only [uval, wt, uchild, uother, upos, if_true, Bool.false_eq_true, if_false]
  congr 1
  · by_cases hU : InC C m X r.2.1
    · simp only [hU, if_true]
      unfold term
      rw [Nat.sub_self, conv_right m _ _ (G_dep0 C _)]
      exact sum_extend m m le_rfl _ _ x _ (by omega)
    · simp [hU]
  · by_cases hV : InC C m X r.2.2
    · simp only [hV, if_true]
      unfold term
      rw [Nat.sub_zero, conv_left m _ _ (G_dep0 C _)]
      exact sum_extend m 0 (Nat.zero_le _) _ _ x _ (by omega)
    · simp [hV]

lemma uval_large (u : Unit' C) (x : ℕ → ℕ) (h : x 0 + x m + 1 ≤ u.2.2) : uval m X u x = 0 := by
  unfold uval shiftF
  rw [if_neg, mul_zero]
  intro hge
  have hp : upos m u ≤ m := by unfold upos; split_ifs <;> omega
  have := hge (upos m u) hp
  simp only [sg, if_true] at this
  unfold upos at this
  split_ifs at this <;> omega

lemma mem_index {Z : C.N} {u : Unit' C} (hu : u.1 ∈ binOf C Z) (x : ℕ → ℕ) :
    u ∈ binOf C Z ×ˢ (univ ×ˢ range (x 0 + x m + 1)) ∨ x 0 + x m + 1 ≤ u.2.2 := by
  by_cases h : u.2.2 < x 0 + x m + 1
  · left; simp [hu, h]
  · right; omega

lemma uval_le_CP {Z : C.N} {u : Unit' C} (hu : u.1 ∈ binOf C Z) (x : ℕ → ℕ) :
    uval m X u x ≤ CP C m X Z x := by
  rw [CP_units]
  rcases mem_index hu x with h | h
  · exact Finset.single_le_sum (f := fun u => uval m X u x) (fun _ _ => zero_le) h
  · rw [uval_large u x h]; exact zero_le

lemma two_le_CP {Z : C.N} {u u' : Unit' C} (hu : u.1 ∈ binOf C Z) (hu' : u'.1 ∈ binOf C Z)
    (hne : u ≠ u') (x : ℕ → ℕ) : uval m X u x + uval m X u' x ≤ CP C m X Z x := by
  rcases mem_index (m := m) hu x with h | h
  · rcases mem_index (m := m) hu' x with h' | h'
    · rw [CP_units]
      refine le_trans (le_of_eq (Finset.sum_pair (f := fun u => uval m X u x) hne).symm) ?_
      apply Finset.sum_le_sum_of_subset
      intro v hv
      simp only [mem_insert, mem_singleton] at hv
      rcases hv with rfl | rfl <;> assumption
    · rw [uval_large u' x h', add_zero]; exact uval_le_CP hu x
  · rw [uval_large u x h, zero_add]; exact uval_le_CP hu' x

lemma uval_dom {Z : C.N} (hZ : InC C m X Z) (u : Unit' C) (n : ℕ) (hn : (n : ℕ∞) ≤ wt m X u)
    (hn0 : n ≠ 0) : ∃ α, ∀ x, (n : ℕ∞) * shiftF m α (G C Z m) x ≤ uval m X u x := by
  classical
  have hc : InC C m X (uchild u) := by
    by_contra h
    simp only [wt, h, if_false] at hn
    norm_cast at hn
    omega
  obtain ⟨q, -, hq⟩ := path_dom C (inC_to hZ hc)
  refine ⟨sg (upos m u) u.2.2 + q, fun x => ?_⟩
  unfold uval
  rw [← shiftF_comp]
  exact mul_le_mul' hn (shiftF_mono m _ hq x)

lemma edge_unit {Z W : C.N} (e : Edge C m Z W) (hW : InC C m X W) :
    ∃ u : Unit' C, u.1 ∈ binOf C Z ∧ uchild u = W ∧ wt m X u ≠ 0 := by
  classical
  obtain ⟨-, r, hr, (⟨rfl, y, hy⟩ | ⟨rfl, y, hy⟩)⟩ := e
  · refine ⟨(r, true, y 0), hr, rfl, ?_⟩
    simp only [wt, uchild, uother, if_true, hW]
    rwa [G_dep0 C _ (fun _ => y 0) y rfl]
  · refine ⟨(r, false, y 0), hr, rfl, ?_⟩
    simp only [wt, uchild, uother, Bool.false_eq_true, if_false, hW, if_true]
    rwa [G_dep0 C _ (fun _ => y 0) y rfl]

lemma mass (hcyc : TransGen (Edge C m) X X) (hX : Bdd C k m X) {Z : C.N} (hZ : InC C m X Z)
    (hCP : ∀ x, CP C m X Z x ≤ G C Z m x) :
    ∃ u0 : Unit' C, u0.1 ∈ binOf C Z ∧ wt m X u0 = 1 ∧ u0.2.2 ≠ 0 ∧
      ∀ u : Unit' C, u.1 ∈ binOf C Z → u ≠ u0 → wt m X u = 0 := by
  classical
  have hbdd := inC_bdd hX hZ
  obtain ⟨a, ha⟩ := inC_nz hcyc hZ
  have pump : ∀ α β : ℕ → ℕ, (∀ x, shiftF m α (G C Z m) x + shiftF m β (G C Z m) x ≤
      CP C m X Z x) → False :=
    fun α β h => pump_linear m (G C Z m) α β (fun x => (h x).trans (hCP x)) a ha k hbdd
  obtain ⟨W, e, hW⟩ := inC_out hcyc hZ
  obtain ⟨u0, hu0, -, hw0⟩ := edge_unit e hW
  have one_le : ∀ u : Unit' C, wt m X u ≠ 0 → ((1 : ℕ) : ℕ∞) ≤ wt m X u := fun u h => by
    simpa using Order.one_le_iff_ne_zero.mpr h
  have hlt : wt m X u0 < 2 := by
    by_contra hge
    push_neg at hge
    obtain ⟨α, hα⟩ := uval_dom hZ u0 2 (by simpa using hge) (by norm_num)
    exact pump α α fun x => by
      rw [← two_mul]; exact (hα x).trans (uval_le_CP hu0 x)
  refine ⟨u0, hu0, ?_, ?_, ?_⟩
  · generalize wt m X u0 = w at hw0 hlt
    induction w using ENat.recTopCoe with
    | top => simp at hlt
    | coe n =>
      norm_cast at hw0 hlt ⊢
      omega
  · intro h
    apply hw0
    simp only [wt]
    split_ifs
    · exact G_zero_level C _ _ (by simpa using h)
    · rfl
  · intro u hu hne
    by_contra hw
    obtain ⟨α, hα⟩ := uval_dom hZ u0 1 (one_le u0 hw0) one_ne_zero
    obtain ⟨β, hβ⟩ := uval_dom hZ u 1 (one_le u hw) one_ne_zero
    refine pump α β fun x => ?_
    have := add_le_add (hα x) (hβ x)
    simp only [Nat.cast_one, one_mul] at this
    exact this.trans (two_le_CP hu0 hu (Ne.symm hne) x)

lemma CP_single {Z : C.N} {u0 : Unit' C} (hu0 : u0.1 ∈ binOf C Z) (hw : wt m X u0 = 1)
    (hoth : ∀ u : Unit' C, u.1 ∈ binOf C Z → u ≠ u0 → wt m X u = 0) (x : ℕ → ℕ) :
    CP C m X Z x = shiftF m (sg (upos m u0) u0.2.2) (G C (uchild u0) m) x := by
  rw [CP_units, Finset.sum_eq_single u0]
  · simp [uval, hw]
  · intro u hu hne
    simp only [mem_product] at hu
    simp [uval, hoth u hu.1 hne]
  · intro h
    rcases mem_index (m := m) hu0 x with h' | h'
    · exact absurd h' h
    · exact uval_large u0 x h'

/-! ## The cyclic step -/

lemma step_cyclic (hlow : ∀ i < m, ∀ Z, Bdd C k i Z → Rep i (G C Z i))
    (hrank : ∀ Z, rank C m Z < rank C m X → Bdd C k m Z → Rep m (G C Z m))
    (hX : Bdd C k m X) (hcyc : TransGen (Edge C m) X X) : Rep m (G C X m) := by
  classical
  have key : ∀ Z, InC C m X Z → ∃ W p R, InC C m X W ∧ Supp m p ∧ (∃ j ≤ m, p j ≠ 0) ∧
      Rep m R ∧ (∀ x, G C Z m x = shiftF m p (G C W m) x + R x) ∧
      (∀ W', Edge C m Z W' → InC C m X W' → W' = W) := by
    intro Z hZ
    obtain ⟨R, hR, hG⟩ := decomp hlow hrank hcyc hX hZ
    have hCP : ∀ x, CP C m X Z x ≤ G C Z m x := fun x => by rw [hG]; exact le_self_add
    obtain ⟨u0, hu0, hw, hs, hoth⟩ := mass hcyc hX hZ hCP
    have hc : InC C m X (uchild u0) := by
      by_contra h; simp [wt, h] at hw
    refine ⟨uchild u0, sg (upos m u0) u0.2.2, R, hc, ?_, ⟨upos m u0, ?_, ?_⟩, hR, ?_, ?_⟩
    · simpa [upos] using supp_sg m u0.2.2 u0.2.1
    · unfold upos; split_ifs <;> omega
    · simpa [sg] using hs
    · intro x; rw [hG, CP_single hu0 hw hoth]
    · intro W' e hW'
      obtain ⟨u, hu, rfl, hwu⟩ := edge_unit e hW'
      by_contra hne
      exact hwu (hoth u hu (fun h => hne (h ▸ rfl)))
  have tele : ∀ Z, ReflTransGen (Edge C m) Z X → InC C m X Z → ∃ P E, Supp m P ∧ Rep m E ∧
      ∀ x, G C Z m x = E x + shiftF m P (G C X m) x := by
    intro Z h
    induction h using ReflTransGen.head_induction_on with
    | refl =>
      intro _
      exact ⟨0, fun _ => 0, fun k hk => absurd rfl hk, rep_zero m,
        fun x => by rw [shiftF_zero_vec, zero_add]⟩
    | head e h ih =>
      rename_i Z' W'
      intro hZ
      obtain ⟨W, p, R, hW, hp, -, hR, hG, huniq⟩ := key Z' hZ
      have hW' : InC C m X W' := ⟨hZ.1.tail e, h⟩
      obtain rfl := huniq W' e hW'
      obtain ⟨P, E, hP, hE, hGW⟩ := ih hW'
      refine ⟨p + P, fun x => R x + shiftF m p E x, supp_add hp hP, rep_add hR (rep_shift p hE),
        fun x => ?_⟩
      have hfun : G C W' m = fun y => E y + shiftF m P (G C X m) y := funext hGW
      rw [hG, hfun, shiftF_add, shiftF_comp]
      ring
  obtain ⟨W, p, R, hW, hp, hp0, hR, hG, -⟩ := key X ⟨ReflTransGen.refl, ReflTransGen.refl⟩
  obtain ⟨P, E, hP, hE, hGW⟩ := tele W hW.2 hW
  refine rep_ring (p + P) (supp_add hp hP) ?_ (rep_add hR (rep_shift p hE)) (fun x => ?_)
  · obtain ⟨j, hj, hpj⟩ := hp0
    exact ⟨j, hj, by simp only [Pi.add_apply]; omega⟩
  · have hfun : G C W m = fun y => E y + shiftF m P (G C X m) y := funext hGW
    rw [hG, hfun, shiftF_add, shiftF_comp]
    ring

/-! ## The main induction -/

variable (C) in
theorem rep_main (k : ℕ) : ∀ m X, Bdd C k m X → Rep m (G C X m) := by
  intro m
  induction m using Nat.strong_induction_on with
  | _ m IHm =>
  have key : ∀ n X, rank C m X = n → Bdd C k m X → Rep m (G C X m) := by
    intro n
    induction n using Nat.strong_induction_on with
    | _ n IHn =>
    intro X hn hX
    have hrank : ∀ Z, rank C m Z < rank C m X → Bdd C k m Z → Rep m (G C Z m) :=
      fun Z h hZ => IHn _ (hn ▸ h) Z rfl hZ
    by_cases hcyc : TransGen (Edge C m) X X
    · exact step_cyclic (fun i hi Z hZ => IHm i hi Z hZ) hrank hX hcyc
    · exact step_acyclic C (fun i hi Z hZ => IHm i hi Z hZ) hrank hX hcyc
  exact fun X hX => key _ X rfl hX

end S2
end FA
