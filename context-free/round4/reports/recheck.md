# recheck: blocked/stalled routes vs. the hypothesis sup amb_G = ∞

Principle: a barrier of the form "language X (slice, product, image, CF subset) is CF / satisfies lemma Y"
is a statement about languages, hence independent of which grammar G for Q is assumed. Only barriers that
reason about a single tree or about counts of trees can change.

| Route | Barrier | Still applies under amb = ∞? | New leverage? |
|---|---|---|---|
| ogden (stalled) | Ceiling Thm B: L CF ⇔ every word has *one* tree with ≤ N labels whose rule set stays in L | Yes. B is a language-level equivalence; the hypothesis only adds trees, while B needs one | **Some.** By Wich's ambiguity classification, amb = ∞ forces a nonterminal A with two distinct derivations A ⇒* uAv, A ⇒* u′Av′ of equal combined yield, which can be interleaved (a free monoid of trees with the *same* yield). That is a cross-tree iteration principle, i.e. exactly the reopen condition. Does not by itself force a power |
| kk (stalled) | One-scale Dickson obstructions fail: Q ∩ (ab*)^n is covered by stratified linear sets | Yes. Semilinear/stratified covers are a language fact. Ambiguity of G restricted to a bounded slice can be bounded even if global amb = ∞ (ambiguity can sit outside the slice) | No |
| transduce (stalled) | T1 (equality languages are not images), T2 (bounded images reduce to KK), Prop D | Yes. Images of Q are fixed sets; no grammar enters | No |
| uniform / r6 (blocked) | gcd barrier: Q ∩ R = R ∩ coPow_d is CF; R6 Cover Lemma | The barrier still holds (language level). But the *route* assumed bounded ambiguity (it is the finite-ambiguity slice argument), so under amb = ∞ its premise fails and it gives nothing | Negative: the route is inapplicable, not strengthened |
| crossing (blocked) | Thm 1: Q CF ⇔ finitely many CF pairs with L_i·M_i ⊆ Q cover a conjugate of every primitive word | Yes. Proved from one tree per word; ambiguity-free | Slight: amb = ∞ yields infinitely many distinct (context, yield) splittings of the same words, i.e. many rectangles through one word, a fooling-set multiplicity. No mechanism links that to a power |
| periodic CL1–CL3 (refuted) | Explicit linear CF L ⊆ Q | Counterexample languages are *linear*, unambiguous or bounded ambiguous. They refute "every CFL ⊇ F contains a power" outright. They do **not** refute "every *infinitely ambiguous* CFG ⊇ F generates a power" | **Yes, formally.** CL1–CL3 reopen in the restricted form "every G with amb = ∞ and L(G) ⊇ F", but a grammar that is inf. ambiguous only on some unrelated part of Σ* (G ∪ G′) is still ⊆ Q, so the restriction is vacuous unless the ambiguity is localised on F. Net: no real gain |
| density (Q½ refuted; walk) | T^k(E′) is CF ⊆ Q with density ≍ n^{-2^{-(k+1)}} | Yes. A language fact; T is built from cyclic shift, which is itself inherently ambiguous, so the counterexamples are already ambiguous | No |
| analytic (running/stalled) | Supports of N-series = CFLs (circular); counting equivalence false (L1 has non-algebraic series) | Yes, and the counterexample L1 is inherently (infinitely) ambiguous, so the barrier was already in the amb = ∞ regime | **Some.** Under amb = ∞ the tree series Σ amb_G(w) w is N-algebraic and dominates 1_Q, with infinite excess. Pole data of the *tree-count* series, not Q's series, are constrained (algebraic, finitely many singularity moduli), but the excess hides Q's 2^{-1/p} poles. Usable only together with a bound on the excess |
| builder (positive) | n/a (not blocked) | — | — |

## Flags (genuine new leverage)
1. **ogden / multitree**: amb = ∞ gives (Wich-type) twin loops at one nonterminal with equal yields, hence
   a yield-preserving free monoid of trees. This is the "cross-tree/transplant" iteration principle that
   ogden and thue name as their reopen condition. Mechanism: swapping twin loops changes the tree but not
   the word, so it cannot directly produce a power; it is leverage only combined with a pump that does.
2. **analytic**: the N-algebraic tree-count series majorises 1_Q. A negative proof would need
   "excess = o(Q's p-pole contribution)", which the hypothesis does not supply.
Everything else is language-level and unchanged. No barrier silently assumed bounded ambiguity except
`uniform` (explicitly) and `ogden`'s use of a single tree (harmless: B needs only existence).
