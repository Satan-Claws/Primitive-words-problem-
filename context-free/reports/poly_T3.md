# poly_T3: does polynomial ambiguity force a global restriction (finite index / FR)?

Status: REFUTED as a route (counterexample PROVED; one ingredient LITERATURE).

## Claim
There is an unambiguous (amb = 1) cycle-free grammar with a branching self-embedding whose language
L lies inside Q, has growth rate 2, is not in FR, and is not of finite index. Hence no implication
"poly-ambiguous (even unambiguous) ⇒ finite index / ultralinear / metalinear / FR" holds, not even
for languages contained in Q.

## Counterexample
L = D1·b, where D1 = Dyck language over a = "(", b = ")".
Grammar: S → T b, T → a T b T | ε (CNF conversion keeps it unambiguous and cycle-free).
- Unambiguous: standard (first-return decomposition of a Dyck word is unique). PROVED.
- Branching self-embedding: T ⇒ aTbT, i.e. T ⇒* uTvTw with u=a, v=b, w=ε. PROVED.
- L ⊆ Q: every w ∈ L has |w|_b − |w|_a = 1; if w = u^k then k·(|u|_b−|u|_a) = 1, so k = 1. PROVED.
- γ(L) = 2: |L_{2m+1}| = Catalan(m) ~ 4^m / (m^{3/2}√π). PROVED.
- L ∉ FR: density.md Corollary 2 (FR-languages inside Q have γ < 2). PROVED.
- L not of finite index: D1 has infinite index (Salomaa/Gruska, LITERATURE, not re-checked);
  finite-index languages form a full AFL, so closed under right quotient by b; D1 = L/b. LITERATURE.

## Why branching is not the exponential mechanism
For cycle-free reduced G, exponential ambiguity is equivalent to some A having two distinct derivation
trees A ⇒+ uAv with the same (u,v) (Wich 2005, LITERATURE). A branching self-embedding gives no such
pair (D1 example). The PROOF.md §3(c) ring property on (ab*)^n slices is exactly a local instance of the
negation of Wich's criterion; it does not lift to a global index/rate bound.

## Q-specific variant
Any lemma using only "L(G) ⊆ Q, γ(L(G)) = 2, amb polynomial" is refuted by D1·b. A Q-specific proof of
"poly-amb G with L(G) = Q ⇒ L(G) ∈ FR (or finite index)" would, since Q ∉ FR (density.md) — and
finite index for Q is OPEN (finiteindex.md) — be equivalent to (FR case) the target itself: it must
use the superset direction L(G) ⊇ Q (the exact complement structure), not structure of G. Not a reduction.
