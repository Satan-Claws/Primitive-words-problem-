# R2/realise: the converse of Lemma 3P on S_N (data bounds, uniformity, realisation)

W2, 2026-11-24. Script: `round2/scripts/realise_bounded.py` (`… 3 4` ≈ 26 s, `… 4 2` ≈ 3 s).
Setting and notation: prompt §4.3–4.4, `R2/tile2.md`, `R2/audit_tile2.md`, `PA/poly_LAM.md` §2, `PA/poly_S2P.md`,
`PA/poly_T2a.md` §2. n = P², P = p_1⋯p_N, s_k = n/p_k, position = a + iP (fibre a, index i ∈ [0,P)),
CRT coordinates x_j = i mod p_j.

**Verdict.**
- (1) Data bounds: **YES, with K = 2 and offsets ≤ 2n, for every N** [written proof + exact check N = 3, 4].
  LAM's facets do *not* satisfy them, but a simpler facet family does. As a by-product, **Lemma C holds for all N**
  for this family, and every piece is **unimodular**.
- (2) Uniformity: formulated exactly (U1–U3). Data bounds do not imply it [written proof, toy example]. Whether
  S_N covers can be uniform is **not decided** [assessment]. U's single-split content is already blocked (§6).
  Its cross-split content is equivalent to the full problem. No non-uniformity mechanism is found.
- (3) Realisation: a sketch of the grammar gadgets, and the exact list of what is missing.
- Net: S_N is now blocked **at the level of every per-slice necessary condition known (Lemma 3P data, laminarity,
  Lemma C, lattice index)**. It is not dead. Killing it needs a uniform grammar, which is the affirmative problem.

## 1. Data bounds of the transport-rule pieces

### 1.1 LAM's facets violate the K-bound [computational + written]
- A piece's ring vectors on a tree edge {p,q} are (|μ_q| e_p + |μ_p| e_q)/gcd. This is forced: the edge must lie in
  ker μ_k.
- So ‖v‖₁ is the height of the ratio μ_q/μ_p. For μ_k = g·ν_k with generic ν_k this is unbounded. At N = 3 with
  |ν| ≤ 50, the transport trees T* have max ‖v‖₁ = 84 to 261 (medians 35 to 64; Part A of the script).
- audit_tile2 item 5 says "no n-dependence enters K". That is true of h and y, but not of μ. K is fixed only if the
  entries of μ_k come from a bounded set (more precisely, only if tree-adjacent ratios have bounded height).

### 1.2 Pair facets: bounded data [written proof]
**Definition.** For each k and each fibre a, pick an index i_a in the window [I_k, I_k + p_k) and a sign ε_a = ±1.
Put b_a = a + i_a P and set

  μ_k := Σ_a ε_a (δ_{b_a} − δ_{b_a + s_k}) = (1 − T^{s_k}) ν_k,   with entries in {0, ±1}.

Use the windows I_k = Σ_{j<k} p_j (in i-units).

**Fibrewise picture.**
- On fibre a, the space E_k^{(a)} consists of the zero-sum functions of x_k. U is the fibre-constants.
  V_{p_k} is the functions of x_{−k}, and E_j is the functions of x_j.
- The shift by s_k moves i by P/p_k. This changes x_k by c_k := P/p_k mod p_k ≠ 0 and fixes x_{−k}.

**Lemma 1 (admissibility).** μ_k ⊥ U, μ_k ⊥ V_{p_k}, μ_k ⊥ E_j for j ≠ k, and μ_k|_{E_k} ≠ 0.
*Proof.* Each pair ±(δ_b − δ_{b+s_k}) lies in one fibre and on one x_k-line (x_{−k} fixed). So the pair kills
every function of x_{−k}, which covers U, V_{p_k} and every E_j with j ≠ k. On E_k it gives f_a(x_k) − f_a(x_k + c_k),
which is ≠ 0 for f = e_r − e_{r+c_k}. ∎

**Lemma 2 (Lemma C for all N).** No nonempty proper cyclic arc I of supp μ_k is identically balanced on W.
*Proof.*
- The U-part of the form of I is the vector of fibre sums. Each fibre carries exactly the two points b_a and
  b_a + s_k, with values ±ε_a. So the U-part vanishes iff I contains both points of each fibre or neither.
- A fibre with both points contributes f_a(x_k) − f_a(x_k + c_k) to the E_k-part. This is a non-zero functional on
  E_k^{(a)}, and the fibres are independent coordinates of E_k.
- So the form of I vanishes on W only if I meets no fibre, that is, only if I = ∅. ∎
- With Thm B of tile2 and audit fix C1 (root at a positive vertex), the rule F_c has **ply exactly 1** on the near-U
  region, for every N. No computation is needed.

**Lemma 3 (pieces).** For a transport tree T on S_k = supp μ_k, rooted at a positive vertex t_k, put

  V_σ = ⋃_k ({e_p + e_q : pq ∈ T_k} ∪ {e_{t_k}}) ∪ {e_i : i ∉ ⋃S_k}.

Then the following hold.
- **(a) Norms.** ‖v‖₁ ≤ 2. Tree edges join opposite signs and |μ| = 1, so e_p + e_q ∈ ker μ_k. The root ring is a
  one-block b-loop. Lemma 3P permits one-block rings, and LAM's outside vertex o_k is unnecessary.
- **(b) Unimodularity.** Per component, the unsigned incidence matrix of a bipartite tree is totally unimodular,
  and e_{t_k} is independent of the edges (its signed sum is ±1). So det = ±1, ℤV_σ = ℤ^n, and the piece is
  c_σ + (cone V_σ ∩ ℤ^n).
  - Consequence: the covering-radius part of G3** vanishes for these pieces. Only the apex and the inradius remain.
- **(c) Coordinates.** The coordinate of a tree edge is the transport flow (an integer). The coordinate of e_{t_k} is
  τ_k = μ_k(x). The coordinate of e_i is x_i.
- **(d) Avoidance.** μ_k(c_σ + ΣqV) = μ_k(c_σ) + q_{t_k}, so L_σ ⊆ {μ_k ≥ 1 for all k} once μ_k(c_σ) = 1. This set
  misses ⋃_k V_{p_k}, which is the set of non-primitive vectors.
- **(e) Offsets.** The lex rule (S2P §1(b)) puts coefficients in {0,1}, so c_σ = Σ ε_v v has ‖c_σ‖₁ ≤ 2n. Hence
  K = 2, independent of n.
- **(f) Laminarity.** Each T_k is non-crossing, and crossing is cut-invariant.
  - Component k occupies the clusters [I_kP, (I_k+p_k)P) and that interval shifted by s_k.
  - Component k+1 lies in the gap between them iff p_{k−1} + p_k − 1 < P(p_k − p_{k−1})/(p_{k−1}p_k).
  - This holds when P > 2p_N³ (all N ≥ 6). It also holds as computed at N = 4. At N = 3 the script uses window
    width 1.

**Lemma 4 (VC ply, sketch on T2a §2's template).** Draw i_a uniformly in the window and ε_a = ±1 uniformly.
- Lower bound. For δ_k ∈ E_k∖0, some f_a is non-constant, so Pr[f_a(x_k) ≠ f_a(x_k + c_k)] ≥ 1/p_k. By
  Erdős–Littlewood–Offord and symmetry, Pr[u_k(δ_k) > 0] ≥ 1/(4p_k).
- Upper bound. Pr[u_k(δ_k) > 0] ≤ 1/2.
- Relative approximation with α = ∏1/(4p_k) = 1/(4^N P) gives ply_VC ≤ O((β/α)·D·log) with β = 2^{−N} and
  D = O(N log N Σd_k). So **ply_VC ≤ n^{1+o(1)}**. This is worse than T2a's √n·polylog n, but polynomial.
  [written sketch; constants not optimised]
- Total ply ≤ ply_VC · ∏q_k = ply_VC (Lemma 2). The number of pieces is ≤ exp(O(NP)) ≤ exp(O(n)), consistent with
  Lemma 3P.

**Exact checks** (Part B, integers). For N = 3 (n = 900, 4 samples) and N = 4 (n = 44100, 2 samples, laminarity on
2500 sampled pairs):
- entries ∈ {±1};
- ⊥ U, V_{p_k}, E_j all True, and ≠ 0 on E_k;
- 0 balanced cyclic arcs (N = 3 all arcs; N = 4 arcs from one start);
- T* spanning, NC and S2P-valid;
- x|_S = Σ coord·v exactly, with all coordinates > 0;
- max‖v‖₁ = 2; laminar True; component |det| = 1 (N = 3);
- the root has μ = +1.

**Answer to (1).** Lemma 3P's data bounds (K fixed, ‖c‖₁ ≤ nK, pair support, laminarity, d_σ = 0, and even
unimodularity) do **not** separate S_N from a low-ply family. Stanley refinement is not needed.

## 2. Uniformity: what one grammar forces across n

Fix G and its CNF G''. For (ab*)ⁿ, D_R is trivial, and by Fact A the nonterminals of G_n are (X, i, j) with
[i..j] the a-range (recon §2).

- **(U1) Regular skeleton family [written proof, standard].** There is a finite tree automaton 𝒜_G over V'' and a
  finite ring table R_G ⊆ ring types × ℕ² such that:
  - for every n, Sk_n = {t ∈ L(𝒜_G) : #_a(t) = n};
  - the piece of t is computed by a position-tracking homomorphism. A ring occurrence π of type ρ with (α,β) ∈ R_G,
    at a node with a-range [s..t], contributes α e_s + β e_t. Non-ring nodes contribute ≤ K to c.
- **(U2) Exchange [written proof].** Let t ∈ Sk_n and t′ ∈ Sk_{n′} have nodes of equal type X, with a-lengths ℓ and
  ℓ′. Then the transplant t[X ← t′|_X] lies in Sk_{n−ℓ+ℓ′}, and its piece lies in the primitive set.
  - Taking n = n′ and ℓ = ℓ′ at a different position gives a transplant by d = i′ − i. So the inner sets
    Inner(X, ℓ) are **translation- and slice-independent**.
- **(U3) Rectangularity.** For each (X, [i..j]), the pieces with that node form Inner × Outer.

**Facts about U.**
- **Data bounds do not imply U [written proof].** Take L_n with one piece: ring e_1 + e_n, loops elsewhere, and
  offset [n prime]·e_n. Then K = 2, the piece is laminar, and ply = 1. But L ∩ a a* a b = {aⁿb : n prime} is not
  CF. So U is strictly stronger than Lemma 3P.
  - For Q, however, n-dependence (on the factorisation of n) is unavoidable, since Q's slices themselves depend on
    it. Non-uniformity "in n" alone can never be the mechanism.
- **The single-split content of U is blocked.** At fixed n, (U3) at one node is a rectangle decomposition at one
  split. Prompt §6 says Q's split matrices have nonnegative rank O(n). Any argument must use (U2) across positions
  or across slices.
- **Can the transport covers satisfy U? Not decided [assessment].**
  - *Against, as constructed:* the windows I_k are absolute positions, and the spans s_k = n/p_k are tied to n.
    Transplanting the inner content of a pair edge (p, p+s_k) by d ∉ Pℤ breaks the fibre pairing. Every pair
    (b, b+s_k) straddles such an edge, so the hybrid facet is not ⊥ U. This makes the *specific* family non-uniform,
    unless types separate Ω(P) positions, i.e. |V''| grows.
  - *For a uniform refinement:* every admissibility condition (⊥ U, V_p, E_j), primitivity, and the transport cost
    h(|y_i − y_j|) is shift-invariant. Shifted facets are admissible. Closing the cover under all n rotations costs
    a factor ≤ n in ply.
  - No step forces a ring span to equal s_k: μ ⊥ V_{p_k} only says μ ∈ im(1 − T^{s_k}), and tree edges may join any
    opposite-sign points.
  - A rigorous "no uniform low-ply family exists" statement, made per word and polynomial in |w|, would therefore
    have to exploit (U2) across slices of different factorisation type. In particular, it must survive the fact
    that the same Inner(X, ℓ) serve prime-power and squarefree slices, where ply ≤ linear. I found no such
    mechanism.
  - **Exact open form (NONUNIF).** For every (𝒜, R_G) with |V''| fixed and N → ∞, every (U1)-family covering the
    primitive vectors of the n = P_N² slice has a point of ply n^{ω(1)} and norm n^{o(N)}. By Lemma 3P and
    amb ≥ ply this is *equivalent* to the S_N negative statement for all grammars. Formulating U adds a constraint,
    not yet a proof.

## 3. From slice covers to one grammar (sketch, [assessment])
**Gadgets.** These are the converses of the gadgets in Lemma 3P's proof.
- A pair ring e_p + e_q is X → b X b, read as left material in block p and right material in block q. It sits at a
  node whose a-yield is the blocks p+1..q.
- A one-block loop e_t is Y → b Y.
- A non-crossing tree becomes a well-nested system of such rings. A laminar family becomes a tree of a-spans,
  i.e. a CF skeleton.
- So any single piece, and any finite union of pieces on one slice, is a CFG with ambiguity equal to the ply.
  That grammar has size depending on n.

**What is missing for one grammar for Q.**
1. **Uniformity (U1–U2).** One finite automaton must produce, for all n, skeletons whose spans are shift-free
   (Inner(X, ℓ) position-independent). The pair facets need spans s_k = n/p_k for unboundedly many p_k, so the
   gadget "ring span = n/p" must come from cross-slice-consistent nonterminals. No construction is known.
2. **The off-W_n part.** T1 P1 gives ply ≤ φ(n). It must be produced by the same grammar and glued without
   double cover. The boundary between near-U and far-from-U regions (outside R⁰, tile2 §2(f)) is untreated.
3. **Lower strata.** These are boundary ω ∈ ∂U_{≥0}, vectors with zeros, and the lex walls. The lex rule handles
   walls inside one region only.
4. **All n,** not only P_N². General n has prime powers p^e and arbitrary multiplicities. The tiling and Lemma 2
   are written for n = P².
5. **G3** at lattice points.** It is simplified here: unimodular pieces have covering radius 0. The apex and
   inradius of ply-sets still need poly bounds.

## 4. Status summary
| claim | status |
|---|---|
| LAM facets give unbounded ‖v‖ (ratio heights) | [computational] N = 3; forced by ker μ_k [written] |
| Pair facets: admissible, entries ±1, Lemma C all N | [written proof]; exact check N = 3, 4 |
| Pieces K = 2, ‖c‖₁ ≤ 2n, unimodular, laminar (N = 3, 4, and N ≥ 6 by the nesting inequality), avoid V_p | [written proof]; exact check N = 3, 4 |
| ply_VC ≤ n^{1+o(1)} with pair facets | [written sketch] (T2a template, LO bound) |
| U1–U3 necessary for one grammar | [written proof, standard] |
| Lemma 3P data ⇏ U | [written proof] (prime-length toy) |
| Transport covers uniform / not | OPEN [assessment]: specific family non-uniform; no obstruction to a uniform refinement |
| Global grammar from slice covers | OPEN; gaps 1–5 of §3 |
