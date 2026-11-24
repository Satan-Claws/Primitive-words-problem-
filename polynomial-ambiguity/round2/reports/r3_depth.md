# R3-depth: recursion depth and ply accounting for G-glob

R3, 2026-11-24. Script: `round2/scripts/r3_depth_localbound.py` (< 1 s).
Notation follows `R2/global.md`, `R2/gglob*.md`, `R2/r3_i2.md` and `R2/r3_sep.md`:
- n = P², and s_k = n/p_k;
- fibre r is the residue class R_r = r + Pℤ;
- a position is x = r + P·t, with t read in CRT coordinates;
- f_{k,r,β} := 1{x ∈ R_r, t_k(x) = β}.

**Verdict.**
1. The per-halving factor in audit caveat C1 comes from the wrong accounting. In every construction used so far, the
   pieces tile their facet regions exactly (G1, S1, the C1 products). For those constructions the ply is the overlap
   number of a facet-tuple family, ply(x) = #{σ : x ∈ R_σ}. It is never a product over levels: matchings and levels
   are tiling devices. The quantity 1/Pr_𝒟 is not the factor either.
2. Depth is not log₂ n. At most N + 1 levels are essential, and G-glob proper (t ≫ s ≫ 1) has depth 2. Even so,
   depth is the wrong question. Point 3 is the decisive one.
3. **Lemma D1 [written proof]: local certificates force superpolynomial ply at depth 1.** Take any exact
   facet-tuple family in which each facet touches ≤ s fibres. It has a point of norm ≤ (2N+1)n with
   ply ≥ (P/(2s))^N.
   - The I0/I2 witnesses have s = 2, and so do the J-share repairs of r3_sep. They give ply ≥ (P/4)^N = n^{N/2−O(N/log N)}.
   - So **the I2 route to G-glob is dead as a construction**, whatever the depth. This independently reproves
     PA/poly_LAM §1(a), now at polynomial norm.
4. This is **not a new negative candidate**. The adversary in D1 is pure ⊕E_k, single-scale, with no mixed types.
   realise's *spread* facets already cover it with ply n^{1+o(1)} (global.md G1). D1 constrains only the paradigm
   of exact facet tilings with local facets. Mixed multi-scale defects add nothing that I can turn into a lower bound
   (§4).
5. The G-glob gap is now sharper: the certificates must be **spread** (touch ≥ P/N^{O(1)} fibres per prime) and also
   **jointly NC and chord-disjoint** (r3_sep Lemma C1). This is SPREAD-JOINT (§5), and it is OPEN.

## 1. Ply accounting (answer to task (2)) [written proof]
**Exact facet-tuple constructions.** Let Σ be a family of tuples σ = (μ_1, …, μ_N) with μ_k ∈ V_k^⊥ integral (sign
absorbed into μ_k). Put R_σ = {x ∈ ℕⁿ : μ_k(x) ≥ 1 ∀k}. Suppose each R_σ is tiled by valid laminar pieces with
ply exactly 1, as G1 does per facet, S1 does on d_M-space, and r3_sep C1 does for products. Then:
- **ply(x) = #{σ ∈ Σ : x ∈ R_σ}.**
- A matching M is part of the *tiling* of R_σ: its chords are lineality rings, and the facets lie in A(M). It is not
  an extra covering choice. "∃M ∀k, then a signed sub-instance" only adds a factor if the sub-instance is solved by
  another covering family rather than by a tiling. In that case the factor at x is that family's overlap at x.
- The matchings that work at x do count, because x ∈ R_σ for each of them. So the overlap is the right quantity, and
  1/Pr_𝒟 is not. Sampling 𝒟 gives a family of size ≈ (1/π)·log(#types). Its overlap at a *generic* x, where every
  witness difference is nonzero, is the full family size divided by 2^N, by sign matching.
- So C1's "(729/16)^N per halving" is neither an upper nor a lower bound on the true ply. The true question is the
  minimum overlap of a covering family of jointly tileable tuples. That is a depth-1 covering-design problem.

## 2. Depth (answer to task (1)) [written proof for local forms; assessment for constructions]
Take a flag x = t₁ω₁ + t₂ω₂ + … + η with lineality L_j at level j. Level j is **essential** if some still-uncertified
k has ω_j ∉ L_{j−1} + V_k.
- If level j is not essential, then V_k + L_j = V_k + L_{j−1} for every uncertified k. So the local instance (the
  complement of ⋃(V_k + L) in the quotient) does not change.
- Hence at most N essential levels follow the U level.
- For G-glob proper (three scales t, s, bounded η) there are exactly two levels: M at level t, then δ- and
  η-certification (r3_sep).
- In d_M-space the top direction is an arbitrary δ′, not 1. If δ′ has no balanced ±1 relation on any ring component,
  every component has a loop and the recursion stops. So deep recursion occurs only for structured (sparse/±1)
  defects.

**Budget check (task's arithmetic).**
- If each essential level did cost (729/16)^N, then depth 2 would cost n^{O(1/log log n)}, which is fine.
- Depth N would cost exp(Θ(N²)) = n^{Θ(log n/(log log n)²)}, which is superpolynomial. It is still far below the
  natural n^{N/2}.
- §1 makes this moot: the factor is not 1/Pr, and Lemma D1 shows that local certificates fail already at depth 1.

## 3. Lemma D1 (local certificates ⇒ ply ≥ (P/(2s))^N) [written proof]
**Statement.** Let Σ be an exact facet-tuple family as in §1 that covers every primitive point. Write fib(μ) for the
set of fibres meeting supp μ, and suppose |fib(μ_k)| ≤ s for all σ and k. Then some
x* = (N+1)·1 + Σ_{k,r,β} c_{k,r,β} f_{k,r,β}, with c ∈ {±1}, satisfies

  ply(x*) ≥ (P/(2s))^N,  and ‖x*‖₁ ≤ (2N+1)n.

**Proof.**
1. *Adversary points.* f_{k,r,β} depends, inside fibre r, only on t_k. So it is invariant under s_j for j ≠ k, and
   it lies in V_j. It is not s_k-invariant, so it is not in V_k.
   - Put x_ι = (N+1)·1 + Σ_k ε_k f_{k,r_k,β_k}, with ι = (r_k, β_k, ε_k)_k. There are (2P·p_k) choices per k.
   - Each x_ι is a primitive point of ℕⁿ.
   - μ_k ⊥ 1 and μ_k ⊥ f_j for j ≠ k. Hence μ_k(x_ι) = ε_k μ_k(f_{k,r_k,β_k}).
2. *Each tuple serves few adversary indices.* If σ covers x_ι, then for each k, ε_k μ_k(f_{k,r_k,β_k}) ≥ 1.
   - So r_k ∈ fib(μ_k), which leaves ≤ s choices.
   - β_k then has ≤ p_k choices.
   - ε_k is then determined by the sign of μ_k(f).
   - So σ serves ≤ ∏ s·p_k indices. Covering all of them needs ≥ ∏_k (2P p_k)/(s p_k) = (2P/s)^N distinct tuples.
     Call this used set Σ′.
3. *One point lies in many regions.* Draw c iid uniform ±1.
   - Each coordinate of x* − (N+1)·1 receives at most one term per k, so x* ∈ ℕⁿ.
   - For σ ∈ Σ′ and each k, μ_k(x*) = Σ_{r,β} c_{k,r,β} μ_k(f_{k,r,β}) is a symmetric integer sum with at least one
     nonzero coefficient. Conditioning on the other c's, at most one value of that coefficient gives 0, so
     Pr[μ_k(x*) = 0] ≤ 1/2 and Pr[μ_k(x*) ≥ 1] ≥ 1/4.
   - The families c_{k,·} are disjoint across k, hence independent, so Pr[x* ∈ R_σ] ≥ 4^{−N}.
   - Therefore E ply(x*) ≥ (2P/s)^N·4^{−N} = (P/(2s))^N. ∎

**Corollaries.**
- I0 witnesses μ = e_a − e_{a+1} − e_b + e_{b+1} (a ≡ b mod s_k) touch the fibres {r, r+1}, so s = 2.
  - Every exact family built from I2 witness sets, including any derandomisation of 𝒟, has ply ≥ (P/4)^N.
  - That is n^{N/2}·4^{−N} = n^{N/2 − O(N/log N)}, which is superpolynomial.
- r3_sep's J-share repair (chords c₀ + {0, 150, 300, 450} at n = 900) stays inside one or two fibres. So it is local,
  and D1 applies.
- *Necessary spread.* (P/(2s))^N ≤ n^c forces s ≥ P/(2N^{O(c)}). So, for poly ply, almost every used facet of every
  prime must touch a 1/poly(N) fraction of all fibres.

**What D1 does not prove.** D1 is relative to the paradigm. A general cover may use pieces strictly smaller than
facet regions, so x* ∈ R_σ does not put x* in a piece. This is exactly why "pure convex geometry" cannot give a lower
bound (§6). D1 is a no-go for a construction strategy, not a lower bound for Q.

## 4. Mixed / multi-scale defects: is there a new negative candidate? (task (3)) [assessment, with the key steps proved]
**Locality, not mixing, drives D1.**
- The D1 adversary is ⊕E_k at a single scale.
- The other way to force many independent certificate centres is a fibre set {K_r} whose cover number c tends to
  infinity. That already forces n^{Ω(c)} for local families. But K_r = [N] ∖ J_r with large J_r makes u_r constant
  along J_r, which is spread, not sparse.
- Sparse (mixed-type) defects are the opposite case:
  - a point mass is a hub, with K_r = [N];
  - G2-type 1_D + 1_T has cover number 2.
- So sparse mixed defects have only poly(n) placements per certificate pattern, and local families handle them with
  poly overlap (stars: n·∏(p_k − 1) ≤ n^{3/2} tuples).

**Combined two-level adversary** (r3_sep's bad case, with level s made spread):
- δ = Σ_{k∈A} f_{k,r_k,β_k}, with η = e_q for the deferred primes D.
- The A-primes need spread facets (by D1), and these see only δ.
- The D-primes need facets through the chord at q. Two or more D-primes share it (J-share). That is repaired by
  nested local facets, and there are only n choices of q.
- So the overlap is ≤ (spread family for A) × (local family for D) = poly × poly, *provided* the spread A-facets and
  the local D-facets are jointly chord-disjoint and NC (C1).
- I found no argument that C1 forces crossings here. The D-facets live near q and the A-facets can be routed around
  one chord. So no superpolynomial forcing from mixed multi-scale defects is established.

**Candidate lemma (would give a laminarity-based negative mechanism) [conjecture, unproved].**
> *SPREAD-CROSS.* For N ≥ 3, any N facets μ_k ∈ V_k^⊥ that are spread (each touching ≥ P/N^{O(1)} fibres, with ±1
> entries) and whose witness chords are pairwise disjoint and NC jointly certify only an n^{−ω(1)} fraction of the
> ⊕E_k adversary, under the measure of §3.

- If true, D1 plus C1 would force ply n^{ω(1)} on every exact facet-tuple family. That would still be paradigm-relative.
- Evidence *against* it: realise's pair facets are spread, nested and NC, and they cover ⊕E_k ⊕ U with ply
  n^{1+o(1)} (global.md G1, realise Lemma 4). So SPREAD-CROSS is false as stated for pure types. Any true version
  must use the mixed (G2-type) part as well, which is exactly where realise's disjoint supports fail (G2: N ≥ 6).

## 5. Exact remaining gap (sharpened)
**SPREAD-JOINT (OPEN).** Find a poly(n)-size family of tuples σ such that:
1. each prime's facet μ_k ∈ V_k^⊥ (or in A(M)) has ±1 entries, and almost all used facets touch ≥ P/N^{O(1)} fibres
   (forced by D1);
2. the witness chords of the facets that need arcs are pairwise disjoint and NC, after nested recombinations
   (forced by C1);
3. every primitive two-level x = t·1 + sδ + η lies in some R_σ.

Then ply(x) = #{σ ∋ x} ≤ |Σ| = poly, and G-glob closes with depth 2.
- realise solves 1 + 2 + 3 on ⊕E_k ⊕ U.
- G3/r3_sep solve 2 + 3 locally (but not 1) for sparse mixed defects.
- The open problem is the overlay of the two. The simplest candidate is Σ_realise ∪ Σ_local, where Σ_local is used
  only on points missed by realise. Such points have small mixed support (G2: |supp δ| < N). If they have only
  poly(n) local patterns, D1 does not bite. Whether the "missed by realise" points are exactly the hub-like/low
  cover number ones is the precise question.

## 6. Computation [computational] (`r3_depth_localbound.py`)
| n | check | result |
|---|---|---|
| 36, 900 | μ_k(f_{j,r,β}) = 0 for j ≠ k, over all I0 facets | 0 violations |
| 36 | per-k max coverage / LB / greedy cover size | 4 / (6, 9) / (7, 12); ply_max of product family over 30 random x* = 12 |
| 900 | same | 4 / (30, 45, 75) / (31, 60, 91); ply_max = 9152 = n^{1.34}, mean 5105 |
| N = 3…15 | exponent log_n (P/4)^N | 0.89, 1.48, 2.05, …, 6.74, 7.25 (≈ N/2 − O(N/log N); unbounded) |

The maximum coverage per option is 4, which matches the s·p_k/p_k count of step 2 (2 fibres × 2 values of β).

## Status
| claim | status |
|---|---|
| Exact facet-tuple constructions: ply = #{σ : x ∈ R_σ}; levels and matchings are tiling devices; C1's per-halving factor is the wrong accounting | [written proof] |
| Essential depth ≤ N + 1; G-glob proper has depth 2; depth N × (729/16)^N would be exp(Θ(N²)), superpolynomial | [written proof] (local forms) / [assessment] (constructions) |
| D1: facets touching ≤ s fibres ⇒ ply ≥ (P/(2s))^N at norm ≤ (2N+1)n; I2/I0/J-share ⇒ n^{N/2−o(N)} | [written proof] + numerics |
| I2 route to G-glob dead in any depth; spread certificates necessary | [written proof] (paradigm-relative) |
| New negative candidate from mixed multi-scale defects | NOT found; SPREAD-CROSS stated, false for pure types |
| SPREAD-JOINT (G-glob, sharpened) | OPEN |

## Files
- `polynomial-ambiguity/round2/scripts/r3_depth_localbound.py`
