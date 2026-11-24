# R2/lemmaC: Lemma C (W-arc-genericity of the actual μ_k), cyclic form

Status:
- **Lemma C holds for every N ≤ 45 and every k**, in the cyclic form that audit C1 requires (wrapping arcs
  included) [written proof of the reduction + exact computation].
- **For all N, Lemma C is reduced to Hypothesis H**, a statement only about where the coefficients of
  ρ_0 = ∏_{j≠k}(1 − X^{p_j}) ∈ ℤ[X] are zero (§4). H holds for 10 ≤ N ≤ 45 [computational, exact]. It fails at a few small (N, k), all covered by the direct check.
  Given H, the proof is complete for all N [written proof + finite exact check].
- **No counterexample.** The free choice of ν_k is not needed (§5).

Notation:
- P = p_1⋯p_N and n = P².
- μ = g ν with g = (1 − T^{n/p_k}) ∏_{j≠k}(1 − T^{Pp_j}), and ν generic on the window [0, Pp_k).
- W = Σ_j V_{Pp_j}, where V_M is the space of vectors of period M. A vector v is ⊥ W iff fold_{Pp_j} v = 0 for
  all j.
- An arc is a cyclic interval J of ℤ_n. It is *proper* if ∅ ≠ J ∩ supp μ ≠ supp μ, and *balanced* if
  μ|_J ⊥ W identically in ν. Balanced for a generic ν is the same as balanced identically in ν, because the
  conditions are linear in ν.

**Lemma C (cyclic).** No proper arc J of the circle ℤ_n is balanced.

## 1. Fine-to-coarse decoupling [written proof]
Write i = r + Pc with r ∈ ℤ_P (the class) and c ∈ ℤ_P (the coarse index).
- Every shift in g is a multiple of P, so g = h(T^P), where

    h(X) = (1 − X^s) ρ_0(X) ∈ ℤ[X]/(X^P − 1),  s = P/p_k.

- On class r, μ^{(r)} = h · ν^{(r)}, where ν^{(r)}_t = ν_{r+Pt} for t ∈ [0, p_k). The vectors ν^{(r)} are
  independent variables for different r.
- i mod Pp_j ↔ (r, c mod p_j). Hence fold_{Pp_j}(v)[(r, ·)] = fold_{p_j}(v^{(r)}). So v ⊥ W iff every class
  satisfies fold_{p_j} v^{(r)} = 0 for all j. In polynomial terms:

    L | v^{(r)}, where L = (X − 1) ∏_j Φ_{p_j}.

- A cyclic arc J meets class r in a coarse cyclic interval C_r. As r varies, these intervals agree up to ±1 at
  each end.

So **J is balanced ⇔ every class piece (hν^{(r)})|_{C_r} is ≡ 0 mod L identically.**
- A *full* class (C_r ⊇ supp) is never balanced. Its fold mod p_k is h̄ ν̄, where h̄ = h mod (X^{p_k} − 1).
  Here h̄ is invertible on the nontrivial p_k-characters (s, p_j ≢ 0 mod p_k), and ν̄ = ν^{(r)} is generic.
- If J is proper, some class is proper or some class is full.
- Conversely, a bad coarse arc C gives the bad fine arc J = [Pa, Pb + P − 1]. For this J, C_r = C for every r.

So Lemma C ⇔ the coarse statement for h.

## 2. Shift-difference lemma: cuts sit in gaps [written proof]
(hν)|_C = Σ_t ν_t X^t h|_{C−t}. So balanced identically means L | h|_{C−t} for each t = 0..p_k−1.

Take two consecutive windows. Their difference is h_α X^α − h_{β+1} X^{β+1}, where C − t = [α, β] has length
ℓ < P.
- L | difference forces h_α = h_{β+1}, using the factor (X − 1).
- If that common value is nonzero, then P | ℓ, using the factors Φ_{p_j}. That is impossible.
- So h vanishes on the p_k − 1 positions before C and on the last p_k − 1 positions of C.

Define the **blocks of h** to be the maximal runs of supp h on ℤ_P in which consecutive points are at distance
< p_k. Then:

**Thm 1.** Lemma C(N, k) ⇔ BLOCK(N, k): no proper nonempty cyclically consecutive union B of blocks of h
satisfies L | B, that is, fold_{p_j}(B) = 0 for all j.

This holds in both directions. For such C, all the h|_{C−t} equal h|_C. A union of all blocks gives the full
class, and the empty union gives an empty piece.

## 3. Two clusters [written proof]
Let D := deg ρ_0 = Σ_{j≠k} p_j.
- For N ≥ 4, s − D ≥ p_k and P − s − D ≥ p_k. So h = ρ_0 − X^s ρ_0 consists of two separated clusters, and
  every block lies in exactly one cluster.
- These two clusters are the poly_LAM §2 / tile2 "two clusters". Each has zero fold mod 1 and mod p_j for
  j ≠ k. That is why the ω-level fails (`lemmaC_blocks.py … 1` lists them).
- Each cluster has fold mod p_k equal to ρ̄_0 ≠ 0, so neither cluster is balanced at x-level.

Let A_i be the block-prefixes of ρ_0, with 0 = A_0, …, A_m = ρ_0. Put φ(f) := (f mod (X^{p_j} − 1))_j and
v_i := φ(A_i) = (v'_i, v^k_i), where v'_i collects the components j ≠ k. Every unit X^s is ≡ 1 modulo
L'_k := (X − 1) ∏_{j≠k} Φ_{p_j}.

BLOCK becomes three conditions:
- (α) The vectors v_i are pairwise distinct (arcs inside one cluster).
- (γ) There is no 0 ≤ a < m, 0 < b ≤ m with v'_a + v'_b = 0 and r_k = v^k_a + R_s v^k_b. Here r_k = φ_k(ρ_0)
  and R_s is rotation by s mod p_k. These are arcs that cross the gap of length s.
- (δ) The same with v^k_a + R_s v^k_b = R_s r_k (arcs that wrap across the long gap).

**Width tool.** A nonzero f with L'_k | f has width ≥ d' := deg L'_k = D − N + 2. With L in place of L'_k, the
bound is d := D + p_k − N + 1.

**Split trick.** If ρ_0 = A + S, with A a proper block-prefix and S the rest, then L'_k cannot divide both A and
S. Their widths sum to ≤ D − p_k < 2d'.

Consequences, valid for all N:
- A single cluster is never bad.
- A prefix or suffix of a cluster is never bad.
- A cross arc whose two cuts in the two clusters match (a = b) is never bad.
- A cross arc that contains one cluster fully is never bad.

## 4. All N, modulo Hypothesis H
**H.** The blocks of ρ_0 are a fixed head, one middle block, and the mirror tail. (ρ_0 is palindromic up to the
sign (−1)^{N−1}.) Concretely:
- k = 1: the head blocks are {0}, {3}, {5}, {7, 8}. H says ρ_0 has **no zero coefficient** in [10, D − 10].
- k = 2: the head blocks are {0, 2}, {5}. H says there are **no two consecutive zeros** in [9, D − 9].
- k ≥ 3: H says there are no p_k − 1 consecutive zeros in [0, D], so each cluster is one block.

`lemmaC_blocks.py` confirms H exactly for 10 ≤ N ≤ 45: block counts 18, 10, 2, 2, …. At N = 6..9 a few k have extra
middle blocks (for example N = 6, k = 1: 22 blocks). Those N are covered by the direct check.

**Thm 2 (given H, all N ≥ 6).** BLOCK(N, k) holds. Proof:
- **k ≥ 3.** The only proper unions are the single clusters, and these are not bad (§3).
- **k = 1, 2, unions inside the head or tail.** These have width ≤ 8 < d.
- **Unions with both cuts in the head (cross arcs).** A_a + A_b has constant term 2 and width ≤ 8.
- **Unions with both cuts in the tail.** These are the mirror image of the previous case: the leading
  coefficient is ±2.
- **Mixed unions.** Every remaining condition reads

    f = A ± X^D A′(1/X) ≡ 0 mod L′_k,

  with A and A′ nonzero head prefixes. `lemmaC_ends.py` checks all 32 cases (A, A′, ±) exactly over all
  residues of D. In 29 cases a fixed Φ_q (q ∈ {1, 2, 3, 5, 7, 11, 13}, all dividing P/p_k) never divides f.
  The 3 surviving forms factor:
  - 1 − X^D;
  - (1 − X^3)(1 − X^{D−3}) for k = 1;
  - (1 − X^2)(1 − X^{D−2}) for k = 2.

  Each would need ∏_{j≠k, p_j∤3·2} p_j | D − c with c ∈ {0, 3, 2}. That is impossible, because
  0 < D − c < that product.

So Lemma C holds for all N, given H.
- N ≤ 45 is covered unconditionally by the direct run below.
- H itself is a statement about where the coefficients of ∏(1 − X^p) are zero. I did not prove it. It is the
  only remaining gap.

## 5. Free choice of ν_k
Given u_k, the vector ν is determined up to K = ⊕_r ℝ·1_{class r window}. Each condition "J balanced" is a
subspace K_J ≠ ℝ^w (Lemma C).
- The whole fiber ν_0(u) + K is bad only if K ⊆ K_J and u ∈ π(K_J), where π(K_J) is a proper subspace of E_k*.
- So for u_k outside a finite union of proper subspaces, every ν in the fiber outside a finite union of proper
  affine subspaces is W-arc-generic. T2a's random u_k qualify.
- The freedom of ν cannot remove ω-level bad arcs (the clusters). Those are structural: g kills U for every ν.
  Only the W-directions resolve them, as in Thm B.

## Computation
| run | result |
|---|---|
| `lemmaC_blocks.py 2 45 0` (x-level, cyclic, exact) | 0 bad unions, all k, N = 2..45 (about 1 min). Blocks for N ≥ 10: k=1 → 18, k=2 → 10, k≥3 → 2 |
| `lemmaC_blocks.py 2 6 1` (ω-level) | bad unions exist for N ≥ 3 (clusters etc.), N = 3 k = 3: 0. Matches tile2 §3 |
| `lemmaC_ends.py` | 29/32 cases killed by a single Φ_q; 3 killed by the divisibility argument above |

Consistency: N ≤ 4 agrees with tile2's fine-level exact check and with the audit's cyclic check.
