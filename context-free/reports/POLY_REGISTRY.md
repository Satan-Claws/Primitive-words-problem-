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
- [published, Wich DLT'99 Thm 3.18+4.3/4.4, Cor 6.1; read in full] Cycle-free G: am_G(n)=2^{Θ(n)} iff C_exp: ∃A, α,β∈(N∪Σ)* with am_G(A,αAβ)>1 (two distinct pumping trees A⇒+αAβ, same interface) and αAβ has no useless/ε-symbols; else am_G(n)=O(n^d), d effective; C_exp undecidable (Thm 5.2). Notes: poly_WE.md.
- [published, Wich MFCS'01 LNCS 2136:703–714, abstract verbatim] PCFL = closure of UCFL under projections deleting only Parikh-bounded symbols (a Parikh-bounded in L: ∃c, no word of L has >c a's); PCFL closed under Parikh-bounded substitution; closure of UCFL under ∪,· is PROPER subset of PCFL. Theorem no. unseen (Springer/thesis PDF blocked).
- [audited report, rectangles.md Thm 5.2 / redteam.md §1] only limsup e_G(n)^{1/n}>1 is proved; no exact rate. For poly-ambiguous G, e_G(n) ≤ C n^k 2^n trivially. BLOCKED: rate ≤ 2.
- [L, BLOCKED; Lemma O PROVED] Global pumping+Wich-collision lever: L_{r,s,±1}={r#a−s#b=±1} is DCFL ⊆ Q (gcd|1); finite unions are finitely ambiguous and contain x^p y high-power families, satisfy Ogden/L–S, avoid (a^nb^n)^2. So any lever with test words in such a union (or regular) yields no collision; must use non-Parikh-certified words, i.e. reduces to slice method (PROOF.md §3(c)). poly_L.md.
- [root, from Wich MFCS'01 abstract, published] Reformulation: Q has a poly-ambiguous grammar ⇔ Q = h(L), L ∈ UCFL over Σ∪Γ, every γ∈Γ Parikh-bounded in L (≤ c occurrences), h erases Γ. Splitting by marker pattern: Q = ∪_p {u_0⋯u_r : u_0γ_{p1}u_1⋯γ_{pr}u_r ∈ L_p}, finitely many unambiguous L_p, r ≤ c "cut points". Counting d_n = Σ_p F_p(z,1) stays inside the blocked sandwich; any use must exploit the marker variable t or the cut structure.
