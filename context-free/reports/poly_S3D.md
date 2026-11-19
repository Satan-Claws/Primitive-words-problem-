# poly_S3D: can a covering requirement force a piece of large degree d_σ? — NO (PROVED)

Setting: Lemma 3P (poly_P.md §2): amb = Σ_σ P_σ(exp w − c_σ), L_σ = c_σ + ℕV_σ, supports of V_σ laminar pairs,
d_σ = #V_σ − rank V_σ ≤ k. Valid cover := finite family {c_σ + ℕV_σ} with laminar 2-supports, ∪ = primitive
part of the slice (e.g. (ab*)^n, any n), disjoint from the non-primitive part.

## Claim (PROVED)
Every valid cover has a refinement {e + ℕB} with B ⊆ V_σ linearly independent (so every d = 0), the same
union, still laminar, and pointwise ply ≤ #{σ : u ∈ L_σ} ≤ amb(u). Hence no covering/avoidance/laminarity
requirement, on any slice (ab*)^n or family of slices, forces d_σ > 0; a fortiori not d_σ > k.

## Proof
Ito (1969) / Eilenberg–Schützenberger: every linear set c + ℕV ⊂ ℕ^n is a finite *disjoint* union of linear
sets e + ℕB with B ⊆ V linearly independent (integer Carathéodory: y = Σq_j v_j, peel a dependent relation
until the remaining periods are independent; the offsets form a finite set). Apply to each L_σ:
- union unchanged ⇒ cover and avoidance preserved;
- periods are sub-lists of V_σ ⇒ supports still pairs, still laminar (a subfamily of a laminar family);
- disjointness inside each σ ⇒ new ply(u) = #{σ : u ∈ L_σ} ≤ Σ_σ P_σ = amb(u). ∎
Two rings with equal collinear pair support {s,t} (the d ≥ 1 configuration asked about) are exactly what the
refinement removes: c + ℕ{v,v'} with v' = λv is a finite union of e + ℕ{v}.

## Consequence
d_σ is a property of the grammar's tree-counting, invisible at the level of supports L_σ. Any lower bound
must come from ply of supports (degree-0 covers), i.e. the existing cover-ply / G3** / TILE_k routes.
The class of covers with all d_σ = 0 is: every valid cover after Ito refinement (in particular the R_m
half-space covers of PROOF.md §6). Caveat: grammar-realizability of the refined pieces is not claimed and
not needed (the negative is at cover level). Route BLOCKED.
