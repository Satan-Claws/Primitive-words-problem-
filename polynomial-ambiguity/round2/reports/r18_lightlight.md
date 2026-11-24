# r18_lightlight.md — R18-LL: the light/light critical linear SCC in G⁻

Status (honest):
- **Light/light case: CLOSED** [written proof, Theorem LL below]. In a reduced, ε-free, polynomially ambiguous G with
  L(G) ⊆ G⁻, **no** critical linear SCC T has light tokens with both sides nonempty. "Light" means the side material
  has radius > ½, finite sides included. Spanning is not needed.
- So the light/light part of r18_gend's R⁻ is **vacuous**. Together with r18_gend2 (light-or-finite-left / heavy-right),
  **R⁻ is empty.**
- **No (AM)-type multiplicity bound is used.** Multiplicity enters only once, in Case II.1, where the exit position is
  pinned and r17_gtrunk Lemma 1 gives m ≡ 1.
- **Inputs.**
  - Polynomial ambiguity: #trees ≤ n^k·#words, and IF/Lemma 1 (r17_gstruct, r17_gtrunk; both audited, SURVIVE).
  - Criticality plus lightness: renewal mass u(n) → const > 0, and exponential moments.
  - Standard probability: Cramér, the renewal-reward CLT with Anscombe, and the return-count large deviation.
- **Mechanism.** The two "single-word density" objections in the brief do not apply, because the contradiction is on
  the **tree measure**, not the word measure:
  - **every** tree of the pair family yields a word in G⁻;
  - the tree measure is an i.i.d. product of tokens;
  - and one read of a single infinite token sequence serves **all** lengths n at once.
  So G⁻ becomes a **deterministic, almost-sure** statement about a mean-zero renewal-reward walk, and a CLT kills it
  unless the walk is degenerate. The degenerate cases are then ruled out one by one: by counting (Case I), by exit
  pinning plus Lemma 1 (Case II.1), and by explicit adversarial token sequences (Case II.2).

Script: `scripts/r18_ll_checks.py` → `scripts/r18_ll_checks_out.txt` (~4 s). Results:
- **(1) Case I.** The exact fraction of words with ≥ 0.15n visits to level 0 is 2.2e−1, 1.1e−1, 2.2e−2, 4.8e−3 for
  n = 50, 100, 200, 300. Its rate, −log(fraction)/n, falls from 0.030 to 0.018 and is still decreasing. The Chernoff
  bound used in Case I gives the rate 0.0133, which is consistent with this.
- **(2) Step-3 variance formula.** It matches Monte Carlo to within about 5% on 4 random symmetric laws
  (e.g. 1.357 vs 1.340).
- **(3) Case II.2(iii) adversary.** Each token alone satisfies the slope condition, but d(3m) = 2, 2, 4, 8, 14, 28 for
  m = 1, 2, 5, 10, 20, 40, so d grows linearly.
- **(4) Step 3 empirically.** In 190 of 192 random mean-zero non-degenerate laws, one sampled sequence already reaches
  d ≥ 0 by k = 2000.

Notation is as in r18_gend / r18_gend2. Steps are ±1. A(k) = P(k) and B(k) = P(n) − P(n−k), and
G⁻ = {A(k) < B(k) for 1 ≤ k ≤ n/2}.

## 0. Setting
- T is a critical linear SCC, and X ∈ T.
- Fix any context tree S ⇒* pXq (one exists, since G is reduced) and any exit X ⇒* w.
- The pair family 𝒫 is the set of trees "context · first-return T-tokens τ₁…τ_r · exit". Here τ_i is a first-return
  pumping tree X ⇒⁺ u_i X v_i, and every finite token sequence is allowed. The word is W = p u₁⋯u_r w v_r⋯v₁ q.
- Token law: π(τ) = 2^{−|u|−|v|}.
- **Criticality** means Σπ = 1.
- **Light/light** means every side branch of a T-rule (left and right) has radius > ½.
  - Then the first-return generating function at X is analytic beyond ½. The reason: it equals J_XX + J_X,R(I − J_R)⁻¹J_R,X,
    and the proper principal submatrix J_R(½) of the irreducible J_T(½) has spectral radius < 1.
  - Hence |u| + |v| has exponential moments under π.
- **Two-sided** means π(u ≠ ε) > 0 and π(v ≠ ε) > 0. One-sided T are treated in Remark 5.
- Write μ_u = E|u| > 0, μ_v = E|v| > 0, δ_u = D(u), δ_v = D(v).
- **Tree count.** By the renewal theorem, #{t ∈ 𝒫 : |t| = n} ≥ c·2ⁿ along a progression of n (the period of the
  token lengths).

## 1. Step 1: zero drift on each side [written proof; this is r18_gend §4.2 made rigorous]
**Claim.** E δ_u = E δ_v = 0.

**Proof.**
1. Put θ := μ_u/(2(μ_u + μ_v)) and k₀ = ⌊θn⌋.
2. Under the length-n tree law, Cramér for the renewal-reward pair (Σ|u_j|, Σδ_{u_j}) applies, since tokens have
   exponential moments. Conditioning on "n − c₀ is a renewal epoch" costs only a factor 1/c. So, outside an
   exponentially small fraction of trees:
   - k₀ < |pU|;
   - |A(k₀) − k₀·Eδ_u/μ_u| ≤ εn.
3. Suppose Eδ_u ≠ 0. Then those trees have words with |P(k₀)| ≥ c′n.
4. Such words number ≤ 2ⁿ·2e^{−c″n} (Hoeffding).
5. But polynomial ambiguity gives #trees ≤ n^k·#words. Comparing with the tree count c·2ⁿ in §0 is a contradiction.
6. The claim for δ_v is the mirror argument, read from the end of W. ∎

## 2. Step 2: the deterministic infinite constraint [written proof]
**Setup.** Let τ₁τ₂… be an infinite token sequence with infinitely many u_j ≠ ε and infinitely many v_j ≠ ε. Define:
- A_∞(k) as the prefix walk of the infinite word p u₁ u₂ ⋯;
- B_∞(k) as the walk of the last k letters of ⋯ v₂ v₁ q, read from the right;
- d_∞ := A_∞ − B_∞.

**Lemma S2.** d_∞(k) < 0 for **every** k ≥ 1.

**Proof.**
1. Fix k. Choose r so large that |pU_r| ≥ k and |V_r q| ≥ k.
2. Then W_r := p u₁⋯u_r w v_r⋯v₁ q ∈ L ⊆ G⁻, and n_r ≥ |pU_r| + |V_r q| ≥ 2k.
3. The first k letters of W_r are those of p u₁u₂⋯, and the last k letters are those of ⋯v₂v₁q.
4. So A_{W_r}(k) = A_∞(k) and B_{W_r}(k) = B_∞(k). Since W_r ∈ G⁻ and k ≤ n_r/2, A_∞(k) < B_∞(k). ∎

The same holds if the sequence is only **eventually** in a set on which one side keeps growing, as long as the k being
tested satisfies k ≤ |pU_r| for large r. This is used in §4.

**Corollary (LLN form).** Repeat any finite token block β = τ_{i₁}⋯τ_{i_s} forever. Then the slopes satisfy
D(u_β)/|u_β| ≤ D(v_β)/|v_β|. If u_β = ε, this is read as "no constraint"; if v_β = ε, the block is not admissible.
- *Proof.* Otherwise d_∞(k) ≥ c·k − O(1) → +∞. ∎

## 3. Step 3: CLT ⇒ degeneracy [written proof]
Let the τ_j be i.i.d. ∼ π. By Lemma S2, almost surely d_∞(N) < 0 for all N.

**Expansion of d_∞(N).** Let S^A_i = Σ_{j≤i} δ_{u_j}, S^B_i = Σ_{j≤i} δ_{v_j}, and let N_A(N), N_B(N) be the numbers
of complete tokens inside the first N letters on each side. Then

  d_∞(N) = S^A_{N_A(N)} − S^B_{N_B(N)} + O(max_{j≤2N}(|u_j| + |v_j|) + |p| + |q|).

The error term is O_P(log N).

**Limit law.**
- N_A(N)/N → 1/μ_u almost surely, and N_A(N) − N/μ_u = O_P(√N).
- Step 1 gives mean-zero increments. So Anscombe's theorem gives S^A_{N_A} = S^A_{⌊N/μ_u⌋} + o_P(√N), and the same
  for B.
- The 2-D CLT for (S^A, S^B) at the fixed indices a = N/μ_u and b = N/μ_v then gives d_∞(N)/√N ⇒ 𝒩(0, σ²), with

  σ² = Var(δ_u − δ_v)/max(μ_u, μ_v) + Var(δ_slow)·|1/μ_u − 1/μ_v|.

  Here δ_slow is δ_u if μ_u < μ_v, and δ_v otherwise. To see this, split S^A_a − S^B_b at min(a, b) into two
  independent pieces.

**Conclusion.**
- The limit is supported on (−∞, 0], because d_∞ < 0 almost surely.
- A centred Gaussian supported on (−∞, 0] has σ² = 0.
- π charges every token. Therefore **every** token satisfies

  (D) δ_u = δ_v,  and  (μ_u = μ_v or δ_u ≡ 0).

This leaves three cases:
- **Case I:** δ_u ≡ δ_v ≡ 0.
- **Case II.1:** δ_u = δ_v and |u| = |v| for every token.
- **Case II.2:** δ_u = δ_v, μ_u = μ_v, δ ≢ 0, and ℓ := |u| − |v| ≢ 0.

## 4. The degenerate cases [written proofs]
**Case I (all tokens balanced on both sides).**
1. In every tree, P returns to the level D(p) at every left token boundary.
2. Under the length-n tree law, outside an exponentially small fraction, there are ≥ εn distinct such positions,
   since ε < π(u ≠ ε)/(μ_u + μ_v).
3. Words whose walk visits a fixed level at ≥ εn positions number ≤ (n+1)·2ⁿ·e^{−c(ε)n}.
   - The inter-visit times of SRW are i.i.d. with E e^{−θT} = 1 − √(1 − e^{−2θ}).
   - So P(#visits ≥ εn) ≤ exp(n(θ + ε·log(1 − √(1 − e^{−2θ})))), which is < e^{−cn} for small θ.
4. Polynomial ambiguity then gives a contradiction exactly as in Step 1.
- Script (1) checks the decay exactly.

**Case II.1 (|u| = |v| and δ_u = δ_v for every token).**
1. Every tree of length n has |U| = |V| = (n − c₀)/2. So the exit node has the same span in all of them.
2. By r17_gtrunk Lemma 1, which needs IF and therefore C_exp-freeness (that is, polynomial ambiguity), 𝒫_n → words is
   **injective**.
3. All these words have D(U) = D(V) on two fixed disjoint windows of length (n − c₀)/2, so there are ≤ C·2ⁿ/√n of them.
4. That is fewer than c·2ⁿ trees, a contradiction for large n.

**Case II.2 (μ_u = μ_v, δ_u = δ_v =: δ, δ ≢ 0, ℓ ≢ 0).** Put z_τ = (δ_τ, ℓ_τ). The π-mean of z_τ is (0, 0) by
Step 1 and μ_u = μ_v.
- **(i)** Some token has δℓ < 0.
  - Take δ > 0 and ℓ < 0. Then |v| > |u| > 0, since δ ≠ 0 forces u ≠ ε.
  - Repeating this token gives slope δ/|u| > δ/|v|, which violates the LLN Corollary.
  - The case δ < 0, ℓ > 0 is symmetric: the slope δ/|u| > δ/|v|, i.e. A is less negative.
- **(ii)** All tokens have δℓ ≥ 0, but the z_τ are not all on one line through 0. Mean zero gives tokens τ₁ with z₁ in
  the closed first quadrant Q1 \ {0} and τ₃ with z₃ in Q3 \ {0}, and they can be chosen not antiparallel.
  - The segment [z₃, z₁] misses 0. Its x- and y-coordinates change sign at different parameters. Between those
    parameters the segment lies in the open Q2 or the open Q4.
  - Pick integers s₁, s₃ ≥ 1 with s₁z₁ + s₃z₃ there.
  - The block β = τ₁^{s₁}τ₃^{s₃} has δ_β·ℓ_β < 0, which is excluded by (i) applied to β.
- **(iii)** z_τ = (δ_τ, cδ_τ) for every τ, with a fixed c > 0. Slope 0 would mean ℓ ≡ 0, and a vertical line would mean
  δ ≡ 0. Take τ₊ = (u₊, v₊) with δ₊ > 0 (so a₊ := |u₊| > b₊ := |v₊|), and τ₋ with δ₋ < 0 (so b₋ > a₋ ≥ 0).
  - Feed the sequence τ₊^m τ₋^∞. Lemma S2 applies: v grows, and the test point K below satisfies K ≤ |pU|.
  - At K = |p| + m·a₊ (the end of A's τ₊-block), A(K) = D(p) + mδ₊.
  - B has used m·b₊ letters on τ₊-tokens and then j = ⌊(mℓ₊ + |p| − |q|)/b₋⌋ full τ₋-tokens. So
    B(K) = D(q) + mδ₊ + jδ₋ + O(b₋).
  - Therefore d(K) = −jδ₋ + O(1) ≥ m·ℓ₊/b₋ − O(1) → +∞. This contradicts Lemma S2.
  - Script (3) runs this for τ₊ = (aab, a) and τ₋ = (b, abb).

**Theorem LL.** Let G be reduced, ε-free and polynomially ambiguous, with L(G) ⊆ G⁻. Then G has no critical linear SCC
with light, two-sided tokens.

*Proof.* Cases I, II.1 and II.2 exhaust (D), and each one is contradictory. ∎

## 5. Remarks
- **Where criticality enters.** Only in Step 1 (zero drift, through the tree count c·2ⁿ) and in Cases I and II.1
  (counting). Subcritical T are invisible here, as they should be: their tree mass is exponentially small.
- **One-sided T (all v = ε, light, critical)** [written sketch].
  - Lemma S2 is not available, because both A and B read U.
  - Under the length-n tree law the beginning and the end of U are asymptotically independent, so
    d(tn)/√n ⇒ W₁(t/μ) − W₂(t/μ) with W₁, W₂ independent Brownian motions.
  - Hence P_n(d ≤ 0 on [δn, n/2]) → P(·) < 1. But P_n(G⁻) = 1 for the tree law. So σ² = 0, i.e. δ ≡ 0, and Case I
    counting finishes.
  - This is not needed for R⁻: pure-left T is left-good (LG(b)) or carries no left letters.
- **Relation to (AM).** Theorem LL does **not** prove (AM) or Conjecture CR. Those concern two-sided **level**
  (heavy, β₀ < 1) critical SCCs, where the tree count is 2ⁿn^{β₀−1} and Step 1's counting is too weak. It only shows
  that in G⁻ the light/light obstruction is not reached in the first place. The SH6 question (r18_am) is unaffected.
- **Consistency with SH6 (r18_sh6).** Without G⁻, E_n[m] = o(n) is false: SH6 has E_n[m] − 1 ≈ 0.0073n. Theorem LL
  does not contradict this, for two reasons:
  - it never bounds multiplicity, and G⁻ enters essentially (Lemma S2 is the chord condition read on one infinite token
    sequence);
  - SH6 has Dyck tokens, which are heavy, so it is not light/light at all.
  - SH6's escape from G⁻ (d_k > 0 at k = |p| + m on p·aᵐbᵐ·a·ab·aᵐbᵐ·bb·q) is the same kind of adversarial token block
    as §4 (iii).
- **Why the brief's worry ("G⁻ has density n^{−½}, so not immediately contradicted") does not bite.** The density of
  G⁻ among words is irrelevant. What matters is that the **tree** process is i.i.d., and G⁻ must hold for **all** of
  its realisations. A deterministic constraint on a non-degenerate mean-zero CLT walk is impossible.

## Status
| item | label |
|---|---|
| Step 1: E D(u) = E D(v) = 0 (light critical, poly-ambiguous) | written proof |
| Lemma S2: d_∞(k) < 0 for every infinite two-sided token sequence | written proof |
| Step 3: CLT ⇒ (D): δ_u = δ_v and (μ_u = μ_v or δ ≡ 0) | written proof (standard Anscombe/renewal CLT) |
| Case I (balanced tokens): visit-count LD + poly ambiguity | written proof + exact check |
| Case II.1 (\|u\| = \|v\|): exit pinned ⇒ m ≡ 1 (Lemma 1) ⇒ count 2ⁿ/√n contradiction | written proof |
| Case II.2: LLN on blocks (convex-hull lemma) + two-phase adversary τ₊^mτ₋^∞ | written proof + script |
| **Theorem LL: no critical light/light linear SCC in poly-ambiguous L ⊆ G⁻** | **written proof** |
| R⁻ (r18_gend §4) | **empty**: light/light by LL, light-left/heavy-right by r18_gend2 |
| One-sided light critical T | written sketch (not needed) |
