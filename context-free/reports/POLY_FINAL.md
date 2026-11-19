# Polynomial ambiguity of Q: stop report (no route unblocked)

Session 2026-11-18, 15:07–~16:00 UTC, three rounds of agents. The problem is **not resolved**: neither
resolution of §3 of the task is proved. Supporting notes: `poly_*.md` in this directory; log: `POLY_REGISTRY.md`.
Nothing below has been through a gated audit (no candidate claimed to close a named gap).

## 1. Strongest rigorously proved statements (all [written proof], unaudited)

**Theorem P (quantitative lower bound on the ambiguity function).** For every cycle-free CFG G with
L(G) = Q, A_G(L) = Ω(√(log L / log log L)).

The proof is the chain below.
- *Exponential case:* if G is exponentially ambiguous (Wich's C_exp, [published] DLT'99 Thm 4.4), then
  A_G(L) = 2^{Θ(L)}.
- *Polynomial case:*
  1. CNF conversion and the DFA product with R_m [Lean-checked].
  2. Structure part (c) holds without finite ambiguity (`poly_P.md` §1). Its 2^N trees sit on one word of
     length O(N). The Dyck caveat does not apply, because both contexts insert b's only into fixed blocks.
  3. **Lemma 3P** (`poly_P.md` §2): amb(w) = Σ_σ P_σ(exp w − c_σ), where P_σ is the vector partition function
     of a laminar, pair-supported period list. Its degree is d_σ = #V_σ − rank V_σ ≤ k, uniformly over all
     slice grammars.
  4. The §5 argument survives with these supports (`poly_P.md` §3), giving a word of Q ∩ R_m with ≥ ⌈m/2⌉ trees.
  5. Skeleton bounds with a constant K of G (`poly_T2b.md` §1): ‖v_π‖ ≤ K, ‖c_σ‖ ≤ nK,
     #skeletons ≤ exp(O(n)).
  6. Lemmas C and G, effective ply (`poly_G3.md` §1).
  7. **Lemma F**, face restriction (`poly_G4.md`): fixing all but r diagonal pairs to 1 keeps a valid cover with
     the same K. Hence some word has ply ≥ p at length 2m + exp(O(p² log pK)).
  8. Choosing p ≈ √(log L / log log L) gives the bound.

This strictly quantifies the Lean-checked "not finitely ambiguous" result. It is far from superpolynomial.

**Further proved lemmas used or discovered:**
- **Theorem E:** some word of Q ∩ R_m has ≥ ⌈m/2⌉ trees and length ≤ exp(O(m² log mK)), via Papadimitriou's
  small-solution bound (`poly_T2b.md`).
- **T1-P1:** on any slice of (ab*)^n, the part outside W_n = Σ_{p|n} V_p has a grammar with ambiguity ≤ φ(n).
  Hence prime-power n slices are at most linearly ambiguous.
- **T1-P2:** the slice (ab+abb)* is equivalent to the whole problem (`poly_T1.md`).
- **Lemma O:** {r#a − s#b = ±1} is a DCFL contained in Q (`poly_L.md`).
- **M1:** GF(Q ∩ (ab⁺)*) is not algebraic. **M2:** on a slice with non-algebraic GF, the marked preimage is not
  unique infinitely often (`poly_M.md`).
- **Reformulation** ([published] Wich MFCS'01): a polynomially ambiguous grammar for Q exists iff Q = h(L) with
  L an unambiguous CFL and h erasing boundedly many marker symbols.

## 2. Exact remaining gap (one lemma)

**Lemma G\* (open).** There are slices (ab*)^{n_N} and constants such that every family of laminar pair-supported
linear pieces with data ≤ K that covers the primitive exponent vectors (with multiplicity ≥ 1) and avoids the
non-primitive ones has a point of ply ≥ n_N^{ω(1)} and ℓ¹-norm ≤ n_N^{o(log n_N/log log n_N)}.

Lemma G\* plus Lemma 3P and Lemma G gives the negative resolution. It splits into:
- **G-LAM** (ply): the S_N = (ab*)^{P_N²} product region. The pure convex geometry has a cover of ply
  √n·polylog n (`poly_T2a.md` §2, VC-dimension sampling), which refutes the conjectured ply lemma G1. A laminar
  realisation of that cover exists at any fixed generic base point (`poly_LAM.md` §2). What is open is
  uniformity over base points and non-generic points (`poly_LAM.md` §3). Laminarity is the only remaining source
  of superpolynomial ply.
  `poly_GLAM.md` sharpens this to **G-LAM′**: for each u_k, is there an admissible facet μ_k with a non-crossing
  bichromatic tree all of whose residue folds are nonzero with the sign of the top vertex? If yes, the √n·polylog
  cover is global and the S_N candidate is BLOCKED. Forced blow-up from many incident chambers is refuted (lex rule).
- **G3\*\*** (length): for some ply-set S, bound by poly(n)·K the apex of ∩(c_σ + A_σ), the covering radius of
  Λ_S = ∩ℤV_σ, and the inradius of ∩A_σ (`poly_G3.md` §4). Laminar chains {e_1, e_i + 2e_{i+1}} have index 2^ρ
  and are realisable by a fixed grammar fragment on any spaced slice (`poly_R3a.md`). No valid cover forcing
  exponential length is known (`poly_G4.md` §4).

## 3. Approach families

| family | status | where and why it stalled |
|---|---|---|
| restricted class (T3) | BLOCKED | D1·b is unambiguous, branching, inside Q, and not in FR or finite index; "poly-ambiguous ⇒ FR" is the target restated (`poly_T3.md`) |
| counting: rectangles.md rate (E) | BLOCKED | only limsup e_G(n)^{1/n} > 1 is proved; rate ≤ 2 under polynomial ambiguity |
| counting: Wich marker projection (M) | BLOCKED | M2; intersections of PCFLs not CF; the marker variable is trivial; reduces to the sandwich (`poly_M.md`) |
| global pumping / Wich collision (L) | BLOCKED | Lemma O: test families inside letter-count DCFLs admit finitely ambiguous grammars (`poly_L.md`) |
| structural transfer (P) | DONE | Lemma 3P; R_m caps at linear in m with uncontrolled length |
| slice family (T1) | candidate S_N, reduced to G-LAM | squarefree n caps at φ(n); nested R_m gives L^{<1} |
| cover-ply geometry (T2a) | G1 REFUTED | VC sampling gives ply √n·polylog n; the Lemma X analogue fails for class size > 2 |
| laminar ply (LAM) | locally BLOCKED, uniform version open | merge-tree lemma realises low-ply facets |
| witness length (T2b, G3, R3a, G4) | reduced to G3\*\* | N! trick fatal; averaging blocked; slice congruences blocked (Lemma B); spacers blocked; constant ply at poly length proved (Cor F) |
| constructive (AG, A2) | no polynomial construction | one-witness-per-prime fails on coverage; canonical laminar choice impossible (Lemma A) |

## 4. Witness families and counterexamples
- D1·b: unambiguous, non-finite-index sublanguage of Q with γ = 2. L_{r,s,±1}: DCFL sublanguages of Q.
- Laminar chain {e_1} ∪ {e_i + 2e_{i+1}}: lattice index 2^ρ; realised by Y → bYbb | T on every spaced slice.
- L₁ ∩ L₂ = ℕ(1, 2, …, 2^ρ): two laminar pieces whose common points are exponentially large.
- d = (2,2): 7 product pieces with max ply 3 < ∏d_k = 4 (exact ILP, [computational]), refuting the product ply
  lower bound.
- Near-grammars G_A (coPow₂) and G_B (length dispatch): linear max ambiguity, errors from aaa, bbb / a, b, ababab
  ([computational], `poly_AG.md`).
- Multi-prime n: single-defect words (all exponents equal except one) defeat one-witness-per-prime grammars;
  at n = 36, witness-system counts ≈ 5·m₂·m₃ ([computational], `poly_A2.md`).
- `walk.md` and `builder3.md` are not present in the repository, so they were not measured.

## 5. Session 2 addendum (2026-11-18, 22:15–22:45 UTC)

Still unresolved, and no route unblocked. New proved results ([written proof], unaudited):
- **G-LAM′ refuted** (`poly_GLAM2.md`). Fold-dominance forces single-fibre support, so trees that are uniform in
  ω have one-fibre facets. **Corollary:** a cover by ω-uniform pieces has ply ≥ (P_N/2)^N = n^{ω(1)}. This
  partly revives the ply side of the S_N candidate.
- **Symmetric base point** (`poly_S2W.md`). ω = 𝟙 does not force one-fibre facets: laminar low-ply covers exist
  at any single base point.
- **Patching** (`poly_S2P.md`). ply ≤ ply_VC·∏_k q_k, and walls are not double-counted. The question reduces
  exactly to **TILE_k**: do trees exist whose validity cones K_T cover the base-point region with ply
  ≤ p_k^{O(1)}? If yes, S_N is blocked geometrically. If no, S_N survives on ply. The n = 36 computation is
  inconclusive ([computational], `poly_S2X.md`).
- **Witness length.** Lemma S2T and Lemma S2T′ (`poly_S2T.md`, `poly_S2L.md`): polynomial facet heights,
  quotient exponents, Deep constants and genericity-hyperplane count together give poly-length witnesses.
  c-locality cannot be forced (star cover). The hyperplane count is a fourth exponential source for G3\*\*
  (Siegel).
- **Slices (a⁺b⁺)^n** (`poly_S2R.md`): the same covering problem as (ab⁺)^{2n}. No new lever.
- **Devil region n = 6, 12** (`poly_S2D.md`). A non-CF proof is impossible here (Kászonyi–Katsura, cited in
  devil.md). Lemma U: one non-crossing matching cannot cover the region.

**Updated exact gap:** Lemma G\* = **TILE_k** (ply) + **G3\*\*** with the hyperplane-count term (length).
- **Explicit cover for n = 6** (`poly_S2K.md`). 16 stratified pieces built from "rectangles"
  {i, i+A, i+A+B, i+B}. It covers Q ∩ (ab*)^6 with max ply ≤ 5 ([computational], entries ≤ 4). It appears to
  extend to squarefree pq with ply O(n) [conjecture], and fails as given for p^a q^b with a or b ≥ 2.
- **TILE_k sharpened** (`poly_S2Y.md`). It suffices to have Q1 (a chain-valid tree T(π) for every order cone π)
  and Q2 (each K_{T(π)} meets ≤ p_k^{O(1)} order cones). Together these block S_N geometrically. A lower bound
  from cone width alone is impossible, since order cones are equally narrow yet tile with ply 1.

**Final exact gap (session 2):** Lemma G\* = TILE_k (≡ Q1 ∧ Q2, or their failure) + G3\*\* (four height terms).
- **Q1 at n = 36** (`poly_S2Z.md`, [computational], INCONCLUSIVE). A non-exhaustive search found no
  chain-valid tree for 400 of 400 sampled orders (node cap hit). This is weak evidence against Q1, so the
  low-ply blocking route for S_N is unconfirmed.
- **Q1 not refuted by the fold argument** (`poly_S2Q.md`). A 6-vertex, 3-fibre chain-valid abstract tree
  exists, so chain-validity forces no single-fibre restriction. The induction gives only π-monotonicity: f_u
  vanishes on fibres π-before res(u). Q1 stays OPEN, and a negative answer must use the fixed supp μ_k and
  non-crossing on ℤ_n.

## 6. Session 3 addendum (2026-11-19, 10:52–~11:20 UTC)

Still unresolved, and no route unblocked.
- **Degree route BLOCKED** (`poly_S3D.md`, [written proof]). Ito / Eilenberg–Schützenberger refinement makes
  every piece degree 0 without raising ply, so no covering requirement can force d_σ > k.
- **Q2 false as posed** (`poly_S3Q.md`). Every chain-valid tree is valid at ω = 𝟙, so the right measure is
  D_k, the number of distinct trees. For abstract μ, **D ∈ {P−1, P}** (`poly_S3E.md`, `poly_S3L.md`). This is far
  above the p_k^{O(1)} needed to block S_N, so the order-cone selection cannot block the candidate.
- **Q1 false at n = 36** ([computational], exhaustive interval DP over all non-crossing trees, `poly_S3A.md`).
  There are 0 chain-valid trees for 20 targets × 720 orders.
- **Near-vertex base points** (`poly_S3V.md`). At any single ω, valid trees exist for every u_k
  ([written proof]). For M ≥ poly(n), no tree is valid near two different vertices (fold-dominance ⇒ |F| = 1;
  data [computational]). This forces D_k ≥ 2 but no overlap, since fans remain possible.
- **Length.**
  - The hyperplane-count term folds into the inradius (Lemma H, `poly_S3H.md`), so G3\*\* is back to its three
    height terms.
  - Conditional **Theorem P′** (`poly_S3P.md`): with polynomial facet heights and lattice exponents on one
    (2p−1)-face, A_G(L) = Ω(log L / log log L).
  - The p² in Theorem P comes from heights K^{Θ(p)} and from the lcm of p quotient exponents.

**Exact gap (unchanged in form):** a lower bound on overlap for fans of tree-validity cones (TILE_k in its
general form, beyond order-cone selection), together with G3\*\* (three height terms).
- **TILE_k exact-cone test at n = 36** (`poly_S3T.md`, [computational], INCONCLUSIVE). Covers need ply 2 once
  the training set is large. Fresh max ply is 3 for both p = 2 and p = 3 (a weak hint that q_k = O(1), i.e.
  towards blocking S_N). Coverage reached only 51–92%, with gaps near faces and vertices.
