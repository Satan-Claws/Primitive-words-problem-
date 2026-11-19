# Round 4 — agent "cl5neg": negative direction for CL5 (and foldbar's mirror-certificate question)

**No proof of either resolution. CL5 is neither proved nor refuted.** No scripts were run.

## 1. Reductions (PROVED)
- **R1.** We may assume L ⊆ ODD = {|w|_0 and |w|_1 both odd}. This is regular and contains T. Every power in L is
  then v^q with q odd ≥ 3, |v| even, and |v|_0, |v|_1 odd. Decompositions in a pumping lemma for L must keep
  |vz|_0 and |vz|_1 even.
- **R2 (witness families must avoid cheap certificates).** Let f = Σ c_δ·#_δ, a fixed integer combination of
  circular factor counts. Then {w ∈ ODD : f(w) ∈ {±2^j : j ≤ J}} is CF (one-counter) and ⊆ Q, because q | #_δ for
  every δ when w = t^q with q odd. Special cases:
  - "δ occurs exactly once circularly" (regular);
  - "#runs is a power of 2";
  - Parikh imbalance |y|_1 − |y|_0 = ±2^j.

  Consequences:
  - Bounded-run subfamilies of T, and {1u^k0u^k} for a fixed u, all have regular certificates.
  - A CL5 witness family needs an unbounded number of runs, no bounded unique circular factor, and must evade
    every such f.

## 2. Lemma R (rigidity; PROVED)
Let V = P + Δ ∈ Z^K, where P is ρ-periodic (ρ | K) and s = |supp Δ| satisfies 2s < K/ρ. Suppose V is
σ_{K/Q}-invariant for some Q ≥ 2.

**Claim.** Then P and Δ are both σ_{K/Q}-invariant. Hence, if 0 < s < Q, no such V exists.

*Proof.*
1. Write h = K/Q. We have P − σ_hP = σ_hΔ − Δ.
2. The left side is ρ-periodic. The right side has support ≤ 2s < K/ρ.
3. A nonzero ρ-periodic vector has support ≥ K/ρ, so both sides are 0. This shows P and Δ are σ_h-invariant.
4. A nonzero σ_h-invariant vector has support ≥ Q (each orbit has Q elements). So s < Q forces Δ = 0. ∎

**Corollary (unary-pump escape, PROVED).**
- **Setup.** Take a "y close to a power" witness: w ∈ T whose cyclic run vector is P + (−e_a + e_{a+1}) with K/ρ > 8.
  A natural example is a one-flip neighbour of s^{2q}, w = s^q·flip₀(s)·s^{q−1}.
- **Claim.** Every pump whose v and z are each unary inside runs (any distance apart, any i, with no run deleted)
  gives a primitive word.
- **Proof.**
  1. The pumped deviation is Δ′ = −e_a + e_{a+1} + (i−1)(k₁e_{j₁} + k₂e_{j₂}), with support ≤ 4.
  2. By Lemma R (needs 2·4 < K/ρ), Δ′ is σ_h-invariant with Q odd ≥ 3, so Q = 3.
  3. Δ′ ≠ 0: repairing both deviations needs (i−1)k₁ = 1 and (i−1)k₂ = −1, which is impossible with k₁, k₂ ≥ 0.
  4. So supp Δ′ is one 3-orbit O. O cannot contain both a and a+1, so the deviation outside O is cancelled by a pump.
  5. That leaves at most 2 positions for O, a contradiction. ∎
- **Consequence.** Ogden attacks on near-power witnesses fail whenever the defender can pump a marked run of
  length ≥ 3 with v = c², which respects R1.
- **What remains.** The attacker must mark only runs of length ≤ 2 and force non-unary pumps. This is exactly
  where cl1 found that T-type members escape bounded certificates.
- **Hint for the refutation side.** The escaping decomposition is: one unary pump in a long run, z = ε.

## 3. Part 2 (foldbar): mirror-pair certificates
Question: does a finite union of rotation-closed C_R = {w : the mirror-pair sequence of w about some axis lies in a
regular R} lie inside Q and cover T? **Not settled.**

The natural pumping attack fails:
- **Pump.** Take w = 1u^m0u^m with u chiral. Over the long u-periodic stretch, the automaton has a loop of length ℓ|u|
  with ℓ ≤ #states. The loop inserts u^{ℓt} at two mirrored places.
- **Resulting words.** These are 1u^A0u^B.
  - If A = B, the word is in T and so is primitive.
  - If A ≠ B, there are two defects. By Lemma R (support 2 < 3) the word is not a power with Q ≥ 3, and R1 excludes
    Q = 2.
- **So the attack escapes.** The barrier question stays open.
- **What would settle it.** The attacker would need witnesses where the loop region overlaps a defect. That needs
  low-complexity u with short runs.

## Registry entry
1. **Aim:** CL5 (negative side), and the mirror-certificate barrier.
2. **Proved:**
   - R1 and R2;
   - Lemma R;
   - the unary-pump escape corollary;
   - the mirrored-loop attack fails on 1u^m0u^m.
3. **Missing step:** a family of T-words with runs ≤ 2 and no bounded unique factor, together with a marking, such
   that every non-unary pump (and every two-site mirrored loop) creates an odd power.
4. **Counterexamples:** the escaping decompositions in §2–§3, i.e. a single unary pump, or a periodic mirrored loop.
5. **Strength:** the missing step is stronger than "Q not CF".
6. **What would reopen the route:**
   - a cross-length transplant lemma that defeats Lemma R (deviation sets forming a full 3-orbit); or
   - a CF certificate exploiting short-run T-words, which would be evidence for the positive side.
