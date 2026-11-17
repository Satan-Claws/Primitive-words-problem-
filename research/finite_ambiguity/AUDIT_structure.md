# Audit of PROOF.md §2 (reductions) and §3 (Structure Lemma 3)

**Verdict: CORRECT WITH FIXES.** All the fixes are local. I found no counterexample. The
mathematical content of Lemma 3 holds: the structural conclusions (a)–(c), the bijection between
trees and pairs (σ, q), finiteness of the skeletons, independence and laminarity. Four places need
an added sentence or a changed definition (F1–F4 below). None of them affects §4–§5.

## Step-by-step check

**§2, Lemma 1.1 (CNF).** Correct. Each step comes with a yield-preserving injection from new trees
to old trees:
* ε-removal: re-insert fixed ε-trees, delete the subtrees with empty yield to recover the tree.
* Unit removal: canonical chains, inverted by contracting maximal unit chains.
* Binarisation: a bijection.

The proof only needs d_G(w) < ∞, which is weaker than cycle-free. A unit cycle in G′ would give
infinitely many G′-trees and so, through the injection, infinitely many G-trees. That is why G′ has
no unit cycle.

**§2, Lemma 1.2 (DFA product).** Correct. Annotations are forced by the positions, so G-trees and
G_D-trees are in bijection. Merging the start symbols (s₀,S,f) is harmless because only
f = δ(s₀,w) carries trees. Reducing the grammar does not change any tree of a word.

**(a), Steps 1–2 of Theorem A.** Correct.
* Step 1: different Catalan arrangements are different trees. At the first address where two
  arrangements differ, one subtree has yield length ≥ |uvz| + 2|w| > |w| and the other has yield
  length |w|.
* Step 2: pumping the cycle X ⇒⁺ αXβZ forces L(Z) ⊆ b⁺.
* With the DFA D_n, a b-only Z is annotated (t,Z,t), so the annotation is constant on C.
  See F1 for the interface with §2.

**(b).** Correct. A C-node below any non-C child Y of a C-node would put Y in C. So:
* the C-nodes of a tree form disjoint contiguous chains;
* nothing below an exit node is in C.

**(c), unique first-return context.** Correct. The construction with ε ∈ {12,21}^N balances the
inserted b's, so it works even when κ₁ and κ₂ have *different* yields. The tree determines ε: the
address of the top inserted X is fixed by `outer`. The C-chain below it is unique by (b). The hole
of κ_{ε_i} is the first X on that chain below its root. X-nodes inside T_X are irrelevant, because
only the first 2N returns are read.

This gives the following consequences.
* Each X ∈ C has exactly one rule with a child in C. For each such rule there is a first-return
  context that starts with it: follow a shortest C-path from the child back to X, so that it avoids
  X, and fill the side positions with any trees (all symbols are useful).
* Every X ∈ C therefore has out-degree 1 inside C. A strongly connected functional graph is a
  single cycle, so C is a simple ring.
* Each side child Z has exactly one tree *in total*, over all words. Two trees of Z, even of
  different words, give two first-return contexts.

**(d), skeletons.** Correct.
* The ring is deterministic: each X_i has one ring rule, and each side child has one fixed tree. So
  a maximal C-chain is determined by its entry X_i, its length and the exit subtree.
* Removing or inserting q full turns is therefore well defined, and the map (σ,q) ↔ tree is a
  bijection.
* Turns are removed independently on nested chains. An inner chain lies in the exit subtree of the
  outer one, and that subtree is untouched.
* In a skeleton no root-to-leaf path repeats a nonterminal. A repeat would put all nodes between the
  two occurrences in one nontrivial SCC. Such a repeat is impossible in three places:
  * inside a side subtree (see F3);
  * between different SCCs, because an SCC is never re-entered;
  * inside a ring, because a skeleton chain has fewer than r steps.
* Hence depth ≤ |N| and there are finitely many skeletons.

**(e), independence.** Correct. Split an integer dependence into q ≠ q′ ∈ ℕ^r. The points
jq + (K−j)q′, j = 0..K, are distinct and have the same yield. So the parametrisation is injective
and amb(w) = Σ_σ 1[exp w ∈ L_σ].

Two C-paths of the *same* SCC in one skeleton are only possible when s = t. Disjoint factors that
both span states s < t would each contain t−s a's, which is impossible. When s = t the two paths
give equal vectors, so (e) excludes them. Two *different* SCCs with the same pair, one nested
inside the other, are possible and allowed (example `nested_same_pair` below).

**(f), laminarity.** Correct. The argument is the interval argument on states: either the
intervals are nested, [s′,t′] ⊆ [s,t], or they are disjoint, t ≤ s′ or t′ ≤ s. Neither case is a
crossing. The justification for "π′ is not in a side subtree" needs F3.

## Gaps and fixes

**F1 (interface §2 → Lemma 3).**
* The problem: §2 builds G_m as a product with a DFA for R_m, but Lemma 3 assumes the annotation by
  D_n. With the natural DFA of R_m, whose states are (number of a's, "a b has been seen"), a b-only
  Z can be annotated ((i,0),Z,(i,1)). So the sentence "Z's annotation is (t,Z,t)" in Theorem A,
  Step 2 is D_n-specific.
* Fix: apply Lemma 1.2 a second time and take G_m := (G″ × D_{R_m}) × D_n, reduced. Tree counts
  are preserved, L(G_m) = Q ∩ R_m ⊆ (ab*)^n, and Lemma 3 then applies verbatim.
* Alternative: use any DFA that refines D_n. The annotation along a ring is then monotone, so it is
  constant.

**F2 (pairs may contain 0).**
* The problem: for a ring with only right side children, s can be 0, so the "pair" {0,t} ⊄ [n].
  Example: S → S b | a with n = 1 gives the pair {0,1}; case `s_zero` below.
* Fix: put π := {s,t} when s ≥ 1, and π := {t} when s = 0. Then supp v ⊆ {t} (a left side child
  would read b in state 0, which goes to the sink).
* Laminarity survives, because shrinking pairs never creates a crossing. §5 uses only the supports
  in any case.

**F3 (side subtrees contain no nontrivial SCC).**
* The problem: (f) says side subtrees have "no cycles by (c)". But "no repeated nonterminal on a
  path" does not, by itself, rule out a node W of a nontrivial SCC C′ that sits on a chain with 0
  turns.
* Fix: add the sentence "if a side child Z's unique tree contained a node W of a nontrivial C′,
  inserting a turn of C′ at W would give a second tree of Z, contradicting (c)."
* The same sentence is needed in (d), for "side subtrees are fixed and repetition-free".

**F4 (wording in (c)).** Say explicitly that a first-return context exists for *each* ring rule,
via a shortest C-path from the child back to X (see the (c) paragraph above). Also say that
"exactly one tree" for a side child means over all words. Both facts are already supplied by the
2^N argument, so this is only a matter of stating them.

Points that are not gaps:
* The statement allows repeated or nested equal pairs inside one skeleton.
* Lemma 4.1 and Lemma 4.2 work with multigraphs, so §5 is unaffected.

## Computer checks (`audit_struct/`)

`struct_check.py` does the following for a grammar G and a number of blocks n:
* builds G × D_n and reduces it;
* tests the conclusions of (a)–(c): linear SCCs, rings, and side children with exactly one tree
  and no nontrivial SCC below;
* if they hold, enumerates the skeletons exactly as in (d), tests independence (e) and laminarity
  (f), and compares Σ_σ 1[exp w ∈ L_σ] with a CYK tree count for every word with blocks ≤ B;
* if they fail, Lemma 3 predicts infinite ambiguity, and the script checks that the maximum tree
  count grows with B.

Two random runs (`run_random.py`, `run_random2.py`, CNF grammars with 3–7 nonterminals,
n = 2, 3, 4):

| run | seed | grammars | structure ok | independent | ≥ 2 periods | ≥ 2 distinct 2-pairs | max amb ≥ 2 | laminarity / formula failures |
|---|---|---|---|---|---|---|---|---|
| `run_random.py` | 1 | 2000 | 335 | 289 | 28 | not recorded | 106 | **0** |
| `run_random2.py` | 3 | 3000 | 592 | 496 | 89 | 87 | not recorded | **0** |

Further runs of `run_random.py`:
* seed 7 (2000 grammars): 325 independent, 0 failures;
* seed 11 (2000 grammars): 302 independent, 0 failures.

Grammars that fail the structural conclusions are labelled by the first test that fails:
* nonlinear SCC;
* two ring rules;
* a side child with ≥ 2 trees or a nontrivial SCC below it.

For all of them the maximum tree count grows with B. The few plateaus between consecutive B are
parity steps. For example, one "two ring rules" grammar gives maxima
0, 0, 3, 15, 186, 2124, 33168, 270487, 2399418 for B = 1, 4, …, 25.

`handmade.py` checks finitely ambiguous grammars converted to CNF. The formula is exact and the
family laminar in every case:

| grammar | language | max amb | skeletons |
|---|---|---|---|
| `L3_2amb` | {x₁≠x₂} ∪ {x₂≠x₃}, n = 3 | 2 | 4 |
| `three_way` | adds {x₁≠x₃}, a nested pair {1,3}, n = 3 | 3 | 8 |
| `nested_same_pair` | a b^{p+q} a b^p, periods (1,1) and (1,0) on the same pair {1,2} | 1 | 2 |
| `two_disjoint` | a b^i a b^i a b^j a b^j | 1 | 1 |
| `s_zero` | S → Sb \| a, pair {0,1}, the F2 case | 1 | 1 |

All of these report 0 dependent skeletons, 0 crossing pairs and 0 mismatches.
