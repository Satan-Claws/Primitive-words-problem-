# audit_ll.md — gated audit of r18_lightlight.md (Theorem LL)

**Verdict: SURVIVES (with caveats).** No fatal flaw found. Each of the targeted steps (a)–(e) checks out;
caveats are listed in §6.

Script: `scripts/audit_ll_search.py` (exhaustive search over small critical token sets + deep adversarial test).

## 1. (a) Lemma S2 — truncations are words of L, and the centre is irrelevant
- Linear SCC: each T-node has at most one T-child, so the spine is unique and every tree of 𝒫 decomposes uniquely into
  first-return tokens. Conversely ANY finite token sequence composes (X ⇒ u₁Xv₁ ⇒ u₁u₂Xv₂v₁ ⇒ …) and closes with the
  SAME fixed exit X ⇒* w. So W_r = p u₁⋯u_r w v_r⋯v₁ q ∈ L for every r. ✓
- Token order: the outer token is outermost, so the prefix of W_r is a prefix of p u₁u₂⋯ and the suffix of W_r is a suffix
  of ⋯v₂v₁q. ✓
- Centre moving with r: G⁻ is "d_k < 0 for all k ≤ n/2" and d_k reads only the first/last k letters. It does not use the
  centre. All that is needed is k ≤ n_r/2, which holds once |pU_r| ≥ k and |V_r q| ≥ k. ✓
- The "eventually one-side-growing" extension used in II.2(iii) (a₋ = 0 allowed): the test point K = |p| + m·a₊ satisfies
  K ≤ |pU_r| (with equality if a₋ = 0) and |V_r q| → ∞. So n_r ≥ 2K. ✓

## 2. (b) "Gaussian on (−∞,0] ⇒ σ² = 0": is d_∞ along one sequence the CLT object?
- Yes. d_∞(N) is a deterministic functional of ONE infinite sequence (τ_j). Lemma S2 says d_∞(N) < 0 for EVERY
  sequence with infinitely many nonempty u's and v's, so P_π(d_∞(N) < 0) = 1 for each N.
- The CLT is for the law of that same functional under i.i.d. τ_j ∼ π. It is not the law of the length-n word measure,
  so there is no "different truncations" mismatch: both A_∞ and B_∞ are read off the same (τ_j). The u- and v-coordinates
  of a token are correlated, and the 2-D CLT for (S^A, S^B) takes care of that.
- Variance formula re-derived: for a = N/μ_u > b = N/μ_v,
  S^A_a − S^B_b = Σ_{j≤b}(δ_u − δ_v)_j + Σ_{b<j≤a} δ_{u_j}, the two sums are independent, and
  Var = b·Var(δ_u − δ_v) + (a − b)·Var(δ_u). This matches the report (δ_slow = δ_u when μ_u < μ_v).
- Anscombe: N_A − a = O_P(√N) and the increments have mean 0, so S^A_{N_A} − S^A_a = O_P(N^{1/4}). The straddling
  token is O_P(log N) (exponential moments). ✓
- σ² = 0 ⇒ δ_u = δ_v a.s. (mean zero), and, if μ_u ≠ μ_v, δ_slow ≡ 0. So δ ≡ 0. The countable token set is fully charged
  by π, so these hold for every token. ✓

## 3. (c) Zero drift / polynomial ambiguity: per-word use is correct
- "Polynomially ambiguous" is used only as the per-word bound #trees(W) ≤ n^k. It gives
  #(trees in a bad set) ≤ n^k·#(image words) (prompt §2 reading). It is used in Step 1, Case I and Case II.1, each time
  as "≥ (c/2)·2ⁿ trees map into an exponentially small (or 2ⁿ/√n with m ≡ 1) word set". No total-tree-count misreading. ✓
- Zero drift really is needed. A nonzero drift of the right sign (δ_u < 0 < δ_v) is compatible with G⁻ (d → −∞), and
  it is killed only by counting. That counting is valid because the tree law conditioned on length n is the i.i.d. token
  law conditioned on a renewal epoch, which costs a factor ≤ 1/c.
- Spine uniqueness (§1) makes trees ↔ token sequences a bijection, so the c·2ⁿ count is a count of distinct trees. ✓

## 4. (d) Case II.2 adversary
- Tokens are freely concatenable (§1), so τ₊^m τ₋^∞ is realisable. Recomputed B(K): the reverse read takes |q| letters,
  then m·b₊ letters of the τ₊ v's, then j ≈ (mℓ₊ + |p| − |q|)/b₋ τ₋ v's. That gives d(K) = D(p) − D(q) − jδ₋ + O(b₋) → +∞,
  which contradicts S2 at a legal k. ✓
- (i): for a token or block with δℓ < 0, both u and v are nonempty (δ_u = δ_v ≠ 0), and the slope inequality fails in
  both sign cases. ✓
- (ii): in the closed Q1 ∪ Q3 with mean 0 and not all collinear, a non-antiparallel pair z₁ ∈ Q1\0, z₃ ∈ Q3\0 exists.
  The segment misses 0, an integer combination lands in an open Q2/Q4, and (i) applies to the block. Q1/Q3 points on
  the axes are fine: the sign change happens at an endpoint. ✓
- Exhaustiveness: (D) gives δ_u = δ_v and (μ_u = μ_v or δ ≡ 0). δ ≡ 0 is Case I. Otherwise μ_u = μ_v, and either ℓ ≡ 0
  (II.1) or ℓ ≢ 0 (II.2: (i), (ii), (iii) cover the slopes c < 0, non-collinear, and c > 0; slope ∞ is δ ≡ 0). ✓

## 5. (e) Configurations
- Theorem LL matches r18_gend §4.1's light/light bullet exactly: spanning critical linear T, light tokens on both
  sides, fixed context and exit. Spanning is not used.
- One-sided T is outside the theorem and is only sketched (Remark 5). The report says it is not needed for R⁻
  (left-good by LG(b), or no left letters). I did not re-audit that classification. It is inherited from r18_gend.
- Heavy sides belong to r18_gend2 and LG(c). Theorem LL does not touch them.

## 6. Experiments (`scripts/audit_ll_search.py`)
- Exhaustive search over all critical (Σ2^{−|u|−|v|} = 1) two-sided sets of distinct tokens with |u| + |v| ≤ 2:
  737 sets, 57 of them with exact zero drift.
- For every p, q with |p|, |q| ≤ 3 and every w with 1 ≤ |w| ≤ 3, all truncations up to depth 6 were tested. 160
  (set, p, w, q) tuples survive depth 6, e.g. T = {(ε,ab), (ε,ba), (a,a), (b,b)} with p = bbb, q = aa. They survive
  only because of the −(D(p) − D(q)) offset.
- This example is the generic Step-3 situation: δ_u = δ_v, but μ_u = ½ ≠ μ_v = 3/2 and δ ≢ 0, so σ² > 0. The block
  (a,a)(ε,ab) has slope 1 > 1/3, so the LLN Corollary kills it.
- Phase 2 (deep periodic and two-phase adversaries β₁^m β₂^40): see the result line below.

RESULT_PHASE2: of the 160 depth-6 survivors (8 token sets), the deep adversaries (blocks of length ≤ 2, β₁^m β₂^40 with
m ∈ {0, 5, 20}) kill every one except 124 tuples. Those 124 all belong to ONE token set,
T = {(ab,ε), (ba,ε), (ε,ab), (ε,ba)}, which is **Case I (δ ≡ 0)**. This is exactly the case that Lemma S2 and the CLT
cannot reach, and the report kills it by counting instead. That counting is valid: the grammar X → abX | baX | Xab | Xba
has C(r,i) interleavings per word, so it is exponentially ambiguous (≈ n·2^{n/2} words vs 2ⁿ trees).
So the experiment agrees with the report's case split. S2 together with the adversaries removes everything with
δ ≢ 0, and only the counting cases remain.

## 7. Caveats (non-fatal)
1. **Case II.1 depends on r17_gtrunk Lemma 1 (IF/SU from C_exp-freeness).** n^k ambiguity alone does not beat
   c·2ⁿ vs C·2ⁿ/√n. The audit status of IF is inherited.
2. **Step 3 is "standard" but written tersely.** The joint renewal-reward CLT with two different renewal clocks
   (N_A, N_B) on one sequence deserves a displayed lemma. I re-derived it (§2) and found no gap.
3. **Periodicity.** The tree count holds only along the lattice of token lengths. Step 1, Case I and Case II.1 must
   pick n in that progression. This is harmless, but it is not spelled out in every step.
4. **The one-sided case is a sketch.** Its exclusion from R⁻ rests on r18_gend's LG(b) classification.
5. **"Light" is used only for exponential moments** (Cramér in Step 1, the O(log N) straddle bound). It is also used
   for the analyticity argument ρ(J_R(½)) < 1, which is a correct Perron–Frobenius strict-monotonicity step.
