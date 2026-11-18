# multitree: can many trees of one word force a power? — NO (structural obstruction)

## Claim (negative / barrier)
Recombination of distinct parse trees of a single word never produces anything outside the set
C(A)·L(A) of single-grammar context substitutions, hence never anything outside L(G).
So unbounded ambiguity *as such* cannot force L(G) ⊄ Q; any argument must use language-level
structure (that L(G) ⊇ some specific family), not the multiplicity of trees.

## Lemma 1 (recombination is closed)
Let T1, T2 be trees of w, node v1∈T1 labelled A spanning w[i,j), node v2∈T2 labelled A spanning w[k,l).
Grafting T2|v2 into T1 at v1 gives a tree of w[0,i)·w[k,l)·w[j,n). This is the context of v1 in T1
applied to an element of L(A): exactly a single-tree substitution with a yield from another tree.
Mixing pump pairs (x,y) from T1 with (x',y') from T2: each pump pair is (context fragment of A ⇒* xAy);
inserting both produces derivations S ⇒* uAv ⇒* u x A y v ⇒* … all of which are ordinary derivations
of G. Every recombined object is a parse tree of G, so its yield is in L(G). ∎ (trivial, but decisive)

## Counterexample (unboundedly ambiguous, cycle-free CNF, L ⊆ Q)
S → A B, A → a, B → B B | b.  L(G) = a b^+ ⊆ Q (one a ⇒ primitive). amb(a b^n) = Catalan(n-1) → ∞.
All recombinations (swap B-subtrees across spans, combine B ⇒* b^p B b^q pumps from different trees)
yield a b^m, m ≥ 1: always primitive. Isolating why: the ambiguity lives entirely in a sub-language
(L(B)=b^+) whose contexts all carry a fixed primitive-forcing letter count (|w|_a = 1); trees differ
only in bracketing, not in which letters each nonterminal can emit.
More generally, for any CF L ⊆ Q and any grammar H for it, adding a padded ambiguous copy
(e.g. duplicate nonterminals X, X' with identical rules) makes amb unbounded without changing L.
So "ambiguity ⇒ power" is false for languages ⊆ Q in general; it can only bite for L(G)=Q, where the
finite-ambiguity proof already shows ambiguity is necessary but not sufficient as a contradiction.

## Gap
What remains: use that a grammar for Q must have ambiguity *growing* on specific slices
(finitely-ambiguous/PROOF.md slices), and show the nonterminals carrying that ambiguity have
contexts × yields that cover a power. That is a language-level statement about L(A)'s and C(A)'s,
not a tree-recombination statement; tree multiplicity adds no information beyond {C(A), L(A)}.
