# r15_side.md — R15-A: side mismatch cannot occur

**Status: gap 1 of r14 §5 is CLOSED [written proof; elementary + standard Perron–Frobenius/IFT facts].**
- On the U side, every heavy block admits a choice (w₀, binary form) in Prop HL with e ≥ 0. So it is U-level or
  U-log-level. The mirror statement holds on the V side (e ≤ 0).
- The mechanism is the zero-mean-drift heuristic made exact, and it needs no bivariate analysis. Suppose D is bounded
  above on a critical SCC. Then D has a **potential**: every rule of the SCC is drift-balanced, D is "cohomologous to a
  constant", and e = 0 is attained. If instead some rule had positive slack, the language would have exponentially
  fewer than 2ⁿ words, which contradicts radius ½.
- The other gaps stay open: the one-sided case (R15-C), heavier tails (R15-B), and T8_unamb.

Script: `scripts/r15_side_checks.py` → `scripts/r15_side_checks_out.txt`.
Notation as in r13 and r14: D(a) = +½ and D(b) = −½. The grammar is unambiguous and reduced. C* and Y ∈ C* come from
Lemma Bot: C* is a critical nonlinear SCC of radius ½, and every SCC strictly below it has radius > ½. B ⇒* sYt.

## 1. Statement
**Theorem SM.** Let C* and Y be as above, and let Y ⇒* αYβYγ be any binary form from Lemma Bot, with d = D(αβγ).
(U) If D(w₀) + d < 0 for every w₀ ∈ L(Y), we get a contradiction. More precisely, some binary form and some w₀ give
    e = D(w₀) + d = 0.
(V) Mirror: some choice gives e ≤ 0.
So, by Prop HL, a heavy block on the U side is U-level or U-log-level, and a heavy block on the V side is V-level or
V-log-level. **Side mismatch is impossible.**

## 2. Proof of (U)
**Step 0: D is bounded above on L(Y).** The hypothesis says D(w₀) < −d for every w₀ ∈ L(Y).
- Let Z be any nonterminal occurring in a derivation tree from Y, so Y ⇒* sZt. Then D(z) ≤ −d − D(st) for every
  z ∈ L(Z).
- So h(Z) := max_{z∈L(Z)} D(z) is finite. The maximum is attained, because D takes values in ½ℤ.

**Step 1: the potential identity.** For a rule r : Z → u₀Z₁u₁⋯Z_k u_k, define the slack
σ(r) := h(Z) − D(u₀⋯u_k) − Σᵢ h(Zᵢ).
- σ(r) ≥ 0: substituting maximisers for each Zᵢ gives a word of L(Z).
- σ(r) ∈ ½ℤ, so σ(r) > 0 implies σ(r) ≥ ½.
- Telescoping over a derivation tree t of w ∈ L(Z): every non-root node's h appears once as a left-hand side and once
  as a child. This gives the **exact identity h(Z) − D(w) = Σ_{nodes ν of t} σ(r_ν).**

**Step 2: every rule with left-hand side in C* has σ = 0.** Suppose instead that r has lhs ∈ C* and σ(r) ≥ ½. Write
n_r(t) for the number of uses of r in t, and let N_n be the number of words of length n in L(Y).
1. By Step 1, D(w) ≤ h(Y) − n_r(t)/2.
2. **Few uses of r are exponentially rare.** Mark r by v ∈ (0,1). At z = ½, the lower SCCs are analytic because their
   radii are > ½.
   - The least fixed point y_v of the C*-system satisfies y_v ≤ y₁ < ∞, with strict inequality at lhs(r), and so
     everywhere by irreducibility.
   - C* is nonlinear, so some Jacobian entry contains a positive multiple of some y_j and therefore strictly decreases.
     Hence J_v(y_v) ≤ J₁(y₁) entrywise, and J_v(y_v) ≠ J₁(y₁).
   - J₁ is irreducible with ρ = 1, so strict Perron–Frobenius monotonicity gives ρ(J_v(y_v)) < 1.
   - The IFT and Pringsheim then show that y_v(z) is analytic past ½: its radius ρ_v is > ½.
   - Hence, for every ε > 0, #{w ∈ L(Y)_n : n_r < εn} ≤ v^{−εn}[zⁿ]y_v(z) ≤ C·(v^{−ε}/ρ′)ⁿ for any ρ′ < ρ_v.
   - Unambiguity lets us count trees in place of words.
   - Choose ε small enough that v^{−ε}/ρ′ < 2 − δ.
3. **Many uses force negative drift, which is exponentially rare among all words.** If n_r ≥ εn, then D(w) ≤ h(Y) − εn/2.
   By Hoeffding, #{x ∈ {a,b}ⁿ : D(x) ≤ h(Y) − εn/2} ≤ 2ⁿ·exp(−ε²n/2 + O(1)).
4. Together these give N_n ≤ (2−δ′)ⁿ, so L(Y) has radius > ½. This contradicts Y ∈ C*. ∎(Step 2)

**Step 3: e = 0 is attained.** Rebuild the binary form of Lemma Bot (Y ⇒* αYβYγ through rules of C*), expanding
every other nonterminal by a maximiser.
- The tree of α w* β w* γ, with w* a maximiser of L(Y), has total slack 0:
  - C* rules have zero slack by Step 2;
  - the maximiser subtrees contribute 0 by Step 1.
- So h(Y) = D(α w* β w* γ) = d + 2h(Y), which gives h(Y) = −d.
- With w₀ = w* we get e = h(Y) + d = 0. This contradicts the hypothesis, which needs D(w₀) < −d for every w₀. ∎

**(V)** Apply (U) to the grammar of φ(x^R). This grammar is unambiguous and has the same radii, and the map sends D to −D.

**Corollary (what was conjectured).** If D is bounded above, or below, on L(Y) for a critical nonlinear Y, then every
C*-rule is balanced against a potential h, and e = 0 is attained. Combined with Step 0, every heavy block is in one of
two cases:
- D is unbounded in the direction its side needs, so e > 0 (U side) or e < 0 (V side) is available and Prop HL gives
  level directly;
- e = 0 is available, so Prop HL gives U- and V-(log-)level.
This is the precise form of "ρ′(1) = 0 from the cosh tilt". Here the zero mean is not used analytically. It is replaced
by the counting fact in Step 2.3 (Hoeffding = the cosh bound), against the rarity of avoiding a slack rule in Step 2.2.

## 3. Checks (`r15_side_checks_out.txt`)
1. **All 18,746 Polish-notation grammars** Y → f Y^{k_f} over complete prefix codes of depth ≤ 3. These are unambiguous.
   - 3,194 of them are critical, meaning Σ2^{−|f|}(1 − k_f) = 0.
   - D is bounded above in exactly 4 of these, by exact DP up to n = 40. **In all 4, D is constant**, for example
     {a:0, b:2} with D ≡ ½, and {aa:0, ab:1, ba:1, bb:2} with D ≡ 1. That is Theorem SM with h = λ(1 − k).
   - Here Step 2 is visible in closed form. Wald gives Σ2^{−|f|}D(f) = 0, and criticality gives
     Σ2^{−|f|}(k_f − 1) = 0. So the nonpositive slacks D(f) + λ(k_f − 1) sum to 0, and each must be 0.
2. **Y → bYa | bYYb | a | bbbb.** The derivation GF is critical (y = 9/16 + y/4 + y²/4 has a double root), D ≤ ½, and
   σ(bYYb) = ½ > 0. So Theorem SM says this grammar must be ambiguous **and** its language must have radius > ½.
   - It is ambiguous from n = 9.
   - Distinct words / derivations: 0.95 → 0.79 for n = 12..26, decreasing.
   - |L_n|/|L_{n−2}| ≈ 3.45 < 4. This is consistent, though pre-asymptotic.

## 4. What remains (not this lemma)
- Theorem SM settles r14 §5 item 1, apart from its sub-item "the other tape carries no infinite block". That sub-item is
  the one-sided case of r13 §5, handled by R15-C.
- Inputs used: Lemma Bot (r14) and Prop HL (r14), including its e = 0 log-level subcase, which is taken as proved there.
- Heavier tails (R15-B) and the uniform DW bound are untouched. **T8_unamb is still OPEN.**

| claim | label |
|---|---|
| Potential identity h(Z) − D(w) = Σσ | written proof |
| D bounded above on critical nonlinear SCC ⇒ all C*-rules balanced | written proof (PF strict monotonicity, IFT, Hoeffding) |
| Theorem SM: side mismatch impossible (U and V) | written proof, modulo r14 Lemma Bot / Prop HL |
| Polish-grammar exhaustive check; ambiguous critical example | numerical, consistent |
