/-
# Lemma 1: on the slice `R_m`, a word is primitive iff its two halves differ.
-/
import FiniteAmbiguity.Defs

namespace FA

/-- Concatenation of blocks `a b^{n}` for a list of exponents. -/
def F (L : List ℕ) : Word := (L.map ab).flatten

@[simp] lemma F_nil : F [] = [] := rfl
@[simp] lemma F_cons (n : ℕ) (L : List ℕ) : F (n :: L) = false :: (List.replicate n true ++ F L) := by
  simp [F, ab]
lemma F_append (L₁ L₂ : List ℕ) : F (L₁ ++ L₂) = F L₁ ++ F L₂ := by simp [F]

/-- `F L` is empty or starts with `a`. -/
def StartsA (s : Word) : Prop := s = [] ∨ s.head? = some false

lemma startsA_F (L : List ℕ) : StartsA (F L) := by
  cases L with
  | nil => left; rfl
  | cons n L => right; simp

lemma rep_cancel : ∀ (n m : ℕ) (s s' : Word), StartsA s → StartsA s' →
    List.replicate n true ++ s = List.replicate m true ++ s' → n = m ∧ s = s'
  | 0, 0, s, s', _, _, h => ⟨rfl, by simpa using h⟩
  | n + 1, 0, s, s', _, hs', h => by
      exfalso
      simp only [List.replicate_succ, List.cons_append, List.replicate_zero, List.nil_append] at h
      subst h
      rcases hs' with h | h <;> simp at h
  | 0, m + 1, s, s', hs, _, h => by
      exfalso
      simp only [List.replicate_succ, List.cons_append, List.replicate_zero, List.nil_append] at h
      subst h
      rcases hs with h | h <;> simp at h
  | n + 1, m + 1, s, s', hs, hs', h => by
      simp [List.replicate_succ] at h
      obtain ⟨h1, h2⟩ := rep_cancel n m s s' hs hs' h
      exact ⟨by omega, h2⟩

lemma F_injective : ∀ L₁ L₂ : List ℕ, F L₁ = F L₂ → L₁ = L₂
  | [], [], _ => rfl
  | [], _ :: _, h => by simp at h
  | _ :: _, [], h => by simp at h
  | n :: L₁, m :: L₂, h => by
      simp only [F_cons, List.cons.injEq, true_and] at h
      obtain ⟨rfl, h2⟩ := rep_cancel n m _ _ (startsA_F _) (startsA_F _) h
      rw [F_injective L₁ L₂ h2]

/-- A cut of `F L` just before an `a` (or at the end) is a cut between blocks. -/
lemma F_split : ∀ (L : List ℕ) (u v : Word), F L = u ++ v → StartsA v →
    ∃ L₁ L₂, L = L₁ ++ L₂ ∧ u = F L₁ ∧ v = F L₂
  | [], u, v, h, _ => by
      have : u = [] ∧ v = [] := by simpa [eq_comm] using h
      exact ⟨[], [], by simp, by simp [this.1], by simp [this.2]⟩
  | n :: L, u, v, h, hv => by
      rcases u with _ | ⟨c, u'⟩
      · exact ⟨[], n :: L, by simp, by simp, by simpa using h.symm⟩
      · simp only [F_cons, List.cons_append, List.cons.injEq] at h
        obtain ⟨rfl, h⟩ := h
        -- `replicate n true ++ F L = u' ++ v`
        have hlen : n ≤ u'.length := by
          by_contra hlt
          push Not at hlt
          -- then `v` begins inside the run of `b`s
          have hv' : v ≠ [] := by
            intro hv0; subst hv0
            have := congrArg List.length h
            simp at this; omega
          rcases hv with hv | hv
          · exact hv' hv
          · have key : (List.replicate n true ++ F L)[u'.length]? = some false := by
              rw [h, List.getElem?_append_right (le_refl _)]
              simpa [List.head?_eq_getElem?] using hv
            rw [List.getElem?_append_left (by simpa using hlt)] at key
            simp [hlt] at key
        obtain ⟨u'', rfl⟩ : ∃ u'', u' = List.replicate n true ++ u'' := by
          refine ⟨u'.drop n, ?_⟩
          have h1 := congrArg (List.take n) h
          rw [List.take_append_of_le_length (by simp)] at h1
          rw [List.take_append_of_le_length hlen] at h1
          simp only [List.take_replicate, min_self] at h1
          rw [h1, List.take_append_drop]
        rw [List.append_assoc] at h
        have h' := List.append_cancel_left h
        obtain ⟨L₁, L₂, rfl, rfl, rfl⟩ := F_split L u'' v h' hv
        exact ⟨n :: L₁, L₂, by simp, by simp, rfl⟩

lemma pow_succ' (u : Word) (k : ℕ) : pow u (k + 1) = u ++ pow u k := by
  simp [pow, List.replicate_succ]

lemma F_pow (L : List ℕ) (k : ℕ) : F (List.replicate k L).flatten = pow (F L) k := by
  induction k with
  | zero => simp [pow, F]
  | succ k ih => rw [List.replicate_succ, List.flatten_cons, F_append, ih, pow_succ']

lemma count_flatten_replicate (L : List ℕ) (k : ℕ) :
    ((List.replicate k L).flatten).count 0 = k * L.count 0 := by
  induction k with
  | zero => simp
  | succ k ih => rw [List.replicate_succ, List.flatten_cons, List.count_append, ih, Nat.add_mul, Nat.one_mul, Nat.add_comm]

/-- The exponent list of a slice word. -/
def expList {M : ℕ} (p : Fin (M + M) → ℕ) : List ℕ :=
  (0 :: List.ofFn fun i => p (Fin.castAdd M i)) ++ (0 :: List.ofFn fun i => p (Fin.natAdd M i))

lemma half_eq {M : ℕ} (x : Fin M → ℕ) : half x = F (0 :: List.ofFn x) := by
  simp [half, F, ab, List.map_ofFn]
  rfl

lemma sliceWord_eq {M : ℕ} (p : Fin (M + M) → ℕ) : sliceWord p = F (expList p) := by
  rw [sliceWord, expList, F_append, half_eq, half_eq]

lemma count_zero_ofFn {M : ℕ} (x : Fin M → ℕ) (hx : ∀ i, 1 ≤ x i) :
    (List.ofFn x).count 0 = 0 := by
  rw [List.count_eq_zero]
  intro hmem
  obtain ⟨i, hi⟩ := List.mem_ofFn.mp hmem
  have := hx i; omega

/-- **Lemma 1.** For positive block vectors, the slice word is primitive iff `x ≠ y`. -/
theorem slice_primitive_iff {M : ℕ} (p : Fin (M + M) → ℕ) (hp : ∀ i, 1 ≤ p i) :
    IsPrimitive (sliceWord p) ↔
      (fun i => p (Fin.castAdd M i)) ≠ (fun i => p (Fin.natAdd M i)) := by
  set x := fun i => p (Fin.castAdd M i)
  set y := fun i => p (Fin.natAdd M i)
  have hx : ∀ i, 1 ≤ x i := fun i => hp _
  have hy : ∀ i, 1 ≤ y i := fun i => hp _
  constructor
  · rintro ⟨-, hprim⟩ hxy
    have : sliceWord p = pow (half x) 2 := by
      change half x ++ half y = _
      rw [← hxy]; simp [pow]
    exact absurd (hprim _ _ this) (by omega)
  · intro hxy
    refine ⟨by simp [sliceWord, half], ?_⟩
    intro u k hw
    rw [sliceWord_eq] at hw
    by_contra hk1
    -- k ≠ 0 since the word is non-empty
    have hk0 : k ≠ 0 := by
      rintro rfl; simp [pow, expList, F, ab] at hw
    obtain ⟨k, rfl⟩ : ∃ k', k = k' + 2 := ⟨k - 2, by omega⟩
    -- the second copy of `u` starts with `a`, so `u` is a union of blocks
    have hu0 : u ≠ [] := by
      rintro rfl; simp [pow, expList, F, ab] at hw
    have hstart : StartsA (pow u (k + 1)) := by
      right
      have h1 : (F (expList p)).head? = some false := by simp [expList]
      rw [hw, pow_succ'] at h1
      rw [pow_succ']
      rcases u with _ | ⟨c, u⟩
      · exact absurd rfl hu0
      · simpa using h1
    rw [pow_succ'] at hw
    obtain ⟨L₁, L₂, hL, hu, -⟩ := F_split _ u _ hw hstart
    have hLeq : expList p = (List.replicate (k + 2) L₁).flatten := by
      apply F_injective
      rw [F_pow, ← hu, pow_succ']; exact hw
    -- count the zeros
    have hc := congrArg (List.count 0) hLeq
    rw [count_flatten_replicate] at hc
    have h2 : (expList p).count 0 = 2 := by
      rw [expList, List.count_append, List.count_cons, List.count_cons,
        count_zero_ofFn (fun i => p (Fin.castAdd M i)) hx,
        count_zero_ofFn (fun i => p (Fin.natAdd M i)) hy]
      rfl
    have hL1 : 1 ≤ L₁.count 0 := by
      -- `L₁` is a non-empty prefix of `expList p`, whose head is `0`
      have hne : L₁ ≠ [] := by
        rintro rfl; simp at hu; exact hu0 hu
      obtain ⟨a, L₁', rfl⟩ := List.exists_cons_of_ne_nil hne
      have : a = 0 := by
        have := congrArg List.head? hLeq
        simpa [expList, List.replicate_succ] using this.symm
      subst this; simp [List.count_cons]
    have hk : k = 0 := by
      rw [h2] at hc
      have : (k + 2) * L₁.count 0 ≥ (k + 2) * 1 := Nat.mul_le_mul_left _ hL1
      omega
    subst hk
    -- now `expList p = L₁ ++ L₁`, and both halves have length `M + 1`
    have hLL : expList p = L₁ ++ L₁ := by simpa [List.replicate_succ] using hLeq
    have hlen : L₁.length = M + 1 := by
      have := congrArg List.length hLL
      simp [expList] at this; omega
    rw [expList] at hLL
    have := List.append_inj hLL (by simp [hlen])
    have h3 := this.1.trans this.2.symm
    exact hxy (List.ofFn_injective (List.cons.inj h3).2)

end FA
