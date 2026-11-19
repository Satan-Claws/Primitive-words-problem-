# Round 4 — agent "ogden": multi-pump / derivation-tree iteration

Scripts: `infinite-ambiguity/claude_round4-5_2026-11-18/scripts/ogden/` (`multipump.py`, `marked2.py`, `freeloops.py`, `tmtest.py`, `mu.py`, `mu_hard.py`).
I do **not** claim a proof of either resolution.

## 0. Summary

1. Two iteration theorems valid for every CFG are written out and proved: (A) k nested, independently iterable
   Ogden pumps; (A′) m loops at one nonterminal, iterable in any order (a free monoid of loops).
2. **Theorem B (exact ceiling of the method).** Q is CF iff there is N such that every primitive word has a
   binary derivation tree, internal labels in [N], whose rule grammar generates only primitive words. Every
   per-word iteration theorem (Ogden, Bader–Moura, A, A′, any multi-pump variant) is a consequence of
   "μ ≤ N". So the multi-pump route is a hierarchy of weakenings of this one statement.
3. **Where Q escapes.**
   - (C) In unary runs the defender (the side trying to keep Q CF) can choose all k loops to commute. The
     k-pump conclusion then collapses to a single pump with a deeper pump-down range.
   - (D) In cube-free (for example Thue–Morse) regions, commuting loops are provably unavailable once m ≥ 3,
     so A′ forces truly non-commutative iteration. Even so, exact search finds good non-commuting loops
     every time.
4. **Computation (EVIDENCE only).** Q satisfies the 2-nested, free-2, free-3 and free-4 versions in every case
   tested. The label-complexity μ(w) is ≤ 3 for all primitive w with |w| ≤ 8 (closure checked up to length 16).

## 1. Iteration theorems valid for all CFLs

Preliminaries:
- Let L be CF. Then L∖{ε} has a CNF grammar G with N nonterminals; the language is preserved, and only the
  language is used below.
- Pick a path from the root by always entering the child with more marked leaves. A path node is a *branch
  point* if both of its children have marked leaves.
- Standard fact: a node with i branch points at or below it on the path has ≤ 2^i marked leaves.

**Theorem A (k-nested Ogden).** PROVED. Let p_k = 2^{kN+1}. Let w ∈ L with a set D of marked positions,
|D| ≥ p_k. Then
w = s₀ v₁ s₁ v₂ ⋯ s_{k−1} v_k z x_k t_{k−1} ⋯ x₂ t₁ x₁ t₀
such that:
- (i) each v_j x_j contains a mark;
- (ii) v₁⋯x₁ contains ≤ p_k marks;
- (iii) for all (i₁,…,i_k) ∈ ℕ^k, s₀ v₁^{i₁} s₁ ⋯ v_k^{i_k} z x_k^{i_k} ⋯ t₁ x₁^{i₁} t₀ ∈ L.

*Proof.*
1. Every leaf-to-root path through marked leaves has ≥ log₂|D| ≥ kN+1 branch points along the chosen path.
2. Take the lowest kN+1 branch points and cut them into k consecutive groups of N+1 (top group first; one
   spare point).
3. By pigeonhole, group j contains two nodes with the same label A_j. Call the upper one α_j and the lower one
   β_j. Then A_j ⇒* v_j A_j x_j, and the side child of α_j carries a mark inside v_j or x_j. This gives (i).
4. Groups are disjoint segments of the path, so α_{j+1} lies in the subtree of β_j. Hence the loops are nested,
   which gives the stated factorisation.
5. α₁ has ≤ kN+1 branch points at or below it, so its subtree has ≤ p_k marks. This gives (ii).
6. Iterating loop j means replacing subtree(α_j) by the i_j-fold iterate (i_j = 0 means using subtree(β_j)).
   This leaves subtree(β_j) intact, and subtree(β_j) contains all loops j' > j. So the k operations commute.
   This gives (iii). ∎

**Theorem A′ (free loops at one nonterminal).** PROVED. Let q_m = 2^{mN+1}. Let w ∈ L with |D| ≥ q_m. Then there
are A and w = u v₁ v₂ ⋯ v_m z x_m ⋯ x₁ y such that:
- each v_j x_j contains a mark;
- v₁⋯x₁ has ≤ q_m marks;
- for every finite sequence c ∈ [m]*, u v_{c₁}⋯v_{c_r} z x_{c_r}⋯x_{c₁} y ∈ L.

*Proof.* mN+1 branch points carry some label at least m+1 times, at nodes γ₀ > γ₁ > ⋯ > γ_m. The segment
between γ_{j−1} and γ_j is a loop A ⇒* v_j A x_j. Each loop starts at a branch point, so its side child carries
a mark. Loops at the same nonterminal compose in any order, and the word is closed off by subtree(γ_m) = z. ∎

## 2. The ceiling: Theorem B

For a binary tree T yielding w, with internal nodes labelled in [N] (leaves are letters), let G_T be the
grammar whose rules are exactly the local rules X → c₁c₂ occurring in T (each c_i a label or a letter), with
start symbol the root label. Define μ_L(w) = min{N : ∃T, L(G_T) ⊆ L}.

**Theorem B.** PROVED. For L ⊆ Σ⁺: L is CF iff sup_{w∈L} μ_L(w) < ∞.

*Proof.*
- (⇒) Turn a CNF grammar for L into the form above, with N nonterminals, by substituting the terminal rules
  A → a into the parents. This preserves the language. A derivation tree of w then gives G_T ⊆ G, so
  L(G_T) ⊆ L.
- (⇐) Over [N] there are only finitely many such grammars, since a rule set is a subset of a finite set. Each
  word lies in L(G_T) ⊆ L for one of them. So L is a finite union of CFLs. ∎

*Consequences.*
- Ogden, Bader–Moura, the interchange lemma restricted to one word, and Theorems A and A′ only use a bounded
  part of L(G_T): finitely many ancestor/descendant loops of T.
- A refutation of Q by derivation-tree iteration must establish, for every N, a primitive word all of whose
  N-labelled trees have a non-primitive word in a specified finite sub-closure.
- **Hierarchy of targets**, each implying "Q not CF":
  - "Q fails A (some k)";
  - "Q fails A′ (some m)";
  - MP: "ancestor-pumping closure unbounded", where the ancestor-pumping closure is the set of words obtained
    by repeatedly iterating or deleting loops between same-label ancestor/descendant pairs of the current
    tree;
  - "μ_Q unbounded", which is ⇔ Q not CF.

**Computation (COMPUTER-CHECKED, `mu.py`, `mu_hard.py`).** Closures were truncated at length |w|+8, so these
numbers are evidence about the truncated closure only.
- Over words starting with a, the counts of primitive words by μ are:
  - n = 4: {1: 5, 2: 1};
  - n = 5: {1: 7, 2: 8};
  - n = 6: {1: 9, 2: 18};
  - n = 7: {1: 11, 2: 52};
  - n = 8: {1: 13, 2: 103, 3: 4}.
- The four n = 8 words needing 3 labels are aabaaaab, aabaabaa, abaaaaba and abbbbabb. Their witnesses are
  mostly right-comb trees with a mod-3 labelling, so the closures are regular sublanguages of Q.
- No growth signal is visible at these lengths, and none is expected: comb-tree witnesses give regular
  sublanguages, which need unboundedly many labels only at large n.

## 3. Where Q escapes the multi-pump theorems

**Proposition C (commuting collapse).** PROVED. Suppose that in Theorem A:
- the factors v₁, s₁, …, v_k all lie in one run a^M;
- x_k, t_{k−1}, …, x₁ all lie in one run a^{M′} (or are all empty);
- |x_j| = ρ|v_j| for one fixed ρ ∈ {0, 1}.

Then the pumped word depends only on S = Σ_j |v_j|(i_j − 1). It equals w with the two runs changed to
M + S and M′ + ρS.

So the k-pump family is the single "run pump" family with shifts S ∈ gℤ ∩ [−Σ|v_j|, ∞), where
g = gcd|v_j|. The same holds when a is replaced by any primitive c and the runs by c-periodic factors.

*Consequence.* At every (w, D) where the defender has a run pump that is safe for all shifts S ≥ −kℓ, Q meets
Theorem A for that k. Examples are an equal-length partner pump (ρ = 1) across two long runs (Lemma 8.6 /
Thm 8.5 of the campaign findings), or a one-sided pump in a run whose unique bad length lies outside the
reachable shifts.

*Example (PROVED).* Take near-powers (aᵐb)^{K−1}a^{m+δ}b with marks on the defect block, and k equal-length
partner loops (a^ℓ in an unmarked block r, a^ℓ in the defect block).
- Block r becomes m+S and the defect becomes m+δ+S.
- These are never equal, since δ ≠ 0, and at most one of them equals m.
- So the run sequence has one or two singleton values, and is not periodic for K ≥ 3. All pumpings are
  primitive.
- Near-powers therefore give no leverage for A or A′. Whole-period loops (aᵐb)^j are also always safe.

**Proposition D (cube-free regions force non-commuting loops).** PROVED. Suppose v₁, …, v_m are adjacent,
nonempty and pairwise commuting. Commutation of nonempty words means they are powers of one primitive c, so
v₁⋯v_m = c^e with e ≥ m.

Hence suppose the marks of Theorem A′ lie in a cube-free factor (for example a Thue–Morse factor), and every
loop meets the marks on its left side, so all v_j ≠ ε. Then for m ≥ 3 the loops cannot all commute: A′ forces
a genuinely non-commutative family {u σ z y : σ ∈ ⟨v₁,…,v_m⟩}. This is the only regime where A′ is
strictly stronger than single-pump Ogden in the defender's eyes.

**Computation (COMPUTER-CHECKED; the infinite exponent and sequence ranges are truncated, so EVIDENCE).**

| Test | Range | Result |
|---|---|---|
| NEST2, full marking, (i,j) ∈ [0,4]² | n ≤ 12 | window ≤ 3 always suffices |
| FREE2 (sequences of length ≤ 4) | n ≤ 11 | same |
| NEST2, marks = every interval of length 3 | n ≤ 10 | ≤ 3 marks in the window always suffice |
| FREE3, marks = every interval of length 4, sequences ≤ 3 | n = 7, 8, 9 | always satisfied with ≤ 4 marks |
| FREE3 and FREE4, sequences ≤ 3 and ≤ 4 | Thue–Morse prefixes of length 12–32, marks = 8-intervals | satisfied with window mark count exactly m |

- For FREE3 at n = 6, the two failures (aababa, D = [2,6)) are within the Ogden constant, not
  counterexamples.
- In the Thue–Morse tests the defender used non-commuting loops, for example (x₄,x₃,x₂,x₁) =
  (abb, a, b, a) in TM₂₀–TM₃₂.

**Diagnosis.**
- In every iteration theorem of the form "∀w ∀D ∃ loops …", the defender picks the loops after seeing w.
- In runs it picks commuting loops (C). In aperiodic regions it picks short loops with fresh conjugates.
  Campaign Lemma U makes positive exponents safe, and deletions are finitely many and avoidable by choice of
  position. Free products of fresh loops behave the same way (evidence above).
- What would bite is a loop being *forced* to be inserted into a context where it creates a period. That is
  cross-word or cross-paste information, which only the full closure L(G_T), or several words sharing
  nonterminals, carries. Theorem B shows that using all of it is exactly the original problem.

## 4. Registry entry

1. **Exact statement aimed at.** For some k (or m), Q violates Theorem A (k nested independent Ogden pumps)
   or Theorem A′ (m free loops at one nonterminal). Either would give "Q not CF".
2. **Strongest lemma actually proved.**
   - Theorems A and A′, valid for every CFL.
   - Theorem B: Q is CF ⇔ μ_Q is bounded, so per-word tree iteration has exactly this ceiling.
   - Proposition C: commuting collapse of multi-pumps inside runs to one shifted run pump. The near-power
     family is safe for all k.
   - Proposition D: in cube-free marked regions, m ≥ 3 loops at one nonterminal cannot commute.
3. **Missing step (precise).** ∃m ∀p ∃ primitive w and marks D with |D| ≥ p such that for every factorisation
   w = u v₁⋯v_m z x_m⋯x₁ y with each v_j x_j meeting D and ≤ p marks in v₁⋯x₁, some c ∈ [m]* makes
   u v_{c₁}⋯v_{c_r} z x_{c_r}⋯x_{c₁} y non-primitive. The k-nested commutative analogue is the same with
   independent exponents.
4. **Counterexamples found.** None to Q satisfying A or A′. All tested cases satisfy them (§3 table). The
   evidence indicates that the missing step is **false**, as OG(Q) was.
5. **Strength relative to "Q not CF".** The missing step for A or A′ is **stronger** than "Q not CF": it
   implies it, and Theorem B shows that bounded-loop conclusions are strict weakenings of CF-ness. MP is
   stronger than or equal to "Q not CF"; only "μ_Q unbounded" is equivalent.
6. **What would reopen the route.**
   - (a) A witness family in which the marked region is cube-free *and* has no reachable partner run within
     the window, and in which the free monoid ⟨v₁,…,v_m⟩ provably always contains a "repair" word making
     u σ z y a power. Words of the form B^N·(B with a deletion) with B Thue–Morse-like are the natural
     candidates, but the defender chooses the loops away from the repair site.
   - (b) An iteration theorem with cross-word content strictly between A′ and Theorem B, for example forced
     transplantation of a loop into every other occurrence of its nonterminal across a pigeonholed family,
     with a family designed so that some occurrence sits in a context where the loop creates a period.
     Bounded slices are CF (campaign §9), so such a family must use an unbounded number of blocks.
