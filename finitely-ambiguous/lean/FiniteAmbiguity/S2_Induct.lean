/-
# S2: the main induction (tree counts on segment words are representable)
-/
import FiniteAmbiguity.S2_Shift

namespace FA
namespace S2

open Finset Relation

variable (C : CNF)

lemma G_dep0 (X : C.N) : Dep0 (G C X 0) := fun x y h =>
  G_congr C X 0 x y (fun k hk => by rw [Nat.le_zero.mp hk]; exact h)

/-- The term of rule `r` splitting at block `i`, on level `m`. -/
noncomputable def term (m : ℕ) (r : C.N × C.N × C.N) (i : ℕ) : (ℕ → ℕ) → ℕ∞ :=
  conv i (G C r.2.1 i) (G C r.2.2 (m - i))

lemma G_eq' (X : C.N) (m : ℕ) (x : ℕ → ℕ) :
    G C X m x = leafT C X (segWord m x) + ∑ r ∈ binOf C X, ∑ i ∈ range (m + 1), term C m r i x :=
  G_eq C X m x

lemma term_le {X : C.N} {m : ℕ} {r : C.N × C.N × C.N} (hr : r ∈ binOf C X) {i : ℕ} (hi : i ≤ m)
    (x : ℕ → ℕ) : term C m r i x ≤ G C X m x := by
  rw [G_eq']
  refine le_trans ?_ le_add_self
  refine le_trans ?_ (Finset.single_le_sum (fun r _ => zero_le) hr)
  exact Finset.single_le_sum (f := fun i => term C m r i x) (fun i _ => zero_le)
    (by simp; omega)

/-- Gluing two segment vectors at block `i`. -/
def merge (i : ℕ) (y z : ℕ → ℕ) : ℕ → ℕ :=
  fun k => if k < i then y k else if k = i then y i + z 0 else z (k - i)

lemma term_ge_prod (m : ℕ) (r : C.N × C.N × C.N) {i : ℕ} (hi : i ≤ m) (y z : ℕ → ℕ) :
    G C r.2.1 i y * G C r.2.2 (m - i) z ≤ term C m r i (merge i y z) := by
  unfold term conv
  have hmem : y i ∈ range (merge i y z i + 1) := by simp [merge]
  refine le_trans (le_of_eq ?_) (Finset.single_le_sum (f := fun j =>
    G C r.2.1 i (Function.update (merge i y z) i j) * G C r.2.2 (m - i) (zf i j (merge i y z)))
    (fun j _ => zero_le) hmem)
  congr 1
  · apply G_congr
    intro k hk
    rcases Nat.lt_or_ge k i with h | h
    · rw [Function.update_of_ne (by omega)]; simp [merge, h]
    · have : k = i := by omega
      subst this; simp
  · apply G_congr
    intro k hk
    by_cases h0 : k = 0
    · subst h0; simp [zf, merge]
    · simp only [zf, merge, h0, if_false, show ¬ (k + i < i) by omega, show k + i ≠ i by omega]
      congr 1; omega

/-- Bounded on level `m`. -/
def Bdd (k m : ℕ) (X : C.N) : Prop := ∀ x, G C X m x ≤ k

/-- Not identically zero on level `m`. -/
def NZ (m : ℕ) (X : C.N) : Prop := ∃ x, G C X m x ≠ 0

lemma term_cases {k m : ℕ} {Y : C.N} (hY : Bdd C k m Y) {r : C.N × C.N × C.N}
    (hr : r ∈ binOf C Y) {i : ℕ} (hi : i ≤ m) :
    (∀ x, term C m r i x = 0) ∨
      (NZ C i r.2.1 ∧ NZ C (m - i) r.2.2 ∧ Bdd C k i r.2.1 ∧ Bdd C k (m - i) r.2.2) := by
  by_cases hU : NZ C i r.2.1
  · by_cases hV : NZ C (m - i) r.2.2
    · right
      refine ⟨hU, hV, ?_, ?_⟩
      · intro y
        obtain ⟨z, hz⟩ := hV
        calc G C r.2.1 i y ≤ G C r.2.1 i y * G C r.2.2 (m - i) z :=
              le_mul_of_one_le_right' (Order.one_le_iff_ne_zero.mpr hz)
          _ ≤ term C m r i (merge i y z) := term_ge_prod C m r hi y z
          _ ≤ G C Y m (merge i y z) := term_le C hr hi _
          _ ≤ k := hY _
      · intro z
        obtain ⟨y, hy⟩ := hU
        calc G C r.2.2 (m - i) z ≤ G C r.2.1 i y * G C r.2.2 (m - i) z :=
              le_mul_of_one_le_left' (Order.one_le_iff_ne_zero.mpr hy)
          _ ≤ term C m r i (merge i y z) := term_ge_prod C m r hi y z
          _ ≤ G C Y m (merge i y z) := term_le C hr hi _
          _ ≤ k := hY _
    · left
      intro x
      simp only [NZ, not_exists, not_not] at hV
      simp [term, conv, hV]
  · left
    intro x
    simp only [NZ, not_exists, not_not] at hU
    simp [term, conv, hU]

/-! ## The edge relation on level `m` -/

/-- `X → Y` on level `m`: a rule of `X` has `Y` as the level-`m` child and a non-empty side. -/
def Edge (m : ℕ) (X Y : C.N) : Prop :=
  NZ C m Y ∧ ∃ r ∈ binOf C X, (r.2.1 = Y ∧ NZ C 0 r.2.2) ∨ (r.2.2 = Y ∧ NZ C 0 r.2.1)

/-- Support in `{0, m}`. -/
def Supp (m : ℕ) (p : ℕ → ℕ) : Prop := ∀ k, p k ≠ 0 → k = 0 ∨ k = m

lemma supp_add {m : ℕ} {p q : ℕ → ℕ} (hp : Supp m p) (hq : Supp m q) : Supp m (p + q) := by
  intro k hk
  simp only [Pi.add_apply] at hk
  by_cases h : p k = 0
  · exact hq k (by omega)
  · exact hp k h

lemma supp_sg (m s : ℕ) (b : Bool) : Supp m (sg (if b then m else 0) s) := by
  intro k hk
  by_contra hc
  push_neg at hc
  apply hk
  simp only [sg]
  cases b <;> simp_all

lemma unit_le (m i s : ℕ) (hi : i ≤ m) (w : ℕ → ℕ∞) (f : (ℕ → ℕ) → ℕ∞) (x : ℕ → ℕ) :
    w s * shiftF m (sg i s) f x ≤ ∑ s' ∈ range (x i + 1), w s' * shiftF m (sg i s') f x := by
  by_cases hs : s < x i + 1
  · exact Finset.single_le_sum (f := fun s' => w s' * shiftF m (sg i s') f x)
      (fun _ _ => zero_le) (by simpa using hs)
  · unfold shiftF
    rw [if_neg, mul_zero]
    · exact zero_le
    · intro h; have := h i hi; simp [sg] at this; omega

lemma G_zero_of_nz {X : C.N} {y : ℕ → ℕ} (h : G C X 0 y ≠ 0) : y 0 ≠ 0 :=
  fun h' => h (G_zero_level C X y h')

/-- An edge gives a shifted copy of the child below the parent. -/
lemma edge_dom {m : ℕ} {X Y : C.N} (h : Edge C m X Y) :
    ∃ p, Supp m p ∧ (∃ k ≤ m, p k ≠ 0) ∧ ∀ x, shiftF m p (G C Y m) x ≤ G C X m x := by
  obtain ⟨-, r, hr, (⟨rfl, y, hy⟩ | ⟨rfl, y, hy⟩)⟩ := h
  · refine ⟨sg m (y 0), ?_, ⟨m, le_rfl, by simpa [sg] using G_zero_of_nz C hy⟩, fun x => ?_⟩
    · simpa using supp_sg m (y 0) true
    · have h1 := term_le C hr (le_refl m) x
      unfold term at h1
      rw [Nat.sub_self, conv_right m _ _ (G_dep0 C _)] at h1
      refine le_trans ?_ (le_trans (unit_le m m (y 0) le_rfl _ _ x) h1)
      have : G C r.2.2 0 (fun _ => y 0) = G C r.2.2 0 y := G_dep0 C _ _ _ rfl
      rw [this]
      exact le_mul_of_one_le_left' (Order.one_le_iff_ne_zero.mpr hy)
  · refine ⟨sg 0 (y 0), ?_, ⟨0, Nat.zero_le _, by simpa [sg] using G_zero_of_nz C hy⟩,
      fun x => ?_⟩
    · simpa using supp_sg m (y 0) false
    · have h1 := term_le C hr (Nat.zero_le m) x
      unfold term at h1
      rw [Nat.sub_zero, conv_left m _ _ (G_dep0 C _)] at h1
      refine le_trans ?_ (le_trans (unit_le m 0 (y 0) (Nat.zero_le _) _ _ x) h1)
      have : G C r.2.1 0 (fun _ => y 0) = G C r.2.1 0 y := G_dep0 C _ _ _ rfl
      rw [this]
      exact le_mul_of_one_le_left' (Order.one_le_iff_ne_zero.mpr hy)

lemma path_dom {m : ℕ} {X Y : C.N} (h : ReflTransGen (Edge C m) X Y) :
    ∃ p, Supp m p ∧ ∀ x, shiftF m p (G C Y m) x ≤ G C X m x := by
  induction h with
  | refl => exact ⟨0, fun k hk => absurd rfl hk, fun x => le_of_eq (shiftF_zero_vec m _ x)⟩
  | tail _ e ih =>
    obtain ⟨p, hp, hle⟩ := ih
    obtain ⟨q, hq, -, hle'⟩ := edge_dom C e
    refine ⟨p + q, supp_add hp hq, fun x => ?_⟩
    rw [← shiftF_comp]
    exact le_trans (shiftF_mono m p hle' x) (hle x)

lemma dom_bdd {k m : ℕ} {X Y : C.N} {p : ℕ → ℕ} (h : ∀ x, shiftF m p (G C Y m) x ≤ G C X m x)
    (hX : Bdd C k m X) : Bdd C k m Y := by
  intro y
  calc G C Y m y = shiftF m p (G C Y m) (y + p) := (shiftF_at m p _ y).symm
    _ ≤ G C X m (y + p) := h _
    _ ≤ k := hX _

open Classical in
/-- Number of nonterminals reachable on level `m`. -/
noncomputable def rank (m : ℕ) (X : C.N) : ℕ :=
  (univ.filter (fun Y => ReflTransGen (Edge C m) X Y)).card

lemma rank_lt {m : ℕ} {X Y : C.N} (h : ReflTransGen (Edge C m) X Y)
    (h' : ¬ ReflTransGen (Edge C m) Y X) : rank C m Y < rank C m X := by
  classical
  unfold rank
  apply Finset.card_lt_card
  rw [Finset.ssubset_iff_of_subset]
  · refine ⟨X, ?_, by simpa using h'⟩
    simp only [mem_filter, mem_univ, true_and]; exact ReflTransGen.refl
  · intro Z hZ
    simp only [mem_filter, mem_univ, true_and] at hZ ⊢
    exact h.trans hZ

/-! ## Terminal rules -/

lemma leafT_eq (X : C.N) (w : Word) :
    leafT C X w = if w = [true] then (if (X, true) ∈ C.term then 1 else 0)
      else if w = [false] then (if (X, false) ∈ C.term then 1 else 0) else 0 := by
  match w with
  | [] => simp [leafT]
  | [c] => cases c <;> simp [leafT]
  | c :: d :: w => simp [leafT]

lemma leaf_rep (X : C.N) (m : ℕ) : Rep m (fun x => leafT C X (segWord m x)) := by
  classical
  match m with
  | 0 =>
    refine rep_congr (rep_ite ((X, true) ∈ C.term) fun _ => rep_point 0 (fun _ => 1)) ?_
    intro x
    rw [leafT_eq]
    have e : (∀ k ≤ 0, (fun _ => 1) k = x k) ↔ x 0 = 1 := by
      constructor
      · intro h; exact (h 0 le_rfl).symm
      · intro h k hk; rw [Nat.le_zero.mp hk]; exact h.symm
    simp only [segWord, e]
    by_cases h1 : x 0 = 1
    · simp [h1]
    · have : List.replicate (x 0) true ≠ [true] := by
        intro h; have := congrArg List.length h; simp at this; exact h1 this
      have h2 : List.replicate (x 0) true ≠ [false] := by
        intro h; have := congrArg List.head? h; cases hx : x 0 <;> simp_all [List.replicate_succ]
      simp [this, h2, h1]
  | 1 =>
    refine rep_congr (rep_ite ((X, false) ∈ C.term) fun _ => rep_point 1 (fun _ => 0)) ?_
    intro x
    rw [leafT_eq]
    have e : (∀ k ≤ 1, (fun _ => 0) k = x k) ↔ x 0 = 0 ∧ x 1 = 0 := by
      constructor
      · intro h; exact ⟨(h 0 (by omega)).symm, (h 1 le_rfl).symm⟩
      · intro h k hk
        rcases Nat.le_one_iff_eq_zero_or_eq_one.mp hk with rfl | rfl
        exacts [h.1.symm, h.2.symm]
    simp only [segWord, e]
    have hne : List.replicate (x 0) true ++ false :: List.replicate (x 1) true ≠ [true] := by
      intro h
      have hl := congrArg List.length h
      cases hx : x 0 <;> simp_all [List.replicate_succ]
    simp only [hne, if_false]
    by_cases h1 : x 0 = 0 ∧ x 1 = 0
    · simp [h1.1, h1.2]
    · have : List.replicate (x 0) true ++ false :: List.replicate (x 1) true ≠ [false] := by
        intro h
        apply h1
        have hl := congrArg List.length h
        simp at hl
        refine ⟨by omega, by omega⟩
      simp [this, h1]
  | m + 2 =>
    refine rep_congr (rep_zero (m + 2)) ?_
    intro x
    rw [leafT_eq]
    have hl : 2 ≤ (segWord (m + 2) x).length := by
      simp [segWord]; omega
    have h1 : segWord (m + 2) x ≠ [true] := fun h => by rw [h] at hl; simp at hl
    have h2 : segWord (m + 2) x ≠ [false] := fun h => by rw [h] at hl; simp at hl
    simp [h1, h2]

/-! ## Representability of terms -/

lemma term_rep {k m : ℕ} {Y : C.N} (P : C.N → Prop)
    (hlow : ∀ i < m, ∀ Z, Bdd C k i Z → Rep i (G C Z i))
    (hchild : ∀ Z, Edge C m Y Z → P Z → Bdd C k m Z → Rep m (G C Z m))
    (hY : Bdd C k m Y) {r : C.N × C.N × C.N} (hr : r ∈ binOf C Y) {i : ℕ} (hi : i ≤ m)
    (hPU : i = m → P r.2.1) (hPV : i = 0 → P r.2.2) : Rep m (term C m r i) := by
  rcases term_cases C hY hr hi with h0 | ⟨nU, nV, bU, bV⟩
  · exact rep_congr (rep_zero m) (fun x => (h0 x).symm)
  have hU : Rep i (G C r.2.1 i) := by
    rcases Nat.lt_or_ge i m with h | h
    · exact hlow i h _ bU
    · have him : i = m := by omega
      subst him
      rw [Nat.sub_self] at nV
      exact hchild _ ⟨nU, r, hr, Or.inl ⟨rfl, nV⟩⟩ (hPU rfl) bU
  have hV : Rep (m - i) (G C r.2.2 (m - i)) := by
    rcases Nat.lt_or_ge (m - i) m with h | h
    · exact hlow _ h _ bV
    · have hi0 : i = 0 := by omega
      subst hi0
      rw [Nat.sub_zero] at nV bV ⊢
      exact hchild _ ⟨nV, r, hr, Or.inr ⟨rfl, nU⟩⟩ (hPV rfl) bV
  have := rep_conv hU hV
  rw [show i + (m - i) = m by omega] at this
  exact this

/-! ## The acyclic case -/

lemma step_acyclic {k m : ℕ} {X : C.N}
    (hlow : ∀ i < m, ∀ Z, Bdd C k i Z → Rep i (G C Z i))
    (hrank : ∀ Z, rank C m Z < rank C m X → Bdd C k m Z → Rep m (G C Z m))
    (hX : Bdd C k m X) (hcyc : ¬ TransGen (Edge C m) X X) : Rep m (G C X m) := by
  have hchild : ∀ Z, Edge C m X Z → True → Bdd C k m Z → Rep m (G C Z m) := by
    intro Z e _ hZ
    refine hrank Z (rank_lt C (ReflTransGen.single e) fun h => hcyc ?_) hZ
    exact TransGen.head' e h
  refine rep_congr (rep_add (leaf_rep C X m) (rep_sum (binOf C X)
    (fun r x => ∑ i ∈ range (m + 1), term C m r i x) fun r hr =>
    rep_sum (range (m + 1)) (fun i => term C m r i) fun i hi => term_rep C (fun _ => True) hlow hchild hX hr
      (by have := Finset.mem_range.mp hi; omega) (fun _ => trivial) (fun _ => trivial))) ?_
  intro x
  rw [G_eq']

end S2
end FA
