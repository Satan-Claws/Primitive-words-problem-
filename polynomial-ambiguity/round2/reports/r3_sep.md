# R3/r3_sep: G-glob′ (ii) without (H2): separating chords, unequal weights, F₁-laminarity

R3-D, 2026-11-24. Builds on `R2/gglob_ii.md` (Theorem S1, O1, O2), `R2/gglob.md` (Lemma G5), `R2/gglob_i.md` (𝒟, I0–I2).
Scripts: `round2/scripts/r3_sep_checks.py` (parts A–D, < 2 s) and `round2/scripts/r3_sep_i2nc.py` (< 1 s at n = 36).

**Verdict.**
- **(H1), (H2) and the F₁ caveat are removed upstream, at the per-facet level [written proof + exact check].**
  - Change 𝒟 to 𝒟′: keep only the isolated adjacent pairs and drop the adjacent completion. M is then a partial NC
    matching, and gglob_i Thm I1 is unchanged.
  - Every chord of M then bounds the outer face, so G_M(S) is complete for every S and (H2) always holds.
  - W_k^⊥ has a ±1 basis, so non-±1 facets (O2) are never needed.
  - F₁ := M ∪ singletons makes F₁-laminarity identical to M-laminarity.
  - So S1 applies to every facet that is needed: ply 1, TU, K = 2, offsets ≤ 4 for pair facets.
- **Option (2) is impossible [written proof].** O1 survives even with pieces that are not in one facet half-space
  (parity-straddling pieces), with rings through the separating chord, and with several facets. With fixed M a
  separating chord cannot be repaired. Under the original 𝒟 about half of the needed pair facets are separated
  (Part C), so the upstream change is necessary.
- **New gap: joint (multi-prime) laminarity [written proof + computational].** S1 is per facet. One piece that needs
  balanced arcs for several primes at once needs a *non-crossing, chord-disjoint* system:
  - Criterion (N*) and Lemma C1: pair facets work jointly iff their witness chords are disjoint and pairwise NC.
  - I2's witness systems often violate this. At n = 36, 76 of 100 adversarial restarts and 45 of 292 structured
    defects satisfy I2 but have no NC disjoint system; hubs share a point.
  - Arcs are needed only in two places:
    - at level s, for primes whose two witness chords carry same-sign d-values;
    - at level η, for ≥ 2 deferred primes, which requires N ≥ 3.
  - Larger ±1 facets can repair a shared chord (Part B, "repaired"). A crossing pair has no general repair.
- **Status of (ii):** per-facet **closed** via 𝒟′. Joint multi-prime tiling is **OPEN**, reduced to an NC-witness
  covering condition (§4).

## 1. Option (1): the partial matching 𝒟′ [written proof]
**𝒟′.** Draw A as in gglob_i (iid Bernoulli(1/3) points, keep the isolated ones). Put M = {{x, x+1} : x ∈ A}, with
no completion. The points that are not matched become singleton components of F₁, with ring e_p.

**Thm P.**
- (a) Lemma G5 allows partial M. The level-t lineality is L₁ = L(M) ⊕ span{e_p : p unmatched}, and
  L₁^⊥ = A(M).
  - The I0 certificate μ = e_a − e_{a+1} − e_b + e_{b+1} lies in A(M) ∩ V_k^⊥.
  - So gglob_i Thm I1 holds verbatim for 𝒟′, with Pr ≥ (16/729)^N. The proof only ever used S ⊆ A.
- (b) Every chord {x, x+1} has no endpoint strictly inside it, so the region it cuts off contains no other chord.
  The complement is one face bounded by all chords. Hence G_M(S) = K_S for every S, and (H2) always holds.
- (c) Take F₁ = M-edges ∪ {e_p : p unmatched}.
  - Then 1 = Σ_M (e_p + e_q) + Σ e_p lies in the relative interior.
  - Its ballot matching is M, and its 2-point chords *are* the M-chords.
  - The S1 arcs h(a)t(b) form a forest on the chords and are NC with M (S1(c)). So M-edges ∪ arcs is an NC forest.
  - This settles the "laminarity against F₁" caveat of gglob_ii §5 for this design.
- (d) Total ring count: |M| + (arcs + loops = |S|) + (|M| − |S|) off-support one-point rings + #unmatched = n. So
  the piece has full rank.

**Check (Part A).**
- Setup: 12 instances from 𝒟′ with n ∈ {12, …, 30}; random ±1 facets, pair facets, and all-+1 (transversal-type)
  facets with |S| ≤ 6; 180 cells.
- Results:
  - all cells have |det| = 1;
  - all cells are rooted forests;
  - arcs are pairwise NC and NC with M;
  - M-edges ∪ arcs is a forest;
  - ply violations: 0 of 4546 box points.
- Part D shows that the choice F₁ = M matters. If F₁ has a tree chord that is not an M-chord, S1 arcs cross it in
  855 of 1221 cells.

## 2. Option (3): non-±1 facets are never needed under 𝒟′ [written proof]
- Let C_r be the set of chords of A whose left endpoint is ≡ r (mod s_k). Then d_M(v)_x = (Dv)_x, and D(V_k) is the
  set of s_k-periodic vectors with period sum 0.
- If A misses some residue mod s_k (always the case when |A| < s_k), then:
  - W_k := d_M(V_k) is the set of vectors that are constant on each C_r;
  - W_k^⊥ = {μ : Σ_{C_r} μ = 0 ∀r}, which is spanned by the pair facets e_a − e_b (a, b ∈ C_r).
- If A hits every residue, then W_k^⊥ = {μ : all class sums equal}. Add the transversal μ* = Σ_r e_{x_r}, with one
  chord per class.
- Every basis vector is in {0, ±1}^A. Any z ∉ W_k has μ_j(z) ≠ 0 for some basis facet μ_j.
- So the ±μ_j (j ≤ |A|) cover ℤ^A ∖ W_k using only ±1 facets, and by Thm P(b) S1 applies to each of them. O2 never
  arises. It can arise only for general perfect M, which 𝒟′ never uses. The realise.md facets are ±1 per fibre for
  the same reason.
- Caveat: the number of facets per prime is ≤ |A| = O(n). Per facet the ply is 1; across facets the ply is ≤ 2|A|N
  for a fixed M. This is polynomial, but it is not O(1) per halving.

## 3. Option (2): separating chords cannot be handled directly [written proof]
**Prop O1⁺.** Use O1: M = {a = (1,2), e = (0,3), b = (4,5)} and R = {z : μ(z) ≠ 0} with μ = z_a − z_b. No finite
family of M-laminar pieces with ‖ring‖₁ ≤ 2 covers R, whatever the sign structure of the generators.
- *Proof.*
  - The M-laminar ring images have μ(v) ∈ {0, ±1, ±2}.
  - Suppose a piece c + ℕV avoids {μ = 0} and has generators of both μ-signs. Its μ-values contain μ(c) + gℤ, where
    g = gcd μ(V). So g = 2 and μ(c) is odd.
  - Hence the points of L₂ = {μ = 2} lie only in sign-definite pieces. In such a piece μ(c + Σ n_v v) = 2 bounds every
    n_v with μ(v) ≠ 0.
  - So L₂ ∩ piece lies in finitely many translates of ℕ{v : μ(v) = 0}. That set has rank ≤ 1, since the only
    balanced laminar images are ±e_e and ±2e_e (gglob_ii O1).
  - L₂ ≅ ℤ² cannot be covered by finitely many sets of linear growth. ∎
- Rings "through e" do not help. A ring with images on both a and b has endpoints on both sides of e, so it crosses
  e. Rings ending at e's endpoints give only ±e_e. Several facets do not help either, since R is unchanged.
- Under the original 𝒟 (perfect, adjacent completion), n = 36, same-class A-pair facets are face-separated in
  809 of 1569 cases (s = 18) and 1489 of 3037 cases (s = 12) (Part C). So option (1) is needed, not cosmetic.

## 4. The remaining gap: joint laminarity across primes
**Criterion (N\*) [written proof].** The argument of §3 with L₂ = {μ_k = 2 ∀k} gives a necessary condition. A finite
M-laminar K = 2 cover of ∩_k{μ_k ≠ 0} (facets μ_1..μ_r, with W_k = ker μ_k) needs one piece whose pairwise-NC balanced
rings have d_M-images spanning ∩_k ker μ_k.

**Lemma C1 [written proof + Part B].** Take pair facets μ_k = e_{a_k} − e_{b_k} on 𝒟′-chords. Their joint tiling exists
(ply 1, NC, K = 2) **iff** the witness chords are pairwise disjoint and the chords a_k b_k are pairwise NC.
- *If:* take the product of the 2-dimensional S1 tilings. Each tiling has 3 cells and uses only the arc a_k–b_k, so
  the arcs are NC by hypothesis.
- *Only if:*
  - A balanced ring touching a_k has image ±e_{a_k} ± e_x, and it lies in ker μ_k only if x = b_k. If a chord is
    shared, a_1 = a_2, then no ring touching it is in both kernels, and the rank is deficient.
  - With disjoint chords, the only joint-balanced 2-point rings are the arcs a_k–b_k, so crossing arcs give rank
    deficit 1.
- Part B: J-nest and J-disj are OK; J-cross and J-share are OBSTRUCTED. J-share is repaired by
  μ_2 = e_0 + e_1 − e_2 − e_3 (nested arcs).

**When arcs are needed.** Take a level with d = d_M(δ).
- *Level s, k ∈ A(δ).* Loops e_{h(c)} suffice for chord c iff sign(d_c)·μ_k(c) ≥ 0 for all k with c ∈ supp μ_k.
  Otherwise the arc a_k–b_k is needed, for example when d_{a_k} > d_{b_k} > 0.
  - Point-mass and hub δ need loops only. This is why gglob's G3 overlapping certificates are harmless.
- *Level η, k ∉ A(δ).* This requires a global joint tiling of ∩{μ_k ≥ 1} over the deferred primes, so C1 applies
  whenever ≥ 2 primes are deferred (N ≥ 3).
- *Explicit bad case.* Take N = 3, δ ∈ V_1 ∩ V_2 ∖ V_3 and η = e_q.
  - d_M(η) is nonzero on exactly one 𝒟′-chord c₀ ∋ q. Of the two candidate chords {q−1,q} and {q,q+1}, at most one
    is in A.
  - So every certifying facet of primes 1 and 2 contains c₀, and pair facets always share it. They are impossible by
    C1.
  - The 4-chord repair μ_1 = e_{c₀} − e_{c₀+450}, μ_2 = e_{c₀} − e_{c₀+450} + e_{c₀+150} − e_{c₀+300} at n = 900
    satisfies (N\*) with nested arcs. That needs those four chords in A.
  - Admissibility of the repair: μ_2's mod-300 class sums are (c₀: 1 − 1), (c₀+150: −1 + 1), so it lies in W_2^⊥.
    [checked by hand; joint tiling of the repaired system not computed]

**I2-NC (`r3_sep_i2nc.py`) [computational].** I2-NC is I2 plus three conditions: the witness pairs are
point-disjoint, the chords are pairwise NC, and no two points are consecutive. At n = 36:

| test | I2 failures | I2-NC failures |
|---|---|---|
| `climb 2 300 100 1` | 0 | 76 / 100 |
| `struct 2 300` | (not reported) | 45 / 292 |

- The structured failures include y = 1_{6ℤ} and the orbit y = 1_{5+12ℤ}.
- So I2 witness systems are typically **not** C1-compatible.
- For N = 2 at most one prime is deferred, so the η-level coupling never arises. Level-s coupling arises only for
  same-sign arc-needing witnesses. This case is not separately enumerated.

**Exact open statement (ii-joint).** For every primitive two-level (δ, η), find a 𝒟′-matching and ±1 facets, one per
prime from W_k^⊥, such that two families of witness chords are pairwise NC and chord-disjoint after unimodular
recombination (as in the J-share repair):
- the arc-needing level-s primes;
- the deferred primes.

A probabilistic version would follow from an "I2-NC with repairs" covering lemma. Not attempted.

## Status
| claim | status |
|---|---|
| Thm P: 𝒟′ (partial isolated adjacent pairs) keeps (i)/I1; G_M(S) complete ⇒ (H2) always; F₁ := M ⇒ F₁-laminarity = M-laminarity; S1 applies to every needed facet | [written proof] + Part A (180 cells, 0/4546 ply violations) |
| W_k^⊥ has a ±1 basis under 𝒟′ ⇒ non-±1 facets (O2) never needed | [written proof] |
| O1⁺: separating chord unrepairable by ANY finite M-laminar K=2 family (straddling, through-e rings, multi-facet) | [written proof] + Part B |
| Original 𝒟: ≈ 50 % of needed pair facets face-separated (n = 36) | [computational] |
| F₁ ≠ M (extra tree chords): S1 arcs cross them in 855/1221 cells | [computational] |
| (N\*) criterion; Lemma C1 (pair facets jointly ⇔ disjoint + NC witness chords) | [written proof] + Part B |
| I2 does not imply I2-NC (n = 36: 76/100 adversarial, 45/292 structured) | [computational] |
| (ii) per facet | **CLOSED** (via 𝒟′) |
| (ii) joint multi-prime (arc-needing level-s primes; ≥ 2 deferred primes, N ≥ 3) | **OPEN**, reduced to §4 |
