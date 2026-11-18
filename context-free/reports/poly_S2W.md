# poly_S2W: symmetric base point ω = 𝟙 — does it force fold-dominance? (agent S2W; geometry only)

Setting: poly_GLAM.md §1 (cone K_σ, lex rule), poly_GLAM2.md §1 (single-fibre lemma), poly_LAM.md §1–2.
Status: **idea REFUTED as stated (PROVED); residual = structural ties at 𝟙 (OPEN, minor).**

## 1. The implication fails at the first step (PROVED)
Lex-validity of t𝟙+δ (t ≫ 1, δ ∈ ⊕E_k generic small) for tree T_k needs, for every internal u,
  n_u(𝟙) = Σ_{i∈S_u} μ_i = ⟨fold(μ|_{S_u}), 𝟙⟩  has the sign of top(u), or = 0 and n_u(δ) has that sign.
This is ONE scalar condition per u (the 𝟙-weighted sum of the fold vector). Fold-dominance (GLAM §3(c)) is the
P_N-coordinate condition fold(μ|_{S_u}) ≥ 0 / ≤ 0 entrywise, which is equivalent to Ω_T ⊇ U_{>0}, i.e. validity
at EVERY ω ∈ U_{>0}, not at 𝟙. "Subtree folds at 𝟙 are fold values" only yields ⟨fold,𝟙⟩, so the hypothesis of
the GLAM2 lemma is not implied, and the lemma (one-fibre support) does not apply.
Positive counterpart: LAM §2(b) with masses m_i := μ_i ω_i = μ_i (ω = 𝟙) builds, for ANY multi-fibre u_k, a
non-crossing bichromatic tree with all subtree masses of top sign at 𝟙 (needs only Σ m_i = 0, generic ties
avoided). Nested assembly (LAM §2(c)) then realizes the T2a cover, ply O(N log N Σ d_k) = √n·polylog, at the
points t𝟙+δ. So ω = 𝟙 gives NO ply ≥ (P_N/2)^N; LAM §1 needs one-fibre facets, which nothing here forces.
Non-genericity of 𝟙 only helps the cover: pieces whose Ω_T has 𝟙 on its boundary are resolved by the lex rule
(GLAM §2: lex tilings, ply 1 per tie), and half-open strata (T2a §1(c)) add freedom, not obstructions.

## 2. Exact residue (OPEN, minor)
Ties n_u(𝟙) = 0 forced for every admissible μ_k (with ⟨μ_k,·⟩|_{E_k} = u_k) would add lex facets n_u(δ) > 0.
Known structural zeros: S ∩ A_k fibre-complete (fold(ρ'_k) = 0 ⇒ Σ_{A_k∩fibre r} μ = 0 for each r) — but these
vanish at every ω ∈ U, so they are not specific to 𝟙, and the merge order can avoid them. Extra 𝟙-only zeros
need 𝟙_S ∈ (pairing-determined span) ∖ ω·(…); none found, not classified. Even when present they give facets
touching all fibres of S, not one fibre.

## 3. Length (t poly(n)?) (PLAUSIBLE, not proved)
Entries of t𝟙+N!δ are t + O(N!|δ|). If μ_k is integral of height poly(n) (N factors (1−T^·) give 2^N·|ν|;
inverting them on E_k costs |1−e^{2πi·/p_k}|^{-1} ≤ poly), nonzero subtree masses are ≥ 1, so the lex threshold
t ≥ max|n_u(δ)|/min n_u(𝟙) + |c_σ|-terms is poly(n)·|δ|, provided T2a's rational normals and the offsets c_σ have
poly height. But generic ω ∈ U∩[1,P_N]^n already has poly entries, so 𝟙 gives no real gain for G3**.
