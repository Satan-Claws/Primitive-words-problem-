/-
# Conversion of a cycle-free grammar to CNF without increasing tree counts
(PROOF.md §2, Lemma 1.1 of research/reports/ambiguity.md.)  OWNER: agent S1.

## Construction
We use a *semantic* CNF grammar `S1.cnf G` together with a normalisation map
`S1.norm : Tree G.N → Option (CTree _)` which deletes ε-subtrees, contracts unit chains
(by relabelling) and binarises children lists.  Nonterminals of the CNF grammar are
* `sym x` for a symbol `x : Bool ⊕ G.N` (`sym (inl c)` lifts the terminal `c`), and
* `lab β` for a suffix `β` of a right-hand side of `G` (a list of sibling subtrees).

The rules are *defined* so that `norm` maps valid `G`-trees with non-empty yield to valid
CNF trees (same yield, root `sym (root)`), and conversely every valid CNF tree is `norm s`
for some valid `G`-tree `s` with the corresponding root.  So `norm` maps the `G`-derivations of
`w` onto the CNF derivations of `w`, which gives both the language equality and
`amb_C(w) ≤ amb_G(w)`.  (Cycle-freeness is not even needed for this statement.)
-/
import FiniteAmbiguity.CNFDefs
import FiniteAmbiguity.Prelude

namespace FA

namespace S1

open Relation

variable (G : CFG)

/-- All suffixes of right-hand sides of rules of `G`. -/
def sufs : Finset (List (Bool ⊕ G.N)) := G.rules.biUnion fun p => p.2.tails.toFinset

variable {G}

lemma mem_sufs {β : List (Bool ⊕ G.N)} : β ∈ sufs G ↔ ∃ p ∈ G.rules, β <:+ p.2 := by
  simp [sufs, List.mem_tails]

lemma sufs_tail {x : Bool ⊕ G.N} {β} (h : x :: β ∈ sufs G) : β ∈ sufs G := by
  rw [mem_sufs] at *
  obtain ⟨p, hp, hs⟩ := h
  exact ⟨p, hp, (List.suffix_cons x β).trans hs⟩

lemma rhs_mem_sufs {A : G.N} {β} (h : (A, β) ∈ G.rules) : β ∈ sufs G :=
  mem_sufs.2 ⟨_, h, List.suffix_refl _⟩

variable (G)

/-- Nonterminals of the CNF grammar. -/
abbrev NT := (Bool ⊕ G.N) ⊕ Option {β // β ∈ sufs G}

/-- The CNF nonterminal of a symbol. -/
def sym (x : Bool ⊕ G.N) : NT G := .inl x

/-- The CNF nonterminal of a list of sibling symbols (junk value `none` off `sufs G`). -/
def lab (β : List (Bool ⊕ G.N)) : NT G :=
  .inr (if h : β ∈ sufs G then some ⟨β, h⟩ else none)

variable {G}

lemma sym_inj {x y : Bool ⊕ G.N} (h : sym G x = sym G y) : x = y := Sum.inl_injective h

lemma lab_inj {β γ : List (Bool ⊕ G.N)} (hγ : γ ∈ sufs G) (h : lab G β = lab G γ) : β = γ := by
  unfold lab at h
  by_cases hβ : β ∈ sufs G <;> simp_all

lemma sym_ne_lab {x : Bool ⊕ G.N} {β} : sym G x ≠ lab G β := by
  simp [sym, lab]

/-- Replace the root label. -/
def relabel {N : Type} (X : N) : CTree N → CTree N
  | .leaf _ c => .leaf X c
  | .node _ l r => .node X l r

@[simp] lemma relabel_root {N : Type} (X : N) (t : CTree N) : (relabel X t).root = X := by
  cases t <;> rfl

@[simp] lemma relabel_yield {N : Type} (X : N) (t : CTree N) :
    (relabel X t).yield = t.yield := by
  cases t <;> rfl

@[simp] lemma relabel_relabel {N : Type} (X Y : N) (t : CTree N) :
    relabel X (relabel Y t) = relabel X t := by
  cases t <;> rfl

lemma relabel_self {N : Type} (t : CTree N) : relabel t.root t = t := by
  cases t <;> rfl

lemma CTree.yield_ne_nil {N : Type} : ∀ t : CTree N, t.yield ≠ []
  | .leaf _ _ => by simp [CTree.yield]
  | .node _ l _ => by simp [CTree.yield, CTree.yield_ne_nil l]

variable (G)

-- Normalisation of `G`-trees: delete ε-subtrees, contract unit nodes, binarise.
mutual
def norm : Tree G.N → Option (CTree (NT G))
  | .leaf c => some (.leaf (sym G (.inl c)) c)
  | .node A ts => (binL ts).map (relabel (sym G (.inr A)))
def binL : List (Tree G.N) → Option (CTree (NT G))
  | [] => none
  | t :: ts =>
    match norm t, binL ts with
    | none, none => none
    | none, some r => some (relabel (lab G ((t :: ts).map Tree.root)) r)
    | some l, none => some (relabel (lab G ((t :: ts).map Tree.root)) l)
    | some l, some r => some (.node (lab G ((t :: ts).map Tree.root)) l r)
end

/-- A symbol deriving the empty word. -/
def Nullable (x : Bool ⊕ G.N) : Prop := ∃ s, G.Valid s ∧ s.root = x ∧ s.yield = []

/-- Unit steps of the CNF grammar (relabellings performed by `norm`). -/
inductive U : NT G → NT G → Prop
  | rule {A : G.N} {β} : (A, β) ∈ G.rules → U (sym G (.inr A)) (lab G β)
  | skip {x : Bool ⊕ G.N} {γ} : x :: γ ∈ sufs G → Nullable G x → U (lab G (x :: γ)) (lab G γ)
  | unit {x : Bool ⊕ G.N} {γ} : x :: γ ∈ sufs G → (∀ y ∈ γ, Nullable G y) →
      U (lab G (x :: γ)) (sym G x)

/-- Genuinely binary steps of the CNF grammar. -/
def Own (X Y Z : NT G) : Prop :=
  ∃ x γ, x :: γ ∈ sufs G ∧ X = lab G (x :: γ) ∧ Y = sym G x ∧ Z = lab G γ

open Classical in
/-- The CNF grammar. -/
noncomputable def cnf : CNF where
  N := NT G
  start := sym G (.inr G.start)
  bin := Finset.univ.filter fun p => ∃ X', ReflTransGen (U G) p.1 X' ∧ Own G X' p.2.1 p.2.2
  term := Finset.univ.filter fun p => ReflTransGen (U G) p.1 (sym G (.inl p.2))

/-- The rule used at the top of `relabel X t` is a rule of `cnf G`. -/
def TopOK (X : NT G) : CTree (NT G) → Prop
  | .leaf _ c => ReflTransGen (U G) X (sym G (.inl c))
  | .node _ l r => ∃ X', ReflTransGen (U G) X X' ∧ Own G X' l.root r.root

/-- Validity of the immediate subtrees. -/
def ChildValid : CTree (NT G) → Prop
  | .leaf _ _ => True
  | .node _ l r => (cnf G).Valid l ∧ (cnf G).Valid r

variable {G}

lemma valid_relabel {X : NT G} {t : CTree (NT G)} (h1 : TopOK G X t) (h2 : ChildValid G t) :
    (cnf G).Valid (relabel X t) := by
  cases t with
  | leaf Y c =>
    show (X, c) ∈ (cnf G).term
    exact Finset.mem_filter.2 ⟨Finset.mem_univ _, h1⟩
  | node Y l r =>
    exact ⟨Finset.mem_filter.2 ⟨Finset.mem_univ _, h1⟩, h2.1, h2.2⟩

lemma topOK_mono {X Y : NT G} (h : ReflTransGen (U G) X Y) {t : CTree (NT G)}
    (ht : TopOK G Y t) : TopOK G X t := by
  cases t with
  | leaf Z c => exact h.trans ht
  | node Z l r =>
    obtain ⟨X', h', hown⟩ := ht
    exact ⟨X', h.trans h', hown⟩

/-! ### Yield and root of `norm` -/

mutual
theorem norm_spec : ∀ s : Tree G.N,
    (norm G s = none ∧ s.yield = []) ∨ ∃ t, norm G s = some t ∧ t.yield = s.yield
  | .leaf c => Or.inr ⟨_, rfl, rfl⟩
  | .node A ts => by
    rcases binL_spec ts with ⟨h1, h2⟩ | ⟨t, h1, h2⟩
    · left; simp [norm, h1, Tree.yield, h2]
    · right; exact ⟨relabel (sym G (.inr A)) t, by simp [norm, h1], by simp [Tree.yield, h2]⟩
theorem binL_spec : ∀ ts : List (Tree G.N),
    (binL G ts = none ∧ Tree.yieldList ts = []) ∨
      ∃ t, binL G ts = some t ∧ t.yield = Tree.yieldList ts
  | [] => Or.inl ⟨by simp [binL], by simp [Tree.yieldList]⟩
  | s :: ts => by
    rcases norm_spec s with ⟨h1, h2⟩ | ⟨l, h1, h2⟩ <;>
      rcases binL_spec ts with ⟨h3, h4⟩ | ⟨r, h3, h4⟩
    · left; simp [binL, h1, h3, Tree.yieldList, h2, h4]
    · right; exact ⟨relabel (lab G ((s :: ts).map Tree.root)) r, by simp [binL, h1, h3],
        by simp [Tree.yieldList, h2, h4]⟩
    · right; exact ⟨relabel (lab G ((s :: ts).map Tree.root)) l, by simp [binL, h1, h3],
        by simp [Tree.yieldList, h2, h4]⟩
    · right; exact ⟨.node (lab G ((s :: ts).map Tree.root)) l r, by simp [binL, h1, h3],
        by simp [Tree.yieldList, h2, h4, CTree.yield]⟩
end

lemma norm_yield {s : Tree G.N} {t} (h : norm G s = some t) : t.yield = s.yield := by
  rcases norm_spec s with ⟨h1, _⟩ | ⟨t', h1, h2⟩
  · simp [h1] at h
  · rw [h1] at h; cases h; exact h2

lemma norm_eq_none {s : Tree G.N} : norm G s = none ↔ s.yield = [] := by
  rcases norm_spec s with ⟨h1, h2⟩ | ⟨t', h1, h2⟩
  · simp [h1, h2]
  · simp only [h1, reduceCtorEq, false_iff]
    rw [← h2]; exact CTree.yield_ne_nil _

lemma binL_eq_none {ts : List (Tree G.N)} : binL G ts = none ↔ Tree.yieldList ts = [] := by
  rcases binL_spec ts with ⟨h1, h2⟩ | ⟨t', h1, h2⟩
  · simp [h1, h2]
  · simp only [h1, reduceCtorEq, false_iff]
    rw [← h2]; exact CTree.yield_ne_nil _

lemma norm_root {s : Tree G.N} {t} (h : norm G s = some t) : t.root = sym G s.root := by
  cases s with
  | leaf c => simp [norm] at h; subst h; rfl
  | node A ts =>
    simp only [norm, Option.map_eq_some_iff] at h
    obtain ⟨t', -, rfl⟩ := h
    simp [Tree.root]

lemma binL_root {ts : List (Tree G.N)} {t} (h : binL G ts = some t) :
    t.root = lab G (ts.map Tree.root) := by
  cases ts with
  | nil => simp [binL] at h
  | cons s ts =>
    simp only [binL] at h
    split at h <;> simp at h <;> subst h <;> simp [CTree.root]

lemma yieldList_eq_nil {ts : List (Tree G.N)} (h : Tree.yieldList ts = []) :
    ∀ s ∈ ts, s.yield = [] := by
  induction ts with
  | nil => simp
  | cons s ts ih =>
    simp only [Tree.yieldList, List.append_eq_nil_iff] at h
    simp only [List.mem_cons, forall_eq_or_imp]
    exact ⟨h.1, ih h.2⟩

lemma validList_iff {ts : List (Tree G.N)} : G.ValidList ts ↔ ∀ s ∈ ts, G.Valid s := by
  induction ts with
  | nil => simp [CFG.ValidList]
  | cons s ts ih => simp [CFG.ValidList, ih]

/-! ### `norm` produces valid CNF trees -/

mutual
theorem norm_valid : ∀ s : Tree G.N, G.Valid s → ∀ t, norm G s = some t →
    TopOK G (sym G s.root) t ∧ ChildValid G t
  | .leaf c, _, t, h => by
    simp [norm] at h; subst h
    exact ⟨ReflTransGen.refl, trivial⟩
  | .node A ts, hv, t, h => by
    simp only [norm, Option.map_eq_some_iff] at h
    obtain ⟨t', h', rfl⟩ := h
    obtain ⟨hr, hvl⟩ := hv
    obtain ⟨h1, h2⟩ := binL_valid ts hvl (rhs_mem_sufs hr) t' h'
    refine ⟨?_, ?_⟩
    · exact topOK_mono (ReflTransGen.single (U.rule hr)) (by cases t' <;> exact h1)
    · cases t' <;> exact h2
theorem binL_valid : ∀ ts : List (Tree G.N), G.ValidList ts → ts.map Tree.root ∈ sufs G →
    ∀ t, binL G ts = some t → TopOK G (lab G (ts.map Tree.root)) t ∧ ChildValid G t
  | [], _, _, t, h => by simp [binL] at h
  | s :: ts, hv, hsuf, t, h => by
    obtain ⟨hvs, hvts⟩ := hv
    have hsuf' : ts.map Tree.root ∈ sufs G := sufs_tail (by simpa using hsuf)
    simp only [binL] at h
    split at h
    · simp at h
    · rename_i hn r hr
      simp only [Option.some.injEq] at h; subst h
      obtain ⟨h1, h2⟩ := binL_valid ts hvts hsuf' r hr
      have hnull : Nullable G s.root := ⟨s, hvs, rfl, norm_eq_none.1 hn⟩
      refine ⟨?_, by cases r <;> exact h2⟩
      refine topOK_mono (ReflTransGen.single ?_) (by cases r <;> exact h1)
      exact U.skip (by simpa using hsuf) hnull
    · rename_i l hl hn
      simp only [Option.some.injEq] at h; subst h
      obtain ⟨h1, h2⟩ := norm_valid s hvs l hl
      refine ⟨?_, by cases l <;> exact h2⟩
      refine topOK_mono (ReflTransGen.single ?_) (by cases l <;> exact h1)
      refine U.unit (by simpa using hsuf) ?_
      intro y hy
      obtain ⟨s', hs', rfl⟩ := List.mem_map.1 hy
      exact ⟨s', (validList_iff.1 hvts) s' hs', rfl,
        yieldList_eq_nil (binL_eq_none.1 hn) s' hs'⟩
    · rename_i l r hl hr
      simp only [Option.some.injEq] at h; subst h
      obtain ⟨h1, h2⟩ := norm_valid s hvs l hl
      obtain ⟨h3, h4⟩ := binL_valid ts hvts hsuf' r hr
      refine ⟨⟨_, ReflTransGen.refl, s.root, ts.map Tree.root, by simpa using hsuf,
        by simp, norm_root hl, binL_root hr⟩, ?_, ?_⟩
      · rw [← relabel_self l]; exact valid_relabel (by rw [norm_root hl]; exact h1) h2
      · rw [← relabel_self r]; exact valid_relabel (by rw [binL_root hr]; exact h3) h4
end

/-! ### Every valid CNF tree is the normalisation of a valid `G`-tree -/

/-- `t` is the normal form of a valid tree or of a valid list of siblings. -/
def Realized (t : CTree (NT G)) : Prop :=
  (∃ s, G.Valid s ∧ norm G s = some t) ∨
    ∃ ts, ts.map Tree.root ∈ sufs G ∧ G.ValidList ts ∧ binL G ts = some t

lemma nullable_list {γ : List (Bool ⊕ G.N)} (h : ∀ y ∈ γ, Nullable G y) :
    ∃ es, G.ValidList es ∧ es.map Tree.root = γ ∧ Tree.yieldList es = [] := by
  induction γ with
  | nil => exact ⟨[], trivial, rfl, rfl⟩
  | cons y γ ih =>
    obtain ⟨e, he, hr, hy⟩ := h y (by simp)
    obtain ⟨es, h1, h2, h3⟩ := ih (fun z hz => h z (by simp [hz]))
    exact ⟨e :: es, ⟨he, h1⟩, by simp [hr, h2], by simp [Tree.yieldList, hy, h3]⟩

lemma realized_lab {t : CTree (NT G)} {β} (hβ : β ∈ sufs G) (ht : Realized t)
    (hroot : t.root = lab G β) :
    ∃ ts, ts.map Tree.root = β ∧ G.ValidList ts ∧ binL G ts = some t := by
  rcases ht with ⟨s, -, hs⟩ | ⟨ts, -, hv, hts⟩
  · exact absurd (hroot ▸ norm_root hs).symm sym_ne_lab
  · exact ⟨ts, lab_inj hβ (binL_root hts ▸ hroot), hv, hts⟩

lemma realized_sym {t : CTree (NT G)} {x} (ht : Realized t) (hroot : t.root = sym G x) :
    ∃ s, s.root = x ∧ G.Valid s ∧ norm G s = some t := by
  rcases ht with ⟨s, hv, hs⟩ | ⟨ts, -, -, hts⟩
  · exact ⟨s, sym_inj ((norm_root hs).symm.trans hroot), hv, hs⟩
  · exact absurd (hroot ▸ binL_root hts) sym_ne_lab

lemma realized_step {X Y : NT G} (hU : U G X Y) {t : CTree (NT G)} (ht : Realized t)
    (hroot : t.root = Y) : Realized (relabel X t) := by
  cases hU with
  | @rule A β hr =>
    obtain ⟨ts, hβ, hv, hts⟩ := realized_lab (rhs_mem_sufs hr) ht hroot
    subst hβ
    exact Or.inl ⟨.node A ts, ⟨hr, hv⟩, by simp [norm, hts]⟩
  | @skip x γ hsuf hnull =>
    obtain ⟨ts, hγ, hv, hts⟩ := realized_lab (sufs_tail hsuf) ht hroot
    obtain ⟨e, he, hr, hy⟩ := hnull
    refine Or.inr ⟨e :: ts, by simpa [hr, hγ] using hsuf, ⟨he, hv⟩, ?_⟩
    have hn : norm G e = none := norm_eq_none.2 hy
    simp [binL, hn, hts, hr, hγ]
  | @unit x γ hsuf hnull =>
    obtain ⟨s, hsr, hv, hs⟩ := realized_sym ht hroot
    obtain ⟨es, h1, h2, h3⟩ := nullable_list hnull
    refine Or.inr ⟨s :: es, by simpa [hsr, h2] using hsuf, ⟨hv, h1⟩, ?_⟩
    have hn : binL G es = none := binL_eq_none.2 h3
    simp [binL, hn, hs, hsr, h2]

lemma realized_chain {X Y : NT G} (h : ReflTransGen (U G) X Y) {t : CTree (NT G)}
    (ht : Realized t) (hroot : t.root = Y) : Realized (relabel X t) := by
  induction h using ReflTransGen.head_induction_on with
  | refl => rw [← hroot, relabel_self]; exact ht
  | head hU _ ih =>
    have := realized_step hU ih (relabel_root _ _)
    rwa [relabel_relabel] at this

theorem realized_of_valid : ∀ t : CTree (NT G), (cnf G).Valid t → Realized t
  | .leaf X c, h => by
    have h' : ReflTransGen (U G) X (sym G (.inl c)) := by
      have : (X, c) ∈ (cnf G).term := h
      simpa [cnf] using this
    have base : Realized (CTree.leaf (sym G (.inl c)) c) :=
      Or.inl ⟨.leaf c, trivial, rfl⟩
    exact realized_chain h' base rfl
  | .node X l r, h => by
    obtain ⟨hb, hl, hr⟩ := h
    have hb' : ∃ X', ReflTransGen (U G) X X' ∧ Own G X' l.root r.root := by
      have : (X, l.root, r.root) ∈ (cnf G).bin := hb
      simpa [cnf] using this
    obtain ⟨X', hX, x, γ, hsuf, rfl, hlr, hrr⟩ := hb'
    obtain ⟨s, hsr, hsv, hs⟩ := realized_sym (realized_of_valid l hl) hlr
    obtain ⟨ts, hγ, htv, hts⟩ := realized_lab (sufs_tail hsuf) (realized_of_valid r hr) hrr
    have base : Realized (CTree.node (lab G (x :: γ)) l r) := by
      refine Or.inr ⟨s :: ts, by simpa [hsr, hγ] using hsuf, ⟨hsv, htv⟩, ?_⟩
      simp [binL, hs, hts, hsr, hγ]
    exact realized_chain hX base rfl

end S1

open S1 in
/-- Every cycle-free grammar has a CNF grammar with the same non-empty words and no more trees on
any word. -/
theorem to_cnf (G : CFG) (hcf : G.CycleFree) :
    ∃ C : CNF, (∀ w, w ≠ [] → (C.Generates w ↔ G.Generates w)) ∧ (∀ w, C.amb w ≤ G.amb w) := by
  -- Every CNF derivation of `w` is the normal form of a `G`-derivation of `w`.
  have key : ∀ w t, (cnf G).IsDerivFrom (cnf G).start t w →
      ∃ s, G.IsDerivation s w ∧ norm G s = some t := by
    rintro w t ⟨hv, hroot, hy⟩
    obtain ⟨s, hsr, hsv, hs⟩ := realized_sym (realized_of_valid t hv) hroot
    exact ⟨s, ⟨hsv, hsr, (norm_yield hs).symm.trans hy⟩, hs⟩
  refine ⟨cnf G, fun w hw => ⟨?_, ?_⟩, fun w => ?_⟩
  · rintro ⟨t, ht⟩
    obtain ⟨s, hs, -⟩ := key w t ht
    exact ⟨s, hs⟩
  · rintro ⟨s, hv, hroot, hy⟩
    obtain ⟨t, ht⟩ : ∃ t, norm G s = some t := by
      cases h : norm G s with
      | none => exact absurd ((norm_eq_none.1 h).symm.trans hy).symm hw
      | some t => exact ⟨t, rfl⟩
    refine ⟨t, ?_, ?_, ?_⟩
    · rw [← relabel_self t]
      have := norm_valid s hv t ht
      exact valid_relabel (by rw [norm_root ht]; exact this.1) this.2
    · rw [norm_root ht, hroot]; rfl
    · rw [norm_yield ht, hy]
  · unfold CNF.amb CFG.amb
    let f : Tree G.N → CTree (cnf G).N := fun s => (norm G s).getD (.leaf (cnf G).start false)
    calc {t | (cnf G).IsDerivFrom (cnf G).start t w}.encard
        ≤ (f '' {s | G.IsDerivation s w}).encard := by
          apply Set.encard_le_encard
          intro t ht
          obtain ⟨s, hs, hn⟩ := key w t ht
          exact ⟨s, hs, by simp [f, hn]⟩
      _ ≤ _ := Set.encard_image_le _ _

end FA
