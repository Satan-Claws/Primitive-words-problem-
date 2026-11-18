# poly_P: PROOF.md §3/§5 under polynomial ambiguity

Setting: G cycle-free, L(G)=Q, amb_G(w) ≤ C|w|^k. G_m := ((G''×D_{R_m})×D_n) reduced (PROOF.md §2);
Lemmas 1.1/1.2 give amb_{G_m}(w) ≤ amb_G(w) ≤ C|w|^k, same C,k for every m. n = 2m.

## 1. §3(c) under polynomial ambiguity — CONFIRMED (PROVED)
(c) produces, for one word of length |w0| + N·(|κ1|+|κ2|) (each block 12/21 inserts the same b's into
blocks s,t), 2^N distinct trees. 2^N > C(|w0|+O(N))^k for N large. Same for the side-child uniqueness
and F3 (two trees of a side child Z give two first-return contexts; then rerun the 2^N construction).
So rings, unique side trees, skeleton finiteness (d) and laminarity (f) all hold. Only (e)
(independence) used finite ambiguity essentially: its K+1 trees sit on a word of length Θ(K), which is
compatible with polynomial ambiguity. So (e) is dropped.

## 2. Lemma 3P (structure, polynomial version) — PROVED
For each skeleton σ let V_σ = (v_π)_π be the *list* (with repetitions) of ring vectors of its C-paths,
r_σ = #V_σ, ρ_σ = rank V_σ, d_σ := r_σ − ρ_σ. Define the vector partition function
  P_σ(u) := #{q ∈ ℕ^{r_σ} : Σ_π q_π v_π = u}   (finite: v_π ∈ ℕ^n∖0 so q_π ≤ ‖u‖₁).
Then (i) supports of V_σ are pairs forming a laminar family; (ii) for all w ∈ (ab*)^n
  amb_{G}(w) = Σ_σ P_σ(exp w − c_σ).
*Proof.* (a)–(d),(f) of PROOF.md §3 hold (Part 1). (d) is a bijection trees ↔ (σ, q ∈ ℕ^{r_σ}) with
exp(yield) = c_σ + Σ q_π v_π; count fibres. ∎

**Growth (precise).** Let A_σ = cone(V_σ). For a face F of A_σ put V_F = V_σ ∩ F (as a list), d_F =
#V_F − dim span F. If u ∈ F then every representation uses only V_F, so P_σ(u) = P_{V_F}(u).
 (U) P_σ(u) ≤ (‖u‖₁+1)^{d_σ} for all u (fix a basis B ⊆ V_σ; q is determined by q_{V∖B}, each ≤ ‖u‖₁).
 (L) For u₀ := Σ_π v_π (∈ relint A_σ ∩ ℤV_σ) and t ∈ ℕ: P_σ(t u₀) ≥ #{z ∈ ker V_σ ∩ ℤ^{r_σ} : ‖z‖_∞ ≤ t}
     ≥ c_σ t^{d_σ} (q = t·1 + z ≥ 0; ker V_σ ∩ ℤ^{r} is a lattice of rank d_σ).
 So degree d_σ is attained only along rays in relint A_σ (in the lattice coset ℤV_σ); on relint F
 the growth degree is d_F ≤ d_σ, and P_σ = 0 off c_σ + ℕV_σ.

**Degree bound d_σ ≤ k (uniform in m) — PROVED.** w_t with exp w_t = c_σ + t u₀ has amb ≥ P_σ(t u₀) > 0,
so w_t ∈ L(G_m), |w_t| = n + ‖c_σ‖₁ + t‖u₀‖₁. By (L): c_σ t^{d_σ} ≤ C(n+‖c_σ‖₁+t‖u₀‖₁)^k for all t,
hence d_σ ≤ k. Only the exponent k enters (t → ∞ with n fixed), so the bound holds for every σ of every
G_m. (C and n affect constants only.)

## 3. §5 with partition functions — cases 1–4 SURVIVE (PROVED); bound ⌈m/2⌉
f(x,y) := Σ_σ P_σ((x,y) − c_σ) ≥ 1 on NE_M, = 0 on Δ. Let L_σ := supp P_σ(· − c_σ) = c_σ + ℕV_σ (an
affine monoid, not free). Since P_σ ≥ 0: L_σ ∩ Δ = ∅, ∪_σ L_σ = NE_M. Only the following are used.
Choose ω generic as before (outside ∂C_σ, C_σ = {u : (u,u) ∈ A_σ}). If ω ∈ int C_σ, let F be the face of
A_σ with (ω,ω) ∈ relint F; a W-ball around (ω,ω) lies in A_σ, and a segment of A_σ with midpoint in F
lies in F, so W ⊆ span F; Lemma X (PROOF.md §4, valid for dependent V) applied to V_F gives
dim F ≥ 2M−1. Hence: F = A_σ (dim 2M−1 or 2M) [cases 2,3] or F a facet of full-dim A_σ [case 4].

Two facts replacing the "lattice/positivity facts":
 (Lat) Let I_σ = [span V_σ ∩ ℤ^{2M} : ℤV_σ], I_F likewise; take N! divisible by all of them.
 (Deep) For a finite list V ⊂ ℕ^{2M}∖0, u₀ = Σv: there is K₀(V) with ℤV ∩ (K₀u₀ + cone V) ⊆ ℕV.
   (For y ∈ ℤV ∩ cone V write y = Σλ_j v_j, λ ≥ 0; e := y − Σ⌊λ_j⌋v_j lies in the finite set
   E = ℤV ∩ {Σμ_j v_j : 0 ≤ μ < 1}; e = Vz_e with z_e ∈ ℤ^V, so e + K₀u₀ ∈ ℕV for K₀ ≥ max_e‖z_e‖_∞;
   hence y + K₀u₀ ∈ ℕV.)
 Case 1 (ω ∉ C_σ): L_σ ⊆ c_σ + A_σ; unchanged.
 Cases 2,3 (F = A_σ): if some P(t₁,δ₁) ∈ L_σ then as in PROOF.md (λ-argument in case 2) (tω,tω) − c_σ ∈
   ℤV_σ by (Lat); (ω,ω) ∈ relint A_σ so (tω,tω) − c_σ − K₀u₀ ∈ A_σ for t large; (Deep) ⇒ (tω,tω) ∈ L_σ ∩ Δ.
   Contradiction; no P(t,δ) in L_σ.
 Case 4 (F facet, normal ν integral, ν ≥ 0 on A_σ, span F = ν^⊥): ψ_σ(δ) := ν(0,δ) ≠ 0 (ν vanishes on W).
   For |δ|_∞ ≤ R, t ≥ t₀(R): ψ>0 ⇒ P−c ∈ ℤV_σ (Lat) and P−c−K₀u₀ ∈ A_σ once N!/D_σ > ν(c_σ)+K₀ν(u₀)
   (other facets strictly positive near (ω,ω)) ⇒ P ∈ L_σ; ψ<0 ⇒ ν(P−c) < 0 ⇒ P ∉ L_σ; ψ = 0: the layer
   ν = h := −ν(c_σ) of ℕV_σ is E_h + ℕV_F with E_h finite (finitely many (q_j)_{v_j∉F} of ν-weight h);
   P(t,δ) − P(t,0) = N!(0,δ) ∈ N!(span F ∩ ℤ^{2M}) ⊆ ℤV_F; both points are deep in relint F, so by (Deep)
   for V_F: P(t,δ) ∈ L_σ ⇔ P(t,0) ∈ L_σ, false (Δ). So P(t,δ) ∈ L_σ ⇔ ψ_σ(δ) > 0, as before.
Conclusion unchanged: K = ∩_{σ∈𝓗}{ψ_σ ≤ 0} = {0}, |𝓗| ≥ M+1, and for generic δ
  f(P(t,δ)) + f(P(t,−δ)) ≥ Σ_{σ∈𝓗} P_σ(·) ≥ |𝓗| ≥ M+1 ⇒ some w ∈ Q ∩ R_m has amb(w) ≥ ⌈m/2⌉.
(The P_σ values on type-4 σ grow like t^{d_F} in t, but t ~ |w|/(2‖ω‖₁M), so this is ≤ poly(|w|) — no gain.)

**Length — NOT controlled; and irrelevant.** Witnesses need t ≥ t₀(R) > N!R with N! divisible by all
indices/determinants of G_m: no bound in m. Even ideally |w| ≥ 4m−2 (min length in R_m) gives only
amb ≥ m/2 ≈ |w|/8, i.e. amb = Ω(|w|) at best — consistent with C|w|^k for any k ≥ 1. And this is sharp
for the slice: §6 grammar "∃i x_i ≠ y_i" has amb ≤ m−1 ≤ |w|/4 on Q ∩ R_m. Route = registry BLOCKED
"R_m alone"; this report quantifies it.

## 4. Missing ingredient for superlinear (OPEN)
Any argument through one slice R with amb ≤ (inherent ambiguity of Q∩R) caps at that inherent value;
needed: a family of regular slices R_m ⊆ (ab*)^{n_m} whose non-primitive part is a union of many
periodicity subspaces Δ_d (d | n_m), plus a **cover-ply lemma**: every finite family of affine monoids
c + ℕV with laminar 2-supports, avoiding ∪Δ_d and covering ℕ^{n}∖∪Δ_d, has a point of ply
≥ superpoly(‖·‖₁ + n) at bounded norm (i.e. an *effective* §5 with ‖P‖₁ = poly(n) and ply ≫ n^k).
Partition-function degree cannot help: d_σ ≤ k by Part 2.
