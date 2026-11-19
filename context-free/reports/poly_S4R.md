# poly_S4R — bounded-entry support rank ("inner × outer" matrices): verdict DEAD

Session 4, mechanism "bounded-entry support rank". Read: rectangles.md §1–2 (and the
statement of Theorem B in §3).

## Setup
For a span (i,ℓ) let A_n(y,(x,z)) = #parse trees of xyz having a node of span (i,ℓ).
Amb ≤ C|w|^k gives A_n = Σ_{A∈V} O_A ⊗ I_A (nonnegative rank-1 terms, one per nonterminal),
so nonneg-rank(A_n) ≤ |V|, entries ∈ {0} ∪ [1, Cn^k], supp(A_n) ⊆ Q-pattern, and over the
≤ n² balanced spans every w ∈ Q_n is covered. The proposed route: show that every
nonnegative matrix with Q's 0-pattern and entries in [1, poly(n)] has rank n^{ω(1)}.

## Claim (PROVED, short)
The route is dead: Q itself has such a matrix, of nonnegative rank 2⌈n/3⌉ and
entries in [1, ⌈n/3⌉], with **exact** support Q. So no rank / nonneg-rank / support-rank /
sign-type bound on Q's pattern (or any sub-pattern) can exceed O(n).

*Proof.* Split L = ⌊2n/3⌋ | s = ⌈n/3⌉. Theorem A (rectangles.md §2): yz ∉ Q iff z = π(y)
(π partial). Take M = Σ_{j<s, c∈Σ} 1_{R_{j,c}}. Then
M(y,z) = d_H(z, π(y)) if π(y) defined, = s if π(y) = ⊥; so M(y,z) = 0 exactly off Q, and
1 ≤ M ≤ s on Q. M is a sum of 2s nonnegative rank-1 0/1 matrices. ∎
(Equivalently M = ‖φ(z) − φ(π(y))‖², the "(x_i − x_j)²" trick: rank ≤ s+2 over ℝ.)
By rotation (Cor. 2.4) the same holds at every span with ℓ ≤ ⌈n/3⌉ or ℓ ≥ ⌊2n/3⌋; for
middle spans, Theorem B (§3) gives a cover by ≤ ⌈2^k n ln 2⌉ affine sets, each splitting into
≤ 2^k rectangles across any cut (k = ω(n), 2^k ≤ n), so the multiplicity-sum is again a
nonneg-rank-poly(n), entries ≤ poly(n), exact-support matrix at **every** span simultaneously.

## Answers
(1) Yes, dead — not merely because Alon-type bounds are weak (Ω(log N / log C) with
N = 2^{Θ(n)} gives only Ω(n/ log n), matching the O(n) upper bound): the upper bound is
attained by an explicit bounded-multiplicity cover, so even the true value is Θ(n) (Prop. 2.8
lower bound ⌈n/3⌉ for even n is Boolean rank; real support rank is also ≤ s+2).
(2) No. Every submatrix inherits nonneg rank ≤ 2⌈n/3⌉ with entries in [1, n]; so no
Hadamard / inner-product sub-pattern with superpoly bounded-entry rank exists (Forster-type
bounds concern sign patterns of ±1 matrices; Q's pattern is "J minus ≤ ω(n) partial function
graphs", whose support rank is O(n^{O(1)}) by Hamming-distance products, and O(n) at the
canonical split). Any successful argument must use the coupling across spans / the tree
structure (consistency of the same node in many trees), not single-span matrices.

Status: PROVED (barrier). Mechanism closed.
