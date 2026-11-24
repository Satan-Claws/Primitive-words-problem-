# R2/gglob: the G-glob gap (large-scale sparse mixed-type defects)

W4, 2026-11-24. Script: `round2/scripts/gglob_matching.py` (≈ 5 s with arguments `200 20`).
Notation as in `R2/global.md`: n = P², V_k = s_k-periodic vectors (s_k = n/p_k), A(δ) = {k : δ ∉ V_k} = ⋃{T : δ_T ≠ 0}.
For a matching M: L(M) = span{e_p + e_q : pq ∈ M} (the pair-constant vectors), A(M) = span{e_p − e_q : pq ∈ M}, and
d_M(y) = (y_p − y_q)_{pq∈M}.

**Verdict.** Direction (A) collapses. With K = 2, laminarity enters G4 only through one non-crossing matching per
piece (Lemma G5). The resulting criterion is linear algebra, and random NC matchings satisfy it for every tested
sparse mixed defect, so it gives no set-cover or hitting-set obstruction. Direction (B) is not finished. global.md's
"per-prime σ-or-d" recursion is an artifact of fixing the adjacent matching: the right recursion is "∃M ∀k", with no
2^N factor. That leaves one exact gap, G-glob′ (§4).

## 1. Lemma G5 (matching reduction of G4 at K = 2) [written proof, modulo the convex separation of G4]
**Setup.** Let c + ℕV be a laminar piece (K = 2, d_σ = 0, rank n). It contains x = t·1 + sδ + η for unboundedly
many t ≫ s ≫ 1.
- Ring coordinates are q = V⁻¹(x − c) = tV⁻¹1 + sV⁻¹δ + V⁻¹(η − c).
- Put F₁ = supp V⁻¹1 and L₁ = span F₁. Put F₂ = F₁ ∪ {v : (V⁻¹δ)_v > 0} and L₂ = span F₂.
- Every coordinate of x is ≈ t, so the F₁-rings cover every position.

**Claim.** There is a non-crossing (partial) matching M with L₁^⊥ ⊆ A(M). Consequently:
- for k ∈ A(δ), a certificate exists only if δ ∉ V_k + L(M), that is, d_M(δ) ∉ d_M(V_k);
- for k ∉ A(δ), a certificate exists only if η ∉ V_k + L(M) + ℝδ, since L₂ ⊇ L₁ + ℝδ.

**Proof.**
1. *Shape of L₁^⊥.* With K = 2, a two-point ring is e_p + e_q, and the one-point rings are e_p and 2e_p.
   - A component C of the F₁ ring graph that contains a one-point ring spans ℝ^C.
   - Otherwise C is a tree of edges e_p + e_q, since d_σ = 0. Its span is ν_C^⊥, where ν_C ∈ {±1}^C is the
     bipartition sign.
   - 1_C ∈ cone forces ν_C(1_C) = 0, so C is balanced.
   - So L₁^⊥ = span{ν_C : C balanced}. The components are the blocks of a non-crossing partition.
2. *Ballot step.* A balanced ±1 sequence on the cyclically ordered set C has a non-crossing perfect matching M_C
   that pairs + with − (match parentheses after rotating to a ballot sequence). Then ν_C = Σ_{pq∈M_C} ±(e_p − e_q).
3. *Combining blocks.* The blocks are pairwise non-crossing, so M = ⋃ M_C is non-crossing, and L₁^⊥ ⊆ A(M).
4. *Certificates.* Prime k is certified at level t iff some μ ∈ L₁^⊥ ∩ V_k^⊥ has μ(δ) > 0. Write μ = Σ a_pq(e_p − e_q).
   Then μ ⊥ V_k ⇔ a ⊥ d_M(V_k). Such a with a·d_M(δ) ≠ 0 exists iff d_M(δ) ∉ d_M(V_k).
5. *Level η.* Take k ∉ A(δ). Then μ ≥ 0 on the F₂-rings and μ(δ) = 0, so μ ⊥ L₂. ∎

**Consequences.**
- The extra structure laminarity adds to G4 is exactly the choice of one NC matching M, shared by all primes and by
  both levels. Certificate supports may overlap (as in G3).
- **The σ/d OR is an artifact.** For the adjacent matching M₀, d_{M₀} is global.md's d. Its σ-branch corresponds
  to the primes that M₀ cannot certify, and those must be handled by *another matching*, not by recursing on σ.
  The correct recursion is "∃M ∀k", followed by one signed sub-instance on d_M-space of dimension n/2. Level-s rings
  e_p + e_q map there to ±e_a ± e_b. This has no 2^N factor and no squaring.
- **Shift certificates.** Suppose M is invariant under the shift by s_k (for example, P-periodic). Put
  g_k := y − T^{−s_k}y. Then g_k ∉ L(M) already certifies k, via μ = (1 − T^{s_k})(e_p − e_q).
  - For M₀ and M₁ (the adjacent matchings, shift-2 invariant), g_k ∈ L(M₀) ∩ L(M₁) means g_k is constant, hence 0.
  - So **for each single k**, M₀ or M₁ works. What fails is using one matching for all k (Lemma G6).

## 2. Lemma G6 (two adjacent matchings do not suffice) [written proof + exact example]
- dim(V_k + L(M₀)) = n/2 + n/(2p_k). At n = 36: 27 for p = 2 and 24 for p = 3.
- So (V₂ + L(M₀)) ∩ (V₃ + L(M₁)) has dimension ≥ 15. It contains primitive y, for example
  y = (−2,−1,1,−4,4,0,0,3,3,2,3,−1,−2,−1,1,−2,6,3,3,4,4,−1,0,−4,−5,−2,0,−1,7,3,3,4,4,1,2,−1) (Part C).
- Neither M₀ nor M₁ certifies all k for this y. 248 of 300 random NC matchings do.
- So any affirmative construction needs a genuinely varying matching family, not only the σ/d split.

## 3. Exact tests at N = 2, 3 [computational]
Uniform random NC perfect matchings (cycle lemma, random rotation). Exact rank mod 2³¹−19.

| n | defect y (sparse, mixed types) | \|supp\| | M₀, M₁ ok | random NC M certifying all k |
|---|---|---|---|---|
| 36 | 1_D + 1_T (G2) | 5 | yes, yes | 200/200 |
| 36 | Σ_k 1_{s_k-orbit} | 5 | yes, yes | 200/200 |
| 36 | random 6-point, entries ±1, ±2 | 6 | yes, yes | 183/200 |
| 900 | 1_D + 1_T | 5 | yes, yes | 20/20 |
| 900 | Σ_k 1_{s_k-orbit} | 10 | yes, yes | 20/20 |
| 900 | 1_{X₁₃} + 1_{X₂₃} + 1_{X₁₂} (orbits of n/(p_ip_j)) | 29 | yes, yes | 20/20 |
| 900 | random 6-point | 6 | yes, yes | 20/20 |
| 36 | Lemma G6 y | 34 | **no, no** | 248/300 |

**Two-level G-glob condition (Part B).** Here δ ∈ V_{k*} (A(δ) = [N] ∖ {k*}), η is e_q or a sparse orbit, and the
test is the full Lemma G5 condition on both levels.

| n | M satisfying the full condition, η = e_q | η = sparse orbit |
|---|---|---|
| 36 | 202/202 | 202/202 |
| 900 | 22/22 | 22/22 |

There is no sign of a defect family whose certifiable matchings are rare.

## 4. Exact remaining gap
**G-glob′ (affirmative side).** Two parts remain open.
- **(i) Level t.** Find a distribution 𝒟 on NC matchings of ℤ_n with
  Pr_{M∼𝒟}[∀k: y ∉ V_k + L(M)] ≥ n^{−O(1)} for every y ∉ ⋃_k V_k.
  - Heuristic: each single-k bad event has probability ≤ ≈ 3/4 (a non-constant g_k must not be split by M). If the
    N bad events were independent or positively correlated, this would give ≥ (1/4)^N = n^{−o(1)}.
  - The union bound fails, and I have no correlation inequality for NC matchings.
- **(ii) Level s.** Solve the signed sub-instance on d_M-space with poly ply, keeping the rings laminar with M.
  - Its local forms are again complements of ≤ N subspaces, now in ℤ^{n/2} with no positivity.
  - A G1-style slack-forest tiling would close it if it extends to signed rings ±e_a ± e_b.

If (i) and (ii) hold with factor C per halving, the ply is n^{O(log C)}.

**Negative side.** Lemma G5 shows that the G4 criterion carries no laminarity content beyond the choice of M.
Lemma G6 and the tables show that a single NC matching suffices for every tested sparse mixed defect. A lower bound
would therefore need a correlation obstruction for (i): a primitive y for which all N bad events cover all but an
n^{−ω(1)} fraction of NC matchings. Pure linear algebra cannot supply this, so it is §6 "pure convex geometry" again,
unless it uses the joint NC constraint on M.

## Status
| claim | status |
|---|---|
| G5: K = 2 ⇒ L₁^⊥ ⊆ A(M), M NC; G4 ⇔ ∃M ∀k d_M(y) ∉ d_M(V_k) (both levels) | [written proof, modulo G4 separation] |
| σ/d per-prime OR recursion is an artifact; correct recursion ∃M ∀k + signed d_M sub-instance | [written proof] |
| G6: {M₀, M₁} fail on explicit primitive y, n = 36 | [written proof + exact] |
| random NC matchings certify all tested sparse mixed defects (n = 36, 900), both levels | [computational] |
| G-glob′ (i) correlation bound, (ii) signed sub-instance | OPEN |

## Files
- `polynomial-ambiguity/round2/scripts/gglob_matching.py`: Parts A–C (exact mod-p rank tests).
