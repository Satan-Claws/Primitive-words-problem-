# audit_foundations_bot_cites.md — R17b gated audit: r14 Lemma Bot / PC / HL, r15 Lemma ST, and the cited theorems

No scripts. Every check here is a proof re-derivation or a comparison with the source text.
Sources read:
- Banderier–Drmota (B–D), DMTCS proc. AS (FPSAC 2013) 1065–1076 (dmtcs.episciences.org/2366), and the long preprint
  "Coefficients of algebraic functions: formulae and asymptotics" (dmg.tuwien.ac.at/drmota/Alg-short.pdf).
- Denisov–Wachtel (DW), "Random walks in cones", arXiv:1110.1254 = Ann. Probab. 43(3) 2015.
- DLW in its standard published forms (Flajolet–Sedgewick Thm VII.6; Drmota, *Random Trees*, Thm 2.33).

## Verdict
**No fatal flaw.** Every item **SURVIVES**, with the caveats below. T8_unamb's critical path does **not** use DW.
Its use of DLW can be replaced by an elementary one-line bound. B–D is used within its hypotheses, but the right
citation for the residue-class statement is **Thm 4** (DMTCS numbering), not Thm 3.

| item | verdict |
|---|---|
| r14 Lemma Bot | SURVIVES (caveats B1, B2) |
| r14 Lemma PC | SURVIVES (re-derived) |
| r14 Prop HL | SURVIVES (caveat H1) |
| r15 Lemma ST(i) | SURVIVES. ST(ii) is a heuristic mechanism and nothing on the critical path uses it |
| DLW citation | SURVIVES. Its hypotheses fail as written in r9 Lemma F, but the conclusion holds elementarily (D1) |
| B–D citation | SURVIVES. Hypotheses are met. Cite Thm 4 for the per-residue-class asymptotics (BD1–BD3) |
| DW citation | SURVIVES as "off critical path". The *uniform* bound attributed to DW 2015 is **not** in the paper in that form (W1) |

## 1. r14 Lemma Bot
Setting: B is heavy, meaning μ(B) = B(½) < ∞ and Σ|x|2^{−|x|} = ∞. The grammar is unambiguous and reduced, so every
nonterminal's GF equals its language GF and has radius ≥ ½.

The argument, step by step:
- **Radius ½.** A radius > ½ would make the mean finite. ✓
- **C\* exists.** The set of SCCs with radius exactly ½ that are reachable from B is non-empty, because B's own SCC is
  in it. Take a minimal element C\*. Every SCC strictly below C\* has radius ≥ ½ and ≠ ½, so its radius is > ½. ✓
- **C\* is non-trivial (B1, omitted in r14).** A trivial SCC has a polynomial GF in z and the lower GFs, so its radius
  is > ½. Hence C\* is non-trivial and the linear/nonlinear dichotomy applies.
- **Linear C\*.** The lower data are analytic past ½.
  - ρ(M(½)) < 1 would give Y = (I−M)⁻¹A analytic at ½, which contradicts Pringsheim. So ρ(M(½)) ≥ 1.
  - If Y(½) were finite, let w > 0 be the left Perron vector of the irreducible M(½), with wM = ρw and ρ ≥ 1.
    Then 0 ≥ w(I−M)Y = wA > 0. Here A ≠ 0 because a productive SCC has an exit rule.
  - So μ(Y) = ∞. The injection x ↦ sxt gives μ(B) ≥ 2^{−|st|}μ(Y) = ∞, a contradiction. ✓
  - (r14 says "pole". The Perron argument above is the rigorous form, and it is exactly ST(i).)
- **Nonlinear C\*.** Some rule has two C\*-occurrences. Strong connectivity and productivity then give
  Y ⇒⁺ αYβYγ with α, β, γ terminal words. ✓
- **B2 (bonus, strengthens the chain).** The same form gives μ(Y) ≤ 2^{|αβγ|}, by the bound in D1 below. So C\* has
  finite value at ½ without citing DLW.

## 2. r14 Lemma PC and Prop HL
I re-derived both, region by region. This agrees with audit_t8 §1.
- **PC(U).** In the copies of y, the shift is iD(v) + (j−1)D(y) ≥ (i−1)(D(v)+D(y)) + D(v) ≥ 0. In z, it is
  i(D(v)+D(y)) ≥ 0.
- **PC(V).** φ∘reverse maps (v, y) to (φ(y^R), φ(v^R)) and negates drifts. ✓
- **HL drift.** D(T_{k+1}) = 2D(T_k) + d gives D(T_k) = 2^k e − d. ✓
- **HL cases.**
  - e > 0: the cycle (αT_kβ, γ). D(v) → ∞ and the total is 2^k e ≥ 0, so PC(U).
  - e < 0: the cycle (α, βT_kγ), so PC(V).
  - e = 0 with D(α) ≥ 0, or with D(γ) ≤ 0: the total is 0, so U and V both hold.
  - The remaining case: depth(T_{k+1}) ≤ depth(T_k) + |α| + |β| + |d|, and the suffix bound is symmetric. ✓
- **H1 (cosmetic).** |T_k| ≍ 2^k needs w₀ ≠ ε or αβγ ≠ ε. Choose w₀ ≠ ε. This is always possible, since L(Y) is
  infinite. If Y ⇒⁺ YY with Y ⇒ ε, the grammar would be ambiguous anyway.

## 3. r15 Lemma ST
**(i)** μ(B) < ∞ makes every reachable nonterminal finite at ½, so M(½) and A(½) are finite. Then:
- Y = A + MY holds at ½, by monotone convergence;
- M(½) is irreducible, and A(½) ≠ 0;
- if ρ = 1, then w(I−M)Y = 0 ≠ wA. ✓
- (The same argument excludes ρ > 1.)

**(ii)** "Exponent 2^{−k} ⇐ k stacked critical nonlinear SCCs" matches the B–D proof mechanism, and B–D Example 1 is
exactly such a stack. It is labelled as checked numerically, not proved. **No T8 link uses (ii).** Only (i) and the
B–D exponent set are used.

## 4. Cited theorems

### (a) Drmota–Lalley–Woods
**Statement** (F–S Thm VII.6; Drmota *Random Trees* Thm 2.33):
- Hypotheses on y = Φ(z, y):
  - Φ is polynomial (F–S), or analytic around the relevant point (Drmota), with non-negative coefficients;
  - the system is proper/well-posed: Φ(0,0) = 0, and Φ_y(0,0) is nilpotent or has ρ < 1;
  - it is **nonlinear** and **strongly connected** (irreducible);
  - Drmota's version also needs a solution (z₀, y₀) of y = Φ, det(I − Φ_y) = 0 inside the analyticity domain of Φ.
- Conclusions:
  - all components share one radius ρ;
  - y_j = a_j − b_j√(1 − z/ρ) + …, with a_j finite and b_j > 0;
  - the other dominant singularities are ρ·(roots of unity);
  - if the system is aperiodic, the coefficients are ~ c ρ^{−n} n^{−3/2}.

**Where the campaign uses it:**
1. r9 Lemma F(a): "a nonlinear SCC with finite inputs has a finite value at its singularity". audit_t8 §4 step 1
   depends on this.
2. r15_side SM Step 2.2: J₁(y(½)) is irreducible with ρ = 1 at the critical C\*.
3. r16 lists it for Lemma ST and "reduction rounds".

**Hypotheses.**
- **Use 2 (C\* from Lemma Bot).** Met. The lower SCCs have radius > ½, so after substituting them C\* is a strongly
  connected nonlinear system with coefficients analytic past ½ (Drmota's analytic version). The facts used also follow
  directly:
  - y(½) is finite, by D1;
  - ρ(J) ≤ 1, as a limit of values < 1;
  - ρ(J) = 1, since otherwise IFT plus Pringsheim give radius > ½.
- **Use 1 (r9 Lemma F).** **Not met as written.** "Finite inputs" means μ < ∞ for the lower components, and those may
  have radius exactly ½: heavy blocks are exactly this. Then Φ is not analytic at ½, and DLW does not apply.
  - **D1 (repair, elementary).** In a nonlinear SCC, take Y ⇒⁺ αYβYγ. Grafting is injective on trees, and trees
    correspond to words by unambiguity. So y(z) ≥ z^{|αβγ|}y(z)² coefficientwise.
  - For z < ½, y(z) is finite and positive, so y(z) ≤ z^{−|αβγ|}. Letting z ↑ ½ gives μ(Y) ≤ 2^{|αβγ|} < ∞.
  - So Lemma F(a) holds **without DLW** and without any analyticity of the inputs.
  - Lemma F(b), ρ(M(½)) = 1: the entries of M are left-continuous at ½ by monotone convergence, so ρ > 1 would give
    y = ∞ before ½. ✓
- **Verdict: SURVIVES.** Replace the DLW citation in r9 Lemma F by D1.

### (b) Banderier–Drmota
Verbatim, from the DMTCS 2013 text:
> **Theorem 3** (dyadic critical exponents for N-algebraic function). The critical exponent of an N-algebraic (or
> even R₊-algebraic) function is either 2^{−k} for some k ≥ 1 or −m2^{−k} for some m ≥ 1 and some k ≥ 0. If f₁(z) is
> aperiodic […] f_n ∼ Aρ^{−n}n^{−1−α} […] In the general (non-aperiodic) case, we have to distinguish between residue
> classes but the asymptotics are still of the same form.
>
> **Theorem 4.** Let f₁(z) be the power series expansion of a well defined N-algebraic (or even R₊-algebraic) system
> y = P(z, y). Then there is an integer M ≥ 1 such that for every j ∈ {0,…,M−1} we either have f_n = 0 for all (but
> finitely many) n ≡ j mod M or there exist positive numbers A_j, ρ_j and β_j that is either −1−2^{−k} for some k ≥ 1
> or −1+m2^{−k} for some m ≥ 1 and some k ≥ 0 such that f_n ∼ A_j ρ_j^{−n} n^{β_j} (n → ∞, n ≡ j mod M).

- **Long-version hypotheses** (Thm 3 there): a "well posed positive polynomial system". That means:
  - P has non-negative coefficients;
  - P(0, 0) = 0;
  - ρ(P_y(0, 0)) < 1;
  - no component is a polynomial.
- **Non-strongly-connected systems are explicitly covered.** That is the point of the paper; see their Fig. 1.
- The convention is f ∼ c(1 − z/ρ)^α. α = 2^{−k} is the finite-value branch.

**Where the campaign uses it, and whether the hypotheses are met:**

| use | location | hypotheses met? |
|---|---|---|
| exponent −1 never occurs, μ < ∞ ⟺ o(2ⁿ/n) per class | r9 Thm M(ii) | Yes (Thm 4; also Puiseux, so no log) |
| finite-μ block at radius ½ is ~n^{−1−2^{−k}}·2ⁿ per class | r15 §1; r16 PR2⁺ step 1; r17_oh_level §0 | Yes (Thm 4) |
| F̄(y) = O(y^{−β₀}) (C4a) | PR2⁺ step 1, OH | Yes. Upper bound only, by a union bound over finitely many blocks and classes |
| lower tail P(\|u\| > y) ≥ c y^{−β₀} for the heaviest U block (C4b) | r17_oh_level step 4 | Yes. Take a class j with ρ_j = ½ and β_j = −1−β₀: the tail is ≥ Σ_{n>y, n≡j} A_j n^{−1−β₀}/2 ≍ y^{−β₀} |
| finite mean ⇒ radius > ½ (C4c) | OH step 4, PR2⁺ | Yes. A class with ρ_j = ½ has β_j ≥ −3/2 > −2, so the mean diverges |

**Caveats.**
- **BD1.** The per-residue-class statement, including ρ_j that may differ by class, is **Thm 4** (DMTCS) and is only
  summarised in Thm 3. Cite "B–D Thms 3–4". The CPC 2015 numbering was not checked.
- **BD2.** The block GF must be put in well-posed form: P(0,0) = 0, ρ(P_y(0,0)) < 1, finite blocks removed. For an
  unambiguous grammar this is the standard ε-/unit-rule elimination, which preserves unambiguity; a unit cycle would
  itself be ambiguous. This is routine but not written anywhere.
- **BD3.** The theorem is used as a black box. Its completeness for all non-strongly-connected positive systems (the
  r14 caveat) is exactly what the paper claims. I did not re-check its proof.
- **Verdict: SURVIVES.**

### (c) Denisov–Wachtel 2015
**Hypotheses, verbatim:**
- normalisation: EX_j = 0, EX_j² = 1, cov(X_i, X_j) = 0;
- moments: E|X|^α < ∞ with α = p if p > 2, and some α > 2 if p ≤ 2;
- cone conditions as in §1.1 (a 2-D wedge qualifies).

**Theorem 1:** "P(τ_x > n) ∼ κV(x)n^{−p/2}, x ∈ K", **pointwise** in x. Lemma 13(b): V(x) ≤ C(1 + |x|^p).
**Lemma 20, (39):** "P(τ_y > n) ≤ C|y|^p/n^{p/2} uniformly in y ∈ K_{n,ε}". Here
K_{n,ε} = {dist(x, ∂K) ≥ n^{1/2−ε}}, so it covers only points *far from the boundary*.

**Applied to our walk:**
- In 2-D, p = π/θ. For the Valley wedge (θ = 3π/4), p = 4/3 and the survival exponent is 2/3. ✓
- (A, B) has independent ±½ coordinates, so the covariance is ¼I. That is isotropic, so the angle is preserved. ✓
- The steps are bounded, so all moments exist. ✓

**Uses:**
- r13 Lemma K / PR2 (fixed start near the apex): **Theorem 1 suffices.** Finitely many starts. ✓
- r14 PR2ˡᵒᵍ step 3, r15 Lemma QW step 2, r15_onesided Lemmas CM/J and PR1s, audit_r16: all use
  "P_x(τ > m) ≤ C(1+|x|)^p m^{−p/2} **for all x**".

**W1.** That uniform-in-x form is **not stated in DW 2015**. The paper has only pointwise asymptotics and (39) on
K_{n,ε}, and r14's attribution "uniform upper bound accompanying Thm 1" is inaccurate.
- The bound is very plausible: it follows the DW proof scheme (Lemma 14 + (39) + V ≤ C(1+|x|^p)).
- As a citation, though, it is unsupported, and the results that rely on it stay "modulo an uncited lemma".

**Not fatal for T8_unamb.** The assembly in audit_t8 §4 uses PR2⁺ (Q_n(C) count, ballot only) and Thm OH (Lemma D,
ballot only). It states that PR1, PR1s, PR2 and PR2^β are subsumed. SM is elementary; r16's remark that "DW is used
by SM" is wrong, since SM uses Perron–Frobenius, IFT and Hoeffding.
**Verdict: SURVIVES (off critical path). Fix the attribution if PR1s or QW are ever reused.**

## 5. Net effect on audit_t8 §4
The links "r14 Lemma Bot" and "cited DLW / B–D" are now gated:
- Lemma Bot is correct (add B1);
- DLW can be dropped from Lemma F via D1;
- B–D holds within its hypotheses (cite Thm 4; well-posed normalisation BD2).

Still **not** audited here: r9 Lemma Rn and Cor H, the r10 §2 pair model, and the renewal theorem citation.
