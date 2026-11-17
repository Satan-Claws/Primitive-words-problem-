/-
# Structure of finitely ambiguous CNF grammars on block words
(PROOF.md §3, Lemma 3.)  OWNER: agent S2.

The proof is split over the helper files `S2_*.lean`:
* `S2_Trees`  — tree counts `T`, their recursion, segment words `b^{x_0} a ⋯ a b^{x_m}`;
* `S2_Sys`    — laminar linear systems with multiplicities, closure under sums, shifts,
                convolution (gluing at a block) and adding a ring period;
* `S2_Shift`  — shifts, convolutions, and the two pumping lemmas (linear / quadratic);
* `S2_Induct` — the edge relation of a level, terms of the recursion, the acyclic step;
* `S2_Cyclic` — nontrivial components are rings with one unit side (pumping), the cyclic step,
                and the main induction `rep_main`;
* `S2_Final`  — bounded multiplicities are injective; restriction to `x_0 = 0` gives
                `LamLinSet`s (audit fix F2: pairs `{0, t}` become `{t}`).
-/
import FiniteAmbiguity.S2_Final

namespace FA

/-- **Structure lemma.** If a CNF grammar is `k`-ambiguous then, for every `n`, its tree count on
block words `a b^{e_0} ⋯ a b^{e_{n-1}}` is the ply of a finite list of laminar simple linear sets. -/
theorem cnf_structure_blocks (C : CNF) (k : ℕ) (hk : ∀ w, C.amb w ≤ k) (n : ℕ) :
    ∃ Ls : List (LamLinSet n), ∀ e : Fin n → ℕ, C.amb (blockWord e) = (ply Ls e : ℕ∞) := by
  have hB : S2.Bdd C k n C.start := fun x => hk (S2.segWord n x)
  obtain ⟨Ls, hW, he⟩ := S2.rep_main C k n C.start hB
  have hb : ∀ S ∈ Ls, ∀ x, S2.cnt n S x ≤ k := fun S hS x =>
    (S2.list_le_sum Ls (fun S => S2.cnt n S x) hS).trans ((he x).symm ▸ hB x)
  obtain ⟨Ls', h'⟩ := S2.final_lists n k Ls hW hb
  refine ⟨Ls', fun e => ?_⟩
  rw [S2.blockWord_eq, ← h' e, ← he]
  rfl

end FA
