# poly_S4W: forcing Wich Cor 3.20 / 3.21 (weaker than same-interface collision) — status: BLOCKED on fixed slices (obstruction PROVED); global version OPEN (= original problem or stronger)

Inputs: poly_WE.md (Wich DLT'99: Cor 3.20 ⇒ C_exp; Cor 3.21; Thm 4.4: exp-ambiguous ⇔ C_exp, else polynomial),
poly_L.md (Lemma O), finitely-ambiguous/PROOF.md §6 ("∃ i: x_i ≠ y_i" grammar, ply m−1) and §7 G1 (non-interleaving).

## 1. The test slice R = a^+b^+a^+b^+ (PROVED)
a^i b^j a^k b^l (all ≥1) is non-primitive iff it is a square, iff (i,j) = (k,l) (a cube or higher power
would need ≥ 3 a-blocks). So Q ∩ R = {i ≠ k} ∪ {j ≠ l} = L1 ∪ L2 with
  L1: S1 → T B,  T → aTa | A D | D A,  D → bD | b,  A → aA | a,  B → bB | b  (a^i b^+ a^k, i≠k);
  L2: S2 → A U,  U → bUb | C E | E C,  E → aE | a,  C → bC | b  (b^j a^+ b^l, j≠l).
Each piece is unambiguous, so H = G1 ∪ G2 has ambiguity ≤ 2 on Q ∩ R. Note: {i = k, j ≠ l} is NOT CF
(crossing), so the 2-piece overlap on {i≠k, j≠l} is unavoidable for this decomposition; it is still finite.

## 2. Exactly where the Cor 3.20 attempt fails (PROVED)
(a) Crossing. Ogden on a^N b^M a^N b^{M+1} (mark block 1/3) and a^{N+1} b^M a^N b^M (mark blocks 2/4) gives a
pumping node whose yield is a^x b^j a^y (interface (a^p, a^q)) resp. b^x a^k b^y (interface (b^r, b^s)).
These intervals interleave, so in ONE tree neither node is an ancestor of the other; nothing forces the
same nonterminal to carry both loops in different trees — and H realises them at distinct nonterminals
(T in G1, U in G2). (Same non-interleaving fact as finitely-ambiguous/PROOF.md §7 G1.)
(b) Ratios are forced EQUAL, not non-proportional. If a loop A ⇒ a^p A a^q (block-1/3 span) occurs in a
tree of a word with j = l, then p = q: otherwise pumping reaches i = k, giving (a^i b^j)^2 ∉ Q. So
primitivity pins the (block1, block3) ratio to 1:1 (and (block2, block4) to 1:1). Cor 3.20 needs
lm ≠ kn with common α,β; with α = a, β = a all forced interfaces are (a^p, a^p) — proportional. Mixed
α = a, β = b loops (a^p, b^q) can only span blocks 1→2 or 3→4 and are not forced (H has none with both sides
non-empty at a recursive nonterminal; A, B, C are one-sided, so Cor 3.21 also fails: no nonterminal is both
left- and right-recursive).
(c) General obstruction (slice transfer). Any argument whose inputs are: G ⊇ W, L(G) ⊆ Q, W ⊆ Q ∩ R for a
bounded regular R, Ogden/pumping on W, is satisfied verbatim by a polynomially (indeed finitely,
ply m−1) ambiguous grammar for Q ∩ R (PROOF.md §6). By Wich Thm 4.4 that grammar violates C_exp, hence has
no Cor 3.20 pair and no Cor 3.21 nonterminal. So no fixed-slice argument can force Cor 3.20/3.21. ∎

## 3. Growing block counts (OPEN, with reduction)
- Cor 3.20 ⇒ C_exp ⇔ exponential ambiguity (Thm 4.4). So "every cycle-free G for Q has a Cor 3.20 pair or a
  Cor 3.21 nonterminal" IMPLIES "Q is not polynomially ambiguous" — it is at least as strong as the negative
  resolution, not a weaker route; it adds only a concrete target shape.
- Across slices R_m with m → ∞ the per-slice grammars do not glue (unbounded #pieces), so 2(c) does not
  exclude a global argument; but any such argument must use words outside every single bounded slice
  (unbounded number of blocks in ONE derivation) — the same caveat as poly_L.md's last line. Natural
  candidate: a nonterminal deriving (ab^x)-block sequences with loops (u^k, v^l), (u^m, v^n) where u,v are
  block-words; 2(b) suggests primitivity again forces proportional ratios whenever the loop spans
  "matching" positions, so a forcing argument would need loops spanning NON-matching positions, which
  L(G) ⊆ Q does not constrain. No mechanism found.
Verdict: fixed-slice Cor 3.20/3.21 forcing BLOCKED (PROVED obstruction); global version OPEN, ≥ original problem.
