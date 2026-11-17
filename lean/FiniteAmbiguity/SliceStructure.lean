/-
# From block words to slice words.  OWNER: agent S3.
Slice words are block words with two forced zero blocks; restrict the linear sets accordingly.
-/
import FiniteAmbiguity.CNFStructure

namespace FA

namespace SliceRestrict
open Classical

variable {n m : ℕ} (ι : Fin m → Fin n)

/-- A period is usable iff it vanishes off the range of `ι`. -/
def Good (L : LamLinSet n) (j : Fin L.r) : Prop := ∀ i, i ∉ Set.range ι → L.v j i = 0

/-- Enumeration of the good periods. -/
noncomputable def σ (L : LamLinSet n) : Fin (Fintype.card {j // Good ι L j}) → Fin L.r :=
  fun j' => ((Fintype.equivFin {j // Good ι L j}).symm j').val

lemma σ_good (L : LamLinSet n) (j') : Good ι L (σ ι L j') :=
  ((Fintype.equivFin {j // Good ι L j}).symm j').2

lemma sum_reindex (L : LamLinSet n) {X : Type*} [AddCommMonoid X] (f : Fin L.r → X)
    (hf : ∀ j, ¬ Good ι L j → f j = 0) : ∑ j, f j = ∑ j', f (σ ι L j') := by
  rw [← Finset.sum_filter_of_ne (p := Good ι L) (fun j _ h => by_contra fun hg => h (hf j hg))]
  rw [Finset.sum_subtype (Finset.filter (Good ι L) Finset.univ) (p := Good ι L) (by simp)]
  exact (Equiv.sum_comp (Fintype.equivFin {j // Good ι L j}).symm (fun x => f x.val)).symm

/-- Extension by zero of a coefficient vector on the good periods. -/
noncomputable def ext (L : LamLinSet n) (q : Fin (Fintype.card {j // Good ι L j}) → ℕ) :
    Fin L.r → ℕ :=
  fun j => if h : Good ι L j then q (Fintype.equivFin {j // Good ι L j} ⟨j, h⟩) else 0

lemma ext_σ (L : LamLinSet n) (q) (j') : ext ι L q (σ ι L j') = q j' := by
  simp only [ext]; rw [dite_eq_left_of_eq_true (eq_true (σ_good ι L j'))]; simp [σ]

lemma ext_bad (L : LamLinSet n) (q) (j) (h : ¬ Good ι L j) : ext ι L q j = 0 := by
  simp [ext, h]

/-- Preimage under `ι` with default. -/
noncomputable def pre (x : Fin n) (d : Fin m) : Fin m :=
  if h : ∃ k, ι k = x then h.choose else d

lemma pre_pos {x : Fin n} (d : Fin m) (h : ∃ k, ι k = x) : pre ι x d = h.choose := by simp only [pre]; rw [dite_eq_left_of_eq_true (eq_true h)]
lemma pre_neg {x : Fin n} (d : Fin m) (h : ¬ ∃ k, ι k = x) : pre ι x d = d := by simp only [pre]; rw [dite_eq_right_of_eq_false (eq_false h)]

variable {ι}

lemma coord_eq (L : LamLinSet n) (q : Fin L.r → ℕ) (i : Fin n) :
    (L.c + ∑ j, q j • L.v j) i = L.c i + ∑ j, q j * L.v j i := by
  simp [Finset.sum_apply]

variable (ι) in
lemma exists_ne (L : LamLinSet n) (j' : Fin (Fintype.card {j // Good ι L j})) :
    ∃ k, L.v (σ ι L j') (ι k) ≠ 0 := by
  have h := L.nonzero (σ ι L j')
  obtain ⟨i, hi⟩ : ∃ i, L.v (σ ι L j') i ≠ 0 := by
    by_contra h'; push Not at h'; exact h (funext h')
  by_cases hr : i ∈ Set.range ι
  · obtain ⟨k, rfl⟩ := hr; exact ⟨k, hi⟩
  · exact absurd (σ_good ι L j' i hr) hi

variable (ι) in
noncomputable def pick (L : LamLinSet n) (j' : Fin (Fintype.card {j // Good ι L j})) : Fin m :=
  (exists_ne ι L j').choose

variable (ι) in
noncomputable def pair' (L : LamLinSet n) (j' : Fin (Fintype.card {j // Good ι L j})) :
    Fin m × Fin m :=
  let s := (L.pair (σ ι L j')).1
  let t := (L.pair (σ ι L j')).2
  (pre ι s (pre ι t (pick ι L j')), pre ι t (pre ι s (pick ι L j')))

variable (ι) in
lemma pair'_cases (L : LamLinSet n) (j') :
    (pair' ι L j').1 = (pair' ι L j').2 ∨
      (ι (pair' ι L j').1 = (L.pair (σ ι L j')).1 ∧
        ι (pair' ι L j').2 = (L.pair (σ ι L j')).2) := by
  simp only [pair']
  by_cases hs : ∃ k, ι k = (L.pair (σ ι L j')).1 <;>
    by_cases ht : ∃ k, ι k = (L.pair (σ ι L j')).2
  · right; rw [pre_pos ι _ hs, pre_pos ι _ ht]; exact ⟨hs.choose_spec, ht.choose_spec⟩
  · left; rw [pre_pos ι _ hs, pre_neg ι _ ht, pre_pos ι _ hs]
  · left; rw [pre_neg ι _ hs, pre_pos ι _ ht, pre_pos ι _ ht]
  · left; rw [pre_neg ι _ hs, pre_neg ι _ ht, pre_neg ι _ hs, pre_neg ι _ ht]

variable (hι : StrictMono ι)
include hι

/-- The restriction of `L` along `ι`, assuming the base point vanishes off the range. -/
noncomputable def restr (L : LamLinSet n) : LamLinSet m where
  c := fun k => L.c (ι k)
  r := Fintype.card {j // Good ι L j}
  v := fun j' k => L.v (σ ι L j') (ι k)
  pair := pair' ι L
  le := by
    intro j
    rcases pair'_cases ι L j with h | ⟨h1, h2⟩
    · exact h.le
    · rw [← hι.le_iff_le, h1, h2]; exact L.le _
  supp := by
    intro j k hk
    rcases L.supp _ _ hk with h | h
    · left
      simp only [pair']
      have hs : ∃ k', ι k' = (L.pair (σ ι L j)).1 := ⟨k, h⟩
      rw [pre_pos ι _ hs]; exact hι.injective (h.trans hs.choose_spec.symm)
    · right
      simp only [pair']
      have ht : ∃ k', ι k' = (L.pair (σ ι L j)).2 := ⟨k, h⟩
      rw [pre_pos ι _ ht]; exact hι.injective (h.trans ht.choose_spec.symm)
  nonzero := by
    intro j h
    obtain ⟨k, hk⟩ := exists_ne ι L j
    exact hk (congrFun h k)
  inj := by
    intro q₁ q₂ hq
    have key : ∀ q, ∑ j, ext ι L q j • L.v j = ∑ j', q j' • L.v (σ ι L j') := by
      intro q
      rw [sum_reindex ι L _ (fun j hj => by simp [ext_bad ι L q j hj])]
      simp [ext_σ]
    have : ∑ j, ext ι L q₁ j • L.v j = ∑ j, ext ι L q₂ j • L.v j := by
      rw [key, key]
      funext i
      by_cases hr : i ∈ Set.range ι
      · obtain ⟨k, rfl⟩ := hr
        have := congrFun hq k
        simpa [Finset.sum_apply] using this
      · simp [Finset.sum_apply, σ_good ι L _ i hr]
    have h := L.inj this
    funext j'
    have := congrFun h (σ ι L j')
    simpa [ext_σ] using this
  laminar := by
    intro j j' ⟨h1, h2, h3⟩
    rcases pair'_cases ι L j with e | ⟨a1, b1⟩
    · exact absurd (h1.trans h2) (by rw [e]; exact lt_irrefl _)
    rcases pair'_cases ι L j' with e' | ⟨a2, b2⟩
    · exact absurd (h2.trans h3) (by rw [e']; exact lt_irrefl _)
    apply L.laminar (σ ι L j) (σ ι L j')
    rw [← a1, ← b1, ← a2, ← b2]
    exact ⟨hι h1, hι h2, hι h3⟩

lemma restr_coord (L : LamLinSet n) (q : Fin (restr hι L).r → ℕ) (k : Fin m) :
    ((restr hι L).c + ∑ j, q j • (restr hι L).v j) k =
      L.c (ι k) + ∑ j', q j' * L.v (σ ι L j') (ι k) := by
  simp only [Pi.add_apply, Finset.sum_apply, Pi.smul_apply, smul_eq_mul]; rfl

/-- The restriction as an optional linear set. -/
noncomputable def restrict (L : LamLinSet n) : Option (LamLinSet m) :=
  if ∀ i, i ∉ Set.range ι → L.c i = 0 then some (restr hι L) else none

lemma restrict_spec (L : LamLinSet n) (e : Fin n → ℕ) (he : ∀ i, i ∉ Set.range ι → e i = 0) :
    (((restrict hι L).map fun L' => decide (L'.Mem (fun k => e (ι k)))).getD false) =
      decide (L.Mem e) := by
  unfold restrict
  split_ifs with hc
  · simp only [Option.map_some, Option.getD_some, decide_eq_decide]
    constructor
    · rintro ⟨q, hq⟩
      refine ⟨ext ι L q, ?_⟩
      funext i
      rw [coord_eq]
      by_cases hr : i ∈ Set.range ι
      · obtain ⟨k, rfl⟩ := hr
        have := congrFun hq k
        rw [this, restr_coord]
        congr 1
        rw [sum_reindex ι L (fun j => ext ι L q j * L.v j (ι k))
          (fun j hj => by simp [ext_bad ι L q j hj])]
        exact Finset.sum_congr rfl fun j _ => congrArg (· * L.v (σ ι L j) (ι k)) (ext_σ ι L q j).symm
      · rw [he i hr, hc i hr]
        symm
        simp only [zero_add]
        exact Finset.sum_eq_zero fun j _ => by
          by_cases hg : Good ι L j
          · simp [hg i hr]
          · simp [ext_bad ι L q j hg]
    · rintro ⟨q, hq⟩
      -- bad periods have zero coefficient
      have hbad : ∀ j, ¬ Good ι L j → q j = 0 := by
        intro j hj
        simp only [Good, not_forall] at hj
        obtain ⟨i, hr, hv⟩ := hj
        have h0 := congrFun hq i
        rw [coord_eq, he i hr] at h0
        have hle : q j * L.v j i ≤ ∑ j, q j * L.v j i :=
          Finset.single_le_sum (f := fun j => q j * L.v j i) (fun _ _ => Nat.zero_le _)
            (Finset.mem_univ j)
        rcases Nat.eq_zero_of_le_zero (by omega : q j * L.v j i ≤ 0) |> Nat.mul_eq_zero.mp
          with h | h
        · exact h
        · exact absurd h hv
      refine ⟨fun j' => q (σ ι L j'), ?_⟩
      funext k
      have := congrFun hq (ι k)
      rw [coord_eq] at this
      rw [this, restr_coord]
      congr 1
      exact sum_reindex ι L (fun j => q j * L.v j (ι k)) (fun j hj => by simp [hbad j hj])
  · simp only [Option.map_none, Option.getD_none, Bool.false_eq, decide_eq_false_iff_not]
    rintro ⟨q, hq⟩
    push Not at hc
    obtain ⟨i, hr, hci⟩ := hc
    have := congrFun hq i
    rw [coord_eq, he i hr] at this
    omega

lemma ply_restrict (Ls : List (LamLinSet n)) (e : Fin n → ℕ)
    (he : ∀ i, i ∉ Set.range ι → e i = 0) :
    ply (Ls.filterMap (restrict hι)) (fun k => e (ι k)) = ply Ls e := by
  unfold ply
  rw [List.countP_filterMap]
  exact List.countP_congr fun L _ => by rw [restrict_spec hι L e he]

end SliceRestrict

namespace SliceEmbed

variable (M : ℕ)

@[simp] lemma append_addNat {α : Type*} {m : ℕ} (u v : Fin m → α) (i : Fin m) :
    Fin.append u v (i.addNat m) = v i := by
  rw [← Fin.natAdd_eq_addNat]; exact Fin.append_right u v i

/-- The non-marker coordinates of a block vector of length `2M+2`. -/
def ι : Fin (M + M) → Fin ((M + 1) + (M + 1)) :=
  Fin.append (fun i : Fin M => Fin.castAdd (M + 1) i.succ) (fun i : Fin M => Fin.natAdd (M + 1) i.succ)

/-- `(0, x, 0, y)`. -/
def embed (p : Fin (M + M) → ℕ) : Fin ((M + 1) + (M + 1)) → ℕ :=
  Fin.append (Fin.cons 0 fun i => p (Fin.castAdd M i)) (Fin.cons 0 fun i => p (Fin.natAdd M i))

lemma ι_val (k : Fin (M + M)) : (ι M k).val = if k.val < M then k.val + 1 else k.val + 2 := by
  refine Fin.addCases (fun i => ?_) (fun i => ?_) k
  · simp [ι]
  · simp [ι]; omega

lemma ι_strictMono : StrictMono (ι M) := by
  intro a b h
  rw [Fin.lt_def, ι_val, ι_val]
  rw [Fin.lt_def] at h
  split_ifs <;> omega

lemma embed_ι (p : Fin (M + M) → ℕ) : (fun k => embed M p (ι M k)) = p := by
  funext k
  refine Fin.addCases (fun i => ?_) (fun i => ?_) k <;> simp [ι, embed]

lemma embed_off (p : Fin (M + M) → ℕ) (i : Fin ((M + 1) + (M + 1)))
    (hi : i ∉ Set.range (ι M)) : embed M p i = 0 := by
  revert hi
  refine Fin.addCases (fun i => ?_) (fun i => ?_) i
  · refine Fin.cases (fun _ => by simp [embed]) (fun j hj => ?_) i
    exact absurd ⟨Fin.castAdd M j, by simp [ι]⟩ hj
  · refine Fin.cases (fun _ => by simp [embed]) (fun j hj => ?_) i
    exact absurd ⟨Fin.natAdd M j, by simp [ι]⟩ hj

lemma sliceWord_eq (p : Fin (M + M) → ℕ) : sliceWord p = blockWord (embed M p) := by
  unfold sliceWord blockWord half embed
  rw [List.ofFn_add]
  simp [List.ofFn_succ, ab, Fin.append_left']

end SliceEmbed

/-- The structure lemma on slice words. -/
theorem cnf_structure (C : CNF) (k : ℕ) (hk : ∀ w, C.amb w ≤ k) (M : ℕ) :
    ∃ Ls : List (LamLinSet (M + M)),
      ∀ p : Fin (M + M) → ℕ, C.amb (sliceWord p) = (ply Ls p : ℕ∞) := by
  obtain ⟨Ls₀, h₀⟩ := cnf_structure_blocks C k hk ((M + 1) + (M + 1))
  refine ⟨Ls₀.filterMap (SliceRestrict.restrict (SliceEmbed.ι_strictMono M)), fun p => ?_⟩
  rw [SliceEmbed.sliceWord_eq, h₀, ← SliceRestrict.ply_restrict (SliceEmbed.ι_strictMono M) Ls₀
    (SliceEmbed.embed M p) (SliceEmbed.embed_off M p), SliceEmbed.embed_ι]

end FA
