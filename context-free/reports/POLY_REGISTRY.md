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
- [P, PROVED] §3(c),(d),(f) hold under poly amb (2^N trees on length O(N)); only (e) fails. Lemma 3P: amb(w)=Σ_σ P_σ(exp w−c_σ), P_σ = vector partition fn of laminar list V_σ; growth t^{d_F} on relint F, d_σ=#V_σ−rank V_σ ≤ k for all σ, all m. poly_P.md §1–2.
- [P, PROVED] §5 cases 1–4 survive for supports c_σ+ℕV_σ (non-free monoids; facts Lat+Deep, Lemma X on face F∋(ω,ω)): some w∈Q∩R_m has amb ≥ ⌈m/2⌉; |w| uncontrolled, ≤ |w|/8 at best; capped by inherent amb(Q∩R_m) ≤ m−1 (=R_m-alone BLOCK). poly_P.md §3.
- [P, OPEN] superlinear needs multi-period slices (∪_{d|n}Δ_d) + effective cover-ply lemma at ‖exp‖₁=poly(n); partition degree can't help (d_σ≤k). poly_P.md §4.

## Blocked routes
- fixed-block-count slices; R_m alone; count sandwiches; non-CF of Q as intermediate goal.

## Tables
- [AG, computational] walk.md/builder3.md not found anywhere; substitutes coPow_2 / length-dispatch: L Δ Q starts aaa / ababab, max amb linear (n/2, 2n/3). poly_AG.md
| Q_n=(ab*)^n witness grammar | p^h | 6 | 10 | 12 | 15 |
|---|---|---|---|---|---|
| uncovered (adj, V=2) / max amb | 0 / n−n/p | 27(all) / 0 | 21 / 14 | 240 / 7 | 39 / 52 |
- [AG] Witness-union breaks on coverage, not on ambiguity: with ≥2 primes, single-defect words always need shared-endpoint (3-way) comparisons.

## Round syntheses
- [T3, REFUTED route] Poly (even un-)ambiguity forces no global restriction: D1·b (S→Tb, T→aTbT|ε) is unambiguous, branching, ⊆ Q, γ=2, ∉ FR (density.md Cor 2), infinite index (LITERATURE). See poly_T3.md.
- [T3] Branching A⇒*uAvAw ≠ exponential; exp ⇔ two distinct trees A⇒+uAv same (u,v) (Wich 2005, LITERATURE). "poly-amb G for Q ⇒ FR" is equivalent to the target (uses L⊇Q only); not a reduction.
- [published, Wich DLT'99 Thm 3.18+4.3/4.4, Cor 6.1; read in full] Cycle-free G: am_G(n)=2^{Θ(n)} iff C_exp: ∃A, α,β∈(N∪Σ)* with am_G(A,αAβ)>1 (two distinct pumping trees A⇒+αAβ, same interface) and αAβ has no useless/ε-symbols; else am_G(n)=O(n^d), d effective; C_exp undecidable (Thm 5.2). Notes: poly_WE.md.
- [published, Wich MFCS'01 LNCS 2136:703–714, abstract verbatim] PCFL = closure of UCFL under projections deleting only Parikh-bounded symbols (a Parikh-bounded in L: ∃c, no word of L has >c a's); PCFL closed under Parikh-bounded substitution; closure of UCFL under ∪,· is PROPER subset of PCFL. Theorem no. unseen (Springer/thesis PDF blocked).
- [audited report, rectangles.md Thm 5.2 / redteam.md §1] only limsup e_G(n)^{1/n}>1 is proved; no exact rate. For poly-ambiguous G, e_G(n) ≤ C n^k 2^n trivially. BLOCKED: rate ≤ 2.
- [L, BLOCKED; Lemma O PROVED] Global pumping+Wich-collision lever: L_{r,s,±1}={r#a−s#b=±1} is DCFL ⊆ Q (gcd|1); finite unions are finitely ambiguous and contain x^p y high-power families, satisfy Ogden/L–S, avoid (a^nb^n)^2. So any lever with test words in such a union (or regular) yields no collision; must use non-Parikh-certified words, i.e. reduces to slice method (PROOF.md §3(c)). poly_L.md.
- [root, from Wich MFCS'01 abstract, published] Reformulation: Q has a poly-ambiguous grammar ⇔ Q = h(L), L ∈ UCFL over Σ∪Γ, every γ∈Γ Parikh-bounded in L (≤ c occurrences), h erases Γ. Splitting by marker pattern: Q = ∪_p {u_0⋯u_r : u_0γ_{p1}u_1⋯γ_{pr}u_r ∈ L_p}, finitely many unambiguous L_p, r ≤ c "cut points". Counting d_n = Σ_p F_p(z,1) stays inside the blocked sandwich; any use must exploit the marker variable t or the cut structure.
- [M, PROVED] GF(Q∩(ab⁺)*) = Σ μ(d)·z^{2d}/(1−z^d−z^{2d}) not algebraic (poles |z|=φ^{-1/d}, distinct d). Lemma M2: for any Q=h(L) and any R with non-algebraic GF(Q∩R), amb(w)≥2 for infinitely many w∈Q∩R (else Σ amb·z^{|w|} algebraic). poly_M.md.
- [M, BLOCKED] Wich route (i) "forced unique cut placement + inclusion–exclusion": uniqueness refuted by M2 exactly where transcendence holds; ∩ of PCFLs not CF; P=1 WLOG (disjoint marker alphabets), marker-count t is t^r; residue = sandwich. Only open residue: cut-POSITION variable B_R(z,t) (algebraic), needs structural input.
- [T1] PROVED: off-W_n part of any slice has amb ≤ φ(n); prime-power n slices linear; nested R_m gives L^{<1}; (ab+abb)^* slice = h(Q), so "all slices poly" ⇔ main target (T1-impossibility not separately provable).
- [T1] PROVED: conjunctive (product) configs ⊕E_k have ∏dim = (n/rad n)^{ω(n)}φ(rad n): ≤ n for squarefree n (primorial idea BLOCKED), ≥ n^{N/2} for n = P_N².
- [T1] CONJECTURED candidate: S_N=(ab*)^{P_N²}, amb ≥ ∏(d_k+1)/2^N; gaps G1 (product ply lemma), G2 (Lemma X for classes >2), G3 (length/T2). No upper grammar. See poly_T1.md.

### Round 1 synthesis (root, 15:15)
- BLOCKED: T3 restricted class (D1·b counterexample); E rectangles rate ≤ 2; global Ogden/loop collision (Lemma O); marker-projection analytic route (M1, M2); test grammars (walk.md/builder3.md absent; near-grammars linear).
- PROVED: §3(c) survives; Lemma 3P, amb = Σ_σ P_σ with laminar periods and d_σ = #V_σ − rank ≤ k; §5 gives only ⌈m/2⌉ with uncontrolled length. T1-P1: off W_n = Σ_p V_p, ambiguity ≤ φ(n), so all extra ambiguity lives in Q ∩ W_n. P2: the bounded-exponent slice (ab+abb)* is equivalent to the full problem.
- LIVE CANDIDATE [conjecture]: S_N = (ab*)^{n}, n = P_N² (P_N = N-th primorial), product region ⊕E_k ⊆ W_n where primitive ⇔ all e_k ≠ 0; natural ply ∏ d_k ≥ n^{N/2}.
- KEY OBSERVATION [root]: since N → ∞, it suffices that the witness length is n^{O(1)}, or even n^{o(N)}. Exponential-in-n length (from the N! / det trick of PROOF.md §5) is fatal.
- Round 2: T2a cover-ply geometry (G1, G2, restriction to the subspace ⊕E_k); T2b effective witness length (G3); A2 upper-bound attack on the candidate.
