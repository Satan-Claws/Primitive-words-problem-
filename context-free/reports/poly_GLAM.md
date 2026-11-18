# poly_GLAM: ω-uniformity of the laminar low-ply cover (agent GLAM; geometry only)

Setting: poly_LAM.md §2–3, poly_T2a.md §1–2. W := U ⊕ ⊕_k E_k. Piece σ = (u-tuple from T2a, trees T_1..T_N),
tree T_k on supp μ_k as in LAM §2(b). Status: OPEN (reduced); mechanism (ii) REFUTED as stated.

## 1. Correct local picture (PROVED, routine)
In the edge basis V_σ every coordinate is linear on W: root n_{v_k}(x) = c_k μ_k(x), internal n_u(x) =
μ_k(x|_{S_u})/|μ_top(u)| (S_u = subtree of u), loops x_i. So near U the piece is the open simplicial-type cone
  K_σ = {x : μ_k(x) > 0, n_u(x) > 0 (u internal), x_i > 0}.
tω+δ ∈ L_σ for t ≫ 1  ⇔  every defining form f has f(ω) > 0, or f(ω) = 0 and f(δ) > 0 (lex rule; f(δ)=0 ties
are lower strata, all-or-nothing by T2a §1(c)). Since μ_k(ω) = 0, ω-validity is ω ∈ cl Ω_{T_k},
Ω_T := {ω ∈ U : μ_k(ω|_{S_u}) has sign of top(u) ∀u}.
Consequence: ply(ω,δ) = Σ_{u-tuples} ∏_k #{T ∈ 𝒯_k(u) : (ω,δ) lex-valid for T}.

## 2. (ii) is not a valid mechanism (PROVED)
"Pieces from all chambers incident to a wall point must contain nearby points" gives ply ≥ #incident only if
one point lies in all of them. If the chosen cl Ω_T tile U_{>0} (complete fan), the lex rule assigns every
(ω,δ) with generic δ to exactly one tree per component: incidence ≠ ply. A blow-up must show that the
*realizable* cones Ω_T (fixed by T, cannot be shrunk) admit no poly-overlap subcover.

## 3. Reductions (PROVED)
(a) Product: ply_k ≤ C per component ⇒ total factor C^N = n^{o(1)} (log n ≍ N log N); even ply_k ≤ p_k^{O(1)}
gives ∏_k p_k^{O(1)} = P_N^{O(1)} = poly(n). So G-LAM is a per-component question.
(b) ε-approximation criterion (as T2a §2): if for each k there is a distribution 𝒟_k on trees with
  ρ_k := sup_ω Pr_T[ω lex-valid] / inf_ω Pr_T[ω lex-valid] ≤ poly(n),
then sampling (jointly with T2a's u-tuples) gives ply ≤ O(D log(·) · ∏ρ_k-type factor) with
VC-dim D ≤ log₂#trees = O(|supp μ_k| log) = Õ(√n). Ranges = {T valid at (ω,δ)}, includes non-generic ω.
(c) ω-free sufficient condition ("fold-dominance"): fold(x)_r := Σ_{i≡r (P_N)} x_i. If T satisfies
  fold(μ_k|_{S_u}) ≥ 0 (resp. ≤ 0), ≠ 0, with the sign of top(u), for every internal u,
then Ω_T ⊇ U_{>0} (ω is P_N-periodic and > 0), no ω-walls exist, non-generic ω are automatic, and the
T2a cover (ply √n·polylog) is realized globally: G-LAM holds.
Necessary local facts: a leaf child y of x must have y ≡ x (mod P_N) and |μ_y| < |μ_x| ... (bichromatic +
sign-definite ⇒ off-residue parts of children must cancel inside the child subtree).
Freedom: ν_k may be changed by anything with ⟨μ_k,·⟩|_{E_k} fixed; μ_k = (1−T^{s_k})ρ_k with P_N | s_k, so
masses on the two clusters are exact negatives (m_{i+s_k} = −m_i).

## 4. Exact sub-question
(G-LAM′) For every u_k ∈ E_k* (or a T2a-sufficient random family), does some admissible μ_k admit a
non-crossing bichromatic fold-dominant tree on supp μ_k? Yes ⇒ G-LAM true, candidate's laminar route dead.
Obstacle: per-residue greedy trees (ω-independent, since ω constant on a residue) are crossing because
residues interleave with period P_N; splitting into per-residue root edges yields one-fibre facets μ^{(r)},
which LAM §1 shows force ply ≥ (P_N/2)^N. If G-LAM′ fails, fall back to criterion 3(b) (ratio ρ_k).
