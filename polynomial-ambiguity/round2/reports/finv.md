# R2/finv: refinement-invariant length side — work with f = amb directly

Setting: prompt §§4.3, 4.4(ii); R2/g3.md (Prop BC, §3(a) Stanley refinement, §4 Lemma F_S + Cor F′); R2/recon.md
(Lemma 3P, Lemma F repaired). f(x) = Σ_σ P_σ(x − c_σ). Every quantity below is a function of f alone, so it is
unchanged when the cover is refined. Scripts: `round2/scripts/finv_crt_search.py`, `finv_crt_check.py`.

**Verdict.**
- (a) Ehrhart/QP onset is not the bottleneck: f equals its chamber quasi-polynomial already at depth ≤ ‖c‖ + rK.
- (b) Monotonicity propagates only outward. It is useless for pulling high ply back towards the apex.
- The requested transfer "f ≥ q asymptotically along a ray (lim sup / on a progression / in the QP leading
  coefficient pointwise) ⇒ f ≥ q at small norm" is **FALSE**, and the obstruction is refinement-invariant.
  - Counterexample (§3): CRT pieces, full rank, laminar, d = 0, K = 3. They are added to any valid cover.
  - The result is f = f₀ + q far out, but f ≤ f₀ + O(1 + log R / m) on the R-ball.
- What does transfer is the **asymptotic density** ρ (the leading Ehrhart coefficient, §4, Lemma D). Its bound
  depends only on the facet height at ω of the *coarsest* representation of f.
  - So g3 §3(a) (refinement) no longer bites.
  - The genuine (non-refinement) chain pieces with height 2^ρ remain the exact gap.

## 1. Onset of the quasi-polynomial regime (PROVED / [published] input)
For d_σ = 0 and B = V_σ independent: c + ℕB = (c + cone B) ∩ (c + ℤB). So 1_{L_σ} *is* its quasi-polynomial
(a coset indicator) on the whole closed shifted cone, with no onset delay.
For d_σ > 0, Szenes–Vergne (2003) / Brion–Vergne give the following. P_V agrees with the quasi-polynomial of a
chamber 𝔠 on (𝔠̄ − □(V)) ∩ ℤ^n, where □(V) = Σ[0,1]v.
Hence f agrees with one QP on ∩_σ(c_σ + C̄) for every cell C of the common chamber refinement, i.e. from depth
ν(x) ≥ max_σ ν(c_σ) ≤ ‖ν‖_∞·nK on each facet ν of C.
**So candidate (a) reduces to the same two numbers as Prop BC:** the facet heights of the cells, and the period
lattice. It gives nothing new.

## 2. Monotonicity (PROVED, negative)
P_σ(x + v) ≥ P_σ(x) for v ∈ ℕV_σ. Therefore f(x + v) ≥ f(x) for v ∈ ∩_{σ active at x} ℕV_σ.
This moves high values *outward* only.
The pull-back f(x − v) ≥ f(x) fails already for a single piece: take x = c, v ∈ V.
In §3, every pull-back of a ply-q point to norm < R_s loses all but s − 1 pieces.

## 3. CRT obstruction: refinement-invariant, full rank (PROVED; [computational] check)
Blocks 0..m−1 and ℓ(x) := Σ_j (−2)^j x_j.
- Chain C = {2e_j + e_{j+1} : j < m−1}. Since e_{j+1} ≡ −2e_j mod ℤC, ℤ^m/ℤC ≅ ℤ via ℓ, so **ℤC = ker ℓ ∩ ℤ^m**.
- For t ∈ T := {odd primes in [m/2, m)}, put w_t = e_0 + e_t, with ℓ(w_t) = −D_t, D_t = 2^t − 1.
  - gcd(D_t, D_t') = 2^{gcd(t,t')} − 1 = 1, so the D_t are pairwise coprime.
- B_t := C ∪ {w_t} is laminar: the pairs {j,j+1} and {0,t} never cross.
  - It is independent, with d = 0, entries ≤ 2 and ‖v‖₁ ≤ 3.
  - **ℤB_t = {x : ℓ(x) ≡ 0 mod D_t}**, of index D_t.
- ω := 2(2,3,…,3,1) + e_1 lies in the open cone of every B_t. In chain coordinates the correction has size
  ≤ 2·2^{t−1}/(2^t−1)·const, which is below 1.
- Offsets: c_t = 1 + negabinary digits of a residue r_t, so ‖c_t‖₁ ≤ 2m. Put A_t := c_t + ℕB_t.

**Claim.** For a suitable choice of residues (r_t), f_CRT := Σ_t 1_{A_t} satisfies, for every s ≥ 3,
  f_CRT(x) ≥ s ⇒ ‖x‖₁ > R_s := 2^{s(m/2 − 2 − log₂ m) − m − 3}.
Equivalently, max_{‖x‖₁ ≤ R} f_CRT ≤ 2 + (log₂ R + m + 3)/(m/2 − 2 − log₂ m) = O(1 + log R / m).
At the same time f_CRT = q := |T| ≈ m/(2 ln m) at some point, and on a whole progression of every ray in direction ω.

*Proof.*
1. If x ∈ A_t, then ℓ(x) ≡ r_t (mod D_t).
2. If x lies in the pieces of a set T′ with |T′| = s, then ℓ(x) lies in one CRT class mod L_{T′} = ∏_{T′} D_t,
   and L_{T′} ≥ 2^{s(m/2−1)}.
3. Also |ℓ(x)| ≤ 2^{m−1}‖x‖₁.
4. Take the r_t uniform and independent. Each class is uniform mod L_{T′}, so it meets [−Y, Y] with
   probability ≤ (2Y+1)/L_{T′}.
5. Put Y = 2^{m−1}R_s. The union over ≤ m^s sets T′ and over s ≥ 3 has total probability
   Σ_s m^s 2^{m+log R_s+1−s(m/2−1)} ≤ Σ_s 2^{−s−2} < 1. So good residues exist.
6. For the far point: by CRT and full rank, the coset ∩_t(c_t + ℤB_t) is a coset of a full-rank lattice. So it
   contains points of tω + (bounded) arbitrarily deep in every cone. Then x − c_t ∈ cone ∩ ℤB_t = ℕB_t. ∎

*Check* (`finv_crt_check.py`, m = 30, 9 pieces).
- Verified: laminarity, |det B_t| = D_t, ω interior, offsets.
- The far point x = Sω + k e_0 with S = 2^170 has f = 9 (norm ≈ 2^177).
- 3000 random x for each norm 10..10^5 give congruence count ≤ 2.
- `finv_crt_search.py` shows the obvious alternative (ℓ = (1..m)) fails. Large coprime indices need a form with
  exponential coefficients, which chains supply.

**Validity embedding** (abstract; grammar realisability NOT checked).
- Use the Lemma F_S face of (ab⁺)^n (g3 §4): I = [1..m], m ≤ n/6, every other coordinate 1.
- Lift A_t with offset 1 + c_t + e_0. Every point has z_1 ≥ 2 ≠ 1 = z_{1+n/2}, so it is primitive.
- Hence for **any** valid cover F₀, the cover F₀ ∪ {A_t} is valid and laminar per skeleton, with K = 3 and
  offsets ≤ n + 3m.
- Its f = f₀ + f_CRT has
  - lim sup along a ray ≥ f₀ + q, with q = Θ(m/log m);
  - max over the R-ball ≤ max f₀ + O(1 + log R/m).
- This also answers T2b's remark "no full-rank exponential example": here the example is full rank and is a
  level set of f, so it is refinement-invariant.
- It is *not* a counterexample to Lemma G*. The added ply is unforced, and Cor F′ still forces f₀ ≥ p at
  n·exp(O(p² log pK)).
- In particular the literal target "f ≤ 2 until R = exp(n^{Ω(1)})" is impossible on S_N, by g3 §4.

**Consequence.** No length argument can use asymptotic ply in the lim-sup / per-progression / pointwise-QP sense.
A length argument must either:
- (i) use the covering property at the near scale, i.e. G* itself; or
- (ii) use an *averaged* asymptotic quantity, §4.

## 4. Density transfer (PROVED for full-rank pieces, e.g. on Lemma F faces)
Write ρ(ω) := Σ_{σ : ω ∈ int cone V_σ} 1/[ℤ^m : ℤV_σ] over d = 0 pieces.
- ρ(ω) = lim_{R→∞} lim_{t→∞} avg_{tω+[0,R)^m} f, so ρ is a function of f. Stanley refinement preserves it.
- For d > 0 use f ≥ Σ 1_{L_σ} as a lower bound.
- In §3, ρ_CRT = Σ 2^{−t} < 2^{1−m/2}, which is consistent with the lemma below.

**Lemma D.** Let ω ∈ ℤ^m_{≥1}, ρ(ω) ≥ q, R := 2m²Kq.
- Put h := max over the pieces σ counted in ρ(ω), and over the primitive facet normals ν of cone V_σ, of
  ‖ν‖_∞/ν(ω).
- Put t := h(nK + mR).
- Then max f over tω + [0,R)^m is ≥ q. That point has ‖x‖₁ ≤ t‖ω‖₁ + mR = poly(m, K, q, ‖ω‖)·h.

*Proof.*
1. For x = tω + z with ‖z‖₁ ≤ mR: ν(x − c_σ) ≥ tν(ω) − ‖ν‖_∞(mR + nK) ≥ 0. So the box lies in c_σ + cone.
2. The fundamental parallelepiped of V_σ has ℓ∞-diameter ≤ mK. So the box has ≥ (R − mK)^m/idx_σ points of
   the coset, all in L_σ.
3. Hence avg f ≥ ρ(1 − mK/R)^m ≥ q(1 − 1/(2q)) = q − 1/2.
4. f is integer-valued, so max f ≥ q. ∎

h may be taken from **any** representation of f, in particular the coarsest one (refinement only adds walls).
The box needs side only mK, not lcm(E_σ) and not μ(Λ_S). So L = lcm E_σ disappears entirely: index costs
nothing for density.

**Exact gap (refinement-invariant).**
- (G-ρ) Density-TILE: is ρ(ω) ≥ n^{ω(1)} forced at some ω by validity on S_N?
  - Real-cone ply (TILE_k) does not imply it: Stanley refinement has real ply 2^ρ with ρ = 1.
  - The S_N subspace W needs Lemma D with lattices ℤV_σ ∩ W (not done).
- (G-h) Coarsest-representation facet height h at that ω must be n^{o(N)}.
  - Genuine chain rings (Y → bYbb) give h = 2^ρ. Refinement can no longer be blamed, but no argument rules
    them out.
- OPEN.

## 5. Status
- §1: PROVED (with Szenes–Vergne [published]).
- §2: PROVED.
- §3: PROVED, [computational] check. The face embedding is abstract; realisability is unchecked.
- §4 Lemma D: PROVED for full-rank pieces.
- G-ρ, G-h: OPEN.
