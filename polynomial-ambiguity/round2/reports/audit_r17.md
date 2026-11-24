# audit_r17.md — R17b-A gated audit: Lemma MS⁺, Thm PR2⁺, T8_unamb assembly (r16_unbal)

Script: `scripts/audit_r17_msplus.py` → `scripts/audit_r17_msplus_out.txt` (own code, brute force + exact DP).

## Verdict
| candidate | verdict |
|---|---|
| Lemma MS⁺ (full-range A ≤ C_U, B ≥ −C_V) | **SURVIVES** (caveat C1 wording) |
| Quadrant density c_C/n | **SURVIVES** |
| Thm PR2⁺ (two-sided level, all tails) | **SURVIVES** (caveat C2: state the log-level form) |
| T8_unamb assembly (r16 §6) | **INCOMPLETE as written**: the open one-sided heavy case must also include q_V = 0 (caveat C3) |

No fatal flaw.

## 1. MS⁺: the crux re-derived (fold-centre shift)
Notation as in r13 §0. W = p M q with M = U w V, n = |W|. ρ is placed **outermost**, so W' = p α x β M v_ρ q, and
n' = n + |x| + |αβv_ρ|. Here M is contiguous in W'.
- **Suffix side.** For |q| ≤ k ≤ n − |p|, the suffix of W' of length k + |v_ρ| is (suffix of M of length k − |q|)·v_ρ q.
  So B_{W'}(k+|v_ρ|) = B_W(k) + wt(v_ρ), exactly. B_W is measured from W's own end, and W's end is moved by the fixed
  block v_ρ only. The fold centre does not enter here.
- **Prefix side.** For k' ≤ |pαx|, A_{W'}(k') ≥ −|p| − |α| − K.
- **Window.** For k ≤ n/2, k' = k + |v_ρ| satisfies k' ≤ n'/2 when |x| ≥ |v_ρ|, and k' ≤ |pαx| when |x| ≥ n/2 + |v_ρ|.
  The fold centre of W' is at about (n + |x|)/2. That is **to the right of** every k' that is needed, so lengthening helps.
  The chord condition of W' even constrains B_W(k) for all k ≤ n − |p|, not only k ≤ n/2.
- **Conclusion.** G⁻(W') gives B_W(k) > −K − |p| − |α| − wt(v_ρ) for |q| ≤ k ≤ n/2. Since W' ∈ L (prepending a
  first-return loop to the token sequence is a legal derivation), this holds for every pair-model word. (a) is the mirror
  image (u_ρ outermost on the left, the V-level y in v_ρ), and I checked it the same way.
- r13's restriction to U-positions was indeed gratuitous: r13 step 4 already transports A for every position inside M.
  audit_r16 recorded the restricted form "B ≥ −C_V for k ≤ |Vq|", which is weaker than needed but not wrong.

**Brute force** (Test 1/2). 300 random (p, q, α, β, v_ρ) instances, |M| ≤ 12, all 2^{|M|} middles each, a random U-level
x of length ≥ n (resp. a V-level y). Every W with W' ∈ G⁻ was checked against the full-range bound at **every**
k ≤ n/2: 10,173 + 11,445 words tested, **0 violations**.

## 2. Quadrant density
A(·) for k ≤ ⌊n/2⌋ reads letters 1…⌊n/2⌋, and B(·) reads letters n−⌊n/2⌋+1…n. These are disjoint, so the two
coordinates are exactly independent under the uniform measure. The density is a product of two one-dimensional
ballot probabilities, each ≤ c(C+1)m^{−1/2}.
- With ±1 steps: brute force equals the DP exactly for n = 8, 12, 16.
- n·density (C = 0) = 1.2683, 1.2720, 1.2729 → 4/π.
- C = 10: n·density/(C+1)² = 0.95, 1.18, 1.25, so it stays bounded.
- r16's C = 1 values (≈11) use ±½ steps, i.e. C = 2 in my scale. That is consistent.

## 3. PR2⁺
The renewal lower bound is correct: Lemma R plus a tail upper bound only. F̄ = O(y^{−β₀}) follows from the union bound
with a geometric step count. Mass O(log N) versus cN^{β₀} gives the contradiction. The tail step relies on the cited
B–D Thm 3 for the exponents, which I did not re-check.

## Caveats
- **C1 (wording).** "For every W ∈ L" should read "for every pair-model word p·M(s)·q (same context p, q, exit w)". Only
  these words enter the lower bound, so nothing changes. Small n (with |p| > n/2) is absorbed in the constants.
- **C2 (log-level).** Theorem SM / Prop HL only guarantee that heavy blocks are U-/V-**level or log-level**. PR2⁺ as
  stated needs constant K. The fix is immediate and should be written:
  - take x from the geometric family with |x| ∈ [n, 2n + c] (as in r14 §4);
  - then K₁ = O(log n), so L_n ⊆ Q_n(C + c log n);
  - its density is ≤ c(log n)²/n, so the mass is O(log³ N) ≪ N^{β₀}.
  - No DW uniform bound is needed (the bound is 1-D and linear in C+1). This also removes audit_r16 C7.
  - Also note that MS⁺ needs no *heaviness* of the level block, only arbitrarily long level words. So a **light** V-level
    block on the V tape (e.g. b*) already makes a model two-sided.
- **C3 (assembly gap is larger than flagged).**
  - r16 §6 lists the one-tape case as covered by "PR1 and r15_onesided §4".
  - PR1 needs a block that is **both** U- and V-(log-)level. That is HL's e = 0 branch. With that, the case is covered for
    all tails, because μ = ∞.
  - r15_onesided §4 (one-tape, U-level only) ends with mass O(N^{1/3}) < c√N. So it needs (T½), and r15_tails §6's
    "one-tape holds for all k" is true only for the PR1 subcase.
  - Hence the **uncovered case** is: the U side has a heavy U-(log-)level block that is not V-(log-)level (HL e > 0
    branch); the V side has no V-(log-)level block at all; and β₀ ≤ 1/4. Here **q_V ≥ 0, including the one-tape case
    q_V = 0**, together with its mirror.
  - In all of it, MS⁺(b) gives only the 3π/4 wedge (N^{1/3}).
- **C4.** I did not re-audit the reduction chain (r9 Cor H / r10–r12 ⇒ critical linear SCC with a pair model) or
  B–D Thm 3. I also did not re-audit Theorem SM's dependence on r14 Lemma Bot and Prop HL, beyond audit_r16.

## T8_unamb status
Closed for every pair model with a U-(log-)level block on the U tape **and** a V-(log-)level block (heavy or light) on
the V tape, for any tails, given C2.
- One-tape and one-sided models are closed under (T½). One-tape models with an e = 0 block are closed for any tail.
- Side mismatch is impossible (SM).
- **Remaining:** one-sided heavy (C3, q_V ≥ 0), modulo the reduction chain.
