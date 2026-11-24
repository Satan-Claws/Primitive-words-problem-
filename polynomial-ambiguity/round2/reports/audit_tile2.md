# R2/audit_tile2: gated audit of R2/tile2.md, Theorems A and B (min-cost-transport rule, ply 1)

**Verdict: SURVIVES, with one mandatory correction (C1).** No fatal flaw was found. As written, the x-level
dictionary of §0 does not match S2P's K_T when μ_{v₀} < 0. The fix is one line (root at a positive vertex). I checked
that the fix keeps all hypotheses: Lemma C holds for every *cyclic* arc [computational, exact for N = 2, 3].

## Checks against the definitions
1. **Validity ⇔ positive tree flows (ω-level): correct.**
   - For a child c of the root: if c is positive, f = m′(S_c); if c is negative, f = −m′(S_c), since Σm′ = 0.
   - So "all f_e > 0" is exactly tile.md / S2Y's K_T. This holds with bichromatic colours sgn μ_i, masses
     μ_i x_i on unfolded x ∈ W, and folds only at ω-level.
2. **(C1) Root condition missing at x-level. Not fatal: repaired.**
   - S2P defines K_T = {x ∈ W : n_v(x) has the sign of top(v) **for all v**}. This includes the root:
     n_root = μ_k(x) = τ.
   - LAM §2(b) gives the same condition. The root-edge coordinate is c_root = τ / (a μ_root), so the piece needs
     sgn μ_root = sgn τ.
   - On S2P's region R_k(u), τ = u_k(x_k) > 0. So the root must be **positive**.
   - tile2 roots every tree at v₀ = supp[0] and imposes only non-root conditions. When μ_{v₀} < 0, every
     F_c tree is S2P-invalid everywhere on R_k(u). Coverage is then 0, not 1.
   - Concrete case (N = 2, k = 1, n = 36): ν = [−30, 24, −3, −17, 44, −44, −1, 50, 39, 25, 26, −19] gives
     μ_{v₀} = −60. At x = 10ω + δ (script seed), τ = 7536 > 0. The tree T* = supp of the LP optimum is "valid" in
     tile2's sense and NC, but fails S2P's condition at root v₀ (`audit_tile2_root.py`).
   - **Repair:** cut the circle just before a positive support vertex and root there.
     - The proofs of (i) and (ii) do not use which vertex is the cut. The near-U region R⁰ = {m_{v₀} > τ} still
       contains R_k(u) near U.
     - Lemma C must then hold for arcs that wrap the old cut. `audit_tile2_cyclicarcs.py` checks this: 0 balanced
       cyclic arcs on W for N = 2, 3 (exact in ν) and N = 4 (one random ν, all k).
     - Rule test with a positive root and S2P's full condition, N = 2, k = 1, 2, 3 values of ν each: T* is
       S2P-valid 30/30 every time, with 0 pairwise ply violations (`audit_tile2_repair.py`).
3. **Uncrossing (Q): correct.**
   - Crossing on ℤ_n is interleaving, which does not depend on the cut. So the line cost h(|y_i − y_j|) is
     legitimate.
   - Same colour: the nested re-pairing (a,d), (b,c) is bichromatic. Lengths have equal sums with a larger spread,
     so strict concavity gives a strict decrease.
   - Opposite colour: the disjoint re-pairing (a,b), (c,d) is bichromatic. Both lengths shrink, so strict
     monotonicity gives a strict decrease.
   - Marginals are preserved.
4. **Non-degeneracy and genericity: correct.**
   - Ply ≤ 1 uses only that the generic c makes the optimum unique. Reduced costs are the alternating sums around
     fundamental cycles.
   - Each component of an optimal forest is balanced. Components of an NC forest are non-interleaving, so if there
     are ≥ 2, one is a proper arc.
   - An arc containing v₀ is handled through its complement. tile2 leaves this implicit; it is fine because
     Σm′ = 0.
   - The bad x lie in finitely many hyperplanes {m(I) = 0}, so a generic η ∈ W resolves every wall. This is S2P
     §1(b)'s rule, since every edge form is non-zero on W.
   - The lex rule needs η ∈ W rather than η ∈ U, because for N ≥ 3 the cluster arcs are ≡ 0 on U. tile2 states
     this correctly.
5. **Patching (S2P §1(a)): correct.**
   - q_k counts trees, so the bound is ply_VC · 1.
   - The edge-vector data of a piece (LAM §2(b): a/b = |μ_q|/|μ_p|) do not depend on h or y. The cost only selects
     *which* trees are used, so no n-dependence enters K or the piece data.
   - The number of pieces can be exponential. tile2 says so.
6. **Scope of "S_N blocked geometrically for N ≤ 4": mislabelled, otherwise fine.**
   - It says [written proof], but Lemma C at N = 2, 3, 4 is [computational, exact certificate]. At N = 4 it rests
     on one random integer ν. Balance is linear in ν, so this suffices for generic ν, but not for "every u_k".
   - "Modulo realisability" is stated in the next paragraph and should sit in the claim itself, as S2P §3 phrases
     it.

## Non-fatal caveats
- C1 (above) must be applied to Theorem B and §5. Without it, the claimed equality with "S2P's K_T with root v₀" is
  false for half of the ν.
- Realisability of the root edge {v₀, o_k}: the outside vertex o_k must lie in a gap next to v₀ for laminar
  nesting. The positive root may then be constrained further. For N = 2, k = 2 the support is all of ℤ₃₆. This
  belongs to LAM §2(c) and is not TILE's concern, but it belongs in the realisability list (§5, item 2).
- For N ≥ 3 the selected trees at a base point ω have cluster-cut edges with forms ≡ 0 on U. These enter V′, so
  near ω the piece is {u_k > 0} ∩ {cluster-cut forms > 0}, not a half-space. LAM's face condition still holds,
  because U ⊆ span V_F, but "Local form" (prompt §4.4(i)) must be read with this extra factor.
- Genericity of a cost of the form h(|y_i − y_j|) off all alternating-cycle hyperplanes is asserted, not proved. It
  is easy for h = √ and algebraically independent y, but should be stated.
- Numerics are a float LP with exact checks of validity, NC and spanning. Fine as evidence only.

## Files
- `polynomial-ambiguity/round2/scripts/audit_tile2_root.py`: C1 counterexample (μ_{v₀} < 0, τ > 0).
- `polynomial-ambiguity/round2/scripts/audit_tile2_cyclicarcs.py`: Lemma C for all cyclic arcs, N = 2, 3, 4.
- `polynomial-ambiguity/round2/scripts/audit_tile2_repair.py`: repaired rule with S2P's full validity, N = 2.
