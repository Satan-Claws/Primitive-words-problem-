# poly_GLAM2: G-LAM′ decided — fold-dominant trees exist only on one fibre (agent GLAM2)

Setting: poly_GLAM.md §3(c), §4; poly_LAM.md §2. fold(x)_r := Σ_{i≡r (P_N)} x_i. A tree T on supp μ_k is
*fold-dominant* if it is bichromatic and, for every non-root vertex u, fold(μ_k|_{S_u}) is ≥ 0 (top u positive)
or ≤ 0 (top negative) and ≠ 0. Status: **G-LAM′ REFUTED (PROVED, all N); computer-confirmed in the toy cases.**

## 1. Lemma (Single fibre, PROVED)
If μ ⊥ U (i.e. fold(μ) = 0) and T is fold-dominant on supp μ, then supp μ lies in one residue class mod P_N.
Proof. Let ρ := root residue, root sign +. Children c of the root are −, fold(S_c) ≤ 0, and
Σ_c fold(S_c) = fold(μ) − μ_root e_ρ = −μ_root e_ρ. A sum of ≤ 0 vectors that vanishes off ρ has every term
vanishing off ρ; as fold(S_c) ≠ 0, it is supported exactly at ρ. Induction claim: every non-root u has
fold(S_u) supported exactly at ρ (sign of u) and res u = ρ. Given it for u: its children d have the opposite sign,
and Σ_d fold(S_d) = fold(S_u) − μ_u e_{res u}. If res u ≠ ρ, the ρ-entry of the left side has the sign of the
children, the right side has the sign of u, and it is ≠ 0: contradiction. So res u = ρ, the right side vanishes
off ρ, hence so does each fold(S_d) (same-sign terms), and fold(S_d) ≠ 0 puts it exactly at ρ. ∎
(Non-crossing is not used; nor is the shape of the admissible space beyond μ ⊥ U.)

## 2. Consequence for G-LAM′
E_k = ⊕_r E_k^{(r)} splits by fibre (zero-fibre-sum and the periods P_N p_k are fibre-wise), so u_k = ⟨μ_k,·⟩|_{E_k}
depends on μ_k|_{fibre r} on E_k^{(r)} only. A fold-dominant μ_k therefore realizes only *one-fibre* targets u_k.
For any u_k touching ≥ 2 fibres (generic u_k, in particular T2a's random normals) **no admissible μ_k has a
fold-dominant tree**: answer NO for every N, every k. Every tree then has an ω-wall (some subtree fold of mixed
sign), so Ω_T ⊊ U_{>0}.
Corollary (PROVED, from LAM §1 with s = 1): a cover all of whose pieces are ω-uniform (Ω_T ⊇ U_{>0} for all
components) has ply ≥ (P_N/2)^N = n^{ω(1)}. So ω-uniformity and low ply are incompatible; any poly-ply laminar
cover must use ω-dependent trees.

## 3. Data (`scripts/poly/glam2_search.py`, exact)
| case | search | fold-dominant found |
|---|---|---|
| abstract, m ≤ 5 vertices (any n, crossing allowed) | all rooted labelled trees × residue labellings, LP (strict via scaling) | 145 feasible, **all single-residue**; 0 with ≥ 2 residues |
| toy P=2, n=4 (μ forced by u) | 12 NC trees × 4 roots, 3 random u | 0 |
| toy P=3, n=9 (μ forced by u) | 43263 NC trees × 9 roots, 3 random u | 0 (93–171 bichromatic) |
| N=2, P_N=6, n=36 | admissible dims 18 (k=1), 24 (k=2); E_k fibre ranks 1^6 (6), 2^6 (12) | decided by Lemma: NO |
(Abstract m = 6: see registry line / script run; Lemma covers all m.)

## 4. Status
G-LAM′: REFUTED (hand proof, generalizes to all N). Fold-dominance route to kill the candidate: DEAD.
Ply side of candidate S_N: partially revived — ω-uniform laminar covers have superpolynomial ply. G-LAM itself
remains OPEN: it is now exactly criterion poly_GLAM §3(b) (distributions of ω-dependent trees with validity
ratio ρ_k ≤ poly(n)), not settled here.
