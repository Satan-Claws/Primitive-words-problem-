# poly_S3F: option (A) of poly_G4 §4 at ply 2 with chain pieces — IMPOSSIBLE (obstruction + M=2 data)

Setting: poly_G4 (valid cover of NE_M, Lemma F / Cor. F), poly_T2b §2–3 (Thm E, chain ℤ/2^ρ), poly_R3a (chain
realisable), poly_G3 (Lemma G), poly_S3H. Goal tested: a valid cover (laminar, Δ-avoiding, data ≤ K fixed) in
which every ply-≥2 point has norm ≥ exp(Ω(ρ)), ρ = 2-adic chain length of some piece.

## 1. Obstruction (PROVED)
(a) **ρ is bounded by M.** A full-rank piece has [ℤ^{2M} : ℤV_σ] = |det| ≤ ∏‖v‖₂ ≤ K^{2M} (Hadamard), so
2^ρ ≤ K^{2M}, ρ ≤ 2M log₂K. For fixed M (= 2, 3, 4) and fixed K, ρ cannot grow at all; for fixed M every
quantity is K^{O_M(1)} (poly_G4 §1). So "ρ → ∞ with K fixed" forces M ≥ ρ/(2 log₂K) → ∞.
(b) **Then Cor. F kills it.** Restrict to any 2-pair face F_I (|I| = 2, other coords = 1): by Lemma F this is a
valid cover of NE_2 with the same K (chain pieces either restrict to their J-supported generators or vanish);
⌈(2+1)/2⌉ = 2 forces a ply-2 point there of norm ≤ B(2,K) = K^{O(1)} (Thm E at n = 6). Lifting by ones:
  min{‖P‖₁ : ply(P) ≥ 2} ≤ 2(M−2) + B(2,K) = O(ρ/log K) + K^{O(1)}   — at most LINEAR in ρ, never exp(ρ).
Mechanism, in G3** language: the ply-2 point lives on a face where only ≤ 4 coordinates move, so Λ_S, apex
and θ_S are those of a 4-dimensional sub-cover; the chain's index 2^ρ is invisible there (its 2-power on a
4-dim face is ≤ K^4). Lemma S (one coset has a rep. of norm ≤ nK) + Lemma G on the face give the point.
(c) **The literal chain of T2b/R3a is not Δ-avoiding in full rank (M = 2).** V = {e_{x1}, e_{x1}+2e_{x2},
e_{x2}+2e_{y1}, e_{y1}+2e_{y2}}: φ = (0,4,−2,1) mod 8 gives ℤ^4/ℤV ≅ ℤ/8 with φ(0,1,0,1) = 5 a generator, so
every coset meets Δ_ℤ; and π(v) = y−x projections (1,0),(1,2),(−2,1),(−1,−2) positively span ℝ², so c+cone V
meets Δ arbitrarily deep ⇒ c+ℕV ∩ Δ ≠ ∅ for every c. Other cyclic ℤ/2^ρ pieces (ρ ≤ 3) are Δ-avoiding (§2).

## 2. M = 2 computation [computational]
`scripts/poly/s3f_ilp.py T C E ρ` (pool `s3f_pool.py`): all full-rank laminar pieces with generator entries
≤ 2 (K ≤ 3), offsets c ∈ {1,2}^4 (chain-type pieces {1..3}^4), Δ-avoidance checked on (u,v,u,v), u,v < 30;
ILP (HiGHS): cover all of NE_2 ∩ [1,5]^4, ply ≤ 1 at every box point of norm < N0, maximise N0; ρ > 0 forces a
piece with cyclic quotient ℤ/2^ρ (Smith-form check). Box restriction only relaxes, so "infeasible" is a true
upper bound for the pool; "feasible" is box-certified only.

| ρ (forced cyclic ℤ/2^ρ piece) | pool size | Δ-avoiding chain pieces | max min-norm of a ply-2 point | N0=10 |
|---|---|---|---|---|
| 0 (none)  | 12692 | – | 9 | infeasible (proved) |
| 1 | 28612 | 19304 | 9 | time limit (300 s) |
| 2 | 15996 | 4016 | 9 | time limit (300 s) |
| 3 (= 2M−1, max) | 12972 | 352 | 9 | infeasible (proved) |
Index-2^ρ pieces enter valid covers but do not push ply 2 outward: the optimum is 9 (e.g. ply-2 at (1,1,4,3)),
independent of ρ. Smallest-norm points of NE_2 have norm 5; the first forced overlap is at norm ≤ 9.
M = 3, 4: not run (pool ≥ 10^6); by §1(b) the answer is ≤ 2(M−2) + [M=2 value] for every cover, so
≤ 11, 13 within the same pool class [PROVED reduction + computational M=2 input].

## 3. Status
- PROVED: §1 — option (A) is impossible at ply 2 (any constant ply, via Cor. F with r = 2p−1) for every
  choice of chain pieces; ρ-growth needs M-growth and face restriction removes it. Consistent with poly_G4 Cor. F.
- [computational]: M = 2 table — max over pool covers of the min ply-2 norm is 9 for ρ = 0..3.
- OPEN (unchanged): (A)/(B) at threshold ⌈m/2⌉, where no face of bounded size suffices (poly_G4 §4).
