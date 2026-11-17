/-
# Lemma 4.1 (non-interleaving) and Lemma X (PROOF.md §4).  OWNER: agent G1.
Coordinates of `Fin (M + M)`: `Fin.castAdd M i` is `x_i`, `Fin.natAdd M i` is `y_i`.
-/
import FiniteAmbiguity.Defs
import FiniteAmbiguity.Prelude

namespace FA

/-- The diagonal vector `e_{x_i} + e_{y_i}`. -/
def diagVec (M : ℕ) (i : Fin M) : Fin (M + M) → ℚ :=
  Pi.single (Fin.castAdd M i) 1 + Pi.single (Fin.natAdd M i) 1

namespace LemmaXAux

variable {N : ℕ} {ι : Type*}

/-- Adjacency in the support graph: both coordinates lie in the support of a common vector. -/
def Adj (v : ι → Fin N → ℚ) (a b : Fin N) : Prop := ∃ j, v j a ≠ 0 ∧ v j b ≠ 0

/-- Same connected component of the support graph. -/
def R (v : ι → Fin N → ℚ) : Fin N → Fin N → Prop := Relation.ReflTransGen (Adj v)

lemma adj_symm {v : ι → Fin N → ℚ} {a b : Fin N} (h : Adj v a b) : Adj v b a := by
  obtain ⟨j, h1, h2⟩ := h; exact ⟨j, h2, h1⟩

lemma R_symm {v : ι → Fin N → ℚ} {a b : Fin N} (h : R v a b) : R v b a :=
  by
  induction h with
  | refl => exact Relation.ReflTransGen.refl
  | tail _ hadj ih => exact Relation.ReflTransGen.head (adj_symm hadj) ih

lemma R_refl {v : ι → Fin N → ℚ} {a : Fin N} : R v a a := Relation.ReflTransGen.refl

lemma R_trans {v : ι → Fin N → ℚ} {a b c : Fin N} (h : R v a b) (h' : R v b c) : R v a c :=
  Relation.ReflTransGen.trans h h'

lemma R_adj {v : ι → Fin N → ℚ} {a b c : Fin N} (h : R v a b) (h' : Adj v b c) : R v a c :=
  Relation.ReflTransGen.tail h h'

section
variable {v : ι → Fin N → ℚ} {pair : ι → Fin N × Fin N}
  (hle : ∀ j, (pair j).1 ≤ (pair j).2)
  (hsupp : ∀ j i, v j i ≠ 0 → i = (pair j).1 ∨ i = (pair j).2)
include hle hsupp

lemma adj_pair {a b : Fin N} {j : ι} (ha : v j a ≠ 0) (hb : v j b ≠ 0) (hab : a < b) :
    (pair j).1 = a ∧ (pair j).2 = b := by
  have h1 := hle j
  rcases hsupp j a ha with h | h <;> rcases hsupp j b hb with h' | h'
  · subst h; subst h'; exact absurd hab (lt_irrefl _)
  · exact ⟨h.symm, h'.symm⟩
  · subst h; subst h'; exact absurd (lt_of_lt_of_le hab h1) (lt_irrefl _)
  · subst h; subst h'; exact absurd hab (lt_irrefl _)

variable (hlam : ∀ j j', ¬ ((pair j).1 < (pair j').1 ∧ (pair j').1 < (pair j).2 ∧
      (pair j).2 < (pair j').2))
include hlam

lemma nc {a b c d : Fin N} (h1 : Adj v a b) (h2 : Adj v c d) (hac : a < c) (hcb : c < b)
    (hbd : b < d) : False := by
  obtain ⟨j, ha, hb⟩ := h1
  obtain ⟨j', hc, hd⟩ := h2
  obtain ⟨e1, e2⟩ := adj_pair hle hsupp ha hb (lt_trans hac hcb)
  obtain ⟨e3, e4⟩ := adj_pair hle hsupp hc hd (lt_trans hcb hbd)
  exact hlam j j' ⟨by rw [e1, e3]; exact hac, by rw [e3, e2]; exact hcb, by rw [e2, e4]; exact hbd⟩

omit hle hsupp hlam in
/-- A path from `p` to `r` passing over `q ∉ C` uses an edge `{a,b}` with `a < q < b`. -/
lemma lemA {p r q : Fin N} (hpr : R v p r) (hpq : p < q) (hqr : q < r) (hnq : ¬ R v p q) :
    ∃ a b, R v p a ∧ Adj v a b ∧ a < q ∧ q < b := by
  induction hpr with
  | refl => exact absurd (lt_trans hpq hqr) (lt_irrefl _)
  | @tail r' r hr' hadj ih =>
    rcases lt_trichotomy r' q with h | h | h
    · exact ⟨r', r, hr', hadj, h, hqr⟩
    · subst h; exact absurd hr' hnq
    · exact ih h

/-- A component meeting the interior of an edge `{a,b}` of another component lies inside it. -/
lemma lemB {a b c d : Fin N} (hab : Adj v a b) (hcd : R v c d) (hac : a < c) (hcb : c < b)
    (hna : ¬ R v c a) (hnb : ¬ R v c b) : a < d ∧ d < b := by
  induction hcd with
  | refl => exact ⟨hac, hcb⟩
  | @tail d' d hd' hadj ih =>
    obtain ⟨h1, h2⟩ := ih
    refine ⟨?_, ?_⟩
    · rcases lt_trichotomy a d with h | h | h
      · exact h
      · subst h; exact absurd (R_adj hd' hadj) hna
      · exact (nc hle hsupp hlam (adj_symm hadj) hab h h1 h2).elim
    · rcases lt_trichotomy d b with h | h | h
      · exact h
      · subst h; exact absurd (R_adj hd' hadj) hnb
      · exact (nc hle hsupp hlam hab hadj h1 h2 h).elim

/-- **Lemma 4.1 (non-interleaving).** -/
lemma noninterleave {p q r s : Fin N} (hpq : p < q) (hqr : q < r) (hrs : r < s)
    (hpr : R v p r) (hqs : R v q s) (hn : ¬ R v p q) : False := by
  obtain ⟨a, b, hpa, hab, haq, hqb⟩ := lemA hpr hpq hqr hn
  have hpb : R v p b := R_adj hpa hab
  have hnqr : ¬ R v q r := fun h => hn (R_trans hpr (R_symm h))
  obtain ⟨c, d, hqc, hcd, hcr, hrd⟩ := lemA hqs hqr hrs hnqr
  have hqd : R v q d := R_adj hqc hcd
  -- `c ∈ (a, b)`
  have h1 := lemB hle hsupp hlam hab hqc haq hqb
    (fun h => hn (R_trans hpa (R_symm h))) (fun h => hn (R_trans hpb (R_symm h)))
  -- `a ∈ (c, d)`
  have h2 := lemB hle hsupp hlam hcd (R_trans (R_symm hpr) hpa) hcr hrd
    (fun h => hn (R_symm (R_trans (R_trans hqc (R_symm h)) (R_symm hpr))))
    (fun h => hn (R_symm (R_trans (R_trans hqd (R_symm h)) (R_symm hpr))))
  exact lt_asymm h1.1 h2.1

end

/-- Restriction of a vector to the coordinates satisfying `P`. -/
def restr (P : Fin N → Prop) [DecidablePred P] : (Fin N → ℚ) →ₗ[ℚ] (Fin N → ℚ) where
  toFun w k := if P k then w k else 0
  map_add' x y := by funext k; by_cases h : P k <;> simp [h]
  map_smul' c x := by funext k; by_cases h : P k <;> simp [h]

lemma restr_apply (P : Fin N → Prop) [DecidablePred P] (w : Fin N → ℚ) (k : Fin N) :
    restr P w k = if P k then w k else 0 := rfl

lemma restr_single (P : Fin N → Prop) [DecidablePred P] (k : Fin N) :
    restr P (Pi.single k 1) = if P k then Pi.single k 1 else 0 := by
  funext l
  by_cases hl : l = k
  · subst hl; by_cases h : P l <;> simp [restr_apply, h]
  · by_cases h : P k <;> simp [restr_apply, hl, h]

end LemmaXAux

open LemmaXAux in

/-- **Lemma X.** A family of non-negative vectors, each supported on a pair `s ≤ t`, with pairwise
non-crossing pairs, whose span contains every diagonal vector, spans a space of dimension at least
`2M - 1`. -/
theorem lemmaX {M : ℕ} {ι : Type*} (v : ι → Fin (M + M) → ℚ) (pair : ι → Fin (M + M) × Fin (M + M))
    (hle : ∀ j, (pair j).1 ≤ (pair j).2)
    (hnonneg : ∀ j i, 0 ≤ v j i)
    (hsupp : ∀ j i, v j i ≠ 0 → i = (pair j).1 ∨ i = (pair j).2)
    (hlam : ∀ j j', ¬ ((pair j).1 < (pair j').1 ∧ (pair j').1 < (pair j).2 ∧
      (pair j).2 < (pair j').2))
    (hW : ∀ i : Fin M, diagVec M i ∈ Submodule.span ℚ (Set.range v)) :
    M + M ≤ Module.finrank ℚ (Submodule.span ℚ (Set.range v)) + 1 := by
  classical
  set V := Submodule.span ℚ (Set.range v) with hV
  set D := V.dualAnnihilator with hD
  set e : Fin (M + M) → Fin (M + M) → ℚ := fun k => Pi.single k 1 with he
  have hvD : ∀ f ∈ D, ∀ j, f (v j) = 0 := fun f hf j =>
    (Submodule.mem_dualAnnihilator f).1 hf _ (Submodule.subset_span ⟨j, rfl⟩)
  have hdiag : ∀ f ∈ D, ∀ i, f (e (Fin.castAdd M i)) + f (e (Fin.natAdd M i)) = 0 := by
    intro f hf i
    have := (Submodule.mem_dualAnnihilator f).1 hf _ (hW i)
    simpa [diagVec, map_add, he] using this
  -- propagation of (non)vanishing along edges
  have hprop_lt : ∀ f ∈ D, ∀ a b, a < b → Adj v a b → (f (e a) = 0 ↔ f (e b) = 0) := by
    rintro f hf a b hab ⟨j, ha, hb⟩
    obtain ⟨h1, h2⟩ := adj_pair hle hsupp ha hb hab
    have hvj : v j = v j a • e a + v j b • e b := by
      funext k
      by_cases hka : k = a
      · subst hka; simp [he, hab.ne]
      · by_cases hkb : k = b
        · subst hkb; simp [he, hka]
        · have : v j k = 0 := by
            by_contra hne
            rcases hsupp j k hne with h | h
            · exact hka (h.trans h1)
            · exact hkb (h.trans h2)
          simp [he, hka, hkb, this]
    have h0 := hvD f hf j
    rw [hvj, map_add, map_smul, map_smul, smul_eq_mul, smul_eq_mul] at h0
    constructor
    · intro h; rw [h, mul_zero, zero_add] at h0; exact (mul_eq_zero.1 h0).resolve_left hb
    · intro h; rw [h, mul_zero, add_zero] at h0; exact (mul_eq_zero.1 h0).resolve_left ha
  have hprop_adj : ∀ f ∈ D, ∀ a b, Adj v a b → (f (e a) = 0 ↔ f (e b) = 0) := by
    intro f hf a b hadj
    rcases lt_trichotomy a b with h | h | h
    · exact hprop_lt f hf a b h hadj
    · subst h; exact Iff.rfl
    · exact (hprop_lt f hf b a h (adj_symm hadj)).symm
  have hprop_R : ∀ f ∈ D, ∀ a b, R v a b → (f (e a) = 0 ↔ f (e b) = 0) := by
    intro f hf a b h
    induction h with
    | refl => exact Iff.rfl
    | tail _ hadj ih => exact ih.trans (hprop_adj f hf _ _ hadj)
  -- restriction to a component stays in the annihilator
  have hrestrD : ∀ f ∈ D, ∀ q, f ∘ₗ restr (R v q) ∈ D := by
    intro f hf q
    rw [Submodule.mem_dualAnnihilator]
    intro w hw
    have hle' : V ≤ LinearMap.ker (f ∘ₗ restr (R v q)) := by
      rw [hV, Submodule.span_le]
      rintro _ ⟨j, rfl⟩
      simp only [SetLike.mem_coe, LinearMap.mem_ker, LinearMap.comp_apply]
      by_cases h : ∃ k, v j k ≠ 0 ∧ R v q k
      · obtain ⟨k0, hk0, hRk0⟩ := h
        have : restr (R v q) (v j) = v j := by
          funext k
          rw [restr_apply]
          split_ifs with hk
          · rfl
          · by_contra hne
            exact hk (R_adj hRk0 ⟨j, hk0, Ne.symm hne⟩)
        rw [this]; exact hvD f hf j
      · push Not at h
        have : restr (R v q) (v j) = 0 := by
          funext k
          rw [restr_apply]
          split_ifs with hk
          · by_contra hne; exact h k hne hk
          · rfl
        rw [this, map_zero]
    exact hle' hw
  have hcomp : ∀ (f : Module.Dual ℚ (Fin (M + M) → ℚ)) q k,
      (f ∘ₗ restr (R v q)) (e k) = if R v q k then f (e k) else 0 := by
    intro f q k
    rw [LinearMap.comp_apply, he]
    simp only [restr_single]
    split_ifs <;> simp
  -- a component carrying a nonzero annihilating functional contains a diagonal pair
  have hpairR : ∀ f ∈ D, ∀ q, f (e q) ≠ 0 →
      ∃ i, R v q (Fin.castAdd M i) ∧ R v q (Fin.natAdd M i) := by
    intro f hf q hq
    have hq'' := hdiag _ (hrestrD f hf q)
    rcases (show (∃ i, q = Fin.castAdd M i) ∨ ∃ i, q = Fin.natAdd M i from
      Fin.addCases (fun i => Or.inl ⟨i, rfl⟩) (fun i => Or.inr ⟨i, rfl⟩) q) with
      ⟨i, rfl⟩ | ⟨i, rfl⟩
    · refine ⟨i, Relation.ReflTransGen.refl, ?_⟩
      have hq' := hq'' i
      rw [hcomp, hcomp] at hq'
      by_contra hn
      simp only [R_refl, ↓reduceIte, hn, add_zero] at hq'
      exact hq hq'
    · refine ⟨i, ?_, Relation.ReflTransGen.refl⟩
      have hq' := hq'' i
      rw [hcomp, hcomp] at hq'
      by_contra hn
      simp only [R_refl, ↓reduceIte, hn, zero_add] at hq'
      exact hq hq'
  -- the key rigidity statement
  have hL : ∀ f ∈ D, ∀ g ∈ D, ∀ p, f (e p) ≠ 0 → g (e p) = 0 → ∀ q, g (e q) = 0 := by
    intro f hf g hg p hfp hgp q
    by_contra hq
    have hnpq : ¬ R v p q := fun h => hq ((hprop_R g hg p q h).1 hgp)
    obtain ⟨i, hi1, hi2⟩ := hpairR f hf p hfp
    obtain ⟨k, hk1, hk2⟩ := hpairR g hg q hq
    have hRi : R v (Fin.castAdd M i) (Fin.natAdd M i) := R_trans (R_symm hi1) hi2
    have hRk : R v (Fin.castAdd M k) (Fin.natAdd M k) := R_trans (R_symm hk1) hk2
    rcases lt_trichotomy i k with h | h | h
    · have h' : i.val < k.val := h
      refine noninterleave hle hsupp hlam (p := Fin.castAdd M i) (q := Fin.castAdd M k)
        (r := Fin.natAdd M i) (s := Fin.natAdd M k) ?_ ?_ ?_ hRi hRk ?_
      · rw [Fin.lt_def]; simp; omega
      · rw [Fin.lt_def]; simp; omega
      · rw [Fin.lt_def]; simp; omega
      · intro hx; exact hnpq (R_trans (R_trans hi1 hx) (R_symm hk1))
    · subst h; exact hnpq (R_trans hi1 (R_symm hk1))
    · have h' : k.val < i.val := h
      refine noninterleave hle hsupp hlam (p := Fin.castAdd M k) (q := Fin.castAdd M i)
        (r := Fin.natAdd M k) (s := Fin.natAdd M i) ?_ ?_ ?_ hRk hRi ?_
      · rw [Fin.lt_def]; simp; omega
      · rw [Fin.lt_def]; simp; omega
      · rw [Fin.lt_def]; simp; omega
      · intro hx; exact hnpq (R_trans (R_trans hi1 (R_symm hx)) (R_symm hk1))
  -- functionals are determined by their values on the `e k`
  have hext : ∀ f : Module.Dual ℚ (Fin (M + M) → ℚ), (∀ k, f (e k) = 0) → f = 0 := by
    intro f h
    apply LinearMap.pi_ext
    intro i x
    have : (Pi.single i x : Fin (M + M) → ℚ) = x • e i := by
      funext k; by_cases hk : k = i
      · subst hk; simp [he]
      · simp [he, hk]
    rw [this, map_smul, h i]; simp
  have hdim := Subspace.finrank_add_finrank_dualAnnihilator_eq V
  rw [Module.finrank_fin_fun, ← hD] at hdim
  suffices hD1 : Module.finrank ℚ D ≤ 1 by omega
  by_cases hD0 : ∀ f ∈ D, f = 0
  · have : D = ⊥ := (Submodule.eq_bot_iff _).2 hD0
    rw [this, finrank_bot]; omega
  · push Not at hD0
    obtain ⟨f0, hf0, hne⟩ := hD0
    have : ∃ p, f0 (e p) ≠ 0 := by
      by_contra h; push Not at h; exact hne (hext f0 h)
    obtain ⟨p, hp⟩ := this
    let φ : D →ₗ[ℚ] ℚ := (Module.Dual.eval ℚ _ (e p)).comp D.subtype
    have hinj : Function.Injective φ := by
      rw [← LinearMap.ker_eq_bot, LinearMap.ker_eq_bot']
      intro g hg
      apply Subtype.ext
      exact hext g (hL f0 hf0 g g.2 p hp hg)
    have := LinearMap.finrank_le_finrank_of_injective hinj
    simpa using this

end FA
