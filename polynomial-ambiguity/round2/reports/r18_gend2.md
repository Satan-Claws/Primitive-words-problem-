# r18_gend2.md — R18-B2: the light-left / heavy-right spanning SCC in G⁻

Status (honest):
- **Light-or-finite-left / heavy-right spanning linear SCC: CLOSED** [written proof]. It is removed from the
  residual R⁻ of r18_gend §4. Inputs: Lemma L in its poly-ambiguous form (the mirror of r18_gend LG(c), i.e. SM + HL,
  with the audit caveats C3/C7 for log-level), plus elementary walk counting. **Criticality of T, spanning, and the
  (AM) bound are not used.**
- Mechanism: this is **not** an end insertion. The heavy right part gives a V-level insertion **at the top node of the
  T-segment**. It puts a ceiling on A over the whole segment, and the ceiling depends only on the right context q of
  that node. So it **survives every re-routing or pumping below the node**, which is exactly what failed in r18 Step 1
  ("pumping moves the right part across the centre").
  - Consequence: every cycle left-yield s of T has D(s) ≤ 0.
  - So the left-label prefix is a walk with all rises ≤ R = O(log n).
  - The count gain is exp(−c·h/log²n), and h = log⁴n suffices.
- The task's "innermost" insertion is the special case where the node is the spine bottom (r17 MS^in). On its own it
  gives only a relative barrier (A ≤ max_{j≤|Vq|}B + c), and that is useless when |Vq| ≈ n. What makes it work is
  inserting **at or above the pumped cycle**.
- **R⁻ after this note:** only the light/light case remains (both parts radius > ½). That case reduces to (AM)
  (r18_gend §4.1, R18-A).

Script: `scripts/r18_gend2_checks.py` → `scripts/r18_gend2_checks_out.txt` (~1 s).

Notation: as in r18_gend. Steps are ±1. P is the prefix walk, A(k) = P(k), B(k) = P(n) − P(n−k), and
G⁻ = {A(k) < B(k) for 1 ≤ k ≤ n/2}. G is reduced, ε-free and polynomially ambiguous, with L(G) ⊆ G⁻.

## 0. Hypothesis RH
A linear SCC T is **right-heavy (RH)** if some T-rule Z₁ → α₁Z₂β₁ has, in β₁, a nonterminal H with H ⇒* sYt, where Y
is a critical nonlinear SCC.
- For critical T, right parts are either light (radius > ½) or RH. A radius-½ right part must reach a critical SCC; a
  critical *linear* one below T is impossible by Lemma ST(i).
- So "heavy V-parts" in r18_gend §4.1 is RH.
- Left parts of a left-bad T are light or finite. A heavy left part would make T left-good by LG(c), and a critical
  linear SCC below T is again impossible.

**V-level supply [cited: r18 LG(c), mirrored].** G⁻ is invariant under reverse + swap (A ↦ −B, B ↦ −A). Applying LG(c)
to the mirrored grammar gives the following.
- L(Y) contains words of geometric lengths (ℓ_{i+1} ≤ 2ℓ_i + c) with suffix profile D(x) − P_x(|x|−j) ≤ K(ℓ), where
  K(ℓ) = c log ℓ, or K constant in the level case.
- Padding by s and t keeps this up to a constant.
- This is Lemma L's V-half in the poly-ambiguous form. Only "trees ≤ poly·words" is used, in SM Step 2.

## 1. Lemma RP (right-part insertion at a node) [written proof]
**Statement.** Let T be RH, let W ∈ L with a derivation containing a T-node ν with span [s, e), and put q := W[e, n).
Then for every k ≤ e:

  A_W(k) ≤ max_{0≤j≤|q|} B_W(j) + c₁ + K(3n + c),

where c₁ depends only on G.

**Proof.**
1. *Construction.* Strong connectivity gives a cycle at ν's label X through the RH rule:
   X ⇒* σZ₁τ ⇒ σα₁Z₂β₁τ ⇒* σα₁σ′Xτ′β₁τ.
   Fix shortest words for every nonterminal except H. The cycle then has a fixed left part u_ρ and a right part
   α x β, where x is any V-level word as in §0 with n + 2|u_ρ| ≤ |x| ≤ 3n + c.
   Put W′ = W[0, s) u_ρ W[s, e) α x β q ∈ L, with n′ ≥ 2n + 2|u_ρ|.
2. *Prefix side.* For k ≤ s, A_{W′}(k) = A_W(k). For s ≤ k ≤ e, A_{W′}(k + |u_ρ|) = A_W(k) + D(u_ρ).
3. *Suffix side.*
   - For j ≤ |q|, B_{W′}(j) = B_W(j).
   - Across β, B_{W′} ≤ B_W(|q|) + |β|.
   - Across x, B_{W′} = B_W(|q|) + D(β) + (suffix profile of x), which is ≤ B_W(|q|) + |β| + K.
   - These three ranges cover every j ≤ |q| + |β| + |x|. That includes every j ≤ e + |u_ρ|, because |x| ≥ n.
4. *Apply G⁻ to W′.* Every k ≤ e + |u_ρ| satisfies k ≤ n′/2. So A_{W′}(k) < B_{W′}(k) ≤ max_{j≤|q|}B_W(j) + |β| + K.
   Undo the shift D(u_ρ) to get the claim, with c₁ = |β| + |u_ρ|. ∎

Check (1) of the script tests this bookkeeping: 7,538 random instances with W′ ∈ G⁻, 53,826 values of k, **0
violations**.

**Comparison with r17 MS^in.** MS^in is Lemma RP at the spine bottom, mirrored. The new points are these:
- RP holds at **every** node, and the barrier covers all k ≤ e, not only k ≤ n/2.
- The barrier depends only on q = W[e, n).
- So it is **invariant under any change of the derivation strictly inside ν** (§2).

## 2. Proposition NC (no positive cycles) [written proof]
**Statement.** Let T be RH. Every cycle of T — a spine path X ⇒* s X t through T-rules, with **any** choice of
left-sibling yields — satisfies D(s) ≤ 0.

**Proof.**
1. Fix W ∈ L with a T-node ν₀ labelled X. G is reduced, so such a W exists. Let s₀ be its span start and q its right
   context.
2. Pump the cycle m times directly below ν₀: W_m = W[0, s₀) sᵐ (yield of ν₀) tᵐ q ∈ L. Here ν₀ is still a T-node with
   right context q, and |W_m| ≤ n + m(|s| + |t|).
3. Lemma RP for W_m at k = s₀ + m|s| gives
   A_W(s₀) + m·D(s) ≤ max_{j≤|q|}B_W(j) + c₁ + c·log(3(n + m(|s| + |t|)) + c).
4. The left side is linear in m and the right side is logarithmic in m. Since D(s) is an integer, D(s) ≤ 0. ∎

(For a cycle at a different state, pump it at the corresponding spine node below ν₀, or use a W containing that state.)

**Corollary NC′ (bounded rises).** Let ℓ = b₁b₂⋯b_r be the left-label word of a T-spine segment, where b_i is the
left-sibling yield of step i. Suppose every |b_i| < L. Then every rise satisfies P_ℓ(j) − P_ℓ(i) ≤ R := (N_T + 2)L for
i < j, where N_T is the number of T-states.

*Proof.* The steps between the blocks containing i and j form a spine path. Delete cycles repeatedly; by NC each one
has D ≤ 0. What remains is a simple path of ≤ N_T steps, each contributing ≤ L. The two partial blocks contribute
≤ 2L. ∎

(Left-finite case: L = max label length is a constant, so R is a constant. NC′ then says directly that the regular
language Lft_T has no complete DFA component, i.e. growth < 2. This is r18 Step 1 restored for spanning T.)

## 3. Theorem GE⁻-RH [written proof, modulo r18_gend §2/§4 framework + §0 citation]
**Statement.** Take h = log⁴n in the r18_gend §2 h-path decomposition. Consider the words W ∈ L_n with a derivation in
which ≥ h/2 letters of [0, h) are left parts of π_h-nodes in left-bad **RH** linear SCCs. Their rotation image is
o(2ⁿ).

**Proof.**
- Bad-left is as in r18. The T-factors of W[0, h) are the left-label words of RH segments, plus partial blocks.
- There are at most 2c₁ factors in total.
- **Long blocks.**
  - A single step's left yield is a word of a product of light languages, with radius ≥ z₁ > ½.
  - The prefixes of length h containing such a block of length ≥ L = A log n number ≤ c·h²·2ʰ(2z₁)^{−L}.
  - After the factor n for rotation and (h+1)^{c₁} for skeletons this is o(2ʰ), for A large.
- **All blocks < L.**
  - By NC′, each RH factor of length ℓ_j is a walk with all rises ≤ R = O(log n).
  - The rise-bounded walks of length ℓ are counted by a transfer matrix on the states r = P − running min ∈ [0, R].
    Its spectral radius is ρ_R = 2cos(π/(2R+3)), so 2 − ρ_R ≍ π²/(4R²) (script check (2), exact). The count is
    therefore ≤ (R+1)·ρ_R^ℓ.
  - The RH factors have total length ≥ h/2. So the number of prefixes is
    ≤ (h+1)^{c₁}(R+1)^{2c₁}·2ʰ·exp(−c·h/R²) = 2ʰ·exp(−c log²n + O(log log n)).
  - Other factors are bounded by 2^{length}, or by r18's g < 2.
- **Rotation.** The factor n·2^{n−h} gives |Rot| ≤ 2ⁿ·n·exp(−c log²n) → 0.
- **Compatibility of h = log⁴n with the rest of the chain.**
  - T-tol needs h = o(n/log n). ✓
  - r18 §4's C_W ≤ √n log n restriction is unchanged.
  - r18 Steps 1–2 and 3 give exponential gains in h, which only improve for larger h. ∎

**Corollary (R⁻ update).** The irreducible remainder of r18_gend §4.1, "spanning critical linear T with finite or
light U-parts and heavy V-parts", is **empty** as an obstruction: its words are o(2ⁿ) after rotation. Only the
light/light spanning case remains, and it is excluded by an (AM)-type bound E_n[m] = o(n).

## 4. Remarks / caveats
- **Side corollary (critical T, RH).** With r18 §4.2 (E D(u) = 0, written sketch), NC forces D(u) = 0 for every
  first-return token in the support. This is consistent with r18's numerical check (2b): finite balanced G⁻ tokens are
  pure-left.
- **Non-critical RH T** is covered as well; nothing in §1–3 uses ρ = 1.
- **Inputs.**
  - The only non-elementary input is the V-level supply (§0). It is exactly what r18 §4.1 already asserts ("right-end
    insertions are fine").
  - The log-level variant affects only Proposition NC, and only through log m. It is harmless.
- **Not done.** The light/light case. Lemma RP needs a radius-½ nonlinear block in some right part, so it gives nothing
  there.

## Status table
| item | label |
|---|---|
| Lemma RP (V-level right-part insertion at any node: A ≤ max_{j≤\|q\|}B + c on [0, e]) | written proof + bookkeeping check (0/53,826) |
| Prop NC: RH ⇒ every cycle left-yield has D ≤ 0 | written proof |
| Cor NC′: bounded rises R = (N_T + 2)L; left-finite ⇒ Lft growth < 2 | written proof |
| Rise-bounded count ρ_R = 2cos(π/(2R+3)) | exact (DP = brute force, eigenvalues) |
| Thm GE⁻-RH: light/finite-left + heavy-right spanning segments are rotation-negligible (h = log⁴n) | **written proof** modulo §0 citation + r18 framework |
| R⁻ remainder | light/light only (⇐ (AM)-type E_n[m] = o(n)) |
