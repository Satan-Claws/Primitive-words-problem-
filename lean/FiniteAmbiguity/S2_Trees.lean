/-
# S2: tree counts of a CNF grammar and their recursion (helper for `CNFStructure.lean`)
-/
import FiniteAmbiguity.CNFDefs
import FiniteAmbiguity.Prelude

namespace FA
namespace S2

open Finset

/-- encard of a finite pairwise-disjoint union indexed by a finset. -/
lemma encard_biUnion_finset {ι α : Type*} [DecidableEq ι] (t : Finset ι) (s : ι → Set α)
    (hs : ∀ i ∈ t, ∀ j ∈ t, i ≠ j → Disjoint (s i) (s j)) :
    (⋃ i ∈ t, s i).encard = ∑ i ∈ t, (s i).encard := by
  induction t using Finset.induction_on with
  | empty => simp
  | insert a t ha ih =>
    rw [Finset.sum_insert ha, Finset.set_biUnion_insert, Set.encard_union_eq]
    · rw [ih (fun i hi j hj hij => hs i (by simp [hi]) j (by simp [hj]) hij)]
    · rw [Set.disjoint_iUnion₂_right]
      intro i hi
      exact hs a (by simp) i (by simp [hi]) (by rintro rfl; exact ha hi)

lemma CTree.yield_ne_nil {N : Type} (t : CTree N) : t.yield ≠ [] := by
  induction t with
  | leaf A c => simp [CTree.yield]
  | node A l r ihl _ => simp [CTree.yield, ihl]

variable (C : CNF)

/-- Number of derivation trees of `w` from `X`. -/
noncomputable def T (X : C.N) (w : Word) : ℕ∞ := {t | C.IsDerivFrom X t w}.encard

lemma T_nil (X : C.N) : T C X [] = 0 := by
  simp only [T, Set.encard_eq_zero]
  ext t
  simp only [Set.mem_ofPred_eq, Set.mem_empty_iff_false, iff_false]
  rintro ⟨-, -, h⟩
  exact CTree.yield_ne_nil t h

/-- Contribution of terminal rules. -/
noncomputable def leafT (X : C.N) : Word → ℕ∞
  | [c] => if (X, c) ∈ C.term then 1 else 0
  | _ => 0

/-- Rules with left side `X`. -/
noncomputable def binOf (X : C.N) : Finset (C.N × C.N × C.N) := C.bin.filter (fun r => r.1 = X)

lemma leaf_part (X : C.N) (w : Word) :
    {t | C.IsDerivFrom X t w ∧ ∃ c, t = CTree.leaf X c}.encard = leafT C X w := by
  match w with
  | [] =>
    simp only [leafT, Set.encard_eq_zero]
    ext t; simp only [Set.mem_ofPred_eq, Set.mem_empty_iff_false, iff_false]
    rintro ⟨⟨-, -, h⟩, -⟩; exact CTree.yield_ne_nil t h
  | [c] =>
    simp only [leafT]
    split_ifs with hc
    · rw [Set.encard_eq_one]
      refine ⟨.leaf X c, ?_⟩
      ext t
      simp only [Set.mem_ofPred_eq, Set.mem_singleton_iff]
      constructor
      · rintro ⟨⟨-, -, hy⟩, c', rfl⟩
        simp [CTree.yield] at hy; rw [hy]
      · rintro rfl; exact ⟨⟨hc, rfl, rfl⟩, c, rfl⟩
    · rw [Set.encard_eq_zero]
      ext t
      simp only [Set.mem_ofPred_eq, Set.mem_empty_iff_false, iff_false]
      rintro ⟨⟨hv, -, hy⟩, c', rfl⟩
      simp [CTree.yield] at hy; subst hy
      exact hc hv
  | c :: d :: w' =>
    simp only [leafT, Set.encard_eq_zero]
    ext t; simp only [Set.mem_ofPred_eq, Set.mem_empty_iff_false, iff_false]
    rintro ⟨⟨-, -, hy⟩, c', rfl⟩
    simp [CTree.yield] at hy

lemma T_eq (X : C.N) (w : Word) :
    T C X w = leafT C X w + ∑ r ∈ binOf C X, ∑ k ∈ range (w.length + 1),
      T C r.2.1 (w.take k) * T C r.2.2 (w.drop k) := by
  classical
  -- decompose the set
  let L : Set (CTree C.N) := {t | C.IsDerivFrom X t w ∧ ∃ c, t = .leaf X c}
  let S : (C.N × C.N × C.N) × ℕ → Set (CTree C.N) := fun p =>
    (fun q : CTree C.N × CTree C.N => CTree.node X q.1 q.2) ''
      ({l | C.IsDerivFrom p.1.2.1 l (w.take p.2)} ×ˢ {r | C.IsDerivFrom p.1.2.2 r (w.drop p.2)})
  have hset : {t | C.IsDerivFrom X t w} = L ∪ ⋃ p ∈ binOf C X ×ˢ range (w.length + 1), S p := by
    ext t
    constructor
    · intro ht
      cases t with
      | leaf A c =>
        have h := ht.2.1
        simp only [CTree.root] at h
        exact Or.inl ⟨ht, c, by rw [h]⟩
      | node A l r =>
        obtain ⟨⟨hrule, hl, hr⟩, hroot, hy⟩ := ht
        simp only [CTree.root] at hroot
        subst hroot
        refine Or.inr ?_
        simp only [Set.mem_iUnion]
        refine ⟨((A, l.root, r.root), l.yield.length), ?_, ?_⟩
        · simp only [CTree.yield] at hy
          simp [binOf, hrule, ← hy]
        · refine ⟨(l, r), ?_, rfl⟩
          simp only [CTree.yield] at hy
          subst hy
          simp [CNF.IsDerivFrom, hl, hr]
    · rintro (⟨h, -⟩ | h)
      · exact h
      · simp only [Set.mem_iUnion] at h
        obtain ⟨⟨⟨A, U, V⟩, k⟩, hp, ⟨l, r⟩, ⟨hl, hr⟩, rfl⟩ := h
        simp only [binOf, mem_product, mem_filter] at hp
        obtain ⟨⟨hrule, rfl⟩, -⟩ := hp
        obtain ⟨hlv, hlr, hly⟩ := hl
        obtain ⟨hrv, hrr, hry⟩ := hr
        refine ⟨⟨?_, hlv, hrv⟩, rfl, ?_⟩
        · simp only at hlr hrr; rw [hlr, hrr]; exact hrule
        · simp only [CTree.yield] at *; rw [hly, hry, List.take_append_drop]
  have hdisj : Disjoint L (⋃ p ∈ binOf C X ×ˢ range (w.length + 1), S p) := by
    rw [Set.disjoint_iUnion₂_right]
    intro p _
    rw [Set.disjoint_left]
    rintro t ⟨-, c, rfl⟩ ⟨q, -, hq⟩
    cases hq
  have hpair : ∀ i ∈ binOf C X ×ˢ range (w.length + 1), ∀ j ∈ binOf C X ×ˢ range (w.length + 1),
      i ≠ j → Disjoint (S i) (S j) := by
    rintro ⟨⟨A, U, V⟩, k⟩ hi ⟨⟨A', U', V'⟩, k'⟩ hj hij
    simp only [binOf, mem_product, mem_filter, mem_range] at hi hj
    obtain ⟨⟨-, rfl⟩, hk⟩ := hi
    obtain ⟨⟨-, rfl⟩, hk'⟩ := hj
    rw [Set.disjoint_left]
    rintro t ⟨⟨l, r⟩, ⟨hl, hr⟩, rfl⟩ ⟨⟨l', r'⟩, ⟨hl', hr'⟩, he⟩
    simp only [CTree.node.injEq, true_and] at he
    obtain ⟨rfl, rfl⟩ := he
    apply hij
    simp only [Set.mem_ofPred_eq] at hl hr hl' hr'
    have h1 : U' = U := hl'.2.1.symm.trans hl.2.1
    have h2 : V' = V := hr'.2.1.symm.trans hr.2.1
    have h3 : (w.take k).length = (w.take k').length := by rw [← hl.2.2, hl'.2.2]
    simp only [List.length_take] at h3
    have : k = k' := by omega
    subst h1 h2 this; rfl
  have hinj : Function.Injective (fun q : CTree C.N × CTree C.N => CTree.node X q.1 q.2) := by
    rintro ⟨a, b⟩ ⟨a', b'⟩ h
    simp only [CTree.node.injEq, true_and] at h
    rw [h.1, h.2]
  have hL : L.encard = leafT C X w := leaf_part C X w
  unfold T
  rw [hset, Set.encard_union_eq hdisj, hL, encard_biUnion_finset _ _ hpair, Finset.sum_product]
  congr 1
  refine Finset.sum_congr rfl fun r _ => Finset.sum_congr rfl fun k _ => ?_
  simp only [S]
  rw [hinj.encard_image, Set.encard_prod]

/-! ## Segment words `b^{x_0} a b^{x_1} ⋯ a b^{x_m}` -/

/-- The segment word `b^{x 0} a b^{x 1} ⋯ a b^{x m}`. -/
def segWord : ℕ → (ℕ → ℕ) → Word
  | 0, x => List.replicate (x 0) true
  | m + 1, x => List.replicate (x 0) true ++ false :: segWord m (fun k => x (k + 1))

/-- Right part of a split at block `i`, position `j`. -/
def zf (i j : ℕ) (x : ℕ → ℕ) : ℕ → ℕ := fun k => if k = 0 then x i - j else x (k + i)

lemma segWord_congr : ∀ (m : ℕ) (x y : ℕ → ℕ), (∀ k ≤ m, x k = y k) → segWord m x = segWord m y
  | 0, x, y, h => by simp [segWord, h 0 le_rfl]
  | m + 1, x, y, h => by
    simp only [segWord, h 0 (Nat.zero_le _)]
    rw [segWord_congr m _ _ (fun k hk => h (k + 1) (by omega))]

/-- Sum over all ways to split `w`. -/
noncomputable def splitSum (F : Word → Word → ℕ∞) (w : Word) : ℕ∞ :=
  ∑ k ∈ range (w.length + 1), F (w.take k) (w.drop k)

lemma splitSum_cons (F : Word → Word → ℕ∞) (c : Bool) (w : Word) :
    splitSum F (c :: w) = F [] (c :: w) + splitSum (fun u v => F (c :: u) v) w := by
  unfold splitSum
  rw [List.length_cons, Finset.sum_range_succ', add_comm]
  simp

lemma splitSum_rep (F : Word → Word → ℕ∞) (n : ℕ) (w : Word) :
    splitSum F (List.replicate n true ++ w) =
      ∑ k ∈ range n, F (List.replicate k true) (List.replicate (n - k) true ++ w) +
      splitSum (fun u v => F (List.replicate n true ++ u) v) w := by
  induction n generalizing F with
  | zero => simp
  | succ n ih =>
    rw [List.replicate_succ, List.cons_append, splitSum_cons, ih, Finset.sum_range_succ']
    simp only [List.replicate_succ, List.cons_append, List.replicate_zero, Nat.sub_zero,
      Nat.succ_sub_succ]
    simp only [← List.replicate_succ]
    ring_nf

lemma splitSum_segWord (F : Word → Word → ℕ∞) : ∀ (m : ℕ) (x : ℕ → ℕ),
    splitSum F (segWord m x) = ∑ i ∈ range (m + 1), ∑ j ∈ range (x i + 1),
      F (segWord i (Function.update x i j)) (segWord (m - i) (zf i j x))
  | 0, x => by
    have h := splitSum_rep F (x 0) []
    simp only [List.append_nil] at h
    simp only [segWord, zero_add, Finset.range_one, Finset.sum_singleton, Function.update_self,
      zf, ite_true, Nat.sub_zero]
    rw [h, Finset.sum_range_succ]
    simp [splitSum]
  | m + 1, x => by
    conv_rhs => rw [Finset.sum_range_succ', add_comm]
    simp only [segWord]
    rw [splitSum_rep, splitSum_cons, splitSum_segWord _ m]
    rw [← add_assoc]
    congr 1
    · simp only [Function.update_self, Nat.sub_zero, zf, ite_true]
      trace_state
      rw [Finset.sum_range_succ]
      congr 1
      · refine Finset.sum_congr rfl fun k hk => ?_
        congr 2
        have : ∀ k', (if k' + 1 = 0 then x 0 - k else x (k' + 1 + 0)) = x (k' + 1) := by
          intro k'; simp
        simp [this]
      · simp
    · refine Finset.sum_congr rfl fun i _ => Finset.sum_congr rfl fun j _ => ?_
      have h1 : Function.update x (i + 1) j 0 = x 0 := by simp
      have h2 : (fun k => Function.update x (i + 1) j (k + 1)) = Function.update (fun k => x (k + 1)) i j := by
        funext k
        by_cases hk : k = i
        · subst hk; simp
        · simp [Function.update_of_ne hk, Function.update_of_ne (show k + 1 ≠ i + 1 by omega)]
      have h3 : zf (i + 1) j x = zf i j (fun k => x (k + 1)) := by
        funext k; simp only [zf]; split_ifs <;> simp [Nat.add_assoc, Nat.add_comm 1]
      rw [h1, h2, h3, show m + 1 - (i + 1) = m - i by omega]

/-- Tree count on segment words. -/
noncomputable def G (X : C.N) (m : ℕ) (x : ℕ → ℕ) : ℕ∞ := T C X (segWord m x)

/-- Convolution at block `i`. -/
noncomputable def conv (i : ℕ) (f g : (ℕ → ℕ) → ℕ∞) (x : ℕ → ℕ) : ℕ∞ :=
  ∑ j ∈ range (x i + 1), f (Function.update x i j) * g (zf i j x)

lemma length_segWord : ∀ (m : ℕ) (x : ℕ → ℕ),
    (segWord m x).length + 1 = ∑ i ∈ range (m + 1), (x i + 1)
  | 0, x => by simp [segWord]
  | m + 1, x => by
    rw [Finset.sum_range_succ']
    simp only [segWord, List.length_append, List.length_replicate, List.length_cons]
    have := length_segWord m (fun k => x (k + 1))
    omega

lemma G_eq (X : C.N) (m : ℕ) (x : ℕ → ℕ) :
    G C X m x = leafT C X (segWord m x) + ∑ r ∈ binOf C X, ∑ i ∈ range (m + 1),
      conv i (G C r.2.1 i) (G C r.2.2 (m - i)) x := by
  unfold G
  rw [T_eq]
  congr 1
  refine Finset.sum_congr rfl fun r _ => ?_
  have := splitSum_segWord (fun u v => T C r.2.1 u * T C r.2.2 v) m x
  simp only [splitSum] at this
  rw [this]
  rfl

lemma G_congr (X : C.N) (m : ℕ) (x y : ℕ → ℕ) (h : ∀ k ≤ m, x k = y k) :
    G C X m x = G C X m y := by
  unfold G; rw [segWord_congr m x y h]

lemma G_zero_level (X : C.N) (x : ℕ → ℕ) (h : x 0 = 0) : G C X 0 x = 0 := by
  simp [G, segWord, h, T_nil]

end S2
end FA
