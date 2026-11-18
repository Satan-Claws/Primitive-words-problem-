# poly_M — Wich cut-marker route, option (i): forced uniqueness / algebraicity

Setting: Q = h(L) (WLOG one L: disjoint marker alphabets per pattern p keep the union unambiguous), L ∈ UCFL over Σ∪Γ, ≤ c markers per word, h erases Γ.
For regular R ⊆ Σ*: L_R := L ∩ h^{-1}(R) ∈ UCFL, so
  A_R(z) := Σ_{w∈Q∩R} amb(w) z^{|w|} is algebraic,  amb(w) = #{marked preimages of w in L} ≥ 1.

## Lemma M1 (PROVED). R = (ab⁺)*: GF(Q∩R) is not algebraic.
Words of R ↔ compositions (k_1..k_n), w primitive ⇔ the cyclic sequence is primitive. With C(z)=Σ_{R∖ε} z^{|w|} = z²/(1−z−z²),
  GF(Q∩R) = Σ_{d≥1} μ(d) C(z^d).
C(z^d) has, in |z|<1, poles only on |z| = φ^{-1/d} (other root −φ of 1−x−x²... has modulus >1). Moduli differ for distinct d, so the poles of squarefree d cannot cancel: infinitely many poles in the open unit disk ⇒ not algebraic (nor D-finite). (Same as Petersen for R=Σ*.)

## Lemma M2 (PROVED, kills forced uniqueness). For every representation Q=h(L) and every regular R with GF(Q∩R) non-algebraic (e.g. R=Σ*, (ab⁺)*), there are infinitely many w ∈ Q∩R with amb(w) ≥ 2.
Proof: if amb(w)=1 for all but finitely many w∈Q∩R then A_R = GF(Q∩R) + polynomial is algebraic. Contradiction.
So marker positions cannot be "forced" by any choice of R making the count transcendental. Restricting markers by a regular M (e.g. "markers only next to the isolated aa blocks of R_m") gives h(L∩M) ⊊ Q∩R in general: marker positions are the grammar's choice, not ours.

## Failing steps of (i)
1. Forced uniqueness: refuted by M2 on exactly the slices where transcendence is available; on slices where it might hold, GF(Q∩R) is algebraic-compatible and no contradiction arises.
2. Inclusion–exclusion over p: needs GF(h(L_p)∩h(L_q)∩R); intersections of PCFLs are not CF, GF unconstrained. Also unnecessary since P=1 WLOG.
3. Marker variable t counting markers is t^r per pattern: no information. With P=1, A_R(z) with 1 ≤ amb ≤ C n^k is exactly the BLOCKED sandwich.
4. The target class (finite unions, r=0, P=2) already contains ambiguity-2 CFLs with natural-boundary GF (PARALLEL_CAMPAIGN_FINDINGS.md Thm 6.2): no property of the word-count GF of Q∩R alone is preserved.

## Only residual (OPEN, unevaluated)
Position-weighted series B_R(z,t) = Σ_{marked x∈L_R} z^{|x|} t^{(index of first cut)} is algebraic in (z,t); B_R(z,1)=A_R. Using t requires a structural statement about where cuts of primitive words can sit — this is the structural route, not analytic.
