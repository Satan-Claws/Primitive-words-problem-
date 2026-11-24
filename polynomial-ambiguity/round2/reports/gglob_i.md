# R2/gglob_i: G-glob′ (i), the level-t correlation bound

W4, 2026-11-24. Builds on `R2/gglob.md` (Lemma G5, §4 (i)). Notation is from there: n = P², s_k = n/p_k,
V_k = s_k-periodic vectors, L(M) = span{e_p + e_q : pq ∈ M}, A(M) = span{e_p − e_q : pq ∈ M}.
Scripts: `round2/scripts/gglobi_csp.py`, `gglobi_struct.py`, `gglobi_dist.py`.

**Verdict.**
- (i) reduces to a purely combinatorial covering lemma (I2) about the difference vector z = Dy. The reduction is a
  written proof (Thm I1), and it gives an explicit 𝒟 that depends only on n.
- When I2 holds, the bound is Pr ≥ (16/729)^N = n^{−o(1)}, which is stronger than the n^{−O(1)} that (i) asks for.
- I2 itself is [written proof] for N = 2 and in a "residue-transversal" case, and [computational] otherwise.
  Adversarial and structured searches at n = 36 and n = 900 found no counterexample.
- So (i) is **conditionally affirmative**. No anti-correlation obstruction was found.

## 0. Adjacent-pair certificates (Lemma I0) [written proof]
Put z = Dy, that is, z_x = y_x − y_{x+1}. Take a ≡ b (mod s_k), a ≠ b, with z_a ≠ z_b, and suppose
{a, a+1} ∈ M and {b, b+1} ∈ M. Put μ = e_a − e_{a+1} − e_b + e_{b+1}. Then:
- μ ∈ A(M);
- μ ⊥ V_k, because a ≡ b and a+1 ≡ b+1 (mod s_k);
- μ(y) = z_a − z_b ≠ 0.

So y ∉ V_k + L(M). Call such {a, b} a **k-witness**.

Facts used below:
- z ∈ V_k ⇔ y ∈ V_k. Indeed, if Dy is s-periodic, then y_x − y_{x+s} = c for all x, and summing over an
  s-class gives p·c = 0.
- The k-witnesses exist ⇔ z is non-constant on some s_k-class ⇔ y ∉ V_k.

This generalises gglob.md's shift certificate. The (1 − T^{s_k})(e_p − e_q) certificate is the case b = a + s_k
with both pairs taken from M₀ or both from M₁. Here the two pairs need only be adjacent pairs, so M can mix the two
parities.

## 1. Thm I1 (reduction of (i) to Lemma I2) [written proof]
**Lemma I2 (witness covering).** For every y ∉ ⋃_k V_k there is a set S ⊆ ℤ_n such that:
- S contains no two cyclically consecutive points;
- |S| ≤ 2N;
- for every k, S contains a k-witness.

**Distribution 𝒟** (depends on n only).
1. Draw X_x ~ Bernoulli(1/3) independently for x ∈ ℤ_n.
2. Put A = {x : X_x = 1, X_{x−1} = X_{x+1} = 0}. Its points are pairwise non-consecutive, so the pairs
   {x, x+1} (x ∈ A) are disjoint.
3. Let M consist of these pairs plus the adjacent matching of the remaining n − 2|A| points in their cyclic order.

M is a non-crossing perfect matching: an adjacent pair {x, x+1} has no point strictly inside it, so it crosses
nothing, and the remaining points are matched adjacently in the reduced cycle.

**Thm I1.** If I2 holds for y, then Pr_{M∼𝒟}[∀k: y ∉ V_k + L(M)] ≥ 3^{−|S|}(2/3)^{|N(S)|} ≥ (16/729)^N.
Since N ~ ln n / (2 ln ln n), this bound is n^{−O(1/ln ln n)} = n^{−o(1)}.

*Proof.*
- If S ⊆ A, Lemma I0 certifies every k.
- The event S ⊆ A says X = 1 on S and X = 0 on N(S) = (S ± 1) ∖ S. These are disjoint sets, because points of S
  are pairwise at distance ≥ 2.
- So the event has probability exactly 3^{−|S|}(2/3)^{|N(S)|}, with |N(S)| ≤ 2|S| ≤ 4N. ∎

A rotation or other poly-size family also works. Any family containing, for each admissible S, a matching that
contains S's adjacent pairs is enough. 𝒟 is simply a convenient one.

## 2. Lemma I2: what is proved
**Residue coordinates.** Write x = r + P·t with r, t ∈ ℤ_P, and u_r(t) := z_{r+Pt}.
- Every s_k-class lies inside one residue class R_r = r + Pℤ, since P | s_k.
- By CRT, ℤ_P = ∏_j ℤ_{p_j}. On R_r, "V_k" means that u_r does not depend on the k-th CRT coordinate. A k-witness
  in R_r is a pair on a k-line (a set of points that differ only in coordinate k) where u_r is non-constant.
- Put K_r = {k : u_r depends on coordinate k} and Q_k = {r : k ∈ K_r}. Primitivity means Q_k ≠ ∅ for all k.
- Two points of S can be adjacent only if their residues are adjacent in ℤ_P.

**(a) Residue-transversal case [written proof].** Suppose some set I ⊆ ℤ_P with no two consecutive residues has
⋃_{r∈I} K_r = [N]. For each k, choose r ∈ I ∩ Q_k and any k-witness in R_r. No conflicts are possible. Special cases:
- a single r with K_r = [N] (a "hub");
- I = even residues, which is M₀;
- I = odd residues, which is M₁;
- I = residues ≡ c (mod 3).

**(b) N = 2 (n = 36, and any two primes p, q, n = (pq)²) [written proof].** If (a) fails:
- Q₁ ∩ Q₂ = ∅, and every r₁ ∈ Q₁ is adjacent to every r₂ ∈ Q₂.
- In C_6, two distinct vertices have at most one common neighbour. So, up to swapping the primes, Q₁ = {ρ} and
  ρ′ := ρ ± 1 ∈ Q₂.
- Then u_ρ depends only on coordinate 1, as f(t₁), and u_{ρ′} depends only on coordinate 2, as g(t₂).
- Adjacency between R_ρ and R_{ρ′} is t ↔ t + ε for a fixed ε ∈ {0, 1}, a translation that preserves lines.
- Take a 1-witness {t, t′}: f(t₁) ≠ f(t′₁), with a common free second coordinate β. Take a 2-witness {s, s′}:
  g(s₂) ≠ g(s′₂), with a common free first coordinate α.
  - If p₂ ≥ 3, choose β ∉ {s₂, s′₂} after the shift.
  - Otherwise p₁ ≥ 3, and choose α ∉ {t₁, t′₁}.
- The two pairs are then disjoint and non-adjacent. ∎

**(c) General N: OPEN.**
- The translation argument extends whenever each used residue has a free coordinate with ≥ 3 values against each
  neighbour.
- The unproved residue is the long chains of adjacent private residues where the free coordinates are p = 2. These
  are cylinder point masses on [N] ∖ {1}.
- A Lovász local lemma or Hall-type argument over the translations is the natural route. I have not done it.

## 3. Computations [computational]
**Lemma I2 searches** (`gglobi_csp.py`, `gglobi_struct.py`).

| test | n | instances | I2 failures | min # admissible witness tuples |
|---|---|---|---|---|
| hill-climb over small-alphabet z, minimising # solutions (3 runs: 10, 200, 200 restarts × 4000 steps) | 36 | 410 restarts | 0 | 2 (hub at a point mass) |
| hill-climb from sparse z (300 steps) | 900 | 6 restarts | 0 | 8 |
| structured: cylinder point masses / one-coordinate functions on runs of adjacent residues (incl. wrap) | 36 | 13 377 primitive | 0 | — |
| same | 900 | 1 749 primitive | 0 | — |

**Exact certification** (`gglobi_dist.py`, rank mod 2³¹−19, via `gglob_matching.in_VkLM`).
- For every tested y, M_S (the pairs of S plus either adjacent completion) certifies all k: 52/52 at n = 36 (G6 y twice, the
  rest sparse/orbit), 6/6 at n = 900.
- Lemma I0 had 0 violations over all sampled M ∼ 𝒟 with S ⊆ A.
- Empirical Pr_𝒟[all k certified]:
  - n = 36 G6 vector: 62/300. The fixed M₀ and M₁ both fail here.
  - n = 36 sparse vectors: ≈ 1.
  - n = 900: 10/10 on 6 vectors.
- The I1 lower bound ranges from 1e−5 to 3e−3 on these vectors. It is very conservative.

## 4. Negative side
No obstruction was found. Note that a failure of I2 would **not** refute (i): M can also use non-adjacent pairs
(chords {x, x+d} with d odd, nested 4-blocks, and so on).
- An obstruction would need a primitive y such that every NC matching except an n^{−ω(1)} fraction has, for some k,
  d_M(y) ∈ d_M(V_k).
- I2 excludes this unless it fails. Where I2 is proved, the event "a certificate exists" is witnessed by O(N) local
  pairs, so it has probability n^{−o(1)}.

## Status
| claim | status |
|---|---|
| I0: adjacent-pair k-witness ⇒ y ∉ V_k + L(M) | [written proof] |
| I1: I2 ⇒ G-glob′ (i), with explicit 𝒟 (depends on n only) and bound (16/729)^N = n^{−o(1)} | [written proof] |
| I2 in the residue-transversal case; I2 for N = 2 | [written proof] |
| I2 for N ≥ 3 | [computational] (n = 900, structured + adversarial), OPEN in general |
| G-glob′ (i) | conditional on I2; unconditional at n = 36 |
| G-glob′ (ii) (signed level-s sub-instance) | untouched, OPEN |
