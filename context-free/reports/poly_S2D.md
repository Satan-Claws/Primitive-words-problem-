# poly_S2D — constructive / Ginsburg probe on the devil region (n = 6, 12)

Status: **no non-CF claim.** Route "Ginsburg stratification ⇒ Q∩(ab*)^6 not CF" is BLOCKED
(the natural pumping obstruction is always satisfiable), consistent with LITERATURE
(Kászonyi–Katsura: Q∩(ab*)^n is CF when n is a product of two prime powers, so n = 6, 12 are CF;
any non-CF "proof" here would contradict a published theorem). No CFG written; exact gap in §4.
Script: `scripts/poly/s2d_probe.py`.

## 1. The region (PROVED)
E_n = {x ∈ ℕ^n : a b^{x_1}⋯a b^{x_n} ∈ Q} = ℕ^n \ ∪_{p|n} V_p, V_p = (n/p)-periodic vectors.
n = 6: V_2 = 3-periodic (dim 3), V_3 = 2-periodic (dim 2), V_2∩V_3 = ℚ·1,
W_6 = V_2+V_3 = {x_1−x_4 = x_3−x_6 = x_5−x_2 =: δ} (dim 4). Writing x = a+b (a 3-periodic, b = (b_1,b_2)^3):
x ∈ E ⇔ δ = b_1−b_2 ≠ 0 ∧ a non-constant. On W_6: alt(x) = Σ(−1)^{i+1}x_i = 3δ, and (with D(x) =
(x_1−x_2, x_3−x_4, x_5−x_6)) D(x) = δ·1 + (a_1−a_2, a_3−a_1, a_2−a_3). So on W_6:
x ∈ E ⇔ alt(x) ≠ 0 ∧ D(x) non-constant.
n = 12: W_12 = V_2(6-per.)+V_3(4-per.), dim 6+4−2 = 8; x = a+b primitive ⇔ a, b both not 2-periodic.

## 2. Ginsburg reduction (PROVED, standard)
On (ab⁺)^n the factorisation over a*b*…(2n blocks) is unique (12 maximal runs), so by Ginsburg
(bounded CFL ⇔ finite union of stratified linear sets) Q∩(ab⁺)^n CF ⇔ E_n⁺ is a finite union of
stratified linear sets c+ℕP (periods: support ≤ 2, pairwise non-crossing; shared endpoints allowed).

## 3. Direction-1 pumping lemma (PROVED) and why it fails to obstruct
Lemma. If S = c+ℕP ⊆ E_n contains x+N·1 for infinitely many N, then there is J ⊆ P (Dickson on the
coefficient vectors: D·1 = Σ_J μ_j p_j, μ_j > 0) with x ∉ V_p + ℤJ for every p | n.
(x + kD1 + v ∈ S for all v ∈ ℤJ, k ≫ 0, and 1 ∈ V_p.) Hence a non-CF proof along this line needs
x ∈ E with x ∈ ∪_p (V_p+span J) for every admissible J.
Prop (PROVED, n=6). J = M1 = {e_1+e_2, e_3+e_4, e_5+e_6} separates every x ∈ E∩W_6:
M1+V_2 = {alt = 0}, M1+V_3 = {D const} (by §1). The rigid piece {y : D(y) = D(x)} is stratified
(disjoint adjacent pairs) and ⊆ E. COMPUTER-CHECKED: every sampled hard vector is separated by a
non-crossing perfect matching (n=6: 3456/3456; n=12: 364/364 over 132 matchings).
⇒ BLOCKED: no obstruction from direction-1 pumping; stratification is never the failing step locally.

## 4. Exact gap (constructive side)
Lemma U (PROVED). M1-pieces {y : D(y) ∈ A_1×A_2×A_3}, A_i ultimately periodic, cannot cover E∩W_6 with
finitely many pieces: the family D = (t, s−t, 0) (s≠0) forces a rectangle A×B with A∩(−B)=∅ containing
(t, −t−M) for t ≫ 0, M = common period, contradiction by periodicity. Same for any single matching.
So a CFG must mix pieces from different matchings / linear forms (B1) with sign-restricted cones (devil B2
rigid example (λ1,λ2,λ3,λ3,λ2,λ1+1)). Gap: a finite mixed cover of E∩W_6 — known to exist (KK) but not
reconstructed here; ambiguity of it not computed.
