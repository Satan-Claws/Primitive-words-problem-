# Registry: polynomial-ambiguity question for Q (primitive words over {a,b})

Target: decide whether there is a cycle-free G with L(G)=Q and amb_G(w) ≤ C|w|^k for all w (C,k constants of G).
Rules: entries ≤ few lines; always carry a status label; never paste report contents.

## Approach families (mechanism → status)
- structural (ring/laminar, PROOF.md §3 transfer): OPEN (agent P/C)
- restricted-class closure (T3: ring ⇒ finite-index/ultralinear/FR): BLOCKED (poly_T3.md)
- slice-ambiguity (T1: superpoly witnesses): OPEN (agent T1)
- partition-function (T2): WAITING on T1
- counting/analytic: BLOCKED (sandwich, §5); rectangles.md rate check: OPEN (agent WE)
- constructive (A/G): OPEN (agent AG)

## Facts recorded
- [root reading, assessment] PROOF.md §3(c) uses only that b-yields inside one block commute; the 2^N trees are for one word of length |w0|+O(N). No finite-ambiguity hypothesis used, so (c) holds under polynomial ambiguity on (ab*)^n slices. The Dyck caveat does not apply: both contexts insert only b's into fixed blocks s,t. (Agent P to confirm in one line.)

## Proved lemmas

## Blocked routes
- fixed-block-count slices; R_m alone; count sandwiches; non-CF of Q as intermediate goal.

## Tables

## Round syntheses
- [T3, REFUTED route] Poly (even un-)ambiguity forces no global restriction: D1·b (S→Tb, T→aTbT|ε) is unambiguous, branching, ⊆ Q, γ=2, ∉ FR (density.md Cor 2), infinite index (LITERATURE). See poly_T3.md.
- [T3] Branching A⇒*uAvAw ≠ exponential; exp ⇔ two distinct trees A⇒+uAv same (u,v) (Wich 2005, LITERATURE). "poly-amb G for Q ⇒ FR" is equivalent to the target (uses L⊇Q only); not a reduction.
