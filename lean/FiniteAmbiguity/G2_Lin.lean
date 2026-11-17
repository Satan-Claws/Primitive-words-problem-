/-
# Linear algebra attached to a laminar linear set (agent G2).
For `L = c + ℕ v₁ + ⋯ + ℕ v_r` we work over `ℚ`: `Φ q = ∑ q_j v_j` is injective, `A` is a left
inverse of `Φ`, and `R = id - Φ ∘ A` vanishes exactly on `span V`.
-/
import FiniteAmbiguity.G2_Basic
import FiniteAmbiguity.Defs

namespace FA.G2

variable {n : ℕ}

/-- The periods, as rational vectors. -/
def Vq (L : LamLinSet n) (j : Fin L.r) : Fin n → ℚ := fun i => (L.v j i : ℚ)

/-- The constant, as a rational vector. -/
def cq (L : LamLinSet n) : Fin n → ℚ := fun i => (L.c i : ℚ)

/-- `Φ q = ∑ q_j v_j`. -/
noncomputable def Φ (L : LamLinSet n) : (Fin L.r → ℚ) →ₗ[ℚ] (Fin n → ℚ) :=
  Fintype.linearCombination ℚ (Vq L)

theorem Φ_apply (L : LamLinSet n) (g : Fin L.r → ℚ) : Φ L g = ∑ j, g j • Vq L j :=
  Fintype.linearCombination_apply _ _ _

/-- The periods are linearly independent over `ℚ` (from injectivity over `ℕ`). -/
theorem linIndep (L : LamLinSet n) : LinearIndependent ℚ (Vq L) := by
  rw [Fintype.linearIndependent_iff]
  intro g hg
  obtain ⟨D, hD, hz⟩ := exists_common_den g
  choose z hz using hz
  let qp : Fin L.r → ℕ := fun j => (z j).toNat
  let qm : Fin L.r → ℕ := fun j => (-z j).toNat
  have hzq : ∀ j, (z j : ℚ) = (qp j : ℚ) - (qm j : ℚ) := by
    intro j
    have h := Int.toNat_sub_toNat_neg (z j)
    have : ((z j : ℤ) : ℚ) = ((((z j).toNat : ℤ) - ((-z j).toNat : ℤ) : ℤ) : ℚ) := by rw [h]
    rw [this]
    push_cast
    rfl
  have heq : ∑ j, qp j • L.v j = ∑ j, qm j • L.v j := by
    funext i
    apply Nat.cast_injective (R := ℚ)
    have := congrFun hg i
    simp only [Finset.sum_apply, Pi.smul_apply, smul_eq_mul, Vq, Pi.zero_apply] at this
    simp only [Finset.sum_apply, Pi.smul_apply, smul_eq_mul, Nat.cast_sum, Nat.cast_mul]
    have h2 : ∑ j, (qp j : ℚ) * L.v j i - ∑ j, (qm j : ℚ) * L.v j i
        = D * ∑ j, g j * L.v j i := by
      rw [← Finset.sum_sub_distrib, Finset.mul_sum]
      refine Finset.sum_congr rfl fun j _ => ?_
      rw [← sub_mul, ← hzq, ← hz]
      ring
    rw [this, mul_zero] at h2
    linarith
  have hq := L.inj heq
  intro j
  have h1 : (qp j : ℚ) = qm j := by rw [congrFun hq j]
  have h2 := hz j
  rw [hzq, h1, sub_self] at h2
  have hD' : (D : ℚ) ≠ 0 := by exact_mod_cast hD.ne'
  exact (mul_eq_zero.1 h2).resolve_left hD'

theorem Φ_injective (L : LamLinSet n) : Function.Injective (Φ L) := by
  intro x y hxy
  have h := (Fintype.linearIndependent_iff.1 (linIndep L)) (x - y)
  rw [← Φ_apply, map_sub, hxy, sub_self] at h
  funext j
  exact sub_eq_zero.1 (h rfl j)

theorem exists_A (L : LamLinSet n) : ∃ g : (Fin n → ℚ) →ₗ[ℚ] (Fin L.r → ℚ),
    g ∘ₗ Φ L = LinearMap.id :=
  LinearMap.exists_leftInverse_of_injective _ (LinearMap.ker_eq_bot.2 (Φ_injective L))

/-- A left inverse of `Φ`. -/
noncomputable def A (L : LamLinSet n) : (Fin n → ℚ) →ₗ[ℚ] (Fin L.r → ℚ) :=
  Classical.choose (exists_A L)

theorem A_Φ (L : LamLinSet n) (x : Fin L.r → ℚ) : A L (Φ L x) = x :=
  LinearMap.congr_fun (Classical.choose_spec (exists_A L)) x

/-- `R = id - Φ ∘ A`; it vanishes exactly on the span of the periods. -/
noncomputable def R (L : LamLinSet n) : (Fin n → ℚ) →ₗ[ℚ] (Fin n → ℚ) :=
  LinearMap.id - Φ L ∘ₗ A L

theorem R_apply (L : LamLinSet n) (x : Fin n → ℚ) : R L x = x - Φ L (A L x) := by
  simp [R]

theorem R_eq_zero_iff (L : LamLinSet n) (x : Fin n → ℚ) : R L x = 0 ↔ x = Φ L (A L x) := by
  rw [R_apply, sub_eq_zero]

/-- Rational membership. -/
def memQ (L : LamLinSet n) (x : Fin n → ℚ) : Prop :=
  ∃ q : Fin L.r → ℕ, x = cq L + Φ L (fun j => (q j : ℚ))

theorem mem_iff_memQ (L : LamLinSet n) (p : Fin n → ℕ) :
    L.Mem p ↔ memQ L (fun i => (p i : ℚ)) := by
  unfold LamLinSet.Mem memQ
  refine exists_congr fun q => ?_
  rw [Φ_apply]
  constructor
  · intro h
    funext i
    subst h
    simp [cq, Vq, Finset.sum_apply]
  · intro h
    funext i
    have := congrFun h i
    simp only [cq, Vq, Pi.add_apply, Finset.sum_apply, Pi.smul_apply, smul_eq_mul] at this
    apply Nat.cast_injective (R := ℚ)
    simp only [Pi.add_apply, Finset.sum_apply, Pi.smul_apply, smul_eq_mul, Nat.cast_add,
      Nat.cast_sum, Nat.cast_mul]
    exact this

theorem memQ_iff (L : LamLinSet n) (x : Fin n → ℚ) :
    memQ L x ↔ R L (x - cq L) = 0 ∧ ∀ j, ∃ m : ℕ, A L (x - cq L) j = m := by
  constructor
  · rintro ⟨q, rfl⟩
    rw [add_sub_cancel_left, R_eq_zero_iff, A_Φ]
    exact ⟨rfl, fun j => ⟨q j, rfl⟩⟩
  · rintro ⟨h1, h2⟩
    choose m hm using h2
    refine ⟨m, ?_⟩
    rw [R_eq_zero_iff] at h1
    have : A L (x - cq L) = fun j => (m j : ℚ) := funext hm
    rw [← this, ← h1]
    abel

theorem r_le (L : LamLinSet n) : L.r ≤ n := by
  simpa using (linIndep L).fintype_card_le_finrank

theorem R_eq_zero_of_r_eq (L : LamLinSet n) (h : L.r = n) (x : Fin n → ℚ) : R L x = 0 := by
  have htop : LinearMap.range (Φ L) = ⊤ := by
    apply Submodule.eq_top_of_finrank_eq
    rw [LinearMap.finrank_range_of_inj (Φ_injective L)]
    simp [h]
  obtain ⟨y, rfl⟩ : x ∈ LinearMap.range (Φ L) := by rw [htop]; trivial
  rw [R_apply, A_Φ, sub_self]

end FA.G2
