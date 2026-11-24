# audit_m1.md — gated audit of r19_m1 (Lemma TS, Lemma D, Thms M1/M1′)

Script: `scripts/audit_m1_words.py` → `scripts/audit_m1_words_out.txt` (~2 s, brute force over {a,b}^n, n ≤ 20).

## Verdict
**SURVIVES**, with caveats C1–C5. No fatal flaw found.

## Checks
**Canonical decomposition.** For a fixed (t, σ) the cut O / Σ / I is determined, and (t, σ) ↦ (O, Σ, I) is injective.
The plug-back recovery of O from (filled tree, hole offset) is unique: in an ε-free grammar, nodes sharing one span form
a unit-rule chain, and with no unit cycles each label appears at most once on that chain. ✓ TS needs no canonical
choice of derivation. It counts **pairs**, and every word of Bad_T(n) has at least one qualifying pair (any of its
derivations with the bad π_h-run). So words ≤ pairs. ✓

**Outer and inner pieces ≤ poly·2^len.** A filled O is an S-tree of a word of length ℓ_o + |f| in L. The number of
such trees is ≤ 2^{ℓ_o+c}(ℓ_o+c)^k by **per-word** polynomial ambiguity. I is handled the same way through a fixed
context. ✓

**Not a count sandwich (§6).** The only counting input is the upper bound d_ℓ ≤ ℓ^k·2^ℓ, used for O and I, and that
bound is true. The gain e^{−θa} comes from a structural fact, ρ(M_θ) < 1, which a sandwich cannot supply. The target
statement |Rot(Bad)| = o(2ⁿ) is itself an upper bound on a set of words, so an upper count is the right tool. ✓

**Transfer matrix and θ range.** In a linear SCC every T-rule X → αYβ lies on a cycle. (H1) gives entrywise
analyticity of B_α(e^θ/2) near θ = 0. The spectral radius is continuous, so ρ(M_θ) < 1 on some [0, θ₁]. The identity
Σ_Σ x^{a′} y^{b} = ((I − M)^{−1})_{XY} is the standard path expansion. ✓
- Exact word-level counts match θ* = sup{θ : ρ(M_θ) < 1} exactly:
  - G1 (the audit example, with critical exit Z → aZ | bZ | a): frac(≥ a + 1)/frac(≥ a) = 0.250 = e^{−ln 4} at
    n = 18 and n = 20.
  - G1′ (left material C = a*b, light infinite, X → CXa | Z): the ratio per 2 letters is 0.562 = (3/4)², which
    gives θ* = ln(4/3).
  - The maximum ambiguity is ≤ n in both, so poly-ambiguity holds.
- The candidate's G1/G3 tree-level numbers are consistent with these.

**Lemma D.**
- (i) ✓ An infinite entry of M_T(½) comes from a lower pole, and then ρ(M_T(z)) → ∞ as z ↑ ½.
- (ii) ✓ This is the Perron pairing (1 − ρ)uᵀF′ = uᵀΦ_z > 0.
- (iii) ✓ F_X ≥ cF_X² holds on [¼, ½) via one two-T rule and strong connectivity. So F_X is bounded below r_T,
  while F_X ≥ c′F_Y → ∞.

**M1′ case 1.** LG(c) is label-based: Z ⇒* (…Z₂…)Z(…) with Z₂ ∈ T. Every T-node is therefore left-good whichever child
π_h enters. ✓ (This inherits A1.)

**Coverage of the left material.** A radius-½ left part is either a pole (excluded by D(i)) or it reaches a critical
nonlinear SCC (then LG(c) applies). The lowest radius-½ SCC is critical. A linear critical SCC gives a pole, which
propagates upward. ✓

## Caveats
- **C1.** The exponent is misstated. #O·#I contributes n^{2k+1}, so the bound is C·n^{2k+4}·2ⁿe^{−θa}, not n^{k+3}.
  This is harmless, because e^{−θ log⁴n/c} is super-polynomial.
- **C2.** The proof of D(i) says "ρ(J(z₀)) ≥ 1 for z₀ ≤ ½ ⇒ divergence below ½". This is false at equality with
  z₀ = ½. It should read ρ > 1 (or ρ ≥ 1 with z₀ < ½). Only the strict case is needed for the conclusion ≤ 1.
- **C3.** "a ≥ h/c" is supplied by the assembly's case split, not by TS. Letters of [0, h) at **between-SCC** steps
  (S-factors) are not in Σ. They remain with U2, and the pigeonhole with c = N_SCC-dependent is U4. TS itself is
  stated correctly as a pair count with no left-badness input.
- **C4.** M1′ case 1 and the "heavy left ⇒ left-good" coverage rest on LG(c), and so carry caveat A1.
- **C5.** θ and C depend on G only, which makes them uniform in n and a, as §9 requires. The claim "in fact
  super-polynomially small" is correct.
