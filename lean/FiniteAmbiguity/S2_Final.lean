/-
# S2: from bounded representable functions to laminar simple linear sets on block words
-/
import FiniteAmbiguity.S2_Cyclic

namespace FA
namespace S2

open Finset

lemma list_le_sum {α : Type*} (L : List α) (f : α → ℕ∞) {a : α} (ha : a ∈ L) :
    f a ≤ (L.map f).sum := by
  induction L with
  | nil => simp at ha
  | cons b L ih =>
    simp only [List.map_cons, List.sum_cons]
    rcases List.mem_cons.mp ha with rfl | h
    · exact le_self_add
    · exact le_trans (ih h) le_add_self

/-- Bounded multiplicity forces an injective parametrisation. -/
lemma inj_of_bdd (S : Sys) (n k : ℕ) (h : ∀ x, cnt n S x ≤ k) (q q' : S.ι → ℕ)
    (hqq : ∀ l ≤ n, S.val q l = S.val q' l) : q = q' := by
  classical
  by_contra hne
  obtain ⟨i0, hi0⟩ : ∃ i, q i ≠ q' i := by
    by_contra h'; push_neg at h'; exact hne (funext h')
  set K := k + 1
  let Q : ℕ → S.ι → ℕ := fun j i => j * q i + (K - j) * q' i
  let x : ℕ → ℕ := fun l => S.c l + K * ∑ i, q i * S.v i l
  have hsum : ∀ l ≤ n, ∑ i, q i * S.v i l = ∑ i, q' i * S.v i l := by
    intro l hl; have := hqq l hl; simp only [Sys.val] at this; omega
  have hmem : ∀ j ≤ K, Q j ∈ S.fib n x := by
    intro j hj l hl
    simp only [Sys.val, Q, x]
    congr 1
    simp only [add_mul, Finset.sum_add_distrib, mul_assoc, ← Finset.mul_sum]
    rw [← hsum l hl, ← add_mul]
    congr 1; omega
  have hinj : Set.InjOn Q (Set.Iic K) := by
    intro j hj j' hj' he
    simp only [Set.mem_Iic] at hj hj'
    have := congrFun he i0
    simp only [Q] at this
    have h2 : ((j : ℤ) - j') * ((q i0 : ℤ) - q' i0) = 0 := by
      have := congrArg (fun t : ℕ => (t : ℤ)) this
      push_cast [Nat.cast_sub hj, Nat.cast_sub hj'] at this
      linarith
    rcases mul_eq_zero.mp h2 with h3 | h3
    · omega
    · exact absurd (by omega) hi0
  have hcard : ((K + 1 : ℕ) : ℕ∞) ≤ cnt n S x := by
    unfold cnt
    calc ((K + 1 : ℕ) : ℕ∞) = (Set.Iic K).encard := by
          rw [Set.encard_eq_coe_toFinset_card]; simp
      _ = (Q '' Set.Iic K).encard := (hinj.encard_image).symm
      _ ≤ (S.fib n x).encard := by
          apply Set.encard_le_encard
          rintro _ ⟨j, hj, rfl⟩
          exact hmem j hj
  have := hcard.trans (h x)
  norm_cast at this
  omega

lemma nonzero_of_inj (S : Sys) (n : ℕ)
    (hinj : ∀ q q' : S.ι → ℕ, (∀ l ≤ n, S.val q l = S.val q' l) → q = q') (j : S.ι) :
    ∃ l ≤ n, S.v j l ≠ 0 := by
  classical
  by_contra h
  push_neg at h
  have := hinj 0 (Pi.single j 1) (fun l hl => by
    simp only [Sys.val, Pi.zero_apply, zero_mul, Finset.sum_const_zero, add_zero]
    rw [Finset.sum_eq_single j]
    · simp [h l hl]
    · intro b _ hb; simp [hb]
    · simp)
  have := congrFun this j
  simp at this

/-- The block vector of `e`: coordinate `0` is the empty leading block. -/
def xe {n : ℕ} (e : Fin n → ℕ) : ℕ → ℕ :=
  fun l => if h : 0 < l ∧ l ≤ n then e ⟨l - 1, by omega⟩ else 0

lemma sum_lift {ι : Type} [Fintype ι] (p : ι → Prop) [DecidablePred p] {r : ℕ}
    (σ : {j // p j} ≃ Fin r) (q : Fin r → ℕ) (w : ι → ℕ) :
    ∑ j, (if h : p j then q (σ ⟨j, h⟩) else 0) * w j = ∑ t, q t * w (σ.symm t).1 := by
  rw [← Fintype.sum_subtype_add_sum_subtype p]
  have h2 : ∑ i : {x // ¬ p x}, (if h : p i.1 then q (σ ⟨i.1, h⟩) else 0) * w i.1 = 0 := by
    apply Finset.sum_eq_zero; intro i _; simp [i.2]
  rw [h2, add_zero]
  have h1 : ∀ i : {x // p x}, (if h : p i.1 then q (σ ⟨i.1, h⟩) else 0) * w i.1 =
      q (σ i) * w i.1 := by
    intro i; simp [i.2]
  simp only [h1]
  exact Fintype.sum_equiv σ _ _ (fun i => by simp)

section toLam

/-- Injectivity of the parametrisation on coordinates `≤ n`. -/
def InjOn' (S : Sys) (n : ℕ) : Prop :=
  ∀ q q' : S.ι → ℕ, (∀ l ≤ n, S.val q l = S.val q' l) → q = q'

/-- Periods not touching coordinate 0. -/
def Jp (S : Sys) (j : S.ι) : Prop := S.v j 0 = 0

lemma pair_snd_pos {S : Sys} {n : ℕ} (hinj : InjOn' S n) (j : S.ι) (hj : S.v j 0 = 0) :
    1 ≤ (S.pair j).2 := by
  obtain ⟨l, hl, hv⟩ := nonzero_of_inj S n hinj j
  rcases S.supp j l hv with h | h
  · have := S.le j
    by_contra h0
    have : l = 0 := by omega
    subst this; exact hv hj
  · by_contra h0
    have : l = 0 := by omega
    subst this; exact hv hj

/-- The new pair of coordinates (in `Fin n`). -/
def newPair {S : Sys} {n : ℕ} (hW : S.Within n) (hinj : InjOn' S n) (j : S.ι)
    (hj : S.v j 0 = 0) : Fin n × Fin n :=
  if h : (S.pair j).1 = 0 then
    (⟨(S.pair j).2 - 1, by have := hW j; have := pair_snd_pos hinj j hj; omega⟩,
     ⟨(S.pair j).2 - 1, by have := hW j; have := pair_snd_pos hinj j hj; omega⟩)
  else
    (⟨(S.pair j).1 - 1, by have := hW j; have := S.le j; omega⟩,
     ⟨(S.pair j).2 - 1, by have := hW j; have := pair_snd_pos hinj j hj; omega⟩)

open Classical in
/-- The laminar simple linear set on `Fin n` obtained by restricting to coordinate `0 = 0`. -/
noncomputable def toLam (S : Sys) {n : ℕ} (hW : S.Within n) (hinj : InjOn' S n) : LamLinSet n where
  c := fun i => S.c (i.1 + 1)
  r := Fintype.card {j // Jp S j}
  v := fun t i => S.v ((Fintype.equivFin {j // Jp S j}).symm t).1 (i.1 + 1)
  pair := fun t => newPair hW hinj _ ((Fintype.equivFin {j // Jp S j}).symm t).2
  le := by
    intro t
    simp only [newPair]
    split_ifs
    · exact le_rfl
    · simp only [Fin.mk_le_mk]; have := S.le ((Fintype.equivFin {j // Jp S j}).symm t).1; omega
  supp := by
    intro t i hv
    generalize (Fintype.equivFin {j // Jp S j}).symm t = J at hv ⊢
    have := S.supp J.1 _ hv
    simp only [newPair]
    split_ifs with h0
    · right; ext; simp only; omega
    · rcases this with h | h
      · left; ext; simp only; omega
      · right; ext; simp only; omega
  nonzero := by
    intro t h
    set j := ((Fintype.equivFin {j // Jp S j}).symm t).1 with hj
    have hj0 : S.v j 0 = 0 := ((Fintype.equivFin {j // Jp S j}).symm t).2
    obtain ⟨l, hl, hv⟩ := nonzero_of_inj S n hinj j
    have hl0 : l ≠ 0 := fun h' => hv (h' ▸ hj0)
    have := congrFun h ⟨l - 1, by omega⟩
    simp only [Pi.zero_apply, show l - 1 + 1 = l by omega] at this
    exact hv this
  inj := by
    intro q q' hqq
    let σ := Fintype.equivFin {j // Jp S j}
    let lift : (Fin (Fintype.card {j // Jp S j}) → ℕ) → S.ι → ℕ :=
      fun q j => if h : Jp S j then q (σ ⟨j, h⟩) else 0
    have hval : ∀ (q : Fin (Fintype.card {j // Jp S j}) → ℕ) (l : ℕ), S.val (lift q) l =
        S.c l + ∑ t, q t * S.v (σ.symm t).1 l := by
      intro q l
      simp only [Sys.val, lift]
      rw [sum_lift (Jp S) σ q (fun j => S.v j l)]
    have hQ : lift q = lift q' := by
      apply hinj
      intro l hl
      rw [hval, hval]
      congr 1
      rcases Nat.eq_zero_or_pos l with rfl | hl0
      · have : ∀ t, S.v (σ.symm t).1 0 = 0 := fun t => (σ.symm t).2
        simp [this]
      · have := congrFun hqq ⟨l - 1, by omega⟩
        simp only [Finset.sum_apply, Pi.smul_apply, smul_eq_mul,
          show l - 1 + 1 = l by omega] at this
        exact this
    funext t
    have := congrFun hQ (σ.symm t).1
    simpa [lift, (σ.symm t).2] using this
  laminar := by
    intro t t'
    generalize (Fintype.equivFin {j // Jp S j}).symm t = J
    generalize (Fintype.equivFin {j // Jp S j}).symm t' = J'
    have hl := S.laminar J.1 J'.1
    have h1 := pair_snd_pos hinj J.1 J.2
    have h2 := pair_snd_pos hinj J'.1 J'.2
    have h3 := S.le J.1
    have h4 := S.le J'.1
    simp only [newPair]
    split_ifs <;> simp only [Fin.mk_lt_mk] <;> omega

open Classical in
lemma cnt_toLam (S : Sys) {n : ℕ} (hW : S.Within n) (hinj : InjOn' S n) (e : Fin n → ℕ) :
    cnt n S (xe e) = if S.c 0 = 0 then (if (toLam S hW hinj).Mem e then 1 else 0) else 0 := by
  classical
  let L := toLam S hW hinj
  let σ : {j // Jp S j} ≃ Fin L.r := Fintype.equivFin {j // Jp S j}
  have hL_c : ∀ i, L.c i = S.c (i.1 + 1) := fun i => rfl
  have hL_v : ∀ t i, L.v t i = S.v (σ.symm t).1 (i.1 + 1) := fun t i => rfl
  let lift : (Fin L.r → ℕ) → S.ι → ℕ := fun q j => if h : Jp S j then q (σ ⟨j, h⟩) else 0
  have hval : ∀ (q : Fin L.r → ℕ) (l : ℕ), S.val (lift q) l =
      S.c l + ∑ t, q t * S.v (σ.symm t).1 l := by
    intro q l
    simp only [Sys.val, lift]
    rw [sum_lift (Jp S) σ q (fun j => S.v j l)]
  have hx0 : xe e 0 = 0 := by simp [xe]
  have hxl : ∀ i : Fin n, xe e (i.1 + 1) = e i := by
    intro i; simp only [xe]; rw [dif_pos (by omega)]; simp
  have hmemiff : ∀ q : Fin L.r → ℕ, (e = L.c + ∑ t, q t • L.v t) ↔
      ∀ i : Fin n, e i = S.c (i.1 + 1) + ∑ t, q t * S.v (σ.symm t).1 (i.1 + 1) := by
    intro q
    rw [funext_iff]
    simp only [Pi.add_apply, Finset.sum_apply, Pi.smul_apply, smul_eq_mul, hL_c, hL_v]
  have hzero : ∀ t, S.v (σ.symm t).1 0 = 0 := fun t => (σ.symm t).2
  have c1 : ∀ q : Fin L.r → ℕ, S.c 0 = 0 → e = L.c + ∑ t, q t • L.v t →
      lift q ∈ S.fib n (xe e) := by
    intro q hc0 hq l hl
    rw [hval]
    rcases Nat.eq_zero_or_pos l with rfl | hl0
    · simp [hzero, hc0, hx0]
    · have h1 := (hmemiff q).mp hq ⟨l - 1, by omega⟩
      have h2 := hxl ⟨l - 1, by omega⟩
      simp only [show l - 1 + 1 = l by omega] at h1 h2
      rw [h2, h1]
  have c2 : ∀ Q ∈ S.fib n (xe e), S.c 0 = 0 ∧ ∃ q : Fin L.r → ℕ, e = L.c + ∑ t, q t • L.v t := by
    intro Q hQ
    have h0 := hQ 0 (Nat.zero_le _)
    rw [hx0] at h0
    simp only [Sys.val] at h0
    have hc0 : S.c 0 = 0 := by omega
    have hsum0 : ∑ j, Q j * S.v j 0 = 0 := by omega
    have hQz : ∀ j, ¬ Jp S j → Q j = 0 := by
      intro j hj
      have := (Finset.sum_eq_zero_iff.mp hsum0) j (mem_univ _)
      rcases mul_eq_zero.mp this with h | h
      · exact h
      · exact absurd h hj
    have hQl : Q = lift (fun t => Q (σ.symm t).1) := by
      funext j
      simp only [lift]
      split_ifs with h
      · simp
      · exact hQz j h
    refine ⟨hc0, fun t => Q (σ.symm t).1, (hmemiff _).mpr fun i => ?_⟩
    have h1 := hQ (i.1 + 1) (by omega)
    have h2 : S.val Q (i.1 + 1) = S.val (lift fun t => Q (σ.symm t).1) (i.1 + 1) := by
      rw [← hQl]
    have h3 := (hval (fun t => Q (σ.symm t).1) (i.1 + 1)).symm.trans (h2.symm.trans h1)
    rw [hxl] at h3
    exact h3.symm
  have c3 : ∀ Q ∈ S.fib n (xe e), ∀ Q' ∈ S.fib n (xe e), Q = Q' :=
    fun Q hQ Q' hQ' => hinj Q Q' fun l hl => (hQ l hl).trans (hQ' l hl).symm
  unfold cnt
  by_cases hc0 : S.c 0 = 0
  · rw [if_pos hc0]
    split_ifs with hm
    · obtain ⟨q, hq⟩ := hm
      rw [Set.encard_eq_one]
      exact ⟨lift q, Set.ext fun Q => ⟨fun hQ => c3 _ hQ _ (c1 q hc0 hq),
        fun h => h ▸ c1 q hc0 hq⟩⟩
    · rw [Set.encard_eq_zero, Set.eq_empty_iff_forall_notMem]
      intro Q hQ; exact hm (c2 Q hQ).2
  · rw [if_neg hc0, Set.encard_eq_zero, Set.eq_empty_iff_forall_notMem]
    intro Q hQ; exact hc0 (c2 Q hQ).1

end toLam

lemma final_lists (n k : ℕ) (Ls : List Sys) (hW : ∀ S ∈ Ls, S.Within n)
    (hb : ∀ S ∈ Ls, ∀ x, cnt n S x ≤ k) :
    ∃ Ls' : List (LamLinSet n), ∀ e, (Ls.map fun S => cnt n S (xe e)).sum = (ply Ls' e : ℕ∞) := by
  classical
  induction Ls with
  | nil => exact ⟨[], fun e => by simp [ply]⟩
  | cons S Ls ih =>
    obtain ⟨Ls', h'⟩ := ih (fun S' h => hW S' (by simp [h])) (fun S' h => hb S' (by simp [h]))
    have hinj : InjOn' S n := inj_of_bdd S n k (hb S (by simp))
    have hWS := hW S (by simp)
    by_cases hc0 : S.c 0 = 0
    · refine ⟨toLam S hWS hinj :: Ls', fun e => ?_⟩
      simp only [List.map_cons, List.sum_cons, h', cnt_toLam S hWS hinj e, if_pos hc0]
      unfold ply
      rw [List.countP_cons]
      by_cases hm : (toLam S hWS hinj).Mem e
      · simp only [hm, decide_true, if_true]; push_cast; ring
      · simp only [hm, decide_false, if_false]; simp
    · refine ⟨Ls', fun e => ?_⟩
      simp only [List.map_cons, List.sum_cons, h', cnt_toLam S hWS hinj e, if_neg hc0, zero_add]

lemma segWord_blocks : ∀ (n c : ℕ) (y : ℕ → ℕ),
    segWord n (fun k => if k = 0 then c else y (k - 1)) =
      List.replicate c true ++ (List.ofFn fun i : Fin n => ab (y i)).flatten
  | 0, c, y => by simp [segWord]
  | n + 1, c, y => by
    simp only [segWord, if_true]
    rw [segWord_congr n _ (fun k => if k = 0 then y 0 else (fun k => y (k + 1)) (k - 1))
      (fun k _ => by rcases k with _ | k <;> simp)]
    rw [segWord_blocks n (y 0) (fun k => y (k + 1)), List.ofFn_succ, List.flatten_cons]
    simp [ab]

lemma blockWord_eq {n : ℕ} (e : Fin n → ℕ) : blockWord e = segWord n (xe e) := by
  have h := segWord_blocks n 0 (fun k => if h : k < n then e ⟨k, h⟩ else 0)
  rw [segWord_congr n (xe e) _ (fun k _ => ?_), h]
  · simp [blockWord]
  · unfold xe
    rcases k with _ | k
    · simp
    · by_cases hk : k < n
      · simp [hk, show k + 1 ≤ n by omega]
      · simp [hk, show ¬ (k + 1 ≤ n) by omega]

end S2
end FA
