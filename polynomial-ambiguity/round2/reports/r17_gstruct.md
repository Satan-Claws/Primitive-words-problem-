# r17_gstruct.md — R17b-G: can G⁻ + rotation-density force C_exp? (G-struct)

Status: **G-struct NOT proved. The brief's mechanism is provably impossible.** You cannot get C_exp by "repeating the
centre slide independently via the nonlinear branching Y ⇒* αYβYγ". In a grammar without C_exp, every nonterminal of a
nonlinear SCC, and every nonterminal hanging off any loop, is **unambiguous** (Lemma SU). So no slide can ever happen
below Y. New items, all written proofs, elementary, no scripts:
- (0) G-struct is *equivalent* to T8_poly (Wich Thm 4.4). It is a reformulation, not a reduction.
- (SU) side-unambiguity;
- (IF) injective interfaces;
- (TR) the Trunk Lemma: all ambiguity of a C_exp-free grammar is the choice of O(1) junction positions on a trunk made
  of ≤ ℓ^{|N|} linear spines. This is a structural form of Wich Thm 4.3.
- (P) side-critical case: T8_poly holds whenever the critical SCC is not on the trunk (modulo the r10–r12 audit flag);
- the exact residual gap (§5).

Notation:
- G is reduced and cycle-free, with maximal RHS length ℓ.
- A loop is X ⇒⁺ αXβ, with α, β ∈ (N ∪ Σ)*.
- A pumping tree at X with terminal interface (U, V) is a derivation tree X ⇒* UXV with one designated X-leaf and
  every other leaf terminal.
- "C_exp-free" means am_G(n) = n^{O(1)}. By Wich DLT'99 Thm 4.4 this is the same as ¬C_exp.

## 0. G-struct ⟺ T8_poly [trivial, but it fixes the logic]
By Thm 4.4, polynomially ambiguous ⟺ ¬C_exp. So "every CFG with L ⊆ G⁻ rotation-dense satisfies C_exp" says exactly
that "no polynomially ambiguous CFG has a rotation-dense L ⊆ G⁻". That statement is T8_poly, and it contains T8_unamb.
So one cannot hope to *construct* the two pumping trees directly from G⁻ data. Any proof must be by contradiction:
assume ¬C_exp, derive the structure (§1–2), and refute density. §1–2 show what that structure is.

## 1. Two exponential-ambiguity criteria [written proof]
**Lemma IF (injective interfaces).** If some X has two distinct pumping trees t₁ ≠ t₂ with the same terminal interface
(U, V), then am_G(n) = 2^{Ω(n)}.

*Proof.*
1. Take a context S ⇒* sXt with s, t terminal and some X ⇒* w with w terminal. UV ≠ ε by cycle-freeness.
2. For each sequence (i₁, …, i_m) ∈ {1,2}^m, compose t_{i₁} ∘ ⋯ ∘ t_{i_m} and add the context and w. This gives a tree
   for s U^m w V^m t, a word of length O(m).
3. Two different sequences give different trees. At the first index where they differ, both trees contain
   t_{i_j}-tops whose designated X-leaves span the same interval of the word. Distinct nodes with the same span and the
   same label X would force X ⇒⁺ X, so the nodes coincide. The tree above a fixed node is then determined, which forces
   t₁ = t₂.
4. So the word has ≥ 2^m trees. ∎

**Lemma SU (side-unambiguity).** Let X ⇒⁺ αXβ be a loop and B a nonterminal occurring in α or β. If am_G(B, z) ≥ 2 for
some z, then am_G(n) = 2^{Ω(n)}. The same holds for every B′ reachable from such a B.

*Proof.*
1. Expand every other nonterminal of α and β to a fixed terminal word. Pump the loop m times, expand each of the m
   copies of B independently by one of the two trees for z, and close with X ⇒* w and the context.
2. All 2^m trees share the same skeleton, and their B-nodes have the same spans. They differ in the subtrees at those
   B-nodes, so they are distinct.
3. The word has length O(m).
4. Reachability: B ⇒* sB′t and am(B′, z′) ≥ 2 give am(B, s̄z′t̄) ≥ 2. ∎

**Corollaries for a C_exp-free G.**
- (a) Every nonterminal of a **nonlinear** SCC is unambiguous, because Y ⇒* αYβYγ puts Y on the side of its own loop.
  In particular Lemma Bot's Y and the whole heavy block containing it are unambiguous.
- (b) Every lower block of every SCC that has a loop is unambiguous. A C-rule with a C-child lies on a loop, so its other
  nonterminals are loop sides.
- (c) For every X, the map {pumping trees at X} → (U, V) is injective (IF). More generally, the same holds for
  X ⇒* UZV with X, Z in the same SCC: compose with Z ⇒* u′Xv′.

## 2. Trunk Lemma (TR) [written proof]
Let N_side be the set of nonterminals reachable from a loop side, and N_T := N \ N_side (the trunk).
- N_side is closed downward, so in every tree the N_T-labelled nodes form a top subtree.
- **Within one SCC, trunk nodes form a path.**
  - A nonlinear SCC lies entirely in N_side, by (a).
  - In a linear SCC C, every rule with a C-child has its other children in N_side, by (b).
  - So branching inside the trunk happens only at exit rules and trivial-SCC rules. Each of these occurs at most once
    per SCC level along any root path.
- Hence the trunk consists of at most K := ℓ^{|N|} maximal SCC-paths.
- **Given the spans of the trunk junction nodes** (entry and exit of each path), the whole tree is determined:
  - each spine is unique by (c);
  - each side subtree is unique by SU.

So am_G(w) ≤ #shapes · (n+1)^{2K}, which recovers Wich's n^{O(c)} bound. **All ambiguity of a C_exp-free grammar is
junction re-placement on ≤ K trunk spines.** This is r17_lift L1 restated without the Wich projection.
E*#E* (X → EX | Z, Z → EZ | ε) is the minimal instance: a trunk of two spines with one sliding junction.

**Consequence for the brief.** A "slide" means two trees of one word with different junction spans, and by TR that can
only happen on the trunk. The nonlinear branching of Lemma Bot is in N_side and is rigid (unambiguous). The MS⁺ flat
loops are pumping trees, and they are injective by IF. So the raw material of the brief (Bot, MS⁺, No-go 2 slides) can
produce C_exp only in a grammar that already has it. The No-go 2 slide (centre word recurring inside E-blocks) is
exactly a trunk-junction slide: its multiplicity ≤ 1 + occ_w(W) is linear, never exponential.

## 3. Prop P: side-critical case [written proof, modulo the r17_lift §1 audit flag]
Let C be the critical linear SCC supplied by Lemma F / Cor H, applied to the tree series. Suppose some X ∈ C is
unambiguous, for instance C ⊆ N_side (C hangs off any loop, or lies below any nonlinear SCC). Then the T8_unamb argument
applies verbatim to the polynomially ambiguous G, and L cannot be rotation-dense.
1. Fix (p, w, q).
2. W = p z q with |p|, |q| fixed determines z, the X-yield.
3. am(X, z) ≤ 1 then determines the X-subtree, and hence the token sequence. So the pair-family map is **injective**.
   This is the only use of unambiguity in PR2⁺ (r17_lift §1).
4. The lower blocks are unambiguous by (b). Radius ≥ ½ holds for poly-ambiguous tree series.
- *Caveat:* the one-sided closure (r17_oh_level / r17_oh_region) was not re-audited for uses of unambiguity other than
  pair injectivity.

## 4. F1 check
Nothing in §1–2 uses G⁻. They are grammar structure only. So G⁻ ∩ (Catalan-type sparse sets) is consistent with them:
those grammars are unambiguous trunk grammars with no slides. Density enters only in §3 (Cor H, PR2⁺) and in the
residual §5. By the r17_lift ceiling lemma it must enter there as a **set-level** fact, not as a count. Slide
multiplicity is ≤ 1 + occ_w(W) ≤ n per junction. Choosing a rarer centre w does not help: the pair mass and the
occurrence budget both scale by 2^{−|w|}, leaving N^{β₀} vs N(C+|w|)².

## 5. Exact remaining gap (G-struct ⟺ this)
**(G-trunk).** Let G be a C_exp-free grammar with L ⊆ G⁻ that is rotation-dense, and let the critical SCC C from Cor H
lie on the trunk with every X ∈ C ambiguous. Show a contradiction. Here all multiplicity is the slide of the C-exit
junction (and of ≤ K−1 further trunk junctions below or above). Equivalently: PR2⁺ with a pair map that is injective up
to centre re-placement. This is the same gap as r17_lift (G-word / junction loss). §1–3 show it is the *only* gap and
that it involves O(1) junctions, but it gives no tool to close it: by the ceiling lemma a polynomial slide budget defeats
every count squeeze.

## Status
| claim | label |
|---|---|
| G-struct ⟺ T8_poly | trivial (Wich Thm 4.4) |
| Lemma IF, Lemma SU, Cor (a)–(c) | written proof |
| Trunk Lemma: ambiguity = junction re-placement on ≤ ℓ^{\|N\|} spines | written proof |
| Brief's mechanism (repeat the slide via Y ⇒* αYβYγ) | **impossible**: Y is unambiguous in any C_exp-free G |
| Prop P: T8_poly when the critical SCC has an unambiguous nonterminal (e.g. C ⊆ N_side) | written proof modulo the r10–r12 / oh audit flag |
| G-struct / T8_poly in the trunk-critical case | **OPEN**: gap (G-trunk), §5 |
